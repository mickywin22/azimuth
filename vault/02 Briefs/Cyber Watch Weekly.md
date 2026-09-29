---
title: Cyber Watch Weekly
type: L2-brief
theme: cyber-watch
week: 2026-W40
updated: 2026-09-30T00:00:00Z
sources: [cyber-threats]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Cyber Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded cyber
> threat indicators** — an IOC is an observed fact (a host, an IP, a first-seen timestamp,
> a severity as the tracker scored it) — and never attributes intent, names a victim, or
> predicts an attack. Every claim links to the L1 note it rests on. Cutoff: the **2026-09-29**
> pull, a two-day advance on 09-27. The surfaced top-severity band holds its shape — **500
> critical malware-host indicators** on this page, all AbuseIPDB score 100, none carrying a
> tagged malware family — but this cycle the scale eased: pagination `totalCount` fell
> **1,082 → 1,050** (net −32), and the country distribution reshuffled back toward the US. The
> United States surges back to a wide first (92 → 121), China eases from second (55 → 42), and
> Germany rises into a tie for fourth (21 → 25).

## This week at a glance

- The abuse.ch / AbuseIPDB channel surfaced **500 active critical-severity indicators** on the
  2026-09-29 pull — every one scored **CRITICAL** (AbuseIPDB confidence 100, tag `score:100`),
  every one typed **MALWARE_HOST**, and none carrying a tagged malware family; feed pagination
  reads `nextCursor` 500 of `totalCount` **1,050**, down from 09-27's **1,082** (net −32)
  ([[cyber-threats]]).
- By indicator-IP geolocation the set now concentrates in the **United States (121)**, then
  **China (42)**, the **Netherlands (41)**, and a tie between **Germany (25)** and **India
  (25)**, then **South Korea (20)** — the familiar hosting-heavy geographies where malware
  infrastructure is registered, not a map of actors ([[cyber-threats]]).
- The tail spreads across **France (18), Hong Kong (16), Brazil (16), Indonesia (14), Russia
  (10), the United Kingdom (9)** and dozens more countries at single digits (Vietnam, Japan,
  Belgium at 8 each) — a broad, hosting-provider-shaped distribution rather than a single origin
  ([[cyber-threats]]).

## Honest scope

- **The surfaced critical band held its composition but not its scale this cycle.** All 500
  rows stay CRITICAL / MALWARE_HOST / score-100 / no-malware-family, but `totalCount` moved a
  genuine net −32 (1,082 → 1,050), giving back the prior cycle's +26 and then some — azimuth
  reports this as real but small day-to-day volatility in page scale, not a directional trend
  ([[cyber-threats]]).
- **Country is geolocation of the indicator IP, not attribution of an actor.** The source records
  an IP, its geolocation and a severity score; azimuth reports the distribution of hosting
  geographies and makes no inference about who operates them or whom they target
  ([[cyber-threats]]).

## Move since prior reading (2026-09-27 → 2026-09-29)

- **Held: composition.** All 500 surfaced indicators on both pulls are CRITICAL / MALWARE_HOST /
  AbuseIPDB score-100 / no-malware-family; the type and severity fields are unchanged
  ([[cyber-threats]]).
- **Moved: total scale.** Pagination `totalCount` fell **1,082 → 1,050** (net −32) over the
  two-day span — giving back the prior cycle's +26 rise, a small net fall rather than a trend
  ([[cyber-threats]]).
- **Moved: the geolocation mix, reshuffling back toward the US.** The United States surges back to
  a wide first, **92 → 121** (+29); China eases from second, **55 → 42** (-13); the Netherlands
  holds its podium spot, essentially flat **45 → 41** (-4); Germany rises into a tie for fourth,
  **21 → 25** (+4); India holds **21 → 25** (+4); South Korea eases **27 → 20** (-7); France
  rises **13 → 18** (+5); Hong Kong **14 → 16** (+2) and Brazil **12 → 16** (+4) firm; the United
  Kingdom eases **14 → 9** (-5) ([[cyber-threats]]).
- **Slipped from the surfaced top tier:** Canada and Taiwan, visible last cycle, drop out of the
  top-12 window as the US re-concentrated the page and the mid-tier reordered ([[cyber-threats]]).
- azimuth reads the composition as holding but the scale and geolocation mix as genuinely moving
  this cycle — a real net-32 fall in total indicators and a reshuffle led by the US re-surging and
  China easing — while still making no claim about actors, motive or forecast beyond the recorded
  numbers ([[cyber-threats]]).

## Reading the week

- Every one of the 500 surfaced indicators is a CYBER_THREAT_TYPE_MALWARE_HOST entry from
  AbuseIPDB at maximum confidence (`score:100`, CRITICALITY_LEVEL_CRITICAL) with an empty
  malwareFamily field on the 09-27 and 09-29 pulls alike — the feed scores criticality and host
  type but tags no specific family on this page ([[cyber-threats]]).
- The geolocation distribution stays hosting-shaped on both days — the US leads, then a
  cluster of large commercial-hosting jurisdictions — but the *order and weight* inside that
  cluster reshuffled back toward the US this cycle: the US re-widened its lead (92 → 121), China's
  share fell back from its prior jump (55 → 42), and Germany firmed into a tie for fourth as the
  mid-tier reordered ([[cyber-threats]]).
- azimuth records each indicator's type, severity and geolocation exactly as the tracker scored
  them, notes the page carries 500 of a `totalCount` that fell net −32 to 1,050, and reads the
  geolocation reshuffle as a genuine week-on-week move in hosting-country weight rather than a
  claim about who operates or targets that infrastructure ([[cyber-threats]]).

## Changelog

- 2026-09-30 — daily-ingest synthesis (2026-W40): absorbed the 2026-09-29 pull, a two-day advance on 09-27. The surfaced critical band held its composition — 500 indicators, all AbuseIPDB score 100 / CRITICAL / MALWARE_HOST / no malware family — but the scale eased: pagination totalCount fell 1,082 → 1,050 (net −32), giving back the prior cycle's +26. The geolocation mix reshuffled back toward the US: US surges back to a wide first 92 → 121, China eases from second 55 → 42, Netherlands holds near-flat 45 → 41, Germany rises into a tie for fourth 21 → 25, India holds 21 → 25, South Korea eases 27 → 20, France rises 13 → 18, Hong Kong 14 → 16 and Brazil 12 → 16 firm, UK eases 14 → 9; Canada and Taiwan slip out of the surfaced top tier. Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections around the net-scale-fall-and-mix move. Observed-only framing held; editorial line held ([[cyber-threats]]).
- 2026-09-28 — daily-ingest synthesis (2026-W39): absorbed the 2026-09-27 pull, a three-day advance on 09-24 (with 09-25 and 09-26 glanced for trajectory). The surfaced critical band held its composition — 500 indicators, all AbuseIPDB score 100 / CRITICAL / MALWARE_HOST / no malware family — but the scale genuinely moved this time: pagination totalCount rose 1,056 → 1,082 (net +26), with a noisy path in between (1,084 on 09-25, 1,047 on 09-26). The geolocation mix reshuffled more sharply than last cycle: US stays first but eases 114 → 92, China leaps from fourth to second 30 → 55 (the largest single-country move recorded in this brief), Netherlands holds near-flat 44 → 45, Germany falls from third to a tie for fifth 33 → 21, South Korea rises 22 → 27, India eases 25 → 21, France eases sharply 23 → 13, UK eases 20 → 14, Singapore/Russia/Indonesia all ease 13 → 9, Brazil holds near-flat 13 → 12; Hong Kong (14) and Canada (15) re-enter/enter the surfaced top tier. Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections around this genuine net-scale-and-mix move, explicitly distinguishing it from the prior cycle's flat read. Observed-only framing held; editorial line held ([[cyber-threats]]).
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