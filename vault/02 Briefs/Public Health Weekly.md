---
title: Public Health Weekly
type: L2-brief
theme: public-health
week: 2026-W36
updated: 2026-09-02T09:54:00Z
sources: [disease-outbreaks]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Public Health Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded disease
> outbreak notifications** — the disease, the place, the case count and the alert level as the
> reporting body published them — never a health prediction, never advice. Every claim links
> to the L1 note it rests on. (Updated from the 2026-09-01 ingest, which held the
> 08-31 aggregate exactly — identical notification, alert-band, disease and country counts and
> identical per-notification case counts — so this cycle restores the case-count leaderboard the
> feed does in fact carry, which the prior cycle had retired on a mistaken read that no case data
> was supplied.)

## This week at a glance

- The WHO / CDC outbreak channel carries **158 active outbreak notifications** on the 2026-09-01
  pull — **119 watch / 39 alert** — **held exactly** from the 08-31 pull (same counts, same alert
  bands, same per-notification case figures); the picture below is the current recorded slate, not
  a fresh move ([[disease-outbreaks]]).
- **Highest single case counts** the feed carries this pull: a **58,000-case Chicken Pox
  notification in Gaza City** (watch) tops the slate, ahead of a **50,820-case Measles alert in the
  Democratic Republic of Congo**, two Guatemala City measles alerts (**27,145** and **21,700**),
  three Bangladesh measles alerts (**18,726 / 17,800 / 16,408**) and a Mongolia measles watch
  (**15,475**); US measles national notifications lead at 2,318 (watch) across 17 US measles
  entries ([[disease-outbreaks]]).
- **Measles remains the largest disease category** at **65 of 158 notifications**, ahead of
  Unknown Disease (26) and **polio (22)**; diphtheria carries 10, whooping cough 7, hepatitis A 4,
  and influenza and H5N1 3 each — the full disease split held exactly from 08-31. azimuth records
  each notification in the disease category and alert band the reporting body assigned it
  ([[disease-outbreaks]]).
- **By country, the United States is the most-cited source of notifications at 38**, ahead of
  Bangladesh (11), Nigeria (9), Afghanistan (6), Brazil (5) and Sudan (4). A further **29
  notifications carry no country attribution** — azimuth reports this as unattributed, not as a
  country. The country split also held exactly from 08-31 ([[disease-outbreaks]]).

## Reading the week

- The 09-01 pull **held the 08-31 slate exactly**: **158 notifications, 119 watch / 39 alert**,
  with identical disease, country and case-count figures — a genuinely flat 24-hour cycle in the
  aggregate ([[disease-outbreaks]]).
- The one substantive change this cycle is on azimuth's side, not the feed's: the per-notification
  **case-count leaderboard is restored**, since the feed does carry case counts (the prior cycle
  had retired it on a mistaken read). The highest single entries are a **58,000-case Chicken Pox
  notification in Gaza City** (watch) and a **50,820-case Measles alert in the DR Congo**, ahead of
  Guatemala City measles (27,145 / 21,700, alert) and Bangladesh measles (18,726 / 17,800 / 16,408,
  alert) ([[disease-outbreaks]]).
- Measles stays the largest disease category (65 of 158), ahead of Unknown Disease (26) and polio
  (22); the United States is the most-cited country of notification at 38, with 29 notifications
  carrying no country attribution — reported separately, not counted as a country
  ([[disease-outbreaks]]).
- azimuth records the notifications as the reporting body published them — disease category,
  country of notification (where attributed), case count and alert level — and attaches no
  assessment of risk, spread or response. A measles-led slate of 158 notifications, held flat from
  08-31 with a Gaza City chicken-pox and a DR Congo measles entry topping the case counts, is what
  the WHO/CDC channel carried on the 2026-09-01 pull; nothing beyond the recorded counts is
  inferred ([[disease-outbreaks]]).

## Changelog

- 2026-09-02 — daily-ingest synthesis (2026-W36): absorbed the 2026-09-01 ingest — a materially flat 24-hour cycle: the slate held the 08-31 pull exactly (158 notifications, 119 watch / 39 alert; measles 65, Unknown Disease 26, polio 22; US 38 the most-cited country, 29 unattributed; identical per-notification case counts, 0 ids added/removed, total 343,952 cases). The substantive change is corrective: restored the per-notification case-count leaderboard the prior cycle wrongly retired (the feed does carry case counts) — highest single entries Gaza City Chicken Pox 58,000 (watch) and DR Congo Measles 50,820 (alert), ahead of Guatemala City measles 27,145 / 21,700 and Bangladesh measles 18,726 / 17,800 / 16,408. Reframed the intro, at-a-glance and reading sections around the held-flat aggregate + restored case leaders. Observed-only framing held; no country attributed to the unattributed bucket ([[disease-outbreaks]]).
- 2026-08-31 — daily-ingest synthesis (2026-W36): absorbed the 2026-08-21 through 2026-08-31 ingests after an 11-day curator gap; notifications rose 154 → 158 (119 watch / 39 alert, from 114 watch / 40 alert); measles stayed the largest category (63 → 65) and polio rose (17 → 22, the largest proportional move), while diphtheria (12→10) and hepatitis A (6→4) eased; United States remains the most-cited country at 38, Russia entered the top-country list at 4, and the unattributed-country bucket rose 27 → 29. Rewrote the at-a-glance and reading sections around this cycle's aggregate figures (notification counts, alert bands, disease and country breakdowns) — no case-count/city-level data was supplied this cycle, so the prior per-notification case-count leaderboard was retired rather than extended with unverified figures. Observed-only framing held; no country attributed to the unattributed bucket ([[disease-outbreaks]]).
- 2026-08-20 — daily-ingest synthesis (2026-W34): absorbed the 2026-08-18 through 08-20 pulls; the slate eased to 154 active signals (114 watch / 40 alert; no warning-level entry) from 156 on 08-17, a modest churn of 10 departures against 7 arrivals. Measles eased to 63 of 154 (from 68); diphtheria rose to 12 (from 9) on fresh Karachi and Minna (Nigeria) entries. The 58,000-case Gaza City Chicken Pox notification (watch) still tops the feed; a fresh Bangladesh measles 17,800 (alert) entered the case-count leaders (source summary: 2026 measles death toll passing 900), ahead of the carried Guatemala City 27,145/21,700 (alert) and Bangladesh 16,408 (alert). US measles national notifications led by 2,318 (watch, 2026 US total above all of 2025); the weekly-tally entry that read 2,465 on 08-17 now records 94 new infections (mostly Pennsylvania). Updated the at-a-glance and reading sections. Observed-only framing held ([[disease-outbreaks]]).
- 2026-08-17 — daily-ingest synthesis (2026-W34): the 08-17 pull matched 08-16 exactly — 156 active signals (115 watch / 41 alert; no warning-level entry), measles unchanged at 68 of 156, the 58,000-case Chicken Pox notification in Gaza City (watch) still the highest single entry, and US measles holding at 2,465 (watch). Zero additions, zero departures and zero case-count changes across all 156 matched entries — the first fully flat 24-hour cycle in the tracked series. Updated the at-a-glance and reading sections to record the hold. Observed-only framing held ([[disease-outbreaks]]).
- 2026-08-16 — daily-ingest synthesis (2026-W33): absorbed the 2026-08-07 through 2026-08-16 pulls after a curator gap. The 08-16 feed carries 156 active signals (115 watch / 41 alert; no warning-level entry), easing from 161 on 08-01; measles leads 68 of 156 (from 75). New top single-entry case count: a 58,000-case Chicken Pox notification in Gaza City (watch), now the feed's highest, above the carried Guatemala City measles 27,145 (alert) and 21,700 (alert); a fresh Bangladesh measles 16,408 (alert) also entered. Mongolia 15,475 (watch), Bangladesh 14,841 (watch) / 13,907 (alert), Mexico 11,771 (watch) / 11,748 (alert) and Dhaka 11,549 (watch) held; US measles rose to 2,465 (watch, source note: 2026 US total surpasses all of 2025). Updated the at-a-glance and reading sections; observed-only framing, no health advice ([[disease-outbreaks]]).
- 2026-08-01 — daily-ingest synthesis (2026-W31): absorbed the 2026-07-31 and 2026-08-01 pulls. The 08-01 feed carries 161 active signals (117 watch / 44 alert; no warning-level entry), easing from 165 on 07-30; measles leads 75 of 161 (from 78). The top case-count ranks all carried — Guatemala City measles 27,145 (alert) and 21,700 (alert), Mongolia 15,475 (watch), Bangladesh 14,841 (watch) and 13,907 (alert), Mexico 11,771 (watch) / 11,748 (alert), Dhaka 11,549 (watch) — as did the US measles 2,318 (watch, source note: 2026 US total surpasses all of 2025). Two-day churn minor and confined to small entries: five low-case notifications departed (measles Ghaziabad 129 / Uganda 12 / Colombia 6, Diphtheria Inchiri 19, a zero-case alert) against one zero-case arrival. Updated the at-a-glance and reading sections; observed-only framing, no health advice ([[disease-outbreaks]]).
- 2026-07-30 — daily-ingest synthesis (2026-W31): absorbed the 07-26 through 07-30 pulls after a 5-day curator gap. The 07-30 feed carries 165 active signals (120 watch / 45 alert; no warning-level entry), easing from the prior cycle; measles leads 78 of 165. Top case counts: Guatemala City measles 27,145 (alert) and 21,700 (alert), Mongolia 15,475 (watch), a new Bangladesh 14,841 (watch), Bangladesh 13,907 (alert), Mexico 11,771 (watch) / 11,748 (alert), Dhaka 11,549 (watch). Notable arrivals: US measles 2,318 (watch, source note: 2026 US total surpasses all of 2025), Whooping Cough Santander 3,171 (watch), Measles Punia 2,089 (watch), Measles Peru 1,233 (watch). Rewrote the at-a-glance and reading sections; observed-only framing, no health advice ([[disease-outbreaks]]).
- 2026-07-25 — daily-ingest synthesis (2026-W30): 07-25 pull carries 173 signals (down from 177 on 07-24; 127 watch / 46 alert); no warning-level entry. No id-matched field mutations. Eight entries departed: Measles Pakistan 4,541 (alert) and Measles Dhaka 4,460 (alert) were the largest departures; Polio Sudan 2 (watch) and five zero-case outbreak-news-today entries also left. Five new zero-case CDC entries entered: Unknown Disease US alert, two California Unknown Disease watch, Lassa watch, and E. coli alert (McDonald's Quarter Pounder cluster, Mountain West states). Top case-count ranking unchanged from 07-24; Guatemala City measles 27,145 (alert) remains highest single entry ([[disease-outbreaks]]).
- 2026-07-24 — daily-ingest synthesis (2026-W30): 07-24 pull carries 177 signals (up from 169 on 07-23; 127 watch / 50 alert); no warning-level entry. Bangladesh 120,000-case alert entry departed the feed; highest Bangladesh measles entry now 13,907 cases (alert). Guatemala City gains a new top-entry at 27,145 cases (alert) alongside the carried 21,700-case alert and a 6,209-case alert — three distinct Guatemala City alert entries on this pull. Mongolia 15,475 (watch) and Mexico three entries (11,771 watch / 11,748 alert / 11,111 alert) carried forward unchanged ([[disease-outbreaks]]).
- 2026-07-23 — daily-ingest synthesis (2026-W30): 07-23 pull carries 169 signals (down from 184 on 07-20); no warning-level entry. Bangladesh measles 120,000 cases (alert) unchanged; Guatemala 21,700 (alert) and Mongolia 15,475 (watch) carried forward; Mexico now shows three distinct entries: 11,771 (watch), 11,748 (alert), 11,111 (alert). Bangladesh also carries two additional watch entries (11,549; 10,949) ([[disease-outbreaks]]).
- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 pulls; the 07-20 feed carries 184 notifications (133 watch / 51 alert), down from 198 on 07-17, with no warning-level entry this pull (the Sudan El Taweisha measles warning dropped off). Measles leads 95 of 184; largest entry measles Bangladesh 120,000 cases; other majors Guatemala City ~21,700, Mongolia ~15,475, Mexico ~11,771 ([[disease-outbreaks]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): 07-16 and 07-17 pulls identical (198 entries, 144 watch / 53 alert / 1 warning); net change vs 07-15 baseline = -1 entry (Measles/Dhaka 3,065-case alert + Lassa/Iowa watch retired; Unknown Disease/HAI watch added). Warning level unchanged: measles El Taweisha, Sudan, 300 cases, 9 pediatric deaths. Largest alert entry: measles Bangladesh 120,000 cases ([[disease-outbreaks]]).
- 2026-07-15 — first Public Health Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the WHO/CDC channel is public-domain, surfaced, and carries 21 committed L1
  days). Wrote the at-a-glance and reading sections from the live 2026-07-15 pull: 199 active
  notifications (144 watch / 54 alert / 1 warning), measles leading at 105 incl. the Sudan
  warning-level outbreak (300 cases), alert-level entries clustering in the US (16) and
  Bangladesh (6). Observed-only framing, no health advice ([[disease-outbreaks]]).
