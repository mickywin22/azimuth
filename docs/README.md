# azimuth — Documentation Index

Everything under `docs/` in one map. azimuth is a public demonstrator of the
HemySphere **L1 sources → L2 synthesis → L3 rules** vault doctrine, fed by
[Worldmonitor](https://worldmonitor.app) open-intelligence data and published as a
static site. Start with the [root README](../README.md) for the one-paragraph pitch
and quick start; come here to go deep.

## Concept & design

| Doc | What it covers |
|-----|----------------|
| [spec.md](spec.md) | The specification — what azimuth is, the doctrine it proves, and why. |
| [plan.md](plan.md) | The implementation plan (phased build sequence). |
| [architecture.md](architecture.md) | How the pieces fit: ingest → synthesis → guardrail → static site. |
| [strategy/okf-and-knowledge-graph.md](strategy/okf-and-knowledge-graph.md) | OKF (Open Knowledge Foundation) conformance + the knowledge-graph layer. |

## The engine (how it runs)

| Doc | What it covers |
|-----|----------------|
| [l1-ingest.md](l1-ingest.md) | L1 ingest — the registry-driven daily pull of WorldMonitor subsets into dated source notes. |
| [synthesis.md](synthesis.md) | L2 synthesis engine — how per-theme briefs evolve from the L1 notes. |
| [source-guardrail.md](source-guardrail.md) | The L3 source guardrail — per-source license + content check enforced in CI. |
| [cli.md](cli.md) | CLI reference — every command under `scripts/`, how to run it, and the layer/gate it serves. |
| [doc-links.md](doc-links.md) | The documentation link gate — no dead relative Markdown link reaches the public front door. |
| [sources/worldmonitor-channel-audit.md](sources/worldmonitor-channel-audit.md) | Which WorldMonitor channels are surfaced, and why (full-universe audit). |

## Publish & operate

| Doc | What it covers |
|-----|----------------|
| [site.md](site.md) | The public static site — build + structure. |
| [deploy.md](deploy.md) | Deploy pipeline (GitHub Pages). |
| [changelog.md](changelog.md) | Notable changes, Keep-a-Changelog format. |
| [LESSONS.md](LESSONS.md) | Running log of build lessons. |

## Security & public-flip readiness

| Doc | What it covers |
|-----|----------------|
| [security/public-flip-readiness.md](security/public-flip-readiness.md) | The go/no-go checklist for flipping the repo public. |
| [security/secret-scan-2026-06-30.md](security/secret-scan-2026-06-30.md) | Point-in-time C1 secret-scan report (gitleaks + stdlib scanner over full history + working tree) — verdict CLEAN, the evidence bank behind the flip gate. |
| _C1c owner-private-history decision_ | The accept-vs-scrub call on the owner-private home-paths in history is an owner go-gate; the decision doc + the one-command `scripts/check_flip_readiness.py` aggregator are staged on the public-flip branch and land with the flip, not before it. See the `Secret Scan` workflow (§ below) for the live gate status. |
| [SECURITY.md](../SECURITY.md) | Vulnerability-reporting policy (repo root). |

## Proof

| Doc | What it covers |
|-----|----------------|
| [proof/README.md](proof/README.md) | The "what-if / show-your-work" living-system proof baked into the demonstrator. |

## Continuous integration & gates

Five GitHub Actions workflows run the engine and guard the repo. All are visible under
[`.github/workflows/`](../.github/workflows/); the two badges at the top of the root README
track the first two.

| Workflow | Runs | Blocks on | Status |
|----------|------|-----------|--------|
| `ci.yml` | every push / PR to `main` | lint · format · type-check · source-guardrail · synthesis-lint · brief-index + graph sync · **doc-link resolve** · **unit + integration tests + ≥80% coverage** | green |
| `ingest.yml` | daily cron + `workflow_dispatch` | a stale L1 day (in-workflow liveness assert) | green, running daily |
| `synthesis-freshness.yml` | weekly cron (Mondays) + `workflow_dispatch` | nothing per-push — opens a dedup'd `synthesis-alarm` issue if any clean-theme brief is genuinely **overdue** (lagging the latest L1 day by more than one weekly cadence) | green, running weekly |
| `pages.yml` | push to `main` | the static-site build | skipped while the repo is private |
| `secret-scan.yml` | every push / PR to `main` | **credentials over full history** (gitleaks + the stdlib scanner) and **owner-private context in the working tree** (C1b); pre-existing *history-only* privacy findings are surfaced non-blocking (C1c — see below) | green |

**How the privacy gate is scoped.** `secret-scan.yml` guards two different things.
*Credentials* (gitleaks + `scripts/scan_secrets.py`) hard-block over the **full history** —
a leaked key committed and reverted is compromised forever. *Owner-private context*
(`scripts/scan_private_leakage.py`) is split by scope: a HARD finding in the **working tree**
blocks the merge, so no push can newly introduce an owner-private path; the handful of
pre-existing **history-only** findings (the owner's local machine paths in since-deleted
notes — never credentials) are surfaced **non-blocking** on every run. Those history findings
are the **C1c** accept-vs-scrub call — a deliberate owner go-gate resolved at flip time
(the `scripts/check_flip_readiness.py` aggregator and the C1c decision write-up are staged
on the public-flip branch and land with the flip), never an autonomous history rewrite.
The split design is pinned by `tests/unit/test_secret_scan_workflow.py`, and the full
rationale lives in [security/public-flip-readiness.md](security/public-flip-readiness.md).

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md), [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md),
and [CREDITS.md](../CREDITS.md) at the repo root. Code is MIT; published content is
CC BY 4.0 (see [LICENSE](../LICENSE) + [LICENSE-CONTENT.md](../LICENSE-CONTENT.md)).
