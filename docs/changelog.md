# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed
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
