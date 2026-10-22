---
title: Cyber Watch Weekly
type: L2-brief
theme: cyber-watch
week: 2026-W43
updated: 2026-10-22T00:00:00Z
sources: [cyber-threats]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Cyber Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded cyber
> threat indicators** — an IOC is an observed fact (a host, an IP, a first-seen timestamp,
> a severity as the tracker scored it) — and never attributes intent, names a victim, or
> predicts an attack. Every claim links to the L1 note it rests on. Cutoff: the **2026-10-22**
> pull. The surfaced band **held its uniform composition for the full week** — all 500 rows on
> every daily pull from 2026-10-16 through 2026-10-22 stayed **CRITICAL severity**,
> **MALWARE_HOST type**, AbuseIPDB-scored and carrying **no malware family**, with **no
> C2_SERVER / Feodo-Tracker-shaped rows** surfacing at any point — this remains an all-URLhaus-shaped
> page; the Feodo split is an honest **HOLD** (nothing to split, not a fresh reading). Scale moved on a
> noisy path: pagination `totalCount` ran **1,205 → 1,041 → 1,038 → 1,462 → 1,303 → 1,273 → 1,319**
> across the week, peaking at **1,462** on 2026-10-19 — the highest `totalCount` recorded in this
> brief's history to date — before easing back, for a week-on-week **net +114** (1,205 → 1,319). By
> indicator-IP geolocation the attributed set stayed US-led but reshuffled second place: **United
> States 155** (from 116) widens its lead, **South Korea 38** (from 29) overtakes **China 37** (from 57)
> for second, the **Netherlands 29** (from 47) and **Germany 18** (from 24) both ease, **France 17**
> (from 8) more than doubles into the upper tier, **India 20** (from 24) and the **United Kingdom 16**
> (from 18) hold roughly flat, and **Singapore 12** (from 5) enters the top ten as **Hong Kong** and
> **Brazil** drop out of it — with **0 rows unattributed** on every day and **55 distinct attributed
> geographies**, down from 60.

## This week at a glance

- The abuse.ch / AbuseIPDB channel surfaced **500 indicators** on every pull from 2026-10-16 through
  2026-10-22 with its **uniform composition held for the full week**: all 500 rows stayed
  **CRITICAL** severity and **MALWARE_HOST** type on every single day, no command-and-control class
  ever entering the page; feed pagination `totalCount` closed the week at **1,319**, net **+114** on
  the 2026-10-16 opening read of **1,205**, after a noisy path that peaked at a brief-record **1,462**
  on 2026-10-19 ([[cyber-threats]]).
- By indicator-IP geolocation the attributed set stayed **US-led** and reshuffled second place: the
  **United States (155)** widens its lead from 116, **South Korea (38)** overtakes **China (37)** for
  second (China eased from 57), the **Netherlands (29)** and **Germany (18)** both ease, **France
  (17)** more than doubles from 8, and **Singapore (12)** enters the top ten as **Hong Kong** and
  **Brazil** fall out of it — the familiar hosting-heavy geographies where infrastructure is
  registered, not a map of actors ([[cyber-threats]]).
- **0 of the 500 rows carry no country** on any day this week (the malware-host rows are all
  geolocated), across **55 distinct attributed geographies** this cycle, down from 60 on
  2026-10-16 ([[cyber-threats]]).

## Honest scope

- **The surfaced critical band held its composition for the full week; only the scale and the
  geolocation mix moved.** All 500 rows stayed CRITICAL severity, MALWARE_HOST type, AbuseIPDB-sourced
  and carrying no malware family on every one of the seven 2026-10-16 → 2026-10-22 pulls — azimuth
  reports that stability as a real feed-shape fact, not an inference that the underlying threat
  landscape itself held still ([[cyber-threats]]).
- **URLhaus vs. Feodo split: HOLD.** No CYBER_THREAT_TYPE_C2_SERVER (Feodo-Tracker-shaped)
  row appeared on any pull this week — the surfaced page stayed entirely URLhaus-shaped
  (MALWARE_HOST). azimuth reports the absence as this cycle's honest read, not a claim that the
  Feodo Tracker channel is empty or retired ([[cyber-threats]]).
- **Country is geolocation of the indicator IP, not attribution of an actor.** The source records
  an IP, its geolocation and a severity score; azimuth reports the distribution of hosting
  geographies and makes no inference about who operates them or whom they target
  ([[cyber-threats]]).

## Move since prior reading (2026-10-16 → 2026-10-22)

- **Held: composition.** Every pull this week — 2026-10-16, 17, 18, 19, 20, 21, 22 — surfaced the
  same uniform band: 500 of 500 rows CRITICAL / MALWARE_HOST / AbuseIPDB / no malware family, with
  no C2_SERVER class entering at any point ([[cyber-threats]]).
- **Moved: total scale, on a noisy path, net up.** Pagination `totalCount` ran 1,205 → 1,041 → 1,038
  → 1,462 → 1,303 → 1,273 → 1,319 across the week — a sharp early dip, a brief-record peak of 1,462 on
  2026-10-19, then an easing back — for a week-on-week net **+114** ([[cyber-threats]]).
- **Moved: South Korea overtook China for second place.** Of the attributed rows the United States
  widened its lead 116 → 155; South Korea rose 29 → 38 to pass China, which eased 57 → 37; the
  Netherlands eased 47 → 29 and Germany 24 → 18; France more than doubled 8 → 17 into the upper tier;
  India eased slightly 24 → 20 and the UK 18 → 16; Singapore entered the top ten 5 → 12 as Hong Kong
  (19 → 11) and Brazil (14 → 10) dropped out of it ([[cyber-threats]]).
- **Attribution coverage held at full, breadth narrowed.** **0 of 500** rows carried no country on
  any day this week (every malware-host row geolocated, as on 2026-10-16), while distinct attributed
  geographies narrowed **60 → 55** ([[cyber-threats]]).
- azimuth reads the composition hold, the noisy-but-net-positive scale move and the US-led
  reshuffle (Korea past China, France's rise, Singapore's entry) as genuine week-on-week feed changes
  — while still making no claim about actors, motive or forecast beyond the recorded numbers
  ([[cyber-threats]]).

## Reading the week

- Every one of the seven 2026-10-16 → 2026-10-22 pulls surfaced **500 of 500 CYBER_THREAT_TYPE_MALWARE_HOST**
  rows, **all CRITICALITY_LEVEL_CRITICAL**, AbuseIPDB-scored with no malware family attributed — the
  uniform all-CRITICAL / all-MALWARE_HOST composition held the entire week with no command-and-control
  class surfacing on any single day ([[cyber-threats]]).
- The geolocation distribution stays hosting-shaped and stayed **US-led** throughout, but second place
  changed hands: the US closed the week at 155 (from 116 on 2026-10-16), South Korea rose to 38 and
  passed China's 37 (down from 57), the Netherlands eased to 29 and Germany to 18, France more than
  doubled to 17, and Singapore broke into the top ten at 12 as Hong Kong and Brazil dropped out — with
  0 of the 500 rows carrying no country on any day across 55 distinct geographies, down from
  60 ([[cyber-threats]]).
- Scale itself was the noisiest signal: pagination `totalCount` swung from 1,205 down to 1,038 and
  back up to a brief-record 1,462 (2026-10-19) before settling at 1,319 — a net +114 for the week.
  azimuth records each indicator's type, severity and geolocation exactly as the tracker scored
  them, and reads the composition hold, the scale swing and the second-place swap as genuine
  day-on-day feed changes rather than a claim about who operates or targets that
  infrastructure ([[cyber-threats]]).

## Changelog

- 2026-10-22 — daily-ingest synthesis (2026-W43): absorbed the 2026-10-17 → 2026-10-22 pulls against the
  2026-10-16 opening read. Composition held the entire week: every pull surfaced 500 of 500 rows
  CRITICAL / MALWARE_HOST / AbuseIPDB / no malware family, no C2_SERVER (Feodo-Tracker-shaped) row ever
  entering — URLhaus vs. Feodo split stays an honest HOLD, nothing to split. Scale moved on a noisy
  path — `totalCount` 1,205 → 1,041 → 1,038 → 1,462 → 1,303 → 1,273 → 1,319, peaking at a brief-record
  1,462 on 2026-10-19 before easing back, net +114 for the week. By indicator-IP geolocation the US
  widened its lead 116 → 155 while South Korea overtook China for second (29 → 38 vs. 57 → 37); the
  Netherlands (47 → 29) and Germany (24 → 18) eased, France more than doubled (8 → 17) into the upper
  tier, and Singapore (5 → 12) entered the top ten as Hong Kong (19 → 11) and Brazil (14 → 10) dropped
  out; 0 unattributed rows held across every day, distinct attributed geographies narrowed 60 → 55.
  Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections around the
  composition-hold + noisy-scale + Korea-past-China move. Observed-indicator framing held — no actor
  attribution, no victim, no forecast ([[cyber-threats]]).

- 2026-10-16 — daily-ingest synthesis (2026-W42): absorbed the 2026-10-14 → 2026-10-15 pulls. The surfaced band snapped back to its uniform composition — the prior cycle's MEDIUM/HIGH + MALWARE_HOST/C2_SERVER break reversed, the 500 rows now all 500 CRITICAL severity and all 500 MALWARE_HOST type as the command-and-control class exited the page. Scale surged: pagination `totalCount` rose 515 → 1,208 (net +693), reversing the prior cycle's contraction. By indicator-IP geolocation the attributed set flipped back from China-led to US-led: US 103, China 46, Netherlands 42, Germany 24, UK 23, France 20, South Korea 19, Canada 18, with 0 unattributed rows across 64 distinct geographies (against the prior cycle's China-concentrated 20). Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections. Observed-indicator framing held — no actor attribution, no victim, no forecast ([[cyber-threats]]).

- 2026-10-13 — daily-ingest synthesis (2026-W42): absorbed the 2026-10-12 → 2026-10-13 pulls — the surfaced composition broke. The 500 rows no longer run uniform all-CRITICAL / all-MALWARE_HOST: they split 264 MEDIUM / 236 HIGH by severity (no CRITICAL this page) and 264 MALWARE_HOST / 236 C2_SERVER by type, a new command-and-control class entering. Scale fell sharply — pagination `totalCount` 1,338 → 515 (net −823), the largest single-cycle contraction recorded in this brief. The geolocation mix flipped from US-led to China-led: of the attributed rows China leads at 106, then Hong Kong 31, the US 13, Singapore 13, Germany 6, Switzerland 6; 301 of 500 rows unattributed (largely the C2-server class), 20 distinct attributed geographies (from 63). Rewrote the intro, at-a-glance, honest-scope, move and reading sections around the composition break, scale fall and geo flip. No-attribution framing held ([[cyber-threats]]).
- 2026-10-11 — daily-ingest synthesis (2026-W41): absorbed the 2026-10-09 → 2026-10-11 pulls. Composition held (500 surfaced indicators all CRITICAL / MALWARE_HOST / AbuseIPDB score-100 / no malware family) while scale rose again — pagination `totalCount` 1,146 → 1,338 (net +192), a second straight rebound. The geolocation mix spread off the US as the UK firmed back into the tier: the United States eased its lead 110 → 103, China firmed to second 49 → 53, the Netherlands rose to third 36 → 41, the United Kingdom firmed sharply back into the tier at 37 and South Korea firmed 14 → 22, while Vietnam eased 20 → 15 and Hong Kong 18 → 11; distinct geographies ticked to 63 (from 62). Rewrote the intro, at-a-glance, honest-scope, move and reading sections. No-attribution framing held ([[cyber-threats]]).
- 2026-10-08 — daily-ingest synthesis (2026-W41): absorbed the 2026-10-07 and 2026-10-08 pulls. Composition held (500 surfaced indicators all CRITICAL / MALWARE_HOST / AbuseIPDB score-100 / no malware family) while scale rebounded — pagination `totalCount` 916 → 1,146 (net +230), reversing last cycle's sharp fall. The geolocation mix concentrated further on the US with China retaking second: the United States widened its lead 107 → 110, China rose to second 43 → 49, the Netherlands fell further 47 → 36, Germany firmed 25 → 28 and Vietnam 13 → 20, Belgium (14) and Canada (13) entered the upper tier, while South Korea eased 20 → 14; distinct geographies held at 62. Rewrote the intro, at-a-glance, honest-scope, move and reading sections. No-attribution framing held ([[cyber-threats]]).
- 2026-10-06 — daily-ingest synthesis (2026-W41): absorbed the 2026-10-05 and 2026-10-06 pulls. Composition held (500 surfaced indicators all CRITICAL / MALWARE_HOST / AbuseIPDB score-100 / no malware family) while scale fell sharply — pagination `totalCount` 1,209 → 916 (net −293), reversing the prior run of small net rises. The geolocation mix reshuffled back toward the US: the United States widened its lead 91 → 107, the Netherlands fell back hard from its near-first surge 77 → 47, China firmed 39 → 43, Germany 21 → 25, India 16 → 21 and Hong Kong 15 → 19, South Korea re-entered the upper tier at 20, while the UK eased 28 → 18 and Brazil 19 → 16; distinct geographies narrowed 66 → 62. Rewrote the intro, at-a-glance, honest-scope, move and reading sections. No-attribution framing held ([[cyber-threats]]).
- 2026-10-04 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-04 pull. Composition held (500 surfaced indicators all CRITICAL / MALWARE_HOST / AbuseIPDB score-100 / no malware family) while scale rose again — pagination `totalCount` 1,177 → 1,209 (net +32, third straight small rise). The geolocation mix reshuffled hard: the United States fell sharply but held the lead 123 → 91, the Netherlands surged again 55 → 77 to within striking distance of first, China firmed 36 → 39, the UK firmed 24 → 28, Brazil entered the upper tier at 19, France 15 → 17 and India 15 → 16, while Germany eased 31 → 21, Hong Kong 23 → 15 and Singapore 14 → 8; distinct geographies widened 58 → 66. Rewrote the intro, at-a-glance, honest-scope, move and reading sections. No-attribution framing held ([[cyber-threats]]).

- 2026-10-03 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-02 and 2026-10-03 pulls. The surfaced critical band held its composition — 500 indicators, all AbuseIPDB score 100 / CRITICAL / MALWARE_HOST / no malware family — and the scale rose again: pagination totalCount climbed 1,092 → 1,177 (net +85), a second straight rise after +42. The geolocation mix reshuffled, the Netherlands surging to second: US eased but held the lead 136 → 123, Netherlands surged 43 → 55, China eased 44 → 36, Germany firmed 27 → 31, the UK re-entered the upper tier at 24, Hong Kong firmed 15 → 23, India eased 21 → 15, South Korea 19 → 15, France firmed 11 → 15, and Singapore's prior surge receded 22 → 14; Canada and Poland slipped out of the surfaced top tier. 58 distinct hosting geographies (from 62). Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections around the net-scale-rise-and-NL-surge move. Observed-only framing held; editorial line held ([[cyber-threats]]).
- 2026-10-01 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-01 pull, a two-day advance on 09-29. The surfaced critical band held its composition — 500 indicators, all AbuseIPDB score 100 / CRITICAL / MALWARE_HOST / no malware family — and the scale rose: pagination totalCount climbed 1,050 → 1,092 (net +42), reversing the prior cycle's −32. The geolocation mix concentrated further on the US: US widens 121 → 136, China firms 42 → 44, Netherlands holds 41 → 43, Germany holds fourth 25 → 27, Singapore surges into fifth (new at 22), India eases 25 → 21, South Korea holds 20 → 19, France eases 18 → 11 and Brazil 16 → 10, Canada re-enters at 14; the UK slips out of the surfaced top tier. 62 distinct hosting geographies. Rewrote the intro, at-a-glance, honest-scope, move-since and reading sections around the net-scale-rise-and-mix move. Observed-only framing held; editorial line held ([[cyber-threats]]).
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