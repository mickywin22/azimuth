# azimuth — Specification v2

> **Status:** Spec-locked (pending Michael sign-off on 3 decisions, IQ #371)
> **Last updated:** 2026-06-09
> **Track:** Coding-Factory (HemySphere vault: `05 Projects/azimuth.md`)
> **Supersedes:** spec v1 (2026-06-09 research scaffold). v2 = audit findings resolved + live API verification.

## Demonstrator concept (one paragraph)

azimuth is a **public, read-only knowledge vault that runs the HemySphere L1→L2→L3 wiki doctrine on open global-intelligence data**. It pulls structured data from the Worldmonitor public API (`api.worldmonitor.app`) as **L1 source notes** (raw, untouched), runs a fleet synthesis pass to produce **L2 wiki notes** (weekly cross-linked meta-briefs), all governed by a small **L3 rule set** (editorial line, attribution, enforcement lint). Published as a public GitHub repo + static site, it proves the HemySphere/Emi doctrine bundle on a live, neutral domain — showing the architecture without exposing Michael's private Emi vault content or USP. Each weekly synthesis cycle doubles as build-in-public / LinkedIn content.

## Vision

Give the HemySphere doctrine a public proof point: a self-updating open-intelligence vault that demonstrates "Michael dumps, Claude organises" applied to world events instead of a personal life — readable by researchers, journalists, OSINT-curious developers, and anyone assessing the doctrine for their own domain.

## Users

| Persona | Description | Key Need |
|---------|-------------|----------|
| Doctrine evaluator | Dev/founder weighing the HemySphere L1/L2/L3 pattern for their own vault | See a real, non-toy public vault, not just a README |
| Generalist analyst | Researcher / journalist / OSINT hobbyist | Weekly synthesised "Energy Supply" meta-briefs with sourced links |
| Michael (promo) | Build-in-public content engine | Each L2 synthesis cycle = a LinkedIn-able artifact |

## Data layer — VERIFIED 2026-06-09

### Access model (corrected from v1)

v1 claimed "no API key, no fees". Live verification corrected this:

| Fact | Verified detail |
|------|-----------------|
| Gate | `POST https://api.worldmonitor.app/api/wm-session` mints an **anonymous HMAC session token** (free, no account) → HttpOnly cookie `wm-session` (`wms_` prefix), **12 h expiry** |
| RPC shape | `GET /api/<domain>/v1/<rpc-kebab>` with the session cookie. sebuf HTTP-RPC over proto definitions |
| Rate limit | 600 req / 60 s sliding window per IP (Upstash). azimuth daily pull ≈ 10 req/day → no risk |
| Paid tiers | Only 4 stock-analysis RPCs are Pro-gated (`ENDPOINT_ENTITLEMENTS`); **all azimuth v0 endpoints are unrestricted** |
| Upstream license | `koala73/worldmonitor` = AGPL-3.0 + commercial dual. Pure API-consumer use does **not** trigger AGPL (no fork, no modified service). Path A holds |
| API ToS | None published. Operator (Elie Habib) can key/limit the API at any time → Risk R1 in `plan.md` |

### v0 endpoint inventory (theme: Energy Supply)

| Endpoint | Status | Sample (2026-06-09) |
|----------|--------|---------------------|
| `/api/economic/v1/get-energy-prices` | ✅ live-verified | WTI $93.45/bbl, Brent, change % |
| `/api/economic/v1/get-eu-gas-storage` | ✅ live-verified | fill 42.48 %, trend "injecting", daily history |
| `/api/economic/v1/get-oil-inventories` | ✅ live-verified | EIA weekly crude stocks + weekly change |
| `/api/prediction/v1/list-prediction-markets` | ✅ live-verified | Polymarket markets, yes-price + volume + URL |
| `/api/seismology/v1/list-earthquakes` | ✅ live-verified (v1 candidate, not v0) | USGS quakes, magnitude/depth/location |
| `/api/economic/v1/get-nat-gas-storage` | 🔶 source-confirmed, smoke at build | proto exists |
| `/api/economic/v1/get-crude-inventories` | 🔶 source-confirmed, smoke at build | proto exists |
| `/api/economic/v1/list-fuel-prices` | 🔶 source-confirmed, smoke at build | proto exists |

**Corrections vs v1:** "power outage monitoring" does not exist as a Worldmonitor subset — the `infrastructure` domain covers *internet* outages/cables/DDoS. The v0 theme drops it and gains gas storage + oil inventories (stronger supply signal anyway). The repo exposes **35 proto domains** (v1 research note said "22 services" — stale).

## Architecture (final)

### Path A — API consumer (locked 2026-05-12, re-confirmed against live LICENSE)

Transform API JSON into HemySphere-format markdown. Publish the derived vault under our own license. No source fork → AGPL untriggered. Attribution via `CREDITS.md`.

### Stack decision (NEW in v2 — resolves audit finding 6)

azimuth is a **flat markdown vault repo**, not a web app:

```
azimuth/
├── vault/
│   ├── 00 Rules/          # L3 — editorial line, attribution policy, synthesis contract
│   ├── 01 Sources/        # L1 — raw API pulls as dated markdown notes (never edited)
│   │   └── YYYY-MM-DD/    #      one folder per pull day
│   └── 02 Briefs/         # L2 — weekly meta-briefs, wikilinked, evolving
├── ingest/                # Python ingest scripts (stdlib + requests only)
├── synthesis/             # azimuth-curator prompt + lint rules
├── .github/workflows/     # daily L1 cron + lint CI
├── CREDITS.md             # Worldmonitor + per-source attribution
└── README.md              # doctrine explainer + how to read the vault
```

**Template strip:** the `project-template` FastAPI backend (`src/backend/`), Next.js frontend (`src/frontend/`), and `docs/coolify-deploy.md` / `docs/multi-tenancy.md` / `docs/openapi-pattern.md` are deleted in Phase 1. No server runtime exists in this product.

### Runtime split (resolves audit finding 8)

| Layer | Runtime | Why |
|-------|---------|-----|
| L1 ingest (daily) | **GitHub Actions cron** — no LLM, pure fetch+transform+commit | Vault self-updates even when Michael's box is off; public-repo-native; strongest demonstrator story |
| L2 synthesis (weekly) | **Fleet role `azimuth-curator`** on Michael's box (scheduled-task framework) → commit + push | Runs on the Max subscription = zero marginal cost; reuses the proven fleet Worker pattern; no API key in Actions |
| Publish | Static — GitHub public repo first, Quartz site in Phase 4 | No backend to operate |

Trade-off accepted: L2 pauses if the box is down ≥1 week. Stale-data guard (Phase 4) posts a Slack alert and stamps the site banner if the newest brief is >10 days old.

## Core Features

### F1 — L1 ingest pipeline (Phase 1)
- **What:** GitHub Actions cron pulls the v0 endpoint set daily → raw markdown L1 notes under `vault/01 Sources/YYYY-MM-DD/`.
- **Acceptance criteria:**
  - [ ] Endpoint smoke for all 🔶 endpoints; final v0 set frozen in `ingest/endpoints.json`
  - [ ] Daily cron green; each L1 note carries `source`, `endpoint`, `retrieved`, `license` frontmatter
  - [ ] L1 notes are verbatim-faithful transforms (JSON → tables/values); **zero synthesis in L1**
  - [ ] Session-mint + retry + degraded-mode handling (skip day, log, no crash)
  - [ ] Gate: 3 consecutive green daily runs + L1 schema lint green in CI

### F2 — L2 synthesis, weekly meta-brief (Phase 2)
- **What:** `azimuth-curator` (fleet role) reads the week's L1 notes → writes/evolves 1 cross-linked **Energy Supply Weekly** brief in `vault/02 Briefs/`.
- **Quality gate (NEW in v2 — resolves audit finding 5).** CI synthesis lint, all blocking:
  - every L2 claim paragraph carries ≥1 wikilink to an existing L1 note
  - git diff guard: synthesis commit touches `vault/02 Briefs/` only — any `01 Sources/` mutation fails the run
  - editorial deny-list regex (investment-advice, safety-prediction, political-opinion phrasings) + curator self-check against `vault/00 Rules/editorial.md`
  - frontmatter schema valid; brief **evolves** the prior week's note (edit-in-place + changelog line), never duplicates
- **Acceptance criteria:**
  - [ ] 2 consecutive weekly briefs pass the full lint
  - [ ] Brief reads as analysis-with-sources, not data dump (Michael spot-review, first 4 cycles)

### F3 — Public publish (Phase 3)
- **What:** Repo flips public immediately after the **first** lint-green L2 brief (resolves audit finding 9 — promo loop starts at first brief, not after site polish).
- **Acceptance criteria:**
  - [ ] gitleaks scan green before flip (no secrets in history)
  - [ ] `CREDITS.md` lists Worldmonitor (primary aggregator) + every surfaced upstream source (EIA, GIE/AGSI, Polymarket, …)
  - [ ] License files in place per the split decision (below)
  - [ ] README explains the L1/L2/L3 doctrine + links HemySphere doctrine bundle
  - [ ] First LinkedIn post published (linkedin-post skill draft, Michael publishes)

### F4 — Static site + hardening (Phase 4)
- **What:** Quartz static site (candidate host: Cloudflare Pages, `azimuth.emi-factory.dev`), stale-data guard, 4-week autonomy streak.
- **Acceptance criteria:**
  - [ ] Site renders vault with working wikilinks + graph view
  - [ ] Stale-data guard: Slack alert + site banner if newest brief >10 days
  - [ ] 4 consecutive fully-autonomous weekly cycles (no manual fix)

## L3 rule set (editorial guardrails — enforced, not aspirational)

`vault/00 Rules/` ships as content (part of the demonstrator — evaluators see the L3 layer):
- `editorial.md` — no individual-country political opinions; no investment advice; no security/safety predictions that could harm readers; uncertainty stated, never dramatised.
- `attribution.md` — per-source license check **before** any new subset is surfaced; CREDITS.md update in the same PR.
- `synthesis-contract.md` — L1 never edited after creation; L2 evolves, never overwrites; every claim sourced.

Enforcement = the F2 CI lint (deny-list + diff guard + link check). A rule without a lint line is a TODO, not a rule.

## License (resolves audit finding 3 — pending Michael, IQ #371)

The v1 drift (CC-BY vs CC-BY-SA vs CC-BY-NC-SA across three docs) is resolved by **splitting code from content** — they are different artifacts:

| Artifact | Recommended license | Rationale |
|----------|--------------------|-----------|
| Code (`ingest/`, `synthesis/`, workflows) | **MIT** | Max reuse of the *pattern* — that is the point of a demonstrator |
| Vault content (`vault/` L1+L2+L3 notes) | **CC BY 4.0** | Attribution preserved, max shareability/credibility. NC variant rejected: azimuth content has no commercial moat to protect — the founding-company option value lives in the private Emi pattern, not here |

## Success metrics (NEW in v2 — resolves audit finding 7)

| Metric | Target | Measures |
|--------|--------|----------|
| Autonomy streak | 4 consecutive weekly cycles, zero manual fixes | The doctrine actually self-runs |
| Publish cadence | ≥1 LinkedIn post per L2 cycle from F3 on | Promo loop real |
| External signal | ≥25 GitHub stars OR ≥1 unsolicited doctrine adoption/mention within 8 weeks of public flip | Demonstrator persuades |
| Cost ceiling | L2 synthesis ≤1 fleet slot/week; $0 API spend | Stays a side-demonstrator, not a product tax |

## Out of scope (v0)

- Higher-friction Worldmonitor subsets (ACLED/UCDP conflict, AIS, ADS-B) — v1+, per-source license review first
- Seismology stream — v1 candidate (endpoint already verified)
- Any web app / backend / search / API of our own
- Monetization (Path C) — post-validation only

## Open decisions (Michael — IQ #371, presented in the PRD)

1. **v0 theme = Energy Supply** (5–8 verified endpoints above) — recommended. Alt: different theme.
2. **Cadence split: L1 daily (Actions) + L2 weekly (fleet)** — recommended. Alt: all-weekly.
3. **License split: code MIT + content CC BY 4.0** — recommended. Alt: CC BY-NC-SA content.
