# azimuth

[![CI](https://github.com/mickywin22/azimuth/actions/workflows/ci.yml/badge.svg)](https://github.com/mickywin22/azimuth/actions/workflows/ci.yml)
[![Daily ingest](https://github.com/mickywin22/azimuth/actions/workflows/ingest.yml/badge.svg)](https://github.com/mickywin22/azimuth/actions/workflows/ingest.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT.md)

Public demonstrator of the HemySphere L1/L2/L3 vault doctrine, fed by Worldmonitor open-intelligence data.

> **Status — engine live, awaiting public flip.** The pipeline runs end-to-end: a daily
> GitHub Actions job pulls the WorldMonitor subsets into dated **L1 source notes**, a weekly
> synthesis cycle evolves the per-theme **L2 briefs**, and a small **L3 rule set** (editorial
> line, attribution, source guardrail) governs both — all enforced by CI. The runtime is
> **pure standard-library Python** (no web server, no third-party runtime deps). The concept,
> data-source feasibility, and build plan are written up in [docs/spec.md](docs/spec.md),
> [docs/plan.md](docs/plan.md), and [docs/architecture.md](docs/architecture.md).

## What it is

A public, read-only knowledge vault that applies the HemySphere **L1 sources → L2 synthesis → L3 rules** wiki pattern to open global-intelligence data sourced from the [Worldmonitor](https://worldmonitor.app) public API. It proves the doctrine bundle in a live, non-personal domain — showing the architecture without exposing any private Emi vault content.

## Quick Start

```bash
# Clone
git clone https://github.com/mickywin22/azimuth.git
cd azimuth

# Install dev tooling (pure-stdlib runtime — no server, no third-party deps)
uv pip install -e ".[dev]"

# Run the L1 ingest (pulls WorldMonitor subsets -> dated L1 notes)
python scripts/run_ingest.py
```

## Development

```bash
# Run tests
pytest tests/ -v

# Lint + format
ruff check guardrail/ ingest/ tests/ --fix
ruff format guardrail/ ingest/ tests/

# Type check
mypy guardrail/ ingest/

# Pre-commit hooks
pre-commit install
```

## Public site & deploy

The browsable read-only site (weekly L2 briefs → L1 sources → L3 editorial line, plus the
cross-channel knowledge graph) builds with `python scripts/build_site.py` and is published
to **GitHub Pages** by [`.github/workflows/pages.yml`](.github/workflows/pages.yml) on every
push to `main`.

The knowledge graph is both **visual** (`site/graph.html` — pick any two channels and
**Trace** how they connect) and **queryable from the command line** via
[`scripts/query_graph.py`](scripts/query_graph.py) over the same `site/graph.json`:

```bash
python scripts/query_graph.py connect energy geophysical   # the cross-channel answer
python scripts/query_graph.py provenance "Greece"          # the L1 notes backing an entity
python scripts/query_graph.py path "Greece" "Energy Supply"
python scripts/query_graph.py bridges                       # all cross-channel bridges
python scripts/query_graph.py hubs --top 8 --json
```

Every edge is typed (`has-brief`, `rests-on`, `mentioned-in`, `named-in`, `reported-in`,
`located-in`). The graph reaches the **L1 sources, not just the briefs**: a `mentioned-in`
edge carries a `weight` (how many L1 notes name the entity) and that count is backed by one
`named-in` edge per actual source note — `provenance` re-expands it into the exact dated L1
notes, channel by channel.

> **Pages URL (once enabled): https://mickywin22.github.io/azimuth/**

The repo is **private** and the site is **not live** until GitHub Pages is explicitly
enabled in the repo settings — that flip is a deliberate manual step. Full build steps,
the ready-to-flip gate, and the local validation command are in
[docs/deploy.md](docs/deploy.md).

## Operations — ingest liveness

The daily L1 ingest ([`.github/workflows/ingest.yml`](.github/workflows/ingest.yml)) is the
engine every brief rests on, so its health is observable, not assumed:

- **In-workflow gate** — after each pull the run asserts the newest committed L1 day is
  within tolerance (`scripts/check_ingest_liveness.py --check`); a stale result fails the job.
- **Failure alarm** — a failed daily run opens (or appends to) a single `ingest-alarm`
  tracking issue, so the engine can never die silently.
- **Anywhere** — check liveness by hand:

```bash
python scripts/check_ingest_liveness.py            # alive / STALE, with the latest L1 day + age
python scripts/check_ingest_liveness.py --check    # exit 1 if the latest L1 day is stale
```

## Repository layout

| Path | What it holds |
|------|---------------|
| `ingest/` | L1 pull — registry-driven WorldMonitor fetch → dated source notes (stdlib) |
| `guardrail/` | L3 per-source license / attribution / editorial guardrail |
| `synthesis/` | L2 curator logic, synthesis lint, cross-theme join |
| `scripts/` | CLIs — ingest, site + graph + index builders, query engine, liveness + secret scans |
| `vault/` | The published vault — `00 Rules` (L3) · `01 Sources` (L1) · `02 Briefs` (L2) |
| `site/` | Built read-only site + `graph.json` / `graph.html` knowledge graph |
| `sources/registry.json` | Single source of truth — every WorldMonitor subset + its license/theme |
| `docs/` | Spec, plan, architecture, deploy, security, and per-feature docs |
| `.github/workflows/` | CI · daily ingest · Pages deploy · secret + privacy scans |

## Documentation

Full map of everything under `docs/` — concept & design, the engine, publish/operate,
security, and the demonstrator proof — is in **[docs/README.md](docs/README.md)**.
Start there to go deep; [docs/architecture.md](docs/architecture.md) is the design-decisions
entry point.

## Contributing & security

- **Contributing:** read [CONTRIBUTING.md](CONTRIBUTING.md) first — it explains the
  L1/L2/L3 layer ownership (the `vault/` content is machine-generated, so PRs there are
  not accepted), the gates every change must pass, and the editorial line.
- **Code of conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- **Security / responsible disclosure:** [SECURITY.md](SECURITY.md).

## License

Split license:

- **Code** (`ingest/`, `guardrail/`, `synthesis/`, `scripts/`, `.github/`): **MIT** — see [`LICENSE`](LICENSE).
- **Vault content** (derived L1/L2/L3 notes under `vault/`): **CC BY 4.0** — see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).

Worldmonitor source data is consumed via its public API (Path A, no fork → AGPL not triggered); per-source attribution ships in [`CREDITS.md`](CREDITS.md) and is enforced by the per-source guardrail (`scripts/check_sources.py`).
