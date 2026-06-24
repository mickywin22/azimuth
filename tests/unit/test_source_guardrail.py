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

ALLOWED = frozenset(
    {
        "market-data",
        "physical-infrastructure",
        "natural-hazard",
        "conflict-event-record",
        "vessel-position",
        "flight-track",
    }
)
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
    # 26 surfaced after the W26 full-universe audit (docs/sources/worldmonitor-channel-audit.md):
    # the original 9 (4 energy + earthquakes + prediction-markets + 3 climate-signals) plus 17
    # free-licensed factual channels surfaced from the full ~34-family WorldMonitor universe —
    # wildfire / thermal / natural-events / radiation, conflict-events-ucdp, maritime-navwarnings,
    # cyber-threats, sanctions-designations, disease-outbreaks, crypto-quotes,
    # world-bank-indicators, tariff-trends, orbital-satellites, consumer-prices, displacement-flows,
    # internet-outages, chokepoint-status. 12 stay held (license / news-filter / derived-composite),
    # each with a surfaced_reason.
    assert result.surfaced == 26
    assert result.checked == 38


def test_live_registry_loads_with_policy() -> None:
    registry = load_registry(REGISTRY_PATH)
    assert "market-data" in registry.allowed_content_classes
    assert "CC-BY-4.0" in registry.license_allowlist
    assert "climate-observation" in registry.allowed_content_classes
    # W26 full-universe audit added six observed-fact classes for the newly-surfaced channels.
    assert "sanctions-record" in registry.allowed_content_classes
    assert "health-event" in registry.allowed_content_classes
    assert "orbital-position" in registry.allowed_content_classes
    assert len(registry.sources) == 38


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
    violations = _check(_entry(content_class="political-propaganda"))
    rules = {v.rule for v in violations}
    assert "denied-content-class" in rules
    # the deny is tagged EDITORIAL (non-factual content), never license.
    assert any(v.rule == "denied-content-class" and v.category == "editorial" for v in violations)


def test_denied_risk_flag_blocks() -> None:
    rules = {v.rule for v in _check(_entry(risk_flags=("opinion-advocacy",)))}
    assert "denied-risk-flag" in rules


def test_unlisted_content_class_blocks() -> None:
    # forecast is a benchmark foil, not an allowed observed-fact channel.
    violations = _check(_entry(content_class="forecast"))
    rules = {v.rule for v in violations}
    assert "unlisted-content-class" in rules
    assert any(v.rule == "unlisted-content-class" and v.category == "policy" for v in violations)


# --- fact-vs-propaganda line (Michael 2026-06-24) ---------------------------------------


def test_sensitive_but_factual_clean_license_passes() -> None:
    # A conflict EVENT record on a sensitive topic, with a clean license, must PASS — under
    # the fact-vs-propaganda line, sensitivity is never a deny reason.
    entry = _entry(
        key="conflict",
        content_class="conflict-event-record",
        risk_flags=("sensitive-topic",),
        license="CC-BY-4.0",
    )
    assert _check(entry, credited=frozenset({"conflict"})) == []


def test_factual_channel_restricted_license_blocks_on_license_only() -> None:
    # Same factual channel, but an unrecognised license -> held on LICENSE grounds, NOT
    # editorial. No denied-content-class fires; the only block is categorised license.
    entry = _entry(
        key="conflict",
        content_class="conflict-event-record",
        risk_flags=("sensitive-topic",),
        license="proprietary-feed",
    )
    violations = _check(entry, credited=frozenset({"conflict"}))
    rules = {v.rule for v in violations}
    assert "unrecognised-license" in rules
    assert "denied-content-class" not in rules  # sensitivity is not editorial
    assert all(v.category != "editorial" for v in violations)
    assert any(v.rule == "unrecognised-license" and v.category == "license" for v in violations)


def test_propaganda_blocks_on_editorial() -> None:
    # A clean-licensed channel that is non-factual (opinion/advocacy) IS an editorial deny.
    entry = _entry(key="oped", content_class="opinion-advocacy", license="CC-BY-4.0")
    violations = _check(entry, credited=frozenset({"oped"}))
    assert any(v.rule == "denied-content-class" and v.category == "editorial" for v in violations)


# --- staged (unsurfaced) sources are exempt from hard rules -----------------------------


def test_unsurfaced_denied_source_is_allowed() -> None:
    # A registered-but-not-surfaced propaganda feed (denied class, unknown license) must NOT
    # block the build — it is honestly staged, awaiting review.
    staged = _entry(
        key="oped",
        content_class="political-propaganda",
        risk_flags=("political-propaganda", "safety-position"),
        license="unknown",
        attribution="",
        surfaced=False,
    )
    assert _check(staged, credited=frozenset()) == []


def test_surfacing_a_denied_source_would_block() -> None:
    # Flip the same staged source to surfaced -> the guardrail catches it.
    surfaced = _entry(
        key="oped",
        content_class="political-propaganda",
        risk_flags=("political-propaganda",),
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
        str(Violation("k", "missing-license", "no license", category="license"))
        == "[k] missing-license (license): no license"
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
