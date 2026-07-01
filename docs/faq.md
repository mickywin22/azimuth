# azimuth — FAQ

Short answers to the questions a first-time visitor asks. Each links to the deep doc if you
want the full story. For the one-paragraph pitch and quick start, start at the
[root README](../README.md); for the full doc map, see the [docs index](README.md).

## What is azimuth?

A public, read-only **knowledge vault** that applies the HemySphere **L1 sources → L2
synthesis → L3 rules** wiki pattern to open global-intelligence data. It exists to *prove the
doctrine* in a live, non-personal domain — showing the architecture without exposing any
private content. The full concept is in [spec.md](spec.md); the design decisions are in
[architecture.md](architecture.md).

## Is the data real, or a mock-up?

Real. A daily GitHub Actions job pulls open-intelligence subsets from the
[Worldmonitor](https://worldmonitor.app) public API into dated **L1 source notes**
(`vault/01 Sources/YYYY-MM-DD/`). Nothing is hand-typed or synthetic. Which channels are
surfaced and why is audited in
[sources/worldmonitor-channel-audit.md](sources/worldmonitor-channel-audit.md), and every
source's license is declared in `sources/registry.json` and enforced in CI. How the pull works:
[l1-ingest.md](l1-ingest.md).

## How current is it?

- **L1 sources** refresh **daily** (automated GitHub Actions cron).
- **L2 briefs** refresh **weekly** (the fleet curator pass).

Both lanes are watched, not assumed: each has a scheduled heartbeat that raises a dedup'd
tracking issue if it dies (the two liveness badges at the top of the [README](../README.md)).
You can also check by hand — `python scripts/check_ingest_liveness.py` and
`python scripts/check_synthesis_freshness.py`. Details in
[l1-ingest.md](l1-ingest.md) and [synthesis.md](synthesis.md).

## Can I trust the L2 briefs and forecasts?

Treat azimuth as a **demonstrator of a synthesis method**, not as investment, safety, or
policy advice. Two things make the briefs auditable rather than opaque:

1. **Provenance** — every claim in an L2 brief rests on dated L1 notes you can open, and the
   knowledge graph re-expands any entity into the exact source notes that name it.
2. **Facts vs forecast** — the demonstrator keeps an honest scoreboard (the `Benchmark` brief
   and the "what-if" [proof](proof/README.md)) so forecast quality is shown, not claimed.

The editorial line and attribution rules that govern every brief live in the L3 layer
(`vault/00 Rules/`) and are enforced by the [source guardrail](source-guardrail.md).

## What license is it under? Can I reuse it?

A **split license**: the code (`ingest/`, `guardrail/`, `synthesis/`, `scripts/`, `.github/`)
is **MIT** ([LICENSE](../LICENSE)); the derived vault content is **CC BY 4.0**
([LICENSE-CONTENT.md](../LICENSE-CONTENT.md)). Worldmonitor data is consumed via its public API
(no fork), and per-source attribution ships in [CREDITS.md](../CREDITS.md). To cite the
project, use [CITATION.cff](../CITATION.cff) (GitHub's "Cite this repository" button).

## Why is the repo private and the site not live yet?

Both are a deliberate manual go-gate, not an oversight. The public flip is owner-gated on a
security decision: the `secret-scan.yml` workflow is intentionally **red** until the owner
resolves the **C1c** owner-private-history finding (accept-as-harmless vs history scrub). The
full go/no-go checklist is in
[security/public-flip-readiness.md](security/public-flip-readiness.md); the deploy steps are in
[deploy.md](deploy.md).

## Can I contribute?

Yes for code and docs — read [CONTRIBUTING.md](../CONTRIBUTING.md) first (it explains the layer
ownership and the gates every change must pass) and
[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md). **Note:** the `vault/` content is
machine-generated, so PRs that hand-edit briefs or sources are not accepted — fix the engine
that produces them instead.

## What is it built with?

**Pure standard-library Python** — no web server, no third-party runtime dependencies. The
read-only site is static HTML built by `scripts/build_site.py` and published to GitHub Pages.
The full CLI surface (18 stdlib tools) is mapped in [cli.md](cli.md).

## I found a security issue.

Please follow the responsible-disclosure policy in [SECURITY.md](../SECURITY.md) — do not open
a public issue for a vulnerability.
