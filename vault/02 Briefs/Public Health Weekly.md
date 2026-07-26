---
title: Public Health Weekly
type: L2-brief
theme: public-health
week: 2026-W30
updated: 2026-07-25T09:00:00Z
sources: [disease-outbreaks]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Public Health Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **recorded disease
> outbreak notifications** — the disease, the place, the case count and the alert level as the
> reporting body published them — never a health prediction, never advice. Every claim links
> to the L1 note it rests on. (Updated from the 2026-07-25 ingest.)

## This week at a glance

- The WHO / CDC outbreak channel carries **173 active outbreak signals** as of the
  2026-07-25 pull — down from 177 on 2026-07-24. No warning-level entry is carried on this
  pull; the feed's own alert bands classify entries as "alert" or "watch" only
  (127 watch / 46 alert) ([[disease-outbreaks]]).
- **Measles dominates the slate by entry count and case count** across the 2026-07-25 pull,
  accounting for 83 of 173 entries. The feed's alertLevelMethodologyVersion is v1; azimuth
  records each notification in the alert band the reporting body assigned it
  ([[disease-outbreaks]]).
- The top case-count ranking is unchanged from 07-24. **Guatemala City (GT) holds the highest
  single-entry case count** on the feed: an alert-level measles entry at **27,145 cases**
  alongside the 21,700-case alert entry and a third entry at 6,209 cases (alert). The
  Bangladesh top entry remains **13,907 cases (alert)**, with further Bangladesh entries at
  11,549 (watch) and 10,949 (watch). Mongolia measles at **15,475 (watch)** and Mexico's
  three entries — **11,771 (watch)**, **11,748 (alert)**, **11,111 (alert)** — are carried
  forward at the same figures ([[disease-outbreaks]]).
- Five entries entered the feed on the 07-25 pull, all with zero recorded cases: a CDC
  Unknown Disease alert for the United States, two CDC Unknown Disease watch entries for
  California, a CDC Lassa watch entry, and a CDC E. coli alert entry referencing the
  McDonald's Quarter Pounder linked cluster in Mountain West states ([[disease-outbreaks]]).

## Reading the week

- The slate contracted from 177 notifications on 07-24 to 173 signals on 07-25, a net
  reduction of 4 entries. No warning-level notification is present; the feed's highest band on
  the 07-25 pull remains "alert", now at 46 entries (down from 50 on 07-24)
  ([[disease-outbreaks]]).
- Eight entries departed the feed between 07-24 and 07-25. The two most case-rich departures
  were measles notifications with recorded cases: **Measles Pakistan (Lahore area) at 4,541
  cases (alert)** and **Measles Dhaka (Bangladesh) at 4,460 cases (alert)**. Also departed:
  a Polio Sudan watch entry (2 cases) and five zero-case entries from outbreak-news-today
  sources (including H5N1 Kozhikode, Meningitis GB, Unknown Disease Spain alert, and two
  Unknown Disease alerts without location). No entry that previously appeared changed its
  field values — zero id-matched mutations on this pull ([[disease-outbreaks]]).
- Five new entries arrived, all sourced from the CDC HAN and all carrying zero recorded
  cases at the time of the 07-25 pull. The E. coli entry references the McDonald's
  Quarter Pounder cluster in Mountain West states; the location cell carries the full
  situation descriptor as the CDC published it. azimuth records the notifications as the
  reporting bodies published them — disease, location, case count, alert level — and
  attaches no assessment of risk, spread or response ([[disease-outbreaks]]).

## Changelog

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
