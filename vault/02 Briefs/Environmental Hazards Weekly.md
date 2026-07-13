---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W29
updated: 2026-07-13T18:30:00Z
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
> L1 note it rests on. (This cycle absorbs the 2026-07-06 through 2026-07-13 ingests after an
> 11-day curator gap. The wildfire note
> renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power**,
  **Russia** again led but eased to 225 of 250, with **Iran (15)** entering the strongest-fires
  subset alongside Turkey (5), Ukraine (3), Saudi Arabia (1) and Syria (1); the strongest fire
  eased to ~98 MW FRP (from ~226 MW) and none carried the feed's `possibleExplosion` flag (the
  full feed returns 1,022 detections; only the strongest 250 are rendered —
  [[wildfire-detections]]).
- The FIRMS thermal-escalation feed independently clustered the same window into **12
  escalation signals** — all twelve over Russia this cycle — and held a fully-heated status mix:
  **all 12 classed `SPIKE`** (0 elevated, 0 normal, 0 persistent), all 12 tagged
  `conflict-adjacent` by the feed's own geospatial layer and all 12 flagged high-relevance
  ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed narrowed to **16 active events** — 13 iceberg /
  sea-lake-ice tracks, **1 severe storm** (Tropical Cyclone BAVI-26, no wind speed carried in
  this pull), 1 volcano entry (the generic `Volcanoes` category, unnamed this cycle) and the
  Madagascar drought ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere it was measured: **11 observations**
  (10 US-EPA RadNet stations + 1 Safecast), **zero anomalies and zero elevated readings**, values
  spanning a routine 26–74 nSv/h ([[radiation-observations]]).

## Active fire — where the detections clustered

- Russia accounted for 225 of the 250 top-by-FRP detections this cycle — easing further from the
  prior pull's 244 — with Iran (15) the notable new entrant to the strongest-fires subset, ahead
  of Turkey (5), Ukraine (3), Saudi Arabia (1) and Syria (1). The peak fire radiative power eased
  to ~98 MW FRP (from ~226 MW), well below the ~565 MW peak seen earlier in the run
  ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most energetic
  fires — because the endpoint returns the full detection set (1,022 this pull) and ignores limit
  parameters; the cap is recorded in the note's own caption so the truncation is never silent, and
  the full set remains at the source endpoint. The country shares above therefore describe the
  strongest-fire subset, not the entire detection count ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters all resolved over Russia this cycle (the two Ukraine clusters
  of last week gone), and the status mix held fully heated — **all 12 classed `SPIKE`** against
  their own local baselines (none `elevated`, `normal` or `persistent`). The largest cluster
  carried 72 observations, a ~98 MW peak FRP and ~1,183 MW total FRP — smaller than the prior
  cycle's 341-observation / ~5,393 MW cluster — while the sharpest baseline departure was a
  Russian cluster at a z-score of 46.5 ([[thermal-escalations]]).
- The feed's own geospatial tagging again marked all 12 clusters `conflict-adjacent` and all 12
  high-relevance this cycle. azimuth reports those classifications as the observed feed output and
  takes no position on them — a thermal anomaly is a measured radiance, and the L2 line stops at
  what was detected, where, and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate narrowed to 16 active events this cycle: 13 iceberg /
  sea-lake-ice tracks (the Antarctic-iceberg series), a **single severe storm** — the storm count
  falling from five to one as only Tropical Cyclone BAVI-26 remained (no wind speed carried in
  this pull, where the prior cycle recorded 140 kt) — plus one volcano entry (the generic
  `Volcanoes` category, unnamed this cycle) and the Madagascar drought ([[natural-events]]).
- Every radiation reading in the window sat in the ordinary background band (26–74 nSv/h), with
  the EPA RadNet network and a single Safecast sensor reporting and the feed's anomaly and
  elevated counts both at zero — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The window's environmental-hazard picture stayed fire-led and held its heated status mix while
  the disaster slate cooled: all 12 thermal clusters classed `SPIKE`, all conflict-adjacent and
  high-relevance and all over Russia this cycle, while the strongest-fire subset stayed
  Russia-dominated (225 of 250) with Iran newly entering and peak radiative power easing to
  ~98 MW. The storm side of the disaster slate fell from five active systems to one (Tropical
  Cyclone BAVI-26) alongside the standing Antarctic-iceberg series, a single volcano entry and the
  Madagascar drought, while ambient radiation stayed entirely normal. azimuth records the
  detections, the cluster statuses, the alert categories and the sensor values, links each to its
  L1 note, and stops there — what the satellites and stations measured, not what may follow
  ([[wildfire-detections]], [[thermal-escalations]], [[natural-events]],
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
</content>
