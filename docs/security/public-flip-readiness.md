# Azimuth Public-Flip Readiness — Go / No-Go Checklist

> **What this is.** The single decision surface for taking
> [`mickywin22/azimuth`](https://github.com/mickywin22/azimuth) from **private →
> public**. The flip itself is a **Michael go-gate** — no automation makes the
> repo public. This page tracks every condition that must be GREEN first, so the
> flip is a one-glance decision, not a re-investigation.

_Last updated: 2026-07-03 (owner decision session)._
_Re-verified: 2026-07-13 (W29, two passes) — every fleet gate is GREEN once the 2026-07-13 weekly L2 curator run lands (it clears the C4b freshness gate; `check_flip_readiness.py` exits 0 with it applied). The flip stays execute-only on Michael's GO (#898); see [2026-W29 re-verification](#2026-w29-re-verification-2026-07-13)._

## Verdict at a glance

| # | Gate | Owner | Status |
|---|------|-------|--------|
| C1 | **Secret scan** — no key in working tree or git history | fleet | ✅ **GREEN** — **re-verified 2026-07-13 @ `cead29a`: 1382 history blobs + 570 working-tree files, 0 findings** (grew from 543+232 on [2026-06-30](./secret-scan-2026-06-30.md) — the W28 UI/SOTA merges + the Cloudflare Pages deploy path are now scan-covered & clean); CI-enforced (`secret-scan.yml`) |
| C1b | **Private-leakage scan (working tree)** — no owner-private context (home paths, personal email, local hook commands) | fleet | ✅ **GREEN** — `scripts/scan_private_leakage.py --worktree`, **0 HARD findings**; CI-enforced. Removed `.claude/settings.local.json` (local hook paths) + `.claude/dependency-cooldown-policy.md` (HemySphere-internal scaffold doctrine) from the publishable tree + gitignored both |
| C1c | **Private-leakage scan (git history)** — same, over every reachable blob | **Michael** | ✅ **ACCEPTED as-is (owner decision 2026-07-03)** — 11 machine-path findings (never credentials; username already public via LICENSE) — the now-removed `.claude/settings.local.json` blobs (this box's absolute hook paths, e.g. `C:\Users\Michael\...lean-ctx.exe`) plus machine paths quoted inside old security-doc / scrub-script blobs (`docs/security/*.md`, `scripts/scrub-history.sh`, `docs/coolify-deploy.md`). **Low severity** (machine paths + a username already public via the LICENSE, *not* credentials), but a public-flip judgement: **(a) accept** as-is, or **(b) scrub** the blobs from history (`git filter-repo`/BFG + force-push) before the flip — a destructive history rewrite, so **Michael/reviewer only**, never autonomous. Surfaced **non-blocking** in the every-push `privacy-scan` job so it doesn't red-fail CI by design; the full-history scan is enforced at flip time |
| C2 | **License files present** — code MIT + content CC-BY-4.0 | fleet | ✅ GREEN — `LICENSE` + `LICENSE-CONTENT.md` on `main` |
| C3 | **Source guardrail green** — every surfaced source licensed + credited | fleet | ✅ GREEN — `scripts/check_sources.py` in CI |
| C4 | **Daily ingest healthy** — GH-Actions L1 pull exits 0 | fleet | ✅ GREEN — re-verified 2026-07-13: ingest **alive**, latest L1 day 2026-07-12 (1d old), 24 days on record; `ingest.yml` 07-10/11/12 all success |
| C4b | **Synthesis freshness** — no clean brief overdue past the weekly cadence (else main CI is red) | fleet | ✅ **GREEN — cleared 2026-07-13** by the weekly L2 curator run (all 5 clean briefs re-synthesised to the 2026-07-13 L1; `check_synthesis_freshness.py --overdue` exits 0, 0/5 stale). Was 🔴 RED earlier the same day (5/5 briefs **11d overdue** → `pytest`'s `test_live_repo_is_internally_consistent` failed → `ci.yml` on `main` = failure). The curator commit (`2e209ba`) lands via the concurrent Azimuth-KR3 dispatch; **`ci.yml` goes green on `main` when it merges.** Blocking gate in `check_flip_readiness.py` |
| C5 | **USP / positioning spot-review** (~15 min) | **Michael** | ✅ **GREEN — approved 2026-07-03** (5 claims + answers/benchmark surface signed off) |
| C6 | **First autonomous weekly cycle spot-review** — the live briefs read neutral + correct | **Michael** | ✅ **GREEN — approved 2026-07-03** (W27 cycle: both lanes autonomous + lint-green) |
| C7 | **prediction-markets editorial line** — confirm it stays HELD (or define how it's briefed) | **Michael** | ⏳ PENDING — IQ #915 (does not block flip; held source is `surfaced:false` for L2) |
| 🚩 | **THE FLIP** — make the repo public | **Michael** | ⛔ **HELD by owner decision 2026-07-03** — every gate is green; the flip is now execute-only on the owner's GO (IQ #898) |

**Bottom line (2026-07-13, later W29 pass):** **every fleet gate is now GREEN.**
The C4b freshness gate — the one red gate earlier today — is **cleared**: the
weekly L2 curator has run (all 5 clean briefs re-synthesised to the 2026-07-13
L1), so `python scripts/check_flip_readiness.py` **exits 0 — all fleet gates
GREEN** (C1 secret scan CLEAN · C1b/C2/C3/C4/C4b green). `ci.yml` on `main` goes
green when that curator commit (`2e209ba`) merges — it is landing via the
concurrent Azimuth-KR3 dispatch. The two Michael spot-reviews and the C1c call are
**already decided** (see the ledger below). So the flip is now **execute-only on
Michael's GO (#898)** — no fleet-actionable step remains once the curator commit
is on `main`.

**Owner decisions are now recorded** in
[`flip-decisions.json`](./flip-decisions.json), which `check_flip_readiness.py`
reads so its verdict reflects your real calls instead of a hard-coded PENDING:
**C5 approved · C6 approved · C1c accepted** (all 2026-07-03) · **C7 pending**
(non-blocking) · **FLIP held** (execute-only on GO #898).

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

### Later W29 pass — C4b cleared, all fleet gates GREEN (2026-07-13)

The earlier pass above found a single red gate: **C4b** (5/5 clean briefs 11d overdue → `ci.yml`
red). This later pass confirms it is **resolved**. The weekly L2 `azimuth-curator` re-synthesised
all five clean-theme briefs to the 2026-07-13 L1 day (commit `2e209ba`), and the full aggregator
was re-run against that exact surface in an isolated `git worktree`:

| Gate | origin/main @ `4189e60` (before curator) | curator tip `2e209ba` (after) |
|------|------------------------------------------|-------------------------------|
| C1 secret scan (history + tree) | ✅ CLEAN | ✅ CLEAN |
| C1b privacy scan (worktree) | ✅ CLEAN (8 advisory only) | ✅ CLEAN (8 advisory only) |
| C2 / C3 / C4 | ✅ GREEN | ✅ GREEN (C4: L1 2026-07-13, 0d old, 25 days on record) |
| C4b synthesis freshness | 🔴 **RED** — 5/5 briefs 11d overdue, `--overdue` exit 1 | ✅ **GREEN** — 0/5 stale, `--overdue` exit 0 |
| `check_flip_readiness.py` verdict | exit 1 (C4b red) | **exit 0 — all fleet gates GREEN** |

So the only fleet-actionable blocker disappears the moment the curator commit (`2e209ba`) is on
`main` — it lands via the concurrent Azimuth-KR3 dispatch. This dispatch (Azimuth-KR1 S2)
**pre-verified** readiness against both the current and post-curator surface; it did **not** run
the curator itself and it did **not** touch repo visibility. The flip remains **execute-only on
Michael's GO (#898)**.

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
