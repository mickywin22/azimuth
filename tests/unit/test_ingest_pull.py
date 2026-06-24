"""Unit tests for the registry-driven L1 ingest.

The central contract under test: the ``license`` (and endpoint + attribution) in every
L1 note is read straight from ``sources/registry.json`` — ingest and the source-guardrail
never drift, and a surfaced source that fails the guardrail produces no L1 note.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import pytest

from guardrail import SourceEntry, load_registry, parse_credited_keys
from ingest import eligible_sources, frontmatter_for, pull, render_note

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = REPO_ROOT / "sources" / "registry.json"
CREDITS_PATH = REPO_ROOT / "CREDITS.md"

FIXED = datetime(2026, 6, 10, 9, 30, 0, tzinfo=UTC)


class DictFetcher:
    """Returns a canned payload per endpoint; raises for endpoints not in the map."""

    def __init__(self, payloads: dict[str, object]) -> None:
        self._payloads = payloads

    def fetch(self, endpoint: str) -> object:
        if endpoint not in self._payloads:
            raise RuntimeError(f"no payload for {endpoint}")
        return self._payloads[endpoint]


def _entry(**overrides: object) -> SourceEntry:
    base: dict[str, object] = {
        "key": "natural-gas-storage-eu",
        "endpoint": "/api/economic/v1/get-nat-gas-storage",
        "upstream_source": "GIE AGSI+ (Gas Infrastructure Europe)",
        "license": "CC-BY-4.0",
        "attribution": "Data: GIE AGSI+ via WorldMonitor (api.worldmonitor.app)",
        "content_class": "physical-infrastructure",
        "surfaced": True,
    }
    base.update(overrides)
    return SourceEntry.from_dict(base)


# --- frontmatter / single-source-of-truth -----------------------------------------


def test_frontmatter_license_comes_from_registry_entry() -> None:
    entry = _entry(license="CC-BY-4.0", attribution="Data: X")
    fm = frontmatter_for(entry, FIXED)
    assert fm["license"] == "CC-BY-4.0"
    assert fm["attribution"] == "Data: X"
    assert fm["endpoint"] == entry.endpoint
    assert fm["source_key"] == entry.key


def test_frontmatter_retrieved_is_utc_iso() -> None:
    fm = frontmatter_for(_entry(), FIXED)
    assert fm["retrieved"] == "2026-06-10T09:30:00Z"


def test_frontmatter_declares_l1_source_type() -> None:
    """Every L1 note carries the OKF layer tag ``type: L1-source`` (OKF v0.1 contract)."""
    fm = frontmatter_for(_entry(), FIXED)
    assert fm["type"] == "L1-source"


def test_note_renders_type_l1_source_in_frontmatter() -> None:
    note = render_note(_entry(), [{"a": 1}], FIXED)
    assert 'type: "L1-source"' in note


def test_note_carries_registry_license_verbatim() -> None:
    entry = _entry(license="US-Gov-public-domain")
    note = render_note(entry, [{"a": 1}], FIXED)
    assert 'license: "US-Gov-public-domain"' in note


@pytest.mark.parametrize("real_entry", load_registry(REGISTRY_PATH).sources)
def test_every_registry_source_frontmatter_matches_registry(real_entry: SourceEntry) -> None:
    """For the live registry: the note's license/endpoint/attribution equal the entry."""
    fm = frontmatter_for(real_entry, FIXED)
    assert fm["license"] == real_entry.license
    assert fm["endpoint"] == real_entry.endpoint
    assert fm["attribution"] == real_entry.attribution


# --- payload transform (verbatim, zero synthesis) ---------------------------------


def test_list_of_objects_renders_markdown_table() -> None:
    payload = [{"date": "2026-06-09", "pct": 71.2}, {"date": "2026-06-10", "pct": 71.5}]
    note = render_note(_entry(), payload, FIXED)
    assert "| date | pct |" in note
    assert "| 2026-06-09 | 71.2 |" in note


def test_single_object_renders_kv_table() -> None:
    note = render_note(_entry(), {"latest": 71.5, "unit": "%"}, FIXED)
    assert "| field | value |" in note
    assert "| latest | 71.5 |" in note


def test_scalar_payload_renders_json_block() -> None:
    note = render_note(_entry(), 42, FIXED)
    assert "```json" in note
    assert "42" in note


def test_pipe_in_value_is_escaped() -> None:
    note = render_note(_entry(), [{"note": "a|b"}], FIXED)
    assert r"a\|b" in note


# --- eligibility = surfaced AND passes guardrail ----------------------------------


def test_eligible_excludes_unsurfaced() -> None:
    from guardrail import Registry

    reg = Registry(
        allowed_content_classes=frozenset({"physical-infrastructure"}),
        license_allowlist=frozenset({"CC-BY-4.0"}),
        sources=(_entry(surfaced=False),),
    )
    assert eligible_sources(reg, frozenset({"natural-gas-storage-eu"})) == []


def test_eligible_excludes_surfaced_but_unlicensed() -> None:
    from guardrail import Registry

    reg = Registry(
        allowed_content_classes=frozenset({"physical-infrastructure"}),
        license_allowlist=frozenset({"CC-BY-4.0"}),
        sources=(_entry(license=""),),  # surfaced but no license
    )
    assert eligible_sources(reg, frozenset({"natural-gas-storage-eu"})) == []


def test_eligible_includes_compliant_surfaced() -> None:
    from guardrail import Registry

    reg = Registry(
        allowed_content_classes=frozenset({"physical-infrastructure"}),
        license_allowlist=frozenset({"CC-BY-4.0"}),
        sources=(_entry(),),
    )
    got = eligible_sources(reg, frozenset({"natural-gas-storage-eu"}))
    assert [e.key for e in got] == ["natural-gas-storage-eu"]


# --- pull() end to end against the live registry ----------------------------------


def test_pull_writes_notes_for_surfaced_sources(tmp_path: Path) -> None:
    registry = load_registry(REGISTRY_PATH)
    credited = parse_credited_keys(CREDITS_PATH.read_text(encoding="utf-8"))
    eligible = eligible_sources(registry, credited)
    fetcher = DictFetcher({e.endpoint: [{"v": 1}] for e in eligible})

    outcome = pull(
        registry_path=REGISTRY_PATH,
        credits_path=CREDITS_PATH,
        fetcher=fetcher,
        out_dir=tmp_path,
        now=FIXED,
    )

    assert outcome.ok
    assert len(outcome.written) == len(eligible)
    day_dir = tmp_path / "2026-06-10"
    for note in outcome.written:
        written_file = tmp_path / note.relative_path
        assert written_file.exists()
        text = written_file.read_text(encoding="utf-8")
        entry = next(e for e in eligible if e.key == note.source_key)
        assert f'license: "{entry.license}"' in text
    # unsurfaced sources must not produce notes
    assert not (day_dir / "conflict-events-acled.md").exists()


def test_pull_degraded_mode_skips_failed_fetch(tmp_path: Path) -> None:
    registry = load_registry(REGISTRY_PATH)
    credited = parse_credited_keys(CREDITS_PATH.read_text(encoding="utf-8"))
    eligible = eligible_sources(registry, credited)
    assert len(eligible) >= 2
    # Serve everything except the first eligible endpoint -> it must error, others write.
    failing = eligible[0]
    fetcher = DictFetcher({e.endpoint: [{"v": 1}] for e in eligible if e.key != failing.key})

    outcome = pull(
        registry_path=REGISTRY_PATH,
        credits_path=CREDITS_PATH,
        fetcher=fetcher,
        out_dir=tmp_path,
        now=FIXED,
    )

    assert not outcome.ok  # one fetch errored
    assert failing.key in outcome.errors
    assert len(outcome.written) == len(eligible) - 1
    assert not (tmp_path / "2026-06-10" / f"{failing.key}.md").exists()


def test_pull_dry_run_writes_nothing(tmp_path: Path) -> None:
    registry = load_registry(REGISTRY_PATH)
    credited = parse_credited_keys(CREDITS_PATH.read_text(encoding="utf-8"))
    eligible = eligible_sources(registry, credited)
    fetcher = DictFetcher({e.endpoint: [{"v": 1}] for e in eligible})

    outcome = pull(
        registry_path=REGISTRY_PATH,
        credits_path=CREDITS_PATH,
        fetcher=fetcher,
        out_dir=tmp_path,
        now=FIXED,
        write=False,
    )

    assert len(outcome.written) == len(eligible)
    assert list(tmp_path.iterdir()) == []  # nothing on disk


def test_note_frontmatter_is_parseable_block() -> None:
    note = render_note(_entry(), [{"v": 1}], FIXED)
    match = re.match(r"^---\n(.*?)\n---\n", note, re.DOTALL)
    assert match is not None
    keys = {line.split(":", 1)[0] for line in match.group(1).splitlines()}
    assert keys == {"type", "source", "source_key", "endpoint", "retrieved", "license", "attribution"}
