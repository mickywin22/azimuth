---
title: Top5 Answers
type: L2-brief
theme: cross-theme
week: 2026-W27
updated: 2026-07-02T04:00:00Z
sources: [climate-anomalies, co2-monitoring, crude-oil-inventories, earthquakes, energy-prices, fuel-prices, natural-events, natural-gas-storage-eu, radiation-observations, sea-ice-extent, thermal-escalations, wildfire-detections]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Ask the World Data — azimuth's TOP5

> These are the five cross-source questions azimuth answers from **live** open data. A static feed (or a static OKF bundle) can store each channel; it cannot answer a question that crosses them. Every answer below connects **>=2 channels**, links **every factual claim to its L1 source note**, and names the **use-case** it serves. Regenerated each weekly cycle by `scripts/build_answers.py` — the *living* answer is the USP, not the format.

## Q1 — Is Europe's energy supply getting safer or more fragile right now?

> **Channels:** EU gas storage + US crude inventories + Energy prices · **Serves:** Energy / policy desk — a one-glance supply-health read across the physical balances and the price tape.

- **Verdict — the data leans well-supplied, not fragile.** Storage is filling and spot crude eased, while the multi-week US crude draw is the single signal to watch; azimuth states what the feeds show, not a safety call ([[natural-gas-storage-eu]], [[crude-oil-inventories]], [[energy-prices]])
- **EU gas storage is building** — 2,835 Bcf as of 2026-06-19, +76 Bcf week-on-week, extending the injection run to 8 straight weeks ([[natural-gas-storage-eu]])
- **US crude inventories drew down** -9,311 (EIA week of 2026-06-26) to 734,014 — the 8th straight weekly draw, the one tightening signal in the picture ([[crude-oil-inventories]])
- **Spot crude eased** this week — WTI $73.59/bbl (-9.6), Brent $73.63/bbl (-9.1) on the reported week-on-week change, so the price tape is not signalling scarcity ([[energy-prices]])

## Q2 — Did supply or demand move energy prices this week?

> **Channels:** US crude inventories + Energy prices · **Serves:** Economist / market analyst — separating a supply story from a demand story without a paywalled terminal.

- **Verdict — demand, not supply, set the tape.** Inventories tightened yet prices fell: the bearish price move overrode a bullish supply signal, so the week's driver was softer demand expectations, read straight off the two feeds ([[crude-oil-inventories]], [[energy-prices]])
- **Supply side:** US crude stocks tightened — -9,311 week of 2026-06-26. A draw normally argues for FIRMER prices ([[crude-oil-inventories]])
- **Price side:** WTI $73.59/bbl fell (-9.6 reported w/w) — the actual tape, against what the inventory draw implied ([[energy-prices]])

## Q3 — Did any major earthquake this week put energy infrastructure or population centres at risk?

> **Channels:** Geophysical + Energy supply · **Serves:** Risk & humanitarian desk — a fast, non-alarmist read of whether a seismic week actually touched the energy map.

- **Largest recorded event:** M6.5 34 km WSW of Sarangani, Philippines — one of 37 events at or above M5 USGS logged this week ([[earthquakes]])
- **No observed reach into energy infrastructure.** The week's quakes cluster away from the physical energy-supply core (US crude inventories, EU gas storage) and from the fuel-reporting countries — the data shows seismicity and the energy balances did not intersect this week ([[earthquakes]], [[crude-oil-inventories]])
- azimuth reports what USGS RECORDED, never what may happen next — a sourced 'no significant overlap' is the honest, efficient answer when that is what the week's data shows ([[earthquakes]])

## Q4 — What is the single biggest shift in the world's open data this week — and what does it connect to?

> **Channels:** Energy + Climate signals · **Serves:** Journalist / newsroom editor — the lede plus its connective tissue, ranked by a transparent rule, not vibes.

- **Biggest move: WTI Crude Oil, -11.5% week-on-week** — the largest swing across the quantitative energy series this week ([[energy-prices]])
- **What it connects to:** the move sits inside the inventories-vs-price loop — US crude drew down while spot prices eased, so the headline swing reflects demand-side repricing rippling from the spot tape into the physical balances and on to pump prices ([[crude-oil-inventories]], [[energy-prices]], [[fuel-prices]])
- **The slow-moving record:** atmospheric CO2 stands at 430.48 ppm (Mauna Loa, 2.86 ppm/yr) — not a weekly 'shift' but the baseline every energy story is told against; the demonstrator flags it as a different time-scale, not the week's headline ([[co2-monitoring]])

## Q5 — Show me everything that connects a given region or commodity across the data.

> **Channels:** Energy supply + Geophysical + Climate signals · **Serves:** Researcher / analyst — the cross-channel graph for one subject, every edge clickable to its L1 note.

- **Commodity spine — crude oil ties three feeds together:** the physical balance (-9,311 EIA stocks, 2026-06-26); the spot price (WTI $73.59/bbl); the pump (downstream fuel-price panel). One commodity, traced from the ground to the pump across separate L1 feeds ([[crude-oil-inventories]], [[energy-prices]], [[fuel-prices]])
- **United States** surfaces under 2 channels this week (Energy supply + environmental-hazards) — a co-occurrence in the open data, reported as a link, not a cause ([[crude-oil-inventories]], [[energy-prices]], [[fuel-prices]], [[natural-events]], [[natural-gas-storage-eu]], [[radiation-observations]], [[thermal-escalations]], [[wildfire-detections]])
- **New Zealand** surfaces under 2 channels this week (Energy supply + Geophysical) — a co-occurrence in the open data, reported as a link, not a cause ([[crude-oil-inventories]], [[earthquakes]], [[energy-prices]], [[fuel-prices]], [[natural-gas-storage-eu]])
- **Ukraine** surfaces under 2 channels this week (Climate signals + environmental-hazards) — a co-occurrence in the open data, reported as a link, not a cause ([[climate-anomalies]], [[co2-monitoring]], [[natural-events]], [[radiation-observations]], [[sea-ice-extent]], [[thermal-escalations]], [[wildfire-detections]])
- **Mexico** surfaces under 2 channels this week (Energy supply + Geophysical) — a co-occurrence in the open data, reported as a link, not a cause ([[crude-oil-inventories]], [[earthquakes]], [[energy-prices]], [[fuel-prices]], [[natural-gas-storage-eu]])

## How these answers are made

> Generated deterministically by `synthesis/answers.py` from the live L1 bundle (the latest dated note per editorially-clean source key — held themes excluded). Numbers are read straight from the source notes; nothing is invented. Re-run after any ingest and the answers refresh in place. This is the living-system layer a static format cannot produce.

## Changelog

- 2026-06-24 — regenerated TOP5 demonstrator answers from the 2026-06-24 live bundle (2026-W26); 5 cross-channel answers, every claim L1-sourced.
- 2026-06-25 — regenerated TOP5 demonstrator answers from the 2026-06-25 live bundle (2026-W26); 5 cross-channel answers, every claim L1-sourced.
- 2026-06-26 — regenerated TOP5 demonstrator answers from the 2026-06-26 live bundle (2026-W26); 5 cross-channel answers, every claim L1-sourced.
- 2026-06-30 — regenerated TOP5 demonstrator answers from the 2026-06-30 live bundle (2026-W27); 5 cross-channel answers, every claim L1-sourced.
- 2026-07-02 — regenerated TOP5 demonstrator answers from the 2026-07-02 live bundle (2026-W27); 5 cross-channel answers, every claim L1-sourced.
