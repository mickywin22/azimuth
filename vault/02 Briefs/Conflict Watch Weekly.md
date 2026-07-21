---
title: Conflict Watch Weekly
type: L2-brief
theme: conflict-watch
week: 2026-W30
updated: 2026-07-21T09:00:00Z
sources: [conflict-events-ucdp]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Conflict Watch Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded conflict
> events** — who, where, when, and the source's own fatality estimate — and never assigns
> blame, takes a side, or predicts escalation: an event record is an observed fact, an opinion
> about it is not surfaced (the editorial line). Every claim links to the L1 note it rests on.

## Honest scope — a lagged research dataset, not a live wire

- The channel is the **UCDP** (Uppsala Conflict Data Program) georeferenced event feed — a
  research-grade dataset published with a deliberate verification lag, not a breaking-news
  wire. The 2026-07-20 pull carries **2,000 events dated 2025-11-05 through 2025-12-31** — the
  window contracted back from the transient 2025-05-28 start the 07-17 pull briefly showed,
  reverting to the same slice the 07-15 baseline carried. The brief describes the
  most recent *published* conflict record, and says so ([[conflict-events-ucdp]]).

## This window at a glance

- The 2,000 recorded events carry a summed best-estimate of **15,012 fatalities** (UCDP's
  `deathsBest` field — the source's own estimate, reported as published). By violence type:
  **1,266 state-based** events, **505 non-state** and **229 one-sided** ([[conflict-events-ucdp]]).
- **Ukraine leads the event count at 536**, the Russia–Ukraine state-based dyad dominating that
  country's record. **Mexico follows at 317**, driven by non-state cartel-on-cartel violence,
  and **Pakistan is third at 175**. **DR Congo (96)** and **Ethiopia (96)** round out the top
  five ([[conflict-events-ucdp]]).
- The top five countries account for 1,220 of 2,000 records. **Ukraine also records the highest
  summed deathsBest at 10,051** — the fatality estimate concentrated on the Russia–Ukraine war
  in this window — ahead of Ethiopia (662), Sudan (639), Pakistan (501) and DR Congo (500)
  ([[conflict-events-ucdp]]).
- The spread is wide: **11 countries each record more than 50 events** across the window, a long
  tail through Brazil (51), Nigeria (56), Colombia (63), Yemen (63), Myanmar (69) and Burkina
  Faso (70) ([[conflict-events-ucdp]]).

## Move since prior reading (2026-07-17 → 2026-07-20)

- The UCDP dataset window **contracted back from 2025-05-28 to 2025-11-05**, dropping the
  roughly six months of older records the 07-17 pull had briefly carried. Event totals hold at
  2,000 (the API cap), but the composition returned to the narrower slice: state-based events
  rose from 976 back to 1,266, non-state fell from 690 to 505, and one-sided fell from 334 to
  229 ([[conflict-events-ucdp]]).
- Country rankings reverted accordingly: Ukraine returned to first (536 events, from second at
  291), Mexico back to second (317, from first at 310), and Pakistan re-entered the top three at
  175; Ethiopia fell from third (212) back to a tie for fourth at 96. This mirrors the 07-15
  baseline composition exactly ([[conflict-events-ucdp]]).
- The summed deathsBest fell from 78,517 back to 15,012 as Sudan's 60,264-fatality window (an
  artefact of the transient date extension) dropped out — an observed dataset-composition change,
  not a change in recorded events on the ground ([[conflict-events-ucdp]]).

## Reading the window

- Read as a record, not a forecast: the published window shows organised-crime violence
  (Mexico, Brazil, Colombia) leading by event count and state-based warfare (Ukraine foremost,
  10,051 of the 15,012 summed deathsBest) leading by fatality estimate. azimuth reports the
  recorded events, the parties as UCDP names them, and the source's own fatality
  estimates — and stops there. Where UCDP extends, contracts or revises its published window
  (the 07-17 pull briefly widened to 2025-05-28 before the 07-20 pull reverted to 2025-11-05),
  each cycle carries the new dataset composition as the observed fact ([[conflict-events-ucdp]]).

## Changelog

- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 pulls. The UCDP window contracted back from the transient 07-17 extension (2025-05-28 → 2025-12-31) to 2025-11-05 → 2025-12-31 — the 07-15 baseline slice. 2,000 events; summed deathsBest fell from 78,517 back to 15,012 (Sudan's 60,264-fatality window dropped out); violence-type split returned to 1,266 state / 505 non-state / 229 one-sided; Ukraine 536 / Mexico 317 / Pakistan 175 lead by event count, Ukraine also the fatality leader at 10,051. Rewrote the honest-scope, at-a-glance, move and reading sections ([[conflict-events-ucdp]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): UCDP dataset window extended to 2025-05-28 → 2025-12-31 (was 2025-11-05); 2,000 events, 78,517 summed deathsBest (up from 15,012, driven by Sudan 60,264 entering the wider window); 976/690/334 state-based/non-state/one-sided; Mexico 310 / Ukraine 291 / Ethiopia 212 lead by event count ([[conflict-events-ucdp]]).
- 2026-07-15 — first Conflict Watch Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the UCDP channel is license-clean CC-BY-4.0, surfaced, and carries 21
  committed L1 days). Wrote the honest-scope (publication lag), at-a-glance and reading
  sections from the live 2026-07-15 pull: 2,000 events (2025-11-05 → 2025-12-31), 15,012
  summed best-estimate fatalities, 1,266/505/229 state-based/non-state/one-sided, Ukraine
  536 / Mexico 317 / Pakistan 175 leading. Observed-only, no-position framing throughout
  ([[conflict-events-ucdp]]).
