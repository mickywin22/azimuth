---
title: Conflict Watch Weekly
type: L2-brief
theme: conflict-watch
week: 2026-W30
updated: 2026-07-23T09:00:00Z
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
> Last pull: **2026-07-23**.

## Honest scope — a lagged research dataset, not a live wire

- The channel is the **UCDP** (Uppsala Conflict Data Program) georeferenced event feed — a
  research-grade dataset published with a deliberate verification lag, not a breaking-news
  wire. The 2026-07-23 pull carries **2,000 events** — a rolling catalog capped at the API
  maximum, with event dates drawn from late 2025 (the dataset's own published verification
  window, not this week's fresh violence). The brief describes the most recent *published*
  conflict record, and says so ([[conflict-events-ucdp]]).

## This window at a glance

- The 2,000 recorded events carry a summed best-estimate of **15,012 fatalities** (UCDP's
  `deathsBest` field — the source's own estimate, reported as published). By violence type:
  **1,266 state-based** events, **505 non-state** and **229 one-sided** ([[conflict-events-ucdp]]).
- **Ukraine leads the event count at 536**, the Russia–Ukraine state-based dyad dominating that
  country's record. **Mexico follows at 317**, driven by non-state violence, and **Pakistan is
  third at 175**. **DR Congo (96)** and **Ethiopia (96)** are tied for fourth; **Burkina Faso
  (70)** follows in sixth ([[conflict-events-ucdp]]).
- The top five countries account for 1,220 of 2,000 records. **Ukraine also records the highest
  summed deathsBest at 10,051** — the fatality estimate concentrated on the Russia–Ukraine
  dyad in this window — ahead of Ethiopia (662), Sudan (639), Pakistan (501) and DR Congo (500)
  ([[conflict-events-ucdp]]).
- The spread is wide: **11 countries each record more than 50 events** across the window, a long
  tail through Brazil (51), Nigeria (56), Colombia (63), Yemen (63), Myanmar (69) and Burkina
  Faso (70) ([[conflict-events-ucdp]]).

## Move since prior reading (2026-07-20 → 2026-07-23)

- The 2026-07-23 pull **holds the same composition as the 07-20 pull**: 2,000 events, summed
  deathsBest of 15,012, violence-type split of 1,266 state-based / 505 non-state / 229
  one-sided. No window shift, no dataset reversion ([[conflict-events-ucdp]]).
- Country rankings are **unchanged**: Ukraine 536 (first), Mexico 317 (second), Pakistan 175
  (third), DR Congo and Ethiopia both at 96 (tied fourth), Burkina Faso 70 (sixth). The
  07-20 → 07-23 interval produced no observable change in the published record
  ([[conflict-events-ucdp]]).
- **Stable composition is itself an observed fact**: the UCDP feed's verification lag means the
  published window does not move with every daily pull; the 07-23 ingest confirms the dataset
  is resting on the same late-2025 slice first seen in the 07-15 baseline
  ([[conflict-events-ucdp]]).

## Reading the window

- Read as a record, not a forecast: the published window shows non-state violence
  (Mexico, Brazil, Colombia) leading by event count and state-based events (Ukraine foremost,
  10,051 of the 15,012 summed deathsBest) leading by fatality estimate. azimuth reports the
  recorded events, the parties as UCDP names them, and the source's own fatality
  estimates — and stops there. Where UCDP extends, contracts or revises its published window,
  each cycle carries the new dataset composition as the observed fact; where the dataset is
  stable across pulls (as from 07-15 through 07-23), that stability is itself the reported
  observation ([[conflict-events-ucdp]]).

## Changelog

- 2026-07-23 — daily-ingest synthesis (2026-W30): 07-23 pull confirms dataset composition stable vs 07-20 — 2,000 events, 15,012 summed deathsBest, 1,266/505/229 state-based/non-state/one-sided, Ukraine 536 / Mexico 317 / Pakistan 175 / DR Congo+Ethiopia 96 / Burkina Faso 70 unchanged; updated honest-scope pull-date, rewrote move section to reflect stable-composition finding, surfaced Burkina Faso (70) explicitly in at-a-glance, updated reading section to cover stable-window pattern ([[conflict-events-ucdp]]).
- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 pulls. The UCDP window contracted back from the transient 07-17 extension (2025-05-28 → 2025-12-31) to 2025-11-05 → 2025-12-31 — the 07-15 baseline slice. 2,000 events; summed deathsBest fell from 78,517 back to 15,012 (Sudan's 60,264-fatality window dropped out); violence-type split returned to 1,266 state / 505 non-state / 229 one-sided; Ukraine 536 / Mexico 317 / Pakistan 175 lead by event count, Ukraine also the fatality leader at 10,051. Rewrote the honest-scope, at-a-glance, move and reading sections ([[conflict-events-ucdp]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): UCDP dataset window extended to 2025-05-28 → 2025-12-31 (was 2025-11-05); 2,000 events, 78,517 summed deathsBest (up from 15,012, driven by Sudan 60,264 entering the wider window); 976/690/334 state-based/non-state/one-sided; Mexico 310 / Ukraine 291 / Ethiopia 212 lead by event count ([[conflict-events-ucdp]]).
- 2026-07-15 — first Conflict Watch Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the UCDP channel is license-clean CC-BY-4.0, surfaced, and carries 21
  committed L1 days). Wrote the honest-scope (publication lag), at-a-glance and reading
  sections from the live 2026-07-15 pull: 2,000 events (2025-11-05 → 2025-12-31), 15,012
  summed best-estimate fatalities, 1,266/505/229 state-based/non-state/one-sided, Ukraine
  536 / Mexico 317 / Pakistan 175 leading. Observed-only, no-position framing throughout
  ([[conflict-events-ucdp]]).
