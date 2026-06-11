# L1 Ingest — registry-driven pull

> **Phase 1, F1.** Pulls each surfaced WorldMonitor subset and writes a dated, verbatim
> L1 markdown note. The endpoint, `license`, and attribution all come from
> [`sources/registry.json`](../sources/registry.json) — ingest and the
> [source-guardrail](source-guardrail.md) share **one** source of truth.

## The single-source-of-truth contract

There is deliberately **no** `ingest/endpoints.json`. The plan's original draft listed one,
but a separate endpoint+license file would drift from the registry the guardrail enforces.
Instead:

- `ingest/pull.py` reads the surfaced endpoint set from `registry.json` via the guardrail's
  `load_registry`.
- The `license` and `attribution` it stamps into every L1 note are read **straight off the
  same registry entry** — never re-typed.
- Before writing a note, ingest runs the guardrail's `check_source` on the entry. A
  surfaced-but-non-compliant source (missing/disallowed license, missing attribution/credit,
  editorial-exclusion class) produces **no** L1 note — for the exact reason CI would fail the
  build. Ingest can never surface what the guardrail would block.

Net effect: to change a source's license, endpoint, or attribution you edit **one** JSON
entry; both the guardrail and the ingest frontmatter follow automatically.

## What a note looks like

`vault/01 Sources/YYYY-MM-DD/<registry-key>.md`:

```markdown
---
source: "GIE AGSI+ (Gas Infrastructure Europe)"
source_key: "natural-gas-storage-eu"
endpoint: "/api/economic/v1/get-nat-gas-storage"
retrieved: "2026-06-10T09:30:00Z"
license: "CC-BY-4.0"
attribution: "Data: GIE AGSI+ via WorldMonitor (api.worldmonitor.app)"
---

# GIE AGSI+ (Gas Infrastructure Europe)

> L1 source pull — `natural-gas-storage-eu` from `/api/economic/v1/get-nat-gas-storage` at 2026-06-10T09:30:00Z. Verbatim transform; never edit by hand.

| date | pct |
| --- | --- |
| 2026-06-09 | 71.2 |
```

Transform is verbatim — list of objects → table, single object → key/value table, anything
else → fenced `json`. **Zero synthesis at L1** (that is the L2 curator's job).

## Running it

```bash
python scripts/run_ingest.py            # live pull + write into vault/01 Sources
python scripts/run_ingest.py --dry-run  # fetch + render, write nothing
python scripts/run_ingest.py --base-url http://localhost:8080   # against a local stub
```

Exit code is `1` if any source errored (so a cron / CI step fails loudly), `0` otherwise —
an all-skipped run is still `0`.

## Degraded mode

A fetch that raises (network, HTTP, non-JSON) is logged and recorded as an error for that
source; the run continues and the other sources still write. No single source can crash the
daily run. The live fetcher (`ingest/http.py`) mints an anonymous WorldMonitor session
(`POST /api/wm-session`, free ~12 h cookie) once per run and reuses it.

## Modules

| File | Role |
|------|------|
| `ingest/pull.py` | registry-driven core: eligibility, frontmatter, transform, write (pure, tested offline) |
| `ingest/http.py` | live `HttpFetcher` — session-mint + JSON GET (stdlib urllib) |
| `scripts/run_ingest.py` | CLI entry point for the daily cron |
| `tests/unit/test_ingest_pull.py` | 23 unit tests incl. the live-registry license-match contract |

## Still to wire (later Phase-1 slices)

- `.github/workflows/ingest.yml` daily cron + commit, and an L1-schema lint CI job.
- 3-consecutive-failure → auto-opened GitHub issue (spec gate).
- ~~Template strip (`src/backend` FastAPI, `src/frontend`) once no server runtime is needed —
  note the guardrail currently lives under `src/backend/guardrail/`, so the strip must move
  it (e.g. to `guardrail/`) rather than delete it.~~ ✅ **Done 2026-06-11:** `src/backend` +
  `src/frontend` deleted, guardrail moved to top-level `guardrail/`, imports + CI/pre-commit
  paths fixed, runtime deps trimmed to pure-stdlib. See `docs/changelog.md`.
