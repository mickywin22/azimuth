# Good first issues

> **Generated file — do not edit by hand.** This catalog is rendered from `scripts/seed_good_first_issues.py` and CI fails if it drifts. To change an issue, edit the `ISSUES` list in that script and run `python scripts/seed_good_first_issues.py --write`.

These are the starter tasks a newcomer can pick up without knowing the ingest or synthesis internals. Each is small, self-contained, and real (open today). New to the repo? Read [CONTRIBUTING.md](../CONTRIBUTING.md) first — especially the 15-minute *add a data channel* walkthrough.

At the public flip these are seeded onto the tracker in one command (`python scripts/seed_good_first_issues.py --create`), each tagged `good first issue` so the [label filter](https://github.com/mickywin22/azimuth/issues?q=label%3A%22good+first+issue%22) returns them. Until then, this page IS the list — comment on the repo to claim one.

| # | Task | Difficulty | Labels |
|---|------|-----------|--------|
| 1 | [Add a new WorldMonitor data channel](#add-data-channel) | Beginner | `good first issue`, `enhancement`, `help wanted` |
| 2 | [Add a docs/glossary.md of the L1/L2/L3 doctrine terms](#docs-glossary) | Beginner | `good first issue`, `documentation`, `help wanted` |
| 3 | [Add a `timeline` query mode to scripts/query_graph.py](#query-graph-timeline) | Intermediate | `good first issue`, `enhancement` |
| 4 | [Add unit tests for ingest/http.py](#ingest-http-tests) | Intermediate | `good first issue`, `tests`, `help wanted` |
| 5 | [Add a synthesis-lint rule for unattributed superlatives](#synthesis-lint-superlatives) | Intermediate | `good first issue`, `enhancement` |

<a id="add-data-channel"></a>

## 1. Add a new WorldMonitor data channel

**Difficulty:** Beginner · **Estimate:** ~15 min

Surface one more clean, free-tier WorldMonitor subset by adding a single entry to `sources/registry.json` (+ its `CREDITS.md` attribution).

**Why it matters.** The whole point of the registry-driven design is that a new source is a one-file change, not a code change — this issue proves it and grows the graph.

**What to do**

1. Read the 15-minute walkthrough in CONTRIBUTING.md.
2. Pick a WorldMonitor subset that clears the editorial + license bar (free anonymous tier, compatible license, factual content class).
3. Append the entry to `sources/registry.json` and its attribution line to `CREDITS.md`.
4. Run `python scripts/check_sources.py` then `python scripts/run_ingest.py` to pull a sample L1 day.

**Files you'll touch**

- `sources/registry.json`
- `CREDITS.md`

**Done when**

- [ ] `python scripts/check_sources.py` passes with the new source surfaced.
- [ ] A sample `vault/01 Sources/<day>/<key>.md` note is produced and looks factual.
- [ ] The new theme (if any) renders in the brief index and site.

**Verify locally**

```bash
python scripts/check_sources.py
python scripts/build_brief_index.py --check
```

---

<a id="docs-glossary"></a>

## 2. Add a docs/glossary.md of the L1/L2/L3 doctrine terms

**Difficulty:** Beginner · **Estimate:** ~20 min

First-time visitors meet 'L1 source', 'L2 brief', 'L3 rule', 'editorial line', 'guardrail', 'source registry' with no single definition list. Add one.

**Why it matters.** A short glossary is the fastest onboarding win and the friendliest first PR — it lowers the bar for everyone who comes after.

**What to do**

1. Create `docs/glossary.md` with a short definition for each core term.
2. Pull the exact meanings from `docs/architecture.md` and `CONTRIBUTING.md` — do not invent new ones.
3. Link the glossary from `docs/README.md` so it is not orphaned (CI enforces this).

**Files you'll touch**

- `docs/glossary.md`
- `docs/README.md`

**Done when**

- [ ] `docs/glossary.md` defines at least the six core doctrine terms.
- [ ] It is linked from `docs/README.md` (the docs index).
- [ ] `python scripts/check_doc_orphans.py` and `check_doc_links.py` both pass.

**Verify locally**

```bash
python scripts/check_doc_links.py
python scripts/check_doc_orphans.py
```

---

<a id="query-graph-timeline"></a>

## 3. Add a `timeline` query mode to scripts/query_graph.py

**Difficulty:** Intermediate · **Estimate:** ~1 hr

The graph query CLI has stats / relations / neighbors / path / connect / provenance / evidence / bridges / hubs — but no way to list an entity's mentions ordered by the L1 source day. Add a `timeline <entity>` subcommand.

**Why it matters.** Time is the one axis the graph does not yet expose on the CLI; a timeline turns 'where is X mentioned' into 'when did X show up', a real analyst question.

**What to do**

1. Add a `timeline` subparser next to the existing ones in `scripts/query_graph.py`.
2. Walk the `named-in` edges for the entity, resolve each to its dated L1 note, sort by day.
3. Support the shared `--json` flag like the other subcommands.
4. Add a unit test mirroring the existing `test_query_graph.py` cases.

**Files you'll touch**

- `scripts/query_graph.py`
- `tests/unit/test_query_graph.py`
- `docs/cli.md`

**Done when**

- [ ] `python scripts/query_graph.py timeline "Greece"` prints the dated mentions in order.
- [ ] `--json` yields a machine-readable list.
- [ ] A new unit test covers the happy path and the unknown-entity path.

**Verify locally**

```bash
python scripts/query_graph.py timeline "Greece"
pytest tests/unit/test_query_graph.py -q
```

---

<a id="ingest-http-tests"></a>

## 4. Add unit tests for ingest/http.py

**Difficulty:** Intermediate · **Estimate:** ~1 hr

The anonymous-session fetcher `ingest/http.py` (stdlib urllib) has no dedicated unit test. Add one that exercises the session mint + fetch against a local stub.

**Why it matters.** It is the one network seam in the ingest path; a focused test protects it from silent regressions and lifts coverage on the riskiest module.

**What to do**

1. Create `tests/unit/test_http.py`.
2. Stand up a `http.server` stub (see `scripts/record_hero_gif.py` for the pattern) that returns a session cookie then a JSON payload.
3. Assert the fetcher mints a session, sends the cookie, and parses the body — with no real network call.

**Files you'll touch**

- `ingest/http.py`
- `tests/unit/test_http.py`

**Done when**

- [ ] New tests cover the session-mint and the authenticated fetch path.
- [ ] `pytest tests/unit/test_http.py -v` is green with no outbound network.
- [ ] Coverage on `ingest/http.py` rises.

**Verify locally**

```bash
pytest tests/unit/test_http.py -v
pytest tests/ --cov=ingest --cov-report=term-missing
```

---

<a id="synthesis-lint-superlatives"></a>

## 5. Add a synthesis-lint rule for unattributed superlatives

**Difficulty:** Intermediate · **Estimate:** ~1.5 hr

The editorial line forbids un-sourced claims. Add a `synthesis/lint.py` check that flags superlatives ('largest', 'worst', 'record') in an L2 brief unless the same sentence cites an L1 source.

**Why it matters.** Superlatives are exactly where a neutral fact quietly becomes an editorial claim; catching them in CI keeps the briefs honest at scale.

**What to do**

1. Add a new check function to `synthesis/lint.py` following the existing rule pattern.
2. Match a small superlative word list; pass only if the sentence carries an L1 link/citation.
3. Wire it into the lint run and add fixtures to `tests/unit/test_lint.py`.

**Files you'll touch**

- `synthesis/lint.py`
- `tests/unit/test_lint.py`

**Done when**

- [ ] A brief with an unattributed superlative fails `python scripts/check_synthesis.py`.
- [ ] The same superlative with an adjacent L1 citation passes.
- [ ] New unit tests cover both directions.

**Verify locally**

```bash
python scripts/check_synthesis.py
pytest tests/unit/test_lint.py -q
```

---

*Unsure which to pick? Start with the **glossary** or a **docs clarity** task — the fastest path to a merged PR and a feel for the codebase.*
