---
title: Editorial Line
type: L3-rule
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator)
---

# Editorial Line (L3)

**facts in, opinions out.** (Michael 2026-06-24.)

azimuth surfaces **any** channel that monitors **facts** — observed events,
measurements, positions, records — and is **free-to-use** (license-clean). It reports
what the open data **shows**, with provenance. It never advises, predicts harm, takes a
political or safety side, or editorialises. This is the line the `azimuth-curator` writes
inside, the `synthesis` lint enforces (`synthesis/lint.py` `check_editorial_denylist`),
and the source-guardrail enforces at the channel boundary (`guardrail/source_guardrail.py`).
A rule without a lint line is a TODO, not a rule — so each clause below names its enforcement.

## The line: facts allowed, propaganda denied

| | Allowed — an observed FACT (surface it) | Denied — an OPINION / POSITION (exclude it) |
|---|------------------------------------------|----------------------------------------------|
| **Markets** | "EU gas storage rose to 62% ([[natural-gas-storage-eu]])" | "buy/sell", "go long", "price target", "will rise to $N" |
| **Hazards** | "USGS logged a M5.8 event ([[earthquakes]])" | "imminent disaster", "the quake will strike", "you should evacuate" |
| **Conflict / unrest** | "A conflict event was recorded at <place> on <date> ([[conflict-events]])" | "the regime is to blame", "war crimes", "the aggressor must be stopped" |
| **Maritime / aviation** | "Vessel X reported position <lat,lon> ([[vessel-tracking]])" | "this proves an imminent blockade / strike is coming" |
| **News** | wire/agency **fact-reporting** of what happened, sourced | op-ed, editorial, advocacy, "in my view", "it is clear that" |

**Sensitivity is never a deny reason.** A factual record is allowed even on a sensitive
topic — a conflict EVENT, a ship POSITION, a flight TRACK, a power outage, a cyber
incident are observed facts (allowed). An OPINION about them is propaganda (denied).

**The gate is two ANDed conditions:** a channel is surfaced iff it is **factual** AND
**free-to-use** (public-domain / CC / API-ToS-permitted / non-commercial-with-attribution,
since azimuth is a non-commercial demonstrator carrying `CREDITS.md`). A restricted or
commercial-only feed stays out on **license** grounds — that is a separate bar from the
editorial line, and the source-guardrail tags the reason `license` vs `editorial`.

### News (allowed) — the per-source filter

NEWS is a factual channel: surface wire/agency **fact-reporting** (what happened, where,
when, sourced). The per-source filter keeps only fact-reporting outlets and **strips
op-ed / editorial / advocacy** sources. Report the event, never the outlet's opinion of it.

### Not surfaced as channels — forecast / assessment / scenario

Predictions, intelligence assessments, and hypothetical scenarios are **not** observed
facts, so they are **not** azimuth channels. azimuth instead uses them as **benchmark
foils**: it proves its USP by contrast — observed + sourced facts vs predicted / assessed
opinion (see work-item `azi-benchmark-vs-forecast-intelligence-W26`). prediction-MARKET
prices are the exception: the **quoted price is an observed fact**, so it stays allowed
(with a synthesis caution forbidding investment framing).

## Positive contract (L2 synthesis)

- Every claim paragraph or bullet carries **>=1 `[[wikilink]]`** to the L1 note it rests on
  (enforced: `check_claim_sourcing` + `check_l1_links_exist`).
- Describe the **signal and its source**, not what the reader should do, think, or feel.
- Quantify from the data; attribute uncertainty to the data, not to a forecast of ours.
- Report **observed**, never **predicted**. Assign no blame, take no political or safety side.
- When data conflicts, say so and link both L1 notes — do not resolve it with an opinion.

## Enforcement map

| Clause | Enforcement |
|--------|-------------|
| Channel is factual, not propaganda/opinion | `guardrail/source_guardrail.py` (`denied-content-class` / `denied-risk-flag`, category `editorial`) |
| Channel is free-to-use (license gate, separate bar) | `guardrail/source_guardrail.py` (`missing-license` / `unrecognised-license`, category `license`) |
| No investment / safety-position / propaganda / advocacy framing in L2 | `synthesis/lint.py` `check_editorial_denylist` |
| Every claim sourced | `check_claim_sourcing` |
| Links point at real L1 notes | `check_l1_links_exist` |
| Curator never edits L1 | `check_diff_guard` |
