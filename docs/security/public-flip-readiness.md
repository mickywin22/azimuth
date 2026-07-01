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
| C1b | **Private-leakage scan (working tree)** — no owner-private context (home paths, personal email, local hook commands) | fleet | ✅ **GREEN** — `scripts/scan_private_leakage.py --worktree`, **0 HARD findings**; CI-enforced. Removed `.claude/settings.local.json` (local hook paths) + `.claude/dependency-cooldown-policy.md` (HemySphere-internal scaffold doctrine) from the publishable tree + gitignored both |
| C1c | **Private-leakage scan (git history)** — same, over every reachable blob | **Michael** | ⚠️ **11 HARD findings in history** (as of 2026-07-01) — the now-removed `.claude/settings.local.json` blobs (this box's absolute hook paths, e.g. `C:\Users\Michael\...lean-ctx.exe`) plus machine paths quoted inside old security-doc / scrub-script blobs (`docs/security/*.md`, `scripts/scrub-history.sh`, `docs/coolify-deploy.md`). **Low severity** (machine paths + a username already public via the LICENSE, *not* credentials), but a public-flip judgement: **(a) accept** as-is, or **(b) scrub** the blobs from history (`git filter-repo`/BFG + force-push) before the flip — a destructive history rewrite, so **Michael/reviewer only**, never autonomous. Surfaced **non-blocking** in the every-push `privacy-scan` job so it doesn't red-fail CI by design; the full-history scan is enforced at flip time |
| C2 | **License files present** — code MIT + content CC-BY-4.0 | fleet | ✅ GREEN — `LICENSE` + `LICENSE-CONTENT.md` on `main` |
| C3 | **Source guardrail green** — every surfaced source licensed + credited | fleet | ✅ GREEN — `scripts/check_sources.py` in CI |
| C4 | **Daily ingest healthy** — GH-Actions L1 pull exits 0 | fleet | ✅ GREEN — 22 written / 0 errored after the 06-25 de-surface fix |
| C5 | **USP / positioning spot-review** (~15 min) — `05 Projects/azimuth — USP & Strategy.md` reads right before it hardens into the public README/LinkedIn pitch | **Michael** | ⏳ **PENDING — IQ #888** |
| C6 | **First autonomous weekly cycle spot-review** — the live briefs read neutral + correct | **Michael** | ⏳ **PENDING — IQ #937** |
| C7 | **prediction-markets editorial line** — confirm it stays HELD (or define how it's briefed) | **Michael** | ⏳ PENDING — IQ #915 (does not block flip; held source is `surfaced:false` for L2) |
| 🚩 | **THE FLIP** — make the repo public | **Michael** | ⛔ **HELD** until C5 + C6 green — IQ #898 |

**Bottom line:** the fleet-owned gates (C1–C4, C1b) are all GREEN — the
**publishable working tree is clean** of both credentials and owner-private
context. The flip now waits on Michael's two ~15-min spot-reviews (C5 #888,
C6 #937) plus one one-line call on C1c (accept vs scrub the history home-paths).
Nothing fleet-actionable blocks it.

### Advisory (does NOT block the flip — a Michael judgement call)

The private-leakage scan also surfaces **23 advisory findings** — internal
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
