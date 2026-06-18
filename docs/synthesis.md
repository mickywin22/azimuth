# L2 Synthesis Engine (Phase 2)

azimuth's L2 lane turns the week's L1 source notes into **one evolving brief per
editorially-clean theme**. This is where the project makes claims about the world, so it
carries the editorial risk — and therefore the heaviest enforcement. Spec: `docs/spec.md` F2.

## Themes (W26 multi-theme expansion)

The brief-per-theme mapping is **data-driven** in `sources/registry.json` (`themes` map +
each source's `theme`), so ingest, the guardrail, the curator and the index all share one
source of truth.

| Theme | Brief | L1 sources | Status |
|-------|-------|------------|--------|
| `energy-supply` | `Energy Supply Weekly.md` | natural-gas-storage-eu, crude-oil-inventories, fuel-prices, energy-prices | ✅ active |
| `geophysical` | `Geophysical Weekly.md` | earthquakes | ✅ active |
| `prediction-markets` | `Prediction Markets Weekly.md` | prediction-markets | ⏸ L1 active, L2 **held** (see registry `hold_reason`) |

Maritime (AIS), Air-traffic (ADS-B) and Conflict (ACLED) stay `surfaced:false` — they fail
the source-guardrail (editorial deny-list + unknown licence) and each carries a logged
`surfaced_reason` in the registry.

## Pieces

| Piece | Path | What it does |
|-------|------|--------------|
| Curator role | `synthesis/azimuth-curator.md` | The fleet role a Worker becomes weekly: read L1 → evolve **each clean theme's** brief in place |
| Lint logic | `synthesis/lint.py` | Pure, stdlib-only blocking checks (the F2 quality gate) |
| Lint CLI | `scripts/check_synthesis.py` | git-diff + file I/O → calls `synthesis.lint`; lints **every** brief; CI + pre-commit entry point |
| Brief index | `scripts/build_brief_index.py` | Regenerates `vault/02 Briefs/README.md` (all briefs + last-updated + held themes); `--check` is a CI/pre-commit guard |
| Editorial line | `vault/00 Rules/editorial.md` | What a brief must not say (with the enforcing lint named) |
| Synthesis contract | `vault/00 Rules/synthesis-contract.md` | The 5 clauses the curator honours |
| The briefs | `vault/02 Briefs/*.md` | One evolving L2 note per clean theme + the auto index |

## The blocking checks (`synthesis/lint.py`)

1. **claim-sourcing** — every claim paragraph/bullet carries ≥1 `[[wikilink]]`. Headings,
   tables, blockquote captions and the `## Changelog` are not claims. Soft-wrapped bullets
   count as one unit, so a link on the continuation line still sources the bullet.
2. **l1-links-exist** — each wikilink resolves to a real L1 note under `vault/01 Sources/`.
3. **frontmatter-schema** — required keys present; `type: L2-brief`, `license: CC-BY-4.0`,
   `week: YYYY-Www`, ISO-Z `updated`.
4. **evolve-not-duplicate** — a `## Changelog` with ≥1 dated line proves edit-in-place.
5. **editorial-denylist** — investment-advice / safety-prediction / political-opinion
   phrasings are rejected.
6. **diff-guard** — a synthesis commit may touch `vault/02 Briefs/` only; editing an L1
   note (or anything else) fails. Runs in CI/pre-commit from the changed-path set.

## Run it

```bash
python scripts/check_synthesis.py                    # lint every brief
python scripts/check_synthesis.py --diff-base origin/main   # + diff guard on a PR
python scripts/build_brief_index.py                  # regenerate the brief index
python scripts/build_brief_index.py --check          # CI guard: index in sync
pytest tests/unit/                                   # synthesis lint + registry-theme cases
```

## Weekly cycle (target — KR-B B3, needs the scheduled-task wiring + a Michael spot-review)

```
Mon ── azimuth-curator (fleet) ── read vault/01 Sources/<week> ──▶ evolve EACH clean theme's brief
                                          │
                                          └─ self-check: python scripts/check_synthesis.py (exit 0)
                                          └─ regenerate: python scripts/build_brief_index.py
                                          └─ commit vault/02 Briefs/ only ──▶ (first cycles) Michael spot-review
```

> **Status (W26):** engine + lint + role + brief index landed and the curator is now
> **multi-theme** (energy-supply + geophysical active; prediction-markets L1-active, L2 held).
> The daily L1 ingest (GH Actions `ingest.yml`) already pulls every surfaced clean channel.
> The remaining B3 slice is the *scheduled* weekly curator task (`scripts/scheduled/` on the
> HemySphere box / fleet cadence) + Michael spot-review; this dispatch ran the curator by hand
> end-to-end and both active briefs are lint-green off the live 2026-06-18 ingest.
