---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W30
updated: 2026-07-24T09:00:00Z
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
> L1 note it rests on. (This cycle absorbs the 2026-07-24 ingest. The wildfire
> note renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power** (of
  **6,774** total in the endpoint), the feed's own per-detection region field attributes the
  sample entirely to **Russia (250/250)** — exact count, not eyeballed from coordinates (0 rows
  unattributed); the full endpoint grew from 3,747 to 6,774 detections, and the strongest-fire
  subset remains all-Russia; max FRP in the capped set reached 637 MW
  ([[wildfire-detections]]).
- The FIRMS thermal-escalation feed clustered the 2026-07-24 window into **12 signals, all over
  Russia** (all-12-Russia, unchanged pattern); all 12 carry status `THERMAL_STATUS_SPIKE` and
  `THERMAL_RELEVANCE_HIGH`; the largest cluster reached **~67,948 MW total FRP** (1,764
  observations, centroid ~66.8°N 164.4°E), the second **~42,380 MW** (863 observations); sharpest
  z-score 98.87 ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed showed **26 open events** (up from 21): 13 Sea and Lake Ice
  entries, **6 Severe Storm entries** (Tropical Depression Bertha, Tropical Storm Bertha, Hurricane
  Fausto × 2 source entries, Tropical Storm Elida, Category 1 NOUL-26), **4 wildfire entries** (US
  fires in Oregon, Washington, Texas, Louisiana), plus drought entries for Madagascar,
  Ethiopia/Kenya/Somalia (Horn of Africa), and a Europe-wide drought ([[natural-events]]).
- Radiation: **anomalyCount 1, elevatedCount 1** — Anchorage EPA RadNet 33 nSv/h (baseline 31,
  zScore 2.21, `RADIATION_SEVERITY_ELEVATED`) — a single elevated reading returned after clearing
  in the 07-23 pull; all other 10 readings normal; **11 observations** (10 US-EPA RadNet + 1
  Safecast, Fukushima), value range 26–74.3 nSv/h ([[radiation-observations]]).

## Active fire — where the detections clustered

- The top-250-by-FRP sample attributes — by each detection's own `region` field, deterministically
  tallied — as **Russia 250/250** (0 unattributed); the full endpoint returned **6,774 detections**
  (pagination.totalCount), up from 3,747 the prior cycle. The 250-row surfaced subset is entirely
  Russia, the feed's own `region` field on every row; max FRP in the capped set reached 637 MW.
  The Siberian fire season drives the dominant signal across Siberia and the Far East
  ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most energetic
  fires — because the endpoint returns the full detection set (6,774 this pull) and ignores
  limit parameters; the cap is recorded in the note's own caption so the truncation is never
  silent, and the full set remains at the source endpoint. The country split above is exact for
  that strongest-fire subset, not the entire 6,774-detection set ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters all fell over **Russia** this cycle (all-12-Russia again);
  all 12 carry status `THERMAL_STATUS_SPIKE` and `THERMAL_RELEVANCE_HIGH`. The largest cluster
  recorded **~67,948 MW total FRP** (1,764 observations, centroid ~66.8°N 164.4°E, maxBrightness
  367 K, z-score 3.58), followed by **~42,380 MW** (863 observations, centroid ~68.4°N 156.6°E)
  and **~35,358 MW** (719 observations, centroid ~68.6°N 156.9°E); a major step up in FRP
  magnitude from the prior cycle's two-cluster distribution (~24,449 MW and ~20,905 MW). The
  sharpest z-score across the 12 was **98.87** (cluster ~68.5°N 155.6°E, 243 observations,
  ~29,637 MW total FRP) ([[thermal-escalations]]).
- The feed's own narrativeFlags on all 12 clusters are `[conflict_adjacent, spike, multi_source]`
  (five clusters additionally carry `above_baseline`). azimuth reports those flag values as the
  observed feed output and takes no position on them — a thermal cluster is a measured radiance
  aggregate, and the L2 line stops at what was detected, where, and how hot
  ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate grew to **26 open events** (from 21 the prior cycle): 13 Sea
  and Lake Ice entries; **6 Severe Storm entries** — Tropical Depression Bertha, Tropical Storm
  Bertha (same storm, two source entries), Hurricane Fausto (two source entries), Tropical Storm
  Elida, and Category 1 NOUL-26; **4 wildfire entries** — US fires in Oregon (Ten Mile,
  Jefferson County), Washington (Railroad, Grant County), Texas (Gypsum Creek, King County), and
  Louisiana (West Blue Crab, Cameron County); and **3 drought entries** — Madagascar,
  Ethiopia/Kenya/Somalia (Horn of Africa), and a Europe-wide drought ([[natural-events]]).
- Radiation observations this pull: **11 readings** (10 US-EPA RadNet stations — Houston,
  Philadelphia, Boston, San Francisco, Albany, Anchorage, Honolulu, Chicago, Seattle, Washington
  DC — plus 1 Safecast reading, Fukushima, Japan). The feed's **anomalyCount returned to 1,
  elevatedCount 1** — Anchorage EPA RadNet at 33 nSv/h (baseline 31, zScore 2.21,
  `RADIATION_SEVERITY_ELEVATED`); spikeCount 0, conflictingCount 0. The value range across all 11
  readings was 26–74.3 nSv/h. The single elevated reading at Anchorage re-appeared after clearing
  in the 07-23 pull ([[radiation-observations]]).

## Reading the week

- The 2026-07-24 pull shows the Russian Siberian fire season still the sole signal in the
  strongest-fire sample: the top-250-by-FRP detections remain attributed entirely to Russia by the
  feed's own `region` field (250/250, unchanged from 07-23), while the full endpoint grew markedly
  to **6,774 detections** (from 3,747), and peak FRP in the capped set reached 637 MW
  ([[wildfire-detections]]). The thermal-escalation picture held its all-Russia, all-SPIKE shape,
  but the FRP magnitude scaled up substantially: 12 clusters, all carrying the feed's
  narrativeFlags `[conflict_adjacent, spike, multi_source]`, the largest now recording **~67,948
  MW total FRP** (1,764 observations) — nearly three times the prior cycle's largest (~24,449 MW /
  795 observations) — followed by ~42,380 MW and ~35,358 MW; sharpest z-score 98.87 (vs 32.08
  prior) ([[thermal-escalations]]). The disaster slate expanded from 21 to **26 events** — 13 Sea
  and Lake Ice, 6 Severe Storm entries (Bertha, Fausto, Elida, NOUL-26), 4 US wildfire entries
  (Oregon, Washington, Texas, Louisiana), and three drought entries (Madagascar, Horn of Africa,
  Europe-wide) ([[natural-events]]). The radiation picture reversed: anomalyCount and elevatedCount
  returned to 1 — Anchorage EPA RadNet reported 33 nSv/h (`RADIATION_SEVERITY_ELEVATED`, zScore
  2.21), re-appearing after clearing in the 07-23 pull; all other 10 readings at normal background
  26–74.3 nSv/h ([[radiation-observations]]). azimuth records the detections, the cluster statuses,
  the alert categories and the sensor values, links each to its L1 note, and stops there — what the
  satellites and stations measured, not what may follow ([[wildfire-detections]],
  [[thermal-escalations]], [[natural-events]], [[radiation-observations]]).

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
