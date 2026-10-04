---
title: Macro & Markets Weekly
type: L2-brief
theme: macro-markets
week: 2026-W40
updated: 2026-10-03T00:00:00Z
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
> Last updated from the 2026-10-03 pull, a print against the 2026-10-01 baseline: the crypto channel
> **turned mixed — five of ten tracked assets up week-on-week**, the large caps firming (Bitcoin +1.14%
> to $84,626, Solana +1.71% to $119.26, TRON +1.27%) and reversing the prior cycle's broad nine-of-ten
> decline, while Chainlink (-2.93%) stayed the panel's laggard; the feed's own 24-hour change is still
> broadly negative (the daily prints red even as the two-day w/w turned up for the majors). The World
> Bank Open Data channel (GDP/CPI/unemployment, seven reporting economies) **held byte-identical** to
> 10-01, as expected for annual reference-year data that does not move week to week.

## This week at a glance

- The CoinGecko-fed crypto channel's **2026-10-03 pull** printed **mixed — 5 of 10 tracked
  assets up week-on-week** against the 10-01 baseline: **Bitcoin $84,626** (+1.14%, from $83,670),
  **Ethereum $2,682.24** (-0.34%, from $2,691.27), **BNB $768.99** (+0.17%, from $767.72),
  **Solana $119.26** (+1.71%, from $117.26, the panel's firmest major) and **XRP $1.48** (-0.67%,
  from $1.49) ([[crypto-quotes]]).
- Across the wider ten-asset panel the move splits: **ADA $0.245145** (-0.80%), **DOGE
  $0.092701** (-1.78%), **TRX $0.337109** (+1.27%), **AVAX $11.03** (+0.64%) and **LINK $13.92**
  (-2.93%, the panel's steepest faller) — five of the ten closed 10-03 above their 10-01 baseline
  (BTC, BNB, SOL, TRX, AVAX), reversing the prior cycle's nine-of-ten decline; the move measured
  against the prior brief's printed levels, while the feed's own 24-hour `change` field stays broadly
  negative (the daily prints still red) ([[crypto-quotes]]).
- **The World Bank Open Data direct channel held byte-identical to 10-01** across all seven
  reporting economies — only the `retrieved` timestamp advanced. **GDP (current US$, 2025):**
  United States **$30.77T**, China **$19.50T**, Germany **$5.05T**, Japan **$4.44T**, United
  Kingdom **$4.00T**, India **$3.96T**, France **$3.37T** ([[world-bank-gdp]]). **CPI inflation
  (annual %, 2025):** UK **3.88%**, Japan **3.17%**, US **2.95%** (2024), India **2.40%**, Germany
  **2.17%**, France **0.94%**, China **0.06%** ([[world-bank-cpi]]). **Unemployment (%, 2025):**
  France **7.54%**, UK **4.75%**, China **4.62%**, India **4.22%**, US **4.20%**, Germany
  **3.71%**, Japan **2.45%** ([[world-bank-unemployment]]).

## Honest scope — two live channels now

- The macro-markets theme registers several channels; **the crypto-quotes channel and the World
  Bank Open Data direct channel (GDP / CPI / unemployment) now both carry data**, the latter widened
  from five to seven reporting economies this cycle. The older `world-bank-indicators` endpoint went
  parameter-gated and returns no payload — the direct World Bank Open Data pulls (`world-bank-gdp`,
  `world-bank-cpi`, `world-bank-unemployment`) replace it as the live macro-indicator source. The
  tariff and consumer-price channels are not yet surfaced upstream. This brief scopes to the live
  channels and widens as the others land ([[crypto-quotes]], [[world-bank-gdp]]).

## Reading the week

- The 2026-10-03 pull reads a **mixed week-on-week print** against the 10-01 baseline: Bitcoin firmed
  to $84,626 (+1.14%, from $83,670), Solana to $119.26 (+1.71%, from $117.26) and TRON to $0.337109
  (+1.27%), with BNB ($768.99, +0.17%) and Avalanche ($11.03, +0.64%) also higher, while Ethereum eased
  to $2,682.24 (-0.34%), XRP to $1.48 (-0.67%), ADA (-0.80%), DOGE (-1.78%) and Chainlink to $13.92
  (-2.93%, the steepest faller) — five of ten up on the week, reversing the prior cycle's nine-of-ten
  decline, the large caps leading the recovery. The feed's own 24-hour change stays broadly negative,
  so the two-day w/w turned up for the majors even as the daily prints read red. These are the venue's
  numbers, not azimuth's view: no target, no direction call, no investment framing — the caution is the
  contract, not a disclaimer ([[crypto-quotes]]).
- The World Bank Open Data direct channel **held byte-identical to 10-01** across all seven
  reporting economies — the annual reference-year figures do not move week to week, so a stable read
  is expected and this cycle delivered one. Read as recorded national accounts, not a forecast: the
  United States carries the largest 2025 output at $30.77T (France the smallest of the seven at
  $3.37T), the UK the highest 2025 consumer-price inflation at 3.88% (China the lowest at 0.06%),
  and France the highest 2025 unemployment at 7.54% (Japan the lowest at 2.45%). azimuth reports the
  World Bank's published values and attaches no projection
  ([[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).

## Changelog

- 2026-10-03 — daily-ingest synthesis (2026-W40): absorbed the 2026-10-02 and 2026-10-03 pulls; print vs the 2026-10-01 baseline. The crypto panel turned mixed — 5 of 10 tracked assets up on the week: Bitcoin $84,626 (+1.14%, from $83,670), Ethereum $2,682.24 (-0.34%, from $2,691.27), BNB $768.99 (+0.17%, from $767.72), Solana $119.26 (+1.71%, from $117.26), XRP $1.48 (-0.67%, from $1.49), ADA $0.245145 (-0.80%), DOGE $0.092701 (-1.78%), TRX $0.337109 (+1.27%), Avalanche $11.03 (+0.64%), Chainlink $13.92 (-2.93%, the steepest faller) — BTC, BNB, SOL, TRX and AVAX higher, reversing the prior cycle's nine-of-ten decline; the feed's own 24-hour change stays broadly negative (daily prints red even as the two-day w/w turned up for the majors). The World Bank Open Data direct channel (GDP/CPI/unemployment, seven reporting economies) held byte-identical to 10-01 — only the `retrieved` timestamp advanced, as expected for annual reference-year data. Rewrote the intro, at-a-glance and reading sections. no-investment-framing caution held ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-10-01 — daily-ingest synthesis (2026-W40): print vs 2026-09-29. The crypto panel turned broadly lower — 9 of 10 tracked assets down on the week: Bitcoin $83,670 (-0.86%, from $84,399), Ethereum $2,691.27 (-1.87%, from $2,742.48), BNB $767.72 (+0.18%, from $766.34, the only riser), Solana $117.26 (-2.87%, from $120.72), XRP $1.49 (-3.81%, from $1.549), ADA $0.247119 (-2.47%), DOGE $0.094378 (-1.72%), TRX $0.332875 (-0.77%), Avalanche $10.96 (-6.80%), Chainlink $14.34 (-6.88%, the steepest faller) — Chainlink and Avalanche reversing the prior cycle's +7.82% / +7.16% gains almost exactly; the feed's own 24-hour change was negative across all ten. The World Bank Open Data direct channel (GDP/CPI/unemployment, seven reporting economies) held byte-identical to 09-29 — only the `retrieved` timestamp advanced, as expected for annual reference-year data. Rewrote the intro, at-a-glance and reading sections. no-investment-framing caution held ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-09-30 — daily-ingest synthesis (2026-W40): week-on-week print vs 2026-09-27. The crypto panel turned mixed — 5 of 10 tracked assets up on the week: Bitcoin $84,399 (-0.52%, from $84,844), Ethereum $2,742.48 (+1.29%, from $2,707.53), BNB $766.34 (-1.71%, from $779.69), Solana $120.72 (-2.49%, from $123.80, the steepest faller), XRP $1.549 (+0.59%, from $1.54), ADA $0.253372 (-1.21%), DOGE $0.096027 (-1.86%), TRX $0.335463 (+0.39%), Avalanche $11.76 (+7.16%), Chainlink $15.40 (+7.82%, the steepest gainer). The World Bank Open Data direct channel (GDP/CPI/unemployment, seven reporting economies) held byte-identical to 09-27 — only the `retrieved` timestamp advanced, as expected for annual reference-year data. Rewrote the intro, at-a-glance and reading sections. no-investment-framing caution held ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-09-28 — daily-ingest synthesis (2026-W39): week-on-week print vs 2026-09-24. The crypto panel swung back broadly green — 9 of 10 tracked assets up on the week: Bitcoin $84,844 (+1.61%, from $83,502), Ethereum $2,707.53 (+2.24%, from $2,648.15), BNB $779.69 (+1.36%, from $769.20), Solana $123.80 (+9.28%, from $113.29), XRP $1.54 (+4.76%, from $1.47), ADA $0.256469 (+8.62%), DOGE $0.09785 (+5.53%), TRX $0.334166 (-1.47%, the panel's lone faller), Avalanche $10.97 (+7.87%), Chainlink $14.28 (+16.86%, the panel's steepest gainer). The World Bank Open Data direct channel (GDP/CPI/unemployment, seven reporting economies) held byte-identical to 09-24 — only the `retrieved` timestamp advanced, as expected for annual reference-year data. Rewrote the intro, at-a-glance and reading sections. no-investment-framing caution held ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-09-24 — daily-ingest synthesis (2026-W39): day-over-day print vs 2026-09-23. The crypto panel swept fully red — 10 of 10 tracked assets down on the day: Bitcoin $83,502 (-2.36%, from $85,587), Ethereum $2,648.15 (-2.70%, from $2,724.52), BNB $769.20 (-1.59%, from $781.86), Solana $113.29 (-2.90%, from $116.79), XRP $1.47 (-6.75%, from $1.58), ADA $0.236121 (-5.72%), DOGE $0.092726 (-6.50%), TRX $0.339154 (-1.08%, the panel's mildest faller), Avalanche $10.17 (-8.06%, the panel's steepest faller), Chainlink $12.22 (-3.95%). The World Bank Open Data direct channel (GDP/CPI/unemployment, seven reporting economies) held byte-identical to 09-23 — only the `retrieved` timestamp advanced, as expected for annual reference-year data. Rewrote the intro, at-a-glance and reading sections. no-investment-framing caution held ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-09-23 — daily-ingest synthesis (2026-W39): absorbed the 2026-09-22 ingest after a 20-day curator gap. The crypto panel rallied broadly across the gap — Bitcoin $86,029 (from $77,971), Ethereum $2,743.97 (from $2,455), BNB $786.66, Solana $117.14, XRP $1.53, all five majors up ~10-15%, the smaller majors (ADA, DOGE, TRX, AVAX, LINK) higher too; this pull carries no 24h change field, so the move is read as a gap level change, not day-over-day. The World Bank Open Data direct channel widened from five to seven reporting economies (US and UK now published): GDP 2025 US $30.77T > China $19.50T > Germany $5.05T > Japan $4.44T > UK $4.00T > India $3.96T > France $3.37T; CPI 2025 UK 3.88% highest, China 0.06% lowest; unemployment 2025 France 7.54% highest, Japan 2.45% lowest. Rewrote the intro, at-a-glance, honest-scope and reading sections. no-investment-framing caution held ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).

- 2026-09-02 — daily-ingest synthesis (2026-W36): absorbed the 2026-09-01 ingest, an adjacent-day advance on 08-31. After the gap rally cooled into month-end, the crypto panel printed near-flat and mixed: BTC $77,971 (−0.60%, from $77,999), ETH $2,455 (+0.18%, from $2,449), BNB $686 (−0.17%), SOL $102.18 (−1.61%, from $102.71), XRP $1.38 (+0.20%); across the ten-asset panel LINK strongest +1.31%, TRX softest −1.70%, none beyond ~1.7% either way — a sideways low-volatility session, not a fresh leg or reversal. World Bank 2025 annual figures (GDP/CPI/unemployment) held byte-identical to 08-31 for the five reporting economies (China, Germany, Japan, India, France). Reframed the intro, at-a-glance and reading sections around the quiet adjacent-day print. Observed-only framing held — prices and indicators reported as printed, no buy/sell/target language. ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
- 2026-08-31 — daily-ingest synthesis (2026-W36): absorbed the 2026-08-21 through 2026-08-31 ingests after an 11-day curator gap; crypto-quotes rallied hard across the gap then cooled into month-end — BTC $69,807 (08-20, +7.9%) to $77,999 (08-31, −0.9% on the day, net +~11.7% over the window), ETH $2,261 to $2,449 (−0.67%, net +~8.3%), BNB $629 to $686 (−1.55%, net +~9.1%), SOL $85.82 to $102.71 (−3.44%, net +~19.7%, steepest net mover), XRP $1.11 to $1.37 (−2.38%, net +~23.4%, largest net mover) — every one of the five closed 08-31 lower on the day even as all five sit well above their 08-20 print; World Bank 2025 annual figures (GDP/CPI/unemployment) held flat across the gap for the five reporting economies this cycle's pull carries (China, Germany, Japan, India, France). Observed-only framing held throughout — prices and indicators reported as printed, no buy/sell/target language, no direction call. ([[crypto-quotes]], [[world-bank-gdp]], [[world-bank-cpi]], [[world-bank-unemployment]]).
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
