---
title: Synthesis Contract
type: L3-rule
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator)
---

# Synthesis Contract (L3)

The contract the `azimuth-curator` honours every weekly cycle. Enforced by
`synthesis/lint.py` (run in CI + pre-commit via `scripts/check_synthesis.py`).

1. **L1 is never edited after creation.** The curator reads `vault/01 Sources/` and
   writes only `vault/02 Briefs/`. A synthesis commit that touches an L1 note fails the
   build. *(Enforced: `check_diff_guard`.)*
2. **L2 evolves, never overwrites.** Each weekly run deepens the **existing**
   `Energy Supply Weekly` brief in place and appends a dated `## Changelog` line — it does
   not fork a shallow new note per week. *(Enforced: `check_evolve_not_duplicate`.)*
3. **Every claim is sourced.** Each claim paragraph/bullet carries >=1 `[[wikilink]]` that
   resolves to a real L1 note. *(Enforced: `check_claim_sourcing` + `check_l1_links_exist`.)*
4. **Editorial line holds.** No investment advice, safety prediction, or political opinion
   (`editorial.md`). *(Enforced: `check_editorial_denylist`.)*
5. **Frontmatter is valid + locked.** `type: L2-brief`, `license: CC-BY-4.0`, ISO-Z
   `updated`, `YYYY-Www` `week`, plus the required key set. *(Enforced:
   `check_frontmatter_schema`.)*

> A brief that fails any clause does not ship. The lint is blocking; the first weekly
> cycles also carry a Michael spot-review (spec.md F2 / KR-B B3) before the repo flips
> public.
