# azimuth — Specification

> **Status:** Research (2026-W24)
> **Last updated:** 2026-06-09
> **Track:** Coding-Factory KR2 (HemySphere vault: `05 Projects/azimuth.md`)

## Demonstrator concept (one paragraph)

azimuth is a **public, read-only knowledge vault that runs the HemySphere L1→L2→L3 wiki doctrine on open global-intelligence data**. It pulls structured briefs from the Worldmonitor public API (`api.worldmonitor.app`) as **L1 source notes** (raw, untouched), runs the existing fleet synthesis pattern to produce **L2 wiki notes** (weekly meta-briefs, cross-linked, the human-readable synthesis), all governed by a small **L3 rule set** (editorial line, attribution, no investment/safety advice). The whole vault is published as a public GitHub repo + static site, so anyone evaluating the HemySphere/Emi doctrine bundle can see a *live working second brain* on a neutral domain — proving the architecture without ever exposing Michael's private Emi vault content or USP. Each weekly synthesis cycle doubles as shareable build-in-public / LinkedIn content.

## Vision

Give the HemySphere doctrine a public proof point: a self-updating open-intelligence vault that demonstrates "Michael dumps, Claude organises" applied to world events instead of a personal life — readable by researchers, journalists, OSINT-curious developers, and anyone assessing the doctrine for their own domain.

## Users

| Persona | Description | Key Need |
|---------|-------------|----------|
| Doctrine evaluator | Dev/founder weighing the HemySphere L1/L2/L3 pattern for their own vault | See a real, non-toy public vault, not just a README |
| Generalist analyst | Researcher / journalist / OSINT hobbyist | Weekly synthesised "global pulse" meta-briefs with sourced links |
| Michael (promo) | Build-in-public content engine | Each L2 synthesis cycle = a tweetable / LinkedIn-able artifact |

## Architecture decision (locked in research)

**Path A — API consumer** (Michael 2026-05-12). Hit the public `api.worldmonitor.app` endpoints, transform JSON/CSV briefs into HemySphere-format markdown, publish the derived vault under our own license. **No source fork** → AGPL-3.0 of `koala73/worldmonitor` is not triggered (pure API-consumer use). Attribution via `CREDITS.md`. Paths B (fork+self-host, AGPL applies) and C (commercial license) rejected/deferred. Full legal + data-license analysis: `07 Resources/AI Agents & Agentic Systems/Worldmonitor App – Research.md` § azimuth Feasibility.

## Core Features (MVP — v0, deferred to build week)

### F1 — L1 ingest pipeline
- **What:** Scheduled pull of a *lower-friction* Worldmonitor subset → raw markdown L1 source notes.
- **Why:** L1 = untouched sources; the doctrine forbids editing raw at synthesis time.
- **Subset (v0, license-clean):** stock data · earthquake alerts (USGS public domain) · oil prices · prediction markets · power outages. Higher-friction (ACLED/UCDP conflict, AIS ship tracking, ADS-B military flights) deferred to v1 after per-source license review.
- **Acceptance criteria:**
  - [ ] Cron (GitHub Actions or fleet agent) pulls subset and commits L1 notes daily
  - [ ] Each L1 note carries source + retrieval-timestamp frontmatter; no synthesis in L1

### F2 — L2 synthesis (weekly meta-brief)
- **What:** A `azimuth-curator` synthesis pass turns the week's L1 notes into 1–2 cross-linked L2 meta-briefs (e.g. "Energy supply meta-brief" combining oil + power-outage + prediction-market signals).
- **Why:** L2 is where AI synthesis adds value beyond the Worldmonitor dashboard itself.
- **Acceptance criteria:**
  - [ ] Weekly cadence (lower cost, promo-friendly) produces wikilinked L2 notes
  - [ ] L2 never destructively overwrites — it evolves prior synthesis

### F3 — Public publish surface
- **What:** Publish the vault as a public read-only GitHub repo + static site (Quartz / Obsidian Publish candidate).
- **Acceptance criteria:**
  - [ ] Repo public, `CREDITS.md` crediting Worldmonitor + each surfaced source
  - [ ] Vault license chosen (MIT or CC-BY-SA) before first publish

## L3 rule set (editorial guardrails)

- No individual-country political opinions, no investment advice, no security/safety predictions that could harm readers.
- Attribution mandatory; per-source license check before any new subset is surfaced.

## Open Questions (carried from `05 Projects/azimuth.md`)

- [ ] Final subset for v0 (which 1–2 themes best demonstrate the doctrine?)
- [ ] Synthesis cadence: daily vs weekly vs on-demand (research lean: **weekly**)
- [ ] Storage/publish surface: flat repo vs Quartz static site vs live web app
- [ ] Sync mechanism: GitHub Actions cron vs local fleet agent
- [ ] Synthesis engine: dedicated `azimuth-curator` prompt vs extend an existing fleet role
- [ ] Vault license: MIT vs CC-BY-NC-SA

## Out of scope this week (W24)

W24 KR2 = `idea→research` + `project-init` scaffold only. No data pipeline, no synthesis engine, no deploy. This spec captures the locked research so the build week can start from a decided concept.
