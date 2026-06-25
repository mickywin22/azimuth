---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W26
updated: 2026-06-25T13:20:00Z
sources: [wildfire-detections, thermal-escalations, natural-events, radiation-observations]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Environmental Hazards Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **observed**
> environmental hazards — active-fire detections, clustered thermal anomalies, disaster
> alerts and ambient-radiation readings — what the instruments recorded, never what will
> happen, and never a position on any conflict the data sits near. Every claim links to the
> L1 note it rests on. (This is the theme's first cycle, reading the live `2026-06-25`
> ingest. NASA FIRMS active-fire detections were re-added to azimuth this week once the L1
> ingest gained a payload-size cap; the wildfire note now renders the top 250 detections by
> fire radiative power, with the cap stated in the note caption — [[wildfire-detections]].)

## This week at a glance

- The NASA FIRMS VIIRS feed recorded **10,213 active-fire detections** in the 2026-06-25
  ingest, overwhelmingly concentrated in **Russia** (9,639 detections, ~94% of the set),
  with smaller counts over Ukraine (192), Iran (176), Turkey (100) and Syria (82); none of
  the detections carried the feed's `possibleExplosion` flag ([[wildfire-detections]]).
- The FIRMS thermal-escalation feed independently clustered the same window into **12
  escalation signals, all 12 in Russia**, every one tagged `THERMAL_STATUS_SPIKE` at high
  strategic relevance — a spike-led, not persistent, picture (0 persistent, 0 elevated)
  over a 24-hour observation window ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed listed **three active events** — an orange-level
  drought in Madagascar and two red-level earthquakes in Venezuela — the latter the same
  Yumare doublet the seismic feed recorded the same day ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere it was measured: **11
  observations** (10 US-EPA RadNet stations + 1 Safecast), **zero anomalies and zero
  elevated readings**, values spanning a routine 28–68 nSv/h across US cities
  ([[radiation-observations]]).

## Active fire — where the detections clustered

- Russia dominated the active-fire set at ~94% of all detections, the strongest fires by
  fire radiative power all falling in Russia (top detections at ~565 MW FRP); the next-largest
  national counts — Ukraine, Iran, Turkey and Syria — together made up only a few hundred of
  the 10,213 detections ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most
  energetic fires — because the endpoint returns the full multi-thousand-detection set and
  ignores limit parameters; the cap is recorded in the note's own caption so the truncation
  is never silent, and the full set remains at the source endpoint ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- All 12 thermal-escalation clusters resolved over Russian territory, each classed a spike
  against its own local baseline, with the largest cluster reaching ~565 MW peak FRP and one
  central-Siberian cluster (near 59.0°N 90.9°E, Krasnoyarsk Krai) carrying 612 individual
  observations in the window ([[thermal-escalations]]).
- The feed's own geospatial tagging marked all 12 clusters `conflict-adjacent`; azimuth
  reports that classification as the observed feed output and takes no position on it — a
  thermal anomaly is a measured radiance, and the L2 line stops at what was detected, where,
  and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The three GDACS/EONET disaster events were a Madagascar drought (orange severity) and the
  two Venezuela earthquakes (red severity) on 2026-06-24 — the cross-theme tie to the
  seismic record, where the same Yumare M7.5/M7.2 doublet was the week's headline
  ([[natural-events]]).
- Every radiation reading in the window sat in the ordinary background band (28–68 nSv/h),
  with the EPA RadNet network and a single Safecast sensor reporting live and the feed's
  anomaly and elevated counts both at zero — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The window's environmental-hazard picture is fire-dominated and geographically lopsided:
  a very large active-fire count concentrated in Russia, echoed by 12 spike-status thermal
  clusters in the same country, against a quiet disaster slate (one drought, two
  earthquakes already covered by the seismic feed) and entirely normal ambient radiation.
  azimuth records the detections, the cluster statuses, the alert levels and the sensor
  values, links each to its L1 note, and stops there — what the satellites and stations
  measured, not what may follow ([[wildfire-detections]], [[thermal-escalations]],
  [[natural-events]], [[radiation-observations]]).

## Changelog

- 2026-06-25 — first Environmental Hazards Weekly cycle. Written from the live 2026-06-25
  ingest across all four theme channels: NASA FIRMS active-fire detections (10,213, ~94%
  Russia, max ~565 MW FRP — re-added this week after the L1 ingest gained a top-N-by-FRP
  payload cap), FIRMS thermal escalations (12 Russia spike clusters, all high-relevance),
  GDACS/EONET natural events (Madagascar drought + Venezuela earthquake doublet) and EPA
  RadNet + Safecast radiation (11 obs, 0 anomalies, normal 28–68 nSv/h). Observed-only and
  no-political-position framing held throughout; the theme's held brief is now live
  ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
  [[radiation-observations]]).
