---
title: Cyber Watch Weekly
type: L2-brief
theme: cyber-watch
week: 2026-W36
updated: 2026-09-02T09:48:00Z
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
> from the 2026-07-15 ingest; current cutoff: the 2026-09-01 pull, an adjacent-day
> advance on the 2026-08-31 reading — so this cycle is a true one-day rotation, not a
> gap-bridged bookend comparison.)

## This week at a glance

- The abuse.ch / AbuseIPDB channel surfaced **exactly one active critical-severity
  indicator on both the 08-31 and 09-01 adjacent pulls** — the one-indicator critical tier
  holding flat while the surfaced host **rotated country** ([[cyber-threats]]).
- **2026-08-31 pull:** one malware-host IP geolocated to **Romania** (RO), criticality
  CRITICAL, no malware family tagged; feed pagination totalCount **1,006** ([[cyber-threats]]).
- **2026-09-01 pull:** one malware-host IP `85.217.140.43` geolocated to **France** (FR),
  AbuseIPDB confidence score 100, criticality CRITICAL, no malware family attributed; feed
  pagination totalCount **985** (down 21 from 1,006) — same severity and type as 08-31, the
  geolocation rotating RO → FR ([[cyber-threats]]).
- This is an **adjacent-day comparison** (08-31 → 09-01, no curator gap), so azimuth reads it
  as a genuine one-day rotation of the surfaced host rather than a gap-bridged bookend
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

- The 2026-09-01 indicator is a CYBER_THREAT_TYPE_MALWARE_HOST entry, IP `85.217.140.43`,
  sourced from AbuseIPDB at maximum confidence (score:100, CRITICALITY_LEVEL_CRITICAL); the
  malwareFamily field is empty, so no specific malware family was tagged by the tracker at pull
  time ([[cyber-threats]]).
- Against the 2026-08-31 reading (one CRITICAL IP host, Romania) the 09-01 pull holds the same
  severity and type but **rotates the geolocation RO → FR** — a true one-day rotation this time,
  since the two pulls are adjacent days with no curator gap between them ([[cyber-threats]]).
- The country field is geolocation of the indicator IP, not attribution of an actor; azimuth
  infers no actor, victim or campaign behind the listed host ([[cyber-threats]]).
- azimuth records the indicator, its type, severity and geolocation exactly as the tracker
  scored them, notes the totalCount easing 1,006 → 985, and makes no trend claim from a
  single-indicator surfaced tier ([[cyber-threats]]).

## Changelog

- 2026-09-02 — daily-ingest synthesis (2026-W36): absorbed the 2026-09-01 ingest, an adjacent-day advance on the 08-31 reading. The surfaced critical tier held at one active indicator but rotated country: IP 85.217.140.43 geolocated to France (FR), MALWARE_HOST, AbuseIPDB score 100, CRITICAL, no malware family — vs Romania (RO) on 08-31. Feed pagination totalCount eased 1,006 → 985. Because 08-31 → 09-01 are adjacent days (no curator gap), azimuth reads this as a genuine one-day host rotation rather than a gap-bridged bookend. Updated the intro, at-a-glance and reading sections. Observed-only framing held; editorial line held ([[cyber-threats]]).
- 2026-08-31 — daily-ingest synthesis (2026-W36): absorbed the 2026-08-21 through 2026-08-31 ingests after an 11-day curator gap; the 2026-08-31 pull lists the same read as the 2026-08-20 bookend — one active critical-severity indicator, type IP address, geolocated to Romania (RO), no malware family attributed — held flat across the gap. No daily 08-21→08-30 pulls were absorbed this cycle, so azimuth compares only the two bookend pulls and draws no rotation or trend inference from n=2. Observed-only framing held; editorial line held ([[cyber-threats]]).
- 2026-08-20 — daily-ingest synthesis (2026-W34): absorbed the 2026-08-18 through 08-20 abuse.ch pulls; the surfaced critical malware-host rotated every day — 195.178.110.232 (08-18, NL), 69.5.169.180 (08-19, DE), 80.94.95.242 (08-20, RO) — after 170.239.205.222 (08-17, CO), each AbuseIPDB score 100, CRITICAL, no malware family; totalCount eased 1,023 → 996 → 988 → 984 (net -39); origin geolocation CO → NL → DE → RO (geolocation, not attribution). One-indicator critical tier held. Observed-only framing held ([[cyber-threats]]).
- 2026-08-17 — daily-ingest synthesis (2026-W34): surfaced indicator rotated to 170.239.205.222 (CO, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 46.163.144.31 (08-16, RU); totalCount rose from 995 (08-16) to 1,023 (08-17), a net +28; origin country shifted RU → CO (geolocation, not attribution). One-indicator critical tier held. Observed-only framing held ([[cyber-threats]]).
- 2026-08-16 — daily-ingest synthesis (2026-W33): absorbed the 2026-08-14 through 2026-08-16 abuse.ch pulls; the surfaced critical malware-host rotated every day — 82.102.18.116 (08-14, FR), 66.132.186.251 (08-15, US), 46.163.144.31 (08-16, RU) — after 77.239.124.108 (08-13, NL), each AbuseIPDB score 100, CRITICAL, no malware family; totalCount moved 920 → 960 → 887 → 995 (net +75, swinging both directions); origin geolocation NL → FR → US → RU (geolocation, not attribution). One-indicator critical tier held. Observed-only framing held ([[cyber-threats]]).
- 2026-08-01 — daily-ingest flowback (2026-W31): surfaced indicator rotated to 103.191.14.210 (ID, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 103.213.238.91 (07-30, BD); totalCount eased from 1,022 (07-30) to 959 (08-01), a net -63 two-day retirement partly giving back the prior five-day re-expansion; origin country shifted BD → ID (geolocation, not attribution). One-indicator critical tier held ([[cyber-threats]]).
- 2026-07-25 — daily-ingest synthesis (2026-W30): surfaced indicator rotated to 81.19.219.204 (GB, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 179.176.210.17 (07-24, BR); totalCount fell from 922 to 819, a net -103 overnight retirement and the largest single-day drop recorded in this brief to date; origin country shifted BR → GB ([[cyber-threats]]).
- 2026-07-30 — daily-ingest synthesis (2026-W31): absorbed the 2026-07-26 through 2026-07-30 pulls after a five-day gap behind the live L1; surfaced indicator rotated to 103.213.238.91 (BD, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 81.19.219.204 (07-25, GB); totalCount rose from 819 to 1,022, a net +203 re-expansion that reverses the 07-24/07-25 contraction; origin country shifted GB → BD (geolocation, not attribution) ([[cyber-threats]]).
- 2026-07-24 — daily-ingest synthesis (2026-W30): surfaced indicator rotated to 179.176.210.17 (BR, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 50.6.197.105 (07-23, US); totalCount fell sharply from 999 to 922, a net -77 overnight retirement and the steepest single-day drop recorded in this brief; origin country shifted US → BR ([[cyber-threats]]).
- 2026-07-23 — daily-ingest synthesis (2026-W30): surfaced indicator rotated to 50.6.197.105 (US, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 165.22.1.254 (07-20); totalCount eased from 1,004 to 999, lowest reading to date; origin country held US ([[cyber-threats]]).
- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 pulls; the 07-20 pull lists one critical malware-host IP geolocated to the US (165.22.1.254, AbuseIPDB score 100, CRITICAL, no malware family); totalCount eased from 1,021 (07-17) to 1,004 (07-20), a net ~17-indicator retirement; origin country moved to the US after RO (07-17) and RU (07-15/16) ([[cyber-threats]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): absorbed 07-16 (RU IP 85.95.166.40, score 100, totalCount 1031) and 07-17 (RO IP 92.118.39.204, score 100, totalCount 1021); totalCount net -10 over the window; 3 critical IOCs total for W29 so far ([[cyber-threats]]).
- 2026-07-15 — first Cyber Watch Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the abuse.ch channel is CC0, surfaced, and carries 21 committed L1 days).
  Wrote the at-a-glance, honest-scope and reading sections from the live 2026-07-15 pull:
  one critical malware-host IOC (RU-geolocated IP, confidence 100), consistent with the
  one-critical-per-day pattern of recent pulls. Observed-only framing, no attribution
  ([[cyber-threats]]).
- 2026-08-13 — daily-ingest synthesis (2026-W33): absorbed the 2026-08-13 abuse.ch pull after a gap since the 2026-08-01 cycle (L1 ingest missing 08-02–08-06, then continuous daily pulls 08-07 through 08-13); surfaced indicator rotated to 77.239.124.108 (NL, AbuseIPDB score 100, CRITICAL, no malware family); prior slot held 103.191.14.210 (08-01, ID); totalCount eased from 959 (08-01) to 920 (08-13), a net -39 retirement over the 12-day span; origin country shifted ID → NL (geolocation, not attribution). One-indicator critical tier held. Observed-only framing held ([[cyber-threats]]).
