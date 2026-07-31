#!/usr/bin/env python3
"""outlook.forecast — the glass-box baseline ensemble + prediction interval — design §4 / §6 P2.

Given a Tier-A :class:`~outlook.series.Series`, produce a short-horizon point forecast plus an
80% prediction interval, using a deterministic, no-LLM ensemble of transparent classical
baselines. Reproducibility is the moat: the same committed L1 series yields a byte-identical
forecast, so the whole path is auditable — the honest inverse of a black-box forecast.

The ensemble (design §4.1), each robust on the 8-12 points a Tier-A series carries:

- **seasonal-naive** — the value one full cycle ago (also the reference the score is scaled
  against); eligible only once a full season is observed.
- **Theil-Sen drift** — median-of-pairwise-slopes robust linear trend, extrapolated.
- **SES** — simple (level-only) exponential smoothing, for near-flat series.
- **Holt** — double ES (level + trend), for the trended series.
- **Holt-Winters** — triple ES (level + trend + season), guarded to >= 2 full cycles and so
  dormant on today's short Tier-A history — it falls back to Holt, honestly.

The point forecast is the **median of the eligible members** (robust to any one misfiring),
or a single named model when the backtester (P3) picks a decisive best. The 80% interval is a
**seeded residual bootstrap** over an expanding-window one-step backtest — mandatory, because
a point forecast without a published interval is a false-precision claim (the exact thing
azimuth criticizes in the foil).

**Hazard interlock (design §4.4):** :func:`assert_forecastable` rejects any series not on the
Tier-A allow-list — earthquakes and every hazard/sensitive stream can never enter this path,
enforced in code and pinned by a unit test.
"""

from __future__ import annotations

import datetime as dt
import random
import statistics
from dataclasses import dataclass
from typing import TYPE_CHECKING

from outlook.series import FORECASTABLE_KEYS, HAZARD_SOURCE_KEYS, Series

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

__all__ = [
    "Forecast",
    "HazardInterlockError",
    "assert_forecastable",
    "eligible_models",
    "ensemble_point",
    "forecast_series",
    "holt",
    "holt_winters",
    "seasonal_naive",
    "ses",
    "theil_sen_drift",
]

# Determinism knobs — no time / no unseeded randomness anywhere on the forecast path.
_SEED = 20260731
_BOOTSTRAP_DRAWS = 2000
_MIN_TRAIN = 4  # smallest training window an expanding-origin backtest will start from
_ALPHA_GRID = (0.1, 0.3, 0.5, 0.7, 0.9)
_BETA_GRID = (0.1, 0.3, 0.5, 0.7)


class HazardInterlockError(ValueError):
    """Raised when a forecast is attempted on a series outside the Tier-A allow-list."""


def assert_forecastable(series_key: str) -> None:
    """Guard the forecast path: only the four Tier-A series may ever be forecast.

    This is the code-level enforcement of the design's "we do not forecast earthquakes"
    promise (§4.4) — a hazard/sensitive stream is rejected here, before any model runs.
    """
    if series_key in HAZARD_SOURCE_KEYS or series_key not in FORECASTABLE_KEYS:
        raise HazardInterlockError(
            f"series {series_key!r} is not a Tier-A forecastable series; "
            "hazards and sensitive-event streams are never forecast (design §4.4)"
        )


# ── classical baseline models — each: history -> forecast path of length h ─────────────────
def seasonal_naive(y: list[float], season: int, h: int) -> list[float]:
    """Repeat the last full seasonal cycle; falls back to the last value if < 1 cycle."""
    if season <= 1 or len(y) < season:
        return [y[-1]] * h
    return [y[len(y) - season + (i % season)] for i in range(h)]


def theil_sen_drift(y: list[float], h: int) -> list[float]:
    """Robust linear trend: median of pairwise slopes, extrapolated from a robust intercept."""
    n = len(y)
    if n < 2:
        return [y[-1]] * h
    slopes = [(y[j] - y[i]) / (j - i) for i in range(n) for j in range(i + 1, n)]
    slope = statistics.median(slopes)
    intercept = statistics.median([y[i] - slope * i for i in range(n)])
    return [intercept + slope * (n - 1 + k) for k in range(1, h + 1)]


def _ses_level(y: list[float], alpha: float) -> tuple[float, float]:
    """Return (final level, in-sample one-step SSE) for a given alpha."""
    level = y[0]
    sse = 0.0
    for t in range(1, len(y)):
        err = y[t] - level
        sse += err * err
        level = alpha * y[t] + (1 - alpha) * level
    return level, sse


def ses(y: list[float], h: int) -> list[float]:
    """Simple exponential smoothing; alpha chosen by in-sample one-step SSE (deterministic)."""
    if len(y) < 2:
        return [y[-1]] * h
    best_alpha = min(_ALPHA_GRID, key=lambda a: _ses_level(y, a)[1])
    level, _ = _ses_level(y, best_alpha)
    return [level] * h


def _holt_fit(y: list[float], alpha: float, beta: float) -> tuple[float, float, float]:
    """Return (final level, final trend, in-sample one-step SSE) for given alpha/beta."""
    level = y[0]
    trend = y[1] - y[0]
    sse = 0.0
    for t in range(1, len(y)):
        pred = level + trend
        err = y[t] - pred
        sse += err * err
        new_level = alpha * y[t] + (1 - alpha) * (level + trend)
        trend = beta * (new_level - level) + (1 - beta) * trend
        level = new_level
    return level, trend, sse


def holt(y: list[float], h: int) -> list[float]:
    """Holt double exponential smoothing (level + trend); alpha/beta by in-sample SSE."""
    if len(y) < 3:
        return theil_sen_drift(y, h)
    best = min(
        ((a, b) for a in _ALPHA_GRID for b in _BETA_GRID),
        key=lambda ab: _holt_fit(y, ab[0], ab[1])[2],
    )
    level, trend, _ = _holt_fit(y, best[0], best[1])
    return [level + k * trend for k in range(1, h + 1)]


def holt_winters(y: list[float], season: int, h: int) -> list[float]:
    """Additive triple ES; guarded to >= 2 full cycles, else falls back to Holt (design §4.1)."""
    if season <= 1 or len(y) < 2 * season:
        return holt(y, h)
    # Additive Holt-Winters with simple seasonal init from the first cycle.
    alpha, beta, gamma = 0.3, 0.1, 0.3
    seasonals = [y[i] - statistics.fmean(y[:season]) for i in range(season)]
    level = statistics.fmean(y[:season])
    trend = (statistics.fmean(y[season : 2 * season]) - statistics.fmean(y[:season])) / season
    for t in range(len(y)):
        val = y[t]
        s = seasonals[t % season]
        new_level = alpha * (val - s) + (1 - alpha) * (level + trend)
        trend = beta * (new_level - level) + (1 - beta) * trend
        seasonals[t % season] = gamma * (val - new_level) + (1 - gamma) * s
        level = new_level
    return [level + k * trend + seasonals[(len(y) + k - 1) % season] for k in range(1, h + 1)]


# ── ensemble ────────────────────────────────────────────────────────────────────────────────
def eligible_models(series: Series) -> dict[str, Callable[[int], list[float]]]:
    """The ensemble members that are valid for this series' length/seasonality.

    Returns a name -> bound-forecast-function (takes horizon, returns path) mapping, so the
    chosen member is always nameable in the brief — no hidden blending.
    """
    y = series.values
    season = series.season
    members: dict[str, Callable[[int], list[float]]] = {}
    if len(y) >= 2:
        members["theil-sen"] = lambda h: theil_sen_drift(y, h)
        members["ses"] = lambda h: ses(y, h)
    if len(y) >= 3:
        members["holt"] = lambda h: holt(y, h)
    if season > 1 and len(y) >= season:
        members["seasonal-naive"] = lambda h: seasonal_naive(y, season, h)
    if season > 1 and len(y) >= 2 * season:
        members["holt-winters"] = lambda h: holt_winters(y, season, h)
    if not members:  # degenerate single-point series -> honest naive
        members["naive"] = lambda h: [y[-1]] * h
    return members


def ensemble_point(series: Series, h: int, model: str | None = None) -> tuple[list[float], str]:
    """Point forecast + the method label.

    ``model=None`` -> median of the eligible members (robust). A named ``model`` -> that single
    member (the backtester's pick-best path, §4.2). Returns (path, method-label).
    """
    members = eligible_models(series)
    if model is not None and model in members:
        return members[model](h), model
    paths = [fn(h) for fn in members.values()]
    point = [statistics.median([p[k] for p in paths]) for k in range(h)]
    return point, "ensemble-median"


# ── expanding-origin backtest residuals (shared with outlook.backtest) ──────────────────────
def expanding_origins(n: int, min_train: int = _MIN_TRAIN) -> Iterator[int]:
    """Yield each training-set cutoff for an expanding-window one-step backtest."""
    yield from range(max(min_train, 1), n)


def _one_step_residuals(series: Series) -> list[float]:
    """Ensemble one-step-ahead residuals over an expanding window (drives the bootstrap PI)."""
    y = series.values
    resid: list[float] = []
    for cut in expanding_origins(len(y)):
        train = _slice(series, cut)
        pred, _ = ensemble_point(train, 1)
        resid.append(y[cut] - pred[0])
    return resid


def _slice(series: Series, cut: int) -> Series:
    """A copy of ``series`` truncated to its first ``cut`` observations (for backtesting)."""
    return Series(
        key=series.key,
        label=series.label,
        unit=series.unit,
        cadence=series.cadence,
        season=series.season,
        source_key=series.source_key,
        points=series.points[:cut],
    )


# ── prediction interval (seeded residual bootstrap) ─────────────────────────────────────────
def _bootstrap_pi(
    point: list[float], residuals: list[float], level: float
) -> tuple[list[float], list[float]]:
    """80% PI via seeded residual bootstrap; error grows with horizon (accumulated draws).

    Residuals are median-centered before resampling: the point forecast is already our best
    central estimate, so the interval expresses the *spread* of one-step error around it
    (and always contains the point). Any systematic bias in the point is judged separately by
    MASE in the backtester (P3), not smuggled into the interval's centre.
    """
    lo_q, hi_q = (1 - level) / 2, 1 - (1 - level) / 2
    if len(residuals) < 2:
        return _fallback_pi(point, residuals, level)
    centre = statistics.median(residuals)
    centered = [r - centre for r in residuals]
    rng = random.Random(_SEED)
    lower: list[float] = []
    upper: list[float] = []
    for k in range(len(point)):
        cumulative = [
            sum(centered[rng.randrange(len(centered))] for _ in range(k + 1))
            for _ in range(_BOOTSTRAP_DRAWS)
        ]
        cumulative.sort()
        lower.append(point[k] + _quantile(cumulative, lo_q))
        upper.append(point[k] + _quantile(cumulative, hi_q))
    return lower, upper


def _fallback_pi(
    point: list[float], residuals: list[float], level: float
) -> tuple[list[float], list[float]]:
    """When too few residuals exist, a symmetric band from residual spread (still honest)."""
    z = 1.2816  # ~80% two-sided normal quantile
    spread = abs(residuals[0]) if residuals else 0.0
    lower = [p - z * spread * (k + 1) ** 0.5 for k, p in enumerate(point)]
    upper = [p + z * spread * (k + 1) ** 0.5 for k, p in enumerate(point)]
    return lower, upper


def _quantile(sorted_values: list[float], q: float) -> float:
    """Linear-interpolation quantile of an already-sorted list."""
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = q * (len(sorted_values) - 1)
    lo = int(pos)
    frac = pos - lo
    if lo + 1 >= len(sorted_values):
        return sorted_values[-1]
    return sorted_values[lo] * (1 - frac) + sorted_values[lo + 1] * frac


# ── future period projection ────────────────────────────────────────────────────────────────
def _next_periods(series: Series, h: int) -> list[str]:
    """Project the next ``h`` period labels on the series' own clock (monthly or weekly)."""
    last = series.periods[-1]
    if series.cadence == "monthly":
        year, month = (int(x) for x in last.split("-")[:2])
        out: list[str] = []
        for _ in range(h):
            month += 1
            if month > 12:
                month = 1
                year += 1
            out.append(f"{year:04d}-{month:02d}")
        return out
    # weekly: advance 7 days from the last reporting date
    base = dt.date.fromisoformat(last)
    return [(base + dt.timedelta(days=7 * k)).isoformat() for k in range(1, h + 1)]


# ── the Forecast result + top-level entry point ─────────────────────────────────────────────
@dataclass(frozen=True)
class Forecast:
    """A published, auditable forecast: point + 80% interval + the named method behind it."""

    series_key: str
    label: str
    unit: str
    method: str
    members: tuple[str, ...]
    horizon: int
    periods: tuple[str, ...]
    point: tuple[float, ...]
    lower: tuple[float, ...]
    upper: tuple[float, ...]
    pi_level: float = 0.8


def forecast_series(series: Series, h: int, model: str | None = None) -> Forecast:
    """Forecast one Tier-A series ``h`` steps ahead with an 80% PI (design §3 / §4).

    Passes through the hazard interlock first, so a non-Tier-A series raises before any model
    runs. ``model`` optionally forces a single named member (the backtester's pick-best path).
    """
    assert_forecastable(series.key)
    if h < 1:
        raise ValueError("horizon must be >= 1")
    if not series.values:
        raise ValueError(f"series {series.key!r} has no observations to forecast")
    point, method = ensemble_point(series, h, model=model)
    residuals = _one_step_residuals(series)
    lower, upper = _bootstrap_pi(point, residuals, 0.8)
    return Forecast(
        series_key=series.key,
        label=series.label,
        unit=series.unit,
        method=method,
        members=tuple(eligible_models(series)),
        horizon=h,
        periods=tuple(_next_periods(series, h)),
        point=tuple(point),
        lower=tuple(lower),
        upper=tuple(upper),
    )
