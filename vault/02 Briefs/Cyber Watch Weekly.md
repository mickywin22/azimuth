---
title: Cyber Watch Weekly
type: L2-brief
theme: cyber-watch
week: 2026-W29
updated: 2026-07-18T09:00:00Z
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

- The abuse.ch / AbuseIPDB channel has surfaced **one critical-severity indicator per pull**
  across all three W29 ingest days so far — pattern consistent with prior weeks ([[cyber-threats]]).
- **2026-07-17 pull** (retrieved 08:25Z): one malware-host IP geolocated to **Romania** (RO),
  `92.118.39.204`, AbuseIPDB confidence score 100, criticality CRITICAL; feed pagination
  totalCount **1,021** ([[cyber-threats]]).
- **2026-07-16 pull** (retrieved 08:30Z): one malware-host IP geolocated to **Russia** (RU),
  `85.95.166.40`, AbuseIPDB confidence score 100, criticality CRITICAL; feed pagination
  totalCount **1,031** ([[cyber-threats]]).
- The totalCount dropped by 10 between 07-16 (1,031) and 07-17 (1,021), indicating the
  upstream tracker retired or de-listed approximately 10 indicators over that 24-hour window
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

- Both 07-16 and 07-17 indicators are CYBER_THREAT_TYPE_MALWARE_HOST entries sourced from
  AbuseIPDB at maximum confidence (score:100, CRITICALITY_LEVEL_CRITICAL). The malwareFamily
  field is empty on both, meaning no specific malware family was tagged by the tracker at
  pull time ([[cyber-threats]]).
- The geolocation shifted from Russia (07-16) to Romania (07-17). This is a single-indicator
  observation; the feed's curated critical tier is too narrow to draw pattern conclusions from
  a one-day change in origin country ([[cyber-threats]]).
- The 07-15 indicator (first cycle) was also RU-geolocated; 07-17 breaks that two-day run
  with a RO-geolocated host. Aggregate IOC count for W29 so far: **3 critical malware-host
  indicators across 3 days** ([[cyber-threats]]).

## Changelog

- 2026-07-18 — daily-ingest synthesis (2026-W29): absorbed 07-16 (RU IP 85.95.166.40, score 100, totalCount 1031) and 07-17 (RO IP 92.118.39.204, score 100, totalCount 1021); totalCount net -10 over the window; 3 critical IOCs total for W29 so far ([[cyber-threats]]).
- 2026-07-15 — first Cyber Watch Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the abuse.ch channel is CC0, surfaced, and carries 21 committed L1 days).
  Wrote the at-a-glance, honest-scope and reading sections from the live 2026-07-15 pull:
  one critical malware-host IOC (RU-geolocated IP, confidence 100), consistent with the
  one-critical-per-day pattern of recent pulls. Observed-only framing, no attribution
  ([[cyber-threats]]).
