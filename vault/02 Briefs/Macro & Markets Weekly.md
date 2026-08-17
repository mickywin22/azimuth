---
title: Macro & Markets Weekly
type: L2-brief
theme: macro-markets
week: 2026-W34
updated: 2026-08-17T09:00:00Z
sources: [crypto-quotes, world-bank-gdp, world-bank-cpi, world-bank-unemployment, world-bank-indicators]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources
---

# Macro & Markets Weekly

> Synthesised from the week's L1 source notes under `../01 Sources/`. The `azimuth-curator`
> fleet role evolves this single note in place each cycle. azimuth reports **venue-quoted
> market prices as observed facts** — a quote is what a market printed, recorded with its
> change and its source — under the `no-investment-framing` caution: nothing here is advice,
> a target, or a forecast. Every claim links to the L1 note it rests on.
> Last updated from the 2026-08-17 pull.

## This week at a glance

- The CoinGecko-fed crypto channel quotes **10 major assets** on the 2026-08-17 pull. The panel
  **turned fully green — all 10 assets up on the day**, reversing the 08-16 fully-red print.
  **Bitcoin rose to $63,540 (+0.9% on the day)** and **Ethereum to $1,903.83 (+1.4%)**. Ethereum
  was the largest gainer at **+1.4%**; BNB and Cardano were the smallest movers at **+0.1%** each
  ([[crypto-quotes]]).
- Across the 2026-08-07 → 2026-08-17 window the panel recovered off the 08-01 lows to an **08-10
  high (BTC $65,166, +0.8%; ETH $1,923.59)**, then rolled back over — a fully-red 08-14 (BTC
  $62,950), a one-day steadying on 08-15 (BTC $63,030, 3 of 10 up), and a fully-red 08-16 (BTC
  $63,026) — before **rebounding fully green on 08-17 (BTC $63,540, +0.9%, all ten up)**. Bitcoin
  is now **+$514 (+0.8%) week-on-week versus the 08-16 close** and net roughly flat to slightly up
  over the whole window (~$63,043 on 08-01 → $63,540 on 08-17) after round-tripping through the
  mid-week high and the 08-16 low ([[crypto-quotes]]).
- The full quoted panel as of the 2026-08-17 pull: BTC $63,540 (+0.9%) · ETH $1,903.83
  (+1.4%) · BNB $605.60 (+0.1%) · SOL $75.79 (+0.6%) · XRP $1.005 (+0.5%) · ADA
  $0.1767 (+0.1%) · DOGE $0.0703 (+1.1%) · TRX $0.3324 (+0.5%) · AVAX $6.37
  (+0.7%) · LINK $9.48 (+0.9%) — venue-quoted prices and day-changes as published, with
  intraday sparkline series carried in the L1 note ([[crypto-quotes]]).
- **The World Bank Open Data direct channel** carries 2025 reference-year macro indicators for
  seven major economies — **annual data, unchanged since the 2026-08-16 pull** (no fresh World
  Bank note was ingested on 2026-08-17). **GDP (current US$, 2025):** United States **$30.77T**,
  China **$19.50T**, Germany **$5.05T**, Japan **$4.44T**, United Kingdom **$4.00T**, India
  **$3.96T**, France **$3.37T** ([[world-bank-gdp]]). **CPI inflation (annual %, 2025):** United
  Kingdom **3.88%**, Japan **3.17%**, India **2.40%**, Germany **2.17%**, France **0.94%**, China
  **0.06%** — with the United States carried at its **2024** print of **2.95%** (no 2025 US
  figure published yet) ([[world-bank-cpi]]). **Unemployment (%, 2025):** France **7.54%**,
  United Kingdom **4.75%**, China **4.62%**, India **4.22%**, United States **4.20%**, Germany
  **3.71%**, Japan **2.45%** ([[world-bank-unemployment]]).

## Honest scope — two live channels now

- The macro-markets theme registers several channels; **the crypto-quotes channel and the World
  Bank Open Data direct channel (GDP / CPI / unemployment) now both carry data.** The older
  `world-bank-indicators` endpoint went parameter-gated and returns no payload — the direct World
  Bank Open Data pulls (`world-bank-gdp`, `world-bank-cpi`, `world-bank-unemployment`) replace it
  as the live macro-indicator source. The tariff and consumer-price channels are not yet surfaced
  upstream. This brief scopes to the live channels and widens as the others land
  ([[crypto-quotes]], [[world-bank-gdp]]).

## Reading the week

- The 08-07 → 08-17 pulls trace a recover-then-roll-back-then-rebound arc off the 08-01 lows.
  Bitcoin climbed from its 08-01 $63,043 print to an 08-10 high of $65,166 (+0.8% that day) as the
  panel turned broadly green (nine of ten up on 08-08); it then gave the gain back — a fully-red
  08-14 ($62,950), a one-day steadying on 08-15 ($63,030, three of ten up), and a fully-red 08-16
  ($63,026, −0.1%, all ten down, Avalanche the largest faller at −5.7%) — before turning fully
  green again on 08-17 ($63,540, +0.9%, all ten up, Ethereum the largest gainer at +1.4%). Over
  the whole window Bitcoin now sits modestly above where it began, having round-tripped through
  both the mid-week high and the 08-16 low. These are the venue's numbers, not azimuth's view: no
  target, no direction call, no investment framing — the caution is the contract, not a disclaimer
  ([[crypto-quotes]]).
- The World Bank Open Data direct channel, surfaced this cycle, prints its 2025 reference-year
  figures stable across its first three ingest days observed (08-14 → 08-16); no fresh World Bank
  note landed on 08-17, so the read carries forward unchanged. Read as recorded national accounts,
  not a forecast: the United States carries the largest 2025 output at $30.77T (China second at
  $19.50T), the United Kingdom the highest 2025 consumer-price inflation of the seven at 3.88%
  (China the lowest at 0.06%), and France the highest 2025 unemployment at 7.54% (Japan the lowest
  at 2.45%). azimuth reports the World Bank's published values and attaches no projection
  ([[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).

## Changelog

- 2026-08-17 — daily-ingest synthesis (2026-W34): crypto-quotes rebounded to a fully green panel (10 of 10 up) after the 08-16 fully-red print — BTC $63,540 (+0.9% on the day; +$514 / +0.8% week-on-week vs the 08-16 close of $63,026), ETH $1,903.83 (+1.4%), Ethereum the largest gainer, BNB and Cardano the smallest movers (+0.1% each); World Bank indicators held at their last-known 2025 annual values, no fresh 08-17 World Bank note ([[crypto-quotes]]).
- 2026-08-16 — daily-ingest synthesis (2026-W33): absorbed the 2026-08-14 through 2026-08-16 pulls. crypto-quotes rolled back over after the mid-window recovery — a fully-red 08-14 (BTC $62,950), a one-day steadying on 08-15 (BTC $63,030, 3 of 10 up), then a fully-red 08-16: BTC $63,026 (−0.1%), ETH $1,879.17 (−0.2%), Avalanche the largest faller (−5.7%), no gainer; over the window Bitcoin ends roughly flat (~$63,043 on 08-01 → $63,026 on 08-16). NEW: the World Bank Open Data direct channel landed (first L1 2026-08-14) and is briefed for the first time — 2025 reference-year GDP (US $30.77T / China $19.50T lead), CPI inflation (UK 3.88% high, China 0.06% low; US carried at its 2024 2.95% print) and unemployment (France 7.54% high, Japan 2.45% low) for seven major economies, held flat 08-14→08-16; it replaces the parameter-gated world-bank-indicators endpoint as the live macro-indicator source. Updated frontmatter sources, at-a-glance, honest-scope and reading sections ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-07-15 — first Macro & Markets Weekly cycle (2026-W29): theme un-held (the hold was
  ingest-pending; the crypto-quotes channel is API-ToS-cleared, surfaced, and carries 21
  committed L1 days; World Bank / tariff / consumer-price channels documented as empty or
  not-yet-surfaced in the honest-scope note). Wrote the at-a-glance, honest-scope and
  reading sections from the live 2026-07-15 pull: 10 quoted assets, all green, BTC $64,590
  (+3.2%), ETH $1,873 (+5.0%), LINK the largest mover (+5.6%). Venue-quoted facts under the
  no-investment-framing caution ([[crypto-quotes]]).
- 2026-07-18 — daily-ingest synthesis (2026-W29): crypto-quotes moved (07-17 pull): all 10 assets down, BTC $62,740 (−1.96%), ETH $1,823.90 (−3.05%), LINK $8.16 (−3.00%), TRX smallest faller (−0.35%); world-bank-indicators held (empty payload, no new reporting) ([[crypto-quotes]], [[world-bank-indicators]]).
- 2026-07-21 — daily-ingest synthesis (2026-W30): absorbed the 07-18 through 07-20 pulls. crypto-quotes moved: the 07-20 panel is mixed and near-flat with Bitcoin recovering to $64,130 (−0.62%) from the 07-17 $62,740 low, ETH $1,861.78 (−0.30%), SOL/AVAX/LINK marginally green, Cardano the largest faller (−1.37%). world-bank-indicators held (empty payload, no new reporting). Updated the at-a-glance and reading sections ([[crypto-quotes]], [[world-bank-indicators]]).
- 2026-07-23 — daily-ingest synthesis (2026-W30): broad shallow pullback after the 07-21 rally (BTC $66,237 +3.67%, ETH $1,939.59 +4.54%); 07-23 panel: BTC $65,585 (−0.8%), ETH $1,922.61 (−0.1%), LINK the largest faller (−0.9%), ADA the largest gainer (+1.4%); world-bank-indicators held (empty payload, no new reporting) ([[crypto-quotes]]).
- 2026-07-24 — daily-ingest synthesis (2026-W30): pullback broadened — nine of ten assets down on the day; BTC $65,361 (−0.4%, down $224 from 07-23), ETH $1,889.61 (−1.5%, down $33), AVAX the largest faller (−4.6%), DOGE −3.6%, ADA −3.5%; sole gainer TRX +0.7%; world-bank-indicators held (empty payload, no new reporting) ([[crypto-quotes]], [[world-bank-indicators]]).
- 2026-07-25 — daily-ingest synthesis (2026-W30): the pullback went fully red — all ten assets down on the day (from nine of ten on 07-24), the first clean down-sweep since the 07-21 rally; BTC $63,929 (−2.3%, down $1,432 from 07-24 and its first sub-$64,000 print of the pullback), ETH $1,854.00 (−1.9%), ADA the largest faller (−3.5%), SOL −2.8%, XRP −2.5%, LINK −2.2%; no gainer; world-bank-indicators held (empty payload, no new reporting) ([[crypto-quotes]], [[world-bank-indicators]]).
- 2026-07-30 — daily-ingest synthesis (2026-W31): absorbed the 2026-07-26 through 2026-07-30 pulls after a five-day gap behind the live L1. crypto-quotes steadied after the 07-25 fully-red sweep — 8 of 10 assets down on the day but two green; levels recovered modestly from the 07-25 lows: BTC $64,174 (−0.7%, ~$245 above the 07-25 print), ETH $1,911.08 (−0.9%), LINK the largest faller (−1.6%), BNB (+0.6%) and TRX (+0.5%) the only gainers. world-bank-indicators held (empty payload, no new reporting). Updated the at-a-glance and reading sections ([[crypto-quotes]], [[world-bank-indicators]]).
- 2026-08-01 — daily-ingest synthesis (2026-W31): absorbed the 2026-07-31 and 2026-08-01 pulls. crypto-quotes turned broadly lower again after the 07-30 steadying — 9 of 10 assets down on the day, only Cardano green (+1.6%); BTC $63,043 (−1.8%, ~$1,131 below the 07-30 print and back under $64,000), ETH $1,867.81 (−1.7%), LINK the largest faller (−2.4%), the remaining seven down 0.2–1.6%. world-bank-indicators held (empty payload, no new reporting). Updated the at-a-glance and reading sections ([[crypto-quotes]], [[world-bank-indicators]]).
- 2026-08-13 — daily-ingest synthesis (2026-W33): absorbed the 2026-08-07 through 2026-08-13 pulls (no macro-markets L1 was committed 08-02→08-06). crypto-quotes recovered off the 08-01 lows — the panel turned broadly green (nine of ten up on 08-08) and Bitcoin reached an 08-10 high of $65,166 (+0.8%, ETH $1,923.59) — then gave it back on 08-11 (BTC $63,902 −1.9%, ETH $1,871.16 −2.6%, Cardano the largest faller at −4.6%) before steadying. The 08-13 pull is mixed with 6 of 10 up: BTC $63,819 (+0.1%), ETH $1,895.43 (+0.3%), AVAX the largest gainer (+3.8%), DOGE the largest faller (−2.0%); over the window Bitcoin ends roughly flat after peaking mid-week. world-bank-indicators held (no L1 note written after 08-01; endpoint now parameter-gated). Updated the at-a-glance and reading sections ([[crypto-quotes]], [[world-bank-indicators]]).
