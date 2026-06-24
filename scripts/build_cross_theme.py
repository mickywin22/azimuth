#!/usr/bin/env python3
"""Generate the cross-theme *World Watch Weekly* meta-brief from the live L1 data.

This is the strongest demonstration of azimuth's thesis: a static OKF bundle stores one
brief per theme; Emi's synthesis layer *connects* them. Today's briefs synthesise WITHIN a
theme (energy, geophysics). This script adds the layer that synthesises ACROSS clean themes
— it scans the week's L1 notes for regions that surface under more than one channel
(``synthesis/cross_theme.py``) and renders a brief that names every such cross-channel link,
sourced back to its L1 notes per the synthesis contract.

The brief is fully **re-runnable**: run this script again after a fresh L1 ingest and it
regenerates ``vault/02 Briefs/World Watch Weekly.md`` from current data, preserving the
dated ``## Changelog`` history (evolve-in-place, never fork). Output is lint-green by
construction (``scripts/check_synthesis.py``): every claim bullet carries an L1 wikilink.

Usage:
    python scripts/build_cross_theme.py            # (re)write the World Watch Weekly brief
    python scripts/build_cross_theme.py --check     # exit 1 if the brief is stale vs L1
    python scripts/build_cross_theme.py --json       # emit the bridge scan as JSON
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.cross_theme import Bridge, CrossThemeScan, scan  # noqa: E402

_VAULT = _REPO_ROOT / "vault"
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"
_BRIEF = _VAULT / "02 Briefs" / "World Watch Weekly.md"

_LICENSE = "CC-BY-4.0"
_ATTRIBUTION = "azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources"
_CHANGELOG_DATED_RE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\b")


def _iso_week(day: str) -> str:
    """``YYYY-MM-DD`` -> ``YYYY-Www`` ISO week label (deterministic from the L1 day)."""
    y, w, _ = _dt.date.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


def _theme_title(registry: dict[str, Any], slug: str) -> str:
    """Human channel name for a theme slug, e.g. ``energy-supply`` -> ``Energy Supply``."""
    raw = registry.get("themes", {}).get(slug, {}).get("title", slug)
    return re.sub(r"\s+weekly$", "", raw, flags=re.IGNORECASE).strip() or slug


def _links(stems: list[str]) -> str:
    """Render a comma-joined list of ``[[stem]]`` wikilinks."""
    return ", ".join(f"[[{s}]]" for s in stems)


def _existing_changelog(text: str) -> list[str]:
    """Pull the prior ``## Changelog`` dated lines so regeneration evolves, not forks."""
    lines = text.splitlines()
    out: list[str] = []
    in_cl = False
    for ln in lines:
        if ln.strip().lstrip("#").strip().lower().startswith("changelog"):
            in_cl = True
            continue
        if in_cl and ln.strip().startswith("#"):
            break
        if in_cl and _CHANGELOG_DATED_RE.match(ln):
            out.append(ln.rstrip())
    return out


def _bridge_bullets(brg: list[Bridge], registry: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for b in brg:
        chans = " + ".join(_theme_title(registry, t) for t in b.theme_slugs)
        # Concrete, data-backed evidence per channel where we could extract it.
        per: list[str] = []
        for t in b.theme_slugs:
            label = _theme_title(registry, t)
            ev = "; ".join(snip for key in b.themes[t] for snip in b.evidence.get(key, []))
            cite = _links(b.themes[t])
            per.append(f"{label}: {ev} ({cite})" if ev else f"{label} ({cite})")
        out.append(
            f"- **{b.region}** is recorded under {len(b.themes)} channels this week "
            f"({chans}) — {' | '.join(per)}. The shared name is a co-occurrence in two open "
            f"feeds, not a causal link unless the physical data shows reach."
        )
    return out


def render(s: CrossThemeScan, registry: dict[str, Any], prior_changelog: list[str]) -> str:
    week = _iso_week(s.day) if s.day else ""
    updated = f"{s.day}T04:00:00Z" if s.day else ""
    energy_notes = [n for n in s.source_notes if n != "earthquakes"]
    quake_notes = [n for n in s.source_notes if n == "earthquakes"]
    reach_cite = _links(sorted(set(quake_notes + energy_notes))) or "[[earthquakes]]"

    fm = [
        "---",
        "title: World Watch Weekly",
        "type: L2-brief",
        "theme: cross-theme",
        f"week: {week}",
        f"updated: {updated}",
        f"sources: [{', '.join(s.source_notes)}]",
        f"license: {_LICENSE}",
        f"attribution: {_ATTRIBUTION}",
        "---",
        "",
    ]

    chan_list = ", ".join(_theme_title(registry, t) for t in s.clean_themes)
    body = [
        "# World Watch Weekly",
        "",
        "> The **cross-theme** brief. azimuth's per-theme briefs synthesise WITHIN a channel"
        " — energy supply, geophysics. This one synthesises ACROSS them: it names the regions"
        " the week's open data records under more than one channel, and asks whether the"
        " connection actually *reaches* from one to the other. A static OKF bundle can store"
        " each theme's brief; it cannot draw the line between them. That line is what Emi's"
        " synthesis layer adds — and it is drawn from data, never invented: every region below"
        " literally appears in each channel's L1 source note (see `## How this brief is made`).",
        "",
        "## This week at a glance",
        "",
    ]

    if s.bridges:
        regions = ", ".join(b.region for b in s.bridges)
        body.append(
            f"- The {s.day} ingest connects **{len(s.clean_themes)} clean channels** "
            f"({chan_list}) through **{len(s.bridges)} shared region(s)**: {regions} "
            f"({reach_cite})."
        )
    else:
        body.append(
            f"- No region was recorded under more than one channel in the {s.day} ingest — "
            f"the clean channels ({chan_list}) ran without a shared-region bridge this week "
            f"({reach_cite})."
        )
    if s.infra_reach:
        body.append(
            f"- {', '.join(s.infra_reach)} sits on the physical energy-supply core, so this "
            f"week's seismicity has an observed point of reach into the energy balances "
            f"({reach_cite})."
        )
    else:
        body.append(
            "- None of the shared regions fall on the physical energy-supply core "
            "(US crude inventories, EU gas storage), so the week's recorded seismicity shows "
            f"**no observed reach** into the tracked energy balances ({reach_cite})."
        )

    body += ["", "## Shared entities across channels", ""]
    if s.bridges:
        body += _bridge_bullets(s.bridges, registry)
    else:
        body.append(
            f"- The week's L1 notes carry no region under two channels at once "
            f"({reach_cite}). The cross-theme layer reports the honest absence rather than "
            f"manufacturing a link — that restraint is itself the editorial line."
        )

    body += [
        "",
        "## Does the connection reach?",
        "",
        "- The bridges above are **geographic co-occurrences** — the same place named in two "
        "open feeds. azimuth reports observed signal, not predicted harm, so a quake recorded "
        "near a fuel-reporting country is not read as a supply event unless the physical "
        f"energy data itself moves ({reach_cite}).",
    ]
    if s.infra_reach:
        body.append(
            f"- This week one bridge ({', '.join(s.infra_reach)}) touches the energy-supply "
            f"core; the brief flags the overlap and leaves the magnitude to the per-theme "
            f"briefs ({reach_cite})."
        )
    else:
        body.append(
            "- This week the strong seismic clusters sit away from where the energy balances "
            "are measured, so the cross-theme verdict is a sourced **non-finding**: the "
            f"channels share names but the data shows no reach between them ({reach_cite})."
        )

    body += [
        "",
        "## How this brief is made",
        "",
        "> Regenerated deterministically by `scripts/build_cross_theme.py` from the latest L1"
        " ingest. Bridges are regions the live source notes mention under >=2 editorially-clean"
        " themes, scanned with the same fixed gazetteer the knowledge-graph uses for its gold"
        " cross-theme edges (`synthesis/cross_theme.py`). Held themes are excluded. The script"
        " can be re-run after any ingest; it evolves this note in place and keeps the changelog"
        " history. This is the living-system layer OKF's static format cannot produce.",
        "",
        "## Changelog",
        "",
    ]

    new_cl = (
        f"- {s.day} — regenerated from the {s.day} L1 ingest ({week}): "
        f"{len(s.bridges)} cross-channel bridge(s) across {len(s.clean_themes)} clean "
        f"channels"
        + (f" ({', '.join(b.region for b in s.bridges)})" if s.bridges else "")
        + f"; energy-core reach: {'yes — ' + ', '.join(s.infra_reach) if s.infra_reach else 'none observed'}."
    )
    # Evolve-in-place: keep prior dated lines, append this cycle's (dedup on the day prefix).
    kept = [ln for ln in prior_changelog if not ln.lstrip().startswith(f"- {s.day} ")]
    changelog = [*kept, new_cl]

    return "\n".join(fm + body + changelog) + "\n"


def _load() -> tuple[CrossThemeScan, dict[str, Any]]:
    registry = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    return scan(_VAULT, registry), registry


def main() -> int:
    parser = argparse.ArgumentParser(description="build the azimuth cross-theme meta-brief")
    parser.add_argument("--check", action="store_true", help="exit 1 if the brief is stale")
    parser.add_argument("--json", action="store_true", help="emit the bridge scan as JSON")
    args = parser.parse_args()

    s, registry = _load()

    if args.json:
        print(
            json.dumps(
                {
                    "day": s.day,
                    "clean_themes": s.clean_themes,
                    "source_notes": s.source_notes,
                    "infra_reach": s.infra_reach,
                    "bridges": [
                        {"region": b.region, "themes": b.themes, "notes": b.source_notes}
                        for b in s.bridges
                    ],
                },
                indent=2,
            )
        )
        return 0

    prior = _existing_changelog(_BRIEF.read_text(encoding="utf-8")) if _BRIEF.exists() else []
    new = render(s, registry, prior)

    if args.check:
        current = _BRIEF.read_text(encoding="utf-8") if _BRIEF.exists() else ""
        if current != new:
            print("cross-theme: STALE — run `python scripts/build_cross_theme.py` and commit.")
            return 1
        print("cross-theme: up to date.")
        return 0

    _BRIEF.write_text(new, encoding="utf-8")
    print(f"cross-theme: wrote {_BRIEF.relative_to(_REPO_ROOT)} ({len(s.bridges)} bridge(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
