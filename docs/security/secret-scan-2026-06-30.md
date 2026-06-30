# Secret Scan — Azimuth Public-Flip Gate (C1) — 2026-06-30

> **HARD GATE** for the Azimuth public-flip (KR-A). The repository must contain
> **no** secret — in the working tree **or anywhere in reachable git history** —
> before it is made public. A key committed once and later removed still lives
> in history and still leaks once the repo is public. If any secret is found,
> the flip is **BLOCKED**.

## Verdict

# ✅ CLEAN — gate PASSED. No secret-exposure risk blocks the flip.

No API keys, tokens, private keys, webhooks, or credentialed DB URLs were
detected in the Azimuth working tree or in any blob reachable from any ref
(`origin/main` + every local/feature branch).

## Scan metadata

| Field | Value |
|-------|-------|
| Gate | C1 — public-flip secret scan (Azimuth KR-A) |
| Tool | `scripts/scan_secrets.py` (pure-stdlib, this repo) + gitleaks GitHub Action (CI) |
| Scan date | 2026-06-30 |
| Repo | `~/Projects/azimuth` (mickywin22/azimuth) |
| Scope | full history (`git rev-list --all --objects`) + working tree (`git ls-files --cached --others --exclude-standard`) |
| Redaction | enabled — any match is redacted, never printed in clear |

## Results

| Pass | Scope | Scanned | Findings | Exit |
|------|-------|---------|----------|------|
| Full git history | every reachable blob, all refs | **543 blobs** | **0** | 0 |
| Working tree | tracked + untracked-not-ignored | **232 files** | **0** | 0 |

`python scripts/scan_secrets.py --report` → `0 findings`, exit `0`.

## What the gate looks for

Anthropic / OpenAI keys · AWS access keys · GitHub PATs (classic + fine-grained)
· Google API keys · PEM / OpenSSH private-key blocks · Slack webhooks + tokens ·
JWTs (incl. Supabase `service_role`) · database URLs with embedded
`user:password@` · high-entropy values assigned to secret-named variables. The
placeholders that legitimately live in this repo (`sk-ant-...`, `your-anon-key`,
`postgresql://user:password@host`, the canonical AWS docs key) are allowlisted so
the gate fails only on a **real** secret, never on a template. Detection +
allowlist are regression-tested in `tests/unit/test_scan_secrets.py` (14 tests).

## Why this scan supersedes the 2026-06-24 one

The earlier `gitleaks-2026-06-24.md` report ran a real gitleaks binary and was
also CLEAN — but it (a) never merged to `main` (it sat on a dead feature branch),
and (b) predates 35 commits of work since, including six daily ingest pulls
(2026-06-25 … 2026-06-29) and the whole knowledge-graph layer. This scan covers
the **current** publishable surface and lands the gate **on `main`**, enforced
by CI (`.github/workflows/secret-scan.yml`) so it cannot go stale again.

## Reproduce

```bash
# stdlib gate (no install, runs anywhere Python runs):
python scripts/scan_secrets.py            # history + working tree
python scripts/scan_secrets.py --report   # markdown verdict
python scripts/scan_secrets.py --json      # machine-readable

# gitleaks (matches CI), if the binary is on PATH:
gitleaks git . --redact -c .gitleaks.toml  # full history
# exit 0 = clean, exit 1 = leak(s) found
```

---
*Generated for the Azimuth C1 public-flip secret-scan gate. See
[`public-flip-readiness.md`](./public-flip-readiness.md) for the full flip
go/no-go checklist.*
