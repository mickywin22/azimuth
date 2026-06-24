# Credits & Attribution

azimuth is an **API consumer** of [WorldMonitor](https://api.worldmonitor.app) (Path A — no
source fork). It transforms WorldMonitor's open-intelligence API responses into a derived,
HemySphere-pattern public vault. No upstream source code is copied or modified.

Every surfaced data subset is registered in [`sources/registry.json`](sources/registry.json)
and validated by the per-source license guardrail (`scripts/check_sources.py`) before it can
be surfaced. Each credit line below is tagged with its registry `key` so the credit ↔ registry
join stays machine-checkable.

## Primary aggregator

- **WorldMonitor** — `api.worldmonitor.app` — public API aggregator. Upstream project
  [`koala73/worldmonitor`](https://github.com/koala73/worldmonitor) is AGPL-3.0 + commercial
  dual-licensed; pure API-consumer use does not trigger AGPL (no fork, no modified service).

## Surfaced upstream sources (multi-theme)

**Energy Supply theme**

- `natural-gas-storage-eu` — GIE AGSI+ (Gas Infrastructure Europe) — CC-BY-4.0
- `crude-oil-inventories` — U.S. EIA (Energy Information Administration) — US-Gov public domain
- `fuel-prices` — WorldMonitor aggregated fuel-price feed — API-ToS-derived
- `energy-prices` — WorldMonitor aggregated energy spot/forward feed — API-ToS-derived

**Geophysical theme**

- `earthquakes` — USGS Earthquake Hazards Program — US-Gov public domain

**Prediction Markets theme**

- `prediction-markets` — Polymarket public odds via WorldMonitor — API-ToS-derived (raw odds surfaced as L1 data only; L2 carries a no-investment-framing + odds-are-not-forecasts caution)

## Staged sources (registered, NOT yet surfaced — pending per-source license review)

These are present in the registry with `surfaced: false`. Under the fact-vs-propaganda
editorial line (Michael 2026-06-24), `conflict-events-acled`, `vessel-tracking-ais`, and
`military-flights-adsb` are **factual** EVENT/POSITION/TRACK channels — allowed on editorial
grounds (sensitivity is never a deny reason). They stay staged **on LICENSE grounds only**:
their upstream license is unknown (not in the free-to-use allowlist). Each is surfaceable the
moment a clean license is confirmed and a `CREDITS.md` line is added in the same PR.

## License

Split license — confirmed IQ #371 (A), 2026-06-10:

- **azimuth code:** MIT — see [`LICENSE`](LICENSE).
- **azimuth vault content (derived L1/L2/L3 notes under `vault/`):** CC BY 4.0 — see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).
