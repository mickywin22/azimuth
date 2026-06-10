# Source Guardrail — per-source license + content check

> **Standing L3 rule.** Before any new WorldMonitor-derived subset is surfaced as azimuth
> L1 source data, it must pass this guardrail. This is the *lint line* behind the
> `spec.md` L3 rule set — "a rule without a lint line is a TODO, not a rule".

## What it enforces

Every entry in [`sources/registry.json`](../sources/registry.json) marked `surfaced: true`
must satisfy **all** of:

| Check | Rule id | Why |
|-------|---------|-----|
| License recorded and in the allowlist | `missing-license` / `unrecognised-license` | Path A is API-consumer; each upstream source needs a known, compatible license before redistribution |
| Attribution string present | `missing-attribution` | CC-BY / ToS attribution obligation |
| Credited in `CREDITS.md` (by registry `key`) | `missing-credit` | the credit ↔ registry join must be machine-checkable, not fuzzy |
| Content class in the allowed policy list | `unlisted-content-class` | no surfacing an unclassified subset |
| Content class is not an editorial exclusion | `denied-content-class` | no investment-advice / safety-prediction / political-opinion content |
| No risk flag is an editorial exclusion | `denied-risk-flag` | a subset tagged with an excluded risk may not be surfaced |

**Editorial exclusions** (hard deny): `investment-advice`, `safety-prediction`,
`political-opinion`. These mirror `vault/00 Rules/editorial.md` (spec L3).

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

Logic lives in [`src/backend/guardrail/source_guardrail.py`](../src/backend/guardrail/source_guardrail.py)
(pure stdlib, mypy-strict typed); unit tests in `tests/unit/test_source_guardrail.py`.

## Adding a new subset (the workflow this guards)

1. Add the subset to `sources/registry.json` with `surfaced: false` first.
2. Do the per-source license review; set `license`, `attribution`, `content_class`,
   and any `risk_flags` / `synthesis_cautions` honestly.
3. Add the matching `- \`key\` — Source — License` line to `CREDITS.md` **in the same PR**.
4. Flip `surfaced: true`.
5. The guardrail (pre-commit + CI) confirms the subset is licensed, attributed, credited,
   and editorially allowed — or blocks the merge.

A subset that cannot pass (e.g. `conflict-events-acled`, `vessel-tracking-ais`,
`military-flights-adsb` — political-opinion / safety-prediction risk) stays `surfaced: false`
indefinitely under the current editorial line.
