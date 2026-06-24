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

**Climate Signals theme**

- `climate-anomalies` — NOAA/NASA reanalysis regional temperature & precipitation anomalies — US-Gov public domain (observed measurement; L2 reports recorded values, never a forecast)
- `co2-monitoring` — NOAA Global Monitoring Laboratory (atmospheric CO2 record) — US-Gov public domain (observed measurement; L2 reports recorded values, never a forecast)
- `sea-ice-extent` — NSIDC / NOAA@NSIDC Sea Ice Index (passive-microwave sea-ice extent) — US-Gov public domain (observed measurement; L2 reports recorded values, never a forecast)

**Prediction Markets theme**

- `prediction-markets` — Polymarket public odds via WorldMonitor — API-ToS-derived (raw odds surfaced as L1 data only; L2 carries a no-investment-framing + odds-are-not-forecasts caution)

**Environmental Hazards theme** (W26 full-universe audit)

- `wildfire-detections` — NASA FIRMS (VIIRS active-fire detections) — US-Gov public domain
- `thermal-escalations` — NASA FIRMS (VIIRS thermal anomalies, clustered) — US-Gov public domain
- `natural-events` — NASA EONET + GDACS (UN-coordinated disaster alerts) — US-Gov public domain (EONET) + open-with-attribution (GDACS)
- `radiation-observations` — US EPA RadNet (public domain) + Safecast (CC0) — free-to-use

**Conflict Watch theme** (W26)

- `conflict-events-ucdp` — UCDP (Uppsala Conflict Data Program) — CC-BY-4.0 (observed conflict-event records; L2 carries report-observed + no-political-position cautions)

**Maritime Safety theme** (W26)

- `maritime-navwarnings` — NGA (US National Geospatial-Intelligence Agency) Broadcast/Navigational Warnings — US-Gov public domain

**Cyber Watch theme** (W26)

- `cyber-threats` — abuse.ch (URLhaus + Feodo Tracker) — CC0-1.0 (observed IOC records)

**Sanctions Watch theme** (W26)

- `sanctions-designations` — US Treasury OFAC (SDN + Consolidated lists) — US-Gov public domain (official designation records; L2 carries report-observed + no-political-position cautions)

**Public Health theme** (W26)

- `disease-outbreaks` — WHO Disease Outbreak News + US CDC Health Alert Network — WHO open-data + US-Gov public domain

**Macro & Markets theme** (W26)

- `crypto-quotes` — CoinGecko (crypto spot prices) — API-ToS-derived (L2 carries no-investment-framing caution)
- `world-bank-indicators` — World Bank Open Data (development indicators) — CC-BY-4.0
- `tariff-trends` — WTO (applied tariffs & trade restrictions) — CC-BY-4.0
- `consumer-prices` — Eurostat HICP / national statistical offices — CC-BY-4.0

**Orbital Watch theme** (W26)

- `orbital-satellites` — CelesTrak TLE element sets (US Space Command public catalog) — US-Gov public domain

**Humanitarian theme** (W26)

- `displacement-flows` — UNHCR Refugee Data + UN OCHA HAPI — CC-BY-4.0 / open-with-attribution (observed refugee/IDP counts)

**Infrastructure Watch theme** (W26)

- `internet-outages` — Cloudflare Radar (internet outages & traffic anomalies) — API-ToS-derived
- `chokepoint-status` — IMF PortWatch (maritime chokepoint transit) — API-ToS-derived (free/open)

## Staged sources (registered, NOT yet surfaced — pending per-source license review)

These are present in the registry with `surfaced: false`, each carrying a `surfaced_reason`.
Under the fact-vs-propaganda editorial line (Michael 2026-06-24) they are **factual** channels
— so none is held on editorial grounds. The hold is **license** (or, for `positive-events`,
the news per-source fact-filter; for `giving-index`, derived-composite). Each becomes
surfaceable the moment a clean free-to-use license / clean source path is confirmed and a
`CREDITS.md` line is added in the same PR:

- `conflict-events-acled` — ACLED — held: ACLED ToU restricts redistribution (UCDP is the surfaced clean-licensed alternative).
- `vessel-tracking-ais` — AIS aggregators — held: AIS-aggregator license commercial/unknown (NGA navigational warnings are the surfaced clean maritime channel).
- `military-flights-adsb` / `gps-interference` — ADS-B Exchange — held: restrictive/commercial upstream license.
- `market-equities` — Yahoo Finance — held: proprietary-with-fair-use (crypto via CoinGecko is the surfaced clean market channel).
- `bigmac-index` — The Economist — held: proprietary index dataset.
- `comtrade-flows` — UN Comtrade — held: redistribution-restricted (WTO tariff-trends is the surfaced clean trade channel).
- `webcam-streams` — YouTube live streams — held: per-stream third-party licensing.
- `satellite-imagery` — mixed imagery providers — held: surfaceable once narrowed to Sentinel/Landsat public-domain only.
- `positive-events` — good-news RSS outlets — held: news per-source fact-filter (advocacy outlets, not wire/agency fact-reporting).
- `giving-index` — composite charitable-giving index — held: WorldMonitor-derived analytic composite, not a single raw observed feed.
- `research-feeds` — arXiv + HN + GitHub trending — held: mixed per-item licensing (low priority).

## License

Split license — confirmed IQ #371 (A), 2026-06-10:

- **azimuth code:** MIT — see [`LICENSE`](LICENSE).
- **azimuth vault content (derived L1/L2/L3 notes under `vault/`):** CC BY 4.0 — see [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).
