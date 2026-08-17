---
title: Infrastructure Watch Weekly
type: L2-brief
theme: infrastructure-watch
week: 2026-W34
updated: 2026-08-17T09:00:00Z
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
> absorbs the window through 2026-08-17 after a 16-day curator gap (last synthesis:
> 2026-08-01). (Pull date of current cycle: 2026-08-17.)

## This week at a glance

- The Cloudflare Radar channel records **7 active internet outages**: **4 nationwide** and
  **3 regional** in scope. By the source's own cause category: **6 power-outage** and
  **1 natural-disaster** — the first cycle on record with **zero government-directed**
  events ([[internet-outages]]).
- **Each of the 7 holding countries carries exactly 1 event** — Tajikistan, Ukraine, Colombia,
  Gabon, Georgia, Cuba and Kenya — a wider spread than the 08-01 set, where Cuba and Iraq
  each held 2 of 6 ([[internet-outages]]).
- The active set **moved from 6 to 7** since the 2026-08-01 synthesis, but that headline
  number understates the churn across the 16-day gap: only Kenya's nationwide power outage
  (cf-1641, detected 2026-07-29) carried forward unchanged; both Cuba events, both Iraq
  events and the prior Ukraine event aged out, replaced by six new entrants
  ([[internet-outages]]).

## Honest scope

- The theme registry lists a second channel (IMF PortWatch chokepoint status) that is not
  yet surfaced by the upstream API; this brief scopes to the live internet-outage channel
  and widens when the second channel lands ([[internet-outages]]).

## Reading the week

- Tajikistan holds the newest entry: a nationwide total-severity power outage (cf-1649,
  detected 2026-08-14 10:45 UTC), source-described as a mass power outage reported by
  residents across several cities and districts; it is the only event in the set with no
  recorded end time as of the 2026-08-17 pull ([[internet-outages]]).
- Ukraine holds one regional major-severity event (cf-1647, source-labelled POWER OUTAGE,
  detected 2026-08-12 21:00 UTC and ended 2026-08-13 07:00 UTC — a 10-hour outage the source
  attributes to a drone strike on energy infrastructure in Russian-occupied Sevastopol,
  Crimea) — a different event from the Sevastopol outage carried in the 08-01 brief
  ([[internet-outages]]).
- Colombia holds one regional major-severity event (cf-1645, source-labelled NATURAL
  DISASTER, detected 2026-08-10 13:30 UTC and ended 2026-08-14 08:00 UTC — a 7.4-magnitude
  earthquake the source describes as causing building collapses and mass evacuations), the
  set's longest-running event at just over 90 hours and its only natural-disaster entry
  ([[internet-outages]]).
- Gabon holds one regional major-severity event (cf-1646, source-labelled POWER OUTAGE,
  detected 2026-08-08 18:00 UTC and ended 2026-08-08 21:15 UTC — a 3.25-hour outage the
  source attributes to a grid-transmission-line failure on the 225 kV Kinguélé–Bisségué line
  affecting Estuaire province) ([[internet-outages]]).
- Georgia holds one nationwide total-severity event (cf-1644, source-labelled POWER OUTAGE,
  detected 2026-08-05 17:00 UTC and ended 2026-08-05 18:45 UTC — a 1.75-hour outage the
  source attributes to testing at the Enguri hydroelectric plant) ([[internet-outages]]).
- Cuba holds one nationwide total-severity event (cf-1643, source-labelled POWER OUTAGE,
  detected 2026-08-03 03:45 UTC and ended 2026-08-04 13:00 UTC — a roughly 33-hour
  nationwide blackout), a new grid-failure episode distinct from the two Cuba events carried
  in the 08-01 brief ([[internet-outages]]).
- Kenya's nationwide total-severity power outage (cf-1641, detected 2026-07-29 18:15 UTC,
  ended 2026-07-29 22:45 UTC, a national grid failure that dropped internet traffic across
  the Coast and Central regions) is the sole event carried unchanged from the 2026-08-01
  synthesis ([[internet-outages]]).
- Iraq's two government-directed exam-shutdown events (cf-1631, cf-1634) and both Cuba
  events (cf-1632, cf-1637) that anchored the 08-01 active set are absent from the
  2026-08-17 pull ([[internet-outages]]).
- The 2026-08-16 pull was byte-identical to 2026-08-17 (same 7 events, same identifiers):
  the most recent single-day step was flat, and the movement described above spans the full
  16-day gap back to 2026-08-01 ([[internet-outages]]).
- azimuth reports the measurements and the source's cause labels, and stops there
  ([[internet-outages]]).

## Changelog

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
