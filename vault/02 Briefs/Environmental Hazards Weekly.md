---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W27
updated: 2026-06-30T13:20:00Z
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
> L1 note it rests on. (This cycle reads the live `2026-06-30` ingest. The wildfire note
> renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power**, the
  set was led entirely by **Russia** (all 250 of the rendered subset this cycle, up from ~74% a
  week earlier); the strongest fire reached ~262 MW FRP — firmer than last week's ~161 MW — and
  none carried the feed's `possibleExplosion` flag (the full feed returns several thousand
  detections; only the strongest 250 are rendered — [[wildfire-detections]]).
- The FIRMS thermal-escalation feed independently clustered the same window into **12
  escalation signals** — eleven over Russia and one over Ukraine — and heated back up this cycle:
  8 `SPIKE`, 1 `ELEVATED` and 3 `NORMAL` (0 persistent), with **all 12** tagged
  `conflict-adjacent` by the feed's own geospatial layer and 8 flagged high-relevance
  ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed listed **19 active events** — 14 iceberg / sea-lake-ice
  tracks, 2 severe storms (Tropical Storm Higos and Typhoon Mekkhala), 1 volcano (Nevados del
  Chillán, Chile), a Madagascar drought and a Philippines earthquake (the same M6.5 the seismic
  feed recorded WSW of Sarangani) ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere it was measured: **11
  observations** (10 US-EPA RadNet stations + 1 Safecast), **zero anomalies and zero
  elevated readings**, values spanning a routine 26–74 nSv/h across US cities
  ([[radiation-observations]]).

## Active fire — where the detections clustered

- Russia accounted for the entire rendered active-fire set this cycle — all 250 of the
  top-250-by-FRP detections, up from ~74% (184 of 250) a week earlier — with no Ukraine, Turkey
  or Syria detections in the strongest-fires subset this pull. The peak fire radiative power rose
  to ~262 MW FRP (from ~161 MW), still well below the ~565 MW peak seen two weeks earlier
  ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most
  energetic fires — because the endpoint returns the full multi-thousand-detection set and
  ignores limit parameters; the cap is recorded in the note's own caption so the truncation
  is never silent, and the full set remains at the source endpoint. The country shares above
  therefore describe the strongest-fire subset, not the entire detection count
  ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters resolved over Russia (11) and Ukraine (1), and the status
  mix heated back up this cycle — 8 classed `SPIKE`, 1 `ELEVATED` and 3 `NORMAL` against their
  own local baselines (none `persistent`) — firmer than the prior cycle's 3 spike / 3 elevated /
  6 normal. The largest cluster (in Russia) carried 31 observations and a ~89 MW peak FRP
  ([[thermal-escalations]]).
- The feed's own geospatial tagging marked all 12 clusters `conflict-adjacent` this cycle (up
  from 11 of 12); azimuth reports that classification as the observed feed output and takes no
  position on it — a thermal anomaly is a measured radiance, and the L2 line stops at what was
  detected, where, and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate held broad at 19 active events this cycle: 14 iceberg /
  sea-lake-ice tracks (the Antarctic-iceberg series), 2 severe storms (Tropical Storm Higos and
  Typhoon Mekkhala), 1 volcano (Nevados del Chillán, Chile), a Madagascar drought — and a
  Philippines earthquake, the cross-theme tie to the seismic record's M6.5 WSW of Sarangani (the
  tie moved from last cycle's Venezuela doublet as that aged toward the trailing edge)
  ([[natural-events]]).
- Every radiation reading in the window sat in the ordinary background band (26–74 nSv/h),
  with the EPA RadNet network and a single Safecast sensor reporting live and the feed's
  anomaly and elevated counts both at zero — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The window's environmental-hazard picture stayed fire-led and firmed up at the top: the
  strongest-fire subset concentrated entirely in Russia this cycle, peak radiative power rose to
  ~262 MW (from ~161 MW), and the 12 thermal clusters heated back up from a mixed status to 8
  spike / 1 elevated / 3 normal, all 12 now conflict-adjacent. The disaster slate held broad at
  19 events — Antarctic icebergs, two named storms, a Chilean volcano, the Madagascar drought
  and the Philippines earthquake tie — while ambient radiation stayed entirely normal. azimuth
  records the detections, the cluster statuses, the alert categories and the sensor values, links
  each to its L1 note, and stops there — what the satellites and stations measured, not what may
  follow ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
  [[radiation-observations]]).

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
- 2026-06-26 — daily-ingest flowback (2026-W26): refreshed from the live 2026-06-26 ingest. The
  active-fire top-250-by-FRP subset led with Russia (184) and Ukraine (50); peak FRP eased to
  ~161 MW (from ~565 MW) and the thermal-escalation clusters cooled from all-spike to a mixed 3
  spike / 3 elevated / 6 normal across Russia (8), Ukraine (3) and Turkey (1), 11 of 12 still
  conflict-adjacent. The GDACS/EONET slate broadened from 3 to 21 events (12 icebergs, 4
  volcanoes, 2 named storms, the Venezuela earthquakes, a Madagascar drought); radiation stayed
  normal (11 obs, 0 anomalies, 26–74 nSv/h). Dropped the prior pull's severity labels where the
  06-26 EONET feed carried none. Observed-only, no-political-position framing held
  ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
  [[radiation-observations]]).
- 2026-06-30 — daily-ingest flowback (2026-W27): refreshed from the live 2026-06-30 ingest. The
  active-fire top-250-by-FRP subset concentrated entirely in Russia (all 250, up from ~74%) and
  peak FRP firmed to ~262 MW (from ~161 MW). The thermal-escalation clusters heated back up to 8
  spike / 1 elevated / 3 normal across Russia (11) and Ukraine (1), all 12 now conflict-adjacent
  (from 11 of 12). The GDACS/EONET slate held at 19 events (14 icebergs, 2 named storms, the
  Nevados del Chillán volcano, a Madagascar drought and a Philippines earthquake — the
  cross-theme tie shifting from the aging Venezuela doublet to the M6.5 WSW of Sarangani);
  radiation stayed normal (11 obs, 0 anomalies, 26–74 nSv/h). Observed-only, no-political-position
  framing held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
  [[radiation-observations]]).
</content>
