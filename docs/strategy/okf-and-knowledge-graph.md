# azimuth — OKF Conformance + Knowledge-Graph Layer (Strategy)

> **Status:** Strategy / recommendation — **RECOMMEND ONLY, no changes applied to the public bundle or production.**
> **Last updated:** 2026-06-22
> **Track:** Coding-Factory / azimuth · KR `W26-Azimuth-USP`
> **Decision owner:** Michael (go/no-go filed as an Input Queue row)
> **Sources audited:** OKF v0.1 `SPEC.md` + Google reference repo + announcement blog; Hyper-Extract (`github.com/yifanfeng97/Hyper-Extract`). Clippings: `02 Clippings/Open Knowledge Format (OKF)*.md`, `Hyper-Extract.md`.

This doc answers two questions Michael raised on 2026-06-22:

1. **OKF** — should azimuth's public bundle conform to Google's Open Knowledge Format, and what does conformance buy us (USP / credibility / interop)?
2. **Knowledge graph** — should we build a queryable knowledge-graph layer over azimuth (Hyper-Extract evaluated as the engine) to make complex cross-source analysis legible?

**Bottom line up front:**

- **OKF: GO, in two tiers.** Tier-1 conformance (frontmatter `type` + reserved `index.md`/`log.md`) is near-zero cost, buys a real external-legitimacy USP, and fits the W26 public-flip window. Tier-2 (wikilink → standard-markdown-link migration) is the expensive clause — it touches the synthesis lint and curator role — so **defer Tier-2** behind a flag until the graph work needs it.
- **Knowledge graph: GO, but NOT Hyper-Extract first.** Hyper-Extract is over-engineered for azimuth's current scale (21 source notes, 2 briefs). Ship a **lightweight wikilink/markdown-link graph extractor + a static graph view** first (reuses the existing HemySphere `vault-graph` approach), and **revisit Hyper-Extract only when the corpus is large enough and a concrete cross-source analytical question exists.**

The two parts reinforce each other: adopting OKF standard-markdown links (Tier-2) makes the relationship graph standards-native and externally traversable for free — so do OKF Tier-1 now, sequence the graph next, and fold Tier-2 into the graph work.

---

## Part 1 — OKF conformance

### 1.1 What OKF actually requires (v0.1 draft)

OKF is Google Cloud's minimal markdown-corpus standard: a **Knowledge Bundle** = a directory tree of markdown files with YAML frontmatter, distributable as a git repo. Audited against the real `SPEC.md`, the **mandatory** surface is deliberately tiny:

| OKF requirement | Source | Strictness |
|---|---|---|
| Markdown files + YAML frontmatter | §3 Bundle Structure | required |
| Frontmatter key **`type`** on every concept | §4 / §5 | **required (only mandatory key)** |
| Reserved **`index.md`** = directory listing (progressive disclosure, no frontmatter) | §6 | reserved filename |
| Reserved **`log.md`** = chronological update history, newest-first, ISO `YYYY-MM-DD` headings | §7 | reserved filename |
| Concept ID = file path minus `.md` | §2/§4 | structural (automatic) |
| Relationships expressed as **standard markdown links** (`[x](/path.md)`, bundle-relative preferred) | §5 | required form |
| Citations under a `# Citations` heading | §5 | convention |

**Important nuance the KR brief flattened:** the SPEC mandates **only `type`**. The extra keys `resource` + `tags` come from the Google **reference _agent_** (the Python generator), not the spec. So there are two conformance bars:

- **SPEC-minimal:** `type` on every concept + reserved files + markdown-link relationships.
- **Reference-impl-aligned:** also carry `resource` + `tags` (matches Google's published example bundles — GA4 / Stack Overflow / Bitcoin).

We should target reference-impl-aligned for the credibility claim ("looks like Google's own bundles"), but the spec-minimal bar is what "OKF-conformant" strictly means.

### 1.2 Gap list — azimuth `vault/` bundle vs OKF v0.1

Bundle audited: `vault/` = **21 L1 source notes · 2 L2 briefs · 3 L3 rules · 4 READMEs**.

| # | OKF clause | azimuth today | Verdict | Fix cost |
|---|---|---|---|---|
| G1 | `type` required on every concept | L2 briefs have `type: L2-brief`; L3 rules have `type: L3-rule`; **L1 sources have NO `type`** | ⚠️ partial | **Low** — add `type: L1-source` to the ingest writer (`ingest/pull.py`) frontmatter |
| G2 | Reserved `index.md` (directory listing) | uses **`README.md`** per folder; **0 `index.md`** | ❌ gap | **Low** — add `index.md` per level (can be generated from existing READMEs / `build_brief_index.py`) |
| G3 | Reserved `log.md` (chronological history) | per-brief `## Changelog` + dated source folders; **0 top-level `log.md`** | ❌ gap | **Low** — generate `log.md` from the existing changelog lines + ingest dates |
| G4 | Relationships as **standard markdown links** | **25 `[[wikilinks]]`** in briefs (Obsidian-flavoured) | ❌ gap | **HIGH** — the synthesis lint (`check_claim_sourcing`, `check_l1_links_exist`) and the `azimuth-curator` role both assume `[[wikilink]]`; migrating to `[x](/path.md)` is a lint + role rewrite, not a find-replace |
| G5 | Citations under `# Citations` heading | per-note `attribution`/`source`/`endpoint` frontmatter + top-level `CREDITS.md` | ⚠️ partial | **Low-med** — add a generated `# Citations` section, or document the frontmatter-citation mapping as an OKF profile |
| G6 | `resource` + `tags` (reference-impl convention) | absent on all notes | ⚠️ optional | **Low** — additive frontmatter keys |
| G7 | Markdown + frontmatter, git-distributable | ✅ already a public GitHub repo of markdown + YAML | ✅ pass | — |
| G8 | Concept ID = path minus `.md` | ✅ automatic (path-addressable notes) | ✅ pass | — |

**Read:** azimuth is already ~70% OKF by construction (it's literally markdown + frontmatter + git, which is the whole OKF thesis). The gaps split cleanly into **cheap (G1/G2/G3/G6, mostly the ingest + index generators)** and **one expensive clause (G4 wikilinks)** that is entangled with the synthesis lint.

### 1.3 Conformance plan — two tiers

**Tier-1 (cheap, do at/with the W26 public flip):**
1. `type: L1-source` added by `ingest/pull.py` frontmatter (G1).
2. Generate `index.md` per folder level (reuse `scripts/build_brief_index.py` pattern) (G2). Keep `README.md` as the human landing page or fold into `index.md`.
3. Generate a bundle `log.md` (newest-first, ISO date headings) from ingest dates + brief changelogs (G3).
4. Add `resource` + `tags` to the frontmatter schema + lint `check_frontmatter_schema` (G6).
5. Ship an **`OKF.md` / `okf-profile.md`** at the bundle root declaring "azimuth is an OKF v0.1 bundle" + documenting the citation mapping (G5).

→ Result after Tier-1: azimuth is a **declared, reference-impl-aligned OKF bundle** with the single honest caveat that relationships still use wikilinks (note it in the profile).

**Tier-2 (expensive, gate behind the graph work — see Part 2):**
6. Migrate `[[wikilink]]` → bundle-relative `[text](/path.md)` (G4), rewriting `check_claim_sourcing` / `check_l1_links_exist` and the `azimuth-curator` role contract to emit + validate markdown links. This is where the standards-native relationship graph comes from — so do it **as part of** building the graph layer, not before.

### 1.4 USP / value assessment — what OKF conformance buys

| Lever | Value | Strength |
|---|---|---|
| **External legitimacy** | "azimuth speaks a Google-published standard" — the L1/L2/L3 doctrine is no longer a personal invention, it's an instance of a vendor-neutral spec Google independently arrived at. Concrete proof for the doctrine-evaluator persona + LinkedIn build-in-public. | **High** |
| **Interoperability** | Any OKF-aware consumer agent can traverse azimuth's bundle with no bespoke parser. Future-proofs the public bundle as the format gets tooling. | Medium (depends on OKF adoption) |
| **Credibility at near-zero cost** | Tier-1 is generator + frontmatter work — the bundle is already 70% there. Cost-to-signal ratio is excellent. | **High** |
| **Narrative** | "We built the L1/L2/L3 wiki doctrine in 2026; Google published OKF as the same idea; here is azimuth proving it on open data" — a strong, true story. | **High** |

**Risk:** OKF is v0.1 draft — adoption is unproven; don't over-anchor the azimuth pitch on OKF ubiquity. Frame it as *"azimuth is OKF-conformant"* (a credibility + interop fact), not *"OKF is the future"* (a bet). Tier-2's lint/role rewrite is the only real engineering cost and is deferrable.

---

## Part 2 — Knowledge-graph layer

### 2.1 The goal (Michael, 2026-06-22)

> "Build a knowledge graph out of azimuth to make complex analysis clear."

azimuth's L2 briefs already do cross-source synthesis in prose (e.g. "gas storage building while crude tightens but prices soften"). A graph layer would make those cross-source relationships **queryable and visual** instead of locked in prose — "show me everything connecting energy prices to geophysical events across W23–W26".

### 2.2 Hyper-Extract evaluated

**What it is:** an LLM framework that turns unstructured text into **8 structured forms** — graphs, **hypergraphs**, spatio-temporal structures — in one command, with 10+ engines and 80+ templates.

**What it would unlock for azimuth:**
- **Hypergraphs** model n-ary relations natively: an L2 brief that synthesizes 4 L1 sources is one hyperedge over those 4 nodes — a truer model than pairwise links.
- **Spatio-temporal** templates fit azimuth's shape directly: weekly time series (gas storage, crude, prices) + geo (earthquakes, EU gas) → time- and place-indexed graph queries.
- One-command extraction over the whole `vault/` corpus.

**Cost / effort to adopt:** **High.**
- New heavyweight Python dependency + per-note LLM extraction calls (recurring token cost, every ingest cycle) on a project that hasn't flipped public yet.
- Needs a graph store + a query layer + a render surface (none exist in azimuth today).
- Hypergraph/spatio-temporal power only pays off at **large corpus + genuine n-ary analytical questions** — azimuth is currently **21 source notes + 2 briefs**. The framework's strengths are mostly idle at this scale.
- Operational surface (extraction reliability, schema drift, cost monitoring) on a demonstrator whose whole pitch is *simplicity and legibility*.

### 2.3 Lighter alternatives

| Option | What it is | Effort | Fit for azimuth now |
|---|---|---|---|
| **A. Wikilink/markdown-link graph extractor** | Parse the relationships already in the bundle (the 25 wikilinks today, or markdown links post-Tier-2) into a JSON node/edge graph; render as a static graph page. Mirrors the existing HemySphere `vault-graph` skill. | **Low** | ✅ **Best first step** — zero LLM cost, uses links the curator already writes |
| **B. OKF-native link graph** | Same as A but consuming Tier-2 standard markdown links — graph is externally traversable + standards-native for free | Low (after Tier-2) | ✅ the natural Tier-2 payoff |
| **C. Lightweight LLM entity extraction → single JSON graph + Cytoscape/D3 view** | One modest LLM pass extracts entities (commodities, regions, events) into a flat graph; static HTML view | Medium | ⏳ when link-graph proves insufficient |
| **D. Hyper-Extract (graphs/hypergraphs/spatio-temporal)** | The full framework | High | ⏳ later — only at larger corpus + real n-ary question |

### 2.4 Recommendation

**Sequence:**
1. **Now / next:** build **Option A** — a small extractor (`scripts/build_graph.py`) that reads the bundle's relationship links + brief→source mappings into a `graph.json`, plus a static graph view on the site. Reuses what the curator already produces; no new LLM cost. This is the "make complex analysis legible" win at the lowest cost.
2. **With Tier-2:** when migrating to OKF standard markdown links (G4), the graph becomes **Option B** — standards-native, externally traversable.
3. **Defer Hyper-Extract (Option D)** behind two explicit triggers: **(a)** corpus > ~200 concept notes, **AND** **(b)** a concrete cross-source analytical question the simple link-graph demonstrably can't answer (e.g. genuine n-ary or spatio-temporal queries). Re-evaluate then with a small spike, not a commitment.

**Why:** azimuth's USP is *legible, simple, standards-native doctrine on open data*. A link-graph delivers the "queryable cross-source analysis" goal in proportion to the current corpus; Hyper-Extract's hypergraph/spatio-temporal horsepower is real but premature, and its recurring LLM-extraction cost + operational surface cut against the simplicity pitch. Start light, earn the upgrade.

---

## Combined recommendation (the IQ ask)

| | Recommendation | Cost | When |
|---|---|---|---|
| **OKF Tier-1** | **GO** — `type` on L1, generated `index.md` + `log.md`, `resource`/`tags`, declare an OKF profile | Low | W26 public-flip window |
| **OKF Tier-2** | **GO, deferred** — wikilink → markdown-link migration (+ lint/role rewrite) | High | fold into the graph work |
| **Graph layer** | **GO** — lightweight link-graph extractor + static view first | Low | next azimuth build slice |
| **Hyper-Extract** | **NO-GO for now** — defer behind corpus-size + real-question triggers | High | re-evaluate later |

**Gate honoured:** this dispatch applied **zero** changes to the public bundle, the synthesis lint, the curator role, or production. Everything above is a recommendation pending Michael's go/no-go (filed as an Input Queue row).
