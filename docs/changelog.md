# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- **The knowledge graph is now discoverable from the site front door (2026-07-03, KR-B):**
  `graph.html` rendered next to the site but was linked from nowhere — no nav entry, no index
  card — so a visitor could never find the flagship KG visualization. The site-wide nav (every
  page, `synthesis/site_build.py`) and the graph page's own nav (`scripts/build_graph.py`,
  marked `aria-current`) now carry a **Knowledge graph** entry, and the index gains a gold CTA
  card whose node/edge/bridge counts fill live from the published `graph.json` (progressive
  enhancement — the card reads fine if the fetch fails). Guarded by
  `test_graph_is_discoverable_from_the_site` (nav on root + subdir pages, card, live-count
  script) and a nav-parity token in the SOTA guard; proof
  `docs/proof/site-index-graph-cta.png` (Chromium: counts filled, click-through lands on
  `graph.html`).
- **Source-line evidence in the page — the graph now PROVES its bridges (2026-07-03, KR-B):**
  the viz could name *which* L1 notes back a bridge (`named-in` edges) but not show the text.
  The builder now embeds bounded per-theme quotes on every entity node (first whole-word
  match, original casing, ≤2 per theme), and `graph.html` gains an evidence panel: click/tap
  a shared entity — or walk to it with the keyboard and press Enter — and the page quotes the
  literal dated L1 source line from each channel that names it, deep-linked to the per-day
  source page. The in-browser counterpart of `query_graph.py evidence`. DOM-API +
  `textContent` only (hostile ingest text can never become markup); Escape or a visible ✕
  closes it. Proof: `docs/proof/graph-evidence.png` (live 2026-07-02 day — eia.gov fuel-price
  and EPA RADNET lines naming United States across two channels).
- **Evidence-ranked bridges land on `main` — CLI + in-page Trace (2026-07-03, KR-B):** the
  W26 evidence-ranking work (`connect` bridges ranked by min-leg/total `mentioned-in` weight,
  strongest named, path routed through it, per-bridge `[N+M src]` tags — plus the `evidence`
  query that quotes the raw L1 line) had been stranded on two unmerged W26 fleet branches;
  the site shipped alphabetical, unranked bridges. Ported both onto the current codebase and
  mirrored the ranking into the browser Trace, with unit + live-Chromium smoke guards so the
  rank can't silently regress.
- **Docs-index coverage gate — `tests/unit/test_docs_index_coverage.py` (2026-07-03, KR-C):**
  `docs/README.md` promises "Everything under `docs/` in one map", but that completeness was
  checked by eye — a sweep found `security/secret-scan-2026-06-30.md` (the C1 CLEAN evidence
  report) on disk yet absent from the index. Indexed it and added a unit gate that fails the
  build if any `docs/**/*.md` page is missing from the index — the third docs-drift class
  (after dead links and undocumented CLIs) turned into a build failure.
- **GitHub About box — versioned + applied (2026-07-03, KR-C):** the repo's About box (the
  first thing a visitor reads, before the README) was empty — no topics, no homepage, and a
  stale "(research stage)" description from the June scaffold. Now set: a pitch-matching
  description, homepage = the future Pages URL, and 9 topics (python · knowledge-graph ·
  knowledge-management · second-brain · digital-garden · open-data · osint · static-site ·
  github-pages). Because the About box is repo *settings*, not content, the exact
  `gh repo edit` command is versioned in `docs/deploy.md` as the single source of truth.
- **CLI-doc-coverage gate — `tests/unit/test_cli_doc_coverage.py` (2026-07-02, KR-C):**
  `docs/cli.md` promises "Every command under `scripts/` in one map", but that completeness
  was checked by eye — a sweep found `smoke_graph.py` (the KR-B knowledge-graph Playwright
  smoke) and `Build-Graphify-AST-Only.py` (a dev-only code-graph helper) silently
  undocumented. Documented both (`smoke_graph.py` next to `smoke_whatif.py`; the graphify
  helper under a new "Dev tooling — not part of the azimuth engine" section) and added a
  unit gate that fails the build if any runnable `scripts/*.py` is absent from `cli.md` —
  the same "turn a docs-drift class into a build failure" pattern as the dead-link gate.
- **Orphan-doc gate — `scripts/check_doc_orphans.py` (2026-07-01, KR-C):** the dead-link gate
  proves every link *points at something real*; its new companion proves the inverse for the
  documentation set — every `docs/**/*.md` page is *reachable* from a repo front door (README +
  the community files), so no authored doc can silently become an orphan that renders on GitHub
  only if you already know its URL. Reachability reuses the exact link parser of the dead-link
  gate (code spans stripped, external schemes / anchors skipped, `<spaces>` / `%20` handled) and
  walks transitively from every repo-root `*.md`; it flags an *island* (docs that link only each
  other) too. Wired into the `Synthesis Lint` CI job (`Documentation has no orphans`), the
  `doc-orphans` pre-commit hook, and ruff/mypy; documented in
  [doc-links.md](doc-links.md#the-companion-no-orphan-docs) and [cli.md](cli.md); backed by an
  8-case teeth-and-no-false-positives suite (`tests/unit/test_check_doc_orphans.py`). The live
  repo ships **0 orphans across all 20 docs**.
- **Getting-help policy — `SUPPORT.md` (2026-07-01, KR-C):** a public-grade repo needs the
  GitHub-recognised "Get help" file, and azimuth had every community doc *except* that one —
  README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CITATION, CREDITS, issue/PR templates were
  all present, but a first-time visitor with a "how do I…?" or "is this broken?" question had no
  single front door. Added `SUPPORT.md`: a router that sends questions to the right existing doc
  (FAQ, architecture, CLI, docs index) and, crucially, distinguishes a *broken build* from a
  *known-transient alarm* by pointing at the operations runbook (several red badges are red by
  design). It states the honest no-SLA expectation for a solo-maintained demonstrator and the
  scope boundary (upstream Worldmonitor questions belong with Worldmonitor). Surfaced from the
  root README (Contributing & security) and the [docs index](README.md), and wired as a
  `Questions & getting help` contact link in the issue-template chooser
  (`.github/ISSUE_TEMPLATE/config.yml`) so GitHub shows it before someone opens a blank issue.
  All new links resolve under the doc-link gate.
- **Dependabot for the CI toolchain — `.github/dependabot.yml` (2026-07-01, KR-C):** the repo
  brands itself on a per-source supply-chain guardrail for the *data* (`scripts/check_sources.py`),
  but the *build* toolchain had the analogous gap — the six third-party GitHub Actions across the
  five workflows (`actions/checkout`, `actions/setup-python`, `astral-sh/setup-uv`,
  `gitleaks/gitleaks-action`, `actions/github-script`, `actions/upload-pages-artifact` /
  `deploy-pages`) all floated on `@vN` tags with nothing keeping them current or patched. Added a
  weekly `github-actions` Dependabot updater that opens a single grouped PR for minor/patch bumps
  (a major version still opens on its own for a deliberate look), so the CI supply chain stays
  current the same way the data supply chain does — a public-grade hygiene signal a reviewer
  expects before a repo flips public.
- **Operations runbook — `docs/operations.md` (2026-07-01, KR-C):** the operate knowledge
  ("keep the engine operating") was accurate but scattered — the two-lane model in the README,
  the alarm mechanics inside each workflow's YAML, the manual health commands across README +
  cli.md. A public repo that promises a self-running engine needs one on-call page. Added a
  single runbook: the two lanes (L1 GitHub-cron vs L2 fleet-curator) and why only one survives
  a power-off; an at-a-glance table of all five scheduled jobs/gates; and a per-alarm response
  section (`ingest-alarm`, `synthesis-alarm`, the by-design-red `secret-scan`, and normal
  ci/pages breaks) with the exact reproduce-and-close commands. Wired into the [docs index](README.md)
  (Publish & operate) and the root README Operations section; the doc-link gate resolves all
  new links (134 -> 147 across 207 files).
- **First-time-visitor FAQ + engine-liveness badge — `docs/faq.md` (2026-07-01, KR-C):** the
  docs were complete but engine-facing (spec, plan, architecture, CLI) — a non-technical
  visitor landing on the repo had no single page answering the credibility questions ("is the
  data real?", "how current?", "can I trust the forecasts?", "why is it private?", "what
  licence?"). Added a concise FAQ that answers each and cross-links to the deep doc, wired into
  both the [docs index](README.md) (Concept & design) and the root README "Documentation"
  section. Also surfaced the **L2 Synthesis Freshness** heartbeat as a third engine badge at the
  top of the root README, so *both* liveness lanes (daily L1 ingest + weekly L2 synthesis) are
  now visible at a glance rather than only the L1 one — closing the "keep the engine operating"
  signal gap. The doc-link gate resolves all new links (110 → 134 across 206 files).
- **Citation metadata — `CITATION.cff` (2026-07-01, KR-C):** the repo had every other
  public-grade front-door file (README, split license, CONTRIBUTING, CODE_OF_CONDUCT,
  SECURITY, issue/PR templates, CREDITS) but no machine-readable citation, so GitHub showed
  no "Cite this repository" button. Added a CFF 1.2.0 file (software type, MIT, author +
  repo URL + keywords, version 0.1.0) so the project is properly citable, and surfaced it
  from both the root README ("Citing azimuth") and the docs index.
- **Interactive SOTA knowledge-graph viz — `site/graph.html` (2026-07-01, KR-B):** the
  read-only site's knowledge graph went from a static picker to a genuinely explorable,
  phone-usable artifact — and the changelog front door had not logged any of it. Four
  shipped, browser-render-proven features: (1) **typed edges made legible** — the relation
  (`has-brief`, `rests-on`, `mentioned-in`, …) shows on hover and each edge's thickness is
  weighted by how many L1 source notes back it, so provenance strength is visible at a glance;
  (2) **shareable deep links** — a Trace or Find writes to `location.hash`, so any graph state
  is a URL you can send; (3) **mobile touch** — pan/drag/tap plus pinch-zoom (`touchstart`
  handlers), so the graph works on a phone, not just a desktop with a mouse; (4) a banked
  **browser-render proof** test that guards all of the above so they can't silently regress.
- **L2 synthesis-freshness heartbeat — `.github/workflows/synthesis-freshness.yml` (2026-07-01,
  KR-C):** "keep the engine operating" was only half-true — the daily L1 ingest is autonomous
  GitHub infra with its own liveness alarm, but the *weekly L2 brief* is written by the fleet
  curator (an LLM job on Michael's box, off GitHub), so a power-off silently drifts the briefs
  stale with nothing to surface it. New weekly Monday workflow gives the L2 lane the same
  visible heartbeat: it checks each clean-theme brief against the latest L1 day and opens a
  single dedup'd `synthesis-alarm` issue only when a brief is genuinely **overdue** (the
  synthesis actually failed to run) — merely *stale* (awaiting the next scheduled pass) stays
  quiet. Backed by `scripts/check_synthesis_freshness.py` and documented in the root README
  "Operations — engine liveness" section.
- **CLI reference — `docs/cli.md` (2026-07-01, KR-C):** the whole engine is a set of 18
  pure-stdlib Python CLIs under `scripts/`, but no single page mapped them — a new contributor
  had to reverse-engineer the tool surface from the README fragments and each script's argparse.
  Added a complete reference: every command grouped by role (run the engine · build site &
  graph · demonstrator · gates), with usage, key flags, the layer/gate it serves, and a
  cross-link to its per-feature doc. Wired into `docs/README.md` (engine section) and the root
  README repo-layout table. Verified against the live `--help`/subcommand surface; the
  doc-link gate resolves all 17 new links.
- **Documentation link gate (2026-07-01, KR-C):** new `scripts/check_doc_links.py` — a
  pure-stdlib CI + pre-commit gate that walks all ~200 Markdown files and fails the build
  on any dead *relative* link (docs index, changelog, license split, generated brief index).
  It strips fenced/inline code first (so example links like `` `[x](/path.md)` `` are never
  flagged), unwraps `<spaces in path>`, decodes `%20`, resolves `/`-rooted targets against
  the repo root, and skips external URLs + pure anchors. Wired into the `Synthesis Lint` CI
  job and a local `doc-links` pre-commit hook; 15-case regression suite in
  `tests/unit/test_check_doc_links.py`; rule doc at `docs/doc-links.md`. Closes the manual-catch
  gap that let the dead `docs/README.md` link (fixed above) reach `main` in the first place.
  At introduction: 75 local links across 204 files, all resolve.
- **Documentation index (2026-07-01, KR-C):** new `docs/README.md` — a grouped one-map
  index of the whole `docs/` set (Concept/design · Engine · Publish/operate · Security ·
  Proof) linking every doc plus the root meta files, so the documentation is navigable at a
  glance on GitHub.
- **OKF Tier-1 conformance (late June, KR-A):** every L1 source note now carries `type` +
  `resource` front-matter, and `vault/index.md` acts as the bundle root — bringing the
  published vault into Open Knowledge Foundation Tier-1 shape. A one-shot backfill wrote the
  two fields into the 140 pre-existing L1 notes; the ingest writes them going forward. Full
  rationale + the knowledge-graph direction: `docs/strategy/okf-and-knowledge-graph.md`.
- **Public-flip readiness gate (late June, KR-A):** a one-command go/no-go aggregator over
  the privacy/secret invariants, hardened to actually finish and to cover *dangling* git
  blobs (unreferenced objects a naive scan misses). The C1c owner-private-history
  accept-vs-scrub call is written up decision-ready in
  `docs/security/c1c-history-decision.md`; the full checklist lives in
  `docs/security/public-flip-readiness.md`. The C1 secret gate is re-proven on the exact
  published commit and reframed around the CI invariant rather than a one-off scan.
- **W26 weekly-synthesis automation (2026-06-18, KR-B B3):** the L2 weekly cycle is now wired
  end-to-end — no manual curator run. New `scripts/check_synthesis_freshness.py` is the
  deterministic freshness gate: per editorially-clean (non-held) theme it compares the latest
  L1 ingest day against the brief's `updated` date and reports STALE / fresh (`--check` exits
  non-zero if any clean brief lags the latest L1, `--json` for machine use). The `azimuth-curator`
  role now opens each weekly run by finding stale briefs (clean no-op when none) and closes its
  done-gate on `freshness --check`. The HemySphere fleet seeds one azimuth-curator work-item per
  ISO week (`scripts/scheduled/fleet/AzimuthCadence.ps1` -> `Seed-WorkItems.ps1`); the universal
  Reviewer pushes to azimuth `main`. Combined with the daily GH-Actions L1 ingest, the full
  L1-daily / L2-weekly automation is live. New `tests/unit/test_synthesis_freshness.py` (6 cases).
- **W26 multi-theme expansion (2026-06-18):** azimuth now runs more than the single Energy
  brief. The registry gained a data-driven `themes` map + a per-source `theme`; the daily L1
  ingest already pulls every surfaced clean channel, now including `earthquakes` and
  `prediction-markets`. New L2 brief **Geophysical Weekly** (USGS earthquakes, lint-green off
  the live 2026-06-18 ingest). New `scripts/build_brief_index.py` auto-generates the
  `vault/02 Briefs/README.md` index (all briefs + last-updated + held themes), wired into CI +
  pre-commit with a `--check` sync guard. `azimuth-curator` role generalised to evolve one
  brief per clean theme. New `tests/unit/test_registry_themes.py` integrity tests.
- Initial project scaffold from coding factory template

### Fixed
- **Broken link + gate transparency in the docs index (2026-07-01, KR-C):** `docs/README.md`
  linked `security/c1c-history-decision.md`, which is staged on the public-flip branch and is
  not on `main` — a dead link on the public-grade front door. Replaced it with a non-linking
  note that the C1c decision doc + the `check_flip_readiness.py` aggregator land with the flip.
  Added a **Continuous integration & gates** section documenting all four workflows and, in
  particular, why `secret-scan.yml` is intentionally red before the flip (the C1c owner-private
  history go-gate) — so the always-on security gate is visibly accounted for, not mistaken for
  a dropped job.
- **CI red on `main` — site-build test (2026-07-01, KR-C engine):** the KR-B interactive
  knowledge-graph work made `synthesis/site_build.py` render Markdown, so
  `tests/unit/test_site_build.py` (and the coverage step) began raising
  `ModuleNotFoundError: No module named 'markdown'` — the renderer lives in the `site`
  optional-dependency extra, but the CI **Test** job installed only `.[dev]`. Result: three
  consecutive pushes reddened the CI badge on the public-grade README front door while the
  daily ingest and every other job stayed green. Fixed by installing `.[dev,site]` in the
  Test job (the runtime + `dev` stack stay pure-stdlib; only the job that exercises the site
  build pulls the renderer). Locally: 239 unit tests green.
- **README license classification (2026-07-01, KR-C):** the split-license section listed
  `synthesis/` as a *future* MIT-code path, but the L2 synthesis engine (`answers.py`,
  `cross_theme.py`, `lint.py`, `benchmark.py`, `site_build.py`) has shipped and is already
  covered by the repository-layout table above it. Reclassified `synthesis/` as a current
  MIT-code directory so the license front door reads accurately for a public visitor.

### Changed
- **Editorial line rewritten to fact-vs-propaganda (2026-06-24, Michael):** azimuth now
  surfaces ANY free-to-use channel that monitors **facts** (observed events, measurements,
  positions, records) on ANY topic, and denies only **non-factual** content (political
  propaganda, opinion/advocacy, editorial/communication, political-or-safety position-taking,
  investment advice). **Sensitivity is never a deny reason — only LICENSE is.** Implemented
  across the L3 stack: `sources/registry.json` `content_class_policy` (10 observed-fact
  ALLOWED classes incl. `conflict-event-record` / `vessel-position` / `flight-track` /
  `cyber-event` / `civil-unrest-event` / `news-factual`; 6 non-factual DENIED classes;
  new `benchmark_foil_classes` for forecast/assessment/scenario). The three sensitive feeds
  (`conflict-events-acled`, `vessel-tracking-ais`, `military-flights-adsb`) reclassified from
  editorial-excluded to factual channels **held on LICENSE grounds only** (license still
  unknown). `guardrail/source_guardrail.py` gains a `Violation.category` tag (`license` vs
  `editorial`) so a sensitive-but-factual hold is never mistaken for an editorial exclusion.
  `synthesis/lint.py` deny-list relabelled + broadened to flag advocacy/opinion/position
  framing (NOT topics) — a factual report on a sensitive topic passes. `vault/00 Rules/editorial.md`,
  `docs/spec.md`, `docs/source-guardrail.md`, and the published `editorial.html` rewritten to
  state the "facts in, opinions out" line plainly. NEWS allowed as a factual channel
  (fact-reporting sources kept, op-ed/advocacy stripped). 101 tests green, guardrail PASS,
  6 surfaced channels stay green.
- **prediction-markets surfaced as L1** (passes the source-guardrail: API-ToS licence,
  prediction-market class). Its **L2 brief is held** — the live feed currently surfaces a
  single politically-charged market that can't be synthesised neutrally; `hold_reason` logged
  in `sources/registry.json`. The three editorial-excluded channels (conflict / maritime /
  air-traffic) stay `surfaced:false`, each now carrying a logged `surfaced_reason`.

### Removed
- **Phase-1 template strip (2026-06-11):** deleted the unused `project-template`
  FastAPI backend (`src/backend/main.py`, `config.py`) and Next.js frontend
  (`src/frontend/`), plus the `docs/coolify-deploy.md`, `docs/multi-tenancy.md`,
  and `docs/openapi-pattern.md` template guides. azimuth has no server runtime —
  it is a stdlib data pipeline (L1 ingest → L2 synthesis → static publish).
- Trimmed all third-party **runtime** dependencies (fastapi, uvicorn, pydantic,
  pydantic-settings, httpx) — runtime is now pure stdlib (`urllib` for ingest,
  `json`/`dataclasses` for the guardrail).

### Changed
- **Moved the source guardrail out of the deleted backend:**
  `src/backend/guardrail/` → top-level `guardrail/` (the L1 ingest imports it, so
  it was moved, not deleted). Updated every importer (`ingest/pull.py`,
  `scripts/check_sources.py`, the guardrail `__init__`, both unit-test modules)
  from `src.backend.guardrail` to `guardrail`, and repointed the CI
  (`.github/workflows/ci.yml`), pre-commit (`.pre-commit-config.yaml`), and
  pyproject (`known-first-party`, `coverage.source`) paths. Tests green (41
  passed), ruff + format clean, coverage 82%.
