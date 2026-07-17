---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W29
updated: 2026-07-18T09:00:00Z
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
> L1 note it rests on. (This cycle absorbs the 2026-07-16 and 2026-07-17 ingests. The wildfire
> note renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power** (of
  4,693 in the endpoint), **Russia** led at 143 of 250 (down from 246), with **Iran at 46**,
  Saudi Arabia and Turkey each at 19, **Ukraine rising to 13** (from 4), Syria at 9, and
  Israel/Gaza at 1; peak FRP eased to ~282 MW (from ~327 MW); zero `possibleExplosion` flags
  ([[wildfire-detections]]).
- The FIRMS thermal-escalation feed clustered the window into **12 signals — Russia 11, Ukraine
  1** (shifted from Ukraine 7 / Russia 5 the prior day), with status cooling from
  **all-12-SPIKE to all-12-PERSISTENT**; all 12 remain conflict-adjacent and high-relevance;
  largest cluster reached 285 observations and 8,379 MW total FRP; sharpest z-score 4.69
  ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed grew to **30 active events** (from 20): 13 iceberg /
  sea-lake-ice tracks, **10 wildfire entries** (US fires dominating, up from 1), **3 drought
  entries** (Madagascar + Ethiopia/Kenya/Somalia + a multi-country European drought), 2 severe
  storms (*Tropical Storm Elida* × 2 — a duplicate title in the feed — down from 3), 1 flood
  (China), and 1 volcano (Mayon eruption) ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere measured: **2 observations** (1
  US-EPA RadNet station — Houston — + 1 Safecast — Fukushima, historical freshness), down from
  11 the prior day; **zero anomalies and zero elevated readings**, values 36–74.3 nSv/h
  ([[radiation-observations]]).

## Active fire — where the detections clustered

- Russia led the top-250-by-FRP subset at 143 detections (down sharply from 246 the prior day),
  with Iran at 46 (new entrant), Saudi Arabia and Turkey each at 19, Ukraine rising to 13 (from
  4), Syria at 9, and Israel/Gaza at 1; peak FRP eased to ~282 MW (from ~327 MW). The full
  endpoint returned 4,693 detections (up from 793 the prior pull), indicating a substantially
  broader detection sweep — the top-250 subset remains the strongest fires only
  ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most energetic
  fires — because the endpoint returns the full detection set (4,693 this pull) and ignores
  limit parameters; the cap is recorded in the note's own caption so the truncation is never
  silent, and the full set remains at the source endpoint. The country shares above describe the
  strongest-fire subset, not the entire detection count ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters again all fell over Russia and Ukraine, but the geography
  shifted to **Russia 11, Ukraine 1** (from Ukraine 7 / Russia 5 the prior day), and the status
  mix changed: **all 12 now classed `PERSISTENT`** (from all-12-`SPIKE` the prior day; none
  elevated, normal or spike). The largest cluster (Russia, near ~59°N / 91°E) carried 248
  observations and 8,379 MW total FRP; the sharpest baseline departure was a z-score of 4.69;
  persistence hours ranged from ~20 to ~30 hours across the 12 clusters
  ([[thermal-escalations]]).
- The feed's own geospatial tagging again marked all 12 clusters `conflict-adjacent` and all 12
  high-relevance this cycle. azimuth reports those classifications as the observed feed output and
  takes no position on them — a thermal anomaly is a measured radiance, and the L2 line stops at
  what was detected, where, and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate expanded to **30 active events** (from 20 the prior day): 13
  iceberg / sea-lake-ice tracks (the Antarctic-iceberg series, unchanged); **10 wildfire
  entries** — a significant rise from 1 — dominated by US fires in Oregon, Florida and Minnesota
  (titles as carried by the feed: HOPKIN, CROSSWHITE, COVE CREEK, PORCUPINE RIDGE, THORN,
  Charger 2, BUCKET SHOP (53)~, and Little Knife), plus a prescribed burn; **3 drought entries**
  — Madagascar, Ethiopia/Kenya/Somalia and a large multi-country European drought spanning
  Germany, France, Spain and others; 2 severe-storm entries (*Tropical Storm Elida* listed twice
  in the feed); 1 flood (China); 1 volcano (Mayon eruption) ([[natural-events]]).
- Radiation observations fell from 11 (07-16) to **2 this pull** (1 US-EPA RadNet — Houston,
  Texas — and 1 Safecast historical reading — Fukushima, Japan); both sat in the normal
  background band, the feed's anomaly, elevated and spike counts all at zero, and the value
  range was 36–74.3 nSv/h — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The 07-16→07-17 window saw movement across all four feeds. The strongest-fire subset
  diversified sharply: Russia's dominance eased from 246 to 143 detections while Iran (46),
  Saudi Arabia (19), Turkey (19), Syria (9) and Ukraine (13) all registered in the top 250; the
  full endpoint count jumped from 793 to 4,693 detections, suggesting a broad detection sweep
  ([[wildfire-detections]]). The thermal-escalation picture shifted: geography swung to Russia 11
  / Ukraine 1 (from Ukraine 7 / Russia 5), and cluster status moved from all-12-SPIKE to
  all-12-PERSISTENT, with the largest cluster at 248 observations and 8,379 MW total FRP;
  all 12 remain conflict-adjacent and high-relevance ([[thermal-escalations]]). The disaster
  feed grew substantially to 30 events, driven by a rise in wildfire entries from 1 to 10 (US
  fires) and the addition of two further drought entries and a volcano, while the iceberg series
  held at 13 tracks ([[natural-events]]). Radiation coverage narrowed to 2 readings (from 11),
  both entirely normal ([[radiation-observations]]). azimuth records the detections, the cluster
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
