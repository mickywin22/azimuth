"""Tests for the benchmark engine (synthesis/benchmark.py).

The benchmark is azimuth's sharpest USP proof: the SAME world-topic through three columns —
azimuth (observed + sourced facts) vs a forecast product (probability) vs an intelligence
product (assessment). The load-bearing guarantees, each a regression:

* the three fixed head-to-head topics are produced;
* every azimuth claim carries >=1 [[L1 wikilink]] read from the live bundle (so the rendered
  brief is lint-green and azimuth's columns NEVER editorialise/predict);
* the foil columns quote the compared product when present, and degrade to an HONEST absence
  (with reason) when the feed carries no forecast for that topic — no fabricated foil;
* the scorecard is a fair contrast: azimuth wins the 5 USP dimensions, but the
  forward-looking row honestly concedes to the forecast/intel product;
* the foil selector matches by stable domain/keyword (resilient to per-cycle id churn);
* the rendered brief passes the full synthesis lint (azimuth claims sourced, no editorial
  deny-list hit even with the quoted foil text in the body).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from synthesis.benchmark import (
    FOIL_SPECS,
    build_benchmark,
    render_brief_markdown,
    select_foil,
    trim_foil,
)
from synthesis.lint import lint_brief

if TYPE_CHECKING:
    from pathlib import Path

_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "geophysical": {"title": "Geophysical Weekly", "brief": "Geophysical Weekly.md"},
    },
    "sources": [
        {"key": "natural-gas-storage-eu", "theme": "energy-supply", "surfaced": True},
        {"key": "crude-oil-inventories", "theme": "energy-supply", "surfaced": True},
        {"key": "energy-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "fuel-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "earthquakes", "theme": "geophysical", "surfaced": True},
    ],
}

# A pair of trimmed foils (energy + inflation present, seismic absent) — the live shape.
_FOILS = {
    "captured_at": "2026-06-24T19:00:00Z",
    "topics": {
        "energy-supply": {
            "foil": {
                "title": "Oil price impact from Strait of Hormuz disruption",
                "probability": 0.4,
                "confidence": 0.58,
                "time_horizon": "30d",
                "trend": "stable",
                "projections": {"d30": 0.4, "d7": 0.55, "h24": 0.95},
                "scenario_short": "Strait of Hormuz risk: critical.",
                "perspective_strategic": "Strait of Hormuz risk is setting the strategic baseline.",
                "perspective_contrarian": "Restraint could move the forecast below the 40% baseline.",
                "actor_lens": "Commodity traders: price whether stress becomes durable over the 30d.",
                "top_signal": "Strait of Hormuz risk: critical",
            },
            "absence_reason": None,
        },
        "supply-chain-inflation": {
            "foil": {
                "title": "Inflation and rates pressure from Black Sea maritime disruption",
                "probability": 0.61,
                "confidence": 0.75,
                "time_horizon": "30d",
                "trend": "stable",
                "projections": {"d30": 0.61, "d7": 0.84, "h24": 0.95},
                "scenario_short": "Inflation pressure from Black Sea maritime disruption.",
                "perspective_strategic": "A significant economic vulnerability from regional instability.",
                "perspective_contrarian": None,
                "actor_lens": "Commodity traders: price whether stress becomes durable.",
                "top_signal": "shipping cost shock",
            },
            "absence_reason": None,
        },
        "seismic-infrastructure": {"foil": None, "absence_reason": None},
    },
}


def _make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    d1 = vault / "01 Sources" / "2026-06-24"
    d1.mkdir(parents=True)
    (d1 / "natural-gas-storage-eu.md").write_text(
        "---\nsource: GIE\n---\n# Gas\n| field | value |\n| --- | --- |\n"
        '| weeks | [{"period": "2026-06-12", "storBcf": 2759, "weeklyChangeBcf": 73}] |\n',
        encoding="utf-8",
    )
    (d1 / "crude-oil-inventories.md").write_text(
        "---\nsource: EIA\n---\n# Crude\n| field | value |\n| --- | --- |\n"
        '| weeks | [{"period": "2026-06-12", "stocksMb": 758473, "weeklyChangeMb": -17204}] |\n',
        encoding="utf-8",
    )
    (d1 / "energy-prices.md").write_text(
        "---\nsource: WM\n---\n# Prices\n| field | value |\n| --- | --- |\n"
        '| prices | [{"change": -4.9, "commodity": "wti", "name": "WTI", "price": "92.16"}, '
        '{"change": -5.2, "commodity": "brent", "name": "Brent", "price": "93.76"}] |\n',
        encoding="utf-8",
    )
    (d1 / "fuel-prices.md").write_text(
        "---\nsource: Fuel\n---\n# Fuel\n| field | value |\n| --- | --- |\n"
        '| countries | [{"name": "Greece", "diesel": {"usdPrice": 2.02}}] |\n',
        encoding="utf-8",
    )
    (d1 / "earthquakes.md").write_text(
        "---\nsource: USGS\n---\n# Quakes\n| field | value |\n| --- | --- |\n"
        '| earthquakes | [{"id": "q1", "magnitude": 6.7, "place": "43 km ESE of Palu, Indonesia"}, '
        '{"id": "q2", "magnitude": 5.2, "place": "Off Tonga"}] |\n',
        encoding="utf-8",
    )
    return vault


def test_three_fixed_topics(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    assert [t.topic_id for t in bench.topics] == [
        "energy-supply",
        "supply-chain-inflation",
        "seismic-infrastructure",
    ]
    assert bench.day == "2026-06-24" and bench.week == "2026-W26"
    assert bench.foil_captured_at == "2026-06-24T19:00:00Z"


def test_every_azimuth_claim_is_sourced(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    for t in bench.topics:
        assert t.azimuth_claims, f"{t.topic_id} produced no azimuth claims"
        for c in t.azimuth_claims:
            assert c.sources, f"{t.topic_id} has an unsourced azimuth claim: {c.md!r}"
            assert all(f"[[{s}]]" in c.md for s in c.sources), "citation must be inline"
        assert t.verdict.sources, f"{t.topic_id} verdict must cite an L1 note"


def test_numbers_read_from_live_data(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    energy = next(t for t in bench.topics if t.topic_id == "energy-supply")
    blob = " ".join(c.md for c in energy.azimuth_claims)
    assert "2,759" in blob and "-17,204" in blob and "92.16" in blob
    seismic = next(t for t in bench.topics if t.topic_id == "seismic-infrastructure")
    assert "M6.7" in " ".join(c.md for c in seismic.azimuth_claims)


def test_foil_present_and_quoted(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    energy = next(t for t in bench.topics if t.topic_id == "energy-supply")
    assert energy.forecast.present and "40%" in energy.forecast.headline
    assert "WorldMonitor forecast feed" in energy.forecast.attribution
    assert energy.intelligence.present and energy.intelligence.actor_lens


def test_seismic_is_honest_absence_not_fabricated(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    seismic = next(t for t in bench.topics if t.topic_id == "seismic-infrastructure")
    assert not seismic.forecast.present and not seismic.intelligence.present
    assert "not predictable" in seismic.forecast.headline
    # absent foil scores the USP rows '—', never a fabricated win against a missing product
    for row in seismic.scorecard:
        assert row.forecast == "—" and row.intelligence == "—"


def test_scorecard_is_a_fair_contrast(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    energy = next(t for t in bench.topics if t.topic_id == "energy-supply")
    wins = [r for r in energy.scorecard if r.azimuth_wins]
    concedes = [r for r in energy.scorecard if not r.azimuth_wins]
    assert len(wins) == 5, "azimuth wins the 5 USP dimensions"
    assert len(concedes) == 1 and "Forward-looking" in concedes[0].dimension
    # the honest row genuinely credits the forecast product
    assert "Yes" in concedes[0].forecast


def test_foil_selector_matches_by_keyword_not_id() -> None:
    forecasts = [
        {
            "id": "x1",
            "domain": "market",
            "title": "Oil price impact from Hormuz",
            "region": "Middle East",
            "scenarioShort": "",
            "confidence": 0.58,
        },
        {
            "id": "x2",
            "domain": "political",
            "title": "Will X visit Y?",
            "region": "Americas",
            "scenarioShort": "",
            "confidence": 0.9,
        },
    ]
    spec = next(s for s in FOIL_SPECS if s.topic_id == "energy-supply")
    match = select_foil(spec, forecasts)
    assert match is not None and match["id"] == "x1", (
        "keyword/domain match, not highest conf overall"
    )
    # no candidate -> honest None
    spec_seis = next(s for s in FOIL_SPECS if s.topic_id == "seismic-infrastructure")
    assert select_foil(spec_seis, forecasts) is None


def test_trim_foil_keeps_only_quote_fields() -> None:
    raw = {
        "id": "fc1",
        "domain": "market",
        "region": "Middle East",
        "title": "Oil",
        "probability": 0.4,
        "priorProbability": 0.4,
        "confidence": 0.58,
        "timeHorizon": "30d",
        "trend": "stable",
        "projections": {"d30": 0.4},
        "scenarioShort": "short",
        "perspectives": {"strategic": "s", "contrarian": "c"},
        "caseFile": {"actorLenses": ["lens one", "lens two"]},
        "signals": [{"value": "sig", "weight": 0.5}],
        "cascades": ["should-not-survive"],
        "stateDerivedBackfill": "huge",
    }
    t = trim_foil(raw)
    assert t["probability"] == 0.4 and t["actor_lens"] == "lens one"
    assert t["perspective_strategic"] == "s" and t["top_signal"] == "sig"
    assert "cascades" not in t and "stateDerivedBackfill" not in t


def test_rendered_brief_passes_synthesis_lint(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path)
    bench = build_benchmark(vault, _REGISTRY, _FOILS)
    brief = render_brief_markdown(bench, prior_changelog=[])
    violations = lint_brief(brief, sources_root=vault / "01 Sources")
    assert violations == [], f"rendered benchmark brief must be lint-green: {violations}"


def test_brief_evolves_in_place(tmp_path: Path) -> None:
    bench = build_benchmark(_make_vault(tmp_path), _REGISTRY, _FOILS)
    prior = ["- 2026-06-17 — prior cycle line."]
    brief = render_brief_markdown(bench, prior_changelog=prior)
    assert "2026-06-17 — prior cycle line." in brief, "prior changelog preserved"
    assert brief.count("- 2026-06-24 —") == 1, "this cycle appends exactly one dated line"
