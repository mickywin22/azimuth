#!/usr/bin/env python3
"""outlook.backtest — rolling-origin score + the ship-bar — design §5 / §6 P3.

The success metric that decides whether the Outlook layer is worth publishing (design §5),
computed by a deterministic rolling-origin backtest over the committed history:

- **MASE** — mean absolute scaled error vs the seasonal-naive baseline (scale-free, the
  standard forecast metric). Target: **< 1.0** (the ensemble beats naive).
- **sMAPE** — reported alongside for human readability.
- **PI coverage** — the empirical share of actuals that fell inside the published 80%
  interval. Target: **[70%, 90%]** (honest calibration, neither over- nor under-confident).

**Ship-bar (§5):** the ensemble beats naive on **>= 3 of 4** series AND holds coverage in
[70,90]% on **>= 3 of 4**. **Honesty fallback:** a series that cannot beat naive is scored
"seasonal-naive (fallback)" — Outlook then publishes the naive baseline itself, labelled,
rather than a model that is worse than naive just to look sophisticated.

Everything is scored against the *same* published forecast the layer would ship (each origin
re-runs :func:`outlook.forecast.forecast_series`), so the score is honest about the exact
method, PI included. Pure stdlib, deterministic — the score is a reproducible public artifact.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import TYPE_CHECKING

from outlook.forecast import (
    _slice,
    expanding_origins,
    forecast_series,
    seasonal_naive,
)

if TYPE_CHECKING:
    from outlook.series import Series

__all__ = [
    "BacktestRun",
    "ScoreCard",
    "ShipBar",
    "coverage",
    "mase",
    "naive_scale",
    "rolling_origin",
    "score_all",
    "score_series",
    "ship_bar",
    "smape",
]

_COVERAGE_LOW = 0.70
_COVERAGE_HIGH = 0.90
_SHIP_MIN_OF_FOUR = 3


# ── standalone metrics (hand-checkable, independent of the ensemble) ─────────────────────────
def naive_scale(insample: list[float], season: int) -> tuple[float, int]:
    """In-sample MAE of the seasonal-naive method — the MASE denominator.

    Falls back to the lag-1 naive when the history is shorter than one full season (the case
    for today's 8-12 point Tier-A series), so the scale is always computable. Returns
    (scale, effective-lag).
    """
    m = season if (season >= 1 and len(insample) > season) else 1
    diffs = [abs(insample[t] - insample[t - m]) for t in range(m, len(insample))]
    return (statistics.fmean(diffs) if diffs else 0.0), m


def mase(actuals: list[float], forecasts: list[float], insample: list[float], season: int) -> float:
    """Mean absolute scaled error vs the seasonal-naive baseline (design §5).

    < 1 means the forecast beats naive. A zero scale (a flat in-sample series) yields 0.0 when
    the forecast is perfect, else infinity — an honest signal, never a silent divide-by-zero.
    """
    if not actuals:
        return float("nan")
    scale, _ = naive_scale(insample, season)
    numerator = statistics.fmean([abs(a - f) for a, f in zip(actuals, forecasts, strict=True)])
    if scale == 0.0:
        return 0.0 if numerator == 0.0 else float("inf")
    return numerator / scale


def smape(actuals: list[float], forecasts: list[float]) -> float:
    """Symmetric MAPE (%) — a bounded, human-readable error, 0 (perfect) .. 200 (worst)."""
    if not actuals:
        return float("nan")
    terms = []
    for a, f in zip(actuals, forecasts, strict=True):
        denom = abs(a) + abs(f)
        terms.append(0.0 if denom == 0 else 2 * abs(a - f) / denom)
    return 100 * statistics.fmean(terms)


def coverage(actuals: list[float], lowers: list[float], uppers: list[float]) -> float:
    """Empirical share (0..1) of actuals that fell within their prediction interval."""
    if not actuals:
        return float("nan")
    inside = sum(
        lo <= a <= hi for a, lo, hi in zip(actuals, lowers, uppers, strict=True)
    )
    return inside / len(actuals)


# ── rolling-origin backtest ──────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class BacktestRun:
    """The per-origin one-step-ahead record a score is computed from."""

    periods: tuple[str, ...]
    actuals: tuple[float, ...]
    forecasts: tuple[float, ...]
    lowers: tuple[float, ...]
    uppers: tuple[float, ...]
    naive: tuple[float, ...]


def rolling_origin(series: Series, min_train: int = 4, model: str | None = None) -> BacktestRun:
    """Expanding-window one-step-ahead backtest, scoring the *published* forecast each origin.

    At each cutoff the model trains on the observed prefix and forecasts the next single point
    with its 80% PI; the seasonal-naive comparator is scored on the same origins.
    """
    y = series.values
    periods = series.periods
    _, m = naive_scale(y, series.season)
    p_out, a_out, f_out, lo_out, hi_out, n_out = [], [], [], [], [], []
    for cut in expanding_origins(len(y), min_train):
        train = _slice(series, cut)
        fc = forecast_series(train, 1, model=model)
        p_out.append(periods[cut])
        a_out.append(y[cut])
        f_out.append(fc.point[0])
        lo_out.append(fc.lower[0])
        hi_out.append(fc.upper[0])
        n_out.append(seasonal_naive(train.values, m, 1)[0])
    return BacktestRun(
        periods=tuple(p_out),
        actuals=tuple(a_out),
        forecasts=tuple(f_out),
        lowers=tuple(lo_out),
        uppers=tuple(hi_out),
        naive=tuple(n_out),
    )


# ── the per-series score card + the ship-bar ─────────────────────────────────────────────────
@dataclass(frozen=True)
class ScoreCard:
    """One series' rolling-origin score against the §5 targets."""

    series_key: str
    label: str
    unit: str
    n_test: int
    mase: float
    smape: float
    coverage: float
    beats_naive: bool
    coverage_ok: bool
    recommended: str  # "ensemble" | "seasonal-naive (fallback)" — the honesty rule (§5)


def score_series(series: Series, min_train: int = 4, model: str | None = None) -> ScoreCard:
    """Backtest one Tier-A series and score it against the §5 targets + honesty fallback."""
    run = rolling_origin(series, min_train=min_train, model=model)
    actuals = list(run.actuals)
    m_val = mase(actuals, list(run.forecasts), series.values, series.season)
    s_val = smape(actuals, list(run.forecasts))
    c_val = coverage(actuals, list(run.lowers), list(run.uppers))
    beats = m_val < 1.0
    cov_ok = _COVERAGE_LOW <= c_val <= _COVERAGE_HIGH
    return ScoreCard(
        series_key=series.key,
        label=series.label,
        unit=series.unit,
        n_test=len(actuals),
        mase=m_val,
        smape=s_val,
        coverage=c_val,
        beats_naive=beats,
        coverage_ok=cov_ok,
        recommended="forecast" if beats else "seasonal-naive (fallback)",
    )


def score_all(series_map: dict[str, Series], min_train: int = 4) -> dict[str, ScoreCard]:
    """Score every series in a map (e.g. the four Tier-A series from one L1 day)."""
    return {key: score_series(s, min_train=min_train) for key, s in series_map.items()}


@dataclass(frozen=True)
class ShipBar:
    """The go / no-go verdict for the build sprint (design §5)."""

    total: int
    mase_pass: int
    coverage_pass: int
    required: int
    passed: bool


def ship_bar(cards: dict[str, ScoreCard]) -> ShipBar:
    """The ensemble must beat naive on >= 3 of 4 AND cover [70,90]% on >= 3 of 4 (design §5)."""
    total = len(cards)
    mase_pass = sum(c.beats_naive for c in cards.values())
    coverage_pass = sum(c.coverage_ok for c in cards.values())
    required = _SHIP_MIN_OF_FOUR if total >= 4 else total
    passed = total > 0 and mase_pass >= required and coverage_pass >= required
    return ShipBar(
        total=total,
        mase_pass=mase_pass,
        coverage_pass=coverage_pass,
        required=required,
        passed=passed,
    )
