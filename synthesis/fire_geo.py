"""Deterministic country attribution for the NASA FIRMS wildfire feed.

IQ #1161 context
----------------
A curator dispatch reported the top-250-by-FRP active-fire concentration by eyeballing
detection *coordinates* ("almost entirely over Russia, the coordinates fall across Siberia")
and asked whether the ingest needed a coordinate->country **reverse-geocode** step for exact
country attribution in the public brief.

It does not. Every ``fireDetections`` row the WorldMonitor NASA-FIRMS feed returns already
carries its own per-detection ``region`` (country) field — so exact per-country counts are a
deterministic tally over the feed's *own* data: no external geocoder, no vendored polygon
set, nothing inferred. This module is that tally.

A row that is missing ``region`` is counted as ``unattributed`` and **never guessed** (the
honest degradation azimuth's doctrine requires). A coordinate->country reverse-geocode would
only ever be the fallback for that missing-region case; it is deliberately NOT added while the
feed ships ``region`` on every row (0 missing across the audited pulls). If a future pull ever
drops ``region`` in bulk, ``FireGeo.unattributed`` surfaces it loudly instead of inventing a
country — and that is the trigger to revisit a real geocode fallback.

Pure stdlib, typed for mypy --strict. Used by ``synthesis/brief_stats.py`` (the site key-figure
band) and citable by the ``azimuth-curator`` role so the weekly brief states exact counts
(e.g. "Russia 243 / Iran 5 / Ukraine 2") rather than an eyeballed "almost entirely Russia".
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["FireGeo", "country_tally"]


@dataclass(frozen=True)
class FireGeo:
    """Deterministic per-country tally of a wildfire detection payload.

    ``counts`` is ranked count-descending, then country-name-ascending (stable, byte-stable
    output). ``total`` is every detection row considered; ``attributed`` carried a usable
    ``region``; ``unattributed`` did not (never guessed).
    """

    counts: tuple[tuple[str, int], ...]
    total: int
    attributed: int
    unattributed: int

    @property
    def dominant(self) -> tuple[str, int] | None:
        """The single most-represented country (name, count), or None when nothing attributed."""
        return self.counts[0] if self.counts else None

    def summary(self, top: int = 3) -> str:
        """Human string for a brief line: ``"Russia 243 / Iran 5 / Ukraine 2"``.

        Appends ``"(+N more countries)"`` when more than ``top`` are present and
        ``"(+N unattributed)"`` when any row lacked a region — the count is always honest
        about what it could and could not attribute.
        """
        if not self.counts:
            if self.total:
                return f"no country attribution ({self.total} detections carry no region field)"
            return "no active-fire detections"
        parts = [f"{name} {n}" for name, n in self.counts[:top]]
        out = " / ".join(parts)
        remaining = len(self.counts) - top
        if remaining > 0:
            out += f" (+{remaining} more countr{'y' if remaining == 1 else 'ies'})"
        if self.unattributed:
            out += f" (+{self.unattributed} unattributed)"
        return out


def _region_of(row: object) -> str | None:
    """The trimmed ``region`` string of one detection row, or None when absent/blank/non-string."""
    if not isinstance(row, dict):
        return None
    value = row.get("region")
    if isinstance(value, str):
        trimmed = value.strip()
        return trimmed or None
    return None


def country_tally(fires: object) -> FireGeo:
    """Tally NASA-FIRMS ``fireDetections`` rows by their own ``region`` (country) field.

    ``fires`` is the decoded ``fireDetections`` list (as ``brief_stats._load`` returns it).
    Anything that is not a list of dict rows yields an empty tally rather than raising, so a
    malformed payload degrades to "no band" upstream instead of crashing the build.
    """
    rows = [r for r in fires if isinstance(r, dict)] if isinstance(fires, list) else []
    tally: dict[str, int] = {}
    attributed = 0
    for row in rows:
        region = _region_of(row)
        if region is None:
            continue
        attributed += 1
        tally[region] = tally.get(region, 0) + 1
    counts = tuple(sorted(tally.items(), key=lambda kv: (-kv[1], kv[0])))
    return FireGeo(
        counts=counts,
        total=len(rows),
        attributed=attributed,
        unattributed=len(rows) - attributed,
    )
