---
title: Infrastructure Watch Weekly
type: L2-brief
theme: infrastructure-watch
week: 2026-W29
updated: 2026-07-18T09:00:00Z
sources: [internet-outages]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Infrastructure Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded
> infrastructure disruption events** — an internet outage is an observed network measurement
> (Cloudflare Radar), with the cause category the source itself assigns — and takes no
> position on any actor involved. Every claim links to the L1 note it rests on. (First
> cycle, written from the 2026-07-15 ingest.)

## This week at a glance

- The Cloudflare Radar channel records **9 active internet outages**: **6 nationwide** and
  **3 regional** in scope. By the source's own cause category: **4 government-directed**,
  **4 power-outage** and **1 natural-disaster** ([[internet-outages]]).
- **Iraq accounts for 4 of the 9 events** — all carried with the source's
  government-directed cause label — and **Cuba now holds 2 recorded events**, both
  attributed to nationwide power-grid failure, with single events recorded in Ukraine,
  Tanzania and Venezuela ([[internet-outages]]).
- The feed was stable between the 2026-07-16 and 2026-07-17 pulls: no new events entered
  or exited the active set in that window ([[internet-outages]]).

## Honest scope

- The theme registry lists a second channel (IMF PortWatch chokepoint status) that is not
  yet surfaced by the upstream API; this brief scopes to the live internet-outage channel
  and widens when the second channel lands ([[internet-outages]]).

## Reading the week

- Iraq's four government-directed events (the feed's own cause label) dominate the slate;
  three are nationwide and one is regional. The source describes each as an exam-period
  shutdown affecting networks including KNET, Newroz-Telecom-ASN, Earthlink-DMCC-IQ, and
  HulumTele ([[internet-outages]]).
- Cuba carries two separate nationwide total-severity outages this week, both attributed by
  the source to power-grid failure; one was detected on 2026-07-13 (cf-1632) and the second
  on 2026-07-15 (cf-1637, the addition since the last brief cycle) ([[internet-outages]]).
- The remaining three events are one regional power-outage in Ukraine (Sevastopol), one
  nationwide power-grid failure in Tanzania affecting multiple ISPs, and one nationwide
  natural-disaster event in Venezuela attributed to a magnitude-7.5 earthquake ([[internet-outages]]).
- azimuth reports the measurements and the source's cause labels, and stops there
  ([[internet-outages]]).

## Changelog

- 2026-07-18 — daily-ingest synthesis (2026-W29): feed stable at 9 outages (6 nationwide / 3 regional; 4 government-directed, 4 power, 1 natural-disaster); net addition since 07-15 brief = cf-1637 (Cuba, nationwide power outage, total severity, detected 2026-07-15); Cuba moves from 1 to 2 recorded events; 07-16 and 07-17 pulls identical ([[internet-outages]]).
- 2026-07-15 — first Infrastructure Watch Weekly cycle (2026-W29): theme un-held (the hold
  was ingest-pending; the Cloudflare Radar channel is license-cleared, surfaced, and carries
  21 committed L1 days; the PortWatch channel is still not surfaced — honest-scope note).
  Wrote the at-a-glance and reading sections from the live 2026-07-15 pull: 8 outages
  (5 nationwide / 3 regional; 4 government-directed, 3 power, 1 natural-disaster; Iraq 4).
  Observed-only framing, source cause-labels reported as published ([[internet-outages]]).
