# Security Policy

azimuth is a read-only public demonstrator with a **pure standard-library runtime** (no web
server, no database, no third-party runtime dependencies) and **no user accounts or secrets
in the repository**. The attack surface is small by design, but we still take reports
seriously.

## Reporting a vulnerability

Please **do not** open a public issue for a security problem. Instead, use GitHub's private
channel:

1. Go to the repository's **Security** tab → **Report a vulnerability** (GitHub Security
   Advisories), or
2. Open a private security advisory draft if you have access.

Include: what you found, where (file / commit / workflow), how to reproduce, and the impact
you expect. We aim to acknowledge a report within a few days and to agree a disclosure
timeline with you before any public detail is shared.

## What counts as in scope

- A **leaked credential** committed to history or the working tree.
- **Owner-private context** (personal paths, emails, machine-local config) reaching the
  publishable surface.
- A way to make the **CI / ingest workflows** execute untrusted code or exfiltrate secrets.
- A guardrail bypass that lets unlicensed / editorially-excluded content into a brief.

Out of scope: the *content* of WorldMonitor source data itself (we consume it via its public
API and attribute it; data accuracy is upstream), and the absence of features.

## How the repository defends itself

These run in CI on every push/PR and locally via pre-commit — they are the gates a fix must
keep green:

| Gate | What it enforces | Where |
|------|------------------|-------|
| Secret scan | No API keys / tokens / PEM blocks / credentialed URLs in history or tree | `scripts/scan_secrets.py`, `.github/workflows/secret-scan.yml` |
| Privacy / leakage scan | No owner-private paths, emails, or local hook commands | `scripts/scan_private_leakage.py` |
| Source guardrail | Every surfaced source is licensed, attributed, and editorially clean | `scripts/check_sources.py` |
| Synthesis lint | Every L2 claim is sourced; editorial deny-list honoured | `scripts/check_synthesis.py` |

The full public-readiness checklist (the C1–C4 gates behind the public flip) lives in
[docs/security/public-flip-readiness.md](docs/security/public-flip-readiness.md).

## Supported versions

This is a continuously-deployed demonstrator with no release branches; security fixes land
on `main`.
