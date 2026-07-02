#!/usr/bin/env python3
"""Build the azimuth knowledge-graph view (``site/graph.json`` + ``site/graph.html``).

This is the CROSS-CHANNEL layer of the public demonstrator. A static OKF bundle can
store briefs and source notes; what it cannot do is *connect* them. Emi can — so this
graph makes that connection visible.

The graph has FOUR visually-typed node kinds:

* **concept** — one per surfaced channel/theme (the persistent topic an L2 brief is an
  instance of). The top layer: ``concept -> brief -> source``.
* **brief** — the weekly L2 synthesis (one per surfaced theme).
* **source** — the dated L1 source notes a brief's claims rest on.
* **entity** — named things scanned out of the live text, in three sub-kinds:
  ``region`` (countries/areas), ``commodity`` (oil/gas benchmarks) and ``event``
  (individual earthquakes pulled from the USGS feed). The entity layer is what makes
  cross-source relationships legible instead of locked in prose.

Three kinds of link are drawn:

* **concept -> brief** and **brief -> source** — the structural spine (within-theme).
* **commodity/event -> brief** — the per-channel entity texture (within-theme): which
  benchmarks and which actual events each channel is built on.
* **cross-theme** — a shared ENTITY (a region the live data mentions under *different*
  themes) becomes its own node wired to the brief of every theme it appears in. Those
  edges are flagged ``cross_theme: true`` and rendered in gold. Example from the live
  feed: *Greece* and *Mexico* are recorded both as USGS earthquake locations
  (``geophysical``) and in the WorldMonitor fuel-price panel (``energy-supply``), so the
  graph shows the two channels joined through them.

Every edge carries a **typed relation** (``rel``) so the graph is semantic, not just a
shape — a static bundle has no relations at all. The relation vocabulary is fixed and
data-backed:

* ``has-brief`` — channel -> its current weekly L2 brief.
* ``rests-on`` — brief -> the dated L1 source note its claims rest on.
* ``mentioned-in`` — a commodity / region entity -> a brief whose text (or backing L1
  notes) names it. These edges also carry a ``weight``: how many distinct L1 source notes
  in that theme mention the entity (0 = brief-text-only, no raw-source backing). Weight is
  the strength of the entity's tie to the channel, used to rank hubs and bridges.
* ``named-in`` — a commodity / region entity -> the *specific dated L1 source note* whose
  raw text names it. Where ``mentioned-in`` collapses provenance into a ``weight`` count,
  ``named-in`` keeps it: it is the source-level evidence behind that count, so the graph
  spans briefs *and* L1 sources (not just briefs). A ``mentioned-in`` edge with ``weight``
  N is backed by exactly N ``named-in`` edges to the L1 notes that earned it.
* ``reported-in`` — an individual earthquake event -> the geophysical brief.
* ``located-in`` — an earthquake event -> the region it occurred in.

Entities are not invented — regions/commodities are scanned out of the actual L1 source
notes and L2 briefs with a fixed gazetteer, and events are read straight from the USGS
earthquake JSON. So every node and every cross-theme edge is data-backed, never inferred.

Surfacing rules (kept readable, not flooded):

* **regions** surface only when they BRIDGE >=2 themes — that is their cross-channel
  value; a country confined to one theme stays implicit in that theme's cluster.
* **commodities** surface even single-theme — the per-channel economic texture.
* **events** (top earthquakes by magnitude) always surface under ``geophysical``, and
  link to any surfaced region named in their location.

Held themes (``brief_held: true`` in ``sources/registry.json``) are excluded entirely, the
same editorial guarantee the static-site build enforces.

Usage:
    python scripts/build_graph.py                 # build into ./site
    python scripts/build_graph.py --out _site     # custom output dir
    python scripts/build_graph.py --check         # exit 1 if committed graph is stale (CI guard)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import split_frontmatter  # noqa: E402
from synthesis.site_build import (  # noqa: E402
    DEFAULT_REGISTRY,
    DEFAULT_VAULT,
    _slug,
    held_source_keys,
    held_themes,
)

# --- entity gazetteer -------------------------------------------------------
# Curated, whole-word matched. Kept deliberately conservative: a name only joins
# the graph if it literally appears in the live L1/L2 text, so every cross-theme
# edge is data-backed, never inferred.
_REGIONS = [
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
    # added 2026-06-27 (KR-B gazetteer coverage audit): every name below is
    # whole-word present in the live clean-theme L1/L2 text of the latest ingest
    # day, so each is data-backed, not inferred. Four of them BRIDGE >=2 clean
    # themes today (so they surface immediately): Venezuela (geophysical +
    # environmental-hazards), California (climate-signals + geophysical), Ukraine
    # (climate-signals + environmental-hazards), Papua New Guinea (geophysical +
    # environmental-hazards). The rest currently sit in a single clean theme —
    # they stay implicit until they bridge (the >=2-theme surfacing rule still
    # gates them) but are listed so a future cross-theme appearance is caught
    # instead of silently dropped. Held-theme-only names are deliberately NOT
    # added (those themes are excluded from the graph).
    "Venezuela",
    "California",
    "Ukraine",
    "Papua New Guinea",
    "Argentina",
    "Brazil",
    "Peru",
    "Vanuatu",
    "Alaska",
    "Hawaii",
    "Australia",
    "Myanmar",
    "Romania",
    "Croatia",
    "Hungary",
    "Slovakia",
    "Denmark",
    "Sweden",
    "Finland",
]
_COMMODITIES = [
    "WTI",
    "Brent",
    "LNG",
    "natural gas",
    "crude oil",
    "crude",
    "diesel",
    "petrol",
    "gasoline",
    "Bcf",
]

# longest-first so "European Union" wins over "Europe", "crude oil" over "crude"
_ENTITY_TERMS: list[tuple[str, str]] = sorted(
    [(t, "region") for t in _REGIONS] + [(t, "commodity") for t in _COMMODITIES],
    key=lambda p: -len(p[0]),
)

# how many earthquake events (largest by magnitude) to surface as event nodes
_EVENT_TOP_N = 6

# Typed relation vocabulary on edges (see module docstring). Fixed + data-backed.
_REL_HAS_BRIEF = "has-brief"  # concept (channel) -> its weekly L2 brief
_REL_RESTS_ON = "rests-on"  # brief -> the L1 source its claims rest on
_REL_MENTIONED_IN = "mentioned-in"  # commodity / region entity -> brief that names it
_REL_NAMED_IN = "named-in"  # commodity / region entity -> the L1 source note that names it
_REL_REPORTED_IN = "reported-in"  # earthquake event -> the geophysical brief
_REL_LOCATED_IN = "located-in"  # earthquake event -> the region it occurred in

_THEME_COLORS = {
    "energy-supply": "#4cc2ff",  # cyan
    "geophysical": "#ff9d4c",  # orange
    "climate-signals": "#37d6a0",  # emerald — ice/climate
    "prediction-markets": "#b07cff",  # violet
    "environmental-hazards": "#ff5d73",  # rose-red — hazard/fire
    "other": "#8a97a8",  # grey fallback (must stay unused by live channels)
}
_CROSS_THEME_COLOR = "#ffe14c"  # gold — the cross-channel highlight


def _norm(text: str) -> str:
    """Lower-case with collapsed whitespace, for whole-word entity matching."""
    return re.sub(r"\s+", " ", text).lower()


def _mentions(haystack_norm: str, term: str) -> bool:
    """Whole-word, case-insensitive containment of ``term`` in normalised text."""
    pat = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
    return re.search(pat, haystack_norm) is not None


def _latest_source_text(vault_dir: Path, skip_keys: set[str]) -> dict[str, str]:
    """Map each surfaced source key -> normalised text of its newest L1 note."""
    out: dict[str, str] = {}
    sources_dir = vault_dir / "01 Sources"
    if not sources_dir.is_dir():
        return out
    for day_dir in sorted((d for d in sources_dir.iterdir() if d.is_dir()), reverse=True):
        for path in sorted(day_dir.glob("*.md")):
            key = path.stem
            if key == "README" or key in skip_keys or key in out:
                continue
            out[key] = _norm(path.read_text(encoding="utf-8"))
    return out


def _concept_label(theme: str, title: str) -> str:
    """The persistent-channel label — the brief's recurring topic, not this week's note.

    ``Energy Supply Weekly`` (brief) -> ``Energy Supply`` (concept/channel).
    """
    label = re.sub(r"\s+weekly$", "", title, flags=re.IGNORECASE).strip()
    return label or theme


def _extract_quakes(raw: str) -> list[dict[str, Any]]:
    """Best-effort: pull the earthquake JSON array out of a raw USGS L1 source note.

    The L1 note stores the feed as a single markdown table cell holding a JSON array
    of ``{"magnitude", "place", "id", ...}`` objects. We bracket-match the array that
    contains ``"magnitude"`` and parse it. Any failure returns ``[]`` — events only
    ever ENRICH the graph, they never break the build.
    """
    i = raw.find('"magnitude"')
    if i == -1:
        return []
    start = raw.rfind("[", 0, i)
    if start == -1:
        return []
    depth = 0
    end = -1
    for j in range(start, len(raw)):
        c = raw[j]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                end = j
                break
    if end == -1:
        return []
    try:
        arr = json.loads(raw[start : end + 1])
    except (ValueError, json.JSONDecodeError):
        return []
    if not isinstance(arr, list):
        return []
    return [q for q in arr if isinstance(q, dict) and q.get("magnitude") is not None]


def _seismic_events(
    vault_dir: Path,
    skip_keys: set[str],
    geo_brief_id: str | None,
    region_entities: dict[str, str],
    latest_day: str,
    top_n: int = _EVENT_TOP_N,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Surface the largest individual earthquakes as ``event`` entity nodes.

    Reads the newest ``earthquakes`` L1 note, takes the ``top_n`` events by magnitude,
    and wires each to the geophysical brief plus any surfaced region named in its place.
    Returns ``([], [])`` whenever the data is missing or unparseable.
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    if not geo_brief_id:
        return nodes, edges
    sources_dir = vault_dir / "01 Sources"
    if not sources_dir.is_dir():
        return nodes, edges
    raw: str | None = None
    for day_dir in sorted((d for d in sources_dir.iterdir() if d.is_dir()), reverse=True):
        path = day_dir / "earthquakes.md"
        if path.is_file() and "earthquakes" not in skip_keys:
            raw = path.read_text(encoding="utf-8")
            break
    if not raw:
        return nodes, edges
    quakes = sorted(_extract_quakes(raw), key=lambda q: q.get("magnitude") or 0, reverse=True)
    seen: set[str] = set()
    url = f"sources/{latest_day}/earthquakes.html" if latest_day else ""
    for q in quakes:
        if len(seen) >= top_n:
            break
        qid = str(q.get("id") or "")
        if not qid or qid in seen:
            continue
        seen.add(qid)
        mag = q.get("magnitude")
        place = str(q.get("place") or "").strip()
        short = place.split(" of ")[-1] if " of " in place else place
        label = f"M{mag} · {short}" if short else f"M{mag}"
        eid = f"event:{_slug(qid)}"
        nodes.append(
            {
                "id": eid,
                "label": label,
                "kind": "entity",
                "entity_kind": "event",
                "theme": "geophysical",
                "themes": ["geophysical"],
                "magnitude": mag,
                "url": url,
            }
        )
        edges.append(
            {"source": eid, "target": geo_brief_id, "cross_theme": False, "rel": _REL_REPORTED_IN}
        )
        place_norm = _norm(place)
        for term_lower, reid in region_entities.items():
            if _mentions(place_norm, term_lower):
                edges.append(
                    {"source": eid, "target": reid, "cross_theme": False, "rel": _REL_LOCATED_IN}
                )
    return nodes, edges


def build_graph(
    vault_dir: Path = DEFAULT_VAULT,
    registry_path: Path = DEFAULT_REGISTRY,
) -> dict[str, Any]:
    """Return the cross-channel graph as a ``{"nodes": [...], "edges": [...]}`` dict."""
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    skip_themes = held_themes(registry)
    skip_keys = held_source_keys(registry)

    themes_meta = registry.get("themes", {})
    sources = [
        s
        for s in registry.get("sources", [])
        if s.get("surfaced") and s.get("theme") and s.get("theme") not in skip_themes
    ]

    # theme -> brief node id / label
    brief_id: dict[str, str] = {}
    brief_label: dict[str, str] = {}
    for theme, meta in themes_meta.items():
        if theme in skip_themes:
            continue
        title = meta.get("title", theme)
        brief_id[theme] = f"brief:{_slug(title)}"
        brief_label[theme] = title

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    # --- concept nodes (one per surfaced channel) + concept->brief spine ----
    for theme, bid in brief_id.items():
        cid = f"concept:{theme}"
        nodes.append(
            {
                "id": cid,
                "label": _concept_label(theme, brief_label[theme]),
                "kind": "concept",
                "theme": theme,
            }
        )
        edges.append({"source": cid, "target": bid, "cross_theme": False, "rel": _REL_HAS_BRIEF})

    # --- brief nodes (one per surfaced theme) ---------------------------
    for theme, bid in brief_id.items():
        nodes.append(
            {
                "id": bid,
                "label": brief_label[theme],
                "kind": "brief",
                "theme": theme,
                "url": f"briefs/{_slug(brief_label[theme])}.html",
            }
        )

    # --- source nodes + within-theme brief->source edges ----------------
    src_text = _latest_source_text(vault_dir, skip_keys)
    latest_day = ""
    sources_dir = vault_dir / "01 Sources"
    if sources_dir.is_dir():
        day_dirs = sorted((d.name for d in sources_dir.iterdir() if d.is_dir()), reverse=True)
        latest_day = day_dirs[0] if day_dirs else ""

    src_theme: dict[str, str] = {}
    source_node_ids: set[str] = set()
    for s in sources:
        key = s["key"]
        theme = s["theme"]
        src_theme[key] = theme
        sid = f"source:{key}"
        source_node_ids.add(sid)
        nodes.append(
            {
                "id": sid,
                "label": s.get("upstream_source", key),
                "kind": "source",
                "theme": theme,
                "url": f"sources/{latest_day}/{key}.html" if latest_day else "",
            }
        )
        if theme in brief_id:
            edges.append(
                {
                    "source": brief_id[theme],
                    "target": sid,
                    "cross_theme": False,
                    "rel": _REL_RESTS_ON,
                }
            )

    # --- brief text per theme (for entity scan) -------------------------
    brief_text: dict[str, str] = {}
    briefs_dir = vault_dir / "02 Briefs"
    if briefs_dir.is_dir():
        for path in sorted(briefs_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
            theme = (fm or {}).get("theme")
            if theme and theme in brief_id:
                brief_text[theme] = _norm(body)

    # --- entity scan: which themes mention each gazetteer term ----------
    # entity term -> {theme -> set(source_keys mentioning it)}
    entity_hits: dict[str, dict[str, set[str]]] = {}
    entity_kind: dict[str, str] = {}
    for term, kind in _ENTITY_TERMS:
        per_theme: dict[str, set[str]] = {}
        for key, text in src_text.items():
            theme = src_theme.get(key)
            if theme and _mentions(text, term):
                per_theme.setdefault(theme, set()).add(key)
        for theme, btext in brief_text.items():
            if _mentions(btext, term):
                per_theme.setdefault(theme, set())  # brief-level mention, no source key
        if per_theme:
            entity_hits[term] = per_theme
            entity_kind[term] = kind

    # --- entity nodes + edges -------------------------------------------
    # Surfacing rule: a region only earns a node when it BRIDGES >=2 themes (its
    # cross-channel value); a commodity surfaces even single-theme (the per-channel
    # economic texture). Multi-theme entities are "shared" (gold); single-theme ones
    # carry their one theme's colour. Region nodes are tracked so seismic events can
    # link to the region they occurred in.
    region_entities: dict[str, str] = {}  # lowercased region term -> entity id
    for term, per_theme in entity_hits.items():
        kind = entity_kind[term]
        multi = len(per_theme) >= 2
        if not multi and kind != "commodity":
            continue
        eid = f"entity:{_slug(term)}"
        node: dict[str, Any] = {
            "id": eid,
            "label": term,
            "kind": "entity",
            "entity_kind": kind,
        }
        if multi:
            node["theme"] = "shared"
            node["themes"] = sorted(per_theme.keys())
        else:
            only = next(iter(per_theme))
            node["theme"] = only
            node["themes"] = [only]
        nodes.append(node)
        if kind == "region":
            region_entities[term.lower()] = eid
        for theme in sorted(per_theme.keys()):
            if theme in brief_id:
                # weight = how many distinct L1 source notes in this theme name the entity
                # (0 = the brief text mentions it but no raw source backs it).
                edges.append(
                    {
                        "source": eid,
                        "target": brief_id[theme],
                        "cross_theme": multi,
                        "rel": _REL_MENTIONED_IN,
                        "weight": len(per_theme[theme]),
                    }
                )
                # named-in: keep the provenance the weight counts — one edge per L1 source
                # note that actually names the entity, so the graph reaches L1 sources,
                # not just briefs. These are always within-theme (a source belongs to one
                # theme), so never a cross-theme bridge.
                for key in sorted(per_theme[theme]):
                    sid = f"source:{key}"
                    if sid in source_node_ids:
                        edges.append(
                            {
                                "source": eid,
                                "target": sid,
                                "cross_theme": False,
                                "rel": _REL_NAMED_IN,
                            }
                        )

    # --- event entities: the largest live earthquakes -------------------
    ev_nodes, ev_edges = _seismic_events(
        vault_dir, skip_keys, brief_id.get("geophysical"), region_entities, latest_day
    )
    nodes.extend(ev_nodes)
    edges.extend(ev_edges)

    return {"nodes": nodes, "edges": edges}


# --- HTML renderer ----------------------------------------------------------
_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Graph · azimuth</title>
<link rel="stylesheet" href="assets/style.css">
<style>
.gquery{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;margin:.6rem 0 .2rem}
.gquery .qlabel{font-size:.85rem;color:#8a97a8;font-weight:600}
.gquery select{background:#141a23;color:#e7edf5;border:1px solid #2a3a4d;border-radius:6px;
padding:.25rem .5rem;font:inherit;font-size:.85rem}
.gquery button{appearance:none;background:#4cc2ff;color:#08121b;border:0;border-radius:6px;
padding:.3rem .8rem;font:inherit;font-size:.82rem;font-weight:600;cursor:pointer}
.gquery button#qclear,.gquery button#qshare{background:transparent;color:#8a97a8;border:1px solid #2a3a4d}
.gquery input#gsearch{background:#141a23;color:#e7edf5;border:1px solid #2a3a4d;border-radius:6px;
padding:.25rem .5rem;font:inherit;font-size:.85rem;min-width:11rem}
.legend .lg[data-cls]{cursor:pointer;user-select:none}
.legend .lg[data-cls]:hover{color:#8fd0ff}
.legend .lg.off{opacity:.4;text-decoration:line-through}
.legend .lgreset{margin-left:.5rem;appearance:none;background:transparent;color:#8a97a8;
border:1px solid #2a3a4d;border-radius:6px;padding:.15rem .55rem;font:inherit;font-size:.78rem;
font-weight:600;cursor:pointer;vertical-align:middle}
.legend .lgreset:hover{color:#8fd0ff;border-color:#3a4a5d}
.gquery .qout{flex-basis:100%;margin:.35rem 0 0;font-size:.88rem;color:#e7edf5;min-height:1.2em}
#gwrap{position:relative;margin:.4rem 0}
#g{width:100%;height:min(68vh,600px);display:block;background:#0c1118;
border:1px solid #1c2733;border-radius:10px;cursor:grab;touch-action:none}
#g:active{cursor:grabbing}
#g:focus{outline:2px solid #4cc2ff;outline-offset:2px}
#g:focus:not(:focus-visible){outline:none}
#gstatus{font-size:.78rem;color:#8fd0ff;margin:.3rem 0 0;min-height:1.15em}
#gtip{position:absolute;display:none;pointer-events:none;z-index:5;max-width:240px;
background:rgba(12,19,32,.94);border:1px solid #2a3a4d;border-radius:8px;padding:.4rem .55rem;
font-size:.8rem;line-height:1.35;color:#e7edf5;box-shadow:0 4px 14px rgba(0,0,0,.5)}
#gtip strong{color:#8fd0ff}
.gctrls{position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:.3rem;z-index:5}
.gctrls button{width:30px;height:30px;border:1px solid #2a3a4d;background:rgba(20,26,35,.8);
color:#e7edf5;border-radius:7px;font:inherit;font-size:1rem;line-height:1;cursor:pointer}
.gctrls button:hover{background:#1d2735}
.ghint{font-size:.78rem;color:#8a97a8;margin:.3rem 0 0}
</style>
</head><body>
<header class="nav">
  <a class="brand" href="index.html">azimuth</a>
  <nav>
    <a href="answers.html">Ask the data</a>
    <a href="benchmark.html">Benchmark</a>
    <a href="index.html">Briefs</a>
    <a href="index.html#sources">Sources</a>
    <a href="editorial.html">Editorial line</a>
  </nav>
</header>
<main class="content">
<div class="kind kind-brief">Knowledge graph</div>
<h1>Cross-channel relationship graph</h1>
<p class="hero-sub">Four node kinds, drawn straight from the live bundle. A
<strong>channel</strong> (hexagon) holds its <strong>L2 brief</strong> (large circle),
which rests on the dated <strong>L1 source notes</strong> (small dots) its claims come
from. Around them sits the <strong>entity layer</strong> scanned out of the real text:
<strong>commodities</strong> (squares) and individual <strong>earthquake events</strong>
(triangles) give each channel its texture, and <strong>shared regions</strong> (gold
diamonds) bridge channels &mdash; a place the live data records under <em>more than one</em>
theme, joined by <strong>gold edges</strong>. That cross-channel link is the part a static
format cannot produce. Every edge is <strong>typed</strong> (<em>mentioned-in</em>,
<em>rests-on</em>, <em>located-in</em>…) and evidence-weighted — heavier links draw thicker;
<strong>hover a line</strong> to read its relation. Hover a node to spotlight its links,
scroll to zoom and drag to pan; click a node to open its page. Held themes never appear.
<strong>Pick two channels below and Trace</strong> to ask the graph how they connect &mdash;
the queryable half a static bundle cannot answer.</p>
<div id="legend" class="legend"></div>
<div id="query" class="gquery">
  <span class="qlabel">Trace connection:</span>
  <select id="qa"></select> &harr; <select id="qb"></select>
  <button id="qgo" type="button">Trace</button>
  <button id="qclear" type="button">Clear</button>
  <button id="qshare" type="button" title="Copy a link to this view">&#x1F517; Copy link</button>
  <span class="qlabel" style="margin-left:.6rem">Find:</span>
  <input id="gsearch" list="gsearchlist" type="search" placeholder="node name…"
    autocomplete="off" aria-label="Find a node by name">
  <datalist id="gsearchlist"></datalist>
  <p id="qout" class="qout"></p>
</div>
<div id="gwrap">
  <canvas id="g" tabindex="0" role="application"
    aria-label="Interactive cross-channel knowledge graph. Focus it, then use the arrow keys to walk between nodes, Enter to open the focused node's page, plus and minus to zoom, zero to reset the view, and Escape to clear."></canvas>
  <div class="gctrls">
    <button id="zin" type="button" title="Zoom in" aria-label="Zoom in">+</button>
    <button id="zout" type="button" title="Zoom out" aria-label="Zoom out">&minus;</button>
    <button id="zreset" type="button" title="Reset view" aria-label="Reset view">&#x2316;</button>
  </div>
  <div id="gtip"></div>
</div>
<p id="gstatus" class="ghint" role="status" aria-live="polite"></p>
<p class="ghint"><strong>Keyboard:</strong> click or tab to the graph, then <strong>arrow keys</strong>
walk the visible nodes, <strong>Enter</strong> opens the focused node&rsquo;s page,
<strong>+ / &minus;</strong> zoom, <strong>0</strong> resets, <strong>Esc</strong> clears.</p>
<p class="ghint">Scroll to zoom &middot; drag the background to pan &middot; hover a node to
spotlight its links &middot; <strong>hover an edge</strong> to read its relation type + weight
&middot; drag a node to reposition &middot; click to open its page
&middot; <strong>click a legend chip</strong> to hide/show that node kind
(the commodity + earthquake layers start hidden &mdash; <strong>Reset filters</strong>
returns to that default) &middot; <strong>Find</strong> to jump to any node by name.</p>
<noscript><p>Enable JavaScript to view the interactive graph, or browse the
<a href="index.html">briefs and sources</a> directly.</p></noscript>
<div id="glist"></div>
</main>
<footer class="foot">
  azimuth — public demonstrator of the HemySphere L1/L2/L3 vault doctrine.
  Content CC-BY-4.0. Read-only static preview.
</footer>
<script>
const GRAPH = __GRAPH_JSON__;
const THEME_COLORS = __THEME_COLORS__;
const CROSS = "__CROSS_COLOR__";
const cv = document.getElementById("g"), cx = cv.getContext("2d");
const colorOf = n => n.theme === "shared" ? CROSS : (THEME_COLORS[n.theme] || THEME_COLORS.other);
const isEntity = n => n.kind === "entity";
// --- legend: themes + node-kind glyph guide -------------------------------
const themes = [...new Set(GRAPH.nodes.filter(n => !isEntity(n)).map(n => n.theme))];
let legend = themes.map(t =>
  `<span class="lg"><i style="background:${THEME_COLORS[t]||THEME_COLORS.other}"></i>${t}</span>`
).join("");
const has = (k, ek) => GRAPH.nodes.some(n => n.kind === k && (!ek || n.entity_kind === ek));
legend += `<span class="lg" data-cls="channel" title="click to hide/show">&#x2B22; channel</span>`;
legend += `<span class="lg" data-cls="brief" title="click to hide/show">&#x25CF; brief</span>`;
legend += `<span class="lg" data-cls="source" title="click to hide/show">&#xB7; source</span>`;
if (has("entity", "commodity")) legend += `<span class="lg" data-cls="commodity" title="click to hide/show">&#x25A0; commodity</span>`;
if (has("entity", "event")) legend += `<span class="lg" data-cls="event" title="click to hide/show" style="color:${THEME_COLORS.geophysical}">&#x25B2; earthquake</span>`;
if (has("entity", "region")) legend += `<span class="lg" data-cls="region" title="click to hide/show" style="color:${CROSS}">&#x25C6; shared region (cross-theme)</span>`;
legend += `<button id="freset" class="lgreset" type="button" title="Reset layers to the default view">&#x21BB; Reset filters</button>`;
document.getElementById("legend").innerHTML = legend;
// --- legend filter: click a node-kind chip to hide/show that kind ----------
// First paint hides the dense commodity + earthquake entity layers for a cleaner
// public first impression; visitors toggle them on via the legend chips, and the
// "Reset filters" button returns to this default view.
const DEFAULT_HIDDEN = ["commodity", "event"];
const HIDDEN = new Set(DEFAULT_HIDDEN);
// Full view state lives in the URL — the layer-filter set + an active Trace + a focused
// node — so "Copy link" reproduces the EXACT graph a reader is looking at, not just a bare
// trace. VIEW is the single source the #hash is serialised from; layersState() returns the
// hidden-kinds set only when it differs from the default (else null = omit from the hash).
const VIEW = { layers: null, trace: null, node: null };
const layersState = () => {
  const cur = [...HIDDEN].sort(), def = [...DEFAULT_HIDDEN].sort();
  return (cur.length === def.length && cur.every((c, i) => c === def[i])) ? null : cur;
};
const classOf = n => n.kind === "concept" ? "channel"
  : n.kind === "brief" ? "brief"
  : n.kind === "source" ? "source"
  : n.entity_kind === "commodity" ? "commodity"
  : n.entity_kind === "event" ? "event"
  : n.entity_kind === "region" ? "region" : "other";
const visible = n => !HIDDEN.has(classOf(n));
const syncChips = () => document.querySelectorAll("#legend .lg[data-cls]")
  .forEach(el => el.classList.toggle("off", HIDDEN.has(el.dataset.cls)));
document.querySelectorAll("#legend .lg[data-cls]").forEach(el => {
  el.addEventListener("click", () => {
    const c = el.dataset.cls;
    HIDDEN.has(c) ? HIDDEN.delete(c) : HIDDEN.add(c);
    el.classList.toggle("off", HIDDEN.has(c));
    VIEW.layers = layersState(); syncHash();   // the filter set is part of the shareable view
    mark();
  });
});
const freset = document.getElementById("freset");
if (freset) freset.addEventListener("click", () => {
  HIDDEN.clear(); DEFAULT_HIDDEN.forEach(c => HIDDEN.add(c));
  syncChips(); VIEW.layers = null; syncHash(); mark();
});
syncChips();  // reflect the default-hidden layers on the legend chips at load
// --- text fallback / accessibility list -----------------------------------
const nodeById = Object.fromEntries(GRAPH.nodes.map(n => [n.id, n]));
const childrenOf = (id, pred) => GRAPH.edges
  .filter(e => e.source === id).map(e => nodeById[e.target])
  .filter(n => n && pred(n));
const briefList = GRAPH.nodes.filter(n => n.kind === "brief").map(b => {
  const srcs = childrenOf(b.id, n => n.kind === "source")
    .map(n => `<a href="${n.url}">${n.label}</a>`).join(", ");
  const comms = GRAPH.edges.filter(e => e.target === b.id)
    .map(e => nodeById[e.source]).filter(n => n && n.entity_kind === "commodity")
    .map(n => n.label);
  const commTxt = comms.length ? ` <em>(commodities: ${[...new Set(comms)].join(", ")})</em>` : "";
  return `<li><a href="${b.url}"><strong>${b.label}</strong></a> &rarr; ${srcs||"&mdash;"}${commTxt}</li>`;
}).join("");
const events = GRAPH.nodes.filter(n => n.entity_kind === "event")
  .map(n => `<li>${n.label}</li>`).join("");
const bridges = GRAPH.nodes.filter(n => n.entity_kind === "region")
  .map(en => `<li><strong>${en.label}</strong> bridges ${(en.themes||[]).join(" &harr; ")}</li>`).join("");
document.getElementById("glist").innerHTML =
  "<details><summary>Graph as a list</summary><ul>" + briefList + "</ul>" +
  (events ? "<p><strong>Largest live earthquakes</strong></p><ul>" + events + "</ul>" : "") +
  (bridges ? "<p><strong>Cross-theme bridges</strong></p><ul>" + bridges + "</ul>" : "") +
  "</details>";
// --- force layout (stable logical world) + responsive hi-DPI view ----------
// Physics run in a fixed logical world (LW x LH) so the layout stays deterministic;
// a separate view transform (scale + pan) maps world -> screen, redrawn crisply at the
// device pixel ratio. That split is what upgrades the old fixed 820x600 bitmap into a
// zoomable / pannable / retina-sharp / responsive graph.
const LW = 820, LH = 600;
let DPR = 1, CSSW = LW, CSSH = LH;
const view = { s: 1, tx: 0, ty: 0 };   // screen_px = world*s + t  (CSS px)
let userView = false;                   // true once the user zooms/pans -> stop auto-fit
// Layout heat (decays -> physics idle) + repaint flag (draw only on a dirty frame).
// Accessibility: prefers-reduced-motion visitors never get the auto-playing spring
// animation — the layout is pre-settled synchronously at load (heat starts at 0) and
// interactions repaint without re-animating, so nothing on the page moves on its own.
const REDUCED = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
let heat = REDUCED ? 0 : 1, dirty = true;
const reheat = (v = 0.55) => {
  if (REDUCED) { dirty = true; return; }
  heat = Math.min(1, Math.max(heat, v)); dirty = true;
};
const mark = () => { dirty = true; };
function fitView() {
  const pad = 26;
  const s = Math.min((CSSW - 2*pad)/LW, (CSSH - 2*pad)/LH) || 1;
  view.s = s; view.tx = (CSSW - LW*s)/2; view.ty = (CSSH - LH*s)/2;
}
function resize() {
  DPR = Math.max(1, Math.min(window.devicePixelRatio || 1, 2.5));
  const rect = cv.getBoundingClientRect();
  CSSW = Math.max(1, rect.width); CSSH = Math.max(1, rect.height);
  cv.width = Math.round(CSSW*DPR); cv.height = Math.round(CSSH*DPR);
  if (!userView) fitView();
}
const toWorld = (mx, my) => [ (mx - view.tx)/view.s, (my - view.ty)/view.s ];
const radiusOf = n =>
  n.kind === "concept" ? 16 :
  n.kind === "brief"   ? 13 :
  n.kind === "entity"  ? (n.entity_kind === "event"
                           ? Math.min(12, 6 + ((n.magnitude || 5) - 4) * 1.6) : 9) : 7;
const N = GRAPH.nodes.map((n, i) => ({
  ...n, x: LW/2 + Math.cos(i)*220 + (i%5)*7, y: LH/2 + Math.sin(i*1.7)*170 + (i%3)*5,
  vx: 0, vy: 0, r: radiusOf(n)
}));
const idx = Object.fromEntries(N.map(n => [n.id, n]));
const E = GRAPH.edges.map(e => ({
  s: idx[e.source], t: idx[e.target], cross: !!e.cross_theme,
  rel: e.rel || "link", weight: e.weight || 1
})).filter(e => e.s && e.t);
function step() {
  for (const a of N) {
    for (const b of N) {
      if (a === b) continue;
      let dx = a.x-b.x, dy = a.y-b.y, d = Math.hypot(dx,dy)||1;
      const f = 3000/(d*d);
      a.vx += (dx/d)*f; a.vy += (dy/d)*f;
    }
    a.vx += (LW/2-a.x)*0.0024; a.vy += (LH/2-a.y)*0.0024;
  }
  for (const e of E) {
    let dx = e.t.x-e.s.x, dy = e.t.y-e.s.y, d = Math.hypot(dx,dy)||1;
    const rest = e.cross ? 175 : 110;
    const f = (d-rest)*0.012;
    e.s.vx += (dx/d)*f; e.s.vy += (dy/d)*f;
    e.t.vx -= (dx/d)*f; e.t.vy -= (dy/d)*f;
  }
  for (const a of N) {
    a.x += a.vx*0.5; a.y += a.vy*0.5; a.vx *= 0.82; a.vy *= 0.82;
    a.x = Math.max(a.r, Math.min(LW-a.r, a.x)); a.y = Math.max(a.r, Math.min(LH-a.r, a.y));
  }
}
// --- shape primitives -----------------------------------------------------
function diamond(x, y, r) {
  cx.beginPath(); cx.moveTo(x, y-r); cx.lineTo(x+r, y); cx.lineTo(x, y+r);
  cx.lineTo(x-r, y); cx.closePath();
}
function square(x, y, r) { cx.beginPath(); cx.rect(x-r, y-r, 2*r, 2*r); }
function triangle(x, y, r) {
  cx.beginPath(); cx.moveTo(x, y-r); cx.lineTo(x+r*0.92, y+r*0.72);
  cx.lineTo(x-r*0.92, y+r*0.72); cx.closePath();
}
function hexagon(x, y, r) {
  cx.beginPath();
  for (let k=0;k<6;k++) {
    const a = Math.PI/6 + k*Math.PI/3, px = x+r*Math.cos(a), py = y+r*Math.sin(a);
    k ? cx.lineTo(px, py) : cx.moveTo(px, py);
  }
  cx.closePath();
}
// --- queryable layer: trace how two channels connect ----------------------
// The graph is also *answerable*, not just drawable: pick two channels and the page
// runs a BFS over the same node/edge data the CLI uses (scripts/query_graph.py),
// highlighting the shared bridge entities + the shortest path that join them.
const ADJ = {};
for (const n of GRAPH.nodes) ADJ[n.id] = new Set();
for (const e of GRAPH.edges) {
  if (ADJ[e.source] && ADJ[e.target]) { ADJ[e.source].add(e.target); ADJ[e.target].add(e.source); }
}
const briefNodes = GRAPH.nodes.filter(n => n.kind === "brief");
const channelName = lbl => lbl.replace(/ Weekly$/, "");
const qa = document.getElementById("qa"), qb = document.getElementById("qb");
let HILITE = null;
if (qa && qb && briefNodes.length) {
  const opts = briefNodes
    .map(b => `<option value="${b.theme}">${channelName(b.label)}</option>`).join("");
  qa.innerHTML = opts; qb.innerHTML = opts;
  if (briefNodes.length > 1) qb.selectedIndex = 1;
}
const briefIdOf = theme => { const b = briefNodes.find(n => n.theme === theme); return b ? b.id : null; };
function bfsPath(src, dst) {
  if (!ADJ[src] || !ADJ[dst]) return null;
  if (src === dst) return [src];
  const prev = {[src]: src}, q = [src];
  while (q.length) {
    const cur = q.shift();
    for (const nx of [...ADJ[cur]].sort()) {
      if (nx in prev) continue;
      prev[nx] = cur;
      if (nx === dst) {
        const p = [dst];
        while (p[p.length-1] !== src) p.push(prev[p[p.length-1]]);
        return p.reverse();
      }
      q.push(nx);
    }
  }
  return null;
}
function trace() {
  mark();
  const out = document.getElementById("qout"), ta = qa.value, tb = qb.value;
  if (ta === tb) { out.textContent = "Pick two different channels."; HILITE = null; return; }
  const ba = briefIdOf(ta), bb = briefIdOf(tb);
  const shared = [...ADJ[ba]].filter(x => ADJ[bb].has(x) && nodeById[x] && nodeById[x].kind === "entity");
  const path = bfsPath(ba, bb);
  const nodes = new Set(path || []); nodes.add(ba); nodes.add(bb); shared.forEach(x => nodes.add(x));
  const edges = new Set();
  const link = (a, b) => { edges.add(a+"|"+b); edges.add(b+"|"+a); };
  if (path) for (let i=0;i<path.length-1;i++) link(path[i], path[i+1]);
  shared.forEach(x => { link(x, ba); link(x, bb); });
  HILITE = { nodes, edges }; mark();
  const aL = channelName(nodeById[ba].label), bL = channelName(nodeById[bb].label);
  if (!shared.length && !path) { out.textContent = `No connection found between ${aL} and ${bL}.`; return; }
  const names = shared.map(x => nodeById[x].label).join(", ") || "no direct shared entity";
  let txt = `${aL} ↔ ${bL}: ${shared.length} shared bridge(s) — ${names}.`;
  if (path) txt += "  Path: " + path.map(id => nodeById[id].label).join(" → ") + ".";
  out.textContent = txt;
}
// --- shareable deep links --------------------------------------------------
// The whole view is a URL: the layer filters + an active Trace + a focused node each write
// into one composite #hash, and on load that hash replays the exact view — so a specific
// answer ("how energy connects to geophysical, commodity layer on, Ukraine focused") can be
// linked straight from the build-in-public feed and opens already set up. syncHash()
// serialises VIEW into `layers=…&trace=…&node=…` (each key omitted when unset), so a bare
// legacy `#trace=…` or `#node=…` link still parses as a single key. replaceState keeps the
// hash off the back button and out of the hashchange loop.
let applyingHash = false;
const writeHash = h => { applyingHash = true; try {
  history.replaceState(null, "", h ? "#"+h : location.pathname + location.search);
} finally { applyingHash = false; } };
const syncHash = () => {
  const parts = [];
  if (VIEW.layers) parts.push("layers=" + VIEW.layers.map(encodeURIComponent).join(","));
  if (VIEW.trace)  parts.push("trace=" + VIEW.trace.map(encodeURIComponent).join(","));
  if (VIEW.node)   parts.push("node=" + encodeURIComponent(VIEW.node));
  writeHash(parts.join("&"));
};
if (qa && qb) {
  document.getElementById("qgo").addEventListener("click", () => {
    trace();
    VIEW.trace = (qa.value !== qb.value) ? [qa.value, qb.value] : null;
    syncHash();
  });
  document.getElementById("qclear").addEventListener("click", () => {
    HILITE = null; document.getElementById("qout").textContent = "";
    VIEW.trace = null; syncHash(); mark();
  });
}
// --- search: jump to any node by name --------------------------------------
// Type a node name (autocompleted from every label); on select the view centres
// on the match, spotlights its neighbourhood, and parks a focus ring on it so a
// reader can pull one entity out of a dense graph without hunting by eye.
const search = document.getElementById("gsearch");
let doFocus = null;   // exposed so a #node= hash can replay a Find on load
if (search) {
  document.getElementById("gsearchlist").innerHTML =
    GRAPH.nodes.map(n => `<option value="${n.label.replace(/"/g, "&quot;")}"></option>`).join("");
  doFocus = () => {
    const q = search.value.trim().toLowerCase();
    if (!q) { pinnedId = null; VIEW.node = null; syncHash(); mark(); return; }
    const hit = GRAPH.nodes.find(n => n.label.toLowerCase() === q)
      || GRAPH.nodes.find(n => n.label.toLowerCase().includes(q));
    const nn = hit && idx[hit.id];
    if (!nn) { pinnedId = null; mark(); return; }
    pinnedId = nn.id;
    view.s = Math.max(view.s, 1.2);
    view.tx = CSSW/2 - nn.x*view.s; view.ty = CSSH/2 - nn.y*view.s;
    userView = true; reheat(0.15);
    VIEW.node = nodeById[nn.id].label; syncHash();
  };
  search.addEventListener("change", doFocus);
  search.addEventListener("keydown", e => { if (e.key === "Enter") doFocus(); });
  search.addEventListener("input", () => { if (!search.value) { pinnedId = null; mark(); } });
}
// Copy-link button: put the current view's URL on the clipboard (mobile-friendly share).
const qshare = document.getElementById("qshare");
if (qshare) qshare.addEventListener("click", async () => {
  const out = document.getElementById("qout");
  try { await navigator.clipboard.writeText(location.href); if (out) out.textContent = "Link copied to clipboard."; }
  catch (_) { if (out) out.textContent = location.href; }
});
// Replay a deep link on load: any `&`-joined mix of #layers=<kinds>, #trace=<themeA>,<themeB>
// and #node=<label> (a bare single key is just the one-pair case, so old links still work).
// Layers are restored first so a focused/traced node lands against the right visible set.
function applyHash() {
  const raw = location.hash.replace(/^#/, "");
  if (!raw) return;
  const pairs = raw.split("&").map(p => {
    const eq = p.indexOf("=");
    return eq < 0 ? null : [p.slice(0, eq), decodeURIComponent(p.slice(eq + 1))];
  }).filter(Boolean);
  pairs.sort((a, b) => (a[0] === "layers" ? -1 : 0) - (b[0] === "layers" ? -1 : 0));
  for (const [k, v] of pairs) {
    if (k === "layers") {
      HIDDEN.clear();
      v.split(",").filter(Boolean).forEach(c => HIDDEN.add(c));
      syncChips(); VIEW.layers = layersState(); mark();
    } else if (k === "trace" && qa && qb) {
      const [ta, tb] = v.split(",");
      const themes = new Set(briefNodes.map(b => b.theme));
      if (themes.has(ta) && themes.has(tb)) { qa.value = ta; qb.value = tb; trace(); VIEW.trace = [ta, tb]; }
    } else if (k === "node" && search && doFocus) {
      search.value = v; doFocus();
    }
  }
}
// Highlight = an active Trace (HILITE) OR, absent that, the hovered node's neighbourhood.
// Hovering spotlights a node + its direct links and dims the rest, so a reader can read
// one entity's reach without running a full trace.
let hoverId = null, pinnedId = null;   // pinnedId = a node parked by the search box
let hoverEdge = null;                   // the edge object under the cursor (relation tooltip)
function neighHL(id) {
  if (!id || !ADJ[id]) return null;
  const nodes = new Set([id]), edges = new Set();
  for (const nb of ADJ[id]) {
    nodes.add(nb); edges.add(id+"|"+nb); edges.add(nb+"|"+id);
  }
  return { nodes, edges };
}
// Hovering an edge spotlights just its two endpoints, so a reader can isolate a single
// typed link (and read its relation in the tooltip) without a full trace.
const edgeHL = e => e ? {
  nodes: new Set([e.s.id, e.t.id]),
  edges: new Set([e.s.id+"|"+e.t.id, e.t.id+"|"+e.s.id])
} : null;
const activeHL = () => HILITE || neighHL(hoverId) || edgeHL(hoverEdge) || neighHL(pinnedId);
const onNode = n => { const h = activeHL(); return !h || h.nodes.has(n.id); };
const onEdge = e => { const h = activeHL(); return !h || h.edges.has(e.s.id+"|"+e.t.id); };
function draw() {
  // Reset to device space to clear, then apply the world->screen view transform so
  // every shape is drawn in stable world coordinates; stroke widths are divided by the
  // zoom so they stay a constant screen thickness regardless of scale.
  cx.setTransform(DPR,0,0,DPR,0,0);
  cx.clearRect(0,0,CSSW,CSSH);
  cx.setTransform(DPR*view.s,0,0,DPR*view.s, DPR*view.tx, DPR*view.ty);
  const lw = w => w/view.s;
  // within-theme edges first (thin, muted), cross-theme on top (gold, thick).
  // When a trace/hover is active, off-path elements dim so the answer stands out.
  // Edge thickness carries evidence: heavier `weight` (how many L1 notes name the entity)
  // draws a thicker line, so an evidence-ranked link reads as such. The hovered edge lights
  // up cyan on top so its relation type (shown in the tooltip) has something to point at.
  const wLine = e => 0.8 + 0.7 * Math.min(e.weight, 4);   // weight 1->1.5px .. 4->3.6px
  for (const e of E) {
    if (e.cross || !visible(e.s) || !visible(e.t)) continue;
    const hot = e === hoverEdge;
    cx.strokeStyle = hot ? "#8fd0ff" : "#2a3a4d"; cx.lineWidth = lw(hot ? wLine(e) + 1.2 : wLine(e));
    cx.globalAlpha = hot ? 1 : (onEdge(e) ? 1 : 0.08);
    cx.beginPath(); cx.moveTo(e.s.x,e.s.y); cx.lineTo(e.t.x,e.t.y); cx.stroke();
  }
  for (const e of E) {
    if (!e.cross || !visible(e.s) || !visible(e.t)) continue;
    const hot = e === hoverEdge;
    cx.strokeStyle = hot ? "#8fd0ff" : CROSS; cx.lineWidth = lw((hot ? 1.4 : 1) * (2.2 + 0.4 * Math.min(e.weight, 4)));
    cx.globalAlpha = hot ? 1 : (onEdge(e) ? 0.9 : 0.08);
    cx.beginPath(); cx.moveTo(e.s.x,e.s.y); cx.lineTo(e.t.x,e.t.y); cx.stroke();
  }
  cx.globalAlpha = 1;
  if (HILITE) {  // the traced path, drawn bright white on top
    for (const e of E) {
      if (!onEdge(e) || !visible(e.s) || !visible(e.t)) continue;
      cx.strokeStyle = "#ffffff"; cx.lineWidth = lw(3);
      cx.beginPath(); cx.moveTo(e.s.x,e.s.y); cx.lineTo(e.t.x,e.t.y); cx.stroke();
    }
  }
  for (const n of N) {
    if (!visible(n)) continue;
    const baseA = onNode(n) ? 1 : 0.12;
    cx.globalAlpha = baseA; cx.fillStyle = colorOf(n);
    if (n.kind === "concept") {
      hexagon(n.x, n.y, n.r); cx.fill();
      cx.strokeStyle = "#cdd7e3"; cx.lineWidth = lw(2); cx.stroke();
    } else if (n.kind === "entity") {
      if (n.entity_kind === "commodity") square(n.x, n.y, n.r);
      else if (n.entity_kind === "event") triangle(n.x, n.y, n.r);
      else diamond(n.x, n.y, n.r);
      cx.fill();
      cx.strokeStyle = n.theme === "shared" ? "#7a6a10" : "#1c2733";
      cx.lineWidth = lw(1); cx.stroke();
    } else {
      cx.beginPath(); cx.arc(n.x,n.y,n.r,0,7);
      cx.globalAlpha = (n.kind === "brief" ? 1 : 0.85) * baseA; cx.fill();
    }
    if (n.id === hoverId || n.id === pinnedId) {  // a white focus ring on the hovered/found node
      cx.globalAlpha = 1; cx.strokeStyle = "#ffffff"; cx.lineWidth = lw(2);
      cx.beginPath(); cx.arc(n.x, n.y, n.r + lw(3), 0, 7); cx.stroke();
    }
    cx.globalAlpha = baseA;
    if (n.kind !== "source") {
      // font size in world units = constant 12px on screen at any zoom
      cx.fillStyle = "#e7edf5"; cx.font = lw(12)+"px Inter,sans-serif"; cx.textAlign = "center";
      cx.fillText(n.label, n.x, n.y-n.r-lw(5));
    }
    cx.globalAlpha = 1;
  }
}
// --- interaction: hover spotlight + tooltip, drag node, pan, wheel-zoom -----
const tip = document.getElementById("gtip");
const pick = (mx, my) => {                 // nearest node under the cursor, in world space
  const [wx, wy] = toWorld(mx, my);
  let best = null, bd = Infinity;
  for (const n of N) {
    if (!visible(n)) continue;
    const d = Math.hypot(n.x-wx, n.y-wy);
    if (d < n.r + 6 && d < bd) { bd = d; best = n; }
  }
  return best;
};
const relText = n => {                      // one-line description for the tooltip
  const deg = ADJ[n.id] ? ADJ[n.id].size : 0;
  if (n.entity_kind === "region") return `shared region · bridges ${(n.themes||[]).join(" ↔ ")} · ${deg} links`;
  if (n.entity_kind === "commodity") return `commodity (${n.theme}) · ${deg} links`;
  if (n.entity_kind === "event") return `earthquake M${n.magnitude} · ${deg} links`;
  if (n.kind === "concept") return `channel · ${deg} links`;
  if (n.kind === "brief") return `L2 brief (${n.theme}) · ${deg} links`;
  if (n.kind === "source") return `L1 source (${n.theme})`;
  return `${n.kind} · ${deg} links`;
};
// --- typed edges: hover a line to read its relation (+ evidence weight) ------
const REL_LABEL = {"has-brief":"has brief","rests-on":"rests on","mentioned-in":"mentioned in",
  "named-in":"named in","reported-in":"reported in","located-in":"located in","link":"link"};
const edgeText = e => {
  const w = e.weight > 1 ? ` · weight ${e.weight}` : "";
  const kind = e.cross ? " · cross-theme bridge" : "";
  return `<strong>${REL_LABEL[e.rel] || e.rel}</strong>${w}${kind}<br>${e.s.label} ↔ ${e.t.label}`;
};
function segDist(px, py, ax, ay, bx, by) {   // distance from a point to a segment
  const dx = bx-ax, dy = by-ay, L2 = dx*dx + dy*dy || 1;
  let t = ((px-ax)*dx + (py-ay)*dy) / L2; t = Math.max(0, Math.min(1, t));
  return Math.hypot(px - (ax+t*dx), py - (ay+t*dy));
}
const pickEdge = (mx, my) => {               // nearest edge within a few screen px, in screen space
  let best = null, bd = 7;
  for (const e of E) {
    if (!visible(e.s) || !visible(e.t)) continue;
    const ax = e.s.x*view.s+view.tx, ay = e.s.y*view.s+view.ty;
    const bx = e.t.x*view.s+view.tx, by = e.t.y*view.s+view.ty;
    const d = segDist(mx, my, ax, ay, bx, by);
    if (d < bd) { bd = d; best = e; }
  }
  return best;
};
let drag = null, pan = null, moved = 0;
const localXY = ev => { const r = cv.getBoundingClientRect(); return [ev.clientX-r.left, ev.clientY-r.top]; };
cv.addEventListener("mousedown", ev => {
  const [mx, my] = localXY(ev); const hit = pick(mx, my); moved = 0;
  if (hit) drag = hit; else pan = { mx, my, tx: view.tx, ty: view.ty };
});
window.addEventListener("mousemove", ev => {   // drag-node / pan-background (capture anywhere)
  if (!drag && !pan) return;
  const [mx, my] = localXY(ev);
  if (drag) { const [wx, wy] = toWorld(mx, my); drag.x = wx; drag.y = wy; moved++; reheat(0.4); }
  else { view.tx = pan.tx + (mx - pan.mx); view.ty = pan.ty + (my - pan.my); userView = true; moved++; mark(); }
});
cv.addEventListener("mousemove", ev => {       // hover spotlight + tooltip (node first, then edge)
  if (drag || pan) { tip.style.display = "none"; return; }
  const [mx, my] = localXY(ev); const hit = pick(mx, my);
  const he = hit ? null : pickEdge(mx, my);
  const newHover = hit ? hit.id : null;
  if (newHover !== hoverId || he !== hoverEdge) mark();   // repaint even when the layout is idle
  hoverId = newHover; hoverEdge = he;
  if (hit) {
    tip.innerHTML = `<strong>${hit.label}</strong><br>${relText(hit)}`;
    tip.style.display = "block";
    tip.style.left = (mx + 14) + "px"; tip.style.top = (my + 12) + "px";
    cv.style.cursor = hit.url ? "pointer" : "grab";
  } else if (he) {
    tip.innerHTML = edgeText(he);
    tip.style.display = "block";
    tip.style.left = (mx + 14) + "px"; tip.style.top = (my + 12) + "px";
    cv.style.cursor = "grab";
  } else { tip.style.display = "none"; cv.style.cursor = "grab"; }
});
cv.addEventListener("mouseleave", () => { hoverId = null; hoverEdge = null; tip.style.display = "none"; mark(); });
window.addEventListener("mouseup", () => { drag = null; pan = null; });
cv.addEventListener("click", ev => {
  if (moved > 3) return;                       // a drag/pan, not a click
  const [mx, my] = localXY(ev); const hit = pick(mx, my);
  if (hit && hit.url) location.href = hit.url;
});
cv.addEventListener("wheel", ev => {           // zoom toward the cursor
  ev.preventDefault();
  const [mx, my] = localXY(ev); const [wx, wy] = toWorld(mx, my);
  view.s = Math.max(0.25, Math.min(6, view.s * Math.exp(-ev.deltaY * 0.0015)));
  view.tx = mx - wx*view.s; view.ty = my - wy*view.s; userView = true; mark();
}, { passive: false });
// --- touch: one-finger pan/drag + tap-to-open, two-finger pinch-zoom (mobile) ---
// The desktop handlers above are mouse-only, so on a phone the graph is frozen.
// canvas carries touch-action:none so the browser won't steal the gesture.
let pinch = null;
const touchXY = t => { const r = cv.getBoundingClientRect(); return [t.clientX-r.left, t.clientY-r.top]; };
const touchMid = (a, b) => [(a[0]+b[0])/2, (a[1]+b[1])/2];
cv.addEventListener("touchstart", ev => {
  tip.style.display = "none";                  // no hover tooltip on touch
  if (ev.touches.length === 1) {
    const [mx, my] = touchXY(ev.touches[0]); const hit = pick(mx, my); moved = 0; pinch = null;
    if (hit) drag = hit; else pan = { mx, my, tx: view.tx, ty: view.ty };
  } else if (ev.touches.length === 2) {        // start a pinch: remember span + view
    drag = null; pan = null;
    const a = touchXY(ev.touches[0]), b = touchXY(ev.touches[1]);
    pinch = { d: Math.hypot(a[0]-b[0], a[1]-b[1]) || 1, mid: touchMid(a, b),
              s: view.s, tx: view.tx, ty: view.ty };
  }
}, { passive: false });
cv.addEventListener("touchmove", ev => {
  ev.preventDefault();                          // stop the page scrolling under the gesture
  if (pinch && ev.touches.length === 2) {       // pinch-zoom toward the pinch midpoint (+ two-finger pan)
    const a = touchXY(ev.touches[0]), b = touchXY(ev.touches[1]);
    const nd = Math.hypot(a[0]-b[0], a[1]-b[1]) || 1; const mid = touchMid(a, b);
    const s = Math.max(0.25, Math.min(6, pinch.s * (nd / pinch.d)));
    const wx = (pinch.mid[0] - pinch.tx) / pinch.s, wy = (pinch.mid[1] - pinch.ty) / pinch.s;
    view.s = s; view.tx = mid[0] - wx*s; view.ty = mid[1] - wy*s; userView = true; mark();
  } else if (ev.touches.length === 1 && (drag || pan)) {
    const [mx, my] = touchXY(ev.touches[0]);
    if (drag) { const [wx, wy] = toWorld(mx, my); drag.x = wx; drag.y = wy; moved++; reheat(0.4); }
    else { view.tx = pan.tx + (mx - pan.mx); view.ty = pan.ty + (my - pan.my); userView = true; moved++; mark(); }
  }
}, { passive: false });
cv.addEventListener("touchend", ev => {
  if (ev.touches.length < 2) pinch = null;
  if (ev.touches.length === 0) {                // a clean tap (little movement) on a node opens it
    if (moved <= 3 && ev.changedTouches.length) {
      const [mx, my] = touchXY(ev.changedTouches[0]); const hit = pick(mx, my);
      if (hit && hit.url) location.href = hit.url;
    }
    drag = null; pan = null;
  }
}, { passive: false });
function zoomBy(k) {
  const cx0 = CSSW/2, cy0 = CSSH/2, p = toWorld(cx0, cy0);
  view.s = Math.max(0.25, Math.min(6, view.s * k));
  view.tx = cx0 - p[0]*view.s; view.ty = cy0 - p[1]*view.s; userView = true; mark();
}
const zin = document.getElementById("zin"), zout = document.getElementById("zout"),
      zreset = document.getElementById("zreset");
if (zin) zin.addEventListener("click", () => zoomBy(1.3));
if (zout) zout.addEventListener("click", () => zoomBy(1/1.3));
if (zreset) zreset.addEventListener("click", () => { userView = false; resize(); mark(); });
// --- keyboard: make the interactive graph operable without a mouse (WCAG 2.1.1) ---
// The canvas is focusable (tabindex + role=application). Arrow keys walk the *visible*
// nodes in a stable order (most-connected first, then alphabetical); Enter/Space opens
// the focused node's page; +/- zoom, 0 resets, Esc clears. A polite live region
// announces each focused node, so a keyboard / screen-reader visitor hears what a mouse
// user sees spotlighted — the interactive graph itself, not only the list fallback.
const gstatus = document.getElementById("gstatus");
const announce = msg => { if (gstatus) gstatus.textContent = msg; };
const kbOrder = () => N.filter(visible).sort((a, b) =>
  ((ADJ[b.id] ? ADJ[b.id].size : 0) - (ADJ[a.id] ? ADJ[a.id].size : 0)) || a.label.localeCompare(b.label));
let kbi = -1;
function focusNodeAt(i) {
  const order = kbOrder();
  if (!order.length) { announce("No nodes are visible — reset the filters to walk the graph."); return; }
  kbi = ((i % order.length) + order.length) % order.length;
  const n = order[kbi];
  pinnedId = n.id;
  view.s = Math.max(view.s, 1.2);
  view.tx = CSSW/2 - n.x*view.s; view.ty = CSSH/2 - n.y*view.s;
  userView = true; reheat(0.12); mark();
  announce(`${n.label}: ${relText(n)}${n.url ? " — press Enter to open its page" : ""}. Node ${kbi+1} of ${order.length}.`);
  VIEW.node = n.label; syncHash();
}
cv.addEventListener("keydown", ev => {
  switch (ev.key) {
    case "ArrowRight": case "ArrowDown": ev.preventDefault(); focusNodeAt(kbi + 1); break;
    case "ArrowLeft":  case "ArrowUp":   ev.preventDefault(); focusNodeAt(kbi - 1); break;
    case "Home": ev.preventDefault(); focusNodeAt(0); break;
    case "End":  ev.preventDefault(); focusNodeAt(-1); break;
    case "Enter": case " ": {
      ev.preventDefault();
      const n = pinnedId && nodeById[pinnedId] && idx[pinnedId];
      if (n && n.url) location.href = n.url;
      break;
    }
    case "+": case "=": ev.preventDefault(); zoomBy(1.3); break;
    case "-": case "_": ev.preventDefault(); zoomBy(1/1.3); break;
    case "0": ev.preventDefault(); userView = false; resize(); mark(); break;
    case "Escape": ev.preventDefault(); pinnedId = null; kbi = -1; HILITE = null;
      VIEW.node = null; VIEW.trace = null; announce("Selection cleared."); syncHash(); mark(); break;
  }
});
cv.addEventListener("focus", () => {
  if (kbi < 0) announce("Graph focused. Arrow keys walk nodes, Enter opens, plus and minus zoom, Escape clears.");
});
window.addEventListener("resize", () => { resize(); dirty = true; });
resize();
// Reduced-motion: settle the force layout once, synchronously, so the graph opens in its
// final shape with zero on-load animation (the O(N^2) step is cheap at this node count).
if (REDUCED) { for (let k = 0; k < 600; k++) step(); heat = 0; dirty = true; }
// --- cooled render loop -----------------------------------------------------
// The old loop ran the O(N^2) force step twice every frame forever, pinning a CPU
// core for as long as the public page stayed open. Instead the layout carries a
// `heat` that decays to zero once it settles; physics only runs while it is warm,
// and the canvas only repaints on a `dirty` frame. Any interaction (drag / pan /
// zoom / hover / trace / resize) reheats or re-marks, so the graph stays live to
// the touch but idles at ~0% CPU once still.
function loop() {
  if (heat > 0.02) { for (let k=0;k<2;k++) step(); heat *= 0.985; dirty = true; }
  if (dirty) { draw(); dirty = false; }
  requestAnimationFrame(loop);
}
loop();
applyHash();   // replay a shared #trace / #node link on first paint
window.addEventListener("hashchange", () => { if (!applyingHash) applyHash(); });
</script>
</body></html>
"""


def render_html(graph: dict[str, Any]) -> str:
    """Render the interactive graph page with the graph embedded inline."""
    return (
        _HTML_TEMPLATE.replace("__GRAPH_JSON__", json.dumps(graph))
        .replace("__THEME_COLORS__", json.dumps(_THEME_COLORS))
        .replace("__CROSS_COLOR__", _CROSS_THEME_COLOR)
    )


def _serialize(graph: dict[str, Any]) -> tuple[str, str]:
    """Return the exact ``(graph.json, graph.html)`` text a build would write.

    Single source of truth shared by the write path (:func:`build`) and the
    ``--check`` sync guard, so the two can never disagree about what "in sync" means.
    """
    return json.dumps(graph, indent=2) + "\n", render_html(graph)


def build(
    out_dir: Path, vault_dir: Path = DEFAULT_VAULT, registry_path: Path = DEFAULT_REGISTRY
) -> dict[str, Any]:
    """Build the graph and write ``graph.json`` + ``graph.html`` into ``out_dir``."""
    graph = build_graph(vault_dir, registry_path)
    json_text, html_text = _serialize(graph)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph.json").write_text(json_text, encoding="utf-8")
    (out_dir / "graph.html").write_text(html_text, encoding="utf-8")
    return graph


def check(
    out_dir: Path, vault_dir: Path = DEFAULT_VAULT, registry_path: Path = DEFAULT_REGISTRY
) -> list[str]:
    """Return the names of any committed graph artifact that is stale vs the live vault.

    Rebuilds the graph in memory from ``vault_dir`` and compares to the on-disk
    ``out_dir/graph.json`` and ``out_dir/graph.html``. An empty list means in sync.
    This is the CI / pre-commit guard: whoever updates the vault or a brief must also
    regenerate and commit the graph, exactly like the brief-index sync guard.
    """
    graph = build_graph(vault_dir, registry_path)
    json_text, html_text = _serialize(graph)
    stale: list[str] = []
    for name, new_text in (("graph.json", json_text), ("graph.html", html_text)):
        path = out_dir / name
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != new_text:
            stale.append(name)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the azimuth cross-channel knowledge graph."
    )
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if committed graph.json/graph.html are stale vs the live vault (CI guard)",
    )
    args = parser.parse_args(argv)
    out_dir = (_REPO_ROOT / args.out).resolve()
    if args.check:
        stale = check(out_dir)
        if stale:
            print(
                f"graph: STALE ({', '.join(stale)}) — run "
                "`python scripts/build_graph.py` and commit."
            )
            return 1
        print("graph: up to date.")
        return 0
    graph = build(out_dir)
    n_cross = sum(1 for e in graph["edges"] if e.get("cross_theme"))
    n_concept = sum(1 for n in graph["nodes"] if n["kind"] == "concept")
    n_entity = sum(1 for n in graph["nodes"] if n["kind"] == "entity")
    n_event = sum(1 for n in graph["nodes"] if n.get("entity_kind") == "event")
    n_comm = sum(1 for n in graph["nodes"] if n.get("entity_kind") == "commodity")
    print(
        f"Built graph into {out_dir}: {len(graph['nodes'])} nodes, "
        f"{len(graph['edges'])} edges ({n_concept} concepts, {n_entity} entities "
        f"[{n_comm} commodities, {n_event} events], {n_cross} cross-theme edges)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
