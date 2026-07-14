# Azimuth Public-Flip Readiness — Go / No-Go Checklist

> **What this is.** The single decision surface for taking
> [`mickywin22/azimuth`](https://github.com/mickywin22/azimuth) from **private →
> public**. The flip itself is a **Michael go-gate** — no automation makes the
> repo public. This page tracks every condition that must be GREEN first, so the
> flip is a one-glance decision, not a re-investigation.

_Last updated: 2026-07-03 (owner decision session)._
_Re-verified: 2026-07-13 (W29) against `main` @ `cead29a` — credential/owner-private gates GREEN, but C4b synthesis-freshness RED (main CI failing on stale briefs); see [2026-W29 re-verification](#2026-w29-re-verification-2026-07-13)._
_Re-verified: 2026-07-14 (W29) against the curator-fix surface `2e209ba` (= `main` @ `4189e60` + the staged weekly-curator refresh) — **ALL fleet gates GREEN, `check_flip_readiness.py` exits 0, secret-scan CLEAN (1439 history blobs + 595 files, 0 findings)**; C4b now GREEN (0/5 briefs overdue). The C4b-clearing fix is **committed as `2e209ba` but not yet on `main`** — main CI stays RED only until it is pushed. See [2026-07-14 re-verification](#2026-07-14-re-verification-w29)._

## Verdict at a glance

| # | Gate | Owner | Status |
|---|------|-------|--------|
| C1 | **Secret scan** — no key in working tree or git history | fleet | ✅ **GREEN** — **re-verified 2026-07-13 @ `cead29a`: 1382 history blobs + 570 working-tree files, 0 findings** (grew from 543+232 on [2026-06-30](./secret-scan-2026-06-30.md) — the W28 UI/SOTA merges + the Cloudflare Pages deploy path are now scan-covered & clean); CI-enforced (`secret-scan.yml`) |
| C1b | **Private-leakage scan (working tree)** — no owner-private context (home paths, personal email, local hook commands) | fleet | ✅ **GREEN** — `scripts/scan_private_leakage.py --worktree`, **0 HARD findings**; CI-enforced. Removed `.claude/settings.local.json` (local hook paths) + `.claude/dependency-cooldown-policy.md` (HemySphere-internal scaffold doctrine) from the publishable tree + gitignored both |
| C1c | **Private-leakage scan (git history)** — same, over every reachable blob | **Michael** | ✅ **ACCEPTED as-is (owner decision 2026-07-03)** — 11 machine-path findings (never credentials; username already public via LICENSE) — the now-removed `.claude/settings.local.json` blobs (this box's absolute hook paths, e.g. `C:\Users\Michael\...lean-ctx.exe`) plus machine paths quoted inside old security-doc / scrub-script blobs (`docs/security/*.md`, `scripts/scrub-history.sh`, `docs/coolify-deploy.md`). **Low severity** (machine paths + a username already public via the LICENSE, *not* credentials), but a public-flip judgement: **(a) accept** as-is, or **(b) scrub** the blobs from history (`git filter-repo`/BFG + force-push) before the flip — a destructive history rewrite, so **Michael/reviewer only**, never autonomous. Surfaced **non-blocking** in the every-push `privacy-scan` job so it doesn't red-fail CI by design; the full-history scan is enforced at flip time |
| C2 | **License files present** — code MIT + content CC-BY-4.0 | fleet | ✅ GREEN — `LICENSE` + `LICENSE-CONTENT.md` on `main` |
| C3 | **Source guardrail green** — every surfaced source licensed + credited | fleet | ✅ GREEN — `scripts/check_sources.py` in CI |
| C4 | **Daily ingest healthy** — GH-Actions L1 pull exits 0 | fleet | ✅ GREEN — re-verified 2026-07-13: ingest **alive**, latest L1 day 2026-07-12 (1d old), 24 days on record; `ingest.yml` 07-10/11/12 all success |
| C4b | **Synthesis freshness** — no clean brief overdue past the weekly cadence (else main CI is red) | fleet | 🟡 **FIX STAGED (2026-07-14)** — the 10d-overdue stall (5 clean briefs last synthesised 2026-07-02) is resolved by the weekly-curator refresh to the 2026-07-13 L1, **committed as `2e209ba`**. Verified **GREEN on the fix surface**: `check_flip_readiness.py` C4b = 0/5 overdue, exit 0. Still **RED on `main`** only until `2e209ba` is pushed (reviewer's job) → then `pytest`'s `test_live_repo_is_internally_consistent` passes and `ci.yml` goes green. Blocking gate in `check_flip_readiness.py` (added 2026-07-13 so the tool can no longer report "all GREEN" while CI is red) |
| C5 | **USP / positioning spot-review** (~15 min) | **Michael** | ✅ **GREEN — approved 2026-07-03** (5 claims + answers/benchmark surface signed off) |
| C6 | **First autonomous weekly cycle spot-review** — the live briefs read neutral + correct | **Michael** | ✅ **GREEN — approved 2026-07-03** (W27 cycle: both lanes autonomous + lint-green) |
| C7 | **prediction-markets editorial line** — confirm it stays HELD (or define how it's briefed) | **Michael** | ⏳ PENDING — IQ #915 (does not block flip; held source is `surfaced:false` for L2) |
| 🚩 | **THE FLIP** — make the repo public | **Michael** | ⛔ **HELD by owner decision 2026-07-03** — every gate is green; the flip is now execute-only on the owner's GO (IQ #898) |

**Bottom line (2026-07-14):** **every fleet gate is now GREEN and the flip is one
reviewer-push away from execute-ready.** The credential + owner-private surface is
clean (C1/C1b/C2/C3/C4 GREEN — no secret, no owner-private path). The two Michael
spot-reviews and the C1c call are **already decided** (ledger below). The C4b
freshness blocker (the only thing keeping `ci.yml` red) is **fixed** — the weekly
curator ran and the refresh is **committed as `2e209ba`**; `check_flip_readiness.py`
exits 0 on that surface. The **one remaining fleet step is mechanical, not a
decision: push `2e209ba` to `main`** (reviewer's job) so `ci.yml` re-runs green.
Once it lands, **the flip is execute-only on your GO (#898)** — no further fleet
work. This dispatch verified readiness against the fix surface and banked the
snapshot; it did **not** touch repo visibility.

**Owner decisions are now recorded** in
[`flip-decisions.json`](./flip-decisions.json), which `check_flip_readiness.py`
reads so its verdict reflects your real calls instead of a hard-coded PENDING:
**C5 approved · C6 approved · C1c accepted** (all 2026-07-03) · **C7 pending**
(non-blocking) · **FLIP held** (execute-only on GO #898).

## 2026-07-14 re-verification (W29)

`fleet-kr1-auto-W29-07140454` (S2 pre-verify). The 2026-07-13 run left `main` CI **RED**
on C4b (5 clean briefs 10d overdue). Since then the weekly `azimuth-curator` ran and
refreshed all 5 clean briefs to the 2026-07-13 L1 day — **committed as `2e209ba`** — but
that commit was **local-only, not yet on `main`** (`origin/main` @ `4189e60`, `ci.yml`
still failure at re-verify time). This dispatch re-ran **every fleet gate against the fix
surface `2e209ba`** (= `main` + the curator refresh, i.e. the exact tree `main` becomes the
moment the commit is pushed):

| Gate | Result on `2e209ba` (2026-07-14) |
|------|----------------------------------|
| C1 secret scan (history + tree) | ✅ CLEAN — **1439 history blobs + 595 files, 0 findings** (grew from 1382+570 on 07-13; the new ingest day + curator refresh are scan-covered & clean) |
| C1b privacy scan (worktree) | ✅ GREEN — 8 advisory only, 0 HARD |
| C2 license files | ✅ `LICENSE` (MIT) + `LICENSE-CONTENT.md` (CC-BY-4.0) present |
| C3 source guardrail | ✅ PASS — every surfaced source licensed/attributed/credited |
| C4 ingest liveness | ✅ alive — latest L1 day 2026-07-13 (1d old), 25 days on record |
| C4b synthesis freshness | ✅ **GREEN — 0/5 clean briefs overdue** (was RED; `2e209ba` cleared it) |
| **`check_flip_readiness.py`** | ✅ **exits 0 — `all_fleet_green: true`** |

**Verdict:** the S2 fleet-half stop_when is **MET** — `check_flip_readiness.py` exits 0,
secret-scan CLEAN, the owner-decision ledger records C5/C6 approved + C1c accepted, and
#898 is the standing decision-grade GO row. The **only** thing between here and a green
`main` CI is pushing `2e209ba` (this branch carries it) — a mechanical reviewer-push, not a
Michael decision. After it lands, **the flip is execute-only on Michael's GO (#898)**, which
remains HELD by owner choice — untouched by this dispatch.

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
| C4b synthesis freshness | 🔴 **RED** — 5/5 clean briefs 10d overdue (curator due); makes `ci.yml` red |

**Correction (2026-07-13): the earlier "all fleet gates GREEN / ci.yml = success" claim was
wrong.** The credential + owner-private gates (C1/C1b/C2/C3/C4) are GREEN — no new secret or
owner-private path entered the 2.5×-larger tree, and the new Cloudflare Pages deploy path
carries **no `CLOUDFLARE_API_TOKEN`** in tree or history (deploy secrets live only in
GitHub-Actions repo secrets). **But `ci.yml` on `main` is FAILURE** (GH-Actions run
29222624953, the prior re-verify commit `9150ad7`): `pytest tests/unit/` fails
`test_live_repo_is_internally_consistent` because the weekly L2 curator has not run — all 5
clean briefs are 10 days stale (> the 8-day overdue grace). `secret-scan.yml` + the L1
`ingest.yml` 07-10/11/12 are green; **`ci.yml` is not.** The flip must wait for the curator to
run and CI to go green.

This whole re-verify is now **one command** — `python scripts/check_flip_readiness.py`. As of
2026-07-13 it is **hardened** so it can no longer give a false green: it now includes **C4b
(synthesis freshness overdue)** as a blocking gate, so it reports RED whenever main CI is red on
stale briefs — the exact gap that let the prior run print "all GREEN" while `ci.yml` was
failing. It also reads the **owner-decision ledger** (`flip-decisions.json`), so the
Michael-gated rows show your recorded calls (C5/C6 approved, C1c accepted, FLIP held) instead of
a blanket PENDING. Run it at flip time against the exact commit being published; it exits 0 only
if **every** blocking fleet gate — now including freshness — is GREEN.

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
