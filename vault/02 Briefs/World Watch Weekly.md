---
title: World Watch Weekly
type: L2-brief
theme: cross-theme
week: 2026-W26
updated: 2026-06-23T04:00:00Z
sources: [crude-oil-inventories, earthquakes, energy-prices, fuel-prices, natural-gas-storage-eu]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# World Watch Weekly

> The **cross-theme** brief. azimuth's per-theme briefs synthesise WITHIN a channel — energy supply, geophysics. This one synthesises ACROSS them: it names the regions the week's open data records under more than one channel, and asks whether the connection actually *reaches* from one to the other. A static OKF bundle can store each theme's brief; it cannot draw the line between them. That line is what Emi's synthesis layer adds — and it is drawn from data, never invented: every region below literally appears in each channel's L1 source note (see `## How this brief is made`).

## This week at a glance

- The 2026-06-23 ingest connects **2 clean channels** (Energy Supply, Geophysical) through **3 shared region(s)**: Greece, Mexico, New Zealand ([[crude-oil-inventories]], [[earthquakes]], [[energy-prices]], [[fuel-prices]], [[natural-gas-storage-eu]]).
- None of the shared regions fall on the physical energy-supply core (US crude inventories, EU gas storage), so the week's recorded seismicity shows **no observed reach** into the tracked energy balances ([[crude-oil-inventories]], [[earthquakes]], [[energy-prices]], [[fuel-prices]], [[natural-gas-storage-eu]]).

## Shared entities across channels

- **Greece** is recorded under 2 channels this week (Energy Supply + Geophysical) — Energy Supply: diesel $2.021/L, +0.79% w/w; gasoline $2.330/L, -2.03% w/w ([[fuel-prices]]) | Geophysical: M5.2 10 km S of Kastrí, Greece; M4.9 20 km SE of Kastrí, Greece ([[earthquakes]]). The shared name is a co-occurrence in two open feeds, not a causal link unless the physical data shows reach.
- **Mexico** is recorded under 2 channels this week (Energy Supply + Geophysical) — Energy Supply: diesel $1.577/L, +1.37% w/w; gasoline $1.376/L, +1.63% w/w ([[fuel-prices]]) | Geophysical: M4.6 Off the coast of Baja California Sur, Mexico ([[earthquakes]]). The shared name is a co-occurrence in two open feeds, not a causal link unless the physical data shows reach.
- **New Zealand** is recorded under 2 channels this week (Energy Supply + Geophysical) — Energy Supply: fuel feed reported no price this week (listed under failedSources) ([[fuel-prices]]) | Geophysical: M5.1 Kermadec Islands, New Zealand; M4.5 32 km W of Titahi Bay, New Zealand ([[earthquakes]]). The shared name is a co-occurrence in two open feeds, not a causal link unless the physical data shows reach.

## Does the connection reach?

- The bridges above are **geographic co-occurrences** — the same place named in two open feeds. azimuth reports observed signal, not predicted harm, so a quake recorded near a fuel-reporting country is not read as a supply event unless the physical energy data itself moves ([[crude-oil-inventories]], [[earthquakes]], [[energy-prices]], [[fuel-prices]], [[natural-gas-storage-eu]]).
- This week the strong seismic clusters sit away from where the energy balances are measured, so the cross-theme verdict is a sourced **non-finding**: the channels share names but the data shows no reach between them ([[crude-oil-inventories]], [[earthquakes]], [[energy-prices]], [[fuel-prices]], [[natural-gas-storage-eu]]).

## How this brief is made

> Regenerated deterministically by `scripts/build_cross_theme.py` from the latest L1 ingest. Bridges are regions the live source notes mention under >=2 editorially-clean themes, scanned with the same fixed gazetteer the knowledge-graph uses for its gold cross-theme edges (`synthesis/cross_theme.py`). Held themes are excluded. The script can be re-run after any ingest; it evolves this note in place and keeps the changelog history. This is the living-system layer OKF's static format cannot produce.

## Changelog

- 2026-06-23 — regenerated from the 2026-06-23 L1 ingest (2026-W26): 3 cross-channel bridge(s) across 2 clean channels (Greece, Mexico, New Zealand); energy-core reach: none observed.
