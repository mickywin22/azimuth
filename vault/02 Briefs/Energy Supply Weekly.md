---
title: Energy Supply Weekly
type: L2-brief
theme: energy-supply
week: 2026-W28
updated: 2026-07-10T12:00:00Z
sources: [natural-gas-storage-eu, crude-oil-inventories, fuel-prices, energy-prices]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Energy Supply Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each week — it deepens this brief and appends
> a dated `## Changelog` line rather than forking a new file. Every claim links to the L1
> note it rests on. (This cycle reads the live `2026-07-10` daily ingest: gas storage and crude
> inventories each advanced two fresh reporting weeks, the spot benchmarks fell a third
> consecutive leg with Brent breaking below $70, and the road-fuel panel carried no fresh
> week-on-week deltas.)

## This week at a glance

- The oil picture kept easing on both sides at once: US crude inventories drew again to 730.8
  million barrels — the twelfth straight weekly draw, but at just −3.2 million barrels the
  smallest of the run — while WTI fell to $70.48/barrel (−4.2%) and Brent to $69.70 (−5.3%), a
  third consecutive leg down that took Brent below $70 for the first time since the brief began
  ([[crude-oil-inventories]], [[energy-prices]]).
- European gas supply kept refilling: storage advanced two reporting weeks to 2,983 Bcf as of the
  week ending 2026-07-03 (+61 Bcf, the twelfth straight build) — the build decelerating from the
  prior week's +87 Bcf ([[natural-gas-storage-eu]]).
- The pump held flat this pull: the road-fuel panel carried no fresh week-on-week deltas
  (the feed's `wowAvailable` flag is false), with German diesel unchanged at €1.763/L and E5
  petrol at €1.90/L on their standing 2026-06-29 observation ([[fuel-prices]]).

## Storage and inventories

- US commercial crude inventories fell to 730.8 million barrels for the week ending 2026-07-03,
  a draw of ~3.2 million barrels — the twelfth straight weekly draw, but by far the smallest of
  the run as the drawdown decelerated sharply (the prior three weeks ran −15.1, −9.3 and now
  −3.2 million); stocks are down from ~819 million in mid-May but the weekly pull is now close to
  flat ([[crude-oil-inventories]]).
- EU gas storage advanced two reporting weeks to 2,983 Bcf for the week ending 2026-07-03 —
  +61 Bcf on the prior week's 2,922 Bcf (itself +87 Bcf), the twelfth straight build and up from
  2,391 Bcf eight weeks earlier — with the weekly build decelerating from +87 to +61 as the
  refill matures ([[natural-gas-storage-eu]]).
- The two stockpiles still point in opposite directions, but both are decelerating toward
  balance: gas keeps building (though the weekly add is shrinking) while crude keeps drawing
  (though the weekly draw has nearly run out) — a comfortable gas balance alongside an oil
  drawdown that is petering out ([[natural-gas-storage-eu]], [[crude-oil-inventories]]).

## Prices

- Both crude benchmarks fell for a third consecutive cycle: the latest energy-prices feed reads
  WTI at $70.48/barrel (−4.2%) and Brent at $69.70/barrel (−5.3%), down roughly $3 each from the
  prior cycle's $73.59 / $73.63 and down ~$22–24 from the $92.16 / $93.76 of mid-June — a
  cumulative slide of about 23–26% in three reporting steps, with Brent now under $70 even as the
  inventory draw continued ([[energy-prices]], [[crude-oil-inventories]]).
- German road fuel held on its standing 2026-06-29 observation: diesel unchanged at €1.763/L and
  E5 petrol at €1.90/L — the feed reported no fresh week-on-week move in the pump panel this pull
  (`wowAvailable` false) ([[fuel-prices]]).
- Across the wider panel the feed's extremes held familiar shape — Malaysia the cheapest for both
  gasoline and diesel, Denmark the dearest gasoline and Finland the dearest diesel across the 32
  reporting countries (one source, New Zealand, failed to report this pull) — but with no
  week-on-week deltas available, azimuth records the levels and flags the missing move rather than
  inventing one ([[fuel-prices]]).

## Reading the week

- The divergence that ran for weeks is now resolving rather than widening: the crude draw shrank
  to −3.2 Mb (from a −17 Mb peak), so the "tight stocks" signal is fading toward the same soft
  reading the screen has shown — WTI and Brent fell a third leg to $70.48 / $69.70, with Brent
  breaking below $70, roughly 23–26% under mid-June. Stocks and screen are converging on soft.
  Gas supply stayed comfortable at 2,983 Bcf (twelfth straight build, decelerating to +61), and
  the pump held flat with no fresh week-on-week deltas in the panel this pull
  ([[natural-gas-storage-eu]], [[crude-oil-inventories]], [[energy-prices]], [[fuel-prices]]).

## Changelog

- 2026-06-15 — first synthesis cycle: storage/inventory/price sections written from the
  2026-06-15 L1 day (engine-landing seed).
- 2026-06-16 — first REAL ingest cycle: rewrote every section from the live 2026-06-16
  WorldMonitor day. Replaced the seed's placeholder figures (TTF/baseload values absent from
  the live feed) with the actual data — EU gas storage 2,686 Bcf (+108 Bcf w/w), US crude
  775.7 Mb (−15.2 Mb w/w, 8th straight draw), WTI $96.87 / Brent $98.95, German diesel
  €1.87/L. Added a "Reading the week" synthesis of the gas-vs-oil divergence.
- 2026-06-18 — multi-theme cycle: refreshed from the live 2026-06-18 ingest. Crude drew a
  ninth straight week to 758.5 Mb (−17.2 Mb w/w) but WTI/Brent fell ~5% to $92.16/$93.76 —
  reframed "Reading the week" around the stocks-tightening-yet-price-softening divergence
  (demand-side read). Part of the cycle that added the Geophysical brief alongside this one.
- 2026-06-20 — daily-ingest refresh: EU gas storage advanced one reporting week to 2,759 Bcf
  for the week ending 2026-06-12 (+73 Bcf w/w, ninth straight gain but the smallest build in
  four weeks, down from +108 Bcf). Crude inventories, WTI/Brent and pump prices were unchanged
  from the prior reporting week. Added the decelerating-refill read to the storage and
  reading-the-week sections.
- 2026-06-23 — daily-ingest flowback (2026-W26): the live 2026-06-23 WorldMonitor pull carried
  no new reporting week — gas storage (2,759 Bcf, week ending 2026-06-12), crude inventories
  (758.5 Mb), WTI/Brent ($92.16/$93.76) and the EU/German pump panel were byte-identical to the
  2026-06-20 ingest (only the retrieval timestamp moved). Honest flat-week cycle: figures held,
  no fabricated movement; the brief's `updated` was advanced so the freshness gate records that
  the latest L1 day was absorbed ([[natural-gas-storage-eu]], [[crude-oil-inventories]],
  [[energy-prices]], [[fuel-prices]]).
- 2026-06-25 — daily-ingest flowback (2026-W26): a movement cycle. The crude-inventory feed
  advanced a fresh reporting week — 743.3 Mb for the week ending 2026-06-19 (−15.1 Mb w/w, the
  tenth straight draw) — and the spot crude benchmarks dropped sharply to WTI $81.36 (−11.7%)
  and Brent $81.00 (−13.6%), down ~$11 each from the prior cycle. EU gas storage (2,759 Bcf)
  and the road-fuel panel carried no new reporting week and were held. Rewrote the at-a-glance,
  inventory, price and reading sections around the widening tight-stocks / falling-price
  divergence ([[crude-oil-inventories]], [[energy-prices]], [[natural-gas-storage-eu]],
  [[fuel-prices]]).
- 2026-06-26 — daily-ingest flowback (2026-W26): a gas-side movement cycle. EU gas storage
  advanced a fresh reporting week to 2,835 Bcf for the week ending 2026-06-19 (+76 Bcf w/w, the
  tenth straight build, a touch firmer than the prior +73 Bcf). The crude-inventory feed
  (743.3 Mb, week ending 2026-06-19), the spot crude benchmarks (WTI $81.36 / Brent $81.00) and
  the EU/German pump panel carried no new reporting week and were held. Updated the at-a-glance,
  storage and reading sections around the advancing gas refill; the tight-stocks / falling-price
  oil divergence held ([[natural-gas-storage-eu]], [[crude-oil-inventories]], [[energy-prices]],
  [[fuel-prices]]).
- 2026-06-30 — daily-ingest flowback (2026-W27): an honest flat cycle. The live 2026-06-30
  WorldMonitor pull carried no new reporting week in any of the four feeds — EU gas storage
  (2,835 Bcf, week ending 2026-06-19), crude inventories (743.3 Mb, week ending 2026-06-19), the
  spot crude benchmarks (WTI $81.36 / Brent $81.00) and the EU/German pump panel (German diesel
  €1.87, E5 €1.944) were byte-identical to the 2026-06-26 ingest, only the retrieval timestamp
  moved. Figures held with no fabricated movement; the brief's `week` and `updated` were advanced
  so the freshness gate records that the latest L1 day was absorbed ([[natural-gas-storage-eu]],
  [[crude-oil-inventories]], [[energy-prices]], [[fuel-prices]]).
- 2026-07-02 — weekly synthesis (2026-W27): absorbed the 2026-07-01 and 2026-07-02 ingest days —
  a three-feed movement cycle. The crude-inventory feed advanced a fresh reporting week to
  734.0 Mb for the week ending 2026-06-26 (−9.3 Mb w/w, the eleventh straight draw and the
  smallest of the run). The spot benchmarks fell a second consecutive leg to WTI $73.59 (−9.6%)
  and Brent $73.63 (−9.1%), roughly 20% below mid-June in two steps. The road-fuel panel turned
  broadly lower on its 2026-06-29/07-01 observations — German diesel €1.763 (−7.1%), E5 €1.90
  (−3.7%), US diesel −10.4% / gasoline −7.6%, with nearly every EU market down. EU gas storage
  carried no new reporting week and was held at 2,835 Bcf. Rewrote the at-a-glance, inventory,
  price and reading sections around the extending tight-stocks / falling-price divergence now
  reaching the pump ([[crude-oil-inventories]], [[energy-prices]], [[fuel-prices]],
  [[natural-gas-storage-eu]]).
- 2026-07-10 — weekly synthesis (2026-W28): absorbed the week's ingest to the live 2026-07-10
  day — a two-feed movement cycle. Crude inventories advanced two reporting weeks to 730.8 Mb for
  the week ending 2026-07-03 (−3.2 Mb w/w, the twelfth straight draw but by far the smallest of
  the run, the draw decelerating −15.1 → −9.3 → −3.2). The spot benchmarks fell a third
  consecutive leg to WTI $70.48 (−4.2%) and Brent $69.70 (−5.3%), Brent breaking below $70 and
  the two ~23–26% under mid-June. EU gas storage advanced two reporting weeks to 2,983 Bcf (week
  ending 2026-07-03, +61 Bcf, the twelfth straight build, decelerating from +87). The road-fuel
  panel carried no fresh week-on-week deltas (`wowAvailable` false); German diesel held at €1.763
  and E5 at €1.90 on the standing 2026-06-29 observation. Reframed "Reading the week" around the
  tight-stocks / soft-price divergence now *resolving* — the crude draw shrinking toward zero so
  stocks and screen converge on soft ([[crude-oil-inventories]], [[energy-prices]],
  [[natural-gas-storage-eu]], [[fuel-prices]]).
</content>
