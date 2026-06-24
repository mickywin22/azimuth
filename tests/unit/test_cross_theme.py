"""Tests for the cross-theme bridge scanner (synthesis/cross_theme.py).

The load-bearing guarantee of the *World Watch Weekly* meta-brief: a region the live L1
data records under TWO editorially-clean themes becomes a data-backed **bridge**, with
the concrete per-channel evidence pulled straight from the source notes. That is the
cross-channel synthesis a static OKF bundle cannot produce, so it gets a regression test.
Held themes must never bridge; a single-theme region must never bridge.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from synthesis.cross_theme import ENERGY_INFRA_CORE, scan

if TYPE_CHECKING:
    from pathlib import Path

_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "geophysical": {"title": "Geophysical Weekly", "brief": "Geophysical Weekly.md"},
        "prediction-markets": {
            "title": "Prediction Markets Weekly",
            "brief_held": True,
            "hold_reason": "single politically-charged market",
        },
    },
    "sources": [
        {"key": "fuel-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "earthquakes", "theme": "geophysical", "surfaced": True},
        {"key": "prediction-markets", "theme": "prediction-markets", "surfaced": True},
    ],
}


def _make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    d = vault / "01 Sources" / "2026-06-23"
    d.mkdir(parents=True)
    # Greece bridges BOTH themes (fuel row + quake). Japan is geophysical-only (no bridge).
    # Greece also appears in the held prediction-markets note -> must NOT count.
    (d / "fuel-prices.md").write_text(
        '---\nsource: Fuel\n---\n# Fuel\n| field | value |\n| --- | --- |\n'
        '| countries | [{"name": "Greece", "diesel": {"usdPrice": 2.02, "wowPct": 0.79}, '
        '"gasoline": {"usdPrice": 2.33, "wowPct": -2.03}}, '
        '{"name": "Germany", "diesel": {"usdPrice": 2.16, "wowPct": 1.05}, "gasoline": null}] |\n'
        '| failedSources | ["New Zealand"] |\n',
        encoding="utf-8",
    )
    (d / "earthquakes.md").write_text(
        "---\nsource: USGS\n---\n# Quakes\n| field | value |\n| --- | --- |\n"
        '| earthquakes | [{"id": "q1", "magnitude": 5.2, "place": "10 km S of Kastri, Greece"}, '
        '{"id": "q2", "magnitude": 6.1, "place": "Off Japan"}, '
        '{"id": "q3", "magnitude": 5.1, "place": "Kermadec Islands, New Zealand"}] |\n',
        encoding="utf-8",
    )
    (d / "prediction-markets.md").write_text(
        "---\nsource: Polymarket\n---\n# PM\nA market mentioning Greece.\n", encoding="utf-8"
    )
    return vault


def test_shared_region_becomes_bridge(tmp_path: Path) -> None:
    """ACCEPTANCE: a region under >=2 clean themes is a bridge spanning both."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    regions = {b.region for b in s.bridges}
    assert "Greece" in regions, "Greece should bridge energy-supply + geophysical"
    greece = next(b for b in s.bridges if b.region == "Greece")
    assert greece.theme_slugs == ["energy-supply", "geophysical"]


def test_single_theme_region_does_not_bridge(tmp_path: Path) -> None:
    """Japan appears only under geophysical -> it must not surface as a bridge."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    assert "Japan" not in {b.region for b in s.bridges}


def test_held_theme_excluded(tmp_path: Path) -> None:
    """A region's mention inside a HELD theme's note must not count toward bridging."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    assert "prediction-markets" not in s.clean_themes
    greece = next(b for b in s.bridges if b.region == "Greece")
    assert "prediction-markets" not in greece.themes


def test_bridge_carries_concrete_evidence(tmp_path: Path) -> None:
    """Each bridge pulls real per-channel data (quake magnitude, fuel price) from L1."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    greece = next(b for b in s.bridges if b.region == "Greece")
    assert any("M5.2" in snip for snip in greece.evidence.get("earthquakes", []))
    assert any("diesel" in snip for snip in greece.evidence.get("fuel-prices", []))


def test_failed_fuel_source_is_honest_evidence(tmp_path: Path) -> None:
    """New Zealand (seismic + fuel failedSources) reports the missing feed honestly."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    nz = next((b for b in s.bridges if b.region == "New Zealand"), None)
    assert nz is not None, "New Zealand should bridge (quake + failedSources mention)"
    assert any("failedSources" in snip for snip in nz.evidence.get("fuel-prices", []))


def test_no_observed_reach_when_off_energy_core(tmp_path: Path) -> None:
    """With no bridge on the US/EU energy core, infra_reach is empty (sourced non-finding)."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    assert s.infra_reach == []
    assert "United States" in ENERGY_INFRA_CORE


def test_scan_is_json_serialisable_shape(tmp_path: Path) -> None:
    """The scan's public fields round-trip through JSON (CLI --json contract)."""
    s = scan(_make_vault(tmp_path), _REGISTRY)
    payload = {
        "day": s.day,
        "clean_themes": s.clean_themes,
        "bridges": [{"region": b.region, "themes": b.themes} for b in s.bridges],
    }
    assert json.loads(json.dumps(payload))["day"] == "2026-06-23"
