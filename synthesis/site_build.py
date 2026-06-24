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
    kind: str  # "brief" | "source" | "rule"
    day: str = ""  # only for source pages


@dataclass
class SiteModel:
    """Everything the renderer needs, after held-theme exclusion."""

    briefs: list[Page] = field(default_factory=list)
    sources: list[Page] = field(default_factory=list)
    rules: list[Page] = field(default_factory=list)
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
    model = SiteModel()

    # --- L2 briefs (landing surface) -------------------------------------
    briefs_dir = vault_dir / "02 Briefs"
    if briefs_dir.is_dir():
        for path in sorted(briefs_dir.glob("*.md")):
            if path.name == "README.md" or path.name in skip_briefs:
                continue
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
            title = (fm or {}).get("title", path.stem)
            out = f"briefs/{_slug(title)}.html"
            model.briefs.append(Page(out, title, body, "brief"))
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
                model.sources.append(Page(out, f"{title} — {day}", body, "source", day))
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
    <a href="{root}index.html#how">How it works</a>
    <a href="{root}index.html">Briefs</a>
    <a href="{root}index.html#sources">Sources</a>
    <a href="{root}graph.html">Graph</a>
    <a href="{root}editorial.html">Editorial line</a>
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

_KIND_LABEL = {"brief": "L2 Brief", "source": "L1 Source", "rule": "L3 Rule"}


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
  <p class="lede">A public demonstrator of <strong>Emi</strong> — a <strong>living</strong>
  knowledge system. Not a static archive: a system that <strong>creates, connects,
  governs and updates</strong> open-intelligence knowledge on a weekly cadence. Every
  week it ingests fresh data, synthesises it into briefs, links it across sources, and
  publishes under one editorial line — then does it again.</p>
  <p class="thesis">OKF is the skeleton; Emi is the organism.</p>
</div>

<section id="how">
  <h2>How this works — why it&#39;s more than a format</h2>
  <p class="how-intro">A static format standardises how knowledge is <em>stored</em>.
  Emi is the living loop that <em>produces</em> it — autonomous L1 ingest, AI L2
  synthesis, cross-source connections and an editorial L3 line, refreshed every week.
  Watch one cycle:</p>
  <ol class="loop">
    <li><span class="loop-n">1</span><strong>Ingest</strong><em>L1 — daily open data pulled into dated source notes</em></li>
    <li><span class="loop-n">2</span><strong>Synthesise</strong><em>L2 — AI distils the week&#39;s sources into briefs</em></li>
    <li><span class="loop-n">3</span><strong>Connect</strong><em>cross-source links + a shared-entity graph</em></li>
    <li><span class="loop-n">4</span><strong>Govern</strong><em>L3 — one editorial line; held themes excluded</em></li>
    <li><span class="loop-n">5</span><strong>Update</strong><em>weekly cadence — the loop runs again, alive</em></li>
  </ol>
  <p class="okf-note">azimuth also <strong>speaks OKF</strong> — Google&#39;s
  <a href="https://github.com/google/open-knowledge-format">Open Knowledge Format</a>,
  the vendor-neutral standard for how a knowledge bundle is stored — so any OKF-aware
  tool can read it. That&#39;s a credibility and interop detail: OKF defines the
  skeleton; the loop above is the organism that fills it.</p>
</section>

<section><h2>Briefs</h2><div class="cards">{brief_html}</div></section>
<section id="sources"><h2>L1 Sources</h2>{sources_html}</section>
"""
    return _PAGE_TEMPLATE.format(
        title="azimuth — open-intelligence vault",
        root="",
        kind_block="",
        html_body=body,
    )


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
.lede{font-size:1.12rem;color:var(--ink);max-width:66ch}
.thesis{font-family:Rajdhani,Inter,sans-serif;font-size:1.35rem;letter-spacing:.01em;
color:var(--accent);margin:.6rem 0 0;font-weight:600}
.how-intro,.okf-note{color:var(--muted);max-width:68ch}
.okf-note{font-size:.92rem;border-top:1px solid var(--line);padding-top:1rem;margin-top:1.4rem}
.loop{list-style:none;padding:0;margin:1.2rem 0;display:grid;
grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.7rem;counter-reset:loop}
.loop li{position:relative;background:var(--panel);border:1px solid var(--line);
border-radius:12px;padding:1rem .9rem .9rem;display:flex;flex-direction:column;gap:.3rem}
.loop li::after{content:"\\2192";position:absolute;right:-.62rem;top:50%;
transform:translateY(-50%);color:var(--accent);font-size:1.1rem;z-index:1}
.loop li:last-child::after{content:""}
@media(max-width:560px){.loop li::after{content:"\\2193";right:50%;top:auto;
bottom:-.95rem;transform:translateX(50%)}}
.loop-n{display:inline-flex;align-items:center;justify-content:center;width:1.6rem;
height:1.6rem;border-radius:999px;background:var(--accent);color:#04121b;font-weight:700;
font-size:.85rem;font-family:Rajdhani,Inter,sans-serif}
.loop strong{font-family:Rajdhani,Inter,sans-serif;font-size:1.05rem;letter-spacing:.02em}
.loop em{color:var(--muted);font-size:.82rem;font-style:normal;line-height:1.4}
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

    for page in [*model.briefs, *model.sources, *model.rules]:
        target = out_dir / page.out_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_page(page, model.link_map), encoding="utf-8")

    (out_dir / "index.html").write_text(_render_index(model), encoding="utf-8")
    return model
