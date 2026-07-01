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
| [security/c1c-history-decision.md](security/c1c-history-decision.md) | The C1c owner-private-history accept-vs-scrub decision (owner go-gate). |
| [SECURITY.md](../SECURITY.md) | Vulnerability-reporting policy (repo root). |

## Proof

| Doc | What it covers |
|-----|----------------|
| [proof/README.md](proof/README.md) | The "what-if / show-your-work" living-system proof baked into the demonstrator. |

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md), [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md),
and [CREDITS.md](../CREDITS.md) at the repo root. Code is MIT; published content is
CC BY 4.0 (see [LICENSE](../LICENSE) + [LICENSE-CONTENT.md](../LICENSE-CONTENT.md)).
