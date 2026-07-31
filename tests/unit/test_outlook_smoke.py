"""Tests for the Outlook end-to-end proof (scripts/smoke_outlook.py) — design §6 P5.

This is the layer's ship-gate as a regression lock. The load-bearing guarantees:

* the whole pipeline (data -> forecast -> PI -> success metric) runs on the *committed* L1
  and the §5 **ship-bar passes** — the KR done-when, pinned so a refactor can't silently
  break it;
* the scorecard is **deterministic** — two builds off the same committed L1 are identical
  (the reason the score can be a committed, CI-guarded public artifact);
* only the four Tier-A series ever appear (the hazard interlock holds end-to-end), and every
  published forecast carries an honest interval that brackets its own point;
* ``check()`` / ``--check`` detect drift the way build_graph / build_autonomy do — the
  committed ``site/outlook-scorecard.json`` must stay in sync with the committed L1.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from outlook.series import FORECASTABLE_KEYS

# Load the CLI by file path (not `import scripts.smoke_outlook`) — the same idiom
# test_build_autonomy.py / test_build_graph.py use so mypy never sees it under two names.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "smoke_outlook", _REPO_ROOT / "scripts" / "smoke_outlook.py"
)
assert _spec and _spec.loader
so = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(so)


def test_scorecard_is_deterministic() -> None:
    """Same committed L1 -> byte-identical scorecard (the public-artifact contract)."""
    assert so.build_scorecard() == so.build_scorecard()


def test_all_four_tier_a_series_present() -> None:
    card = so.build_scorecard()
    keys = {s["key"] for s in card["series"]}
    assert keys == set(FORECASTABLE_KEYS)


def test_only_allow_list_keys_appear() -> None:
    """The hazard interlock holds end-to-end: nothing off the Tier-A allow-list leaks in."""
    card = so.build_scorecard()
    for s in card["series"]:
        assert s["key"] in FORECASTABLE_KEYS


def test_ship_bar_passes_on_committed_l1() -> None:
    """The §5 go/no-go — the KR done-when — must hold on the real committed data."""
    bar = so.build_scorecard()["ship_bar"]
    assert bar["passed"] is True
    assert bar["mase_pass"] >= bar["required"]
    assert bar["coverage_pass"] >= bar["required"]


def test_each_series_carries_forecast_and_score() -> None:
    """Every series ships the full KR-axis payload: data -> forecast -> PI -> metric."""
    card = so.build_scorecard()
    for s in card["series"]:
        assert s["n_observations"] >= 1
        fc = s["forecast"]
        assert set(fc) >= {"period", "point", "lower", "upper", "pi_level", "method"}
        assert fc["pi_level"] == 0.8
        sc = s["score"]
        assert set(sc) >= {
            "mase",
            "smape",
            "coverage",
            "beats_naive",
            "coverage_ok",
            "recommended",
        }


def test_published_interval_brackets_its_point() -> None:
    """An honest PI: lower <= point <= upper for every published forecast (design §4.3)."""
    card = so.build_scorecard()
    for s in card["series"]:
        fc = s["forecast"]
        assert fc["lower"] <= fc["point"] <= fc["upper"]


def test_scorecard_records_the_l1_day_it_was_fit_on() -> None:
    """Gating behind KR1: the artifact names the committed L1 day, so a stale forecast is visible."""
    card = so.build_scorecard()
    assert card["l1_day"] is not None
    assert card["gated_on"].startswith("KR1")


def test_committed_artifact_is_in_sync() -> None:
    """The committed site/outlook-scorecard.json must not be stale vs the committed L1 (CI guard)."""
    assert so.check(_REPO_ROOT / "site") is False


def test_smoke_main_exits_zero(tmp_path: Path) -> None:
    """End-to-end: the smoke CLI returns 0 on the committed L1 (pipeline healthy + ship-bar pass)."""
    assert so.main(["--out", str(tmp_path)]) == 0
    assert (tmp_path / "outlook-scorecard.json").is_file()
