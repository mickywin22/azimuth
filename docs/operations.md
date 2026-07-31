# Operations Runbook — keeping the engine alive

azimuth runs as a two-lane engine with a heartbeat on each lane. This is the on-call
page: **every scheduled job, what it guards, the alarm it raises, and exactly what to do
when that alarm fires.** It is the operate half of the "keep the engine operating" goal —
the design of each lane is in [architecture.md](architecture.md); this page is what you
read at 2 a.m. when a badge goes red.

## The two lanes

| Lane | Who runs it | Survives a power-off? | Heartbeat |
|------|-------------|-----------------------|-----------|
| **L1 ingest** | GitHub Actions ([`ingest.yml`](../.github/workflows/ingest.yml)), daily | **Yes** — runs on GitHub infra, no local box needed | in-workflow liveness assert + `ingest-alarm` issue |
| **L2 synthesis** | the fleet curator ([`synthesis/azimuth-curator.md`](../synthesis/azimuth-curator.md)), an LLM job on Michael's box, weekly | **No** — a stopped fleet silently drifts the briefs stale | weekly observer ([`synthesis-freshness.yml`](../.github/workflows/synthesis-freshness.yml)) + `synthesis-alarm` issue |

The split matters: L1 cannot die silently because it lives on GitHub, but L2 depends on a
machine that can be off — so L2 gets its own external heartbeat rather than being assumed
healthy. Neither lane can fail without opening a tracking issue.

## Scheduled jobs & gates at a glance

| Workflow | Cadence | Guards | Alarm on failure |
|----------|---------|--------|------------------|
| [`ingest.yml`](../.github/workflows/ingest.yml) | daily, 06:12 UTC | a fresh L1 day lands + graph/index/benchmark stay in sync | `ingest-alarm` issue (dedup by label) |
| [`synthesis-freshness.yml`](../.github/workflows/synthesis-freshness.yml) | weekly, Mon 06:40 UTC | no brief is **overdue** (> 1 weekly cadence behind L1) | `synthesis-alarm` issue (dedup by label) |
| [`ci.yml`](../.github/workflows/ci.yml) | every push / PR to `main` | lint · format · types · guardrail · synthesis-lint · graph+index sync · doc-links · tests ≥ 80% cov | red check on the PR / commit |
| [`pages.yml`](../.github/workflows/pages.yml) | push to `main` | publishes the site to GitHub Pages **once Pages is enabled** | **skip-not-fail** — green no-op until enabled; never red-floods |
| [`deploy-cloudflare.yml`](../.github/workflows/deploy-cloudflare.yml) | push to `main` | publishes the site to Cloudflare Pages **once the `azimuth` CF project exists** | **skip-not-fail** — green no-op until provisioned; never red-floods |
| [`secret-scan.yml`](../.github/workflows/secret-scan.yml) | every push / PR to `main` | the C1 public-flip gate (gitleaks + stdlib + privacy scan over full history) | **red by design pre-flip** — see below |

## The daily-update guarantee

The public site must never silently go stale. A "guaranteed daily update" is three clauses,
each independently observable — no single failure can go unseen:

1. **The L1-daily ingest lands every day** — [`ingest.yml`](../.github/workflows/ingest.yml)
   runs on GitHub infra (survives a local power-off); its in-workflow liveness assert + the
   `ingest-alarm` issue catch a pull that fails or writes nothing.
2. **A freshness pulse alarms on a miss** — an external watchdog on the operator's box polls
   the GitHub Actions API and raises an operator alert the moment the daily cron goes STALE
   (stops firing) or FAILING (fires but the run fails). This is the blind spot an in-workflow
   guard cannot cover: a workflow that never starts runs neither its own gate nor its own alarm.
3. **Neither deploy workflow red-floods** — [`pages.yml`](../.github/workflows/pages.yml) and
   [`deploy-cloudflare.yml`](../.github/workflows/deploy-cloudflare.yml) each **skip green**
   until their one-time infra step is done (Pages enabled / the `azimuth` Cloudflare project
   created), so an un-provisioned repo is a quiet green no-op — never a wall of red X's that
   buries a genuine break under noise.

Clause 3 is what the job table above now reflects: both deploy lanes are `skip-not-fail`,
gated on the real precondition (enablement / project existence) rather than on repo
visibility or mere secret presence. The gating detail is in [deploy.md](deploy.md) and
[deploy-cloudflare.md](deploy-cloudflare.md). Each lane still auto-deploys on the next push
the moment its infra step is done — no further change to these workflows is needed.

## When an alarm fires — response

### `ingest-alarm` — the L1 engine is down
The daily pull failed; the engine every brief rests on is not producing new source notes.

1. Open the linked run under the [Actions tab](https://github.com/mickywin22/azimuth/actions) and read the failing step.
2. Usual causes: WorldMonitor API unreachable / shape change, or the liveness assert tripped
   because the pull wrote nothing. Reproduce locally:
   ```bash
   python scripts/run_ingest.py --base-url https://api.worldmonitor.app
   python scripts/check_ingest_liveness.py --check   # exit 1 == still stale
   ```
3. If the feed changed shape, fix `ingest/` + the registry, land it on `main`, then
   re-run the workflow (`workflow_dispatch`). Confirm liveness goes green and **close the
   issue** — a repeat failure appends a comment to the same issue rather than opening a new one.

### `synthesis-alarm` — the L2 briefs are genuinely overdue
A clean-theme brief is lagging the latest L1 day by more than one weekly cadence, i.e. the
fleet curator did not run. The briefs feed the public site, so a stale L2 layer is visible.

1. This is **not** a code failure — the workflow only observes; it never synthesises.
2. Check why the fleet curator did not dispatch (fleet paused, budget freeze, box off).
3. Re-run the weekly curator, then confirm green and close the issue:
   ```bash
   python scripts/check_synthesis_freshness.py            # per-theme fresh / stale / OVERDUE
   python scripts/check_synthesis_freshness.py --overdue  # exit 1 only if genuinely overdue
   ```
4. Merely *stale* (0–8d, awaiting the next scheduled pass) is expected and never alarms.

### `secret-scan.yml` red — expected before the public flip
This gate is **intentionally red** until the public flip. History carries owner-private
machine paths (`C:\Users\…`) in since-deleted notes — the **C1c** findings (context, not
credentials). Resolving them is an owner go-gate: *accept* (record a scoped allowlist) or
*scrub* (history rewrite + force-push). Do not "fix" this by disabling the gate. The go/no-go
detail is in [security/public-flip-readiness.md](security/public-flip-readiness.md).

### `ci.yml` / `pages.yml` red — a normal build break
Read the failing step and reproduce locally with the matching command from
[cli.md](cli.md) (e.g. `pytest tests/ -v`, `python scripts/check_doc_links.py`,
`python scripts/build_site.py`). These block `main`, so fix-forward on a branch.

## Manual health check — anytime, anywhere

Both lanes are observable by hand without waiting for the scheduled run:

```bash
python scripts/check_ingest_liveness.py        # L1: alive / STALE + latest day & age
python scripts/check_synthesis_freshness.py    # L2: per-theme fresh / stale / OVERDUE table
python scripts/check_doc_links.py              # every relative Markdown link still resolves
```

A green result on all three means the engine is live end-to-end: L1 flowing, L2 within
cadence, and the docs front door has no dead links.
