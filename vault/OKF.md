---
title: OKF Conformance
type: L3-rule
license: CC-BY-4.0
updated: 2026-06-24
resource: false
tags: [okf, doctrine]
---

# azimuth is an Open Knowledge Format bundle

**azimuth's whole USP in one line:** it is a public **Open Knowledge Format (OKF v0.1)
knowledge bundle** — a vendor-neutral, git-distributable corpus of markdown + YAML that
any OKF-aware agent can traverse with no bespoke parser. The L1/L2/L3 wiki doctrine azimuth
runs on is not a personal invention; it is an instance of a standard **Google independently
published**. azimuth proves that doctrine on live open-intelligence data.

> **Open Knowledge Format** (Google Cloud, v0.1 draft) defines a *Knowledge Bundle* as a
> directory tree of markdown files with YAML frontmatter, distributable as a git repository —
> exactly what this vault already is.

## Why this matters (the credibility USP)

| Lever | What azimuth gets |
|---|---|
| **External legitimacy** | "azimuth speaks a Google-published standard." The doctrine is a documented standard, not a one-off. |
| **Interoperability** | Any OKF-aware consumer can read the bundle with no custom adapter — the format is the API. |
| **Near-zero cost** | The bundle was already ~70% OKF by construction (markdown + frontmatter + git). |
| **A true story** | "We built the L1/L2/L3 wiki doctrine; Google published OKF as the same idea; here is azimuth proving it on open data." |

## Conformance status

azimuth targets the **reference-implementation-aligned** bar (matching Google's own
published example bundles, e.g. GA4 / Stack Overflow / Bitcoin):

| OKF clause | azimuth | Status |
|---|---|---|
| Markdown files + YAML frontmatter | every note | ✅ conformant |
| Frontmatter `type` on every concept | `L1-source` / `L2-brief` / `L3-rule` | ✅ conformant |
| Concept ID = file path minus `.md` | path-addressable notes | ✅ conformant |
| git-distributable bundle | public GitHub repo | ✅ conformant |
| Reserved `index.md` (directory listing) | per-folder index | ✅ conformant (Tier-1) |
| Reserved `log.md` (chronological history) | [`log.md`](log.md) — auto-generated from ingest days + brief changelogs | ✅ conformant (Tier-1) |
| Reference-agent keys `resource` + `tags` | on every note; enforced by `synthesis/lint.py` `check_frontmatter_schema`, emitted by `ingest/pull.py` | ✅ conformant (Tier-1, G6) |
| Relationships as standard markdown links | currently Obsidian `[[wikilinks]]` | ⚠️ **honest caveat — Tier-2, deferred** |

**The one honest caveat:** azimuth still expresses cross-note relationships as
`[[wikilinks]]` rather than OKF's standard `[text](/path.md)` markdown links. That migration
(Tier-2) is real engineering — it touches the synthesis lint and the curator role — and is
deliberately **deferred and folded into the knowledge-graph work**, where standards-native
links become the graph's traversal layer for free. See the [graph view](graph.html).

> Framed honestly: *azimuth is OKF-conformant* (a credibility + interop fact), not *OKF is
> the future* (an unproven bet on a v0.1 draft). Full strategy + the two-tier conformance
> plan live in `docs/strategy/okf-and-knowledge-graph.md` in the repo.

## Citations

Upstream open-data sources for every L1 note are credited per-note in frontmatter
(`attribution` / `source` / `endpoint`) and bundle-wide in `CREDITS.md`. Content is licensed
**CC-BY-4.0**; held themes are excluded per the [editorial line](editorial.html).
