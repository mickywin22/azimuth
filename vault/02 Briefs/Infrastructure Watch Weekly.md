---
title: Infrastructure Watch Weekly
type: L2-brief
theme: infrastructure-watch
week: 2026-W31
updated: 2026-08-01T09:00:00Z
sources: [internet-outages]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Infrastructure Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded
> infrastructure disruption events** — an internet outage is an observed network measurement
> (Cloudflare Radar), with the cause category the source itself assigns — and takes no
> position on any actor involved. Every claim links to the L1 note it rests on. (Pull
> date of current cycle: 2026-08-01.)

## This week at a glance

- The Cloudflare Radar channel records **6 active internet outages**: **4 nationwide** and
  **2 regional** in scope. By the source's own cause category: **4 power-outage**
  and **2 government-directed** ([[internet-outages]]).
- **Cuba and Iraq each hold 2 of the 6 events**, with single events in Kenya and Ukraine. Cuba's
  two are both source-labelled POWER OUTAGE (nationwide grid failure amid fuel shortages); Iraq's
  two both carry the GOVERNMENT DIRECTED label (exam shutdowns); Kenya's is a new nationwide
  POWER OUTAGE ([[internet-outages]]).
- The active set **expanded from 5 to 6** since the 2026-07-30 synthesis: a new Kenya nationwide
  power outage (cf-1641, detected 2026-07-29) entered, joining the carried Cuba (2), Iraq (2) and
  Ukraine (1) events detected between 2026-07-05 and 2026-07-14 ([[internet-outages]]).

## Honest scope

- The theme registry lists a second channel (IMF PortWatch chokepoint status) that is not
  yet surfaced by the upstream API; this brief scopes to the live internet-outage channel
  and widens when the second channel lands ([[internet-outages]]).

## Reading the week

- Iraq's two events are both source-labelled GOVERNMENT DIRECTED and described as exam
  shutdowns: a nationwide total-severity event (cf-1631, affecting KNET and Newroz-Telecom-ASN,
  detected 2026-07-05) and a regional major-severity event (cf-1634, same carriers, detected
  2026-07-08) ([[internet-outages]]).
- Cuba carries two nationwide total-severity outages, both source-labelled POWER OUTAGE and
  attributed to nationwide grid collapse amid fuel shortages: cf-1632 (detected 2026-07-06) and
  cf-1637 (detected 2026-07-14) ([[internet-outages]]).
- Ukraine holds one regional major-severity event (cf-1633, source-labelled POWER OUTAGE, a
  power blackout in Sevastopol, detected 2026-07-05) ([[internet-outages]]).
- Kenya holds one new nationwide total-severity event (cf-1641, source-labelled POWER OUTAGE, a
  national power grid failure that dropped internet traffic across the Coast and Central regions,
  detected 2026-07-29) — the one entrant this cycle ([[internet-outages]]).
- The Tanzania power event and two of Iraq's four exam-shutdown entries that appeared in prior
  pulls remain absent from the 2026-08-01 active set ([[internet-outages]]).
- azimuth reports the measurements and the source's cause labels, and stops there
  ([[internet-outages]]).

## Changelog

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
