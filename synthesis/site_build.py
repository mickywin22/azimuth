#!/usr/bin/env python3
"""Lightweight static-site generator for the azimuth public vault.

Renders the ``vault/`` tree (L1 source notes + L2 briefs + the L3 editorial rule)
into a browsable, read-only HTML site. Pure stdlib + the ``markdown`` package; no
Node/Quartz toolchain — this is the "equivalent lightweight SSG" the KR allows, and
it matches the repo's pure-Python runtime ethos.

Editorial guardrail (hard requirement): any theme whose ``sources/registry.json``
entry carries ``brief_held: true`` is EXCLUDED from the site entirely — neither its
held brief nor the L1 source notes that feed it are rendered or linked. The held
``prediction-markets`` theme therefore never appears on the public site.

Landing surface = the L2 briefs. Every ``[[wikilink]]`` in a brief resolves to the
L1 source page it rests on (latest ingest day for that source key), so a reader can
click a claim straight through to the data behind it.

Reuses ``synthesis.lint.split_frontmatter`` / ``find_wikilinks`` so the site can
never disagree with what the lint validated.
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import markdown as md  # type: ignore[import-untyped]

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import split_frontmatter  # noqa: E402

# A repo-local registry / vault path pair, overridable for tests.
DEFAULT_VAULT = _REPO_ROOT / "vault"
DEFAULT_REGISTRY = _REPO_ROOT / "sources" / "registry.json"

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "nl2br"]


@dataclass
class Page:
    """One rendered output page."""

    out_path: str  # site-relative posix path, e.g. "sources/2026-06-20/fuel-prices.html"
    title: str
    body_md: str
    kind: str  # "brief" | "source" | "rule" | "okf"
    day: str = ""  # only for source pages
    theme: str = ""  # theme key (briefs + sources), for graph grouping


@dataclass
class SiteModel:
    """Everything the renderer needs, after held-theme exclusion."""

    briefs: list[Page] = field(default_factory=list)
    sources: list[Page] = field(default_factory=list)
    rules: list[Page] = field(default_factory=list)
    okf: Page | None = None  # the OKF-conformance profile page (vault/OKF.md)
    # wikilink target (e.g. "fuel-prices") -> site-relative posix URL
    link_map: dict[str, str] = field(default_factory=dict)


def held_themes(registry: dict[str, Any]) -> set[str]:
    """Theme keys whose L2 brief is held (``brief_held: true``)."""
    themes = registry.get("themes", {})
    return {name for name, meta in themes.items() if meta.get("brief_held")}


def held_source_keys(registry: dict[str, Any]) -> set[str]:
    """Source keys that map to a held theme — excluded from the public site."""
    held = held_themes(registry)
    return {src["key"] for src in registry.get("sources", []) if src.get("theme") in held}


def held_brief_files(registry: dict[str, Any]) -> set[str]:
    """Brief filenames (e.g. ``Prediction Markets Weekly.md``) for held themes."""
    themes = registry.get("themes", {})
    return {
        meta["brief"]
        for name, meta in themes.items()
        if meta.get("brief_held") and meta.get("brief")
    }


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def discover(vault_dir: Path, registry: dict[str, Any]) -> SiteModel:
    """Walk the vault tree and build the (held-excluded) site model + link map."""
    skip_keys = held_source_keys(registry)
    skip_briefs = held_brief_files(registry)
    src_theme = {s["key"]: s.get("theme") for s in registry.get("sources", [])}
    model = SiteModel()

    # --- L2 briefs (landing surface) -------------------------------------
    briefs_dir = vault_dir / "02 Briefs"
    if briefs_dir.is_dir():
        for path in sorted(briefs_dir.glob("*.md")):
            if path.name == "README.md" or path.name in skip_briefs:
                continue
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
            title = (fm or {}).get("title", path.stem)
            theme = (fm or {}).get("theme", "")
            out = f"briefs/{_slug(title)}.html"
            model.briefs.append(Page(out, title, body, "brief", theme=theme))
            # let wikilinks reach a brief by title or by file stem
            model.link_map[title] = out
            model.link_map[path.stem] = out

    # --- L1 source notes -------------------------------------------------
    sources_dir = vault_dir / "01 Sources"
    if sources_dir.is_dir():
        # newest day first so the link map points each source key at its latest note
        for day_dir in sorted((d for d in sources_dir.iterdir() if d.is_dir()), reverse=True):
            day = day_dir.name
            for path in sorted(day_dir.glob("*.md")):
                if path.name == "README.md":
                    continue
                key = path.stem
                if key in skip_keys:
                    continue  # held theme — never surface its L1 notes
                fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
                title = (fm or {}).get("source", key)
                out = f"sources/{day}/{key}.html"
                model.sources.append(
                    Page(out, f"{title} — {day}", body, "source", day, theme=src_theme.get(key, ""))
                )
                # first (newest) write wins → latest day for this key
                model.link_map.setdefault(key, out)

    # --- L3 editorial rule (context the briefs live under) ---------------
    rules_dir = vault_dir / "00 Rules"
    if rules_dir.is_dir():
        editorial = rules_dir / "editorial.md"
        if editorial.is_file():
            fm, body = split_frontmatter(editorial.read_text(encoding="utf-8"))
            title = (fm or {}).get("title", "Editorial Line")
            out = "editorial.html"
            model.rules.append(Page(out, title, body, "rule"))
            model.link_map["editorial"] = out

    # --- OKF conformance profile (the USP page) --------------------------
    okf_path = vault_dir / "OKF.md"
    if okf_path.is_file():
        fm, body = split_frontmatter(okf_path.read_text(encoding="utf-8"))
        title = (fm or {}).get("title", "OKF Conformance")
        model.okf = Page("okf.html", title, body, "okf")
        model.link_map["OKF"] = "okf.html"
        model.link_map[title] = "okf.html"

    return model


def _relurl(from_page: str, to_page: str) -> str:
    """Site-relative URL from one output page to another (posix, browser-safe)."""
    from_parts = from_page.split("/")[:-1]  # directory of the source page
    to_parts = to_page.split("/")
    # common prefix
    i = 0
    while i < len(from_parts) and i < len(to_parts) - 1 and from_parts[i] == to_parts[i]:
        i += 1
    ups = [".."] * (len(from_parts) - i)
    rel = "/".join(ups + to_parts[i:])
    return rel or to_page


def resolve_wikilinks(body: str, page: str, link_map: dict[str, str]) -> str:
    """Replace ``[[target|alias]]`` with a markdown link to its rendered page.

    Held / unknown targets degrade to plain alias text (no dangling link).
    """

    def repl(m: re.Match[str]) -> str:
        raw = m.group(1)
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        alias = raw.split("|", 1)[1].strip() if "|" in raw else target
        dest = link_map.get(target)
        if not dest:
            return alias  # excluded or unknown → neutral text, never a 404 link
        return f"[{alias}]({_relurl(page, dest)})"

    return _WIKILINK_RE.sub(repl, body)


_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · azimuth</title>
<link rel="stylesheet" href="{root}assets/style.css">
</head><body>
<header class="nav">
  <a class="brand" href="{root}index.html">azimuth</a>
  <nav>
    <a href="{root}index.html">Briefs</a>
    <a href="{root}index.html#sources">Sources</a>
    <a href="{root}graph.html">Graph</a>
    <a href="{root}editorial.html">Editorial</a>
    <a href="{root}okf.html">OKF</a>
  </nav>
</header>
<main class="content">
{kind_block}
{html_body}
</main>
<footer class="foot">
  azimuth — public demonstrator of the HemySphere L1/L2/L3 vault doctrine.
  Content CC-BY-4.0. Held themes (e.g. prediction-markets) are excluded per the
  <a href="{root}editorial.html">editorial line</a>. Read-only static preview.
</footer>
</body></html>
"""

_KIND_LABEL = {"brief": "L2 Brief", "source": "L1 Source", "rule": "L3 Rule", "okf": "OKF Profile"}


def _render_page(page: Page, link_map: dict[str, str]) -> str:
    depth = page.out_path.count("/")
    root = "../" * depth
    linked = resolve_wikilinks(page.body_md, page.out_path, link_map)
    html_body = md.markdown(linked, extensions=_MD_EXTENSIONS)
    label = _KIND_LABEL.get(page.kind, "")
    kind_block = f'<div class="kind kind-{page.kind}">{label}</div>' if label else ""
    return _PAGE_TEMPLATE.format(
        title=html.escape(page.title),
        root=root,
        kind_block=kind_block,
        html_body=html_body,
    )


def _render_index(model: SiteModel) -> str:
    cards = []
    for b in model.briefs:
        cards.append(
            f'<a class="card" href="{b.out_path}"><span class="card-kind">L2 Brief</span>'
            f"<h3>{html.escape(b.title)}</h3></a>"
        )
    brief_html = "\n".join(cards) or "<p>No active briefs.</p>"

    # sources grouped by day (newest first)
    by_day: dict[str, list[Page]] = {}
    for s in model.sources:
        by_day.setdefault(s.day, []).append(s)
    src_blocks = []
    for day in sorted(by_day, reverse=True):
        items = "".join(
            f'<li><a href="{p.out_path}">{html.escape(p.title.split(" — ")[0])}</a></li>'
            for p in sorted(by_day[day], key=lambda p: p.out_path)
        )
        src_blocks.append(f"<h3>{html.escape(day)}</h3><ul class='src-list'>{items}</ul>")
    sources_html = "\n".join(src_blocks) or "<p>No source notes.</p>"

    body = f"""
<div class="hero">
  <h1>azimuth</h1>
  <p class="usp"><strong>An <a href="okf.html">Open Knowledge Format (OKF&nbsp;v0.1)</a>
  knowledge bundle</strong> — a vendor-neutral, git-distributable corpus of markdown + YAML
  that any OKF-aware agent can traverse with no bespoke parser. azimuth runs the L1/L2/L3 wiki
  doctrine as an instance of a standard Google independently published, proven on live
  open-intelligence data.</p>
  <p>A read-only, browsable view of the vault: weekly
  <strong>L2 briefs</strong> synthesised from dated <strong>L1 source notes</strong>,
  under one published <a href="editorial.html">editorial line</a>.
  Every claim in a brief links to the data it rests on — and the
  <a href="graph.html">graph view</a> makes those cross-source relationships visual.</p>
</div>
<section><h2>Briefs</h2><div class="cards">{brief_html}</div></section>
<section id="sources"><h2>L1 Sources</h2>{sources_html}</section>
"""
    return _PAGE_TEMPLATE.format(
        title="azimuth — open-intelligence vault",
        root="",
        kind_block="",
        html_body=body,
    )


def build_graph(model: SiteModel) -> dict[str, Any]:
    """Derive the relationship graph from the discovered (held-excluded) site model.

    Nodes = L2 briefs + L1 source notes (latest day per key). Edges = the actual
    ``[[wikilink]]`` relationships inside each brief, resolved through the same
    ``link_map`` the rendered pages use — so the graph can never disagree with the
    links a reader clicks. Held themes are already absent from the model, so they are
    absent from the graph for free.
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    # one source node per KEY, the latest-day page (the one the link_map points at) —
    # older dated copies of the same source are not separate graph nodes.
    src_node_by_path: dict[str, str] = {}
    for s in model.sources:
        key = Path(s.out_path).stem
        if model.link_map.get(key) != s.out_path:
            continue  # not the latest-day page for this key
        nid = f"source:{key}"
        src_node_by_path[s.out_path] = nid
        nodes.append(
            {
                "id": nid,
                "label": s.title.split(" — ")[0],
                "kind": "source",
                "theme": s.theme or "other",
                "url": s.out_path,
            }
        )

    for b in model.briefs:
        bid = f"brief:{_slug(b.title)}"
        nodes.append(
            {
                "id": bid,
                "label": b.title,
                "kind": "brief",
                "theme": b.theme or "other",
                "url": b.out_path,
            }
        )
        seen: set[str] = set()
        for m in _WIKILINK_RE.finditer(b.body_md):
            target = m.group(1).split("|", 1)[0].split("#", 1)[0].strip()
            dest = model.link_map.get(target)
            tnid = src_node_by_path.get(dest or "")
            if tnid and tnid not in seen:
                seen.add(tnid)
                edges.append({"source": bid, "target": tnid})

    return {"nodes": nodes, "edges": edges}


_GRAPH_TEMPLATE = """<!DOCTYPE html>
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
<h1>Relationship graph</h1>
<p class="hero-sub">Every <strong>L2 brief</strong> (large node) links to the dated
<strong>L1 source notes</strong> (small nodes) its claims rest on, coloured by theme.
This is the lightweight link-graph view of the OKF bundle — drag a node, click it to open
the page. Held themes never appear. A richer entity/hypergraph layer is the planned next
step (see <a href="okf.html">OKF</a>).</p>
<div id="legend" class="legend"></div>
<canvas id="g" width="820" height="520"></canvas>
<noscript><p>Enable JavaScript to view the interactive graph, or browse the
<a href="index.html">briefs and sources</a> directly.</p></noscript>
<div id="glist"></div>
</main>
<footer class="foot">
  azimuth — public demonstrator of the HemySphere L1/L2/L3 vault doctrine.
  Content CC-BY-4.0. Read-only static preview.
</footer>
<script>
const GRAPH = {graph_json};
const THEME_COLORS = {"energy-supply":"#4cc2ff","geophysical":"#ff9d4c",
"prediction-markets":"#b07cff","other":"#8a97a8"};
const cv = document.getElementById("g"), cx = cv.getContext("2d");
const themes = [...new Set(GRAPH.nodes.map(n => n.theme))];
document.getElementById("legend").innerHTML = themes.map(t =>
  `<span class="lg"><i style="background:${THEME_COLORS[t]||THEME_COLORS.other}"></i>${t}</span>`
).join("");
// text fallback / accessibility list
document.getElementById("glist").innerHTML =
  "<details><summary>Graph as a list</summary><ul>" +
  GRAPH.nodes.filter(n => n.kind === "brief").map(b => {
    const kids = GRAPH.edges.filter(e => e.source === b.id)
      .map(e => GRAPH.nodes.find(n => n.id === e.target))
      .filter(Boolean)
      .map(n => `<a href="${n.url}">${n.label}</a>`).join(", ");
    return `<li><a href="${b.url}"><strong>${b.label}</strong></a> &rarr; ${kids||"&mdash;"}</li>`;
  }).join("") + "</ul></details>";
// simple force layout
const W = cv.width, H = cv.height;
const N = GRAPH.nodes.map((n, i) => ({
  ...n, x: W/2 + Math.cos(i)*180 + (i%5)*7, y: H/2 + Math.sin(i*1.7)*150 + (i%3)*5,
  vx: 0, vy: 0, r: n.kind === "brief" ? 13 : 7
}));
const idx = Object.fromEntries(N.map(n => [n.id, n]));
const E = GRAPH.edges.map(e => ({s: idx[e.source], t: idx[e.target]})).filter(e => e.s && e.t);
function step() {
  for (const a of N) {
    for (const b of N) {
      if (a === b) continue;
      let dx = a.x-b.x, dy = a.y-b.y, d = Math.hypot(dx,dy)||1;
      const f = 2600/(d*d);
      a.vx += (dx/d)*f; a.vy += (dy/d)*f;
    }
    a.vx += (W/2-a.x)*0.0025; a.vy += (H/2-a.y)*0.0025;
  }
  for (const e of E) {
    let dx = e.t.x-e.s.x, dy = e.t.y-e.s.y, d = Math.hypot(dx,dy)||1;
    const f = (d-120)*0.012;
    e.s.vx += (dx/d)*f; e.s.vy += (dy/d)*f;
    e.t.vx -= (dx/d)*f; e.t.vy -= (dy/d)*f;
  }
  for (const a of N) {
    a.x += a.vx*0.5; a.y += a.vy*0.5; a.vx *= 0.82; a.vy *= 0.82;
    a.x = Math.max(a.r, Math.min(W-a.r, a.x)); a.y = Math.max(a.r, Math.min(H-a.r, a.y));
  }
}
function draw() {
  cx.clearRect(0,0,W,H);
  cx.strokeStyle = "#2a3a4d"; cx.lineWidth = 1;
  for (const e of E) { cx.beginPath(); cx.moveTo(e.s.x,e.s.y); cx.lineTo(e.t.x,e.t.y); cx.stroke(); }
  for (const n of N) {
    cx.beginPath(); cx.arc(n.x,n.y,n.r,0,7); cx.fillStyle = THEME_COLORS[n.theme]||THEME_COLORS.other;
    cx.globalAlpha = n.kind === "brief" ? 1 : 0.85; cx.fill(); cx.globalAlpha = 1;
    if (n.kind === "brief") {
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


def _render_graph(graph: dict[str, Any]) -> str:
    import json

    return _GRAPH_TEMPLATE.replace("{graph_json}", json.dumps(graph))


_CSS = """:root{--bg:#0c0f14;--panel:#141a23;--ink:#e7edf5;--muted:#8a97a8;
--accent:#4cc2ff;--line:#222c39;--held:#3a4250}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.62}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.nav{display:flex;gap:1.5rem;align-items:center;padding:.9rem 1.2rem;
border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(12,15,20,.92);
backdrop-filter:blur(6px)}
.brand{font-family:Rajdhani,Inter,sans-serif;font-weight:700;font-size:1.3rem;
letter-spacing:.06em;text-transform:uppercase}
.nav nav{display:flex;gap:1.1rem;font-size:.92rem}
.content,.foot{max-width:820px;margin:0 auto;padding:1.4rem 1.2rem}
.kind{display:inline-block;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;
color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.15rem .6rem;
margin-bottom:1rem}
.kind-brief{color:var(--accent);border-color:var(--accent)}
h1,h2,h3{font-family:Rajdhani,Inter,sans-serif;letter-spacing:.01em;line-height:1.2}
h1{font-size:2.1rem;margin:.2rem 0}h2{margin-top:2rem;border-bottom:1px solid var(--line);
padding-bottom:.3rem}
.hero p{color:var(--muted);max-width:64ch}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:.9rem}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:1rem 1.1rem;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--accent);transform:translateY(-2px);text-decoration:none}
.card-kind{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.card h3{margin:.4rem 0 0}
.src-list{columns:2;gap:1.4rem;list-style:none;padding-left:0}
@media(max-width:560px){.src-list{columns:1}}
table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.92rem;display:block;
overflow-x:auto}
th,td{border:1px solid var(--line);padding:.45rem .6rem;text-align:left;vertical-align:top}
th{background:var(--panel)}
blockquote{border-left:3px solid var(--accent);margin:1rem 0;padding:.2rem 1rem;
color:var(--muted);background:var(--panel);border-radius:0 8px 8px 0}
code{background:var(--panel);padding:.1rem .35rem;border-radius:5px;
font-family:JetBrains Mono,ui-monospace,monospace;font-size:.88em}
.foot{color:var(--muted);font-size:.8rem;border-top:1px solid var(--line);margin-top:2rem}
.usp{color:var(--ink);background:var(--panel);border:1px solid var(--line);
border-left:3px solid var(--accent);border-radius:0 10px 10px 0;padding:.8rem 1rem;max-width:68ch}
.usp a{font-weight:700}
.hero-sub{color:var(--muted);max-width:68ch}
.kind-okf{color:#b07cff;border-color:#b07cff}
#g{width:100%;max-width:820px;height:auto;background:var(--panel);border:1px solid var(--line);
border-radius:12px;margin:1rem 0;touch-action:none;cursor:grab}
.legend{display:flex;gap:1rem;flex-wrap:wrap;font-size:.82rem;color:var(--muted);margin:.5rem 0}
.legend .lg{display:inline-flex;align-items:center;gap:.4rem}
.legend i{width:.7rem;height:.7rem;border-radius:50%;display:inline-block}
#glist details{margin-top:1rem}#glist summary{cursor:pointer;color:var(--muted)}
"""


def build_site(
    out_dir: Path,
    vault_dir: Path = DEFAULT_VAULT,
    registry_path: Path = DEFAULT_REGISTRY,
) -> SiteModel:
    """Render the whole site into ``out_dir`` (cleared first). Returns the model."""
    import json

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    model = discover(vault_dir, registry)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "assets").mkdir(parents=True, exist_ok=True)
    (out_dir / "assets" / "style.css").write_text(_CSS, encoding="utf-8")

    pages = [*model.briefs, *model.sources, *model.rules]
    if model.okf is not None:
        pages.append(model.okf)
    for page in pages:
        target = out_dir / page.out_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_page(page, model.link_map), encoding="utf-8")

    (out_dir / "index.html").write_text(_render_index(model), encoding="utf-8")

    graph = build_graph(model)
    (out_dir / "graph.html").write_text(_render_graph(graph), encoding="utf-8")
    (out_dir / "graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    return model
