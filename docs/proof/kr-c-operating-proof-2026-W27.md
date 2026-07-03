# Engine operating proof — week 2026-W27 (Azimuth KR-C)

KR-C's promise is twofold: the repo **reads public-grade** and the two-lane engine
**keeps operating** without anyone touching it. Docs and gates can be reviewed at any
commit, but "keeps operating" is a claim about *time* — it is only provable by pointing
at a specific week and showing every lane fired on schedule. This page banks that
evidence for 2026-W27 (Mon 2026-06-29 → Sun 2026-07-05), the week the docs batch
completed. The operating model itself is documented in the
[operations runbook](../operations.md); this page is the week's observed telemetry.

## Lane 1 — daily L1 ingest (GitHub cron, power-off-proof)

[`ingest.yml`](../../.github/workflows/ingest.yml) runs at 06:12 UTC daily on GitHub
infra. Every scheduled run this week to date fired and went green, and each landed its
dated L1 notes as a commit:

| Day | Actions run (UTC) | Conclusion | Landed commit |
|-----|-------------------|------------|---------------|
| Mon 2026-06-29 | 08:06 | success | `7467d66` |
| Tue 2026-06-30 | 07:35 | success | `739ca0b` |
| Wed 2026-07-01 | 07:47 | success | `6ff016d` |
| Thu 2026-07-02 | 07:22 | success | `9d872dd` |

(The gap between the 06:12 cron line and the actual start times is GitHub's normal
scheduled-run queueing delay, not an engine fault. Later W27 days were still ahead of
the cron when this page was banked; the badge on the root README tracks them live.)

## Lane 2 — weekly L2 synthesis (fleet curator) + its watchdog

The weekly curator pass ran for W27 and evolved **all five clean-theme briefs** from
the 2026-07-02 L1 day — landed as `965860f` (2026-07-02) and refreshed by `f1b891f`
(2026-07-03). Because this lane runs off-GitHub, its liveness is additionally watched
by [`synthesis-freshness.yml`](../../.github/workflows/synthesis-freshness.yml)
(Mondays 06:12+ UTC), which opens a `synthesis-alarm` issue only when a brief is
genuinely overdue. The watchdog itself shipped mid-W27, so its first scheduled firing
is Mon 2026-07-06 — from then on this lane's proof is the third README badge, not a
hand-banked table.

## The public-grade docs surface (what "reads public-grade" means here)

The full front door was in place by the end of W27: README with engine + license
badges, [CONTRIBUTING](../../CONTRIBUTING.md), [SUPPORT](../../SUPPORT.md),
[SECURITY](../../SECURITY.md), [CODE_OF_CONDUCT](../../CODE_OF_CONDUCT.md),
[CREDITS](../../CREDITS.md), [CITATION.cff](../../CITATION.cff), the split
MIT / CC BY 4.0 [license pair](../../LICENSE-CONTENT.md), issue + PR templates, a
[first-time-visitor FAQ](../faq.md), the [operations runbook](../operations.md), and
the [docs index](README.md) mapping every page. Four drift classes are build
failures, not review conventions: dead links, unindexed docs, orphaned docs, and
undocumented CLIs — see the [doc-link gate](../doc-links.md) and the
[changelog](../changelog.md) for each gate's entry.

## The remaining human gate

One KR-C item is deliberately *not* autonomous: the first weekly brief's quality
spot-review is queued as an owner decision row in the private tracker (queued
2026-07-01, open at banking time). Like the C1c history call in
[public-flip-readiness](../security/public-flip-readiness.md), it is an owner go-gate
by design — the engine keeps running either way.
