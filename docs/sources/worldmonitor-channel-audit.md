# WorldMonitor Channel Audit — full-universe surface decision (W26)

**Owner:** azimuth · **KR:** W26-Azimuth-USP · **Directive:** Michael 2026-06-24 — *"azimuth
should have ALL available and free-to-use channels from WorldMonitor."* · **Editorial line:**
[`vault/00 Rules/editorial.md`](../../vault/00%20Rules/editorial.md) — *facts in, opinions out*.

This audit enumerates the **full WorldMonitor channel universe** (pulled live from the
`koala73/worldmonitor` proto definitions + `docs/data-sources.mdx` provider list, 2026-06-24)
and applies the **two-part gate** to every channel:

1. **FACTUAL?** — does it monitor observed events / measurements / positions / records?
   (Forecasts, intelligence assessments and scenarios are *not* facts → benchmark foils, not channels.)
2. **FREE-TO-USE?** — is the upstream license public-domain / CC / API-ToS-permitted /
   non-commercial-with-attribution? (azimuth is a non-commercial demonstrator shipping `CREDITS.md`.)

A channel is **surfaced** iff it passes BOTH. **Sensitivity is never a deny reason** — a conflict
event, a vessel position, a sanctions designation are observed facts. A factual channel that fails
ONLY the license gate is **held-on-license** (never editorial).

## Headline

| | Before (W26 start) | After (this audit) |
|---|---|---|
| **Surfaced channels** | 9 | **26** (+17) |
| **Surfaced themes** | 4 | **12** |
| Held-on-license / filter / derived | 3 | 12 |
| Routed to benchmark (forecast/assessment/scenario) | — | 4 families |

Enforced by `guardrail/source_guardrail.py` (PASS at 26/38) + `tests/unit/test_source_guardrail.py`
+ `tests/unit/test_registry_themes.py`. Registry: [`sources/registry.json`](../../sources/registry.json).
Credits: [`CREDITS.md`](../../CREDITS.md).

## Full audit table

Verdict legend: **surfaced** · **held-on-license** (factual, license bar) · **held-on-filter**
(news per-source advocacy filter) · **held-derived** (WM analytic composite, not a raw feed) ·
**benchmark-only** (prediction/assessment/scenario → foil, not a channel) · **low-pri** (clean path
exists but narrowing needed).

| Channel (proto family) | Category | Upstream source | License | Factual? | Free? | Verdict |
|---|---|---|---|---|---|---|
| natural-gas-storage-eu | economic | GIE AGSI+ | CC-BY-4.0 | yes | yes | **surfaced** |
| crude-oil-inventories | economic | U.S. EIA | US-Gov-PD | yes | yes | **surfaced** |
| fuel-prices | economic | WM fuel-price feed | API-ToS | yes | yes | **surfaced** |
| energy-prices | economic | WM energy feed | API-ToS | yes | yes | **surfaced** |
| earthquakes | seismology | USGS | US-Gov-PD | yes | yes | **surfaced** |
| climate-anomalies | climate | Open-Meteo ERA5 / NOAA-NASA | CC-BY / US-Gov-PD | yes | yes | **surfaced** |
| co2-monitoring | climate | NOAA GML | US-Gov-PD | yes | yes | **surfaced** |
| sea-ice-extent | climate | NSIDC Sea Ice Index | US-Gov-PD | yes | yes | **surfaced** |
| prediction-markets | prediction | Polymarket (price quote only) | API-ToS | yes (price=fact) | yes | **surfaced** (brief held: breadth) |
| wildfire-detections | wildfire | NASA FIRMS (VIIRS) | US-Gov-PD | yes | yes | **surfaced** |
| thermal-escalations | thermal | NASA FIRMS (clustered) | US-Gov-PD | yes | yes | **surfaced** |
| natural-events | natural | NASA EONET + GDACS | US-Gov-PD / open | yes | yes | **surfaced** |
| radiation-observations | radiation | US EPA RadNet + Safecast | US-Gov-PD / CC0 | yes | yes | **surfaced** |
| conflict-events-ucdp | conflict | UCDP (Uppsala) | CC-BY-4.0 | yes | yes | **surfaced** |
| maritime-navwarnings | maritime | NGA navigational warnings | US-Gov-PD | yes | yes | **surfaced** |
| cyber-threats | cyber | abuse.ch (URLhaus/Feodo) | CC0-1.0 | yes | yes | **surfaced** |
| sanctions-designations | sanctions | US Treasury OFAC SDN/Consolidated | US-Gov-PD | yes | yes | **surfaced** |
| disease-outbreaks | health | WHO DON + US CDC HAN | WHO open / US-Gov-PD | yes | yes | **surfaced** |
| crypto-quotes | market | CoinGecko | API-ToS | yes (price=fact) | yes | **surfaced** |
| world-bank-indicators | economic | World Bank Open Data | CC-BY-4.0 | yes | yes | **surfaced** |
| tariff-trends | trade | WTO | CC-BY-4.0 | yes | yes | **surfaced** |
| orbital-satellites | intelligence (TLE) | CelesTrak (US SpaceCom catalog) | US-Gov-PD | yes (position) | yes | **surfaced** |
| consumer-prices | consumer_prices | Eurostat HICP | CC-BY-4.0 | yes | yes | **surfaced** |
| displacement-flows | displacement | UNHCR + UN OCHA HAPI | CC-BY-4.0 / open | yes | yes | **surfaced** |
| internet-outages | infrastructure | Cloudflare Radar | API-ToS | yes | yes | **surfaced** |
| chokepoint-status | supply_chain | IMF PortWatch | API-ToS (free) | yes | yes | **surfaced** |
| conflict-events-acled | conflict | ACLED | restricted ToU | yes | **no** (redistribution restricted) | **held-on-license** (UCDP is the surfaced clean path) |
| vessel-tracking-ais | maritime | AIS aggregators | commercial/unknown | yes (position) | **no** | **held-on-license** (navwarnings is the surfaced maritime path) |
| military-flights-adsb | military/aviation | ADS-B Exchange | restrictive/commercial | yes (track) | **no** | **held-on-license** |
| gps-interference | intelligence | gpsjam.org → ADS-B Exchange | unknown | yes | **no** | **held-on-license** |
| market-equities | market | Yahoo Finance | proprietary-fair-use | yes (price) | **no** | **held-on-license** (crypto is the surfaced market path) |
| bigmac-index | consumer_prices | The Economist | proprietary | yes | **no** | **held-on-license** |
| comtrade-flows | trade | UN Comtrade | redistribution-restricted | yes | **no** | **held-on-license** (WTO tariffs is the surfaced trade path) |
| webcam-streams | webcam | YouTube live streams | per-stream third-party | yes (frame) | **no** | **held-on-license** (low-pri) |
| satellite-imagery | imagery | mixed (Sentinel/Landsat free, commercial not) | mixed | yes | partial | **low-pri** (surface once narrowed to public-domain providers) |
| positive-events | positive_events | good-news RSS outlets | API-ToS | partly | n/a | **held-on-filter** (advocacy outlets fail the news fact-filter) |
| giving-index | giving | composite (annual reports + on-chain) | mixed | partly | n/a | **held-derived** (WM analytic composite, not a raw feed) |
| research-feeds | research | arXiv + HN + GitHub trending | mixed per-item | partly | partial | **low-pri** (surface once narrowed to CC0/CC-BY metadata) |
| forecast | forecast | WM forecast / simulation engine | n/a | **no** (prediction) | n/a | **benchmark-only** |
| intelligence (assessments) | intelligence | WM risk/regime/situation models | n/a | **no** (assessment) | n/a | **benchmark-only** |
| scenario | scenario | WM scenario templates / runs | n/a | **no** (hypothetical) | n/a | **benchmark-only** |
| resilience | resilience | WM resilience ranking/score | n/a | **no** (derived score) | n/a | **benchmark-only / derived** |
| leads | leads | contact-submission RPC | n/a | n/a (not a data feed) | n/a | **excluded** (not a channel) |

> Benchmark-only families (forecast / intelligence-assessment / scenario / resilience) are NOT
> azimuth channels — they are predictions / assessments / hypotheticals. They feed the
> facts-vs-forecast-vs-intelligence **benchmark** demonstrator
> (work-item `azi-benchmark-vs-forecast-intelligence-W26`,
> [`sources/benchmark/foils.json`](../../sources/benchmark/foils.json)), per the editorial line's
> "Not surfaced as channels" clause.

## Re-evaluation of the 3 previously-excluded channels (KR requirement)

Each was re-evaluated under the fact-vs-propaganda line. **All three are factual** — the hold is
**license only**, never editorial:

- **`conflict-events-acled`** — ACLED event records are factual. **Verdict: held-on-license.** ACLED's
  Terms of Use restrict redistribution of the event dataset and require a use agreement; that exceeds
  azimuth's free-to-use-with-attribution bar even for a non-commercial demonstrator. **The conflict
  topic is NOT dropped** — it is surfaced via **UCDP** (`conflict-events-ucdp`), whose Georeferenced
  Event Dataset is published under a clean **CC-BY-4.0** license.
- **`vessel-tracking-ais`** — vessel positions are factual. **Verdict: held-on-license** (AIS-aggregator
  feed is commercial/unknown). **The Maritime theme is NOT empty** — `maritime-navwarnings` (NGA
  navigational warnings, US-Gov public-domain) is surfaced.
- **`military-flights-adsb`** — flight tracks are factual. **Verdict: held-on-license** (ADS-B Exchange
  is restrictive/commercial; OpenSky is free-for-research but still restricts raw redistribution).

## Next steps

- **[fleet]** Wire L1 ingest for the newly-surfaced themes (curator's scheduled pull) so each held
  brief lands — the registry entries are license-cleared, attributed, and credited; only the first
  data pull is pending. Brief generation then runs through the existing `azimuth-curator` + synthesis lint.
- **[fleet]** When a clean license path appears (e.g. a public-domain AIS feed, an ACLED redistribution
  grant, OpenSky research-redistribution clarification), flip the corresponding held entry and add its
  `CREDITS.md` line in the same change.
- **[Michael]** Confirm whether UN Comtrade's CC BY-SA 3.0 IGO terms permit azimuth's derived
  re-surfacing — if yes, `comtrade-flows` flips from held to surfaced.
