---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W28
updated: 2026-07-10T12:00:00Z
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
> L1 note it rests on. (This cycle reads the live `2026-07-10` ingest. The wildfire note
> renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- The strongest-fires subset broadened out of its Russia-only shape: among the NASA FIRMS VIIRS
  feed's **top 250 active-fire detections by radiative power**, Russia fell to 145 of 250 as
  **Iran surged to 81** and Turkey (13), Saudi Arabia (6), Syria (4) and Ukraine (1) filled the
  rest — a Russia-plus-Middle-East mix where the prior cycle was 244 Russia; the peak fire
  strengthened to ~472 MW FRP (from ~226 MW) and none carried the feed's `possibleExplosion`
  flag ([[wildfire-detections]]).
- The FIRMS thermal-escalation feed clustered the window into **12 escalation signals — all 12
  over Russia** (Ukraine dropped out) — and the status mix cooled from last week's all-`SPIKE` to
  **all 12 `PERSISTENT`** (0 spike, 0 elevated): sustained multi-day Siberian complexes rather
  than sudden flares, all 12 still tagged `conflict-adjacent` and high-relevance by the feed's own
  geospatial layer, the largest carrying ~17,306 MW total FRP and a ~1,050 MW peak
  ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed broadened to **31 active events** and, for the first time,
  carried major **land wildfires** — Forest fires in France (6,576 ha) and Portugal (19,670 ha)
  plus ten US incidents (California, Oregon, Washington, Texas and Minnesota) — alongside 14
  iceberg tracks, a new China flood, the Nevados del Chillán volcano (Chile), the Madagascar
  drought and a single, weakening tropical system ([[natural-events]]).
- Ambient radiation stayed in the ordinary background band: **11 observations** (10 US-EPA RadNet
  stations + 1 Safecast), values spanning a routine 26–74 nSv/h, with **one reading (Honolulu,
  29 nSv/h) carrying the feed's `ELEVATED` flag** on a z-score of 2.34 against its low local
  baseline — an above-baseline blip, not an absolute high — and zero spikes
  ([[radiation-observations]]).

## Active fire — where the detections clustered

- The top-250-by-FRP subset shifted from Russia-only to a Russia-plus-Middle-East spread this
  cycle: Russia 145, **Iran 81**, Turkey 13, Saudi Arabia 6, Syria 4 and Ukraine 1 — the Iranian
  surge the week's clearest new signal, where the prior pull was 244 Russia / 4 Ukraine / 2
  Turkey. The peak fire radiative power firmed to ~472 MW FRP (from ~226 MW), and 30 of the 250
  strongest detections were night-time ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most
  energetic fires — because the endpoint returns the full multi-thousand-detection set and
  ignores limit parameters; the cap is recorded in the note's own caption so the truncation
  is never silent, and the full set remains at the source endpoint. The country shares above
  therefore describe the strongest-fire subset, not the entire detection count
  ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters this cycle resolved **entirely over Russia** (Ukraine, which
  carried two clusters last week, dropped out), and the status mix cooled from last week's fully-
  heated all-`SPIKE` to **all 12 `PERSISTENT`** — sustained signals with persistence times of
  ~26–32 hours rather than sudden spikes. The largest cluster (Siberia, ~59 °N 87 °E) carried 543
  observations, a ~1,050 MW peak FRP and ~17,306 MW total FRP; the sharpest baseline departure was
  a Russian cluster at a z-score of 2.7 ([[thermal-escalations]]).
- The feed's own geospatial tagging again marked all 12 clusters `conflict-adjacent` and all 12
  high-relevance this cycle, and three carried the `night_activity` flag. These centroids sit in
  the Siberian taiga (Krasnoyarsk and Sakha), where the annual boreal fire season runs;
  azimuth reports the feed's classifications as its observed output and takes no position on them
  — a thermal anomaly is a measured radiance, and the L2 line stops at what was detected, where,
  and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate broadened to 31 active events, and the composition shifted from
  storm-led to **fire-led on the ground**: 12 wildfire entries — Forest fires in France (6,576 ha,
  GDACS orange) and Portugal (19,670 ha, orange) plus ten US IRWIN incidents (the California VAN
  fire at 1,107 acres, Oregon's Whiskey fire ~999 acres, Washington, Texas and several Minnesota
  prescribed burns) — alongside 14 Antarctic iceberg tracks, a new **Flood in China** (GDACS
  orange), the Nevados del Chillán volcano (Chile) and the standing Madagascar drought. The storm
  side collapsed to a single system: **Tropical Cyclone BAVI-26** (GDACS red-alert, recorded at
  64 kt / Category 1) — the same storm the JTWC lists as "Super Typhoon Bavi" at 75 kt — down
  from last week's five active systems and much weaker than its 140 kt peak ([[natural-events]]).
- Every radiation reading in the window sat in the ordinary background band (26–74 nSv/h), with
  the EPA RadNet network and a single Safecast sensor reporting; the feed's anomaly and elevated
  counts each read one this cycle — a single Honolulu reading at 29 nSv/h flagged `ELEVATED` on a
  z-score of 2.34 against its 27.1 nSv/h local baseline. azimuth reports the flag honestly: it is
  an above-local-baseline blip on a low absolute value, not an elevated dose, and no spike was
  measured ([[radiation-observations]]).

## Reading the week

- The window's environmental-hazard picture turned decisively fire-led and, this cycle, its fire
  signal triangulated across three independent feeds: the FIRMS top-FRP detections broadened to a
  Russia-plus-Middle-East mix (Russia 145 / Iran 81 / Turkey, Saudi Arabia, Syria) with the peak
  firming to ~472 MW; the FIRMS thermal clusters concentrated entirely over Russia and shifted
  from sudden `SPIKE` to sustained `PERSISTENT` (peak cluster ~17,306 MW total FRP); and the
  GDACS/EONET disaster slate carried, for the first time, major land wildfires in France, Portugal
  and the US West — the Northern-Hemisphere summer fire season showing up on all three channels at
  once. Meanwhile the tropical-storm side collapsed to one weakening system (BAVI-26) and ambient
  radiation stayed in the ordinary band (one z-score `ELEVATED` blip at Honolulu, absolute value
  normal). azimuth records the detections, the cluster statuses, the alert categories and the
  sensor values, links each to its L1 note, and stops there — what the satellites and stations
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
- 2026-07-10 — weekly synthesis (2026-W28): absorbed the week's ingest to the live 2026-07-10
  day — a fire-led cycle that triangulated across three feeds. The active-fire top-250-by-FRP
  subset broadened from Russia-only to a Russia-plus-Middle-East mix (Russia 145, Iran 81, Turkey
  13, Saudi Arabia 6, Syria 4, Ukraine 1), peak FRP firming to ~472 MW. The thermal-escalation
  clusters concentrated entirely over Russia (Ukraine dropped out) and cooled from all-`SPIKE` to
  all-`PERSISTENT` (12/12), the largest ~17,306 MW total FRP / ~1,050 MW peak, all
  conflict-adjacent and high-relevance. The GDACS/EONET slate broadened to 31 events and carried
  major land wildfires for the first time (France 6,576 ha, Portugal 19,670 ha, ten US incidents),
  a new China flood, the standing icebergs/volcano/drought, and a storm side collapsed to one
  weakening system (BAVI-26, 64 kt GDACS / 75 kt JTWC, from five systems). Radiation stayed in the
  ordinary band with one z-score `ELEVATED` blip (Honolulu 29 nSv/h). Rewrote the at-a-glance,
  active-fire, thermal, disaster/radiation and reading sections around the broadened fire signal;
  observed-only, no-political-position framing held ([[wildfire-detections]],
  [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
</content>
