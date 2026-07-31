"""Tests for the Outlook baseline ensemble + PI (outlook/forecast.py) — design §4 / §6 P2.

Two contracts matter most and get the hardest tests: (1) the forecast path is deterministic
and every model behaves correctly on a known series, and (2) the **hazard interlock** is real —
earthquakes and every non-Tier-A stream can NEVER be forecast, enforced in code.
"""

from __future__ import annotations

import pytest

from outlook.forecast import (
    Forecast,
    HazardInterlockError,
    assert_forecastable,
    eligible_models,
    ensemble_point,
    forecast_series,
    holt,
    holt_winters,
    seasonal_naive,
    ses,
    theil_sen_drift,
)
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


# ── individual models ───────────────────────────────────────────────────────────────────────
def test_seasonal_naive_repeats_the_cycle() -> None:
    y = [1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0]
    assert seasonal_naive(y, 4, 4) == [1.0, 2.0, 3.0, 4.0]


def test_seasonal_naive_falls_back_when_under_one_cycle() -> None:
    # Fewer points than a full season -> repeat the last value (plain naive).
    assert seasonal_naive([5.0, 6.0], 12, 3) == [6.0, 6.0, 6.0]


def test_theil_sen_extrapolates_a_perfect_line_exactly() -> None:
    y = [2.0, 4.0, 6.0, 8.0, 10.0]  # slope 2, intercept 2
    assert theil_sen_drift(y, 2) == [12.0, 14.0]


def test_theil_sen_is_robust_to_a_single_outlier() -> None:
    clean = theil_sen_drift([2.0, 4.0, 6.0, 8.0, 10.0], 1)[0]
    spiked = theil_sen_drift([2.0, 4.0, 6.0, 8.0, 10.0, 99.0, 14.0], 1)[0]
    # A robust slope shrugs off the spike; an OLS fit would be yanked far more.
    assert abs(spiked - (16.0)) < 6.0 and clean == 12.0


def test_ses_on_a_constant_series_is_flat() -> None:
    assert ses([5.0, 5.0, 5.0, 5.0], 3) == [5.0, 5.0, 5.0]


def test_holt_continues_a_linear_trend() -> None:
    fc = holt([1.0, 2.0, 3.0, 4.0, 5.0], 2)
    assert abs(fc[0] - 6.0) < 0.6 and abs(fc[1] - 7.0) < 0.8


def test_holt_winters_falls_back_to_holt_under_two_cycles() -> None:
    y = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]  # season 4, only 1.5 cycles -> Holt
    assert holt_winters(y, 4, 2) == holt(y, 2)


def test_holt_winters_tracks_a_clean_seasonal_series() -> None:
    y = [10.0, 20.0, 30.0] * 3  # 3 full cycles of a flat seasonal pattern
    fc = holt_winters(y, 3, 3)
    # It must reproduce the seasonal shape (not a flat line).
    assert fc[0] < fc[1] < fc[2]
    assert abs(fc[0] - 10.0) < 4 and abs(fc[2] - 30.0) < 4


@pytest.mark.parametrize(
    "fn",
    [
        lambda: seasonal_naive([1.0, 2.0, 3.0, 4.0], 2, 3),
        lambda: theil_sen_drift([1.0, 3.0, 2.0, 5.0], 3),
        lambda: ses([1.0, 3.0, 2.0, 5.0], 3),
        lambda: holt([1.0, 3.0, 2.0, 5.0], 3),
        lambda: holt_winters([10.0, 20.0, 30.0] * 3, 3, 3),
    ],
)
def test_every_model_is_deterministic(fn) -> None:  # type: ignore[no-untyped-def]
    assert fn() == fn()


# ── ensemble ──────────────────────────────────────────────────────────────────────────────
def test_ensemble_picks_a_named_candidate_by_backtest() -> None:
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    point, method = ensemble_point(s, 1)
    # Pick-best always returns a nameable candidate (an eligible member or the median).
    assert method in {*eligible_models(s), "ensemble-median"}
    assert len(point) == 1


def test_ensemble_prefers_a_trend_model_on_a_linear_series() -> None:
    # A perfect upward line: a level+trend model must beat the flat/median candidates.
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    _, method = ensemble_point(s, 1)
    assert method in {"holt", "theil-sen"}


def test_ensemble_can_force_a_single_named_model() -> None:
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)])
    point, method = ensemble_point(s, 1, model="seasonal-naive")
    assert method == "seasonal-naive"
    # season 12, 12 points -> seasonal-naive returns the value 12 months ago = the first point.
    assert point[0] == 400.0


# ── forecast_series: structure, PI, projection, determinism ────────────────────────────────
def _co2_like() -> Series:
    return _monthly(
        "co2-ppm",
        12,
        [
            427.87,
            425.48,
            424.37,
            424.87,
            426.46,
            427.49,
            428.62,
            429.35,
            430.15,
            431.12,
            432.34,
            431.44,
        ],
    )


def test_forecast_point_sits_inside_its_own_interval() -> None:
    f = forecast_series(_co2_like(), 3)
    for lo, pt, hi in zip(f.lower, f.point, f.upper, strict=True):
        assert lo <= pt <= hi


def test_prediction_interval_widens_with_horizon() -> None:
    f = forecast_series(_co2_like(), 3)
    widths = [hi - lo for lo, hi in zip(f.lower, f.upper, strict=True)]
    assert widths[0] <= widths[1] <= widths[2]
    assert widths[0] > 0  # a point without an interval is not shippable


def test_forecast_is_deterministic() -> None:
    assert forecast_series(_co2_like(), 3) == forecast_series(_co2_like(), 3)


def test_monthly_periods_roll_over_the_year() -> None:
    s = _monthly("co2-ppm", 12, [400.0 + i for i in range(12)], start="2025-12")
    # 12 points from 2025-12 -> last is 2026-11; next three cross into 2027.
    f = forecast_series(s, 3)
    assert f.periods == ("2026-12", "2027-01", "2027-02")


def test_weekly_periods_advance_seven_days() -> None:
    pts = [("2026-06-05", 1.0), ("2026-06-12", 2.0), ("2026-06-19", 3.0), ("2026-06-26", 4.0)]
    s = _series("eu-gas-storage", "weekly", 52, pts)
    f = forecast_series(s, 2)
    assert f.periods == ("2026-07-03", "2026-07-10")


def test_forecast_returns_named_members() -> None:
    f = forecast_series(_co2_like(), 1)
    assert isinstance(f, Forecast)
    assert "theil-sen" in f.members  # the ensemble names every member it used


# ── the hazard interlock (the load-bearing safety contract) ────────────────────────────────
def test_assert_forecastable_accepts_the_four_tier_a() -> None:
    for key in ("co2-ppm", "arctic-sea-ice", "eu-gas-storage", "us-crude-stocks"):
        assert_forecastable(key)  # must not raise


def test_assert_forecastable_rejects_hazards() -> None:
    for key in ("earthquakes", "wildfire-detections", "natural-events", "radiation-observations"):
        with pytest.raises(HazardInterlockError):
            assert_forecastable(key)


def test_assert_forecastable_rejects_anything_off_the_allow_list() -> None:
    with pytest.raises(HazardInterlockError):
        assert_forecastable("prediction-markets")


def test_forecasting_earthquakes_is_impossible() -> None:
    """The design's headline promise, pinned in code: earthquakes can never be forecast."""
    quakes = _series("earthquakes", "weekly", 52, [("2026-07-17", 12.0), ("2026-07-24", 10.0)])
    with pytest.raises(HazardInterlockError):
        forecast_series(quakes, 1)


# ── input validation ────────────────────────────────────────────────────────────────────────
def test_horizon_must_be_positive() -> None:
    with pytest.raises(ValueError, match="horizon"):
        forecast_series(_co2_like(), 0)


def test_empty_series_cannot_be_forecast() -> None:
    with pytest.raises(ValueError, match="no observations"):
        forecast_series(_series("co2-ppm", "monthly", 12, []), 1)
