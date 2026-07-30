---
title: Conflict Watch Weekly
type: L2-brief
theme: conflict-watch
week: 2026-W31
updated: 2026-07-30T09:00:00Z
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
> Last pull: **2026-07-30**.

## Honest scope — a lagged research dataset, not a live wire

- The channel is the **UCDP** (Uppsala Conflict Data Program) georeferenced event feed — a
  research-grade dataset published with a verification lag, not a breaking-news wire. The
  2026-07-30 pull carries **2,000 events** — a rolling catalog capped at the API maximum. This
  cycle the published window **rolled forward roughly seven months**: from the late-2025 slice
  (2025-11-05 → 2025-12-31) that had held for weeks to **2025-12-22 → 2026-07-08**, so the catalog
  now reaches to within weeks of the present. The brief describes the most recent *published*
  conflict record, and says so ([[conflict-events-ucdp]]).

## This window at a glance

- The 2,000 recorded events carry a summed best-estimate of **6,006 fatalities** (UCDP's
  `deathsBest` field — the source's own estimate, reported as published), **down from 15,012** in
  the prior late-2025 window as the newer, lower-fatality-density 2026 events entered. By violence
  type: **1,247 state-based** events, **463 non-state** and **290 one-sided**
  ([[conflict-events-ucdp]]).
- **Ukraine leads the event count at 451**, the Russia–Ukraine state-based dyad still dominant.
  **Colombia follows at 197** and **Nigeria at 170**, then **Pakistan (162)** and **Mexico (158)**;
  **Ethiopia (88)**, **Mali (74)**, **Lebanon (72)**, **Israel (62)** and **Sudan (59)** complete
  the top ten — a markedly different leaderboard from the prior window (Ukraine / Mexico / Pakistan)
  as the catalog advanced into 2026 ([[conflict-events-ucdp]]).
- **Ukraine also records the highest summed deathsBest at 962** — the fatality estimate still
  concentrated on the Russia–Ukraine dyad — ahead of **Nigeria (762)**, **Sudan (504)**,
  **Pakistan (481)**, **Somalia (476)** and **Ethiopia (470)**. The fatality ranking is far flatter
  than the prior window, where Ukraine alone carried 10,051 of 15,012 ([[conflict-events-ucdp]]).
- The spread widened: **13 countries each record more than 50 events** across the window (from 11),
  a long tail now running through Sudan (59), Israel (62), Lebanon (72) and Mali (74)
  ([[conflict-events-ucdp]]).

## Move since prior reading (2026-07-25 → 2026-07-30)

- The 07-30 pull is a **major catalog roll-forward**, not a flat cycle: the published window
  advanced from **2025-11-05 → 2025-12-31** to **2025-12-22 → 2026-07-08**, dropping most of the
  late-2025 slice and adding six months of 2026 events. Total events stay at the 2,000 API cap,
  but summed deathsBest fell from **15,012 to 6,006** as the high-fatality late-2025 Ukraine rows
  aged out of the window ([[conflict-events-ucdp]]).
- The country leaderboard turned over: Ukraine remains first but eased from 536 to **451 events**;
  Mexico fell from second (317) to fifth (158); **Colombia (197)** and **Nigeria (170)** rose into
  second and third, and **Mali, Lebanon and Israel** entered the top ten — the composition tracking
  the catalog's advance into 2026 ([[conflict-events-ucdp]]).
- The violence-type split shifted toward one-sided and away from non-state: **1,247 state-based /
  463 non-state / 290 one-sided** (from 1,266 / 505 / 229). azimuth reports the new published
  composition as the observed fact; where the prior weeks recorded a stable window, this cycle
  records its roll-forward ([[conflict-events-ucdp]]).

## Reading the window

- Read as a record, not a forecast: the newly-published window shows the Russia–Ukraine
  state-based dyad still leading both event count (Ukraine 451) and fatality estimate (Ukraine
  962), but with a far flatter fatality distribution than the prior late-2025 slice — Nigeria
  (762), Sudan (504), Pakistan (481) and Somalia (476) now sit close behind. azimuth reports the
  recorded events, the parties as UCDP names them, and the source's own fatality estimates — and
  stops there. Where UCDP extends, contracts or revises its published window, each cycle carries the
  new dataset composition as the observed fact; this cycle the dataset rolled its window forward
  ~7 months into 2026, and that roll-forward is itself the reported observation
  ([[conflict-events-ucdp]]).

## Changelog

- 2026-07-30 — daily-ingest synthesis (2026-W31): absorbed the 07-26 through 07-30 pulls after a 5-day curator gap — a MAJOR catalog roll-forward, not a flat cycle. The UCDP published window advanced ~7 months from 2025-11-05 → 2025-12-31 to 2025-12-22 → 2026-07-08 (now reaching within weeks of the present). 2,000 events (API cap); summed deathsBest fell 15,012 → 6,006 as the high-fatality late-2025 Ukraine rows aged out; violence split 1,266/505/229 → 1,247/463/290 state-based/non-state/one-sided. Leaderboard turned over: Ukraine 451 (first, from 536), Colombia 197 (2nd), Nigeria 170 (3rd), Pakistan 162, Mexico 158 (from 2nd); Mali/Lebanon/Israel entered the top ten. Fatality ranking flattened: Ukraine 962 / Nigeria 762 / Sudan 504 / Pakistan 481 / Somalia 476 / Ethiopia 470 (from Ukraine 10,051 alone). 13 countries >50 events (from 11). Rewrote honest-scope, at-a-glance, move and reading sections; observed-only, no-position framing held ([[conflict-events-ucdp]]).
- 2026-07-25 — daily-ingest synthesis (2026-W30): 07-25 pull byte-identical to 07-24 — dataset composition unchanged: 2,000 events, 15,012 summed deathsBest, 1,266/505/229 state-based/non-state/one-sided, catalog window 2025-11-05 to 2025-12-31, Ukraine 536 / Mexico 317 / Pakistan 175 / DR Congo+Ethiopia 96 / Burkina Faso 70 all carried; bumped updated date, advanced pull-date refs and move-section header (2026-07-24 → 2026-07-25), extended stable-window span note to 07-15 through 07-25 ([[conflict-events-ucdp]]).
- 2026-07-24 — daily-ingest synthesis (2026-W30): 07-24 pull confirms no fresh catalog rows landed this cycle — dataset composition identical to 07-23: 2,000 events, 15,012 summed deathsBest, 1,266/505/229 state-based/non-state/one-sided, catalog window 2025-11-05 to 2025-12-31 unchanged, Ukraine 536 / Mexico 317 / Pakistan 175 / DR Congo+Ethiopia 96 / Burkina Faso 70 all carried values; bumped updated date, refreshed pull-date in prose and move section header, extended stable-window span note to 07-15 through 07-24 ([[conflict-events-ucdp]]).
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
