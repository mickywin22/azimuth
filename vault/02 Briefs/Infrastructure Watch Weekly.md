---
title: Infrastructure Watch Weekly
type: L2-brief
theme: infrastructure-watch
week: 2026-W39
updated: 2026-09-23T10:14:00Z
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
> absorbs the 2026-09-22 pull after a 20-day curator gap: the active set grew to **18 outages**,
> and its composition shifted hard — **Iraq's recurring "exam shutdown" government-directed pattern
> now dominates with 13 of the 18 events**, alongside two Portugal cyberattack disruptions, a
> multi-day Cuba nationwide blackout, a Honduras grid failure and a Nepal flooding outage.
> (Pull date of current cycle: 2026-09-22.)

## This week at a glance

- The Cloudflare Radar channel records **18 active internet outages**: **2 nationwide**, **2
  network-level** and **14 regional** in scope. By the source's own cause category:
  **13 government-directed**, **2 power-outage**, **2 cyberattack** and **1 natural-disaster** —
  government-directed events now overwhelmingly the largest category ([[internet-outages]]).
- **Five countries hold the 18 events, and Iraq alone carries 13 of them** — the Iraq
  concentration deepened sharply, all 13 the source's recurring early-hours "exam shutdown"
  pattern; Portugal carries 2, and Cuba, Honduras and Nepal one apiece ([[internet-outages]]).
- The composition **turned over across the 20-day gap**: the entire prior per-country set
  (Tajikistan, Ukraine, Colombia, Gabon, Georgia, Cuba's earlier blackout) aged off, replaced by
  the Iraq exam-shutdown run plus a fresh Portugal cyberattack pair and a new multi-day Cuba
  blackout; severity now splits **14 MAJOR / 2 TOTAL / 2 PARTIAL** ([[internet-outages]]).

## Honest scope

- The theme registry lists a second channel (IMF PortWatch chokepoint status) that
  remains unsurfaced: the upstream endpoint has returned HTTP 404 since 2026-06-25, with zero
  committed L1 notes to date (no chokepoint-status note in the 2026-09-22 ingest); this brief
  scopes to the live internet-outage channel and widens when the second channel lands
  ([[internet-outages]]).

## Reading the week

- **Iraq dominates the set with 13 government-directed events**, all the source's recurring "exam
  shutdown" pattern — short (roughly 30-to-90-minute) regional internet suspensions in the early
  hours, recorded across 2026-08-26 → 2026-09-10. azimuth records the cause label the source
  assigns and takes no position on the practice ([[internet-outages]]).
- **Portugal holds two cyberattack-labelled events** — traffic disruptions observed on MEO
  (AS3243) on 2026-09-13 and 2026-09-14, both partial-severity and short (~45-105 minutes) — the
  first cyberattack-cause readings the brief has carried, the source's own category
  ([[internet-outages]]).
- **Cuba holds a nationwide total-severity power outage** (2026-09-18 → 2026-09-21, roughly three
  days), the source-described nationwide blackout the longest-running event in the current set
  ([[internet-outages]]).
- **Honduras holds a nationwide total-severity power outage** (2026-09-10, ~1.5 hours) that the
  source attributes to a failure in Central America's regional power-interconnection system dropping
  internet traffic across multiple providers ([[internet-outages]]).
- **Nepal holds one regional major-severity natural-disaster event** (2026-08-28, ~1h45m) the
  source attributes to regional flooding disrupting power supply across the Kathmandu Valley and
  central Nepal — the set's only natural-disaster entry this cycle ([[internet-outages]]).
- The composition turned over almost entirely across the 20-day curator gap: the prior set's
  Tajikistan, Ukraine, Colombia, Gabon, Georgia and earlier-Cuba events all aged off, and the Iraq
  exam-shutdown run plus the Portugal cyberattack pair and the multi-day Cuba blackout are the new
  anchors ([[internet-outages]]).
- azimuth reports the measurements and the source's cause labels, and stops there
  ([[internet-outages]]).

## Changelog

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
