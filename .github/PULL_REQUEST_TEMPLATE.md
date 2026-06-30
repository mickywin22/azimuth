<!-- Thanks for contributing to azimuth. Please read CONTRIBUTING.md first. -->

## What & why

<!-- What does this change do, and why? Link any related issue (e.g. Closes #123). -->

## Layer touched

<!-- Tick all that apply. NOTE: PRs that hand-edit vault/01 Sources or vault/02 Briefs
     will be closed — those are machine-generated (see CONTRIBUTING.md). -->

- [ ] Code (`ingest/`, `guardrail/`, `synthesis/`, `scripts/`)
- [ ] L3 rules (`vault/00 Rules/`, `sources/registry.json`)
- [ ] Docs only

## Gates (all must be green)

- [ ] `ruff format` + `ruff check` clean (pinned version, unchanged)
- [ ] `mypy` clean
- [ ] `pytest tests/ -v` green, coverage ≥ 80%
- [ ] `python scripts/check_sources.py` (source guardrail) passes
- [ ] `python scripts/check_synthesis.py` (synthesis lint) passes
- [ ] `--check` builders in sync (`build_brief_index.py`, `build_graph.py`) if relevant
- [ ] No new secrets / owner-private context (`scan_secrets.py`, `scan_private_leakage.py`)

## Notes for the reviewer

<!-- Anything non-obvious: tradeoffs, follow-ups, things you deliberately left out. -->
