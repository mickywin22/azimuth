# azimuth — OKF v0.1 Bundle Profile

> **Claim:** azimuth is a **Knowledge Bundle conformant with the Open Knowledge Format (OKF) v0.1**
> (Google Cloud's vendor-neutral markdown-corpus standard), at the **spec-minimal** bar, with the
> honest caveats listed in §4.
> **Bundle root:** [`vault/`](vault/) — 21 L1 source notes, 2 L2 briefs, 3 L3 rules.
> **Verified:** 2026-06-24. Full audit + gap list: [`docs/strategy/okf-and-knowledge-graph.md`](docs/strategy/okf-and-knowledge-graph.md).

## 1. What OKF is, and why azimuth declares conformance

OKF defines a **Knowledge Bundle** as a directory tree of markdown files with YAML frontmatter,
distributable as a git repo. azimuth's `vault/` is already exactly that: it applies the HemySphere
**L1 sources → L2 synthesis → L3 rules** doctrine to open WorldMonitor intelligence data. Declaring
OKF conformance makes that doctrine an instance of a published, vendor-neutral spec rather than a
personal convention — the credibility + interoperability USP for the public demonstrator.

`type` is the **only mandatory frontmatter key** in the OKF v0.1 spec. The extra `resource` + `tags`
keys come from Google's reference *agent* (the example generator), not the spec — so azimuth targets
the **spec-minimal** conformance bar today and tracks reference-impl alignment as a Tier-1 follow-up (§4).

## 2. Conformance matrix (verified 2026-06-24)

| OKF v0.1 requirement | Strictness | azimuth state | Status |
|---|---|---|---|
| Markdown files + YAML frontmatter, git-distributable | required | public GitHub repo of markdown + YAML | ✅ pass |
| Frontmatter key `type` on every concept | **required (only mandatory key)** | `L1-source` / `L2-brief` / `L3-rule` on all 32 concept notes | ✅ pass |
| Concept ID = file path minus `.md` | structural | path-addressable notes under `vault/` | ✅ pass (automatic) |
| Reserved `index.md` = directory listing (no frontmatter) | reserved filename | per-folder **`README.md`** listings serve this role; **0 `index.md`** | ⚠️ named differently (Tier-1 follow-up) |
| Reserved `log.md` = newest-first ISO-dated history | reserved filename | per-brief `## Changelog` + dated source folders; **0 top-level `log.md`** | ⚠️ Tier-1 follow-up |
| Relationships as standard markdown links `[x](/path.md)` | required form | **29 `[[wikilink]]`** relationships in briefs | ❌ **Tier-2 (deferred — see §4)** |
| Citations | convention (`# Citations` heading) | frontmatter citation keys + `CREDITS.md` + `sources/registry.json` | ⚠️ mapped, not heading-based — see §3 |
| `resource` + `tags` (reference-agent convention) | optional | absent | ⚠️ Tier-1 follow-up |

**Read:** azimuth passes every **mandatory** OKF v0.1 clause (markdown + frontmatter + `type` + path-IDs).
The open items are one reserved-filename convention (`index.md`/`log.md`), the optional reference-agent
keys, and the relationship-link form — the last of which is the deferred Tier-2 clause.

## 3. Citation mapping

OKF suggests citations under a `# Citations` heading. azimuth instead carries attribution in
**machine-checkable frontmatter + two bundle-level registries**, and this profile is the declared mapping:

| OKF citation intent | azimuth mechanism | Where |
|---|---|---|
| Per-concept source attribution | L1 frontmatter: `source`, `source_key`, `endpoint`, `retrieved`, `license`, `attribution` | every note under [`vault/01 Sources/`](vault/01%20Sources/) |
| Synthesis → source provenance | L2 frontmatter `sources: [<source_key>, …]` array | [`vault/02 Briefs/`](vault/02%20Briefs/) |
| Bundle-level credit ledger | `CREDITS.md`, each credit line tagged with its registry `key` | [`CREDITS.md`](CREDITS.md) |
| Canonical, guardrail-enforced source registry | `sources/registry.json` — validated by `scripts/check_sources.py` before any subset is surfaced | [`sources/registry.json`](sources/registry.json) |

The `source_key` value is the join key across all four: L1 frontmatter ↔ L2 `sources[]` ↔ `CREDITS.md`
↔ `registry.json`. An OKF-aware consumer reads provenance from frontmatter rather than a `# Citations`
block; this profile is the declaration of that mapping.

## 4. Honest caveats — what is NOT yet conformant

- **Tier-2 deferred — relationships still use `[[wikilinks]]`.** The 29 cross-note relationships in the
  L2 briefs are Obsidian-flavoured `[[wikilink]]`s, **not** the OKF-required standard markdown links
  `[text](/path.md)`. Migrating them is **Tier-2** and is **deliberately deferred**: it is entangled with
  the synthesis lint (`synthesis/lint.py` `check_claim_sourcing` / `check_l1_links_exist`) and the
  `azimuth-curator` role contract, so it is folded into the knowledge-graph build slice rather than done
  as a blind find-replace. Approved deferral: IQ #851. Rationale + plan: §1.3 Tier-2 of the strategy doc.
- **`index.md` / `log.md` not yet generated.** Folder listings use `README.md`; there is no top-level
  `log.md`. These are cheap Tier-1 follow-ups (generators), tracked under KR `W26-Azimuth-USP`.
- **`resource` + `tags` keys absent.** These match Google's reference-agent example bundles but are not
  spec-mandatory; adding them (Tier-1) lifts azimuth from spec-minimal to reference-impl-aligned.

**Framing:** azimuth is **"OKF-conformant"** at the spec-minimal bar (a credibility + interop fact), not
a bet that "OKF is the future" — OKF is a v0.1 draft and its adoption is unproven.
