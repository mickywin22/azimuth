---
title: Conflict Watch Weekly
type: L2-brief
theme: conflict-watch
week: 2026-W29
updated: 2026-07-18T09:00:00Z
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
  wire. The 2026-07-17 pull carries **2,000 events dated 2025-05-28 through 2025-12-31**: a
  wider window than the prior reading (which started 2025-11-05), reflecting a UCDP dataset
  refresh that extended the published record back to late May 2025. The brief describes the
  most recent *published* conflict record, and says so ([[conflict-events-ucdp]]).

## This window at a glance

- The 2,000 recorded events carry a summed best-estimate of **78,517 fatalities** (UCDP's
  `deathsBest` field — the source's own estimate, reported as published). By violence type:
  **976 state-based** events, **690 non-state** and **334 one-sided** ([[conflict-events-ucdp]]).
- **Mexico leads the event count at 310**, driven by non-state cartel-on-cartel violence
  (the Jalisco Cartel New Generation vs Sinaloa Cartel factions account for the largest
  single-dyad totals). **Ukraine follows at 291**, with the Russia–Ukraine state-based dyad
  (306 events naming those two governments) dominating that country's record. **Ethiopia
  is third at 212**, led by the government–Fano dyad at 177 events. **Brazil (191)** and
  **DR Congo (141)** round out the top five ([[conflict-events-ucdp]]).
- The top five countries account for 1,145 of 2,000 records. **Sudan records the highest
  summed deathsBest at 60,264 across 63 events** — a single large-fatality window that
  dominates the aggregate; Ukraine follows at 11,649 ([[conflict-events-ucdp]]).
- The spread is wide: 10+ countries each record more than 50 events across the window, with
  a long tail through Burkina Faso (62), Yemen (64), Nigeria (66) and beyond
  ([[conflict-events-ucdp]]).

## Move since prior reading (2026-07-16 → 2026-07-17)

- The UCDP dataset window **extended backwards from 2025-11-05 to 2025-05-28**, adding
  approximately six months of additional published records. Event totals remain at 2,000
  (the API cap), but the composition shifted: state-based events fell from 1,266 to 976,
  non-state rose from 505 to 690, and one-sided rose from 229 to 334. These reflect a
  different slice of the UCDP corpus, not a drop in recorded state-based activity
  ([[conflict-events-ucdp]]).
- Country rankings shifted accordingly: Ukraine dropped from first (536 events) to second
  (291), Mexico moved to first (310 vs 317 prior), and Ethiopia rose sharply from fifth (96)
  to third (212). Pakistan, which ranked third in the prior window at 175, does not appear
  in the top five of the new window ([[conflict-events-ucdp]]).
- The summed deathsBest rose from 15,012 to 78,517, almost entirely driven by Sudan's
  60,264 entering the wider window — an observed artefact of the dataset date extension,
  not a new event ([[conflict-events-ucdp]]).

## Reading the window

- Read as a record, not a forecast: the published window shows organised-crime violence
  (Mexico, Brazil) and state-based warfare (Ukraine, Ethiopia, Sudan) as the largest
  contributors by event count and fatality estimate respectively. azimuth reports the
  recorded events, the parties as UCDP names them, and the source's own fatality
  estimates — and stops there. Where UCDP extends or revises its published window
  (as occurred between the 07-16 and 07-17 pulls), the next cycle carries the new
  dataset composition as the observed fact ([[conflict-events-ucdp]]).

## Changelog

- 2026-07-18 — daily-ingest synthesis (2026-W29): UCDP dataset window extended to 2025-05-28 → 2025-12-31 (was 2025-11-05); 2,000 events, 78,517 summed deathsBest (up from 15,012, driven by Sudan 60,264 entering the wider window); 976/690/334 state-based/non-state/one-sided; Mexico 310 / Ukraine 291 / Ethiopia 212 lead by event count ([[conflict-events-ucdp]]).
- 2026-07-15 — first Conflict Watch Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the UCDP channel is license-clean CC-BY-4.0, surfaced, and carries 21
  committed L1 days). Wrote the honest-scope (publication lag), at-a-glance and reading
  sections from the live 2026-07-15 pull: 2,000 events (2025-11-05 → 2025-12-31), 15,012
  summed best-estimate fatalities, 1,266/505/229 state-based/non-state/one-sided, Ukraine
  536 / Mexico 317 / Pakistan 175 leading. Observed-only, no-position framing throughout
  ([[conflict-events-ucdp]]).
