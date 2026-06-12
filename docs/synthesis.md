# L2 Synthesis Engine (Phase 2)

azimuth's L2 lane turns the week's L1 source notes into one evolving **Energy Supply
Weekly** brief. This is where the project makes claims about the world, so it carries the
editorial risk — and therefore the heaviest enforcement. Spec: `docs/spec.md` F2.

## Pieces

| Piece | Path | What it does |
|-------|------|--------------|
| Curator role | `synthesis/azimuth-curator.md` | The fleet role a Worker becomes weekly: read L1 → evolve the brief in place |
| Lint logic | `synthesis/lint.py` | Pure, stdlib-only blocking checks (the F2 quality gate) |
| Lint CLI | `scripts/check_synthesis.py` | git-diff + file I/O → calls `synthesis.lint`; CI + pre-commit entry point |
| Editorial line | `vault/00 Rules/editorial.md` | What a brief must not say (with the enforcing lint named) |
| Synthesis contract | `vault/00 Rules/synthesis-contract.md` | The 5 clauses the curator honours |
| The brief | `vault/02 Briefs/Energy Supply Weekly.md` | The single evolving L2 note |

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
pytest tests/unit/test_synthesis_lint.py             # 27 unit cases (green + planted breaches)
```

## Weekly cycle (target — KR-B B3, needs the scheduled-task wiring + a Michael spot-review)

```
Mon ── azimuth-curator (fleet) ── read vault/01 Sources/<week> ──▶ evolve Energy Supply Weekly.md
                                          │
                                          └─ self-check: python scripts/check_synthesis.py (exit 0)
                                          └─ commit vault/02 Briefs/ only ──▶ (first cycles) Michael spot-review
```

> **Status:** engine + lint + role + first lint-green seed brief landed (KR-B B1/B2). The
> weekly `scripts/scheduled/` task + live dry-run on banked L1 + Michael spot-review is the
> remaining B3 slice; the 2-consecutive-brief gate is a W26 verification line by construction.
