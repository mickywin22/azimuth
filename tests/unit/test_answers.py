"""Tests for the TOP5 demonstrator answer engine (synthesis/answers.py).

The demonstrator IS azimuth's USP: it answers cross-source questions a single feed cannot,
from live data, with every claim sourced. The load-bearing guarantees, each a regression:

* exactly the five fixed questions are answered;
* every answer connects >=2 channels and names its use-case/persona;
* every claim bullet carries >=1 [[L1 wikilink]] (so the rendered brief is lint-green);
* numbers are read from the live bundle, never invented (held themes excluded);
* an honest "no observed reach" / "no shared region" non-finding is produced when the data
  shows no overlap (a sourced absence is a valid answer);
* the rendered brief passes the full synthesis lint.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from synthesis.answers import build_answer_set, load_bundle, render_brief_markdown
from synthesis.lint import lint_brief

if TYPE_CHECKING:
    from pathlib import Path

_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "geophysical": {"title": "Geophysical Weekly", "brief": "Geophysical Weekly.md"},
        "climate-signals": {
            "title": "Climate Signals Weekly",
            "brief": "Climate Signals Weekly.md",
        },
        "prediction-markets": {
            "title": "Prediction Markets Weekly",
            "brief_held": True,
            "hold_reason": "single market — too narrow",
        },
    },
    "sources": [
        {"key": "natural-gas-storage-eu", "theme": "energy-supply", "surfaced": True},
        {"key": "crude-oil-inventories", "theme": "energy-supply", "surfaced": True},
        {"key": "energy-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "fuel-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "earthquakes", "theme": "geophysical", "surfaced": True},
        {"key": "co2-monitoring", "theme": "climate-signals", "surfaced": True},
        {"key": "prediction-markets", "theme": "prediction-markets", "surfaced": True},
    ],
}


def _make_vault(tmp_path: Path, *, quake_overlaps_energy: bool = False) -> Path:
    """A minimal but realistic two-day bundle (energy/geo on day 1, climate on day 2)."""
    vault = tmp_path / "vault"
    d1 = vault / "01 Sources" / "2026-06-23"
    d2 = vault / "01 Sources" / "2026-06-24"
    d1.mkdir(parents=True)
    d2.mkdir(parents=True)

    (d1 / "natural-gas-storage-eu.md").write_text(
        "---\nsource: GIE\n---\n# Gas\n| field | value |\n| --- | --- |\n"
        '| weeks | [{"period": "2026-06-12", "storBcf": 2759, "weeklyChangeBcf": 73}, '
        '{"period": "2026-06-05", "storBcf": 2686, "weeklyChangeBcf": 108}] |\n',
        encoding="utf-8",
    )
    (d1 / "crude-oil-inventories.md").write_text(
        "---\nsource: EIA\n---\n# Crude\n| field | value |\n| --- | --- |\n"
        '| weeks | [{"period": "2026-06-12", "stocksMb": 758473, "weeklyChangeMb": -17204}, '
        '{"period": "2026-06-05", "stocksMb": 775677, "weeklyChangeMb": -15154}] |\n',
        encoding="utf-8",
    )
    (d1 / "energy-prices.md").write_text(
        "---\nsource: WM\n---\n# Prices\n| field | value |\n| --- | --- |\n"
        '| prices | [{"change": -4.9, "commodity": "wti", "name": "WTI Crude Oil", '
        '"price": "92.16", "unit": "$/barrel"}, {"change": -5.2, "commodity": "brent", '
        '"name": "Brent Crude Oil", "price": "93.76", "unit": "$/barrel"}] |\n',
        encoding="utf-8",
    )
    # Greece bridges energy (fuel) + geophysical (quake). US quake optional (energy-core reach).
    quake_place = "10 km S of Anchorage, United States" if quake_overlaps_energy else "Off Tonga"
    (d1 / "fuel-prices.md").write_text(
        "---\nsource: Fuel\n---\n# Fuel\n| field | value |\n| --- | --- |\n"
        '| countries | [{"name": "Greece", "diesel": {"usdPrice": 2.02}, "gasoline": null}, '
        '{"name": "United States", "diesel": {"usdPrice": 1.0}, "gasoline": null}] |\n'
        "| failedSources | [] |\n",
        encoding="utf-8",
    )
    (d1 / "earthquakes.md").write_text(
        "---\nsource: USGS\n---\n# Quakes\n| field | value |\n| --- | --- |\n"
        f'| earthquakes | [{{"id": "q1", "magnitude": 6.7, "place": "{quake_place}"}}, '
        '{"id": "q2", "magnitude": 5.2, "place": "10 km S of Kastri, Greece"}] |\n',
        encoding="utf-8",
    )
    (d2 / "co2-monitoring.md").write_text(
        "---\nsource: NOAA\n---\n# CO2\n| field | value |\n| --- | --- |\n"
        '| monitoring | {"annualGrowthRate": 2.86, "currentPpm": 430.78, '
        '"station": "Mauna Loa"} |\n',
        encoding="utf-8",
    )
    # held theme present on disk — must never feed an answer
    (d1 / "prediction-markets.md").write_text(
        "---\nsource: PM\n---\n# PM\n| field | value |\n| --- | --- |\n"
        '| markets | [{"q": "A market mentioning Greece and United States"}] |\n',
        encoding="utf-8",
    )
    return vault


def test_held_theme_excluded_from_bundle(tmp_path: Path) -> None:
    bundle = load_bundle(_make_vault(tmp_path), _REGISTRY)
    assert "prediction-markets" not in bundle, "held theme must never enter the bundle"
    assert "earthquakes" in bundle and "co2-monitoring" in bundle


def test_exactly_five_questions(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    assert [a.qid for a in aset.answers] == ["Q1", "Q2", "Q3", "Q4", "Q5"]
    assert aset.day == "2026-06-24", "representative day = newest note in the bundle"
    assert aset.week == "2026-W26"


def test_every_answer_two_channels_and_a_persona(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    for a in aset.answers:
        assert len(a.channels) >= 2, f"{a.qid} must connect >=2 channels, got {a.channels}"
        assert a.persona.strip(), f"{a.qid} must name a use-case/persona"


def test_every_claim_is_sourced(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    for a in aset.answers:
        assert a.claims, f"{a.qid} produced no claims"
        for c in a.claims:
            assert c.sources, f"{a.qid} has an unsourced claim: {c.md!r}"
            assert all(f"[[{s}]]" in c.md for s in c.sources), "citation must be inline"


def test_numbers_read_from_live_data(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    q1 = next(a for a in aset.answers if a.qid == "Q1")
    blob = " ".join(c.md for c in q1.claims)
    assert "2,759" in blob and "+73" in blob, "gas storage figures must come from the data"
    assert "-17,204" in blob, "crude drawdown figure must come from the data"
    q3 = next(a for a in aset.answers if a.qid == "Q3")
    assert "M6.7" in " ".join(c.md for c in q3.claims), "largest quake read from the data"


def test_q3_honest_non_finding_when_no_energy_reach(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path, quake_overlaps_energy=False), _REGISTRY)
    q3 = next(a for a in aset.answers if a.qid == "Q3")
    assert any("No observed reach" in c.md for c in q3.claims)


def test_q3_flags_observed_reach_when_quake_hits_energy_core(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path, quake_overlaps_energy=True), _REGISTRY)
    q3 = next(a for a in aset.answers if a.qid == "Q3")
    assert any("Observed reach" in c.md for c in q3.claims)


def test_rendered_brief_passes_synthesis_lint(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path)
    aset = build_answer_set(vault, _REGISTRY)
    brief = render_brief_markdown(aset, prior_changelog=[])
    violations = lint_brief(brief, sources_root=vault / "01 Sources")
    assert violations == [], f"rendered demonstrator brief must be lint-green: {violations}"


def test_counterfactual_flips_the_verdict_for_at_least_two_questions(tmp_path: Path) -> None:
    """The 'what-if' proof: feeding the sign-flipped input recomputes a DIFFERENT verdict.

    This is the load-bearing demonstrator guarantee — the verdict is a pure function of the
    bundle, so a flipped input must produce a different branch + a different verdict. >=2 Qs
    must carry a working counterfactual (the KR-B acceptance gate).
    """
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    with_whatif = [a for a in aset.answers if a.whatif is not None]
    assert len(with_whatif) >= 2, "at least two questions must carry a what-if counterfactual"
    for a in with_whatif:
        wf = a.whatif
        assert wf is not None
        real_verdict = a.claims[0].md
        assert wf.flipped_verdict != real_verdict, f"{a.qid}: flip must change the verdict text"
        assert wf.real_branch != wf.flipped_branch, f"{a.qid}: flip must change the branch"
        assert wf.real_value != wf.flipped_value, f"{a.qid}: flipped input must differ"
        # counterfactual verdict stays sourced (still carries its inline [[L1]] citation)
        assert "[[" in wf.flipped_verdict and "]]" in wf.flipped_verdict


def test_q2_counterfactual_is_the_supply_vs_demand_flip(tmp_path: Path) -> None:
    """Q2 real data (draw + price fall) reads 'demand'; flip the price sign -> 'supply'."""
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    q2 = next(a for a in aset.answers if a.qid == "Q2")
    assert q2.whatif is not None
    assert "demand, not supply" in q2.claims[0].md, "real Q2 verdict is the demand read"
    assert "supply drove the tape" in q2.whatif.flipped_verdict, "flipped Q2 verdict is supply"
    assert q2.whatif.real_branch == "inventory draw + price fall"
    assert q2.whatif.flipped_branch == "inventory draw + price rise"


def test_brief_evolves_in_place(tmp_path: Path) -> None:
    aset = build_answer_set(_make_vault(tmp_path), _REGISTRY)
    prior = ["- 2026-06-17 — prior cycle line."]
    brief = render_brief_markdown(aset, prior_changelog=prior)
    assert "2026-06-17 — prior cycle line." in brief, "prior changelog must be preserved"
    assert brief.count("- 2026-06-24 —") == 1, "this cycle appends exactly one dated line"
