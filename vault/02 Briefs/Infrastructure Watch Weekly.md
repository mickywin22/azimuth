---
title: Infrastructure Watch Weekly
type: L2-brief
theme: infrastructure-watch
week: 2026-W30
updated: 2026-07-23T09:00:00Z
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
> date of current cycle: 2026-07-23.)

## This week at a glance

- The Cloudflare Radar channel records **8 active internet outages**: **5 nationwide** and
  **3 regional** in scope. By the source's own cause category: **4 government-directed**
  and **4 power-outage** ([[internet-outages]]).
- **Iraq accounts for 4 of the 8 events** — all carried with the source's
  GOVERNMENT DIRECTED cause label — and **Cuba holds 2 recorded events**, both
  attributed to nationwide power-grid failure, with single events recorded in Ukraine
  and Tanzania ([[internet-outages]]).
- Compared to the 2026-07-21 pull: the Venezuela natural-disaster event (cf-1625 era) has
  exited the active set; the remaining 8 events are held entries from prior pulls; no new
  event entered on the 2026-07-23 pull ([[internet-outages]]).

## Honest scope

- The theme registry lists a second channel (IMF PortWatch chokepoint status) that is not
  yet surfaced by the upstream API; this brief scopes to the live internet-outage channel
  and widens when the second channel lands ([[internet-outages]]).

## Reading the week

- Iraq's four events (all source-labelled GOVERNMENT DIRECTED) dominate the slate. Two are
  nationwide total-severity events (cf-1631 affecting KNET and Newroz-Telecom-ASN;
  cf-1629 affecting Earthlink-DMCC-IQ and HulumTele) and two are regional major-severity
  events (cf-1634 and cf-1625, both affecting KNET and Newroz-Telecom-ASN). The source
  describes each as an exam shutdown ([[internet-outages]]).
- Cuba carries two nationwide total-severity outages, both source-labelled POWER OUTAGE
  and attributed to power-grid failure: cf-1632 (detected 2026-07-13, carrier ETECSA) and
  cf-1637 (detected 2026-07-15, carrier ETECSA) ([[internet-outages]]).
- Ukraine holds one regional major-severity event (cf-1633, source-labelled POWER OUTAGE,
  Sevastopol) and Tanzania holds one nationwide total-severity event (cf-1626,
  source-labelled POWER OUTAGE, carriers TTCLDATA and simbanet-tz) ([[internet-outages]]).
- The Venezuela natural-disaster event that appeared in prior pulls is no longer present in
  the 2026-07-23 active set ([[internet-outages]]).
- azimuth reports the measurements and the source's cause labels, and stops there
  ([[internet-outages]]).

## Changelog

- 2026-07-23 — daily-ingest synthesis (2026-W30): Venezuela natural-disaster event cleared; active set moves from 9 to 8 outages (5 nationwide / 3 regional; 4 government-directed, 4 power, 0 natural-disaster; Iraq 4, Cuba 2, Ukraine 1, Tanzania 1); at-a-glance and reading updated accordingly ([[internet-outages]]).
- 2026-07-21 — daily-ingest flowback (2026-W30): an honest flat cycle. The 2026-07-18, 07-19 and 07-20 Cloudflare Radar pulls held the active set byte-identical to 07-17 (9 outages — 6 nationwide / 3 regional; 4 government-directed, 4 power, 1 natural-disaster; Iraq 4, Cuba 2) apart from the retrieval timestamp; no event entered or exited. `week` and `updated` advanced so the freshness gate records the latest L1 day was absorbed ([[internet-outages]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): feed stable at 9 outages (6 nationwide / 3 regional; 4 government-directed, 4 power, 1 natural-disaster); net addition since 07-15 brief = cf-1637 (Cuba, nationwide power outage, total severity, detected 2026-07-15); Cuba moves from 1 to 2 recorded events; 07-16 and 07-17 pulls identical ([[internet-outages]]).
- 2026-07-15 — first Infrastructure Watch Weekly cycle (2026-W29): theme un-held (the hold
  was ingest-pending; the Cloudflare Radar channel is license-cleared, surfaced, and carries
  21 committed L1 days; the PortWatch channel is still not surfaced — honest-scope note).
  Wrote the at-a-glance and reading sections from the live 2026-07-15 pull: 8 outages
  (5 nationwide / 3 regional; 4 government-directed, 3 power, 1 natural-disaster; Iraq 4).
  Observed-only framing, source cause-labels reported as published ([[internet-outages]]).
