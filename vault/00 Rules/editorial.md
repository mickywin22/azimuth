---
title: Editorial Line
type: L3-rule
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator)
resource: false
tags: [doctrine]
---

# Editorial Line (L3)

azimuth's L2 briefs report what open data **shows**. They never advise, predict harm,
or take a political side. This is the line the `azimuth-curator` writes inside and the
`synthesis` lint enforces (`synthesis/lint.py` `check_editorial_denylist`). A rule
without a lint line is a TODO, not a rule — so each clause below names its enforcement.

## What a brief MUST NOT say

| Class | Forbidden | Allowed (neutral reporting) |
|-------|-----------|------------------------------|
| **Investment advice** | "buy/sell", "go long", "price target", "guaranteed returns", "will rise to $N" | "EU gas storage rose to 62% ([[natural-gas-storage-eu]])" |
| **Safety prediction** | "imminent disaster", "the quake will strike", "will cause N deaths", "you should evacuate" | "USGS logged a M5.8 event ([[earthquakes]])" |
| **Political opinion** | "corrupt regime", "should be sanctioned", "is to blame for", "puppet state" | "Polymarket odds on the policy moved to 41% ([[prediction-markets]])" |

## Positive contract

- Every claim paragraph or bullet carries **>=1 `[[wikilink]]`** to the L1 note it rests on
  (enforced: `check_claim_sourcing` + `check_l1_links_exist`).
- Describe the **signal and its source**, not what the reader should do about it.
- Quantify from the data; attribute uncertainty to the data, not to a forecast of ours.
- When data conflicts, say so and link both L1 notes — do not resolve it with an opinion.

## Enforcement map

| Clause | Lint function (`synthesis/lint.py`) |
|--------|--------------------------------------|
| No investment / safety / political framing | `check_editorial_denylist` |
| Every claim sourced | `check_claim_sourcing` |
| Links point at real L1 notes | `check_l1_links_exist` |
| Curator never edits L1 | `check_diff_guard` |
