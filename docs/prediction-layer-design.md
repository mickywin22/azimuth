# azimuth — Prediction Layer Design (the "Outlook" L2 layer)

> **Status:** Design-locked — decision-grade, ready to dispatch as a build sprint. No open scope questions block the build; one owner *identity* call (D1) is surfaced but the design holds under either answer.
> **Last updated:** 2026-07-21
> **Track:** Azimuth (HemySphere vault: `05 Projects/azimuth.md`) — W30 KR3
> **Scope of this doc:** *scope only* — this is the design; the build lands in a later sprint. It is written so that sprint needs **zero re-scoping**: the four decision axes the KR asks for (**data available → forecast target → method → success metric**) are each locked below with concrete, buildable answers, plus a phased build plan, the editorial reconciliation, and the file/CI surface the build will touch.

---

## 0. Why this needs a design, not just a build ticket

azimuth's whole identity is **"the better witness, not a crystal ball."** Nearly every L1 source carries a `report-observed-not-predicted` synthesis caution; the registry lists `forecast` as an explicit **benchmark *foil* class** — something azimuth deliberately does **not** surface, and instead *contrasts itself against* in [Benchmark.md](../vault/02%20Briefs/Benchmark.md). That brief's own scorecard scores azimuth **"Forward-looking coverage: No — azimuth is a rear/now view, not a crystal ball."**

So bolting on a "prediction layer" is not a neutral feature — done naively it **contradicts the product's stated identity** and hands a critic the obvious jab: *"you said you only report facts; now you're guessing like everyone else."* The single most important job of this design is to resolve that tension **before** any code is written. §1 does that. If it isn't resolved up front, the build sprint would ship something off-brand and get re-scoped — exactly the failure the KR's *"zero-rescoping"* clause guards against.

---

## 1. Editorial reconciliation — the glass-box forecast

**Decision: the prediction layer ships as a separate, explicitly-labelled `Outlook` L2 layer that is a *glass-box baseline forecast* — and it strengthens the identity rather than breaking it.** The reconciliation rests on five rules:

1. **Physical separation.** The Outlook layer is its **own** brief (`Outlook Weekly.md`) and never edits a word of the observed-fact briefs. Energy Supply Weekly, Climate Signals Weekly et al. stay 100% observed-fact, `report-observed-not-predicted`, untouched. A reader can consume azimuth without ever meeting a forecast.

2. **Glass-box, not black-box — that is the entire point.** The Benchmark brief already pits azimuth against a *black-box* WorldMonitor forecast ("a probability you cannot rebuild"). azimuth's own forecast is the **honest inverse**: open data (the same committed L1 notes), open method (a named, deterministic statistical model — no LLM, no hidden model), open uncertainty (a published prediction interval), and — the differentiator — **open score** (every past forecast is scored against what actually happened, and the running track record ships *with* the forecast). azimuth doesn't claim to out-predict anyone; it claims to be the *only* forecast you can fully audit and hold accountable.

3. **Narrow, defensible targets only.** Outlook forecasts **continuous measured physical/market series** where a transparent statistical baseline is genuinely defensible (a smooth CO₂ curve, a seasonal storage cycle). It forecasts **nothing** that would be reckless or off-brand: **no earthquakes / hazards** (the Benchmark brief already says, correctly, *"nobody credibly forecasts earthquakes"* — we honor that in code, see §4.4), no conflict/disease/sanctions/displacement (sensitive events), no re-forecasting of prediction-market odds (the odds are already a forecast; re-forecasting them = investment framing, which the L3 line forbids).

4. **L3 cautions carry over and one is added.** Every market series keeps `no-investment-framing`. A new caution — **`forecast-is-a-baseline-not-advice`** — is added to the L3 editorial vocabulary and asserted on the Outlook brief by the synthesis lint, so the layer cannot silently drift into advice.

5. **It upgrades the Benchmark, honestly.** Today the Benchmark scorecard concedes a blank in the "forward-looking" row. The Outlook layer lets azimuth add a **fourth column — "azimuth Outlook (glass-box forecast)"** — that scores *Yes* on sourced / reproducible / open-licensed / **scored-track-record**, and is candid that a dedicated proprietary model may still have wider predictive reach. The pitch becomes: *"here are the observed facts; here is a fully-auditable baseline forecast with its own report card; and here is the black-box forecast that can't show you either."*

> **Net:** the identity shifts from *"we never predict"* to *"when we predict, we do it in glass — open data, open method, open interval, open score — the one forecast you can actually check."* That is on-brand for a doctrine demonstrator, not against it.

---

## 2. Data available  ← *(KR axis 1 of 4)*

azimuth already collects, every day, more than enough numeric history to forecast a narrow set of series. There are **two tiers**, and v0 uses only Tier-A.

### 2.1 Tier-A — embedded upstream series (forecast-ready at build time)

Several L1 sources return **their own upstream history inside a single daily pull** — so a usable series exists *today*, without waiting for azimuth's own day-by-day accumulation. Verified against the live `2026-07-20` L1 bundle:

| Series | L1 source note | Field | History in one pull | Cadence | Character |
|--------|----------------|-------|---------------------|---------|-----------|
| Atmospheric CO₂ | `co2-monitoring` | `monitoring.trend12m[].ppm` (+ `annualGrowthRate`) | **12 monthly** points | monthly | smooth trend + mild seasonality — the "hello world" of forecastable series |
| Arctic sea-ice extent | `sea-ice-extent` | `data.iceTrend12m[].extentMkm2` | **12 monthly** points | monthly | strong annual seasonal cycle |
| EU gas storage | `natural-gas-storage-eu` | `weeks[].storBcf` | **8 weekly** points | weekly | seasonal inject/withdraw cycle |
| US crude inventories | `crude-oil-inventories` | `weeks[].stocksMb` | **8 weekly** points | weekly | strong recent trend |

Every one of these sits under a `US-Gov-public-domain` or `CC-BY-4.0` license already cleared by the source guardrail — **no new license review is needed** to forecast them.

### 2.2 Tier-B — azimuth's own accumulated daily snapshots (deferred)

azimuth has committed **32 daily L1 days** (2026-06-15 → 2026-07-20; daily since 2026-06-24). Stacking one field across those days yields azimuth-*unique* daily series — e.g. daily fuel/energy price tape, daily peak fire-radiative-power, daily M4.5+ **count**. These are the more novel targets, but at ~32 irregular points (early gaps) they are too thin for a defensible daily forecast today. **Tier-B is explicitly deferred** until ≥90 clean daily observations bank (~2026-09, by which point the daily cron will have closed the early gaps). v0 ships Tier-A; Tier-B is a follow-on cadence with no design change (same extractor/forecaster/scorer, longer series).

### 2.3 Honest data constraints (these drive the method in §4)

- **Short history.** 8–12 points per Tier-A series. This *rules out* deep/ML models and *mandates* few-parameter, robust classical baselines with honest intervals. Stated here so the build sprint never reaches for an LSTM.
- **Revisions.** EIA/GIE weekly figures can revise; the extractor keys on `period`/`month` and takes the **latest** value for a period (upsert), matching how the fact briefs already treat these feeds.
- **Ragged cadence.** Monthly vs weekly series are forecast on their own clock; no resampling across cadences.

---

## 3. Forecast target  ← *(KR axis 2 of 4)*

**v0 forecasts exactly the four Tier-A series, each as a short-horizon point forecast plus an 80% prediction interval.** Concrete and frozen:

| # | Target series | Unit | Primary horizon | Secondary horizon | Seasonality to model |
|---|---------------|------|-----------------|-------------------|----------------------|
| T1 | CO₂ monthly mean | ppm | next 1 month | next 3 months | mild annual |
| T2 | Arctic sea-ice extent | Mkm² | next 1 month | — | strong annual |
| T3 | EU gas storage | Bcf | next 1 week | next 4 weeks | annual inject/withdraw |
| T4 | US crude inventories | Mb | next 1 week | — | weak; trend-dominated |

**Framing rule (applies to every target):** each forecast is published as *"model X projects `<value> ± <interval>` for `<period>`, baseline-only, not advice"* with the model named inline and a link back to the L1 series it was fit on. **The primary output is the point + interval; the secondary output is the running accuracy score** (§5) — the two together *are* the product.

**Explicitly out of scope for v0** (each with the reason, so the build sprint doesn't re-open them):

- ❌ **Earthquakes / natural hazards** — not predictable; forecasting them would torch credibility (honored in code, §4.4).
- ❌ **Conflict / disease / sanctions / displacement** — sensitive event streams; azimuth reports these as facts, never predicts them.
- ❌ **Prediction-market odds** — already a forecast; re-forecasting = investment framing (L3-forbidden).
- ❌ **Fuel/energy *prices* (Tier-B daily)** — near-random-walk on ~32 noisy points; deferred until history deepens (a naive baseline would be the honest answer anyway).

---

## 4. Method  ← *(KR axis 3 of 4)*

**Decision: a deterministic, no-LLM ensemble of transparent classical baselines, with honest prediction intervals — reproducibility is the moat, so the method must be as auditable as the data.** This mirrors azimuth's existing engine (every generator — `benchmark.py`, `build_graph.py` — is pure deterministic Python; the forecast path must be too, or it can't claim the "regenerable, same result" virtue that beats the black-box foil).

### 4.1 The baseline ensemble (per series, per horizon)

Fit these few-parameter models, all robust on 8–12 points:

1. **Seasonal-naive** — last value from one full cycle ago (the reference model MASE is scaled against; §5).
2. **Drift / robust linear trend** — Theil–Sen slope through the series (median-of-slopes, outlier-robust) extrapolated forward.
3. **Simple exponential smoothing (SES)** — level-only, for near-flat series.
4. **Holt (double ES)** — level + trend, for the trended series (T4 crude, CO₂ trend component).
5. **Holt–Winters (triple ES)** — level + trend + seasonal, **only where ≥1 full seasonal cycle is observed** (T2 sea-ice, T1 CO₂ once ≥12 monthly points; guarded — falls back to Holt if a full cycle isn't present).

### 4.2 Combination

Point forecast = **median of the eligible ensemble members** (robust to any single model misfiring) *unless* the backtester (§5) shows one model is decisively best for that series, in which case Outlook uses **pick-best-by-backtest** and names it. Either way the chosen model is **named in the brief** — no hidden blending.

### 4.3 Prediction intervals (the honesty layer)

80% PI via **residual bootstrap** on the rolling-origin backtest residuals (seeded, so deterministic), or a model-native interval where the model provides one. The interval is mandatory — a point forecast without a published interval is not shippable (it would be a false-precision claim, the exact thing azimuth criticizes in the foil).

### 4.4 Determinism & guardrails (build-time invariants)

- **No LLM anywhere in the forecast path.** Classical stats only. Same committed L1 → byte-identical forecast (the CI `--check` pattern the rest of the repo already uses).
- **Dependency stance:** **stdlib + NumPy only for v0** (Theil–Sen, ES, and a bootstrap are ~150 lines of NumPy; keeps the CI install light and the method fully readable). `statsmodels` ETS is a *fallback* only if a series demonstrably needs it — decision deferred to the build, not required.
- **Hazard interlock:** a hard-coded **allow-list of forecastable series keys** (the four T1–T4). Any series carrying `report-observed-not-predicted` for a *hazard* class (earthquakes, wildfire, natural-events, radiation) is **rejected by the forecaster with an assertion**, and a unit test pins that earthquakes can never enter the Outlook path. The "we don't forecast quakes" promise is enforced in code, not just prose.

---

## 5. Success metric  ← *(KR axis 4 of 4)*

**Three metrics, one ship-bar. The track record is a public artifact, not an internal check.**

| Metric | Definition | Target |
|--------|------------|--------|
| **Point accuracy** | **MASE** — mean absolute scaled error vs the seasonal-naive baseline (scale-free, the standard forecast metric). Reported alongside **sMAPE** for human readability. | **MASE < 1.0** (beats naive) on the primary horizon |
| **Calibration** | Empirical coverage of the 80% prediction interval on the rolling-origin backtest | coverage in **[70%, 90%]** |
| **Track record (operational)** | Every *published* forecast is auto-scored when its actual value later lands; a rolling **forecast scorecard** (per-series MASE + coverage over the trailing N forecasts) renders in the Outlook brief | scorecard present + auto-updating every cycle |

**v0 ship / no-go bar for the build sprint** (this is what "the build is done" means):

> The Outlook ensemble beats seasonal-naive (**MASE < 1**) on **≥3 of the 4** targets **and** holds 80% PI coverage in [70%, 90%] on **≥3 of 4**, measured by a rolling-origin backtest over the available history.

**Honesty fallback (also a rule, not a hope):** if a series *cannot* beat naive, Outlook **publishes the seasonal-naive baseline itself, labelled as such** ("no model beat the naive baseline this cycle; showing naive"). That is still a glass-box forecast and still scored — azimuth never ships a model that's worse than naive just to look sophisticated, and it *says so on the page*. This turns a modeling limitation into a credibility feature.

---

## 6. Build plan (the later sprint — dispatch-sized, so this doc is zero-rescoping)

Five logical units, each independently committable and gated. New code lives under a new top-level `outlook/` package (peer of `ingest/`, `synthesis/`, `guardrail/`), so `[tool.setuptools.packages.find]` in `pyproject.toml` gains `outlook*` (mirrors the flat-layout fix already in the repo).

| P | Unit | Deliverable | Acceptance gate |
|---|------|-------------|-----------------|
| P1 | **Series extractor** | `outlook/series.py` — parse the embedded Tier-A series out of the L1 notes into a clean per-series `(period, value)` history table; upsert-by-period; fail-soft on a missing field | unit tests on the 4 series from committed L1 days; deterministic |
| P2 | **Forecaster** | `outlook/forecast.py` — the §4 baseline ensemble + median/pick-best combo + bootstrap PI; the hazard allow-list interlock | unit tests incl. the earthquake-rejection assertion; same input → same output |
| P3 | **Backtester + scorer** | `outlook/backtest.py` — rolling-origin eval → MASE, sMAPE, PI-coverage per series; emits the scorecard data | reproduces a hand-checked MASE on a fixture series; the §5 ship-bar computed |
| P4 | **Outlook L2 brief** | `vault/02 Briefs/Outlook Weekly.md` renderer + wire into `synthesis/lint.py` (assert the new `forecast-is-a-baseline-not-advice` caution + every forecast links its L1 series) + `docs/` + brief-index + a site page + nav entry | synthesis-lint green on the Outlook brief; brief-index `--check` in sync; doc-links + doc-orphans green |
| P5 | **Proof + Benchmark upgrade** | `scripts/smoke_outlook.py` (deterministic smoke over committed L1) + a banked screenshot; add the 4th **"azimuth Outlook (glass-box forecast)"** column to `Benchmark.md` | smoke exit 0; screenshot in `docs/proof/`; benchmark renders the 4th column |

**Cadence & integration:** Outlook regenerates on the **weekly** curator cadence (same clock as the other briefs) — the `azimuth-curator` role gains an Outlook step, and `check_synthesis_freshness.py` covers it like any other clean brief. No new scheduled task on Michael's box.

**Rough envelope:** ~4–6 fleet slots, ~120–160k tokens, **0 Michael-hours to build** (the only Michael input is the identity call D1 below, which can be answered async and does not block P1–P3). Matches the "build a later sprint" framing.

---

## 7. Risks & open decisions

**One owner-*identity* decision is surfaced (D1). It does not block the build** — P1–P3 (extract, forecast, score) are pure infrastructure that are correct under either answer; only the *publishing* framing in P4/P5 flexes. Everything else is a fleet-autonomous call, recommended inline.

| # | Decision / risk | Recommendation | Owner |
|---|-----------------|----------------|-------|
| **D1** | **Does azimuth publish a forecast layer at all, given the "witness not crystal ball" identity?** | **Ship it as the glass-box Outlook (§1).** It's on-brand for a doctrine demonstrator and upgrades the Benchmark. If Michael prefers to stay pure-observed, the fallback is **"backtest-only, internal"**: build P1–P3 + the scorecard, but *don't* publish the Outlook brief — azimuth then gains a private forecast-accuracy report without a public forward claim. Either way P1–P3 are identical. | **[Michael]** (identity call; async, non-blocking) |
| D2 | Include the Tier-B daily M4.5+ **count-rate** (a seismicity *statistic*, arguably fair) once history deepens? | **Exclude from v0.** Even a count-rate reads as "predicting earthquakes" to a lay visitor and dents the clean "we don't forecast quakes" line. Revisit only with an explicit editorial note. | [fleet] default; [Michael] to override |
| D3 | Dependency: stdlib+NumPy vs `statsmodels`. | **stdlib + NumPy for v0** (§4.4); add statsmodels only if a series proves it needs ETS. | [fleet] |
| R1 | Short history → overfit / unstable fits. | Few-parameter robust models + mandatory PI + the naive-fallback rule (§5); MASE bar is *relative* to naive so a weak series just shows naive, honestly. | mitigated in design |
| R2 | A forecast is badly wrong on the public site. | The published **track record** owns this: a wrong forecast lowers the visible score — that's the honesty feature, not a bug. PI makes the uncertainty explicit up front. | mitigated in design |
| R3 | Upstream series revises after a forecast is scored. | Score against the **first-published** actual for the period (frozen at scoring time); note revisions separately. | build-time rule (P3) |

---

## 8. Definition of done (this KR)

- ✅ A decision-grade design doc exists (this file) covering **data available (§2) → forecast target (§3) → method (§4) → success metric (§5)**, each locked with concrete buildable answers.
- ✅ The editorial identity tension is **resolved before build** (§1), so the later sprint ships on-brand.
- ✅ A dispatch-sized, gated **build plan** (§6) + surfaced risks/decisions (§7) mean the build sprint starts with **zero re-scoping** — the one open item (D1) is an async identity preference that leaves the infrastructure unchanged.

## 9. Linked

- [spec.md](spec.md) — the demonstrator spec this layer extends
- [plan.md](plan.md) — the original phased build plan (Phases 1–4; Outlook is the Phase-5 shape)
- [synthesis.md](synthesis.md) — the L2 synthesis engine the Outlook brief plugs into
- [Benchmark.md](../vault/02%20Briefs/Benchmark.md) — the facts-vs-forecast-vs-intelligence brief the Outlook layer adds a 4th column to
- [source-guardrail.md](source-guardrail.md) — the L3 license gate (all four Tier-A series already pass)
- `05 Projects/azimuth.md` (HemySphere vault) — the Azimuth project note / update log
