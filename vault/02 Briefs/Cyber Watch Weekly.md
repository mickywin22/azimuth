---
title: Cyber Watch Weekly
type: L2-brief
theme: cyber-watch
week: 2026-W30
updated: 2026-07-22T09:00:00Z
sources: [cyber-threats]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Cyber Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded cyber
> threat indicators** — an IOC is an observed fact (a host, an IP, a first-seen timestamp,
> a severity as the tracker scored it) — and never attributes intent, names a victim, or
> predicts an attack. Every claim links to the L1 note it rests on. (First cycle written
> from the 2026-07-15 ingest; absorbed 07-16 and 07-17 on 2026-07-18.)

## This week at a glance

- The abuse.ch / AbuseIPDB channel again surfaced **one critical-severity indicator on the
  2026-07-22 pull** — the one-indicator critical tier the feed has shown on every pull this run
  ([[cyber-threats]]).
- **2026-07-22 pull:** one malware-host IP geolocated to the **United States** (US),
  `172.96.182.111`, AbuseIPDB confidence score 100, criticality CRITICAL, no malware family
  tagged; feed pagination totalCount **1,019** ([[cyber-threats]]).
- The curated critical tier's totalCount **rebuilt** across this cycle — **1,004** on the 07-20
  pull, **1,009** on 07-21, **1,019** on 07-22 — recovering roughly 15 indicators after the prior
  window's net retirement, the count drifting inside a narrow ~1,000–1,030 band all run
  ([[cyber-threats]]).

## Honest scope

- **This brief reports what the feed lists — currently a one-indicator critical tier.** The
  upstream trackers (URLhaus, Feodo Tracker, AbuseIPDB) publish far larger raw sets; the
  WorldMonitor channel curates to the top severity band. As the channel widens, this brief
  widens with it — the same honest-scope posture applied since the first cycle
  ([[cyber-threats]]).
- **Country field is geolocation of the indicator IP, not attribution of an actor.** The
  source records only an IP address and its geolocation; azimuth makes no inference beyond
  that ([[cyber-threats]]).

## Reading the week

- The 2026-07-22 indicator is a CYBER_THREAT_TYPE_MALWARE_HOST entry sourced from AbuseIPDB at
  maximum confidence (score:100, CRITICALITY_LEVEL_CRITICAL); the malwareFamily field is empty,
  so no specific malware family was tagged by the tracker at pull time ([[cyber-threats]]).
- The geolocation stayed in the **United States** a second cycle (07-22, after 165.22.1.254 on
  07-20), following Romania (07-17) and Russia (07-15/07-16). This is a single-indicator
  observation; the feed's curated critical tier is too narrow to draw a pattern from a day-to-day
  change in origin country ([[cyber-threats]]).
- azimuth records the indicator, its type, severity and geolocation exactly as the tracker
  scored them, and infers no actor, victim or campaign behind the one listed host
  ([[cyber-threats]]).

## Changelog

- 2026-07-22 — daily-ingest synthesis (2026-W30): absorbed the 07-21 and 07-22 pulls; the 07-22 pull lists one critical malware-host IP geolocated to the US (172.96.182.111, AbuseIPDB score 100, CRITICAL, no malware family); totalCount rebuilt 1,004 (07-20) → 1,009 (07-21) → 1,019 (07-22), recovering ~15 indicators after the prior retirement; US geolocation held a second cycle. Updated the at-a-glance and reading sections ([[cyber-threats]]).
- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 pulls; the 07-20 pull lists one critical malware-host IP geolocated to the US (165.22.1.254, AbuseIPDB score 100, CRITICAL, no malware family); totalCount eased from 1,021 (07-17) to 1,004 (07-20), a net ~17-indicator retirement; origin country moved to the US after RO (07-17) and RU (07-15/16) ([[cyber-threats]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): absorbed 07-16 (RU IP 85.95.166.40, score 100, totalCount 1031) and 07-17 (RO IP 92.118.39.204, score 100, totalCount 1021); totalCount net -10 over the window; 3 critical IOCs total for W29 so far ([[cyber-threats]]).
- 2026-07-15 — first Cyber Watch Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the abuse.ch channel is CC0, surfaced, and carries 21 committed L1 days).
  Wrote the at-a-glance, honest-scope and reading sections from the live 2026-07-15 pull:
  one critical malware-host IOC (RU-geolocated IP, confidence 100), consistent with the
  one-critical-per-day pattern of recent pulls. Observed-only framing, no attribution
  ([[cyber-threats]]).
