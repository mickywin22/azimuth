# Contributing to azimuth

Thanks for your interest. azimuth is a public demonstrator of the HemySphere
**L1 sources → L2 synthesis → L3 rules** vault doctrine, applied to open
global-intelligence data from the [WorldMonitor](https://worldmonitor.app) public API.
This guide explains what you can change, what you can't, and the gates every change
must pass.

## The one rule that surprises people: the vault is machine-generated

The repository has three doctrine layers, and **who may edit each one differs**:

| Layer | Path | Who owns it | PRs accepted? |
|-------|------|-------------|---------------|
| **L1 — Sources** | `vault/01 Sources/` | The daily ingest writes these, untouched | ❌ No — raw API pulls, never hand-edited |
| **L2 — Briefs** | `vault/02 Briefs/` | The weekly synthesis curator evolves these | ❌ No — derived artifacts, regenerated each cycle |
| **L3 — Rules** | `vault/00 Rules/`, `sources/registry.json` | Maintained deliberately | ✅ Yes — via PR + discussion |

So a PR that hand-edits a brief or a source note will be closed: those files are
**regenerated** from the pipeline and your edit would be overwritten on the next run.
If a brief reads wrong, the fix belongs in the **synthesis logic** (`synthesis/`) or the
**editorial rules** (`vault/00 Rules/editorial.md`), not in the brief text.

Good places to contribute:

- **`ingest/`** — the L1 pull (registry-driven, pure stdlib).
- **`synthesis/`** — the L2 curator logic, cross-theme join, synthesis lint.
- **`guardrail/`** — the L3 per-source license / attribution / editorial guardrail.
- **`scripts/`** — the CLIs (site/graph/index builders, query engine, liveness + scans).
- **`sources/registry.json`** — adding a new clean, free-tier, properly-licensed WorldMonitor
  subset (see the editorial + license bar below).
- **`docs/`** — clarity fixes, examples, corrections.

## Development setup

```bash
git clone https://github.com/mickywin22/azimuth.git
cd azimuth
uv pip install -e ".[dev]"   # or: pip install -e ".[dev]"
pre-commit install
```

The runtime is **pure standard-library Python 3.12** — there is no web server and no
third-party *runtime* dependency. The `[dev]` extras are tooling only (pytest, ruff, mypy).

## Before you open a PR — the gates

Every change must pass the same gates CI runs. Run them locally first:

```bash
# format + lint (pinned ruff — must match CI exactly)
ruff format guardrail/ ingest/ synthesis/ tests/ scripts/
ruff check  guardrail/ ingest/ synthesis/ tests/ scripts/

# types
mypy guardrail/ ingest/ synthesis/

# tests (unit + integration + coverage >= 80%)
pytest tests/ -v

# doctrine gates
python scripts/check_sources.py              # L3 per-source license/attribution/editorial
python scripts/check_synthesis.py            # L2 claim-sourcing, links, editorial deny-list
python scripts/build_brief_index.py --check  # brief index in sync
python scripts/build_graph.py --check        # knowledge graph in sync
python scripts/scan_secrets.py --worktree    # no leaked credentials
```

`pre-commit` runs the fast subset on every commit. **The ruff version is pinned**
(`pyproject.toml` and `.pre-commit-config.yaml` are kept in lock-step) — please do not
bump it in an unrelated PR, because a mismatch between the local formatter and CI's
formatter is exactly the drift this project pins against.

## The editorial line (non-negotiable)

azimuth reports observed, sourced **facts** and refuses three classes of content,
enforced by the guardrail and synthesis lint:

- **No investment advice** — odds and prices are reported as venue-quoted facts, never as
  forecasts or recommendations.
- **No safety/security predictions** that could put a reader at risk.
- **No partisan political opinion.**

Every L2 claim must trace to an L1 source note. Adding a source means adding its license
and attribution to `sources/registry.json` + `CREDITS.md`, or the guardrail fails the build.

## Commit & PR conventions

- Conventional-commit style subjects (`fix(ci): …`, `feat(graph): …`, `docs: …`).
- One logical change per PR; keep the diff reviewable.
- Describe **what** changed and **why**; link any related issue.
- Make sure the gates above are green before requesting review.

By contributing you agree your code is licensed **MIT** and any content under `vault/`
is licensed **CC BY 4.0**, matching the repository's [split license](README.md#license).
