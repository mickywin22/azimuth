# azimuth

Public demonstrator of the HemySphere L1/L2/L3 vault doctrine, fed by Worldmonitor open-intelligence data.

> **Stage: `research` (2026-W24).** This is a Coding-Factory scaffold, not a running app yet. The product concept, data-source feasibility, and build plan live in the HemySphere vault (`05 Projects/azimuth.md` + `07 Resources/AI Agents & Agentic Systems/Worldmonitor App – Research.md`) and in [docs/spec.md](docs/spec.md). The FastAPI/Next.js stack below is the factory default and will be reshaped once the data-pipeline design lands.

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

## Architecture

See [docs/architecture.md](docs/architecture.md) for design decisions.

## OKF conformance

The `vault/` bundle is a **Knowledge Bundle conformant with the Open Knowledge Format (OKF) v0.1**
(Google Cloud's vendor-neutral markdown-corpus standard), at the spec-minimal bar. The conformance
claim, citation mapping, and the honest caveat that relationship links are still Tier-2 (deferred
`[[wikilink]]` → markdown-link migration) are documented in the bundle profile: [`OKF.md`](OKF.md).

## License

Split license — confirmed IQ #371 (A), 2026-06-10:

- **Code** (`ingest/`, `guardrail/`, `scripts/`, `.github/`, future `synthesis/`): **MIT** — see [`LICENSE`](LICENSE).
- **Vault content** (derived L1/L2/L3 notes under `vault/`): **CC BY 4.0** — see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).

Worldmonitor source data is consumed via its public API (Path A, no fork → AGPL not triggered); per-source attribution ships in [`CREDITS.md`](CREDITS.md) and is enforced by the per-source guardrail (`scripts/check_sources.py`).
