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

## 15-minute walkthrough: add a new data channel

The most impactful single-file contribution is adding a new WorldMonitor source subset that
clears the editorial + license bar. Here is the exact sequence from zero to a green CI run.

**Prerequisites:** Python 3.12 and `uv` (or pip). WorldMonitor needs **no API key** — the
ingest mints an anonymous, rate-limited session automatically, and every v0 subset is free-tier.

**Step 1 — check the source clears the bar (~2 min)**

Before touching any file, verify three things:

- The endpoint is reachable on the **free anonymous tier** of the
  [WorldMonitor API](https://worldmonitor.app).
- The data carries a **compatible license** (CC BY, CC0, or equivalent) with clear
  attribution requirements.
- The content fits the editorial line: factual, sourced, no investment advice, no
  safety/security predictions, no partisan opinion (run
  `python scripts/check_sources.py` after adding the entry to see what the guardrail
  catches).

**Step 2 — add the source entry (~3 min)**

Open `sources/registry.json` and append a new object inside `"sources"`. Match the shape of
the existing entries — the source-guardrail **requires** `key`, `endpoint`, and
`content_class`, and the `license` must be one of the allowlisted identifiers (`CC-BY-4.0`,
`CC0-1.0`, `ODbL-1.0`, `public-domain`, `US-Gov-public-domain`, `API-ToS-derived`):

```json
{
  "key": "your-source-slug",
  "endpoint": "/api/.../get-your-subset",
  "upstream_source": "Upstream provider name",
  "license": "CC-BY-4.0",
  "attribution": "Data: Upstream provider via WorldMonitor (api.worldmonitor.app)",
  "content_class": "climate-observation",
  "theme": "your-theme-slug",
  "risk_flags": [],
  "synthesis_cautions": [],
  "surfaced": true
}
```

`content_class` must be one of the **allowed** factual classes in the registry's
`content_class_policy` (e.g. `market-data`, `natural-hazard`, `climate-observation`) — a
denied class (opinion, propaganda, investment advice, safety/political position) fails the
build. If the `theme` slug is new, also add it to the top-level `"themes"` map with a
`title` and `brief` filename so the brief index and site can render it.

Add the matching attribution line to `CREDITS.md`:

```
**Your Theme Name** — data via WorldMonitor public API (api.worldmonitor.app), CC-BY-4.0.
```

**Step 3 — run the guardrail locally (~1 min)**

```bash
python scripts/check_sources.py
```

Fix any failures (missing license, missing attribution, deny-list hit) before continuing.

**Step 4 — pull a sample L1 day (~3 min)**

```bash
python scripts/run_ingest.py
```

This writes a dated directory under `vault/01 Sources/YYYY-MM-DD/` with one `.md` note per
fetched item. Open a note and verify the content looks reasonable (factual, sourced, no
deny-list phrases).

**Step 5 — verify the synthesis gates still pass (~3 min)**

```bash
python scripts/check_synthesis.py        # claim-sourcing + editorial deny-list
python scripts/build_brief_index.py --check
python scripts/build_graph.py --check
python scripts/build_autonomy.py --check
```

The synthesis curator will pick up the new channel on the next weekly cycle — you do not
need to write a brief yourself.

**Step 6 — open the PR**

Commit the registry entry + CREDITS line + the new L1 day directory. PR description should
include the source URL, license, and a sample L1 note excerpt to show the data is clean.
The CI gates run automatically.

---

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

## Good first issues

**The concrete, ready-to-pick list is [`.github/GOOD_FIRST_ISSUES.md`](.github/GOOD_FIRST_ISSUES.md)** —
five real, open, self-contained tasks with the exact files to touch and the local commands
to verify each. That catalog is *generated* from `scripts/seed_good_first_issues.py` (CI
fails if it drifts), and at the public flip the same script seeds them onto the tracker in
one command (`python scripts/seed_good_first_issues.py --create`), each tagged
**`good first issue`** so the
[label filter](https://github.com/mickywin22/azimuth/issues?q=label%3A%22good+first+issue%22)
returns them.

The broad shape of what makes a good first contribution:

| Type | What it involves | Skill level |
|------|-----------------|-------------|
| **Add a new data channel** | Follow the 15-min walkthrough above — registry entry + CREDITS + sample L1 pull | Beginner |
| **Docs clarity fix** | Correct a confusing sentence, add a missing example, fix a broken link in `docs/` | Beginner |
| **Script output polish** | Improve the human-readable output of a CLI in `scripts/` (e.g., better progress messages, column alignment) | Beginner |
| **Test coverage gap** | Add a unit test for an untested path in `guardrail/`, `ingest/`, or `synthesis/` (run `pytest --cov` to find gaps) | Intermediate |
| **New query mode** | Add a subcommand to `scripts/query_graph.py` (e.g., `timeline`, `cluster`) following the existing pattern | Intermediate |
| **Synthesis lint rule** | Add a new editorial lint check to `synthesis/lint.py` (e.g., detecting unattributed superlatives) | Intermediate |

If you're unsure which issue to pick, start with a **docs clarity fix** — it's the fastest
path to a merged PR and gives you a feel for the codebase.

## Commit & PR conventions

- Conventional-commit style subjects (`fix(ci): …`, `feat(graph): …`, `docs: …`).
- One logical change per PR; keep the diff reviewable.
- Describe **what** changed and **why**; link any related issue.
- Make sure the gates above are green before requesting review.

By contributing you agree your code is licensed **MIT** and any content under `vault/`
is licensed **CC BY 4.0**, matching the repository's [split license](README.md#license).
