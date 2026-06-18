# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
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
