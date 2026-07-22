---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W30
updated: 2026-07-22T09:00:00Z
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
> L1 note it rests on. (This cycle absorbs the 2026-07-18 through 2026-07-20 ingests. The wildfire
> note renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power** (of
  **4,592** in the endpoint), the feed's own per-detection region field attributes the subset
  **Russia 243 / Iran 5 / Ukraine 2** — exact country counts, not eyeballed from coordinates
  (0 rows unattributed) — the Russian detections falling across Siberia and the Far East, the
  most energetic at ~59°N 85°E and ~67°N 164°E — with **peak FRP firming to ~404 MW** (from
  ~282); zero `possibleExplosion` flags ([[wildfire-detections]]).
- The FIRMS thermal-escalation feed clustered the window into **12 signals, all over Russia**
  (from Russia 11 / Ukraine 1 the prior cycle), with status heating from **all-12-PERSISTENT
  back to all-12-SPIKE**; all 12 remain conflict-adjacent and high-relevance; the largest cluster
  reached **906 observations and 31,279 MW total FRP**; sharpest z-score 2.95
  ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed narrowed to **21 active events** (from 30): 13 iceberg /
  sea-lake-ice tracks, **3 tropical-cyclone entries** (Tropical Depression Two, Tropical Storm
  Fausto, Tropical Storm Elida) plus one further severe-storm entry, **3 drought entries**
  (Madagascar + Ethiopia/Kenya/Somalia + a multi-country European drought) and 1 earthquake
  (Peru); the prior cycle's US wildfire entries dropped off the slate ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere measured: **11 observations** (10
  US-EPA RadNet stations + 1 Safecast), up from 2 the prior cycle; **zero anomalies and zero
  elevated readings**, values 24–74.3 nSv/h ([[radiation-observations]]).

## Active fire — where the detections clustered

- The top-250-by-FRP subset attributes — by each detection's own `region` field, deterministically
  tallied — as **Russia 243 / Iran 5 / Ukraine 2** (0 unattributed); the Russian detections fall
  across Siberia and the Far East, the two strongest at ~59°N 85°E (404 MW) and ~67°N 164°E
  (179 MW). Peak FRP firmed to ~404 MW (from ~282 MW). The full endpoint returned 4,592 detections
  (near the prior 4,693), so the top-250 subset remains the strongest fires only; the per-country
  split above is exact for that strongest-fire subset, not the entire 4,592-detection set
  ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most energetic
  fires — because the endpoint returns the full detection set (4,592 this pull) and ignores
  limit parameters; the cap is recorded in the note's own caption so the truncation is never
  silent, and the full set remains at the source endpoint. The coordinates above describe the
  strongest-fire subset, not the entire detection count ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters all fell over **Russia** this cycle (from Russia 11 /
  Ukraine 1 the prior cycle), and the status mix heated: **all 12 now classed `SPIKE`** (from
  all-12-`PERSISTENT` the prior cycle; none elevated, normal or persistent). The largest cluster
  carried **906 observations and 31,279 MW total FRP** — a sharp jump from the prior 248 / 8,379;
  the sharpest baseline departure was a z-score of 2.95 across the 12 clusters
  ([[thermal-escalations]]).
- The feed's own geospatial tagging again marked all 12 clusters `conflict-adjacent` and all 12
  high-relevance this cycle. azimuth reports those classifications as the observed feed output and
  takes no position on them — a thermal anomaly is a measured radiance, and the L2 line stops at
  what was detected, where, and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate narrowed to **21 active events** (from 30 the prior cycle): 13
  iceberg / sea-lake-ice tracks (the Antarctic-iceberg series, unchanged); **3 tropical-cyclone
  entries** — Tropical Depression Two (Atlantic), Tropical Storm Fausto and Tropical Storm Elida
  (eastern Pacific), with one duplicate Elida title carried as a further severe-storm entry;
  **3 drought entries** — Madagascar, Ethiopia/Kenya/Somalia and a large multi-country European
  drought spanning Germany, France, Spain, Poland and others; and 1 earthquake entry (Peru). The
  prior cycle's 10 US wildfire entries dropped off the EONET slate this cycle ([[natural-events]]).
- Radiation observations rose from 2 (07-17) to **11 this pull** (10 US-EPA RadNet stations —
  Albany, Honolulu, Houston, Seattle, Chicago, Washington DC and others — plus 1 Safecast
  reading); all sat in the normal background band, the feed's anomaly, elevated and spike counts
  all at zero, and the value range was 24–74.3 nSv/h — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The 07-18→07-20 window saw movement across all four feeds. The strongest-fire subset stayed
  concentrated over Russia — the top-250 detection coordinates cluster in Siberian and Far-East
  boreal fires, peak FRP firming to ~404 MW while the full endpoint held near 4,592 detections
  ([[wildfire-detections]]). The thermal-escalation picture heated and re-consolidated: all 12
  clusters fell over Russia (from Russia 11 / Ukraine 1) and status moved from all-12-PERSISTENT
  back to all-12-SPIKE, the largest cluster jumping to 906 observations and 31,279 MW total FRP;
  all 12 remain conflict-adjacent and high-relevance ([[thermal-escalations]]). The disaster feed
  narrowed to 21 events as the prior cycle's US wildfire entries dropped off, leaving 13 iceberg
  tracks, three tropical cyclones (Fausto, Elida, Tropical Depression Two), three droughts and a
  Peru earthquake ([[natural-events]]). Radiation coverage widened back to 11 readings (from 2),
  all entirely normal ([[radiation-observations]]). azimuth records the detections, the cluster
  statuses, the alert categories and the sensor values, links each to its L1 note, and stops
  there — what the satellites and stations measured, not what may follow ([[wildfire-detections]],
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
