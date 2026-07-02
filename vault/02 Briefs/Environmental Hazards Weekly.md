---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W27
updated: 2026-07-02T22:40:00Z
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
> L1 note it rests on. (This cycle reads the live `2026-07-02` ingest. The wildfire note
> renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power**,
  **Russia** again dominated with 244 of 250, with Ukraine (4) and Turkey (2) re-entering the
  strongest-fires subset after a cycle of Russia-only; the strongest fire reached ~226 MW FRP
  (easing from ~262 MW) and none carried the feed's `possibleExplosion` flag (the full feed
  returns several thousand detections; only the strongest 250 are rendered —
  [[wildfire-detections]]).
- The FIRMS thermal-escalation feed independently clustered the same window into **12
  escalation signals** — ten over Russia and two over Ukraine — and reached a fully-heated
  status mix: **all 12 classed `SPIKE`** (0 elevated, 0 normal, 0 persistent), all 12 tagged
  `conflict-adjacent` by the feed's own geospatial layer and all 12 flagged high-relevance;
  both Ukraine clusters carried the feed's `night_activity` flag ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed listed **21 active events** — 14 iceberg / sea-lake-ice
  tracks, **5 severe storms** (Tropical Cyclone BAVI-26 at a recorded 140 kt, Tropical Storm
  Douglas, Tropical Cyclone TEN-26, Tropical Storm Higos and Typhoon Mekkhala), 1 volcano
  (Nevados del Chillán, Chile) and the Madagascar drought ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere it was measured: **11
  observations** (10 US-EPA RadNet stations + 1 Safecast), **zero anomalies and zero
  elevated readings**, values spanning a routine 25–74 nSv/h
  ([[radiation-observations]]).

## Active fire — where the detections clustered

- Russia accounted for 244 of the 250 top-by-FRP detections this cycle — easing from the prior
  pull's clean sweep of all 250 — with Ukraine (4) and Turkey (2) re-entering the
  strongest-fires subset. The peak fire radiative power eased to ~226 MW FRP (from ~262 MW),
  still well below the ~565 MW peak seen earlier in the run ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most
  energetic fires — because the endpoint returns the full multi-thousand-detection set and
  ignores limit parameters; the cap is recorded in the note's own caption so the truncation
  is never silent, and the full set remains at the source endpoint. The country shares above
  therefore describe the strongest-fire subset, not the entire detection count
  ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters resolved over Russia (10) and Ukraine (2), and the status
  mix reached fully heated — **all 12 classed `SPIKE`** against their own local baselines (none
  `elevated`, `normal` or `persistent`) — up from the prior cycle's 8 spike / 1 elevated / 3
  normal. The largest cluster (in Russia) carried 341 observations, a ~132 MW
  peak FRP and ~5,393 MW total FRP; the sharpest baseline departure was a Russian cluster at a
  z-score of 3.86 ([[thermal-escalations]]).
- The feed's own geospatial tagging again marked all 12 clusters `conflict-adjacent` and all 12
  high-relevance this cycle; the two Ukraine clusters were the only ones carrying the
  `night_activity` flag (100% night detections). azimuth reports those classifications as the
  observed feed output and takes no position on them — a thermal anomaly is a measured
  radiance, and the L2 line stops at what was detected, where, and how hot
  ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate broadened to 21 active events this cycle: 14 iceberg /
  sea-lake-ice tracks (the Antarctic-iceberg series), **5 severe storms** — the storm count
  jumping from 2 as Tropical Cyclone BAVI-26 (a recorded 140 kt, the feed's red-alert band),
  Tropical Storm Douglas (35 kt, NHC) and Tropical Cyclone TEN-26 (40 kt) joined the running
  Tropical Storm Higos and Typhoon Mekkhala — plus the Nevados del Chillán volcano (Chile) and
  the Madagascar drought; the prior cycle's Philippines-earthquake entry left the slate
  ([[natural-events]]).
- Every radiation reading in the window sat in the ordinary background band (25–74 nSv/h),
  with the EPA RadNet network and a single Safecast sensor reporting and the feed's
  anomaly and elevated counts both at zero — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The window's environmental-hazard picture stayed fire-led and reached its most heated status
  mix yet: all 12 thermal clusters classed `SPIKE` (from 8/1/3), all conflict-adjacent and
  high-relevance, while the strongest-fire subset stayed Russia-dominated (244 of 250) with
  Ukraine and Turkey re-entering at the margin and peak radiative power easing to ~226 MW. The
  storm side of the disaster slate tripled to five active systems — led by Tropical Cyclone
  BAVI-26 at a recorded 140 kt — alongside the standing Antarctic-iceberg series, the Chilean
  volcano and the Madagascar drought, while ambient radiation stayed entirely normal. azimuth
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
- 2026-07-02 — weekly synthesis (2026-W27): absorbed the 2026-07-01 and 2026-07-02 ingest days.
  The active-fire top-250-by-FRP subset eased off the prior Russia-only sweep to Russia 244 /
  Ukraine 4 / Turkey 2, with peak FRP easing to ~226 MW (from ~262 MW). The thermal-escalation
  clusters reached a fully-heated mix — all 12 `SPIKE` (from 8/1/3) across Russia (10) and
  Ukraine (2), all conflict-adjacent and high-relevance, the Ukraine pair night-flagged, largest
  cluster 341 observations / ~5,393 MW total FRP. The GDACS/EONET slate broadened to 21 events
  as the storm count jumped to five (BAVI-26 at 140 kt red-alert band, Douglas, TEN-26, plus
  the running Higos and Mekkhala) and the Philippines-earthquake entry left; radiation stayed
  normal (11 obs, 0 anomalies, 25–74 nSv/h). Observed-only, no-political-position framing held
  ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
  [[radiation-observations]]).
</content>
