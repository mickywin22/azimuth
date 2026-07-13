# azimuth — CLI reference

Every command under [`scripts/`](../scripts/) in one map. azimuth has **no web-server
runtime** — the whole engine is a set of pure-stdlib Python CLIs you run by hand or that CI
runs for you. This page is the reference: what each command does, how to run it, and which
layer or gate it serves. For the design behind them, follow the per-feature docs linked in
[docs/README.md](README.md).

All commands run from the repo root. Install the dev tooling once with
`uv pip install -e ".[dev]"` (the runtime itself needs no third-party deps).

Legend — **Layer**: L1 = source ingest · L2 = synthesis · L3 = rules/guardrail ·
Site = published static site · Gate = CI / pre-commit / public-flip check.

---

## Run the engine

### `run_ingest.py` — L1 daily pull
Pulls the registry's WorldMonitor subsets into dated L1 source notes under
`vault/01 Sources/`. This is the engine every brief rests on.

```bash
python scripts/run_ingest.py                 # pull today's L1 notes
python scripts/run_ingest.py --dry-run       # show what would be pulled, write nothing
python scripts/run_ingest.py --base-url URL  # point at an alternate WorldMonitor endpoint
python scripts/run_ingest.py --out-dir DIR   # write L1 notes under DIR (default: vault/01 Sources)
```
**Layer:** L1 · runs daily in [`ingest.yml`](../.github/workflows/ingest.yml). See
[l1-ingest.md](l1-ingest.md).

### `build_brief_index.py` — L2 brief index
Regenerates `vault/02 Briefs/README.md` from each brief's frontmatter. Kept in sync by CI.

```bash
python scripts/build_brief_index.py
python scripts/build_brief_index.py --check   # exit 1 if the committed index is stale (CI guard)
```
**Layer:** L2 · See [synthesis.md](synthesis.md).

### `build_cross_theme.py` — *World Watch Weekly* meta-brief
Builds the cross-theme meta-brief that joins the per-theme L2 briefs from the live L1 data.

```bash
python scripts/build_cross_theme.py
python scripts/build_cross_theme.py --check   # exit 1 if the committed meta-brief is stale (CI guard)
python scripts/build_cross_theme.py --json    # emit the bridge scan as JSON
```
**Layer:** L2.

---

## Build the site & graph

### `build_site.py` — the public static site
Builds the read-only site (L2 briefs → L1 sources → L3 editorial line) into `_site/`
(or `--out`). Optionally serves it locally.

```bash
python scripts/build_site.py                 # build into the default output dir
python scripts/build_site.py --out DIR       # build into DIR
python scripts/build_site.py --serve --port 8000   # build + serve locally
```
**Layer:** Site · published by [`pages.yml`](../.github/workflows/pages.yml). See
[site.md](site.md).

### `build_graph.py` — the knowledge graph
Builds the cross-channel knowledge graph (`site/graph.json` + the visual
`site/graph.html`). Every edge is typed (`has-brief`, `rests-on`, `mentioned-in`,
`named-in`, `reported-in`, `located-in`) and reaches down to the L1 sources, not just the
briefs.

```bash
python scripts/build_graph.py                # write site/graph.json + graph.html
python scripts/build_graph.py --out DIR      # write into DIR
python scripts/build_graph.py --check        # exit 1 if committed graph is stale vs the live vault (CI guard)
```
**Layer:** Site · CI asserts the committed graph is in sync. See
[strategy/okf-and-knowledge-graph.md](strategy/okf-and-knowledge-graph.md).

### `build_rdf.py` — lift the vault into RDF (schema.ttl + data.ttl)
Lifts the `vault/` OKF bundle into a linked-data graph via the **Vault-LD OKF compatibility
profile** (SPEC Appendix B): reads the committed composed context (`vault/context.jsonld` +
`vault/ontology/azimuth.context.jsonld`), then emits `schema.ttl` (the ontology) + `data.ttl`
(every note as a typed subject) beside the static site, and copies the context so the graph is
self-describing. Held themes are excluded, exactly as the site build excludes them. `rdflib`
is a **CI-only** dependency (the `ld` extra) — the runtime stays pure-stdlib.

```bash
uv pip install -e ".[ld]"                    # one-time: the CI-only rdflib extra
python scripts/build_rdf.py                   # write site/schema.ttl + site/data.ttl (+ context)
python scripts/build_rdf.py --out DIR         # write into DIR (the Pages build uses _site)
python scripts/build_rdf.py --check           # build + validate in-memory, write nothing (CI gate)
```
**Layer:** Site (linked-data export) · the `linked-data` CI job runs `--check`. See
[linked-data.md](linked-data.md).
### `build_autonomy.py` — the autonomy counters
Builds the "proof it runs itself" counters (`site/autonomy.json` + the visual
`site/autonomy.html`): days operating, daily L1 ingests committed, L1 source notes, L2
briefs, data channels, and an explicitly-labelled LLM-spend estimate. Every counter is
derived from committed vault data (never the wall clock), so it is byte-reproducible and
CI-guarded — and it re-derives each daily ingest, exactly like the graph and brief index.

```bash
python scripts/build_autonomy.py             # write site/autonomy.json + autonomy.html
python scripts/build_autonomy.py --check     # exit 1 if the committed counters are stale (CI guard)
```
**Layer:** Site · re-derived daily in [`ingest.yml`](../.github/workflows/ingest.yml); CI
asserts the committed counters are in sync.

### `record_hero_gif.py` — generate the README hero animation
Records an animated walkthrough of the azimuth site (home → knowledge graph → trace →
autonomy counters) and writes `docs/assets/hero.gif`. Requires the `[demo]` optional
dependencies (Playwright + Pillow) which are NOT installed by default.

```bash
uv pip install -e ".[demo]" && playwright install chromium
python scripts/record_hero_gif.py            # uses already-built site/
python scripts/record_hero_gif.py --serve    # build site first, then record
python scripts/record_hero_gif.py --width 1280 --height 720 --fps 2
```

**Layer:** Docs-only · not part of CI · run manually to refresh `docs/assets/hero.gif`
before a public flip or a major UI change.

### `query_graph.py` — query the graph from the CLI
Answers cross-channel questions over the same `site/graph.json` the visual graph uses.
Subcommands:

| Subcommand | Answers |
|-----------|---------|
| `stats` | headline node / edge counts |
| `relations` | edge counts by relation type |
| `neighbors <term>` | direct neighbours of a node |
| `path <a> <b>` | shortest path between two nodes |
| `connect <a> <b>` | how two channels are connected (flagship) |
| `provenance <term>` | the exact dated L1 notes that name an entity |
| `bridges` | all cross-channel bridge entities |
| `hubs [--top N]` | most-connected nodes |

```bash
python scripts/query_graph.py connect energy geophysical
python scripts/query_graph.py provenance "Greece"
python scripts/query_graph.py path "Greece" "Energy Supply"
python scripts/query_graph.py bridges
python scripts/query_graph.py hubs --top 8 --json
```
Global flags: `--graph PATH` (point at an alternate `graph.json`), `--json` (machine-readable
output). **Layer:** Site.

---

## The demonstrator (show-your-work proof)

### `build_answers.py` — TOP5 multi-channel answers
Generates the demonstrator — the TOP5 cross-channel answers — from live data.

```bash
python scripts/build_answers.py
python scripts/build_answers.py --check   # exit 1 if the committed answer set is stale (CI guard)
python scripts/build_answers.py --json    # emit the answer set as JSON
```
**Layer:** Site / proof · See [proof/README.md](proof/README.md).

### `build_benchmark.py` — facts vs forecast vs intelligence
Builds the benchmark comparing azimuth's output against forecast and intelligence products.

```bash
python scripts/build_benchmark.py
python scripts/build_benchmark.py --check   # exit 1 if the committed benchmark is stale (CI guard)
python scripts/build_benchmark.py --json    # emit the benchmark as JSON
```
**Layer:** proof.

### `pull_benchmark_foils.py` — benchmark foil corpus
Captures the compared forecast / intelligence products (the "foils") the benchmark grades
against.

```bash
python scripts/pull_benchmark_foils.py
python scripts/pull_benchmark_foils.py --from FEED.json   # offline: select from a saved feed JSON
python scripts/pull_benchmark_foils.py --out PATH         # output path (default: sources/benchmark/foils.json)
```
**Layer:** proof.

### `smoke_whatif.py` — live what-if smoke
A live Playwright smoke of the demonstrator's what-if panel — the KR-B acceptance gate.
Needs the Playwright browser deps installed.

```bash
python scripts/smoke_whatif.py
```
**Layer:** Gate (acceptance).

### `smoke_graph.py` — live knowledge-graph smoke
A live Playwright smoke of the knowledge-graph view (the KR-B state-of-the-art
visualization gate). Serves the built `site/` locally, opens `graph.html` in a real
Chromium, and proves what the token-presence unit tests can't reach: the canvas renders a
non-blank graph, the queryable Trace layer answers over it, and on a phone viewport a
one-finger touch-drag actually pans. Screenshots are banked to `_smoke/` (the desktop
overview + Trace shots are copied into `docs/proof/`). Needs the Playwright browser deps
installed.

```bash
python scripts/smoke_graph.py
```
**Layer:** Gate (acceptance).

### `smoke_ui.py` — live "incredible UI" smoke
A live Playwright smoke of the KR1 landing + story-mode surface. Builds the site fresh,
serves it locally, and opens it in a real Chromium to prove what the token-presence unit
tests can't reach: the landing **hero graph centerpiece** canvas draws a non-blank graph
with its live node/bridge badge filled, the **build-time sparklines** (vault pulse + one per
brief card) render as inline SVG, the **mobile hamburger nav** hides the menu then reveals it
on tap, and `graph.html` **story mode** drives a real cross-channel Trace on each of its three
steps (Finish + Escape both exit). Screenshots are banked to `_smoke/` (the landing,
hero-graph, mobile-nav + story shots are copied into `docs/proof/`). Needs the Playwright
browser deps installed (`pip install -e ".[smoke]" && playwright install chromium`).

```bash
python scripts/smoke_ui.py            # builds the site first, then smokes it
python scripts/smoke_ui.py --no-build # smoke the already-built ./site
```
**Layer:** Gate (acceptance).

---

## Gates — CI, pre-commit & public-flip

These are the checks CI runs on every push. You can run any of them by hand before you
commit.

### `check_doc_links.py` — dead-link gate
Fails if any relative Markdown link in the repo doesn't resolve. No dead link reaches the
public front door.

```bash
python scripts/check_doc_links.py
```
**Layer:** Gate (`ci.yml`) · See [doc-links.md](doc-links.md).

### `check_doc_orphans.py` — orphan-doc gate
Fails if any `docs/**/*.md` is unreachable from a repo front door (README + community
files), so no authored doc is orphaned and undiscoverable on the public repo. The
companion to the dead-link gate: links resolve *and* every doc is linked-to.

```bash
python scripts/check_doc_orphans.py
```
**Layer:** Gate (`ci.yml`) · See [doc-links.md](doc-links.md#the-companion-no-orphan-docs).

### `check_sources.py` — L3 source guardrail
Enforces the per-source license / attribution / editorial guardrail from
`sources/registry.json`.

```bash
python scripts/check_sources.py
```
**Layer:** Gate (`ci.yml`, L3) · See [source-guardrail.md](source-guardrail.md).

### `check_synthesis.py` — synthesis lint
The synthesis lint (spec.md F2) — CI + pre-commit entry point for the L2 curator rules.

```bash
python scripts/check_synthesis.py
python scripts/check_synthesis.py --brief "vault/02 Briefs/Energy Supply Weekly.md"   # lint one brief (repeatable)
python scripts/check_synthesis.py --diff-base origin/main        # enforce the diff guard vs a ref
```
Flags: `--brief PATH` (lint only that brief file, repeatable), `--diff-base REF` (git ref the
changed-file diff guard runs against), `--briefs-root` / `--sources-root` (override the default
`vault/` paths). **Layer:** Gate (`ci.yml`, L2) · See [synthesis.md](synthesis.md).

### `check_synthesis_freshness.py` — weekly-cadence gate
Reports which L2 briefs are stale versus the latest L1 ingest.

```bash
python scripts/check_synthesis_freshness.py          # human-readable
python scripts/check_synthesis_freshness.py --json    # machine-readable
python scripts/check_synthesis_freshness.py --check   # exit 1 if any clean brief lags the latest L1
python scripts/check_synthesis_freshness.py --overdue # exit 1 only if a brief lags > one weekly cadence
```
The `--overdue` form is the one to wire into CI/alarms: it tolerates the designed
daily-L1 / weekly-L2 gap and fails only when the weekly synthesis genuinely missed its
cadence. **Layer:** Gate (cadence).

### `check_ingest_liveness.py` — ingest heartbeat
Reports whether the daily L1 ingest is still alive (latest L1 day within tolerance).

```bash
python scripts/check_ingest_liveness.py              # alive / STALE + latest L1 day + age
python scripts/check_ingest_liveness.py --check      # exit 1 if stale (the in-workflow gate)
```
Flags: `--json` (machine-readable), `--today YYYY-MM-DD` (override "now" for testing),
`--max-age-days N` (staleness tolerance, default 2), `--sources PATH` (point at an alternate
`vault/01 Sources/`). **Layer:** Gate (`ingest.yml`).

### `scan_secrets.py` — secret scan (public-flip HARD gate, C1)
Pure-stdlib secret scanner over the working tree or full git history — the public-flip
hard gate.

```bash
python scripts/scan_secrets.py --worktree           # scan the working tree
python scripts/scan_secrets.py --history            # scan full git history
python scripts/scan_secrets.py --history --json                 # findings as JSON
python scripts/scan_secrets.py --history --report > verdict.md  # markdown verdict block (to stdout)
```
Flags: `--worktree` / `--history` (scan scope), `--json` (findings as JSON), `--report`
(emit a markdown verdict block on stdout — redirect to save it). **Layer:** Gate
(`secret-scan.yml`, C1) · See
[security/public-flip-readiness.md](security/public-flip-readiness.md).

### `scan_private_leakage.py` — privacy scan (public-flip gate, C1b)
Pure-stdlib private-leakage scanner (owner home paths, personal email) over the working
tree or full history.

```bash
python scripts/scan_private_leakage.py --worktree
python scripts/scan_private_leakage.py --history --strict
```
Flags: `--strict` (advisory findings also fail the gate), `--json` (findings as JSON),
`--report` (emit a markdown verdict block on stdout — redirect to save it). **Layer:** Gate
(`secret-scan.yml`, C1b).

### `check_flip_readiness.py` — one-command public-flip go/no-go (aggregates C1–C4)
One glance instead of five commands: runs every *fleet-owned* readiness gate — C1 secret
scan · C1b working-tree privacy · C2 license files · C3 source guardrail · C4 ingest
liveness — as isolated child processes, prints a GREEN/RED go-table, and **exits 0 only if
every blocking fleet gate passes**. The Michael-gated decisions (C1c history accept-vs-scrub,
C5/C6 spot-reviews, C7 editorial line, and THE FLIP itself) are listed for context but never
run and never move the exit code. Run it against the exact commit being published as the
flip-time re-verify step.

```bash
python scripts/check_flip_readiness.py             # run all fleet gates, print the go-table
python scripts/check_flip_readiness.py --json      # machine-readable verdict
python scripts/check_flip_readiness.py --history   # also report C1c (history privacy), informational
```
Flags: `--json` (machine-readable verdict), `--history` (also run the C1c git-history privacy
scan — informational, never blocks). **Layer:** Gate aggregator + flip runbook step 1 · See
[security/public-flip-readiness.md](security/public-flip-readiness.md).

### `seed_good_first_issues.py` — good-first-issues catalog
Single source of truth for the newcomer task list: renders
[`.github/GOOD_FIRST_ISSUES.md`](../.github/GOOD_FIRST_ISSUES.md) from the `ISSUES` table
in the script (CI fails if the committed catalog drifts), and at the public flip seeds the
same issues onto the GitHub tracker in one command.

```bash
python scripts/seed_good_first_issues.py --write    # render the committed catalog
python scripts/seed_good_first_issues.py --check    # exit 1 if the catalog drifted (CI guard)
python scripts/seed_good_first_issues.py --create   # flip day: create the issues via gh (needs auth)
```
**Layer:** Gate (CI drift guard) + flip-day tooling.

---

## Dev tooling — not part of the azimuth engine

### `Build-Graphify-AST-Only.py` — deterministic code-graph helper
A standalone [graphify](https://github.com/mickywin22) helper that builds a code-only
knowledge graph (`graphify-out/graph.json` + `GRAPH_REPORT.md`) from a target repo using
pure deterministic Python — zero LLM tokens. It is a developer convenience that lives here
for reuse; it plays **no role** in the azimuth L1 → L2 → L3 runtime or any CI gate.

```bash
python scripts/Build-Graphify-AST-Only.py <target-repo-path>
```
**Layer:** none (dev tooling).

---

See also: [architecture.md](architecture.md) for how these commands chain into the
ingest → synthesis → guardrail → site pipeline, and [docs/README.md](README.md) for the
full documentation map.
