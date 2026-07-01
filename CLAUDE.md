# azimuth

## Overview

Public demonstrator of the HemySphere **L1 sources → L2 synthesis → L3 rules** vault doctrine,
fed by [Worldmonitor](https://worldmonitor.app) open-intelligence data and published as a static
site. Architecture: [docs/architecture.md](docs/architecture.md). Spec: [docs/spec.md](docs/spec.md).

## Tech Stack

- **Runtime:** pure Python standard library — **no web server, no database, no frontend
  framework**. The project-template's FastAPI backend / Next.js frontend were stripped in Phase 1.
- **Dev tooling** (`.[dev]`): ruff · mypy · pytest (+ cov, benchmark, asyncio) · pre-commit.
- **Site extra** (`.[site]`): a Markdown renderer, used *only* by the static-site build.
- **CI / automation:** GitHub Actions (5 workflows). **Publish:** GitHub Pages
  (<https://mickywin22.github.io/azimuth/>).

## Project Structure

```
ingest/         # L1 pull — registry-driven WorldMonitor fetch -> dated source notes (stdlib)
guardrail/      # L3 per-source license / attribution / editorial guardrail (mypy-strict)
synthesis/      # L2 curator logic, synthesis lint, cross-theme join, site build
scripts/        # CLIs — ingest, site + graph + index builders, query engine, liveness + scans
sources/        # registry.json — single source of truth: every subset + its license/theme
vault/          # the published vault — 00 Rules (L3) · 01 Sources (L1) · 02 Briefs (L2)
site/           # built read-only static site + graph.json / graph.html knowledge graph
tests/          # unit/ + integration/ (pytest); >=80% coverage gate
docs/           # spec, plan, architecture, cli, deploy, security, per-feature docs
.github/workflows/  # ci · ingest (daily) · synthesis-freshness (weekly) · pages · secret-scan
```

## Development Commands

```bash
# Install dev tooling (runtime itself is pure-stdlib — no third-party deps)
uv pip install -e ".[dev]"

# Run the L1 ingest (pulls WorldMonitor subsets -> dated L1 notes)
python scripts/run_ingest.py

# Quality (the CI gate, locally)
ruff check . --fix
ruff format .
mypy guardrail/ ingest/ synthesis/
pytest -q                        # full suite
pytest --cov=guardrail --cov=ingest --cov=synthesis   # with coverage

# Engine liveness by hand
python scripts/check_ingest_liveness.py            # L1: alive / STALE
python scripts/check_synthesis_freshness.py        # L2: per-theme fresh / stale / OVERDUE

# Gates (also run in CI + pre-commit)
python scripts/check_doc_links.py                  # no dead relative Markdown link
python scripts/check_sources.py                    # source-guardrail lint
pre-commit run --all-files
```

Full CLI reference: [docs/cli.md](docs/cli.md).

## Quality Rules

1. **Tests first, then code** — every CLI + guardrail path is covered; the suite is the contract.
2. **Type hints everywhere** — mypy strict on `guardrail/` `ingest/` `synthesis/`.
3. **Ruff clean** — zero warnings; `ruff` is pinned `>=0.15,<0.16` in lock-step with the
   pre-commit rev so local + CI format identically (an unpinned ruff caused recurring CI-format drift).
4. **Coverage ≥ 80%** — CI fails below threshold.
5. **No dead docs** — `check_doc_links.py` fails the build on any broken relative link; a public
   repo's dead link is a credibility bug.
6. **Runtime stays pure-stdlib** — nothing may add a third-party *runtime* dependency; only `dev`
   and `site` extras carry third-party packages, and neither is on the ingest/guardrail path.

## Git Workflow

- `main` — the public-grade branch; every workflow guards it.
- `fleet/<name>` — autonomous fleet work branches. **A Worker commits but does not push; the
  reviewer pushes the reviewed commit to `main`** (non-vault repo — reviewer-push policy).
- Commit messages: imperative mood, tag the KR (e.g. `docs(cli): … (KR-C)`).

## Public-flip status

The repo is private at the research stage and flips public at the F3 publish milestone. The
`secret-scan.yml` workflow is **intentionally red** until the owner-private-history call (C1c) is
made — see [docs/security/public-flip-readiness.md](docs/security/public-flip-readiness.md).

## Vault Link

Project note: `05 Projects/azimuth.md` in the HemySphere vault (Coding-Factory track).
Research + feasibility: `07 Resources/AI Agents & Agentic Systems/Worldmonitor App – Research.md`.
