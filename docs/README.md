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
| `synthesis-freshness.yml` | weekly (Monday) + `workflow_dispatch` | an **overdue** L2 brief — opens a single `synthesis-alarm` issue only when the weekly curator pass genuinely failed to run (merely *stale* stays quiet) | green, watching |
| `pages.yml` | push to `main` | the static-site build | — |
| `secret-scan.yml` | every push / PR to `main` | **C1 public-flip gate** — gitleaks + the stdlib secret scan + the private-leakage scan, each over **full history** | **red, by design (see below)** |

**Why `secret-scan.yml` is red before the flip.** The private-leakage job scans the whole
git history for owner-private context (home paths, personal email). History still carries a
handful of the owner's local machine paths (`C:\Users\…`) in since-deleted security-report
notes. These are the **C1c** findings: not credentials, but owner-private context. Resolving
them is a deliberate **owner go-gate** — either *accept* them as harmless machine paths (record
a scoped allowlist) or *scrub* history (a rewrite + force-push). The gate is intentionally kept
**hard and red** until that call is made, so the repo cannot flip public with unresolved
owner-private history. The one-command `scripts/check_flip_readiness.py` aggregator that fronts
this gate, and the C1c decision write-up, are staged on the public-flip branch and land with the
flip. Nothing here is silently dropped — the security gate is a dedicated, always-on workflow.

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md), [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md),
and [CREDITS.md](../CREDITS.md) at the repo root. Code is MIT; published content is
CC BY 4.0 (see [LICENSE](../LICENSE) + [LICENSE-CONTENT.md](../LICENSE-CONTENT.md)).
