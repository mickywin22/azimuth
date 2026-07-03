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
from functools import cache
from pathlib import Path
from typing import Any


@cache
def _md() -> Any:
    """Import the ``markdown`` package lazily — only the HTML render path needs it.

    ``markdown`` lives in the ``site`` optional-dependency group (pyproject), not in base
    deps or ``dev``. Importing this module for its constants/helpers must therefore NOT
    require it: ``scripts/build_graph.py`` pulls ``DEFAULT_VAULT``/``_slug``/``held_*`` from
    here and runs in the stdlib-only Synthesis-Lint CI job and the ``.[dev]`` test job,
    neither of which installs ``site``. A top-level ``import markdown`` made the graph
    ``--check`` guard and ``test_build_graph`` collection fail on every CI run. Deferring
    the import to call time keeps the non-rendering paths pure-stdlib.
    """
    import markdown  # type: ignore[import-untyped]

    return markdown


_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.answers import Answer, AnswerSet, build_answer_set  # noqa: E402
from synthesis.benchmark import Benchmark, build_benchmark  # noqa: E402
from synthesis.lint import split_frontmatter  # noqa: E402

# A repo-local registry / vault path pair, overridable for tests.
DEFAULT_VAULT = _REPO_ROOT / "vault"
DEFAULT_REGISTRY = _REPO_ROOT / "sources" / "registry.json"

README = "README.md"
# The TOP5 demonstrator brief: lint-gated markdown, but surfaced as the dedicated
# answers.html (rendered live from synthesis/answers.py), never as a generic brief card.
DEMONSTRATOR_BRIEF = "Top5 Answers.md"
# The benchmark brief: lint-gated markdown, surfaced as the dedicated benchmark.html
# (rendered live from synthesis/benchmark.py), never as a generic brief card.
BENCHMARK_BRIEF = "Benchmark.md"

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists", "nl2br"]

_DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def latest_source_day(vault_dir: Path = DEFAULT_VAULT) -> str:
    """Latest ingest day (``YYYY-MM-DD``) present under ``vault/01 Sources/``.

    This is the site-wide data-freshness signal: the newest dated L1 folder is, by
    construction, the most recent ingest the published bundle rests on. Returns ""
    when the tree has no dated folders (empty test vaults) — renderers then omit
    the badge instead of showing a wrong date.
    """
    sources_dir = vault_dir / "01 Sources"
    if not sources_dir.is_dir():
        return ""
    days = [d.name for d in sources_dir.iterdir() if d.is_dir() and _DAY_DIR_RE.match(d.name)]
    return max(days, default="")


def _fresh_badge(day: str) -> str:
    """Header badge HTML for the freshness signal ('' when no day is known)."""
    if not day:
        return ""
    return f'<span class="fresh-badge">Data as of {html.escape(day)}</span>'


@dataclass
class Page:
    """One rendered output page."""

    out_path: str  # site-relative posix path, e.g. "sources/2026-06-20/fuel-prices.html"
    title: str
    body_md: str
    kind: str  # "brief" | "source" | "rule"
    day: str = ""  # only for source pages
    updated: str = ""  # only for briefs: YYYY-MM-DD from the `updated:` frontmatter


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
            # README + held briefs skipped; the TOP5 demonstrator brief is the lint-gated
            # source-of-truth markdown, but its public surface is the dedicated answers.html
            # (rendered live from the answer engine), so it is not also a generic brief card.
            if (
                path.name in (README, DEMONSTRATOR_BRIEF, BENCHMARK_BRIEF)
                or path.name in skip_briefs
            ):
                continue
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
            title = (fm or {}).get("title", path.stem)
            # `updated:` is an ISO timestamp in the brief frontmatter; the date part is
            # the visible per-brief freshness signal (card + page header).
            updated = str((fm or {}).get("updated", ""))[:10]
            out = f"briefs/{_slug(title)}.html"
            model.briefs.append(Page(out, title, body, "brief", updated=updated))
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
    <a href="{root}answers.html">Ask the data</a>
    <a href="{root}benchmark.html">Benchmark</a>
    <a href="{root}graph.html">Knowledge graph</a>
    <a href="{root}index.html">Briefs</a>
    <a href="{root}index.html#sources">Sources</a>
    <a href="{root}editorial.html">Editorial line</a>
  </nav>
  {fresh_badge}
</header>
<main class="content">
{kind_block}
{html_body}
</main>
<footer class="foot">
  azimuth — public demonstrator of the HemySphere L1/L2/L3 vault doctrine.
  Content CC-BY-4.0. Channels are surfaced on the facts-in / opinions-out
  <a href="{root}editorial.html">editorial line</a>; a held theme is paused on license
  or synthesis-breadth grounds, not topic sensitivity. Read-only static preview.
</footer>
</body></html>
"""

_KIND_LABEL = {"brief": "L2 Brief", "source": "L1 Source", "rule": "L3 Rule"}


def _render_page(page: Page, link_map: dict[str, str], fresh_day: str = "") -> str:
    depth = page.out_path.count("/")
    root = "../" * depth
    linked = resolve_wikilinks(page.body_md, page.out_path, link_map)
    html_body = _md().markdown(linked, extensions=_MD_EXTENSIONS)
    label = _KIND_LABEL.get(page.kind, "")
    if label and page.updated:
        # freshness at page entry — the kind pill a reader sees first, not a buried line
        label = f"{label} · updated {html.escape(page.updated)}"
    kind_block = f'<div class="kind kind-{page.kind}">{label}</div>' if label else ""
    return _PAGE_TEMPLATE.format(
        title=html.escape(page.title),
        root=root,
        kind_block=kind_block,
        html_body=html_body,
        fresh_badge=_fresh_badge(fresh_day),
    )


def _render_index(model: SiteModel, aset: AnswerSet | None = None, fresh_day: str = "") -> str:
    cards = []
    for b in model.briefs:
        card_fresh = (
            f'<span class="card-fresh">Updated {html.escape(b.updated)}</span>'
            if b.updated
            else ""
        )
        cards.append(
            f'<a class="card" href="{b.out_path}"><span class="card-kind">L2 Brief</span>'
            f"<h3>{html.escape(b.title)}</h3>{card_fresh}</a>"
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

    n_answers = len(aset.answers) if aset else 0
    hero_fresh = (
        f'<p class="hero-fresh"><span class="fresh-badge">Data as of {html.escape(fresh_day)}'
        f"</span> — the latest L1 ingest in the published bundle.</p>"
        if fresh_day
        else ""
    )
    body = f"""
<div class="hero">
  <h1>azimuth</h1>
  {hero_fresh}
  <p>A read-only, browsable view of the open-intelligence vault: weekly
  <strong>L2 briefs</strong> synthesised from dated <strong>L1 source notes</strong>,
  under one published <a href="editorial.html">editorial line</a>.
  Every claim in a brief links to the data it rests on.</p>
</div>
<a class="demo-cta" href="answers.html">
  <span class="demo-kind">The demonstrator</span>
  <h2>Ask the World Data &rarr;</h2>
  <p>The {n_answers} cross-source questions azimuth answers from live data &mdash; energy,
  geophysics and climate read <em>together</em>. Every claim links to its L1 source.
  A static feed stores each channel; only a living system connects them.</p>
</a>
<a class="demo-cta benchmark-cta" href="benchmark.html">
  <span class="demo-kind">The benchmark</span>
  <h2>Facts vs Forecast vs Intelligence &rarr;</h2>
  <p><em>Why not just read a forecast or an intel feed?</em> The same world-topic, three
  columns: azimuth&rsquo;s observed + sourced facts vs a forecast&rsquo;s probability vs an
  analyst&rsquo;s assessment. A fair head-to-head &mdash; azimuth wins on provenance,
  neutrality and reproducibility; a forecast legitimately wins on looking ahead. We say so.</p>
</a>
<a class="demo-cta graph-cta" href="graph.html">
  <span class="demo-kind">The knowledge graph</span>
  <h2>Explore the cross-channel graph &rarr;</h2>
  <p>Every channel, brief, source note and shared entity as one interactive, evidence-weighted
  graph<span id="graph-cta-stats"></span>. Gold bridges mark places the live data records under
  more than one theme &mdash; trace two channels and the page quotes the literal L1 source
  lines that join them. The cross-channel link a static feed cannot draw.</p>
</a>
<script>
// Progressive enhancement only: fill in the live graph size from the published
// graph.json. The card reads fine without it (fetch can fail on file:// previews).
fetch("graph.json").then(function(r){{return r.json()}}).then(function(g){{
  var bridges = g.nodes.filter(function(n){{
    return n.kind === "entity" && (n.themes || []).length >= 2;
  }}).length;
  document.getElementById("graph-cta-stats").textContent =
    " — " + g.nodes.length + " nodes, " + g.edges.length + " edges, " +
    bridges + " cross-channel bridges today";
}}).catch(function(){{}});
</script>
<section><h2>Briefs</h2><div class="cards">{brief_html}</div></section>
<section id="sources"><h2>L1 Sources</h2>{sources_html}</section>
"""
    return _PAGE_TEMPLATE.format(
        title="azimuth — open-intelligence vault",
        root="",
        kind_block="",
        html_body=body,
        fresh_badge=_fresh_badge(fresh_day),
    )


_WHATIF_SCRIPT = """<script>
// Pure presentational toggle: no verdict logic runs in the browser. Both the real and the
// counterfactual verdict are baked at build time by synthesis/answers.py; this only swaps
// which precomputed block is visible. Flip the input -> the baked recompute shows. That IS
// the proof: the answer is computed from the bundle, not canned.
document.querySelectorAll('.whatif').forEach(function (panel) {
  panel.querySelectorAll('.wf-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var mode = btn.getAttribute('data-mode'); // 'real' | 'cf'
      panel.querySelectorAll('.wf-btn').forEach(function (b) {
        b.classList.toggle('is-on', b === btn);
        b.setAttribute('aria-pressed', String(b === btn));
      });
      panel.querySelectorAll('.wf-show-real').forEach(function (el) {
        el.hidden = (mode !== 'real');
      });
      panel.querySelectorAll('.wf-show-cf').forEach(function (el) {
        el.hidden = (mode !== 'cf');
      });
      panel.classList.toggle('is-cf', mode === 'cf');
    });
  });
});
</script>"""


def _render_whatif(a: Answer, page: str, link_map: dict[str, str]) -> str:
    """Render the "show your work / what-if" panel for an answer that carries a counterfactual.

    Both verdicts are precomputed in ``synthesis/answers.py``; this renders them side by side
    (only one visible at a time) plus the flipped input number, its L1 link, and which
    truth-table branch fired. The toggle (``_WHATIF_SCRIPT``) is pure presentation.
    """
    wf = a.whatif
    if wf is None or not a.claims:
        return ""
    real_verdict = _md().markdown(
        resolve_wikilinks(a.claims[0].md, page, link_map), extensions=_MD_EXTENSIONS
    )
    cf_verdict = _md().markdown(
        resolve_wikilinks(wf.flipped_verdict, page, link_map), extensions=_MD_EXTENSIONS
    )
    cite = resolve_wikilinks(" · ".join(f"[[{s}]]" for s in wf.sources), page, link_map)
    cite_html = _md().markdown(cite, extensions=_MD_EXTENSIONS)
    return (
        f'<div class="whatif" data-qid="{html.escape(a.qid)}">'
        f'<div class="whatif-head">'
        f'<span class="whatif-kind">Show your work — what if the data were different?</span>'
        f'<div class="whatif-toggle" role="group" aria-label="Toggle real vs counterfactual data">'
        f'<button type="button" class="wf-btn is-on" data-mode="real" aria-pressed="true">'
        f"Real data</button>"
        f'<button type="button" class="wf-btn" data-mode="cf" aria-pressed="false">'
        f"Flip the input</button>"
        f"</div></div>"
        f'<p class="whatif-input"><strong>Input fed to the verdict:</strong> '
        f"{html.escape(wf.input_label)} — "
        f'<span class="wf-show-real"><code>{html.escape(wf.real_value)}</code></span>'
        f'<span class="wf-show-cf" hidden><code>{html.escape(wf.flipped_value)}</code> '
        f"<em>(sign flipped)</em></span></p>"
        f'<div class="whatif-src">From L1: {cite_html}</div>'
        f'<p class="whatif-branch"><strong>Truth-table branch fired:</strong> '
        f'<span class="wf-show-real"><code>{html.escape(wf.real_branch)}</code></span>'
        f'<span class="wf-show-cf" hidden><code>{html.escape(wf.flipped_branch)}</code></span></p>'
        f'<div class="whatif-verdict">'
        f'<div class="wf-show-real">{real_verdict}</div>'
        f'<div class="wf-show-cf" hidden>{cf_verdict}</div>'
        f"</div>"
        f'<p class="whatif-note">The verdict you see is recomputed from the input above by '
        f"<code>synthesis/answers.py</code> at build time — flip the sign and the branch, and "
        f"the verdict, change. Nothing is canned.</p>"
        f"</div>"
    )


def _render_answers(aset: AnswerSet, link_map: dict[str, str], fresh_day: str = "") -> str:
    """Render the demonstrator page: the TOP5 cross-channel answers, every claim sourced.

    Claim bullets keep their ``[[stem]]`` citations; ``resolve_wikilinks`` turns each into a
    link to that L1 source page (the "every claim links to the data" promise made literal).
    """
    page = "answers.html"
    blocks: list[str] = []
    for a in aset.answers:
        chips = "".join(f'<span class="chip">{html.escape(c)}</span>' for c in a.channels)
        bullets: list[str] = []
        for claim in a.claims:
            linked = resolve_wikilinks(claim.md, page, link_map)
            bullets.append(f"<li>{_md().markdown(linked, extensions=_MD_EXTENSIONS)}</li>")
        whatif_html = _render_whatif(a, page, link_map)
        blocks.append(
            f'<article class="qa">'
            f'<div class="qa-head"><span class="qa-id">{html.escape(a.qid)}</span>'
            f"<h2>{html.escape(a.question)}</h2></div>"
            f'<div class="chips">{chips}</div>'
            f'<p class="persona"><strong>Serves:</strong> {html.escape(a.persona)}</p>'
            f"<ul class='claims'>{''.join(bullets)}</ul>"
            f"{whatif_html}"
            f"</article>"
        )
    answers_html = "\n".join(blocks)
    week = html.escape(aset.week or "this week")
    body = f"""
<div class="kind kind-brief">Demonstrator</div>
<div class="hero">
  <h1>Ask the World Data</h1>
  <p>These are the cross-source questions azimuth answers &mdash; the ones a single feed,
  or a static OKF bundle, cannot. Each answer connects <strong>two or more channels</strong>
  (energy, geophysics, climate), links <strong>every factual claim to its L1 source note</strong>,
  and names the <strong>use-case</strong> it serves. Generated live from the {week} bundle and
  regenerated every weekly cycle &mdash; the <em>living</em> answer is the point.</p>
</div>
{answers_html}
<section class="howmade">
  <h2>How these answers are made</h2>
  <blockquote>Generated deterministically by <code>synthesis/answers.py</code> from the live
  L1 bundle (the latest dated note per editorially-clean source key; held themes excluded).
  Numbers are read straight from the source notes &mdash; nothing is invented. An honest,
  sourced &ldquo;no significant overlap&rdquo; is itself a valid answer when that is what the
  week&rsquo;s data shows. Re-run after any ingest and the answers refresh in place.</blockquote>
</section>
{_WHATIF_SCRIPT}
"""
    return _PAGE_TEMPLATE.format(
        title="Ask the World Data — azimuth demonstrator",
        root="",
        kind_block="",
        html_body=body,
        fresh_badge=_fresh_badge(fresh_day),
    )


def _render_benchmark(bench: Benchmark, link_map: dict[str, str], fresh_day: str = "") -> str:
    """Render the benchmark page: same topic, three columns, scorecard, verdict.

    azimuth's claim bullets keep their ``[[stem]]`` citations and resolve through the same
    link map as the briefs (every fact clickable to its L1 note — the literal proof of the
    USP). The forecast / intelligence columns are the quoted compared product, attributed by
    product + capture date, deliberately NOT clickable L1 links.
    """
    page = "benchmark.html"
    blocks: list[str] = []
    for t in bench.topics:
        az_bullets = "".join(
            f"<li>{_md().markdown(resolve_wikilinks(c.md, page, link_map), extensions=_MD_EXTENSIONS)}</li>"
            for c in t.azimuth_claims
        )
        # forecast column
        if t.forecast.present:
            fc_extra = (
                f'<p class="proj">{html.escape(t.forecast.projection_note)}</p>'
                if t.forecast.projection_note
                else ""
            )
            fc_body = (
                f"{_md().markdown(html.escape(t.forecast.headline), extensions=_MD_EXTENSIONS)}"
                f"{fc_extra}"
                f'<p class="attr">{html.escape(t.forecast.attribution)}</p>'
            )
        else:
            fc_body = f'<p class="absent">{html.escape(t.forecast.headline)}</p>'
        # intelligence column
        if t.intelligence.present:
            lens = (
                f'<p class="lens"><strong>Actor lens:</strong> {html.escape(t.intelligence.actor_lens)}</p>'
                if t.intelligence.actor_lens
                else ""
            )
            intel_body = (
                f"<p>{html.escape(t.intelligence.headline)}</p>{lens}"
                f'<p class="attr">{html.escape(t.intelligence.attribution)}</p>'
            )
        else:
            intel_body = f'<p class="absent">{html.escape(t.intelligence.headline)}</p>'

        rows = "".join(
            f"<tr class='{'win' if r.azimuth_wins else 'concede'}'>"
            f"<td class='dim'>{html.escape(r.dimension)}</td>"
            f"<td class='cell-az'>{html.escape(r.azimuth)}</td>"
            f"<td>{html.escape(r.forecast)}</td>"
            f"<td>{html.escape(r.intelligence)}</td></tr>"
            for r in t.scorecard
        )
        verdict_html = _md().markdown(
            resolve_wikilinks(t.verdict.md, page, link_map), extensions=_MD_EXTENSIONS
        )
        chips = "".join(f'<span class="chip">{html.escape(c)}</span>' for c in t.azimuth_channels)
        blocks.append(
            f'<article class="bench">'
            f"<h2>{html.escape(t.title)}</h2>"
            f'<p class="bench-q"><strong>Head-to-head:</strong> {html.escape(t.question)}</p>'
            f'<div class="cols">'
            f'<div class="col col-az"><div class="col-kind">azimuth — observed facts</div>'
            f'<div class="chips">{chips}</div><ul class="claims">{az_bullets}</ul></div>'
            f'<div class="col col-fc"><div class="col-kind">Forecast product — projection</div>{fc_body}</div>'
            f'<div class="col col-int"><div class="col-kind">Intelligence product — assessment</div>{intel_body}</div>'
            f"</div>"
            f'<table class="score"><thead><tr><th>Dimension</th><th>azimuth</th>'
            f"<th>Forecast</th><th>Intelligence</th></tr></thead><tbody>{rows}</tbody></table>"
            f'<div class="verdict">{verdict_html}</div>'
            f"</article>"
        )
    body_blocks = "\n".join(blocks)
    week = html.escape(bench.week or "this week")
    captured = html.escape(bench.foil_captured_at or "this cycle")
    body = f"""
<div class="kind kind-brief">Benchmark</div>
<div class="hero">
  <h1>Facts vs Forecast vs Intelligence</h1>
  <p><em>Why not just read a forecast or an intelligence feed?</em> Here is the same
  world-topic through three columns &mdash; <strong>azimuth</strong> (observed facts from the
  live {week} bundle, every claim clickable to its L1 source), a <strong>forecast</strong>
  product (a model probability), and an <strong>intelligence</strong> product (an analyst
  assessment). A fair contrast, not a strawman: azimuth wins on provenance, neutrality and
  reproducibility; a forecast / intel feed legitimately wins on <strong>forward-looking
  coverage</strong>. The forecast / intelligence columns quote WorldMonitor as the
  <em>compared product</em> (captured {captured}), deliberately not a clickable L1 link &mdash;
  because that is exactly the difference.</p>
</div>
{body_blocks}
<section class="howmade">
  <h2>How this benchmark is made</h2>
  <blockquote>azimuth&rsquo;s columns are generated deterministically by
  <code>synthesis/benchmark.py</code> from the live L1 bundle &mdash; every figure read straight
  from a source note, every claim carrying its inline L1-source citation, nothing invented and
  nothing predicted. The forecast and intelligence columns are a dated snapshot of the compared
  product, captured by <code>scripts/pull_benchmark_foils.py</code> on the weekly cadence and
  quoted by product + date. azimuth&rsquo;s own columns never editorialise or predict.</blockquote>
</section>
"""
    return _PAGE_TEMPLATE.format(
        title="Benchmark — facts vs forecast vs intelligence — azimuth",
        root="",
        kind_block="",
        html_body=body,
        fresh_badge=_fresh_badge(fresh_day),
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
.fresh-badge{margin-left:auto;font-size:.74rem;letter-spacing:.04em;color:var(--muted);
border:1px solid var(--line);border-radius:999px;padding:.15rem .6rem;white-space:nowrap}
.hero-fresh{margin:.1rem 0 .4rem}
.hero-fresh .fresh-badge{margin-left:0;color:var(--accent);border-color:var(--accent)}
.card-fresh{display:block;font-size:.72rem;color:var(--muted);margin-top:.45rem}
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
.demo-cta{display:block;background:linear-gradient(135deg,#15212e,#101722);
border:1px solid var(--accent);border-radius:14px;padding:1.3rem 1.4rem;margin:1.4rem 0 .5rem;
transition:transform .15s,box-shadow .15s}
.demo-cta:hover{transform:translateY(-2px);text-decoration:none;
box-shadow:0 6px 26px rgba(76,194,255,.18)}
.demo-cta h2{margin:.2rem 0;border:0;padding:0;color:var(--accent)}
.demo-cta p{color:var(--ink);margin:.3rem 0 0;max-width:70ch}
.demo-kind{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.qa{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:1.1rem 1.3rem;margin:1.1rem 0}
.qa-head{display:flex;gap:.7rem;align-items:baseline}
.qa-id{font-family:JetBrains Mono,monospace;color:var(--accent);font-weight:700}
.qa h2{margin:.1rem 0;border:0;padding:0;font-size:1.25rem}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.6rem 0}
.chip{font-size:.72rem;letter-spacing:.04em;color:var(--accent);border:1px solid var(--accent);
border-radius:999px;padding:.12rem .6rem}
.persona{color:var(--muted);font-size:.9rem;margin:.2rem 0 .6rem}
.claims{padding-left:1.1rem;margin:.2rem 0}.claims li{margin:.45rem 0}
.claims li p{margin:0}
.howmade{margin-top:2rem}
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
.benchmark-cta{background:linear-gradient(135deg,#1d1726,#14101c);border-color:#a98bff}
.benchmark-cta h2{color:#c9b3ff}
.benchmark-cta:hover{box-shadow:0 6px 26px rgba(169,139,255,.18)}
.graph-cta{background:linear-gradient(135deg,#26200f,#161209);border-color:#e0b34c}
.graph-cta h2{color:#ffd166}
.graph-cta:hover{box-shadow:0 6px 26px rgba(224,179,76,.18)}
.bench{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:1.1rem 1.3rem;margin:1.4rem 0}
.bench h2{margin:.1rem 0 .4rem;border:0;padding:0;font-size:1.3rem}
.bench-q{color:var(--muted);font-size:.95rem;margin:.2rem 0 .9rem}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin:.5rem 0 1rem}
@media(max-width:680px){.cols{grid-template-columns:1fr}}
.col{border:1px solid var(--line);border-radius:10px;padding:.7rem .85rem;background:#0f141b}
.col-az{border-color:var(--accent)}
.col-fc{border-color:#caa86a}.col-int{border-color:#a98bff}
.col-kind{font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);
margin-bottom:.5rem;font-weight:600}
.col-az .col-kind{color:var(--accent)}.col-fc .col-kind{color:#caa86a}
.col-int .col-kind{color:#a98bff}
.col p{margin:.4rem 0;font-size:.9rem}
.col .claims{padding-left:1rem;margin:.2rem 0}.col .claims li{margin:.4rem 0;font-size:.9rem}
.col .attr{color:var(--muted);font-size:.74rem;font-style:italic;margin-top:.6rem}
.col .proj{font-family:JetBrains Mono,monospace;font-size:.8rem;color:var(--ink)}
.col .lens{font-size:.84rem;color:var(--muted)}
.col .absent{color:var(--muted);font-style:italic}
table.score{font-size:.84rem}
table.score td.dim{font-weight:600;color:var(--ink)}
table.score td.cell-az{color:#dff3ff}
table.score tr.win td.cell-az{background:rgba(76,194,255,.08)}
table.score tr.concede td.cell-az{color:var(--muted)}
.verdict{border-left:3px solid var(--accent);background:#0f141b;border-radius:0 8px 8px 0;
padding:.5rem .9rem;margin-top:.4rem}.verdict p{margin:.3rem 0;font-size:.92rem}
.whatif{margin-top:1rem;border:1px dashed var(--line);border-radius:10px;
padding:.85rem 1rem;background:#0f141b;transition:border-color .15s}
.whatif.is-cf{border-color:#caa86a;border-style:solid}
.whatif-head{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;
justify-content:space-between;margin-bottom:.6rem}
.whatif-kind{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;
color:var(--muted);font-weight:600}
.whatif-toggle{display:inline-flex;border:1px solid var(--line);border-radius:999px;
overflow:hidden}
.wf-btn{appearance:none;background:transparent;border:0;color:var(--muted);
font:inherit;font-size:.8rem;padding:.28rem .8rem;cursor:pointer;transition:all .12s}
.wf-btn:hover{color:var(--ink)}
.wf-btn.is-on{background:var(--accent);color:#08121b;font-weight:600}
.whatif.is-cf .wf-btn.is-on{background:#caa86a;color:#1a1407}
.whatif-input,.whatif-branch{margin:.35rem 0;font-size:.88rem;color:var(--ink)}
.whatif-src{margin:.2rem 0;font-size:.82rem;color:var(--muted)}
.whatif-src p{margin:0;display:inline}
.whatif code{background:#1a2230;padding:.08rem .35rem;border-radius:5px;
font-family:JetBrains Mono,ui-monospace,monospace;font-size:.84em}
.whatif-verdict{margin:.5rem 0;border-left:3px solid var(--accent);background:var(--panel);
border-radius:0 8px 8px 0;padding:.4rem .85rem}
.whatif.is-cf .whatif-verdict{border-left-color:#caa86a}
.whatif-verdict p{margin:.2rem 0;font-size:.92rem}
.whatif-note{margin:.5rem 0 0;font-size:.78rem;color:var(--muted);font-style:italic}
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
    # One freshness date for the whole build: the newest dated L1 ingest folder.
    fresh_day = latest_source_day(vault_dir)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "assets").mkdir(parents=True, exist_ok=True)
    (out_dir / "assets" / "style.css").write_text(_CSS, encoding="utf-8")

    for page in [*model.briefs, *model.sources, *model.rules]:
        target = out_dir / page.out_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render_page(page, model.link_map, fresh_day), encoding="utf-8")

    # The demonstrator centerpiece: TOP5 cross-channel answers, rendered live from the
    # answer engine (every claim wikilink resolves through the same link map as the briefs).
    aset = build_answer_set(vault_dir, registry)
    (out_dir / "answers.html").write_text(
        _render_answers(aset, model.link_map, fresh_day), encoding="utf-8"
    )

    # The benchmark page: same world-topic, observed+sourced facts vs a forecast vs an
    # intelligence product (the USP proof by contrast). azimuth's columns render live from the
    # bundle; the foil columns come from the committed snapshot (absent file => empty foils).
    foils_path = registry_path.parent / "benchmark" / "foils.json"
    foils = json.loads(foils_path.read_text(encoding="utf-8")) if foils_path.exists() else {}
    bench = build_benchmark(vault_dir, registry, foils)
    (out_dir / "benchmark.html").write_text(
        _render_benchmark(bench, model.link_map, fresh_day), encoding="utf-8"
    )

    (out_dir / "index.html").write_text(_render_index(model, aset, fresh_day), encoding="utf-8")
    return model
