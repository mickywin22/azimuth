# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Initial project scaffold from coding factory template

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
