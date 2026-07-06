#!/usr/bin/env python3
"""Deterministic, build-time inline-SVG sparklines for the azimuth site.

No JavaScript, no charting library, no runtime fetch: the sparkline is rendered to a
self-contained ``<svg>`` string at build time from a plain list of numbers, so it appears
instantly, prints, and works on the static ``file://`` preview. The vault doctrine says a
KPI is a curve over time, not a bare number — this is that rule made literal on the public
landing surface.

Two pieces:

* :func:`sparkline_svg` — pure ``list[number] -> <svg>`` renderer (area + line + last-point
  dot), normalised to its own min/max, degrading cleanly for the empty / single / all-equal
  cases. Colours are inherited via ``currentColor`` so the caller styles it in CSS.
* :func:`daily_source_counts` — the site's honest data series: how many L1 source notes the
  published bundle rests on per ingest day, site-wide and per (surfaced) channel. Held themes
  are excluded, exactly as the rest of the site excludes them.

Both are pure functions of the vault tree — deterministic, no clock, no randomness — so the
same vault always renders the same markup (byte-stable builds, testable output).
"""

from __future__ import annotations

import html
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from synthesis.site_build import (
    _DAY_DIR_RE,
    DEFAULT_VAULT,
    held_source_keys,
)

if TYPE_CHECKING:
    from pathlib import Path


def _fmt(n: float) -> str:
    """Compact coordinate string: integers stay integer, floats keep 2 dp, no trailing zeros."""
    if n == int(n):
        return str(int(n))
    return f"{n:.2f}".rstrip("0").rstrip(".")


def sparkline_svg(
    values: list[float],
    *,
    width: int = 132,
    height: int = 30,
    pad: float = 3.0,
    label: str = "",
    cls: str = "spark",
) -> str:
    """Render ``values`` as a self-contained inline-SVG sparkline (area + line + end dot).

    The path is normalised to the series' own ``min..max`` inside a ``pad``-inset box, so the
    shape reads regardless of absolute scale. Degenerate inputs degrade instead of raising:
    an empty series returns ``""``; a single point or an all-equal series draws a flat mid-line
    (there is no trend to show, and saying so honestly beats inventing one).

    ``label`` becomes the accessible ``<title>`` (screen readers read the trend); the SVG
    itself is ``role="img"``. All theme colour comes from ``currentColor`` — style ``.spark-line``
    / ``.spark-area`` / ``.spark-dot`` (or the ``cls`` you pass) in CSS.
    """
    if not values:
        return ""
    n = len(values)
    lo, hi = min(values), max(values)
    span = hi - lo
    inner_w = width - 2 * pad
    inner_h = height - 2 * pad

    def x(i: int) -> float:
        return pad if n == 1 else pad + (i / (n - 1)) * inner_w

    def y(v: float) -> float:
        # No spread (single point or flat series) -> sit on the mid-line, not a divide-by-zero.
        if span == 0:
            return height / 2
        return pad + (1 - (v - lo) / span) * inner_h

    pts = [(x(i), y(v)) for i, v in enumerate(values)]
    line_pts = " ".join(f"{_fmt(px)},{_fmt(py)}" for px, py in pts)
    # Area fill: the line, then down to the baseline and back — a soft ground under the trend.
    area_d = (
        f"M{_fmt(pts[0][0])},{_fmt(height - pad)} "
        + " ".join(f"L{_fmt(px)},{_fmt(py)}" for px, py in pts)
        + f" L{_fmt(pts[-1][0])},{_fmt(height - pad)} Z"
    )
    lx, ly = pts[-1]
    title = f"<title>{html.escape(label)}</title>" if label else ""
    role = ' role="img"' if label else ' aria-hidden="true"'
    return (
        f'<svg class="{html.escape(cls)}" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" preserveAspectRatio="none"{role}>'
        f"{title}"
        f'<path class="spark-area" d="{area_d}"/>'
        f'<polyline class="spark-line" fill="none" points="{line_pts}"/>'
        f'<circle class="spark-dot" cx="{_fmt(lx)}" cy="{_fmt(ly)}" r="2.4"/>'
        f"</svg>"
    )


@dataclass
class PulseSeries:
    """Per-ingest-day L1 source-note counts for the published (non-held) bundle."""

    days: list[str] = field(default_factory=list)  # chronological YYYY-MM-DD
    total: list[int] = field(default_factory=list)  # site-wide notes that day
    per_theme: dict[str, list[int]] = field(default_factory=dict)  # theme -> notes/day


def _source_theme_map(registry: dict[str, Any]) -> dict[str, str]:
    """source key (== note filename stem) -> theme, from the registry."""
    return {
        src["key"]: src.get("theme", "") for src in registry.get("sources", []) if src.get("key")
    }


def daily_source_counts(
    vault_dir: Path = DEFAULT_VAULT,
    registry: dict[str, Any] | None = None,
    *,
    days: int = 12,
) -> PulseSeries:
    """Count published L1 source notes per ingest day — site-wide and per surfaced channel.

    Walks the dated ``01 Sources/<YYYY-MM-DD>/`` folders, keeps the most recent ``days`` of
    them (chronological), and counts the ``.md`` notes on each day. Held-theme source keys are
    excluded so the public series never reflects paused channels — the same exclusion the site
    itself applies. Returns a :class:`PulseSeries`; an empty / dateless vault yields empty lists.
    """
    registry = registry or {}
    sources_dir = vault_dir / "01 Sources"
    if not sources_dir.is_dir():
        return PulseSeries()
    skip = held_source_keys(registry)
    theme_of = _source_theme_map(registry)

    dated = sorted(
        (d for d in sources_dir.iterdir() if d.is_dir() and _DAY_DIR_RE.match(d.name)),
        key=lambda d: d.name,
    )[-days:]

    series = PulseSeries(days=[d.name for d in dated])
    themes_seen: set[str] = {t for t in theme_of.values() if t and t not in _held_themes(registry)}
    per_theme: dict[str, list[int]] = {t: [] for t in sorted(themes_seen)}

    for d in dated:
        total = 0
        day_theme: dict[str, int] = {t: 0 for t in per_theme}
        for note in d.glob("*.md"):
            key = note.stem
            if key == "README" or key in skip:
                continue
            total += 1
            theme = theme_of.get(key, "")
            if theme in day_theme:
                day_theme[theme] += 1
        series.total.append(total)
        for t in per_theme:
            per_theme[t].append(day_theme[t])
    series.per_theme = per_theme
    return series


def _held_themes(registry: dict[str, Any]) -> set[str]:
    """Held theme names (kept local to avoid importing more than needed)."""
    themes = registry.get("themes", {})
    return {name for name, meta in themes.items() if meta.get("brief_held")}
