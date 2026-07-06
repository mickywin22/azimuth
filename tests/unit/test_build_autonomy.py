"""Tests for the autonomy-counter build (scripts/build_autonomy.py).

The load-bearing guarantees:
* every counter is computed from the committed vault fixture (dated L1 day dirs, notes,
  briefs, registry) — the *math* is pinned so a refactor can't silently miscount;
* the output is **wall-clock independent** — two builds of the same fixture are
  byte-identical and depend only on the committed data, so ``--check`` is stable across
  days (the whole reason the counters can be a committed, CI-guarded artifact);
* ``stale()`` / ``--check`` detect drift the way build_graph / build_brief_index do.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import scripts.build_autonomy as ba


def _make_vault(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A minimal fixture: 2 L1 days (2 notes each), 1 brief (+README), 2 surfaced sources."""
    vault = tmp_path / "vault"
    sources = vault / "01 Sources"
    briefs = vault / "02 Briefs"
    for day in ("2026-06-18", "2026-06-20"):
        d = sources / day
        d.mkdir(parents=True)
        (d / "fuel-prices.md").write_text(f"# Fuel {day}\n", encoding="utf-8")
        (d / "earthquakes.md").write_text(f"# Quakes {day}\n", encoding="utf-8")
    # a non-dated dir must be ignored by the day-dir scan
    (sources / "not-a-date").mkdir()
    briefs.mkdir(parents=True)
    (briefs / "Energy Supply Weekly.md").write_text("# Energy\n", encoding="utf-8")
    (briefs / "README.md").write_text("# index\n", encoding="utf-8")  # excluded
    registry = tmp_path / "registry.json"
    registry.write_text(
        json.dumps(
            {
                "sources": [
                    {"key": "fuel-prices", "surfaced": True},
                    {"key": "earthquakes", "surfaced": True},
                    {"key": "sanctions", "surfaced": False},  # not counted
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(ba, "_SOURCES", sources)
    monkeypatch.setattr(ba, "_BRIEFS", briefs)
    monkeypatch.setattr(ba, "_REGISTRY", registry)
    return vault


def test_counter_math(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _make_vault(tmp_path, monkeypatch)
    c = ba.counters()
    assert c["first_l1_day"] == "2026-06-18"
    assert c["latest_l1_day"] == "2026-06-20"
    assert c["days_operating"] == 3  # 18,19,20 inclusive
    assert c["l1_ingests_committed"] == 2  # two dated dirs; "not-a-date" ignored
    assert c["l1_source_notes"] == 4  # 2 notes x 2 days
    assert c["l2_briefs"] == 1  # README excluded
    assert c["channels_surfaced"] == 2  # surfaced:false excluded
    assert c["weeks_operating"] == 0.4
    assert c["est_llm_spend_usd"] == round(0.4 * ba._EST_WEEKLY_SPEND_USD, 2)
    # spend is honestly labelled, never presented as metered truth
    assert "estimate" in c["spend_basis"].lower()


def test_wall_clock_independence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Two builds of the same committed fixture are byte-identical — no `today()` leakage."""
    _make_vault(tmp_path, monkeypatch)
    assert ba.render_json(ba.counters()) == ba.render_json(ba.counters())
    assert ba.render_html(ba.counters()) == ba.render_html(ba.counters())
    # the span is fixed by the fixture dates, not by the current date
    assert ba.counters()["days_operating"] == 3


def test_empty_vault_is_safe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    empty = tmp_path / "none"
    monkeypatch.setattr(ba, "_SOURCES", empty / "01 Sources")
    monkeypatch.setattr(ba, "_BRIEFS", empty / "02 Briefs")
    monkeypatch.setattr(ba, "_REGISTRY", empty / "registry.json")
    c = ba.counters()
    assert c["days_operating"] == 0
    assert c["l1_ingests_committed"] == 0
    assert c["est_llm_spend_usd"] == 0.0
    # render still produces valid strings on an empty vault
    assert ba.render_html(c).startswith("<!DOCTYPE html>")


def test_build_and_check_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _make_vault(tmp_path, monkeypatch)
    out = tmp_path / "site"
    ba.build(out)
    assert (out / "autonomy.json").is_file()
    assert (out / "autonomy.html").is_file()
    # fresh build == committed → in sync
    assert ba.stale(out) == []
    # perturb the committed json → detected as stale
    (out / "autonomy.json").write_text("{}", encoding="utf-8")
    assert "autonomy.json" in ba.stale(out)


def test_json_is_sorted_and_parseable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _make_vault(tmp_path, monkeypatch)
    text = ba.render_json(ba.counters())
    parsed = json.loads(text)  # valid JSON
    assert list(parsed.keys()) == sorted(parsed.keys())  # deterministic key order
    assert text.endswith("\n")
