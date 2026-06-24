# Source Guardrail — per-source license + content check

> **Standing L3 rule.** Before any new WorldMonitor-derived subset is surfaced as azimuth
> L1 source data, it must pass this guardrail. This is the *lint line* behind the
> `spec.md` L3 rule set — "a rule without a lint line is a TODO, not a rule".

## What it enforces

Every entry in [`sources/registry.json`](../sources/registry.json) marked `surfaced: true`
must satisfy **all** of:

The guardrail enforces the **fact-vs-propaganda line** (Michael 2026-06-24): a channel is
surfaceable iff it is **factual** AND **free-to-use** (license-clean). Every breach is
tagged with a `category` so a held channel's reason is machine-readable — the two headline
categories are **`license`** vs **`editorial`**.

| Check | Rule id | Category | Why |
|-------|---------|----------|-----|
| License recorded and in the free-to-use allowlist | `missing-license` / `unrecognised-license` | `license` | Path A is API-consumer; each upstream source needs a known, compatible license before redistribution |
| Attribution string present | `missing-attribution` | `attribution` | CC-BY / ToS attribution obligation |
| Credited in `CREDITS.md` (by registry `key`) | `missing-credit` | `credit` | the credit ↔ registry join must be machine-checkable, not fuzzy |
| Content class is an allowed observed-fact class | `unlisted-content-class` | `policy` | forecast / assessment / scenario are benchmark foils, not channels |
| Content class is not a non-factual class | `denied-content-class` | `editorial` | no propaganda / opinion / position-taking content |
| No risk flag is a non-factual class | `denied-risk-flag` | `editorial` | a subset tagged with a non-factual class may not be surfaced |

**Editorial exclusions** (hard deny, `editorial` category): `political-propaganda`,
`opinion-advocacy`, `editorial-communication`, `political-position`, `safety-position`,
`investment-advice`. These mirror `vault/00 Rules/editorial.md` (spec L3).

**Sensitivity is never a deny reason.** A factual record on a sensitive topic (a conflict
EVENT — `conflict-event-record`, a vessel POSITION — `vessel-position`, a flight TRACK —
`flight-track`, a cyber incident, a news fact-report) is **allowed** — it can only be held
on **`license`** grounds, never `editorial`. Only an OPINION/POSITION about the topic is an
editorial deny. A restricted/commercial feed stays out on `license` grounds, distinct from
the editorial line.

**Staged sources** (`surfaced: false`) are schema-checked only — they may legitimately
carry an `unknown` license or a denied class while awaiting a per-source license review.
The hard rules fire the moment a source is flipped to `surfaced: true`, so the dangerous
move (surfacing an unreviewed/excluded feed) is what gets blocked.

## How it runs (enforcement, not aspiration)

- **CI:** the `source-guardrail` job in `.github/workflows/ci.yml` runs
  `python scripts/check_sources.py` on every push/PR. Non-zero exit fails the build.
- **Pre-commit:** the `source-guardrail` local hook runs the same check whenever
  `sources/registry.json`, `CREDITS.md`, or the guardrail code changes.
- **Local:** `python scripts/check_sources.py` from the repo root.

Logic lives in [`guardrail/source_guardrail.py`](../guardrail/source_guardrail.py)
(pure stdlib, mypy-strict typed); unit tests in `tests/unit/test_source_guardrail.py`.

## Adding a new subset (the workflow this guards)

1. Add the subset to `sources/registry.json` with `surfaced: false` first.
2. Do the per-source license review; set `license`, `attribution`, `content_class`,
   and any `risk_flags` / `synthesis_cautions` honestly.
3. Add the matching `- \`key\` — Source — License` line to `CREDITS.md` **in the same PR**.
4. Flip `surfaced: true`.
5. The guardrail (pre-commit + CI) confirms the subset is licensed, attributed, credited,
   and editorially allowed — or blocks the merge.

`conflict-events-acled`, `vessel-tracking-ais`, and `military-flights-adsb` are **factual
EVENT/POSITION/TRACK channels** (allowed under the fact-vs-propaganda line — sensitivity is
no barrier). They stay `surfaced: false` **on `license` grounds only** — their upstream
license is unknown (not in the free-to-use allowlist). Each is surfaceable the moment a
clean license is confirmed; no editorial barrier remains.
