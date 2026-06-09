# azimuth — Implementation Plan v1

> **Status:** Ready (pending Michael sign-off on PRD + IQ #371 decisions)
> **Last updated:** 2026-06-09
> **Source spec:** `docs/spec.md` v2

## Phases

### Phase 0 — Decision lock (Michael, ~5 min)
**Target:** the 3 IQ #371 calls confirmed (v0 theme · cadence split · license split) via PRD sign-off.

- [x] Live API verification (5 endpoints, access model, rate limits) — done 2026-06-09
- [x] Spec v2 + this plan written — done 2026-06-09
- [ ] Michael confirms/overrides the 3 recommendations

**Gate:** decisions logged in `05 Projects/azimuth.md` + IQ #371 closed.

### Phase 1 — F1 L1 ingest (1–2 fleet slots, ~40k tok)
**Target:** vault self-populates daily with zero LLM involvement.

- [ ] Strip template: delete `src/backend/`, `src/frontend/`, coolify/multi-tenancy/openapi docs
- [ ] Scaffold `vault/` tree (00 Rules / 01 Sources / 02 Briefs) + L3 rule files
- [ ] `ingest/pull.py`: session-mint → endpoint set from `ingest/endpoints.json` → markdown transform → dated L1 notes (frontmatter: source, endpoint, retrieved, license)
- [ ] Smoke the 3 🔶 endpoints (nat-gas-storage, crude-inventories, fuel-prices); freeze v0 set
- [ ] Unit tests: transform fidelity, frontmatter schema, degraded-mode (API down → skip + log)
- [ ] `.github/workflows/ingest.yml`: daily cron + commit; `lint.yml`: L1 schema lint
- [ ] Error path: 3 consecutive failed pulls → GH issue auto-opened (visible even pre-Slack wiring)

**Gate:** 3 consecutive green scheduled (not manual) daily runs + lint CI green.

### Phase 2 — F2 L2 synthesis (2–3 fleet slots, ~50k tok)
**Target:** one lint-green "Energy Supply Weekly" brief produced autonomously.

- [ ] `synthesis/azimuth-curator.md` fleet role (HemySphere `00 Context/Fleet Roles/` contract format) + prompt: read week's L1 → evolve `02 Briefs/Energy Supply Weekly.md`
- [ ] Synthesis lint (CI, blocking): claim→L1-wikilink check · `01 Sources/` diff guard · editorial deny-list regex · frontmatter schema · evolve-not-duplicate check
- [ ] Scheduled-task framework entry: weekly slot on Michael's box → run curator → push
- [ ] Dry-run 1 brief on banked L1 data; Michael spot-review
- [ ] Iterate prompt until brief reads as analysis-with-sources, not data dump

**Gate:** 2 consecutive weekly briefs pass full lint; spot-review verdict ≥ "good".

### Phase 3 — F3 public flip (1 slot, ~15k tok; Michael ~5 min approve)
**Target:** repo public, promo loop live.

- [ ] gitleaks full-history scan → green
- [ ] `CREDITS.md` (Worldmonitor + EIA + GIE/AGSI + Polymarket + USGS-if-v1) · LICENSE (MIT code) + `vault/LICENSE` (CC BY 4.0 content)
- [ ] README: doctrine explainer, vault reading guide, link to HemySphere doctrine bundle
- [ ] Flip public (Michael approve) — immediately after first lint-green brief, not after site polish
- [ ] LinkedIn post #1 via linkedin-post skill (draft → Michael publishes)

**Gate:** repo public + credits/licenses complete + post live.

### Phase 4 — F4 site + hardening (2 slots, ~35k tok)
**Target:** readable public surface + proven autonomy.

- [ ] Quartz static site, candidate `azimuth.emi-factory.dev` (Cloudflare Pages)
- [ ] Stale-data guard: newest brief >10 days → Slack #important + site banner
- [ ] Weekly cycle → automatic Slack #daily one-liner (self-reporting doctrine)
- [ ] Run to the 4-consecutive-autonomous-cycles success metric

**Gate:** site live + 4-week streak + success-metrics check-in logged in vault note.

## Task estimates (totals)

| Phase | Fleet slots | Tokens | Michael time |
|-------|------------|--------|--------------|
| 0 | — | — | 5 min |
| 1 | 1–2 | ~40k | 0 |
| 2 | 2–3 | ~50k | 10 min (spot-reviews) |
| 3 | 1 | ~15k | 5 min (flip + publish) |
| 4 | 2 | ~35k | 0 |
| **Total** | **6–8** | **~140k** | **~20 min** |

## Dependencies

- IQ #371 decisions (Phase 0) gate Phase 1 start
- Phase 2 needs ≥1 week of banked L1 data from Phase 1 (natural sequencing, no idle wait — slots run in different weeks anyway)
- Phase 3 needs first green Phase-2 brief
- Build-week scheduling: F1–F3 sit in HemySphere Solo Queue, gated; Strategic Architect assigns the W-slot (W25+ candidate — W24 board is full with WC26 + Apex pin)

## Risks

| # | Risk | Impact | Mitigation |
|---|------|--------|------------|
| R1 | Worldmonitor keys/limits/kills the public API (no ToS = no guarantee; operator runs a commercial product) | F1 goes dark | Ingest abstraction is per-source; fallback adapters for the same data direct from upstream (EIA, GIE/AGSI, Polymarket — all public). Degraded-mode keeps vault alive on stale data with a banner |
| R2 | Session-mint flow changes (auth hardening upstream, e.g. Turnstile) | Daily cron fails | Pin contract to `koala73/worldmonitor` source; 3-fail GH-issue alarm; fix-forward — or trigger R1 fallback |
| R3 | Editorial breach in a public L2 brief (investment/political/safety wording) | Reputational — this repo carries Michael's name | Blocking deny-list lint + curator self-check + Michael spot-review first 4 cycles |
| R4 | L2 quality mediocre — data dump instead of synthesis | Demonstrator backfires ("the doctrine produces noise") | Phase-2 gate includes human spot-review; brief evolves one note (depth) instead of spawning many shallow notes |
| R5 | Secrets in repo history at public flip | Credential leak | gitleaks full-history scan is a blocking Phase-3 gate |
| R6 | Scope creep (more themes, more endpoints, custom site) | Side-project eats fleet budget | v0 = ONE theme, ONE brief; cost ceiling metric (≤1 slot/week); new subsets need per-source license review by L3 rule |
| R7 | Box-down ≥1 week pauses L2 (runtime-split trade-off) | Stale brief on a public site | Accepted for v0; stale-data guard makes it visible, GH Actions L1 keeps data flowing |
