# Getting help with azimuth

azimuth is a **solo-maintained public demonstrator**, not a supported product. There is
no support SLA, no on-call rota for the public, and no paid tier. What there *is*: a
thorough set of docs and a runbook, because the whole point of azimuth is to show the
HemySphere **L1 → L2 → L3** vault doctrine working in the open. This page routes you to
the right place fast.

## Start here — most questions are already answered

| You want to… | Go to |
|--------------|-------|
| Understand what azimuth is, whether the data is real, how current it is, and the license | [docs/faq.md](docs/faq.md) — the first-time-visitor FAQ |
| See the one-paragraph pitch and run it locally | [README.md](README.md) — Quick Start |
| Understand how the engine fits together (ingest → synthesis → guardrail → site) | [docs/architecture.md](docs/architecture.md) |
| Find every command under `scripts/` and what it does | [docs/cli.md](docs/cli.md) |
| Read the full documentation map | [docs/README.md](docs/README.md) |

## Something looks broken

First check whether it is a *known* transient, not a bug:

- **A status badge is red** on the [README](README.md) (`CI`, `Daily ingest`, or
  `L2 freshness`). The [operations runbook](docs/operations.md) explains exactly what each
  alarm means and what — if anything — needs doing. Several red states are *expected*
  (e.g. the pre-flip `secret-scan` gate); the runbook says which.
- **The daily ingest missed a day.** WorldMonitor is an upstream open API; a single missed
  pull is self-healing (the next day's cron catches up) and only becomes an alarm after
  three consecutive failures. See the runbook's `ingest-alarm` section.

If it is a genuine defect, open a **Bug report** issue using the
[bug template](.github/ISSUE_TEMPLATE/bug_report.md). Include what you ran, what you
expected, and the actual output.

## You have an idea

Open a **Feature request** issue using the
[feature template](.github/ISSUE_TEMPLATE/feature_request.md). Note the scope boundary:
the `vault/` content (the L1 notes and L2 briefs) is **machine-generated** — it is a
build output, not hand-editable, so PRs against it are not accepted. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the layer-ownership rule and the gates every
change must pass.

## You found a security issue

**Do not open a public issue.** Report it privately via a
[GitHub security advisory](https://github.com/mickywin22/azimuth/security/advisories/new).
The policy is in [SECURITY.md](SECURITY.md).

## Expectations, honestly

- **Response time:** best-effort, no guarantee. This is a side project.
- **Support scope:** the code and docs in this repo. Questions about the upstream
  [Worldmonitor](https://worldmonitor.app) API belong with Worldmonitor.
- **Conduct:** all interaction is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
