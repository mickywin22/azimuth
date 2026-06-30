---
type: OKF-Bundle
resource: https://github.com/mickywin22/azimuth
tags: [azimuth, open-data, intelligence, energy, geophysics, climate, open-knowledge-format]
license: CC-BY-4.0
---

# azimuth — Open Knowledge Bundle

> A public, read-only knowledge vault running the HemySphere L1→L2→L3 wiki doctrine on open global-intelligence data. The same structural pattern Google independently published as the Open Knowledge Format (OKF).

## Bundle layers

| Layer | Path | Contents |
|-------|------|----------|
| L1 Sources | `vault/01 Sources/` | Daily verbatim pulls from WorldMonitor feeds (per-source, per-day markdown notes with OKF `type: L1-Source`) |
| L2 Briefs | `vault/02 Briefs/` | Weekly cross-source synthesis — facts only, every claim source-linked, `type: L2-brief` |
| Rules | `vault/00 Rules/` | Editorial line + source registry; the guardrail that makes synthesis safe to publish |

## OKF conformance

azimuth is built against [OKF Tier-1](https://github.com/google-deepmind/open-knowledge-format):

- `type:` on every note (`L1-Source` / `L2-brief` / `OKF-Bundle`)
- `resource:` on L1 notes → the WorldMonitor API endpoint URL
- `license:` on every note (CC-BY-4.0 for briefs; upstream license for L1 sources)
- Machine-readable source registry (`sources/registry.json`)
- Generated `vault/02 Briefs/README.md` as the brief index

See `vault/02 Briefs/README.md` for the live brief index and held-theme list.
