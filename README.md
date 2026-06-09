# world-vault

Public demonstrator of the HemySphere L1/L2/L3 vault doctrine, fed by Worldmonitor open-intelligence data.

> **Stage: `research` (2026-W24).** This is a Coding-Factory scaffold, not a running app yet. The product concept, data-source feasibility, and build plan live in the HemySphere vault (`05 Projects/World Vault.md` + `07 Resources/AI Agents & Agentic Systems/Worldmonitor App – Research.md`) and in [docs/spec.md](docs/spec.md). The FastAPI/Next.js stack below is the factory default and will be reshaped once the data-pipeline design lands.

## What it is

A public, read-only knowledge vault that applies the HemySphere **L1 sources → L2 synthesis → L3 rules** wiki pattern to open global-intelligence data sourced from the [Worldmonitor](https://worldmonitor.app) public API. It proves the doctrine bundle in a live, non-personal domain — showing the architecture without exposing any private Emi vault content.

## Quick Start

```bash
# Clone
git clone https://github.com/mickywin22/world-vault.git
cd world-vault

# Backend
uv pip install -e ".[dev]"
cp .env.example .env  # Fill in values
uvicorn src.backend.main:app --reload

# Frontend
cd src/frontend
npm install
npm run dev
```

## Development

```bash
# Run tests
pytest tests/ -v

# Lint + format
ruff check src/ tests/ --fix
ruff format src/ tests/

# Type check
mypy src/

# Pre-commit hooks
pre-commit install
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for design decisions.

## License

TBD before first public publish — likely MIT or CC-BY-SA for the synthesised vault output. Worldmonitor source data is consumed via its public API (Path A, no fork → AGPL not triggered); attribution ships in `CREDITS.md` per the feasibility analysis. See `07 Resources/AI Agents & Agentic Systems/Worldmonitor App – Research.md` § World Vault Feasibility.
