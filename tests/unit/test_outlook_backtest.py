"""Tests for the Outlook rolling-origin score + ship-bar (outlook/backtest.py) — design §5 / §6 P3.

Two contracts carry the layer's credibility and get the hardest tests: (1) the metrics are
**hand-checkable** — MASE, sMAPE and PI-coverage reproduce values computed by hand on a fixture
series, because a score nobody can rebuild is exactly the black-box foil azimuth criticizes; and
(2) the **honesty rule is real in code** — a series that cannot beat the seasonal-naive baseline
is scored ``seasonal-naive (fallback)`` and the §5 ship-bar (beat naive AND hold 80% coverage on
>= 3 of 4 series) is computed deterministically, not asserted in prose.
"""

from __future__ import annotations

from outlook.backtest import (
    BacktestRun,
    ScoreCard,
    coverage,
    mase,
    naive_scale,
    rolling_origin,
    score_all,
    score_series,
    ship_bar,
    smape,
)
from outlook.forecast import forecast_series
from outlook.series import Series


def _series(key: str, cadence: str, season: int, points: list[tuple[str, float]]) -> Series:
    return Series(
        key=key,
        label=key,
        unit="u",
        cadence=cadence,
        season=season,
        source_key=key,
        points=tuple(points),
    )


def _monthly(key: str, season: int, values: list[float], start: str = "2025-08") -> Series:
    year, month = (int(x) for x in start.split("-"))
    pts: list[tuple[str, float]] = []
    for v in values:
        pts.append((f"{year:04d}-{month:02d}", v))
        month += 1
        if month > 12:
            month, year = 1, year + 1
    return _series(key, "monthly", season, pts)


def _weekly(key: str, values: list[float], start: str = "2026-06-05") -> Series:
    import datetime as _dt

    base = _dt.date.fromisoformat(start)
    pts = [((base + _dt.timedelta(days=7 * k)).isoformat(), v) for k, v in enumerate(values)]
    return _series(key, "weekly", 52, pts)


# ── standalone metrics: hand-checked, independent of the ensemble ─────────────────────────────
def test_mase_reproduces_a_hand_checked_value() -> None:
    """The P3 headline gate: MASE on a fixture matches the value computed by hand.

    in-sample = [10,12,14,16,18], season 1 -> lag-1 naive MAE = mean(|Δ|) = 2.0 (the scale).
    actuals=[20,25], forecasts=[19,22] -> mean(|20-19|,|25-22|) = mean(1,3) = 2.0.
    MASE = 2.0 / 2.0 = 1.0 exactly.
    """
    assert mase([20.0, 25.0], [19.0, 22.0], [10.0, 12.0, 14.0, 16.0, 18.0], 1) == 1.0


def test_mase_is_zero_for_a_perfect_forecast() -> None:
    assert mase([20.0], [20.0], [10.0, 12.0, 14.0, 16.0, 18.0], 1) == 0.0


def test_mase_zero_scale_is_infinite_not_a_crash() -> None:
    # A flat in-sample series has zero naive scale: an imperfect forecast is honestly infinite
    # (never a silent divide-by-zero), a perfect one is exactly zero.
    assert mase([10.0], [11.0], [5.0, 5.0, 5.0, 5.0], 1) == float("inf")
    assert mase([5.0], [5.0], [5.0, 5.0, 5.0, 5.0], 1) == 0.0


def test_naive_scale_uses_lag1_under_one_season() -> None:
    # 5 monthly points, season 12 -> not a full season, so scale is the lag-1 naive MAE.
    assert naive_scale([10.0, 12.0, 14.0, 16.0, 18.0], 12) == (2.0, 1)


def test_naive_scale_uses_the_season_lag_once_a_cycle_is_observed() -> None:
    # 8 points, season 4 (> one full cycle) -> seasonal lag-4; here every year-on-year step is +1.
    assert naive_scale([1.0, 2.0, 3.0, 4.0, 2.0, 3.0, 4.0, 5.0], 4) == (1.0, 4)


def test_smape_is_bounded_and_symmetric() -> None:
    # a=10, f=30 -> 2*20 / (10+30) = 1.0 -> 100%.
    assert smape([10.0], [30.0]) == 100.0


def test_smape_never_divides_by_zero() -> None:
    assert smape([0.0], [0.0]) == 0.0


def test_coverage_counts_actuals_inside_their_interval() -> None:
    # 1 in [0,2] yes, 2 in [0,2] yes, 3 in [0,2] no, 4 in [10,20] no -> 2/4.
    assert coverage([1.0, 2.0, 3.0, 4.0], [0.0, 0.0, 0.0, 10.0], [2.0, 2.0, 2.0, 20.0]) == 0.5


# ── rolling-origin backtest ───────────────────────────────────────────────────────────────────
def test_rolling_origin_arrays_are_aligned() -> None:
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    run = rolling_origin(s, min_train=4)
    n = 12 - 4  # one test point per expanding origin from the 4th
    assert isinstance(run, BacktestRun)
    for arr in (run.periods, run.actuals, run.forecasts, run.lowers, run.uppers, run.naive):
        assert len(arr) == n


def test_rolling_origin_scores_the_forecast_that_would_ship() -> None:
    """Honesty contract: each origin's scored forecast IS the published forecast on that prefix."""
    s = _monthly("co2-ppm", 12, [400.0 + i * 1.3 for i in range(12)])
    run = rolling_origin(s, min_train=4)
    # Re-forecast the first backtest origin by hand and confirm the backtest used that exact value.
    prefix = _monthly("co2-ppm", 12, [400.0 + i * 1.3 for i in range(4)])
    assert run.forecasts[0] == forecast_series(prefix, 1).point[0]


def test_rolling_origin_is_deterministic() -> None:
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    assert rolling_origin(s) == rolling_origin(s)


# ── score card + the §5 honesty fallback ──────────────────────────────────────────────────────
def test_score_series_recommends_the_forecast_when_it_beats_naive() -> None:
    # A clean upward line: the ensemble comfortably beats naive -> recommend the forecast.
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    card = score_series(s)
    assert card.mase < 1.0
    assert card.beats_naive is True
    assert card.recommended == "forecast"


def test_score_series_falls_back_to_naive_when_it_cannot_beat_it() -> None:
    """The §5 honesty rule, enforced in code: a series the model can't beat shows naive, labelled.

    A perfectly periodic series (2+ clean cycles) has a zero seasonal-naive scale, so any
    non-exact model forecast scores MASE = inf — worse than naive — and the card must recommend
    the labelled naive baseline rather than a model that only looks sophisticated.
    """
    periodic = _monthly("co2-ppm", 4, [10.0, 20.0, 30.0, 40.0] * 3)
    card = score_series(periodic)
    assert card.beats_naive is False
    assert card.recommended == "seasonal-naive (fallback)"


def test_score_card_flags_agree_with_the_thresholds() -> None:
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    card = score_series(s)
    assert card.beats_naive == (card.mase < 1.0)
    assert card.coverage_ok == (0.70 <= card.coverage <= 0.90)


def test_score_all_scores_every_series_and_is_deterministic() -> None:
    series_map = {
        "co2-ppm": _monthly("co2-ppm", 12, [400.0 + i for i in range(12)]),
        "us-crude-stocks": _weekly("us-crude-stocks", [700.0 + k for k in range(8)]),
    }
    cards = score_all(series_map)
    assert set(cards) == set(series_map)
    assert all(isinstance(c, ScoreCard) for c in cards.values())
    assert score_all(series_map) == cards  # deterministic


# ── the ship-bar (the §5 go / no-go, computed not asserted in prose) ───────────────────────────
def _card(key: str, beats: bool, cov_ok: bool) -> ScoreCard:
    return ScoreCard(
        series_key=key,
        label=key,
        unit="u",
        n_test=5,
        mase=0.5 if beats else 1.5,
        smape=1.0,
        coverage=0.8 if cov_ok else 0.5,
        beats_naive=beats,
        coverage_ok=cov_ok,
        recommended="forecast" if beats else "seasonal-naive (fallback)",
    )


def _cards(specs: list[tuple[bool, bool]]) -> dict[str, ScoreCard]:
    return {f"s{i}": _card(f"s{i}", b, c) for i, (b, c) in enumerate(specs)}


def test_ship_bar_passes_on_three_of_four() -> None:
    bar = ship_bar(_cards([(True, True), (True, True), (True, False), (False, True)]))
    assert bar.mase_pass == 3
    assert bar.coverage_pass == 3
    assert bar.required == 3
    assert bar.passed is True


def test_ship_bar_fails_when_mase_misses_the_bar() -> None:
    bar = ship_bar(_cards([(True, True), (True, True), (False, False), (False, True)]))
    assert bar.mase_pass == 2
    assert bar.passed is False


def test_ship_bar_fails_when_coverage_misses_the_bar() -> None:
    bar = ship_bar(_cards([(True, True), (True, True), (True, False), (True, False)]))
    assert bar.coverage_pass == 2
    assert bar.passed is False


def test_ship_bar_required_adapts_below_four_series() -> None:
    # With fewer than four series the bar requires ALL of them (no free pass from a small set).
    bar = ship_bar(_cards([(True, True), (True, True)]))
    assert bar.required == 2
    assert bar.passed is True
    assert ship_bar(_cards([(True, True), (False, True)])).passed is False


def test_ship_bar_on_no_series_is_not_a_pass() -> None:
    bar = ship_bar({})
    assert bar.total == 0
    assert bar.passed is False
