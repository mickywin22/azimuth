# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
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

### Added
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
