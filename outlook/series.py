#!/usr/bin/env python3
"""outlook.series — extract the Tier-A upstream series out of the L1 source notes.

Phase-1 of the Outlook prediction layer (``docs/prediction-layer-design.md`` §2 / §6 P1).

Several WorldMonitor L1 sources ship their OWN upstream history inside a single daily pull,
so a forecast-ready numeric series exists *today* without waiting for azimuth's own
day-by-day accumulation. This module reads those embedded series out of the committed L1
notes into a clean, chronological :class:`Series` of ``(period, value)`` observations.

Design invariants (all from the design doc):

- **Tier-A ONLY.** A hard-coded allow-list of exactly four forecastable series (T1-T4,
  :data:`TIER_A`). This same allow-list is the *hazard interlock* the forecaster asserts
  against — a series that is not on it can never be forecast (``outlook.forecast`` enforces
  this in code, and a unit test pins that earthquakes can never enter the path).
- **Pure stdlib, deterministic.** The same committed L1 note yields a byte-identical series;
  no third-party runtime dependency (repo Quality Rule #6).
- **Fail-soft.** A missing note / field / malformed cell yields ``None`` for that series,
  never a crash — one broken feed must not take the layer down.
- **Upsert-by-period.** When the same reporting period appears more than once (e.g. a later
  L1 day revises an earlier week), the LATEST value for that period wins — matching how the
  fact-briefs already treat these revisable EIA / GIE feeds.

The note-cell reader mirrors ``synthesis.brief_stats`` (the L1 notes store each field as a
``| field | value |`` markdown row whose value is a JSON blob), so the same four series that
already render as brief sparklines are the ones forecast here — one source of truth.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

__all__ = [
    "FORECASTABLE_KEYS",
    "HAZARD_SOURCE_KEYS",
    "SPEC_BY_KEY",
    "TIER_A",
    "Series",
    "SeriesSpec",
    "extract_all",
    "extract_latest",
    "extract_series",
    "is_forecastable",
    "latest_day",
]

_FIELD_RE = re.compile(r"^\| (\w+) \| (.*) \|$")

# A ISO period sorts lexicographically in chronological order for both the monthly
# ("2026-07") and weekly ("2026-07-24") series, so ordering is a plain string sort.
_ISO_PERIOD_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")


@dataclass(frozen=True)
class SeriesSpec:
    """The parse recipe for one forecastable Tier-A series.

    ``container`` is the top-level ``| field |`` name in the L1 note. When ``array`` is set
    the container is a JSON object and the observation list lives at ``container[array]``
    (the monthly climate series); when ``array`` is ``None`` the container field *is* the
    list itself (the weekly energy series). ``divisor`` scales the raw value so the stored
    unit matches the human label (US crude ships thousand-barrels; ÷1000 -> million barrels,
    the same transform ``synthesis.brief_stats`` uses for the brief band).
    """

    key: str
    label: str
    unit: str
    cadence: str  # "monthly" | "weekly"
    season: int  # observations per annual cycle (12 monthly, 52 weekly); 1 == non-seasonal
    source_key: str
    container: str
    array: str | None
    period_key: str
    value_key: str
    divisor: float = 1.0


@dataclass(frozen=True)
class Series:
    """A clean, chronological, forecast-ready numeric series."""

    key: str
    label: str
    unit: str
    cadence: str
    season: int
    source_key: str
    points: tuple[tuple[str, float], ...]  # (period, value), oldest -> newest, upserted

    def __len__(self) -> int:
        return len(self.points)

    @property
    def periods(self) -> list[str]:
        return [p for p, _ in self.points]

    @property
    def values(self) -> list[float]:
        return [v for _, v in self.points]

    @property
    def latest(self) -> tuple[str, float] | None:
        return self.points[-1] if self.points else None


# ── the Tier-A allow-list (T1-T4) — also the forecast hazard interlock ────────────────────
TIER_A: tuple[SeriesSpec, ...] = (
    SeriesSpec(
        key="co2-ppm",
        label="Atmospheric CO2 (Mauna Loa)",
        unit="ppm",
        cadence="monthly",
        season=12,
        source_key="co2-monitoring",
        container="monitoring",
        array="trend12m",
        period_key="month",
        value_key="ppm",
    ),
    SeriesSpec(
        key="arctic-sea-ice",
        label="Arctic sea-ice extent",
        unit="Mkm2",
        cadence="monthly",
        season=12,
        source_key="sea-ice-extent",
        container="data",
        array="iceTrend12m",
        period_key="month",
        value_key="extentMkm2",
    ),
    SeriesSpec(
        key="eu-gas-storage",
        label="EU gas storage",
        unit="Bcf",
        cadence="weekly",
        season=52,
        source_key="natural-gas-storage-eu",
        container="weeks",
        array=None,
        period_key="period",
        value_key="storBcf",
    ),
    SeriesSpec(
        key="us-crude-stocks",
        label="US crude oil inventories",
        unit="Mb",
        cadence="weekly",
        season=52,
        source_key="crude-oil-inventories",
        container="weeks",
        array=None,
        period_key="period",
        value_key="stocksMb",
        divisor=1000.0,  # raw feed is thousand-barrels -> million barrels (matches the brief band)
    ),
)

SPEC_BY_KEY: dict[str, SeriesSpec] = {s.key: s for s in TIER_A}
FORECASTABLE_KEYS: frozenset[str] = frozenset(SPEC_BY_KEY)

# Source keys that are hazard / sensitive-event streams and must NEVER be forecast, honored
# in code so the "we don't forecast earthquakes" promise is enforced, not merely documented.
HAZARD_SOURCE_KEYS: frozenset[str] = frozenset(
    {
        "earthquakes",
        "wildfire-detections",
        "natural-events",
        "radiation-observations",
        "thermal-escalations",
    }
)


def is_forecastable(key: str) -> bool:
    """True iff ``key`` is one of the four Tier-A series on the allow-list."""
    return key in FORECASTABLE_KEYS


# ── note reader (mirrors synthesis.brief_stats — one source of truth for the cell format) ──
def _read_fields(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = _FIELD_RE.match(line.rstrip())
            if m and m.group(1) != "field":
                out[m.group(1)] = m.group(2)
    except OSError:
        pass
    return out


def _load_field(day_dir: Path, source_key: str, field: str) -> Any:
    raw = _read_fields(day_dir / f"{source_key}.md").get(field)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return None


def _to_num(x: Any) -> float | None:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if v == v and v not in (float("inf"), float("-inf")) else None  # reject NaN/inf


def _rows_for(day_dir: Path, spec: SeriesSpec) -> list[dict[str, Any]] | None:
    """Pull the raw observation-row list for ``spec`` out of one L1 day, or None."""
    container = _load_field(day_dir, spec.source_key, spec.container)
    if container is None:
        return None
    if spec.array is None:
        rows = container
    elif isinstance(container, dict):
        rows = container.get(spec.array)
    else:
        return None
    if not isinstance(rows, list):
        return None
    return [r for r in rows if isinstance(r, dict)]


def _build(spec: SeriesSpec, observations: list[tuple[str, float]]) -> Series:
    """Upsert ``(period, value)`` observations (latest wins per period) into a Series."""
    upsert: dict[str, float] = {}
    for period, value in observations:
        upsert[period] = value  # later observation for a period overrides an earlier one
    points = tuple(sorted(upsert.items(), key=lambda kv: kv[0]))
    return Series(
        key=spec.key,
        label=spec.label,
        unit=spec.unit,
        cadence=spec.cadence,
        season=spec.season,
        source_key=spec.source_key,
        points=points,
    )


def extract_series(day_dir: Path, spec: SeriesSpec) -> Series | None:
    """Extract one Tier-A series from a single L1 day directory, or None (fail-soft).

    Rows missing the period/value key, carrying a non-numeric value, or a non-ISO period are
    skipped individually; an entirely missing field / malformed note yields ``None``.
    """
    rows = _rows_for(day_dir, spec)
    if rows is None:
        return None
    obs: list[tuple[str, float]] = []
    for row in rows:
        period = row.get(spec.period_key)
        if not isinstance(period, str) or not _ISO_PERIOD_RE.match(period):
            continue
        value = _to_num(row.get(spec.value_key))
        if value is None:
            continue
        obs.append((period, value / spec.divisor))
    if not obs:
        return None
    return _build(spec, obs)


def extract_all(day_dir: Path) -> dict[str, Series]:
    """Extract every Tier-A series present in ``day_dir`` (fail-soft; skips missing ones)."""
    out: dict[str, Series] = {}
    for spec in TIER_A:
        series = extract_series(day_dir, spec)
        if series is not None:
            out[spec.key] = series
    return out


def latest_day(sources_dir: Path) -> Path | None:
    """Newest ``YYYY-MM-DD`` L1 day directory under ``sources_dir``, or None."""
    if not sources_dir.is_dir():
        return None
    days = sorted(
        (p for p in sources_dir.iterdir() if p.is_dir() and _ISO_PERIOD_RE.match(p.name)),
        key=lambda p: p.name,
    )
    return days[-1] if days else None


def extract_latest(sources_dir: Path) -> dict[str, Series]:
    """Convenience: extract all Tier-A series from the newest committed L1 day."""
    day = latest_day(sources_dir)
    return extract_all(day) if day is not None else {}
