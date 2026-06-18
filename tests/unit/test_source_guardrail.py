"""Unit tests for the per-source license guardrail."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from guardrail import (
    GuardrailResult,
    SourceEntry,
    Violation,
    check_registry,
    check_source,
    load_registry,
)
from guardrail.source_guardrail import parse_credited_keys

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "sources" / "registry.json"
CREDITS_PATH = REPO_ROOT / "CREDITS.md"

ALLOWED = frozenset({"market-data", "physical-infrastructure", "natural-hazard"})
LICENSES = frozenset({"CC-BY-4.0", "US-Gov-public-domain"})


def _entry(**overrides: object) -> SourceEntry:
    base: dict[str, object] = {
        "key": "demo",
        "endpoint": "/api/x",
        "upstream_source": "Demo",
        "license": "CC-BY-4.0",
        "attribution": "Data: Demo",
        "content_class": "market-data",
        "surfaced": True,
        "risk_flags": (),
        "synthesis_cautions": (),
    }
    base.update(overrides)
    return SourceEntry(**base)  # type: ignore[arg-type]


def _check(entry: SourceEntry, credited: frozenset[str] = frozenset({"demo"})) -> list[Violation]:
    return check_source(
        entry,
        allowed_content_classes=ALLOWED,
        license_allowlist=LICENSES,
        credited_keys=credited,
    )


# --- the live registry must always pass (this is the standing guardrail itself) ---------


def test_live_registry_passes() -> None:
    result = check_registry(REGISTRY_PATH, CREDITS_PATH)
    assert result.ok, [str(v) for v in result.violations]
    # 6 surfaced after the W26 multi-theme expansion: 4 energy + earthquakes + prediction-markets.
    assert result.surfaced == 6
    assert result.checked == 9


def test_live_registry_loads_with_policy() -> None:
    registry = load_registry(REGISTRY_PATH)
    assert "market-data" in registry.allowed_content_classes
    assert "CC-BY-4.0" in registry.license_allowlist
    assert len(registry.sources) == 9


# --- a clean surfaced source passes -----------------------------------------------------


def test_clean_source_has_no_violations() -> None:
    assert _check(_entry()) == []


# --- each hard rule fires ---------------------------------------------------------------


def test_missing_license_blocks() -> None:
    rules = {v.rule for v in _check(_entry(license=""))}
    assert "missing-license" in rules


def test_unrecognised_license_blocks() -> None:
    rules = {v.rule for v in _check(_entry(license="WTFPL"))}
    assert "unrecognised-license" in rules


def test_missing_attribution_blocks() -> None:
    rules = {v.rule for v in _check(_entry(attribution=""))}
    assert "missing-attribution" in rules


def test_uncredited_surfaced_source_blocks() -> None:
    rules = {v.rule for v in _check(_entry(), credited=frozenset())}
    assert "missing-credit" in rules


def test_denied_content_class_blocks() -> None:
    rules = {v.rule for v in _check(_entry(content_class="investment-advice"))}
    assert "denied-content-class" in rules


def test_denied_risk_flag_blocks() -> None:
    rules = {v.rule for v in _check(_entry(risk_flags=("political-opinion",)))}
    assert "denied-risk-flag" in rules


def test_unlisted_content_class_blocks() -> None:
    rules = {v.rule for v in _check(_entry(content_class="weather-forecast"))}
    assert "unlisted-content-class" in rules


# --- staged (unsurfaced) sources are exempt from hard rules -----------------------------


def test_unsurfaced_denied_source_is_allowed() -> None:
    # A registered-but-not-surfaced conflict feed (denied class, unknown license) must NOT
    # block the build — it is honestly staged, awaiting review.
    staged = _entry(
        key="conflict",
        content_class="political-opinion",
        risk_flags=("political-opinion", "safety-prediction"),
        license="unknown",
        attribution="",
        surfaced=False,
    )
    assert _check(staged, credited=frozenset()) == []


def test_surfacing_a_denied_source_would_block() -> None:
    # Flip the same staged source to surfaced -> the guardrail catches it.
    surfaced = _entry(
        key="conflict",
        content_class="political-opinion",
        risk_flags=("political-opinion",),
        license="unknown",
        attribution="",
        surfaced=True,
    )
    rules = {v.rule for v in _check(surfaced, credited=frozenset())}
    assert {"denied-content-class", "denied-risk-flag", "unrecognised-license"} <= rules


# --- parsing helpers --------------------------------------------------------------------


def test_parse_credited_keys_extracts_backticked_keys() -> None:
    text = "## x\n- `alpha` — Foo — CC-BY-4.0\n- `beta` — Bar\n- no key here\n"
    assert parse_credited_keys(text) == frozenset({"alpha", "beta"})


def test_from_dict_rejects_missing_required_field() -> None:
    with pytest.raises(ValueError, match="missing required field"):
        SourceEntry.from_dict({"endpoint": "/x", "content_class": "market-data"})


def test_from_dict_coerces_lists_to_tuples() -> None:
    entry = SourceEntry.from_dict(
        {
            "key": "k",
            "endpoint": "/e",
            "content_class": "market-data",
            "risk_flags": ["a", "b"],
            "surfaced": True,
        }
    )
    assert entry.risk_flags == ("a", "b")
    assert entry.surfaced is True


def test_violation_str_is_readable() -> None:
    assert (
        str(Violation("k", "missing-license", "no license")) == "[k] missing-license: no license"
    )


def test_result_ok_property() -> None:
    assert GuardrailResult().ok is True
    assert GuardrailResult(violations=[Violation("k", "r", "d")]).ok is False


def test_check_registry_without_credits_file(tmp_path: Path) -> None:
    # registry with one surfaced source, no CREDITS.md -> missing-credit violation.
    reg = {
        "content_class_policy": {"allowed": ["market-data"]},
        "license_allowlist": ["CC-BY-4.0"],
        "sources": [
            {
                "key": "k",
                "endpoint": "/e",
                "upstream_source": "U",
                "license": "CC-BY-4.0",
                "attribution": "Data: U",
                "content_class": "market-data",
                "surfaced": True,
            }
        ],
    }
    registry_file = tmp_path / "registry.json"
    registry_file.write_text(json.dumps(reg), encoding="utf-8")
    result = check_registry(registry_file, tmp_path / "CREDITS.md")
    assert not result.ok
    assert any(v.rule == "missing-credit" for v in result.violations)
