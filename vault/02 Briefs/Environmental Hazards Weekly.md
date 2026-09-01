---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W36
updated: 2026-09-02T09:44:00Z
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
> L1 note it rests on. (This cycle absorbs the 2026-09-01 ingest. The wildfire note renders the
> top 250 detections by fire radiative power, with the cap stated in the note caption, so the
> active-fire figures below describe that strongest-fires subset rather than the full detection
> set — [[wildfire-detections]].)

## This week at a glance

- The NASA FIRMS VIIRS feed's **top-250-by-FRP cap held flat at 250 detections**; the feed's own
  per-detection region field attributes the entire strongest-fire sample to **Russia 250 of 250**
  (from 246 of 250 on 08-31) — exact counts, not eyeballed from coordinates, and every one of the
  250 carried an **emergency flag** this pull. Intensity climbed again: the top-3 fire-radiative-
  power values rose to **~871 / 799 / 740 MW** (from ~768 / 711 / 710 on 08-31), the strongest
  detection at ~64.4N 114.7E in Siberia, against an upstream full detection set of **46,885**
  ([[wildfire-detections]]).
- The FIRMS thermal-escalation feed again clustered the window into **12 signals**, all 12
  `conflict_adjacent`, all 12 `THERMAL_RELEVANCE_HIGH` and all 12 attributed to **Russia**, but the
  status mix **flipped back to all 12 `THERMAL_STATUS_SPIKE`** (from all-12 `PERSISTENT` on 08-31)
  — a re-spiking heat signature, the sharpest cluster at a z-score of **15.3** and the largest at
  ~49,633 MW total FRP ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed's active-event count **jumped from 3 to 25**: 11 Sea and
  Lake Ice tracks, 7 severe-storm entries, 4 tropical cyclones — headlined by **Category-4 Major
  Hurricane Karina (East Pacific)**, with Tropical Storms Edouard (Atlantic), Marie (East Pacific)
  and Lowell (Central Pacific) — a Hong Kong tropical-cyclone warning, and 2 US wildfires (Oregon,
  Texas) — reported as the observed feed state ([[natural-events]]).
- Radiation stayed clean: **0 anomalies, 0 elevated readings, 0 spikes** across 4 EPA RadNet
  stations and 1 Safecast reading (1 low-confidence, 0 conflicting) ([[radiation-observations]]).

## Active fire — where the detections clustered

- The top-250-by-FRP sample attributes — by each detection's own `region` field, deterministically
  tallied — as **Russia 250 of 250** on the 09-01 pull, up from **Russia 246 of 250** on 08-31, so
  the strongest-fire sample is now entirely Siberian/Far-East Russian. The detection count itself
  stayed capped/flat at 250, and the intensity signal climbed further: the top-3 FRP values rose to
  **~871 / 799 / 740 MW** (from ~768 / 711 / 710 on 08-31), with **all 250 detections carrying an
  emergency flag** and the strongest at ~64.4N 114.7E. The upstream full detection set stands at
  **46,885** — far larger than the capped subset — as the Siberian fire season drives the dominant
  signal ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most energetic
  fires — because the endpoint returns a full detection set that dwarfs the capped subset and
  ignores limit parameters; the cap is recorded in the note's own caption so the truncation is
  never silent. The country split and FRP figures above are exact for that strongest-fire subset,
  not the full underlying detection set ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The feed again clustered the window into **12 thermal-escalation signals** on the 09-01 pull,
  matching the 08-31 count. All 12 clusters carried `conflict_adjacent`, all 12
  `THERMAL_RELEVANCE_HIGH` and all 12 an explicit **`countryName` of Russia** this pull — that
  composition held steady. What moved was the status mix: the 08-31 pull had been **all 12
  `THERMAL_STATUS_PERSISTENT`**, and the 09-01 pull **flipped back to all 12
  `THERMAL_STATUS_SPIKE`** (spikeCount 12, persistentCount 0) — the escalation clusters returned to
  a spiking signature, the sharpest at a **z-score of 15.3** and the largest at ~**49,633 MW total
  FRP** ([[thermal-escalations]]).
- azimuth reports that persistent-to-spike status shift as the observed feed output and takes no
  position on it — a thermal cluster is a measured radiance aggregate, and the L2 line stops at
  what was detected, when, and how the signal classified, not what it implies about the ground
  situation. The clusters stayed 12/12 conflict-adjacent and 12/12 high-relevance throughout, only
  the SPIKE/PERSISTENT classification changed ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate's active-event count **jumped from 3 to 25** between the 08-31 and
  09-01 pulls. The 09-01 slate carries 11 Sea and Lake Ice tracks, 7 severe-storm entries, 4
  tropical cyclones — **Category-4 Major Hurricane Karina (East Pacific)** the headline, with
  Tropical Storms Edouard (Atlantic), Marie (East Pacific) and Lowell (Central Pacific) — a Hong
  Kong tropical-cyclone warning, and 2 US wildfire events (Ruggs, Oregon; Harris, Texas). azimuth
  records the count and category slate as the observed feed state, taking no position on any of it
  ([[natural-events]]).
- Radiation stayed clean: **0 anomalies, 0 elevated readings, 0 spikes** across 4 EPA RadNet
  stations and 1 Safecast reading (1 low-confidence, 0 conflicting) on the 09-01 pull
  ([[radiation-observations]]).

## Reading the week

- The 2026-09-01 pull shows the strongest-fire sample tightening to an all-Russia shape while
  intensity climbed again: the top-250-by-FRP cap held flat at 250 detections, Russia's share rose
  to **250 of 250** (from 246), the top-3 FRP values rose to **~871 / 799 / 740 MW** (from
  ~768 / 711 / 710), and **all 250 detections carried an emergency flag**, the strongest at ~64.4N
  114.7E against an upstream set of 46,885 ([[wildfire-detections]]). The thermal-escalation
  picture held its 12-cluster, 12/12-conflict-adjacent, 12/12-high-relevance, 12/12-Russia shape but
  flipped classification back — from **all-12 `THERMAL_STATUS_PERSISTENT`** on 08-31 to **all-12
  `THERMAL_STATUS_SPIKE`** on 09-01 (sharpest z 15.3, largest ~49,633 MW total FRP), a re-spiking
  heat signature ([[thermal-escalations]]). The disaster slate's active-event count **jumped from 3
  to 25**: 11 Sea and Lake Ice tracks, 7 severe storms, 4 tropical cyclones led by Category-4 Major
  Hurricane Karina (East Pacific) with Tropical Storms Edouard/Marie/Lowell, a Hong Kong
  tropical-cyclone warning and 2 US wildfires ([[natural-events]]). The radiation picture stayed
  clean: 0 anomalies, 0 elevated readings and 0 spikes across 4 EPA RadNet stations and 1 Safecast
  reading ([[radiation-observations]]). azimuth records the detections, the cluster statuses,
  the alert categories and the sensor values, links each to its L1 note, and stops there — what
  the satellites and stations measured, not what may follow ([[wildfire-detections]],
  [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).

## Changelog

- 2026-09-02 — daily-ingest synthesis (2026-W36): absorbed the 2026-09-01 ingest. Active-fire top-250 cap held flat at 250, Russia's share rose 246 → 250 of 250 (all 250 emergency-flagged), top-3 FRP ~871 / 799 / 740 MW (from ~768 / 711 / 710), strongest at ~64.4N 114.7E, upstream full set 46,885. Thermal clusters held 12/12 conflict-adjacent, 12/12 high-relevance and 12/12 Russia but flipped status back from all-12 PERSISTENT (08-31) to all-12 SPIKE (09-01), sharpest z 15.3, largest ~49,633 MW total FRP. Natural events jumped 3 → 25: 11 Sea and Lake Ice, 7 severe storms, 4 tropical cyclones (Cat-4 Major Hurricane Karina EP the headline, TS Edouard/Marie/Lowell), a Hong Kong TC warning, 2 US wildfires (Oregon, Texas). Radiation stayed clean: 0 anomalies / 0 elevated / 0 spikes across 4 EPA + 1 Safecast reading. Rewrote the intro, at-a-glance, active-fire, thermal, disaster/radiation and reading sections. Observed-only + editorial framing held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-08-31 — daily-ingest synthesis (2026-W36): absorbed the 2026-08-21 through 2026-08-31 ingests after an 11-day curator gap; active-fire top-250 cap held flat at 250 detections on both 08-20 and 08-31, Russia's share easing slightly (247 of 250 → 246 of 250), while top-5 FRP jumped ~117/117/117/96/96 MW → ~768/711/710/633/627 MW, the strongest 08-31 detection carrying an emergency flag in Russia (Siberia, ~64.3N 112.4E). Thermal clusters held 12/12 conflict-adjacent and 12/12 high-relevance but flipped status from all-12 SPIKE (08-20) to all-12 PERSISTENT (08-31). Natural events rose from 1 to 3 active entries: a Category-3 tropical cyclone (Central Pacific) gave way to a Category-4 tropical cyclone (East Pacific), a tropical storm (Central Pacific) and a tropical-cyclone warning. Radiation stayed clean both pulls: 0 anomalies, 0 elevated, 0 spikes. Observed-only framing held; editorial line held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-08-20 — daily-ingest synthesis (2026-W34): absorbed the 2026-08-18 through 08-20 ingests. Active-fire top-250 held Russia 247 / Ukraine 3 (0 unattributed, Iran leaving) as the full endpoint eased to 3,297 (from 4,147); max FRP in the capped set eased to 117.37 MW (from 182.18), 0 explosion flags. Thermal clusters re-heated from the 8-SPIKE/2-ELEVATED/1-PERSISTENT/1-NORMAL mix back to all-12-SPIKE, conflict_adjacent and high-relevance both back to 12/12 (from 11/12 and 8/12) as the British Columbia wildland cluster dropped off; no country field on the clusters this pull; largest cluster ~540.6 MW / 58 obs (from ~684.6 MW / 50 obs), sharpest z-score eased to 8.03 (from 11.39). Natural events contracted sharply from 19 to 1 — Major Hurricane Lala (re-graded up from Tropical Storm) the sole entry as the 13 Sea and Lake Ice tracks and five other storms dropped off the 08-20 pull. Radiation cleared its anomaly pair: anomalyCount 0 (from 2) as Philadelphia and Houston returned to normal, 11 readings 27.0–74.3 nSv/h. Observed-only framing held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-08-17 — daily-ingest synthesis (2026-W34): refreshed from the live 2026-08-17 ingest (also
  folds in the 2026-08-16 window, which held Russia 240 / Ukraine 7 / Iran 3 on a 2,360-detection
  endpoint, 152.8 MW max FRP, 11 SPIKE / 1 PERSISTENT thermal clusters, 21 open natural events and
  0 radiation anomalies, but was never separately logged here). Active-fire top-250 firmed to
  Russia 246 / Ukraine 3 / Iran 1 (0 unattributed) as the full endpoint rose to 4,147 (from 2,360);
  max FRP firmed to 182.18 MW (from 152.8), 0 explosion flags. Thermal clusters broadened from an
  11-SPIKE/1-PERSISTENT split to 8 SPIKE / 2 ELEVATED / 1 PERSISTENT / 1 NORMAL as a new British
  Columbia cluster entered under THERMAL_CONTEXT_WILDLAND (conflict_adjacent eased to 11/12,
  high-relevance to 8/12), over Ukraine 6 / Russia 5 / British Columbia 1; largest cluster
  ~684.6 MW / 50 obs (from ~635 MW / 8 obs), sharpest z-score firmed to 11.39 (from 6.93). Natural
  events eased from 21 to 19 (13 Sea and Lake Ice unchanged, storm entries from 8 to 6) as
  Tropical Storm 15W and Tropical Cyclone Chan-Hom cleared. Radiation logged its first anomaly
  pair since 2026-08-01: Philadelphia 59 nSv/h SPIKE (zScore 7.53) and Houston 40 nSv/h ELEVATED
  (zScore 2.0), 11 readings ranging 25.0–74.3 nSv/h. Observed-only framing held
  ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
  [[radiation-observations]]).
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
- 2026-07-13 — weekly synthesis (2026-W29): absorbed the 2026-07-06 through 2026-07-13 ingest
  days after an 11-day curator gap. The active-fire top-250-by-FRP subset eased further to Russia
  225 / Iran 15 / Turkey 5 / Ukraine 3 (Iran a new entrant), and peak FRP eased to ~98 MW (from
  ~226 MW) with 0 explosion flags across a 1,022-detection feed. The thermal-escalation clusters
  held a fully-heated all-12-`SPIKE` mix but resolved entirely over Russia this cycle (the two
  Ukraine clusters gone), all conflict-adjacent and high-relevance, largest cluster 72
  observations / ~1,183 MW total FRP, sharpest z-score 46.5. The GDACS/EONET slate narrowed to 16
  events as the storm count fell from five to one (only BAVI-26, no wind speed this pull) with 13
  iceberg tracks, one unnamed volcano entry and the Madagascar drought; radiation stayed normal
  (11 obs, 0 anomalies, 26–74 nSv/h). Observed-only, no-political-position framing held
  ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-07-15 — daily-ingest flowback (2026-W29): absorbed the 2026-07-14 and 2026-07-15 ingests.
  The strongest-fire subset re-concentrated on Russia (231 of 250, from 225) with Ukraine rising
  to 11, Taiwan (3) and North Korea (1) entering, Turkey easing to 2 and Iran (15) leaving; peak
  FRP firmed to ~148 MW (from ~98) on a smaller full set (802 detections, from 1,022). The
  thermal-escalation clusters split Ukraine 6 / Russia 5 / Syria 1 (from all-12-Russia) while
  holding all-12-`SPIKE`, all conflict-adjacent and high-relevance, the Ukraine clusters
  night-flagged; largest cluster 93 obs / ~1,324 MW total FRP, sharpest z 7.1. The GDACS/EONET
  slate broadened to 20 events: three severe-storm entries (Super Typhoon Bavi + a Category 5
  BAVI-26 track + Tropical Depression Five-E), two wildfire entries, one flood, 13 iceberg tracks
  and the Madagascar drought. Radiation stayed normal (11 obs, 0 anomalies, 27–74 nSv/h).
  Observed-only, no-political-position framing held ([[wildfire-detections]],
  [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): absorbed the 2026-07-16 and 2026-07-17 ingests. Active-fire top-250 diversified: Russia eased from 246 to 143; Iran entered at 46, Saudi Arabia and Turkey each at 19, Ukraine rose to 13, Syria 9, Israel/Gaza 1; max FRP eased to ~282 MW; full endpoint jumped from 793 to 4,693 detections. Thermal clusters shifted to Russia 11 / Ukraine 1 (from Ukraine 7 / Russia 5) and status moved from all-12-SPIKE to all-12-PERSISTENT; largest cluster 248 obs / 8,379 MW total FRP, max z-score 4.69. Natural events grew from 20 to 30: wildfire entries surged from 1 to 10 (US fires), drought entries rose to 3, Mayon volcano added, iceberg series held at 13 tracks, severe storms fell to 2. Radiation observations narrowed from 11 to 2 (Houston EPA + Fukushima Safecast), all normal, 36–74.3 nSv/h ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 ingests. Active-fire top-250 stayed concentrated over Russia (Siberia/Far East by detection coordinates), peak FRP firming to ~404 MW on a 4,592-detection full set. Thermal clusters re-consolidated to all-12-Russia and heated from all-12-PERSISTENT back to all-12-SPIKE, all conflict-adjacent and high-relevance, largest cluster 906 obs / 31,279 MW total FRP, sharpest z 2.95. Natural events narrowed from 30 to 21 as the US wildfire entries dropped off — 13 iceberg tracks, 3 tropical cyclones (Fausto, Elida, TD Two), 3 droughts, 1 Peru earthquake. Radiation widened back to 11 observations (10 EPA + 1 Safecast), all normal, 24–74.3 nSv/h ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-07-22 — attribution fix (IQ #1161): the active-fire top-250 country split is now stated as **exact per-country counts** (Russia 243 / Iran 5 / Ukraine 2, 0 unattributed) read from each detection's own `region` field (deterministic tally, `synthesis/fire_geo.country_tally`), replacing the eyeballed-from-coordinates "almost entirely Russia"; the FIRMS feed already ships `region` on every row, so no coordinate reverse-geocode is needed ([[wildfire-detections]]).
- 2026-07-23 — daily-ingest synthesis (2026-W30): active-fire top-250 sample re-concentrated to Russia 250/250 (from 243/5/2) on a smaller full set of 3,747 detections (from 4,592); Siberian fire season dominant. Thermal clusters held all-12-Russia all-SPIKE, FRP distribution shifted from one 31,279 MW dominant cluster to two large clusters at ~24,449 MW and ~20,905 MW (795 and 785 obs), sharpest z-score 32.08. Natural events held at 21 but composition shifted: Peru earthquake and named-cyclone trio replaced by 2 Tropical Cyclone entries (one Atlantic tropical storm, one East Pacific hurricane), 3 Severe Storms, 13 Sea and Lake Ice, 3 droughts (Madagascar, Horn of Africa, Europe-wide ~25 countries). Radiation anomaly cleared: anomalyCount and elevatedCount both 0 (from 1/1 prior cycle); all 11 readings normal 27–74.3 nSv/h ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-07-24 — daily-ingest synthesis (2026-W30): active-fire top-250 held Russia 250/250 (carried) while the full endpoint grew to 6,774 (from 3,747); max FRP in the capped set 637 MW. Thermal clusters held all-12-Russia all-SPIKE with a major FRP step-up: largest cluster ~67,948 MW / 1,764 obs (from ~24,449 MW / 795 obs prior), sharpest z-score 98.87 (from 32.08). Natural events grew from 21 to 26: 6 Severe Storm entries (Bertha TD+TS, Fausto Hurricane x2, Elida TS, NOUL-26 Cat 1), 4 US wildfire entries (Oregon/Washington/Texas/Louisiana), 13 Sea and Lake Ice, 3 droughts. Radiation anomaly re-appeared: anomalyCount 1 / elevatedCount 1 — Anchorage EPA 33 nSv/h (ELEVATED, zScore 2.21), after clearing in the prior cycle; 10 other readings normal 26–74.3 nSv/h ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-07-25 — daily-ingest synthesis (2026-W30): active-fire top-250 attributed Russia 249 / Iran 1 (from Russia 250/250, one Iran detection entering) as the full endpoint eased to 4,286 (from 6,774); max FRP in the capped set firmed to 740 MW (from 637). Thermal clusters held the 12-cluster all-SPIKE all-conflict-adjacent shape but the FRP magnitude eased sharply: largest ~19,555 MW / 761 obs (from ~67,948 MW / 1,764 obs), sharpest z-score 3.39 (from 98.87); the feed carried no country field on the clusters this pull. Natural events eased from 26 to 22: 7 Severe Storm entries (Fausto x2, Bertha, Elida, Genevieve, Noul, a Hong Kong Tropical Cyclone Warning Signal), 2 US wildfire entries (Oregon, Washington — down from 4 as Texas and Louisiana dropped off), 13 Sea and Lake Ice; the three drought entries (Madagascar, Horn of Africa, Europe) all cleared. Radiation anomaly cleared again: anomalyCount and elevatedCount both 0 (from 1/1), 10 readings normal 27–74.3 nSv/h. Observed-only, no-political-position framing held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
- 2026-08-01 — daily-ingest synthesis (2026-W31): absorbed the 07-31 and 08-01 ingests. Active-fire top-250 swept back to Russia 250 / 250 (from Russia 241 / Turkey 9 — the Turkey cluster leaving) as the full endpoint jumped to 16,033 (from 5,929); max FRP in the capped set firmed to 698.3 MW (from 326.7), 0 explosion flags. Thermal clusters held the 12-cluster all-conflict-adjacent all-high-relevance shape but the status mix eased from all-12-SPIKE to 9 SPIKE / 3 PERSISTENT over Russia 11 / Ukraine 1 (from Russia 10 / Ukraine 2); FRP magnitude stepped up, largest cluster ~2,157 MW / 82 obs (from ~792 MW / 63 obs), next ~1,690 MW and ~1,568 MW, sharpest z-score 2.00 (from 5.38). Natural events eased from 18 to 17: 13 Sea and Lake Ice, 4 severe-storm entries (Genevieve as one Tropical Storm + one Hurricane track, Super Typhoon Dolphin, Hurricane Fausto); Typhoon Noul cleared. Radiation stayed clear: anomalyCount and elevatedCount both 0, 11 readings normal 26.0–74.3 nSv/h. Observed-only, no-political-position framing held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]). Active-fire top-250 attributed Russia 241 / Turkey 9 (from Russia 249 / Iran 1 — Turkey entering, Iran leaving) as the full endpoint grew to 5,929 (from 4,286); max FRP in the capped set eased to 326.7 MW (from 740), 0 explosion flags. Thermal clusters held the 12-cluster all-SPIKE all-conflict-adjacent all-high-relevance shape and carried a country field again — Russia 10 / Ukraine 2 (the 07-25 pull carried none); FRP magnitude collapsed, largest cluster ~792 MW / 63 obs (from ~19,555 MW / 761 obs), next ~226 MW and ~224 MW, sharpest z-score 5.38 (from 3.39). Natural events eased from 22 to 18: 13 Sea and Lake Ice, 5 severe-storm entries (Hurricane Genevieve x2, Super Typhoon Dolphin, Typhoon Noul, Hurricane Fausto); the 2 US wildfire entries (Oregon, Washington) and the Hong Kong tropical-cyclone-warning cleared. Radiation stayed clear: anomalyCount and elevatedCount both 0, 11 readings normal 27.0–74.3 nSv/h. Observed-only, no-political-position framing held ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).
