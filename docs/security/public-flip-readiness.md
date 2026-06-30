# Azimuth Public-Flip Readiness — Go / No-Go Checklist

> **What this is.** The single decision surface for taking
> [`mickywin22/azimuth`](https://github.com/mickywin22/azimuth) from **private →
> public**. The flip itself is a **Michael go-gate** — no automation makes the
> repo public. This page tracks every condition that must be GREEN first, so the
> flip is a one-glance decision, not a re-investigation.

_Last updated: 2026-06-30 (fleet, Azimuth KR-A)._

## Verdict at a glance

| # | Gate | Owner | Status |
|---|------|-------|--------|
| C1 | **Secret scan** — no key in working tree or git history | fleet | ✅ **GREEN** — [scan 2026-06-30](./secret-scan-2026-06-30.md), 543 blobs + 232 files, 0 findings; CI-enforced |
| C2 | **License files present** — code MIT + content CC-BY-4.0 | fleet | ✅ GREEN — `LICENSE` + `LICENSE-CONTENT.md` on `main` |
| C3 | **Source guardrail green** — every surfaced source licensed + credited | fleet | ✅ GREEN — `scripts/check_sources.py` in CI |
| C4 | **Daily ingest healthy** — GH-Actions L1 pull exits 0 | fleet | ✅ GREEN — 22 written / 0 errored after the 06-25 de-surface fix |
| C5 | **USP / positioning spot-review** (~15 min) — `05 Projects/azimuth — USP & Strategy.md` reads right before it hardens into the public README/LinkedIn pitch | **Michael** | ⏳ **PENDING — IQ #888** |
| C6 | **First autonomous weekly cycle spot-review** — the live briefs read neutral + correct | **Michael** | ⏳ **PENDING — IQ #937** |
| C7 | **prediction-markets editorial line** — confirm it stays HELD (or define how it's briefed) | **Michael** | ⏳ PENDING — IQ #915 (does not block flip; held source is `surfaced:false` for L2) |
| 🚩 | **THE FLIP** — make the repo public | **Michael** | ⛔ **HELD** until C5 + C6 green — IQ #898 |

**Bottom line:** the fleet-owned gates (C1–C4) are all GREEN. The flip now waits
only on Michael's two ~15-min spot-reviews (C5 #888, C6 #937). Nothing technical
blocks it.

## The flip, when Michael says go

The #851 USP scope is already **approved** (2026-06-22: richer knowledge-graph +
cheap Tier-1 OKF conformance; wikilink migration deferred; Hyper-Extract NO-GO).
Once C5 + C6 are signed off:

```bash
# 1. (re-confirm the gate is still clean on the exact commit being published)
cd ~/Projects/azimuth && git checkout main && git pull
python scripts/scan_secrets.py            # expect: CLEAN, exit 0

# 2. flip visibility
gh repo edit mickywin22/azimuth --visibility public --accept-visibility-change-consequences

# 3. confirm GitHub Pages serves the public site (pages.yml already wired)
gh browse --repo mickywin22/azimuth
```

Then the queued **Career-Promo launch post** (IQ #890) can ride the flip.

## After the flip — the gate stays live

`.github/workflows/secret-scan.yml` runs on every push / PR to `main` (gitleaks
over full history + the stdlib scanner). A secret committed after the flip — even
one reverted in the next commit — trips the gate and fails the build, so the
"clean history" guarantee does not decay once the repo is public.

---
*Owned by the Azimuth public-flip gate (KR-A). C1 detail:
[`secret-scan-2026-06-30.md`](./secret-scan-2026-06-30.md).*
