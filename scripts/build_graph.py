#!/usr/bin/env python3
"""Build the azimuth knowledge-graph view (``site/graph.json`` + ``site/graph.html``).

This is the CROSS-CHANNEL layer of the public demonstrator. A static OKF bundle can
store briefs and source notes; what it cannot do is *connect* them. Emi can — so this
graph makes that connection visible.

Two kinds of link are drawn:

* **within-theme** — every L2 brief links to the L1 source notes its claims rest on
  (the structural link-graph that already existed); and
* **cross-theme** — a shared ENTITY (a region or a commodity/benchmark) that the live
  data mentions under *different* themes becomes its own node, and is wired to the brief
  of every theme it appears in. When an entity bridges >=2 themes those edges are flagged
  ``cross_theme: true`` and rendered distinctly. Example from the live feed: *Greece* and
  *Mexico* are recorded both as USGS earthquake locations (``geophysical``) and in the
  WorldMonitor fuel-price panel (``energy-supply``), so the graph shows the two themes
  joined through them.

Entities are not invented — they are scanned out of the actual L1 source notes and L2
briefs with a fixed gazetteer (countries/regions + energy commodities & benchmarks), so a
cross-theme edge only ever exists because the same name genuinely appears under two themes.

Held themes (``brief_held: true`` in ``sources/registry.json``) are excluded entirely, the
same editorial guarantee the static-site build enforces.

Usage:
    python scripts/build_graph.py                 # build into ./site
    python scripts/build_graph.py --out _site     # custom output dir
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
    "United States", "Germany", "France", "Italy", "Spain", "Greece", "Austria",
    "Belgium", "Netherlands", "Poland", "Norway", "Portugal", "Ireland", "Mexico",
    "United Kingdom", "Europe", "European Union",
    # geophysical / Ring-of-Fire arcs
    "Indonesia", "Philippines", "Japan", "China", "Russia", "Chile", "Turkey",
    "Iran", "India", "Taiwan", "New Zealand", "Tonga", "Fiji", "Kamchatka",
    "Mid-Atlantic Ridge", "Kermadec",
]
_COMMODITIES = [
    "WTI", "Brent", "LNG", "natural gas", "crude oil", "crude", "diesel",
    "petrol", "gasoline", "Bcf",
]

# longest-first so "European Union" wins over "Europe", "crude oil" over "crude"
_ENTITY_TERMS: list[tuple[str, str]] = sorted(
    [(t, "region") for t in _REGIONS] + [(t, "commodity") for t in _COMMODITIES],
    key=lambda p: -len(p[0]),
)

_THEME_COLORS = {
    "energy-supply": "#4cc2ff",
    "geophysical": "#ff9d4c",
    "prediction-markets": "#b07cff",
    "other": "#8a97a8",
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
    for s in sources:
        key = s["key"]
        theme = s["theme"]
        src_theme[key] = theme
        sid = f"source:{key}"
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
            edges.append({"source": brief_id[theme], "target": sid, "cross_theme": False})

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

    # --- entity nodes + edges; cross-theme entities bridge >=2 themes ---
    # Only surface entities that BRIDGE themes (the cross-channel value). A term
    # confined to one theme stays implicit in that theme's brief/source cluster.
    for term, per_theme in entity_hits.items():
        if len(per_theme) < 2:
            continue
        eid = f"entity:{_slug(term)}"
        nodes.append(
            {
                "id": eid,
                "label": term,
                "kind": "entity",
                "entity_kind": entity_kind[term],
                "theme": "shared",
                "themes": sorted(per_theme.keys()),
            }
        )
        for theme in sorted(per_theme.keys()):
            if theme in brief_id:
                edges.append(
                    {"source": eid, "target": brief_id[theme], "cross_theme": True}
                )

    return {"nodes": nodes, "edges": edges}


# --- HTML renderer ----------------------------------------------------------
_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Graph · azimuth</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<header class="nav">
  <a class="brand" href="index.html">azimuth</a>
  <nav>
    <a href="index.html">Briefs</a>
    <a href="index.html#sources">Sources</a>
    <a href="graph.html">Graph</a>
    <a href="editorial.html">Editorial</a>
    <a href="okf.html">OKF</a>
  </nav>
</header>
<main class="content">
<div class="kind kind-brief">Knowledge graph</div>
<h1>Cross-channel relationship graph</h1>
<p class="hero-sub">Each <strong>L2 brief</strong> (large node) links to the dated
<strong>L1 source notes</strong> (small nodes) its claims rest on, coloured by theme.
The <strong>gold diamonds</strong> are <strong>shared entities</strong> &mdash; a region or
commodity the live data mentions under <em>more than one</em> theme &mdash; and the
<strong>gold edges</strong> are the cross-theme links they create. That is the part a static
format cannot produce: Emi connects channels through the entities they have in common.
Drag a node; click it to open its page. Held themes never appear.</p>
<div id="legend" class="legend"></div>
<canvas id="g" width="820" height="560"></canvas>
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
const colorOf = n => n.kind === "entity" ? CROSS : (THEME_COLORS[n.theme] || THEME_COLORS.other);
// legend: each surfaced theme + the shared-entity class
const themes = [...new Set(GRAPH.nodes.filter(n => n.kind !== "entity").map(n => n.theme))];
let legend = themes.map(t =>
  `<span class="lg"><i style="background:${THEME_COLORS[t]||THEME_COLORS.other}"></i>${t}</span>`
).join("");
if (GRAPH.nodes.some(n => n.kind === "entity"))
  legend += `<span class="lg"><i style="background:${CROSS}"></i>shared entity (cross-theme)</span>`;
document.getElementById("legend").innerHTML = legend;
// text fallback / accessibility list
const briefList = GRAPH.nodes.filter(n => n.kind === "brief").map(b => {
  const kids = GRAPH.edges.filter(e => e.source === b.id && !e.cross_theme)
    .map(e => GRAPH.nodes.find(n => n.id === e.target))
    .filter(Boolean).map(n => `<a href="${n.url}">${n.label}</a>`).join(", ");
  return `<li><a href="${b.url}"><strong>${b.label}</strong></a> &rarr; ${kids||"&mdash;"}</li>`;
}).join("");
const bridges = GRAPH.nodes.filter(n => n.kind === "entity").map(en =>
  `<li><strong>${en.label}</strong> bridges ${(en.themes||[]).join(" &harr; ")}</li>`
).join("");
document.getElementById("glist").innerHTML =
  "<details><summary>Graph as a list</summary><ul>" + briefList +
  (bridges ? "</ul><p><strong>Cross-theme bridges</strong></p><ul>" + bridges : "") +
  "</ul></details>";
// simple force layout
const W = cv.width, H = cv.height;
const N = GRAPH.nodes.map((n, i) => ({
  ...n, x: W/2 + Math.cos(i)*200 + (i%5)*7, y: H/2 + Math.sin(i*1.7)*160 + (i%3)*5,
  vx: 0, vy: 0, r: n.kind === "brief" ? 13 : (n.kind === "entity" ? 9 : 7)
}));
const idx = Object.fromEntries(N.map(n => [n.id, n]));
const E = GRAPH.edges.map(e => ({s: idx[e.source], t: idx[e.target], cross: !!e.cross_theme}))
  .filter(e => e.s && e.t);
function step() {
  for (const a of N) {
    for (const b of N) {
      if (a === b) continue;
      let dx = a.x-b.x, dy = a.y-b.y, d = Math.hypot(dx,dy)||1;
      const f = 2800/(d*d);
      a.vx += (dx/d)*f; a.vy += (dy/d)*f;
    }
    a.vx += (W/2-a.x)*0.0025; a.vy += (H/2-a.y)*0.0025;
  }
  for (const e of E) {
    let dx = e.t.x-e.s.x, dy = e.t.y-e.s.y, d = Math.hypot(dx,dy)||1;
    const rest = e.cross ? 170 : 120;
    const f = (d-rest)*0.012;
    e.s.vx += (dx/d)*f; e.s.vy += (dy/d)*f;
    e.t.vx -= (dx/d)*f; e.t.vy -= (dy/d)*f;
  }
  for (const a of N) {
    a.x += a.vx*0.5; a.y += a.vy*0.5; a.vx *= 0.82; a.vy *= 0.82;
    a.x = Math.max(a.r, Math.min(W-a.r, a.x)); a.y = Math.max(a.r, Math.min(H-a.r, a.y));
  }
}
function diamond(x, y, r) {
  cx.beginPath(); cx.moveTo(x, y-r); cx.lineTo(x+r, y); cx.lineTo(x, y+r);
  cx.lineTo(x-r, y); cx.closePath();
}
function draw() {
  cx.clearRect(0,0,W,H);
  // within-theme edges first (thin, muted), cross-theme on top (gold, thick)
  for (const e of E) {
    if (e.cross) continue;
    cx.strokeStyle = "#2a3a4d"; cx.lineWidth = 1;
    cx.beginPath(); cx.moveTo(e.s.x,e.s.y); cx.lineTo(e.t.x,e.t.y); cx.stroke();
  }
  for (const e of E) {
    if (!e.cross) continue;
    cx.strokeStyle = CROSS; cx.lineWidth = 2.6; cx.globalAlpha = 0.9;
    cx.beginPath(); cx.moveTo(e.s.x,e.s.y); cx.lineTo(e.t.x,e.t.y); cx.stroke();
    cx.globalAlpha = 1;
  }
  for (const n of N) {
    cx.fillStyle = colorOf(n);
    if (n.kind === "entity") {
      diamond(n.x, n.y, n.r); cx.fill();
      cx.strokeStyle = "#7a6a10"; cx.lineWidth = 1; cx.stroke();
    } else {
      cx.beginPath(); cx.arc(n.x,n.y,n.r,0,7);
      cx.globalAlpha = n.kind === "brief" ? 1 : 0.85; cx.fill(); cx.globalAlpha = 1;
    }
    if (n.kind === "brief" || n.kind === "entity") {
      cx.fillStyle = "#e7edf5"; cx.font = "12px Inter,sans-serif"; cx.textAlign = "center";
      cx.fillText(n.label, n.x, n.y-n.r-5);
    }
  }
}
let drag = null;
cv.addEventListener("mousedown", ev => {
  const r = cv.getBoundingClientRect(), mx = ev.clientX-r.left, my = ev.clientY-r.top;
  drag = N.find(n => Math.hypot(n.x-mx, n.y-my) < n.r+4) || null;
});
cv.addEventListener("mousemove", ev => {
  if (!drag) return;
  const r = cv.getBoundingClientRect(); drag.x = ev.clientX-r.left; drag.y = ev.clientY-r.top;
});
window.addEventListener("mouseup", () => drag = null);
cv.addEventListener("click", ev => {
  const r = cv.getBoundingClientRect(), mx = ev.clientX-r.left, my = ev.clientY-r.top;
  const hit = N.find(n => Math.hypot(n.x-mx, n.y-my) < n.r+4);
  if (hit && hit.url) location.href = hit.url;
});
(function loop() { for (let k=0;k<2;k++) step(); draw(); requestAnimationFrame(loop); })();
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


def build(out_dir: Path, vault_dir: Path = DEFAULT_VAULT,
          registry_path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    """Build the graph and write ``graph.json`` + ``graph.html`` into ``out_dir``."""
    graph = build_graph(vault_dir, registry_path)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph.json").write_text(
        json.dumps(graph, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "graph.html").write_text(render_html(graph), encoding="utf-8")
    return graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the azimuth cross-channel knowledge graph.")
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    args = parser.parse_args(argv)
    out_dir = (_REPO_ROOT / args.out).resolve()
    graph = build(out_dir)
    n_cross = sum(1 for e in graph["edges"] if e.get("cross_theme"))
    n_entity = sum(1 for n in graph["nodes"] if n["kind"] == "entity")
    print(
        f"Built graph into {out_dir}: {len(graph['nodes'])} nodes, "
        f"{len(graph['edges'])} edges ({n_entity} shared entities, "
        f"{n_cross} cross-theme edges)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
