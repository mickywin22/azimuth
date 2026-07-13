# Azimuth Public-Flip Readiness — Go / No-Go Checklist

> **What this is.** The single decision surface for taking
> [`mickywin22/azimuth`](https://github.com/mickywin22/azimuth) from **private →
> public**. The flip itself is a **Michael go-gate** — no automation makes the
> repo public. This page tracks every condition that must be GREEN first, so the
> flip is a one-glance decision, not a re-investigation.

_Last updated: 2026-07-03 (owner decision session)._
_Re-verified: 2026-07-13 (W29) against `main` @ `cead29a` — fleet gates still all GREEN on the grown surface; see [2026-W29 re-verification](#2026-w29-re-verification-2026-07-13)._

## Verdict at a glance

| # | Gate | Owner | Status |
|---|------|-------|--------|
| C1 | **Secret scan** — no key in working tree or git history | fleet | ✅ **GREEN** — **re-verified 2026-07-13 @ `cead29a`: 1382 history blobs + 570 working-tree files, 0 findings** (grew from 543+232 on [2026-06-30](./secret-scan-2026-06-30.md) — the W28 UI/SOTA merges + the Cloudflare Pages deploy path are now scan-covered & clean); CI-enforced (`secret-scan.yml`) |
| C1b | **Private-leakage scan (working tree)** — no owner-private context (home paths, personal email, local hook commands) | fleet | ✅ **GREEN** — `scripts/scan_private_leakage.py --worktree`, **0 HARD findings**; CI-enforced. Removed `.claude/settings.local.json` (local hook paths) + `.claude/dependency-cooldown-policy.md` (HemySphere-internal scaffold doctrine) from the publishable tree + gitignored both |
| C1c | **Private-leakage scan (git history)** — same, over every reachable blob | **Michael** | ✅ **ACCEPTED as-is (owner decision 2026-07-03)** — 11 machine-path findings (never credentials; username already public via LICENSE) — the now-removed `.claude/settings.local.json` blobs (this box's absolute hook paths, e.g. `C:\Users\Michael\...lean-ctx.exe`) plus machine paths quoted inside old security-doc / scrub-script blobs (`docs/security/*.md`, `scripts/scrub-history.sh`, `docs/coolify-deploy.md`). **Low severity** (machine paths + a username already public via the LICENSE, *not* credentials), but a public-flip judgement: **(a) accept** as-is, or **(b) scrub** the blobs from history (`git filter-repo`/BFG + force-push) before the flip — a destructive history rewrite, so **Michael/reviewer only**, never autonomous. Surfaced **non-blocking** in the every-push `privacy-scan` job so it doesn't red-fail CI by design; the full-history scan is enforced at flip time |
| C2 | **License files present** — code MIT + content CC-BY-4.0 | fleet | ✅ GREEN — `LICENSE` + `LICENSE-CONTENT.md` on `main` |
| C3 | **Source guardrail green** — every surfaced source licensed + credited | fleet | ✅ GREEN — `scripts/check_sources.py` in CI |
| C4 | **Daily ingest healthy** — GH-Actions L1 pull exits 0 | fleet | ✅ GREEN — re-verified 2026-07-13: ingest **alive**, latest L1 day 2026-07-12 (1d old), 24 days on record; `ingest.yml` 07-10/11/12 all success |
| C5 | **USP / positioning spot-review** (~15 min) | **Michael** | ✅ **GREEN — approved 2026-07-03** (5 claims + answers/benchmark surface signed off) |
| C6 | **First autonomous weekly cycle spot-review** — the live briefs read neutral + correct | **Michael** | ✅ **GREEN — approved 2026-07-03** (W27 cycle: both lanes autonomous + lint-green) |
| C7 | **prediction-markets editorial line** — confirm it stays HELD (or define how it's briefed) | **Michael** | ⏳ PENDING — IQ #915 (does not block flip; held source is `surfaced:false` for L2) |
| 🚩 | **THE FLIP** — make the repo public | **Michael** | ⛔ **HELD by owner decision 2026-07-03** — every gate is green; the flip is now execute-only on the owner's GO (IQ #898) |

**Bottom line:** the fleet-owned gates (C1–C4, C1b) are all GREEN — the
**publishable working tree is clean** of both credentials and owner-private
context. The flip now waits on Michael's two ~15-min spot-reviews (C5 #888,
C6 #937) plus one one-line call on C1c (accept vs scrub the history home-paths).
Nothing fleet-actionable blocks it.

## 2026-W29 re-verification (2026-07-13)

The 2026-07-03 owner-decision gates were verified against an earlier `main`. Since then
`main` advanced to `cead29a` (2026-07-12 ingest day) — **5 daily L1 ingests + the W28 KR1
"incredible UI" and KR2 SOTA-repo merges + the KR3 Cloudflare Pages deploy path**
(`wrangler.toml`, `.github/workflows/deploy-cloudflare.yml`). A stale scan no longer covers
the publishable surface — the same dead-branch failure mode that let the 2026-06-24 gitleaks
pass rot 35 commits behind `main` — so every fleet gate was re-run against the current commit:

| Gate | Result on `cead29a` (2026-07-13) |
|------|----------------------------------|
| C1 secret scan (history + tree) | ✅ CLEAN — **1382 history blobs + 570 files, 0 findings** (2.5× the 543+232 surface of 06-30) |
| C1b privacy scan (worktree) | ✅ CLEAN — 568 files, 0 HARD |
| C2 license files | ✅ `LICENSE` (MIT) + `LICENSE-CONTENT.md` (CC-BY-4.0) present |
| C3 source guardrail | ✅ PASS — 38 sources, 22 surfaced, all licensed/attributed/credited |
| C4 ingest liveness | ✅ alive — latest L1 day 2026-07-12 (1d old), 24 days on record |

**All fleet gates GREEN on the current surface.** No new secret or owner-private path entered
the 2.5×-larger tree — notably the new Cloudflare Pages deploy path carries **no
`CLOUDFLARE_API_TOKEN`** in the working tree or git history (the deploy secrets live only in
GitHub-Actions repo secrets, never committed). CI confirms it: `secret-scan.yml` + `ci.yml`
latest runs on `main` = success; `ingest.yml` 07-10 / 07-11 / 07-12 all success.

This whole re-verify is now **one command** — `python scripts/check_flip_readiness.py` — landed
on `main` this dispatch. It had been stranded on the unmerged W27 branch
`fleet/azimuth-kra-secretscan-batch-W27-06300615`, so the "one-glance, not a re-investigation"
tool this page promised was not actually on the surface that flips. Run it at flip time against
the exact commit being published; it exits 0 only if every blocking fleet gate is GREEN.

**The flip itself remains HELD on Michael's GO (IQ #898) — unchanged.** This dispatch verified
readiness only; it did **not** touch repo visibility.

### Advisory — RESOLVED 2026-07-03 (scrubbed to 0)

Owner decision 2026-07-03: internal ticket refs are not needed for azimuth's
function and were scrubbed to neutral provenance phrasing (22 findings -> 0,
`scan_private_leakage.py --worktree` CLEAN). Historical context below.

The private-leakage scan previously surfaced advisory findings — internal
HemySphere **IQ ticket numbers** (`IQ #371`, `#429`, `#915`, …) and a couple of
internal process markers (`Strategic Architect`, `HemySphere Sprint`) cited as
provenance across the public-facing docs (`README.md`, `docs/spec.md`,
`docs/plan.md`, `LICENSE`, `CREDITS.md`, `sources/registry.json`,
`synthesis/azimuth-curator.md`). These are **not owner-private data** — they
expose nothing sensitive, only that a private ticketing system exists — so they
do not HARD-block. The flip decision can choose either way:
- **Keep** — they read as an honest build-provenance trail (the "build-in-public"
  posture azimuth is partly for); or
- **Scrub** — run `python scripts/scan_private_leakage.py --worktree` to list
  them, then replace each `IQ #NNN` with a neutral phrase before the flip.

Run `python scripts/scan_private_leakage.py --strict` to treat the advisory set
as blocking (i.e. enforce a full scrub) if that is the chosen posture.

## The flip, when Michael says go

The #851 USP scope is already **approved** (2026-06-22: richer knowledge-graph +
cheap Tier-1 OKF conformance; wikilink migration deferred; Hyper-Extract NO-GO).
Once C5 + C6 are signed off:

```bash
# 1. (re-confirm every fleet gate is still green on the exact commit being published)
cd ~/Projects/azimuth && git checkout main && git pull
python scripts/check_flip_readiness.py    # expect: FLEET GATES all GREEN, exit 0

# 2. flip visibility
gh repo edit mickywin22/azimuth --visibility public --accept-visibility-change-consequences

# 3. confirm GitHub Pages serves the public site (pages.yml already wired)
gh browse --repo mickywin22/azimuth
```

Then the queued **Career-Promo launch post** (IQ #890) can ride the flip.

## After the flip — the gate stays live

`.github/workflows/secret-scan.yml` runs on every push / PR to `main` — gitleaks
over full history + the stdlib secret scanner (C1) **and** the private-leakage
scanner (C1b). The two gates are scoped differently on purpose:

- **C1 (credentials)** hard-blocks over **full history** — a leaked key is
  compromised forever, so even one committed and reverted in the next commit
  trips the gate.
- **C1b (owner-private context)** hard-blocks on the **working tree** — the fleet
  can never commit a new home-path / hook command — while pre-existing owner-private
  blobs in **history** are surfaced **non-blocking** (the C1c accept-vs-scrub call,
  a Michael go-gate, never an autonomous rewrite). This keeps the every-push gate
  from being red-by-design on the known C1c blobs while still blocking any *new*
  owner-private leak. The full-history privacy scan runs at flip time (C1c below),
  so the flip itself stays protected.

So the "clean surface" guarantee does not decay once the repo is public: any *new*
secret or owner-private path fails the build, and the C1c history call is made once,
explicitly, at the flip.

---
*Owned by the Azimuth public-flip gate (KR-A). C1 detail:
[`secret-scan-2026-06-30.md`](./secret-scan-2026-06-30.md).*
