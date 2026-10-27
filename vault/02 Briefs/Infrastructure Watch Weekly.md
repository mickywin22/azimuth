---
title: Infrastructure Watch Weekly
type: L2-brief
theme: infrastructure-watch
week: 2026-W44
updated: 2026-10-27T00:00:00Z
sources: [internet-outages]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Infrastructure Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded
> infrastructure disruption events** — an internet outage is an observed network measurement
> (Cloudflare Radar), with the cause category the source itself assigns — and takes no
> position on any actor involved. Every claim links to the L1 note it rests on. This cycle
> absorbs the 2026-10-23 → 2026-10-27 pulls: the active set **eased to 13 outages** (from 15 on
> 10-22) as **two Iraq "exam shutdown" rows aged off** the rolling window and **every other row
> held unchanged**. **Iraq now carries 4 of the 13 events** (down from 6, all still
> government-directed exam-shutdown suspensions, the special round that ran
> 2026-09-26 → 2026-10-10); Uruguay and Haiti each still carry a cable-cut, Eswatini, Namibia and
> Sri Lanka their nationwide power-outages, **Syria** its `MAINTENANCE`-cause network row and
> **Ethiopia** its regional government-directed restriction, and **Panama still carries its
> ongoing nationwide total natural-disaster outage** (the M7.7 earthquake still cutting Internet
> traffic, no recorded end) alongside Russia's unchanged military-action-labelled network
> disruption. Cause split now **5 government-directed / 3 power-outage / 2 cable-cut / 1
> natural-disaster / 1 military-action / 1 maintenance** — only the government-directed band
> eased (−2). The active set still spans **10 countries**.
> (Pull date of current cycle: 2026-10-27.)

## This week at a glance

- The Cloudflare Radar channel records **13 active internet outages** on 10-27 — **4
  nationwide**, **3 network-level** and **6 regional** in scope. By the source's own cause
  category: **5 government-directed**, **3 power-outage**, **2 cable-cut**, **1
  natural-disaster**, **1 military-action** and **1 maintenance** — the set eased by a net 2
  rows since 10-22, both the departures Iraq exam-shutdown rows aging off; the six cause
  categories all carried ([[internet-outages]]).
- **Ten countries still hold the 13 events, and Iraq carries 4 of them** (eased from 6) — all
  government-directed exam-shutdown suspensions; Uruguay and Haiti carry a cable-cut apiece;
  Eswatini, Namibia and Sri Lanka each a nationwide power-outage; **Panama a nationwide total
  outage from the M7.7 earthquake** (natural-disaster, ongoing); **Russia a network disruption
  the source labels military-action**; **Syria a network disruption the source labels
  maintenance**; and **Ethiopia a regional government-directed internet restriction**, all
  carried unchanged ([[internet-outages]]).
- The composition **still anchors on the Iraq exam-shutdown pattern** (eased to 4 from 6 as two
  detections aged off) while every other row held unchanged — no entries, no cause category
  cleared; severity now splits **6 MAJOR / 4 TOTAL / 3 PARTIAL** ([[internet-outages]]).

## Honest scope

- The theme registry lists a second channel (IMF PortWatch chokepoint status) that
  remains unsurfaced: the upstream endpoint has returned HTTP 404 since 2026-06-25, with zero
  committed L1 notes to date (no chokepoint-status note in the 2026-09-22 ingest); this brief
  scopes to the live internet-outage channel and widens when the second channel lands
  ([[internet-outages]]).

## Reading the week

- **Iraq eases to 4 government-directed events this cycle** (from 6) — all the source's
  recurring "exam shutdown" pattern, short regional internet suspensions in the early hours,
  the special round that ran 2026-09-26 → 2026-10-10; two detections rolled off the window.
  azimuth records the cause label the source assigns and takes no position on the practice
  ([[internet-outages]]).
- **No new rows entered this cycle:** the only change was two Iraq exam-shutdown detections
  aging off the rolling window — every other prior row (Uruguay, Haiti, Panama, Russia,
  Eswatini, Namibia, Syria, Sri Lanka, Ethiopia and the four remaining Iraq rows) carried
  unchanged ([[internet-outages]]).
- **The two departures were both Iraq exam-shutdown rows:** no cause category cleared and no
  country left the set — Iraq remains present at 4, so all ten countries still hold a row
  ([[internet-outages]]).
- **Cable-cut holds at two events, unchanged** — Uruguay's ANTEL backbone cut and
  Haiti's Digicel network (fibre-optic cable damage on Route Nationale), both carried
  unchanged this cycle ([[internet-outages]]).
- **Power-outage holds three events, unchanged** — Eswatini (Swaziland), the source attributes
  it to planned outages by the Eswatini Electricity Company; the Namibia substation fault; and
  the Sri Lanka nationwide blackout — all carried unchanged this cycle ([[internet-outages]]).
- **Panama holds its nationwide total-severity natural-disaster outage** — the source
  attributes a significant drop in Internet traffic across Panama to the M7.7 earthquake (detected
  2026-10-10, still ongoing with no recorded end), carried unchanged and a cross-channel echo of the
  Geophysical brief's Panama major ([[internet-outages]]).
- **Russia holds its network military-action-labelled disruption, carried unchanged** — Yandex
  data-centre shutdowns the source attributes to drone-strike damage in Sasovo, Ryazan and
  Vladimir, still with no recorded end ([[internet-outages]]).
- The set eased at the edges this cycle while its whole composition held: every non-Iraq row
  carried unchanged and Iraq eased from 6 to 4 as two exam-shutdown detections aged off — taking
  the set from 15 to 13 outages, still across ten countries and still spanning six cause
  categories (only the government-directed band moved, −2) ([[internet-outages]]).
- azimuth reports the measurements and the source's cause labels, and stops there
  ([[internet-outages]]).

## Changelog

- 2026-10-27 — daily-ingest synthesis (2026-W44): absorbed the 2026-10-23 → 2026-10-27 pulls. The active set eased to 13 outages (from 15 on 10-22) as two Iraq "exam shutdown" detections aged off the rolling window; every other row held unchanged (no entries, no cause category cleared). Iraq eased to 4 of the 13 events (from 6, all still government-directed exam-shutdown suspensions); Uruguay and Haiti held a cable-cut apiece, Eswatini / Namibia / Sri Lanka their nationwide power-outages, Syria its MAINTENANCE-cause network row, Ethiopia its regional government-directed restriction, Panama its ongoing nationwide total natural-disaster outage (M7.7 earthquake, no recorded end) and Russia its military-action-labelled network disruption — all carried unchanged. Cause split 5 government-directed / 3 power-outage / 2 cable-cut / 1 natural-disaster / 1 military-action / 1 maintenance (only the government-directed band moved, −2); scope 6 regional / 4 nationwide / 3 network; severity 6 MAJOR / 4 TOTAL / 3 PARTIAL; ten countries (held). Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections around the two Iraq departures and the held composition. Observed-measurement, no-actor-position framing held ([[internet-outages]]).
- 2026-10-22 — daily-ingest synthesis (2026-W43): absorbed the 2026-10-16 → 2026-10-22 pulls. The active set grew to 15 outages (from 13 on 10-15) as four new rows entered — Namibia (POWER_OUTAGE, nationwide), Syria (the set's first MAINTENANCE-cause row, network), Sri Lanka (POWER_OUTAGE, nationwide) and Ethiopia (GOVERNMENT_DIRECTED, regional, an internet restriction the source links to fighting in the Tigray region) — while two rows aged off: Guyana's GT&T cable-cut and Cuba's nationwide power-outage blackout. Iraq held at 6 of the 15 events (unchanged exam-shutdown rows); Uruguay, Haiti, Panama's natural-disaster row and Russia's military-action row all held unchanged. Cause split 7 government-directed / 3 power-outage / 2 cable-cut / 1 natural-disaster / 1 military-action / 1 maintenance (maintenance new this cycle); scope 8 regional / 4 nationwide / 3 network; severity 8 MAJOR / 4 TOTAL / 3 PARTIAL; ten countries (from eight). Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections around the four entries and two exits. Observed-measurement, no-actor-position framing held ([[internet-outages]]).

- 2026-10-16 — daily-ingest synthesis (2026-W42): absorbed the 2026-10-14 → 2026-10-15 pulls. The active set firmed to 13 outages (from 11 on 10-13) as two new rows entered — a Uruguay regional cable-cut (MAJOR) and a Russian Federation network disruption the source labels MILITARY_ACTION (PARTIAL), the first military-action-cause row in the set this run — while every prior row held. Iraq still dominates with 6 of the 13 events (all government-directed exam-shutdown suspensions, the special round that ran 2026-09-26 → 2026-10-10); Haiti, Guyana and Uruguay carry a cable-cut apiece, Eswatini and Cuba nationwide power blackouts, Panama its ongoing nationwide total natural-disaster outage (the M7.7 earthquake, no recorded end) and Russia the new military-action row. Scope 7 regional / 3 nationwide / 3 network; cause 6 government-directed / 3 cable-cut / 2 power-outage / 1 natural-disaster / 1 military-action; severity 7 MAJOR / 3 TOTAL / 3 PARTIAL; eight countries. Rewrote the intro, at-a-glance and reading sections. Observed-measurement, no-actor-position framing held ([[internet-outages]]).

- 2026-10-13 — daily-ingest synthesis (2026-W42): absorbed the 2026-10-12 → 2026-10-13 pulls — the active set eased to 11 outages (from 13 on 10-11) as Portugal's two cyberattack-labelled MEO/AS3243 disruptions aged off the rolling window, clearing the cyberattack cause category entirely; every other row held. Iraq held 6 government-directed exam-shutdown events (the 2026-09-26 → 2026-10-10 special round), Haiti and Guyana a cable-cut apiece, Eswatini and Cuba their nationwide power blackouts, and Panama its ongoing nationwide total natural-disaster outage (the M7.7 earthquake, detected 2026-10-10, no recorded end). Cause split 6 government-directed / 2 power-outage / 2 cable-cut / 1 natural-disaster; scope 6 regional / 2 network / 3 nationwide; severity 6 MAJOR / 2 PARTIAL / 3 TOTAL; six countries (from seven). Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections around the Portugal cyberattack rows aging off. Source-cause-only, no-position framing held ([[internet-outages]]).
- 2026-10-11 — daily-ingest synthesis (2026-W41): absorbed the 2026-10-09 → 2026-10-11 pulls — the active set firmed to 13 outages (from 12 on 10-08) as a fresh Panama nationwide total natural-disaster outage entered (the M7.7 earthquake cut Internet traffic across Panama, detected 2026-10-10, still ongoing) and the Honduras power blackout aged off, while a sixth Iraq exam-shutdown row re-entered. Iraq firmed to 6 government-directed exam-shutdown events (the 2026-09-26 → 2026-10-10 special round), Portugal held 2 cyberattack disruptions on MEO/AS3243, Haiti and Guyana a cable-cut apiece, and Eswatini and Cuba their nationwide power blackouts. Cause split 6 government-directed / 2 power-outage / 2 cyberattack / 2 cable-cut / 1 natural-disaster; scope 6 regional / 4 network / 3 nationwide; severity 6 MAJOR / 4 PARTIAL / 3 TOTAL; seven countries held. Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections around the Panama natural-disaster entry and the Honduras row aging off. Source-cause-only, no-position framing held ([[internet-outages]]).
- 2026-10-08 — daily-ingest synthesis (2026-W41): absorbed the 2026-10-07 and 2026-10-08 pulls — the active set eased to 12 outages (from 13 on 10-06) as one Iraq exam-shutdown detection row aged off the rolling window; the cause mix otherwise unchanged. Iraq eased to 5 government-directed exam-shutdown events (the 2026-09-26 → 2026-10-10 special round), Portugal held 2 cyberattack disruptions on MEO/AS3243, Haiti and Guyana a cable-cut apiece, and Eswatini, Cuba and Honduras their nationwide power blackouts — every non-Iraq row held. Cause split 5 government-directed / 3 power-outage / 2 cyberattack / 2 cable-cut; scope 5 regional / 4 network / 3 nationwide; severity 5 MAJOR / 4 PARTIAL / 3 TOTAL; seven countries held. Chokepoint-status channel still unsurfaced. Advanced the cutoff and reframed the intro, at-a-glance and reading sections around the single Iraq row clearing. Source-cause-only, no-position framing held ([[internet-outages]]).
- 2026-10-06 — daily-ingest synthesis (2026-W41): absorbed the 2026-10-05 and 2026-10-06 pulls — the active set grew to 13 outages (from 10 on 10-04) as a new cable-cut cause category entered: two network-level fibre cuts (Haiti's Digicel, Guyana's GT&T), alongside a fresh Eswatini (Swaziland) nationwide power outage. Iraq held 6 government-directed exam-shutdown events (the 2026-09-26 → 2026-10-10 special round), Portugal 2 cyberattack disruptions on MEO/AS3243, Cuba and Honduras their nationwide power blackouts — all held. Cause split 6 government-directed / 3 power-outage / 2 cyberattack / 2 cable-cut; scope 6 regional / 4 network / 3 nationwide; severity 6 MAJOR / 4 PARTIAL / 3 TOTAL; seven countries (from four). Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections around the cable-cut entry and the set growth. Source-cause-only, no-position framing held ([[internet-outages]]).
- 2026-10-04 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-04 pull, a clean hold. The active set held at 10 outages, byte-identical to 10-03 — the same cause split (6 government-directed / 2 cyberattack / 2 power-outage) and country set (Iraq 6, Portugal 2, Cuba 1, Honduras 1), no row aged off and no new cause category entered. Iraq still carries 6 of 10 (government-directed "exam shutdown" suspensions, the 2026-09-26 → 2026-10-10 special round), alongside two Portugal cyberattack disruptions, the Cuba nationwide blackout and the Honduras grid failure. Bumped the cutoff and logged the hold; no figure moved. Source-cause-only, no-position framing held ([[internet-outages]]).

- 2026-10-03 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-02 and 2026-10-03 pulls. The active set eased to 10 outages (from 11 on 10-01): one more Iraq exam-shutdown row aged off the rolling window, no new cause category entered, and the non-Iraq rows all held. Iraq dominates with 6 government-directed exam-shutdown events (the special round that started 2026-09-26, running through 2026-10-10); Portugal carries 2 cyberattack disruptions on MEO/AS3243, Cuba a nationwide blackout and Honduras a Central-America-interconnection grid failure. Cause split 6 government-directed / 2 power-outage / 2 cyberattack; severity 6 MAJOR / 2 TOTAL / 2 PARTIAL; scope 6 regional / 2 nationwide / 2 network; four countries. Chokepoint-status channel still unsurfaced (no L1 note in the 10-03 ingest). Rewrote the intro, at-a-glance and reading sections. Observed-only framing held; no position on any actor ([[internet-outages]]).
- 2026-10-01 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-01 pull. The active set eased to 11 outages (from 13 on 09-29, via 12 on 09-30): two more Iraq exam-shutdown rows aged off the rolling window, no new cause category entered. Iraq dominates with 7 government-directed exam-shutdown events (the special round that started 2026-09-26, running through 2026-10-10); Portugal carries 2 cyberattack disruptions on MEO/AS3243, Cuba a nationwide blackout and Honduras a Central-America-interconnection grid failure. Cause split 7 government-directed / 2 power-outage / 2 cyberattack; severity 7 MAJOR / 2 TOTAL / 2 PARTIAL; scope 7 regional / 2 nationwide / 2 network; four countries. Chokepoint-status channel still unsurfaced (no L1 note in the 10-01 ingest). Rewrote the intro, at-a-glance and reading sections. Observed-only framing held; no position on any actor ([[internet-outages]]).
- 2026-09-30 — daily-ingest synthesis (2026-W40): absorbed the 2026-09-29 pull. The active set now carries 13 outages (from the 16 last content-synced on 09-24): the Nepal flooding natural-disaster event and part of the Iraq exam-shutdown run aged off the rolling window, and no new cause category entered. Iraq dominates with 9 government-directed exam-shutdown events (the special round that started 2026-09-26, running through 2026-10-10 — the Iraq rows rolled to fresh detections); Portugal carries 2 cyberattack disruptions on MEO/AS3243, Cuba a nationwide blackout and Honduras a Central-America-interconnection grid failure. Cause split 9 government-directed / 2 power-outage / 2 cyberattack; severity 9 MAJOR / 2 TOTAL / 2 PARTIAL; scope 9 regional / 2 nationwide / 2 network; four countries (from five, Nepal off). Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections. Observed-only framing held; no position on any actor ([[internet-outages]]).
- 2026-09-24 — daily-ingest synthesis (2026-W39): day-over-day print vs 2026-09-23. The active set eased from 17 to 16 outages as one Iraq "exam shutdown" event (cf-1653, detected 2026-08-27) aged out of the rolling window — no new outage entered. Iraq still dominates with 11 of the 16 events (down from 12), all government-directed; Portugal (2 cyberattack), Cuba (1 nationwide blackout), Honduras (1 grid failure) and Nepal (1 natural-disaster) carried unchanged. Cause split 11 government-directed / 2 power-outage / 2 cyberattack / 1 natural-disaster; severity 12 MAJOR / 2 TOTAL / 2 PARTIAL (down one MAJOR); scope 12 regional / 2 nationwide / 2 network. Chokepoint-status channel still unsurfaced. Rewrote the intro, at-a-glance and reading sections. Observed-only framing held; no position on any actor ([[internet-outages]]).
- 2026-09-23 — daily-ingest synthesis (2026-W39): absorbed the 2026-09-22 ingest after a 20-day curator gap — the active set grew to 18 outages and its composition turned over almost entirely. Iraq now dominates with 13 government-directed "exam shutdown" events (2026-08-26 → 09-10); Portugal carries 2 cyberattack disruptions on MEO/AS3243 (the first cyberattack-cause readings in the brief), Cuba a multi-day nationwide blackout (09-18 → 09-21), Honduras a Central-America-interconnection grid failure and Nepal a flooding outage. Cause split 13 government-directed / 2 power-outage / 2 cyberattack / 1 natural-disaster; severity 14 MAJOR / 2 TOTAL / 2 PARTIAL; scope 14 regional / 2 nationwide / 2 network. The prior per-country set (Tajikistan, Ukraine, Colombia, Gabon, Georgia, earlier Cuba) all aged off. Chokepoint-status channel still unsurfaced (no note in the 09-22 ingest). Rewrote the intro, at-a-glance, honest-scope and reading sections. Observed-only framing held; no position on any actor ([[internet-outages]]).

- 2026-09-02 — daily-ingest synthesis (2026-W36): absorbed the 2026-09-01 ingest (adjacent to 08-31); active set grew from 12 to 14 outages (4 nationwide / 10 regional; cause split now 6 government-directed / 6 power-outage / 2 natural-disaster; severity 10 MAJOR / 4 TOTAL, from 8/4) as two more Iraq government-directed disruptions (cf-1657, cf-1658) entered — extending the exam-shutdown run — with no event ageing out; Iraq now carries 6 of the 14 events across nine holding countries, and one event (cf-1658) is still open-ended at the pull. Rewrote the intro and at-a-glance around the two new entries. Observed-only framing held, no political or safety side taken on the Iraq government-directed events ([[internet-outages]]).
- 2026-08-31 — daily-ingest synthesis (2026-W36): absorbed the 2026-08-21 through 2026-08-31 ingests after an 11-day curator gap; active set moved from 7 to 12 outages (4 nationwide / 8 regional; 6 power-outage, 4 government-directed, 2 natural-disaster) as four Iraq exam-shutdown events (cf-1652/cf-1653/cf-1655/cf-1656), one Nepal flooding event (cf-1654) and one Botswana nationwide power outage (cf-1651) entered while Kenya's cf-1641 aged out; government-directed events return for the first time since the 08-17 brief's zero reading, all four in Iraq; the six other 08-20 events (Tajikistan, Ukraine, Colombia, Gabon, Georgia, Cuba) carried unchanged; at-a-glance and reading rewritten accordingly. Observed-only framing held, no political or safety side taken on the Iraq government-directed events ([[internet-outages]]).
- 2026-08-17 — daily-ingest synthesis (2026-W34): absorbed the window to 2026-08-17 after a 16-day curator gap; active set moved from 6 to 7 outages (4 nationwide / 3 regional; 6 power-outage, 1 natural-disaster, 0 government-directed) as near-total turnover replaced five of the six 08-01 events — Cuba's cf-1632/cf-1637, Iraq's cf-1631/cf-1634 and Ukraine's cf-1633 all aged out — with six new entrants (Tajikistan cf-1649, Ukraine cf-1647, Colombia cf-1645, Gabon cf-1646, Georgia cf-1644, Cuba cf-1643); only Kenya's cf-1641 (detected 2026-07-29) carried forward unchanged; first natural-disaster reading since the Venezuela event cleared on 2026-07-23, and the first zero-government-directed reading on record; at-a-glance and reading rewritten accordingly. Observed-only framing held ([[internet-outages]]).
- 2026-08-01 — daily-ingest synthesis (2026-W31): absorbed the 2026-07-31 and 2026-08-01 pulls; active set expanded from 5 to 6 outages (4 nationwide / 2 regional; 4 power-outage, 2 government-directed; Cuba 2, Iraq 2, Kenya 1, Ukraine 1) as a new Kenya nationwide total-severity POWER OUTAGE (cf-1641, detected 2026-07-29, a national grid failure dropping internet traffic across the Coast and Central regions) entered; the five carried events (Cuba cf-1637/cf-1632, Iraq cf-1631/cf-1634, Ukraine cf-1633) held unchanged; at-a-glance and reading updated accordingly ([[internet-outages]]).
- 2026-07-25 — daily-ingest synthesis (2026-W30): flat cycle — 2026-07-25 pull byte-identical to 07-24 (same 8 events, same IDs, same split: 5 nationwide / 3 regional; 4 government-directed, 4 power; Iraq 4, Cuba 2, Ukraine 1, Tanzania 1); values carried, no movement to report; `updated` and pull-date advanced ([[internet-outages]]).
- 2026-07-30 — daily-ingest synthesis (2026-W31): absorbed the 2026-07-26 through 2026-07-30 pulls after a five-day gap behind the live L1; active set contracted from 8 to 5 outages (3 nationwide / 2 regional; 3 power, 2 government-directed; Cuba 2, Iraq 2, Ukraine 1) as the Tanzania power event and two of Iraq's four exam-shutdown entries aged out; five remaining events detected 2026-07-05 to 07-14, none new in the window; at-a-glance and reading rewritten accordingly ([[internet-outages]]).
- 2026-07-24 — daily-ingest synthesis (2026-W30): flat cycle — 2026-07-24 pull is byte-identical to 07-23 (same 8 events, same IDs, same split: 5 nationwide / 3 regional; 4 government-directed, 4 power; Iraq 4, Cuba 2, Ukraine 1, Tanzania 1); values carried, no movement to report ([[internet-outages]]).
- 2026-07-23 — daily-ingest synthesis (2026-W30): Venezuela natural-disaster event cleared; active set moves from 9 to 8 outages (5 nationwide / 3 regional; 4 government-directed, 4 power, 0 natural-disaster; Iraq 4, Cuba 2, Ukraine 1, Tanzania 1); at-a-glance and reading updated accordingly ([[internet-outages]]).
- 2026-07-21 — daily-ingest flowback (2026-W30): an honest flat cycle. The 2026-07-18, 07-19 and 07-20 Cloudflare Radar pulls held the active set byte-identical to 07-17 (9 outages — 6 nationwide / 3 regional; 4 government-directed, 4 power, 1 natural-disaster; Iraq 4, Cuba 2) apart from the retrieval timestamp; no event entered or exited. `week` and `updated` advanced so the freshness gate records the latest L1 day was absorbed ([[internet-outages]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): feed stable at 9 outages (6 nationwide / 3 regional; 4 government-directed, 4 power, 1 natural-disaster); net addition since 07-15 brief = cf-1637 (Cuba, nationwide power outage, total severity, detected 2026-07-15); Cuba moves from 1 to 2 recorded events; 07-16 and 07-17 pulls identical ([[internet-outages]]).
- 2026-07-15 — first Infrastructure Watch Weekly cycle (2026-W29): theme un-held (the hold
  was ingest-pending; the Cloudflare Radar channel is license-cleared, surfaced, and carries
  21 committed L1 days; the PortWatch channel is still not surfaced — honest-scope note).
  Wrote the at-a-glance and reading sections from the live 2026-07-15 pull: 8 outages
  (5 nationwide / 3 regional; 4 government-directed, 3 power, 1 natural-disaster; Iraq 4).
  Observed-only framing, source cause-labels reported as published ([[internet-outages]]).
- 2026-08-20 — daily-ingest synthesis (2026-W34): flat cycle — active set held at 7 outages (4 nationwide / 3 regional; 6 power-outage, 1 natural-disaster, 0 government-directed), unchanged from 08-17, with the 08-18 through 08-20 pulls byte-identical to each other; the window's sole field-level move was Tajikistan's cf-1649 gaining a recorded end time (2026-08-14 14:00 UTC, a ~4h15m outage) in the 08-18 pull, closing the set's one previously open-ended event; the chokepoint-status channel remains unsurfaced (HTTP 404 hold since 2026-06-25, reconfirmed today, zero L1 notes to date). Observed-only framing held ([[internet-outages]]).
