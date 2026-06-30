"""Tests for the public-flip secret-scan gate (scripts/scan_secrets.py).

The load-bearing guarantee: the C1 gate has TEETH. It must (a) detect every
credential class it claims to — real Anthropic/AWS/GitHub keys, JWTs, private-key
blocks, Slack webhooks, DB URLs with embedded creds — and (b) NOT false-positive
on the documentation placeholders that legitimately live in this repo
(``sk-ant-...``, ``your-anon-key``, ``user:password@host``). A gate that passes
because it can't see anything is worse than no gate, so both halves get a
regression test.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "scan_secrets", _REPO_ROOT / "scripts" / "scan_secrets.py"
)
assert _spec and _spec.loader
scan = importlib.util.module_from_spec(_spec)
# Register before exec: the module defines frozen dataclasses, and on Python
# 3.14 dataclasses resolves field annotations against sys.modules[__module__].
sys.modules["scan_secrets"] = scan
_spec.loader.exec_module(scan)


def _rules(text: str, path: str = "config.py") -> list[str]:
    return [f.rule for f in scan._scan_text(text, "test", path)]


# --- detection (the gate must catch real secrets) ---------------------------


def test_detects_real_anthropic_key() -> None:
    key = "sk-ant-api03-" + "AbCdEf0123456789" * 2 + "ZZ"
    assert "anthropic-api-key" in _rules(f"ANTHROPIC_API_KEY={key}")


def test_detects_real_aws_access_key() -> None:
    # canonical-format but NOT the "...EXAMPLE" string (which is allowlisted)
    assert "aws-access-key-id" in _rules("aws_key = AKIA1B2C3D4E5F6G7H8I")


def test_detects_github_pat() -> None:
    assert "github-pat" in _rules("token: ghp_" + "a" * 36)


def test_detects_private_key_block() -> None:
    assert "private-key-block" in _rules("-----BEGIN RSA PRIVATE KEY-----")


def test_detects_jwt() -> None:
    jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcDEFghiJKLmnoPQR"
    assert "jwt" in _rules(jwt)


def test_detects_slack_webhook() -> None:
    hook = "https://hooks.slack.com/services/T01ABCDEF/B02GHIJKL/abcdef0123456789ABCD"
    assert "slack-webhook" in _rules(hook)


def test_detects_db_url_with_credentials() -> None:
    url = "DATABASE_URL=postgresql://admin:Sup3rS3cretPw@db.prod.internal:5432/app"
    assert "db-url-credentials" in _rules(url)


def test_detects_generic_assigned_secret_in_code() -> None:
    assert "generic-assigned-secret" in _rules('api_key = "ZsupersecretValue123456"')


# --- allowlist (the gate must not cry wolf on placeholders) -----------------


def test_ignores_anthropic_placeholder() -> None:
    assert _rules("ANTHROPIC_API_KEY=sk-ant-...") == []


def test_ignores_example_db_url() -> None:
    assert _rules("DATABASE_URL=postgresql://user:password@host:5432/dbname") == []


def test_ignores_your_anon_key_placeholder() -> None:
    assert _rules("SUPABASE_KEY=your-anon-key") == []


def test_ignores_aws_canonical_example_key() -> None:
    # AKIAIOSFODNN7EXAMPLE is AWS's own docs key — "example" allowlists it.
    assert _rules("AKIAIOSFODNN7EXAMPLE") == []


def test_generic_rule_muted_in_markdown_docs() -> None:
    # architecture docs name "api_key = ..." illustratively; only strong
    # prefixed rules fire in .md prose, never the entropy-based generic one.
    txt = 'api_key = "ZsupersecretValue123456"'
    assert _rules(txt, path="docs/architecture.md") == []
    assert "generic-assigned-secret" in _rules(txt, path="app/config.py")


def test_strong_rules_still_fire_in_docs() -> None:
    # a REAL key prefix in a doc is still a leak — only the generic rule is muted.
    key = "sk-ant-api03-" + "AbCdEf0123456789" * 2 + "ZZ"
    assert "anthropic-api-key" in _rules(key, path="docs/leak.md")
