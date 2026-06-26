---
title: Environmental Hazards Weekly
type: L2-brief
theme: environmental-hazards
week: 2026-W26
updated: 2026-06-26T13:20:00Z
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
> L1 note it rests on. (This cycle reads the live `2026-06-26` ingest. The wildfire note
> renders the top 250 detections by fire radiative power, with the cap stated in the note
> caption, so the active-fire figures below describe that strongest-fires subset rather than
> the full multi-thousand-detection set — [[wildfire-detections]].)

## This week at a glance

- Among the NASA FIRMS VIIRS feed's **top 250 active-fire detections by radiative power**, the
  set was led by **Russia** (184 detections, ~74% of the rendered subset) and **Ukraine** (50),
  with small counts over Turkey (8), Syria (7) and a single Israel/Gaza detection; the strongest
  fire reached ~161 MW FRP and none carried the feed's `possibleExplosion` flag (the full feed
  returns several thousand detections; only the strongest 250 are rendered — [[wildfire-detections]]).
- The FIRMS thermal-escalation feed independently clustered the same window into **12
  escalation signals** — eight over Russia, three over Ukraine and one over Turkey — with a
  mixed status this cycle: 3 `SPIKE`, 3 `ELEVATED` and 6 `NORMAL` (0 persistent), and 11 of the
  12 tagged `conflict-adjacent` by the feed's own geospatial layer ([[thermal-escalations]]).
- The GDACS / NASA EONET disaster feed listed **21 active events** — 12 iceberg / sea-lake-ice
  tracks, 4 volcanoes, 2 severe storms (Tropical Storm Higos and Typhoon Mekkhala), the two
  Venezuela earthquakes (the same Yumare doublet the seismic feed recorded) and a Madagascar
  drought ([[natural-events]]).
- Ambient radiation stayed at normal background everywhere it was measured: **11
  observations** (10 US-EPA RadNet stations + 1 Safecast), **zero anomalies and zero
  elevated readings**, values spanning a routine 26–74 nSv/h across US cities
  ([[radiation-observations]]).

## Active fire — where the detections clustered

- Russia dominated the rendered active-fire set at ~74% of the top-250-by-FRP detections (184
  of 250), with Ukraine next at 50; the strongest fires by fire radiative power fell in Russia
  and peaked at ~161 MW FRP this cycle — well below the ~565 MW peak two weeks earlier. Turkey
  (8), Syria (7) and a single Israel/Gaza detection rounded out the rendered subset
  ([[wildfire-detections]]).
- azimuth caps this L1 note to the top 250 detections by FRP — the strongest, most
  energetic fires — because the endpoint returns the full multi-thousand-detection set and
  ignores limit parameters; the cap is recorded in the note's own caption so the truncation
  is never silent, and the full set remains at the source endpoint. The country shares above
  therefore describe the strongest-fire subset, not the entire detection count
  ([[wildfire-detections]]).

## Thermal escalations — the clustered signal

- The 12 thermal-escalation clusters resolved over Russia (8), Ukraine (3) and Turkey (1),
  with a mixed status this cycle — 3 classed `SPIKE`, 3 `ELEVATED` and 6 `NORMAL` against their
  own local baselines (none `persistent`) — a calmer picture than two weeks earlier when all 12
  were spikes. The largest cluster (in Russia) carried 81 observations and a ~161 MW peak FRP
  ([[thermal-escalations]]).
- The feed's own geospatial tagging marked 11 of the 12 clusters `conflict-adjacent`; azimuth
  reports that classification as the observed feed output and takes no position on it — a
  thermal anomaly is a measured radiance, and the L2 line stops at what was detected, where,
  and how hot ([[thermal-escalations]]).

## Disaster alerts and radiation

- The GDACS/EONET disaster slate broadened to 21 active events this cycle: 12 iceberg /
  sea-lake-ice tracks (the D33/A8x Antarctic-iceberg series), 4 volcanoes (including Nevados
  del Chillán, Chile), 2 severe storms (Tropical Storm Higos and Typhoon Mekkhala), the two
  Venezuela earthquakes — the cross-theme tie to the seismic record's Yumare M7.5/M7.2 doublet
  — and a Madagascar drought ([[natural-events]]).
- Every radiation reading in the window sat in the ordinary background band (26–74 nSv/h),
  with the EPA RadNet network and a single Safecast sensor reporting live and the feed's
  anomaly and elevated counts both at zero — nothing out of the ordinary was measured
  ([[radiation-observations]]).

## Reading the week

- The window's environmental-hazard picture stayed fire-led but eased at the top: the
  strongest-fire subset is still concentrated in Russia and Ukraine, but peak radiative power
  fell to ~161 MW (from ~565 MW two weeks earlier) and the 12 thermal clusters cooled from
  all-spike to a mixed 3 spike / 3 elevated / 6 normal. The disaster slate, by contrast,
  broadened to 21 events — Antarctic icebergs, volcanoes and two named storms alongside the
  Venezuela earthquakes and a Madagascar drought — while ambient radiation stayed entirely
  normal. azimuth records the detections, the cluster statuses, the alert categories and the
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
