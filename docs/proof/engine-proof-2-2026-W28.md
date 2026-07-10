# Engine proof #2 — 2026-W28

The public-grade claim is *"this runs itself and is watched."* Proof #1
([kr-c-operating-proof-2026-W27.md](kr-c-operating-proof-2026-W27.md)) banked a clean week:
every daily L1 cron run and the weekly L2 synthesis pass observed firing on schedule. Proof #2
is the more valuable kind — **the week the watch caught a real miss.** It shows the safety net
works, not just the happy path.

## TL;DR

| Layer | State this week | Evidence |
|-------|-----------------|----------|
| **Daily L1 ingest** | ✅ alive — committing daily | `chore(ingest)` commits on `main` for 2026-07-08, -09, -10 |
| **Weekly L2 synthesis (on `main`)** | ⚠️ **stale — 8 days behind** | all 5 clean briefs `updated: 2026-07-02`; latest L1 day 2026-07-10 |
| **External synthesis watchdog** | ✅ **first fire, correct alarm** | `azimuth_synthesis_watch` event, 2026-07-10T10:34:20Z, `state: stale`, `max_behind: 8` |

The engine's *ingest* half is healthy; its *weekly-synthesis* half stalled; and the watchdog
built for exactly this failure mode **fired for the first time and correctly flagged it.** That
is the proof.

## What the watchdog is

The in-repo [`synthesis-freshness.yml`](../../.github/workflows/synthesis-freshness.yml)
workflow opens a dedup'd GitHub issue when a clean-theme brief goes *overdue* (more than one full
weekly cadence behind the latest L1). That is one layer. The **second, independent layer** is an
external watchdog on the operator's box (described in [operations.md](../operations.md)) that polls
the same freshness signal on a ~daily throttle and pushes a phone alert — so a synthesis lane
that goes silently dead is caught even if the whole scheduled fleet stops running, not only if a
GitHub Action fires. Its design mirrors the ingest watchdog that, on *its* first live run, caught
a 5-day silent ingest outage.

## The first fire (2026-07-10)

On its first qualifying run this week the external watchdog emitted a single
`azimuth_synthesis_watch` telemetry event (verified: exactly one such event exists — this is the
inaugural fire):

```json
{
  "event_type": "azimuth_synthesis_watch",
  "ts": "2026-07-10T10:34:20Z",
  "state": "stale",
  "stale_count": 5,
  "total_count": 5,
  "max_behind": 8,
  "themes": ["climate-signals", "energy-supply", "environmental-hazards",
             "geophysical", "prediction-markets"]
}
```

It read the freshness report, classified all five clean briefs as lagging the latest L1 day by
more than its 4-day tolerance (max 8 days behind), and raised a `#important`-class alarm naming
the repo and the brief directory. Correct verdict, correct severity, first time asked.

Reproduce the underlying signal from a clone:

```console
$ python scripts/check_synthesis_freshness.py --json
# every clean theme: "brief_updated": "2026-07-02", "latest_l1": "2026-07-10",
#                    "stale": true, "days_behind": 8
```

## What the alarm surfaced (the honest gap)

The alarm is not a false positive — the weekly L2 synthesis genuinely has not landed on `main`
this week. Root cause: the W28 weekly-curator dispatch ran, but its output is **stranded on an
unmerged review branch** (`fleet-review/azimuth-curator-wk-W28-*`) and never reached `main`, so
the published briefs sit at their 2026-07-02 state while the daily ingest kept advancing the L1
floor underneath them. The daily-ingest commits regenerate the derived artifacts (graph, brief
index, benchmark) but deliberately **do not** re-synthesise brief prose — that is the curator's
weekly job — so the freshness gap widened one day at a time until the watchdog tripped at >4 days.

This is the by-design daily-L1 / weekly-L2 cadence gap turning into a real *overdue* because the
weekly pass didn't complete to `main` — precisely the condition the watchdog exists to make
loud instead of silent.

## Fix routed

Landing a fresh weekly synthesis (evolve all 5 clean briefs off the 2026-07-10 L1 day, on
`main`) is the curator role's job and is routed as follow-up work; once it lands, the same
`check_synthesis_freshness.py` signal returns `stale: false` and the watchdog posts its recovery
note. The value banked *here* is independent of that fix: **the watch layer provably works** —
proof #2 is the caught miss.

## Verify

- Daily ingest alive: `git log --oneline -- vault/01\ Sources | head` shows a dated
  `chore(ingest)` commit for each recent day.
- Current freshness: `python scripts/check_synthesis_freshness.py --json`.
- Watchdog design + the freshness gate it reads: [operations.md](../operations.md),
  [synthesis.md](../synthesis.md).
