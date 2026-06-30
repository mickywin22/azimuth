#!/usr/bin/env python3
"""Deterministic cross-theme bridge scanner for the *World Watch Weekly* meta-brief.

A static OKF bundle stores one brief per theme. What it *cannot* do is show the
connections BETWEEN themes. This module computes those connections deterministically
from the live L1 source notes, so the cross-theme brief that narrates them stays inside
the synthesis contract — every cross-channel claim links back to the L1 notes it rests on.

The unit of connection is a **bridge**: a named region that the latest L1 ingest day
mentions under **>=2 editorially-clean themes**. A bridge is data-backed by construction
— the region literally appears in each theme's L1 note (whole-word matched against a
fixed gazetteer, the same one ``scripts/build_graph.py`` uses for its gold cross-theme
edges), never inferred. The scanner also reports whether any bridge region intersects the
**physical energy-supply core** (US crude inventories / EU gas storage) — the only place a
geophysical event could show *observed* reach into the energy balances — so the brief can
state an honest reach verdict instead of a speculative one.

Pure stdlib; the CLI (``scripts/build_cross_theme.py``) does the file/git I/O and rendering.
Verdict/scan logic lives here so it can be unit-tested in isolation (mirrors
``synthesis/lint.py`` vs ``scripts/check_synthesis.py``).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

# --- entity gazetteer --------------------------------------------------------
# Mirrors ``scripts/build_graph.py`` ``_REGIONS`` so the meta-brief's bridges and the
# knowledge-graph's gold edges can never disagree. Curated, whole-word matched: a region
# only joins a bridge if it literally appears in the live L1 text, so every cross-channel
# claim is data-backed.
REGIONS: tuple[str, ...] = (
    # energy / EU fuel panel + general
    "United States",
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Greece",
    "Austria",
    "Belgium",
    "Netherlands",
    "Poland",
    "Norway",
    "Portugal",
    "Ireland",
    "Mexico",
    "United Kingdom",
    "Europe",
    "European Union",
    # geophysical / Ring-of-Fire arcs
    "Indonesia",
    "Philippines",
    "Japan",
    "China",
    "Russia",
    "Chile",
    "Turkey",
    "Iran",
    "India",
    "Taiwan",
    "New Zealand",
    "Tonga",
    "Fiji",
    "Kamchatka",
    "Mid-Atlantic Ridge",
    "Kermadec",
)

# The regions where the energy-supply theme measures a PHYSICAL balance: US crude
# inventories (EIA) and EU gas storage (GIE). A geophysical event can only show *observed*
# reach into the energy data if it falls on one of these — anything else is a name
# coincidence in two feeds, not a supply effect. EU gas storage is reported as a single
# aggregate (not per-country), so only the explicit infrastructure anchors are listed.
ENERGY_INFRA_CORE: frozenset[str] = frozenset({"United States"})

# longest-first so "United States" wins over "States", "New Zealand" over "Zealand"
_REGIONS_LONGEST_FIRST: tuple[str, ...] = tuple(sorted(REGIONS, key=lambda r: -len(r)))


@dataclass
class Bridge:
    """A region the latest L1 day mentions under >=2 clean themes."""

    region: str
    # theme slug -> sorted list of source-note stems (under that theme) mentioning it
    themes: dict[str, list[str]] = field(default_factory=dict)
    # source stem -> concrete data-backed evidence snippets pulled from that L1 note
    evidence: dict[str, list[str]] = field(default_factory=dict)

    @property
    def theme_slugs(self) -> list[str]:
        return sorted(self.themes)

    @property
    def source_notes(self) -> list[str]:
        """Every L1 note stem that mentions this region, across all bridged themes."""
        notes: set[str] = set()
        for keys in self.themes.values():
            notes.update(keys)
        return sorted(notes)


@dataclass
class CrossThemeScan:
    """The full deterministic cross-theme picture for one L1 ingest day."""

    day: str
    clean_themes: list[str]
    bridges: list[Bridge]
    source_notes: list[str]  # every clean L1 note stem read this day (for frontmatter)

    @property
    def infra_reach(self) -> list[str]:
        """Bridge regions that fall on the physical energy-supply core (observed reach)."""
        return [b.region for b in self.bridges if b.region in ENERGY_INFRA_CORE]


def _norm(text: str) -> str:
    """Lower-case with collapsed whitespace, for whole-word entity matching."""
    return re.sub(r"\s+", " ", text).lower()


def _mentions(haystack_norm: str, term: str) -> bool:
    """Whole-word, case-insensitive containment of ``term`` in normalised text."""
    pat = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
    return re.search(pat, haystack_norm) is not None


def _extract_json_array(raw: str, anchor: str) -> list[dict[str, Any]]:
    """Bracket-match the JSON array containing ``anchor`` out of an L1 note table cell.

    The L1 notes store a feed as a single markdown table cell holding a JSON array
    (e.g. earthquake events, fuel-price countries). Mirrors the parser in
    ``scripts/build_graph.py``; any failure returns ``[]`` so evidence only ever
    enriches a bridge, never breaks the scan.
    """
    i = raw.find(anchor)
    if i == -1:
        return []
    start = raw.rfind("[", 0, i)
    if start == -1:
        return []
    depth = 0
    for j in range(start, len(raw)):
        if raw[j] == "[":
            depth += 1
        elif raw[j] == "]":
            depth -= 1
            if depth == 0:
                try:
                    arr = json.loads(raw[start : j + 1])
                except (ValueError, json.JSONDecodeError):
                    return []
                return [x for x in arr if isinstance(x, dict)] if isinstance(arr, list) else []
    return []


def _quake_evidence(raw: str, region: str) -> list[str]:
    """Top recorded earthquakes (by magnitude) whose place names ``region``."""
    events = _extract_json_array(raw, '"magnitude"')
    matched = [
        e
        for e in events
        if _mentions(_norm(str(e.get("place") or "")), region) and e.get("magnitude") is not None
    ]
    matched.sort(key=lambda e: e.get("magnitude") or 0, reverse=True)
    out: list[str] = []
    for e in matched[:2]:
        place = str(e.get("place") or "").strip()
        out.append(f"M{e['magnitude']} {place}")
    return out


def _fuel_evidence(raw: str, region: str) -> list[str]:
    """The region's pump panel row (diesel/gasoline USD price + w/w move), or a failed-feed note."""
    if _mentions(_norm(raw), region) and f'"{region}"' in raw and "failedsources" in _norm(raw):
        # Heuristic: the region appears only inside the failedSources list -> no price row.
        countries = _extract_json_array(raw, '"diesel"')
        if not any(str(c.get("name", "")).strip() == region for c in countries):
            return ["fuel feed reported no price this week (listed under failedSources)"]
    countries = _extract_json_array(raw, '"diesel"')
    for c in countries:
        if str(c.get("name", "")).strip() != region:
            continue
        parts: list[str] = []
        for grade in ("diesel", "gasoline"):
            blk = c.get(grade)
            if isinstance(blk, dict) and blk.get("usdPrice") is not None:
                wow = blk.get("wowPct")
                wow_s = f", {wow:+.2f}% w/w" if isinstance(wow, int | float) else ""
                parts.append(f"{grade} ${blk['usdPrice']:.3f}/L{wow_s}")
        if parts:
            return ["; ".join(parts)]
    return []


_EVIDENCE_EXTRACTORS = {
    "earthquakes": _quake_evidence,
    "fuel-prices": _fuel_evidence,
}


def held_themes(registry: dict[str, Any]) -> set[str]:
    """Theme slugs whose brief is editorially held (excluded from the cross-theme scan)."""
    return {slug for slug, meta in registry.get("themes", {}).items() if meta.get("brief_held")}


def clean_theme_sources(registry: dict[str, Any]) -> dict[str, list[str]]:
    """Map each editorially-clean (surfaced, non-held) theme slug -> its source keys."""
    skip = held_themes(registry)
    out: dict[str, list[str]] = {}
    for src in registry.get("sources", []):
        if not src.get("surfaced"):
            continue
        theme = src.get("theme")
        key = src.get("key")
        if theme and key and theme not in skip:
            out.setdefault(theme, []).append(key)
    return {theme: sorted(keys) for theme, keys in out.items()}


def latest_day(sources_dir: Path) -> str | None:
    """Newest ``YYYY-MM-DD`` ingest day directory under ``01 Sources/``, or None."""
    if not sources_dir.is_dir():
        return None
    days = [
        d.name
        for d in sources_dir.iterdir()
        if d.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d.name)
    ]
    return max(days) if days else None


def scan(vault_dir: Path, registry: dict[str, Any], day: str | None = None) -> CrossThemeScan:
    """Compute the cross-theme bridges for ``day`` (default: the latest L1 ingest day)."""
    sources_dir = vault_dir / "01 Sources"
    the_day = day or latest_day(sources_dir) or ""
    theme_sources = clean_theme_sources(registry)

    # region -> {theme -> set(source stems mentioning it that day)}
    hits: dict[str, dict[str, set[str]]] = {}
    read_notes: set[str] = set()
    raw_by_key: dict[str, str] = {}
    day_dir = sources_dir / the_day
    for theme, keys in theme_sources.items():
        for key in keys:
            note = day_dir / f"{key}.md"
            if not note.is_file():
                continue
            read_notes.add(key)
            raw = note.read_text(encoding="utf-8")
            raw_by_key[key] = raw
            text_norm = _norm(raw)
            for region in _REGIONS_LONGEST_FIRST:
                if _mentions(text_norm, region):
                    hits.setdefault(region, {}).setdefault(theme, set()).add(key)

    bridges: list[Bridge] = []
    for region, per_theme in hits.items():
        if len(per_theme) < 2:  # the defining cross-theme condition
            continue
        evidence: dict[str, list[str]] = {}
        for stems in per_theme.values():
            for key in stems:
                extractor = _EVIDENCE_EXTRACTORS.get(key)
                if extractor and key in raw_by_key:
                    snippets = extractor(raw_by_key[key], region)
                    if snippets:
                        evidence[key] = snippets
        bridges.append(
            Bridge(
                region=region,
                themes={t: sorted(ks) for t, ks in per_theme.items()},
                evidence=evidence,
            )
        )
    bridges.sort(key=lambda b: (-len(b.themes), b.region))

    return CrossThemeScan(
        day=the_day,
        clean_themes=sorted(theme_sources),
        bridges=bridges,
        source_notes=sorted(read_notes),
    )
