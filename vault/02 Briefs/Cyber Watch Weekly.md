---
title: Cyber Watch Weekly
type: L2-brief
theme: cyber-watch
week: 2026-W39
updated: 2026-09-24T12:00:00Z
sources: [cyber-threats]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Cyber Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded cyber
> threat indicators** — an IOC is an observed fact (a host, an IP, a first-seen timestamp,
> a severity as the tracker scored it) — and never attributes intent, names a victim, or
> predicts an attack. Every claim links to the L1 note it rests on. Cutoff: the **2026-09-24**
> pull, a one-day advance on 09-23. The surfaced top-severity band holds its shape — **500
> critical malware-host indicators** on this page, all AbuseIPDB score 100, none carrying a
> tagged malware family — with pagination `totalCount` easing **1,057 → 1,056** (net -1,
> essentially flat). The country distribution churned inside that stable total: the United
> States stays first but eases (118 → 114), the Netherlands jumps to second (33 → 44), and
> several mid-table countries reshuffle.

## This week at a glance

- The abuse.ch / AbuseIPDB channel surfaced **500 active critical-severity indicators** on the
  2026-09-24 pull — every one scored **CRITICAL** (AbuseIPDB confidence 100), every one typed
  **MALWARE_HOST**, and none carrying a tagged malware family; feed pagination reads `nextCursor`
  500 of `totalCount` **1,056**, essentially unchanged from 09-23's **1,057** ([[cyber-threats]]).
- By indicator-IP geolocation the set concentrates in the **United States (114)**, then the
  **Netherlands (44)**, **Germany (33)**, **China (30)**, **India (25)** and **France (23)** —
  the familiar hosting-heavy geographies where malware infrastructure is registered, not a map
  of actors ([[cyber-threats]]).
- The tail spreads across **South Korea (22), the United Kingdom (20), Singapore (13), Russia
  (13), Indonesia (13) and Brazil (13)** and dozens more countries at single digits — a broad,
  hosting-provider-shaped distribution rather than a single origin ([[cyber-threats]]).

## Honest scope

- **The surfaced critical band (500 of a totalCount near 1,056) held its shape day-on-day —
  same severity, same indicator type, same empty malware-family field.** Only the pagination
  total (1,057 → 1,056, net -1) and the geolocation mix moved; this is normal churn inside an
  already-widened feed, not a new structural shift ([[cyber-threats]]).
- **Country is geolocation of the indicator IP, not attribution of an actor.** The source records
  an IP, its geolocation and a severity score; azimuth reports the distribution of hosting
  geographies and makes no inference about who operates them or whom they target
  ([[cyber-threats]]).

## Move since prior reading (2026-09-23 → 2026-09-24)

- **Held: composition and total count.** Both pulls surface exactly 500 CRITICAL /
  MALWARE_HOST / score-100 / no-malware-family indicators; pagination `totalCount` eased by one
  row (1,057 → 1,056) — a genuinely flat read on scale ([[cyber-threats]]).
- **Moved: the geolocation mix.** The United States stays first but eases **118 → 114**; the
  Netherlands rises from third to second, **33 → 44**; Germany rises **24 → 33**; China rises
  **26 → 30**; India rises **23 → 25**; France rises **17 → 23**; South Korea rises **18 → 22**.
  Two countries that were in the 09-23 top tier — Hong Kong (21) and Vietnam (18) — drop out of
  the top-twelve entirely on 09-24; the United Kingdom holds at 20 ([[cyber-threats]]).
- azimuth reads this as ordinary day-to-day rotation of which hosts a fixed-size critical page
  happens to surface, not a measured rise or fall in threat volume — the underlying totalCount
  is flat and the indicator composition (type, severity, malware-family) is unchanged
  ([[cyber-threats]]).

## Reading the week

- Every one of the 500 surfaced indicators is a CYBER_THREAT_TYPE_MALWARE_HOST entry from
  AbuseIPDB at maximum confidence (score:100, CRITICALITY_LEVEL_CRITICAL) with an empty
  malwareFamily field on both the 09-23 and 09-24 pulls — the feed scores criticality and host
  type but tags no specific family on this page ([[cyber-threats]]).
- The geolocation distribution is hosting-shaped on both days: the US leads, then a cluster of
  large commercial-hosting jurisdictions (Netherlands, Germany, China, India, France, South
  Korea) — a fact about infrastructure geography, not about attribution. Day-on-day the *order*
  within that cluster reshuffled (Netherlands and Germany rose, Hong Kong and Vietnam dropped
  out of the top tier) while the *shape* — US first, then a broad multi-country hosting tail —
  held ([[cyber-threats]]).
- azimuth records each indicator's type, severity and geolocation exactly as the tracker scored
  them, notes the page carries 500 of a `totalCount` near 1,056, and makes no trend claim beyond
  the observed one-row pagination move and the geolocation reshuffle — both are read as normal
  churn in a stable-size feed, not a measured escalation ([[cyber-threats]]).

## Changelog

- 2026-09-24 — daily-ingest synthesis (2026-W39): absorbed the 2026-09-24 ingest, a one-day advance on 09-23. The surfaced critical band held its shape — 500 indicators, all AbuseIPDB score 100 / CRITICAL / MALWARE_HOST / no malware family — with pagination totalCount essentially flat (1,057 → 1,056, net -1). The geolocation mix churned: US stays first but eases 118 → 114, Netherlands rises to second 33 → 44, Germany 24 → 33, China 26 → 30, India 23 → 25, France 17 → 23, South Korea 18 → 22; Hong Kong (21) and Vietnam (18) drop out of the top tier, UK holds at 20. Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections around the day-on-day comparison; read the reshuffle as ordinary churn in a stable-size feed, not a volume or trend claim. Observed-only framing held; editorial line held ([[cyber-threats]]).
- 2026-09-23 — daily-ingest synthesis (2026-W39): absorbed the 2026-09-22 ingest after a 20-day curator gap — a major channel widening. The feed no longer surfaces one critical indicator per pull; it now returns the full top-severity band, 500 critical MALWARE_HOST indicators on this page (all AbuseIPDB score 100, no malware family), pagination nextCursor 500 of totalCount 1,024. By indicator-IP geolocation the set concentrates in the US (114), Netherlands (44), China (39), UK (24), Germany (22), then South Korea (20), India (18), Hong Kong (17), France (16), Singapore (14) — a hosting-provider-shaped distribution, not attribution. Rewrote the intro, at-a-glance, honest-scope and reading sections around the widened set; made no trend claim between the widened set and the prior one-indicator tier (different feed shapes). Observed-only framing held; editorial line held ([[cyber-threats]]).
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