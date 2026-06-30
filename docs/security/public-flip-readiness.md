# Azimuth Public-Flip Readiness — Go / No-Go Checklist

> **What this is.** The single decision surface for taking
> [`mickywin22/azimuth`](https://github.com/mickywin22/azimuth) from **private →
> public**. The flip itself is a **Michael go-gate** — no automation makes the
> repo public. This page tracks every condition that must be GREEN first, so the
> flip is a one-glance decision, not a re-investigation.

_Last updated: 2026-06-30 (fleet, Azimuth KR-A) — **hardened + re-ran the secret-scan HARD gate**. The history scan spawned two `git cat-file` per blob (~1240 processes) and **timed out before it could ever return CLEAN** on Windows / a fleet box; rewrote it to a single `git cat-file --batch-all-objects` pass (~30s, finishes). That pass also now covers **UNREACHABLE / dangling blobs** the old reachable-only `rev-list` walk skipped, so a secret hidden in a removed-but-not-scrubbed blob can no longer slip the gate. Re-run over the wider object set: **612 blobs + 241 files, 0 findings, exit 0** — a strictly stronger CLEAN than the prior 576-blob run. Two regression tests added (dangling-blob catch + clean-repo pass). Earlier same-day: fixed a worktree-HARD privacy regression where `scripts/scrub-history.sh` tripped the privacy scanner on the very `/HemySphere/` path it removes; now allowlisted as tooling-docs with a pinning test. Working tree GREEN._

## Verdict at a glance

| # | Gate | Owner | Status |
|---|------|-------|--------|
| C1 | **Secret scan** — no key in working tree or git history | fleet | ✅ **GREEN** — `scripts/scan_secrets.py` over full history + working tree: **612 blobs + 241 files scanned, 0 findings, exit 0** (re-run 2026-06-30, now covering unreachable/dangling blobs too); gitleaks + stdlib both CI-enforced via `.github/workflows/secret-scan.yml`. Evidence inlined under [C1 detail](#c1-detail--secret-scan-evidence) below |
| C1b | **Private-leakage scan (working tree)** — no owner-private context (home paths, personal email, local hook commands) | fleet | ✅ **GREEN** — `scripts/scan_private_leakage.py --worktree`, **0 HARD findings** (241 files, re-verified 2026-06-30); CI-enforced. Removed `.claude/settings.local.json` (local hook paths) + `.claude/dependency-cooldown-policy.md` (HemySphere-internal scaffold doctrine) from the publishable tree + gitignored both. The `scrub-history.sh` helper is allowlisted (it documents the paths it removes — naming them is its job, not a leak) |
| C1c | **Private-leakage scan (git history)** — same, over every reachable blob | **Michael** | ⚠️ **6 HARD findings in history**, all owner-private *paths* (machine layout + vault path — **not** credentials, and the username is already public via the LICENSE). Spread across **four** now-removed-from-HEAD paths, not one: (1) `.claude/settings.local.json` (×3 — local hook paths) · (2) `docs/security/secret-scan-2026-06-30.md` (old blob, `C:\Users\…` — current HEAD copy is clean) · (3) `docs/security/gitleaks-2026-06-24.md` (`C:\Users\…`) · (4) `docs/coolify-deploy.md` (`/HemySphere/`). Public-flip judgement: **(a) accept** as-is, or **(b) scrub** — `bash scripts/scrub-history.sh execute` then force-push. The scrub now purges **all four** paths (verify-proven 0 HARD on a clone) — destructive history rewrite + force-push, so **Michael/reviewer only**, never autonomous |
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
scanner (C1b). A secret OR an owner-private path/email/hook command committed
after the flip — even one reverted in the next commit — trips the gate and fails
the build, so the "clean surface" guarantee does not decay once the repo is
public.

## C1 detail — secret-scan evidence

> **HARD GATE.** The repo must contain **no** secret — in the working tree **or
> anywhere in reachable git history** — before it goes public. A key committed
> once and later removed still lives in history and still leaks. Any finding
> **BLOCKS** the flip.

**Verdict: ✅ CLEAN — gate PASSED.** No API keys, tokens, private keys, webhooks,
or credentialed DB URLs in the working tree or any blob reachable from any ref.

| Pass | Scope | Scanned | Findings | Exit |
|------|-------|---------|----------|------|
| Full git history | **every blob in the object DB — reachable AND dangling**, via `git cat-file --batch-all-objects` | **612 blobs** | **0** | 0 |
| Working tree | tracked + untracked-not-ignored | **241 files** | **0** | 0 |

`python scripts/scan_secrets.py --report` → `0 findings`, exit `0` (re-run
2026-06-30). Tool: `scripts/scan_secrets.py` (pure-stdlib) + gitleaks GitHub
Action, both enforced on every push/PR by `.github/workflows/secret-scan.yml`.

> **Why 612 now, not 576.** The history scan was rewritten from a per-blob
> `git cat-file` loop (two subprocess spawns × every blob → ~1240 processes,
> which **timed out** the gate on Windows / a fleet worker before it could
> return) to a single streamed `git cat-file --batch-all-objects` pass. The new
> object set includes **unreachable / dangling blobs** (the +36) — exactly the
> objects a "removed in a later commit" secret would hide in — so the strongest
> reading of CLEAN now holds: no credential exists anywhere in the object
> database, not just along reachable history. Regression-locked by
> `test_history_scan_catches_secret_removed_in_later_commit`.

**What the gate looks for.** Anthropic / OpenAI keys · AWS access keys · GitHub
PATs (classic + fine-grained) · Google API keys · PEM / OpenSSH private-key
blocks · Slack webhooks + tokens · JWTs (incl. Supabase `service_role`) ·
database URLs with embedded `user:password@` · high-entropy values assigned to
secret-named variables. Known placeholders (`sk-ant-...`, `your-anon-key`, the
canonical AWS docs key) are allowlisted so the gate fails only on a **real**
secret. Detection + allowlist are regression-tested in
`tests/unit/test_scan_secrets.py`.

**Reproduce.**
```bash
python scripts/scan_secrets.py            # history + working tree
python scripts/scan_secrets.py --report   # markdown verdict
gitleaks git . --redact -c .gitleaks.toml # matches CI (if binary on PATH)
```

---
*Owned by the Azimuth public-flip gate (KR-A). C1 secret-scan + C1b/C1c
private-leakage evidence is consolidated on this page (the previously separate
dated reports were folded in here so the history-scrub can purge their old blobs
cleanly). History scrub: `scripts/scrub-history.sh`.*
