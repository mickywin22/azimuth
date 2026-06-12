# azimuth vault

The public knowledge vault — the HemySphere L1 -> L2 -> L3 doctrine run on open
global-intelligence data. All content here is **CC BY 4.0** (`../LICENSE-CONTENT.md`).

| Lane | Folder | Owner | Rule |
|------|--------|-------|------|
| **L3 Rules** | `00 Rules/` | humans + lint | editorial line + synthesis contract; every rule has a lint line |
| **L1 Sources** | `01 Sources/YYYY-MM-DD/<key>.md` | ingest (machine) | verbatim transforms of the WorldMonitor API; never hand-edited |
| **L2 Briefs** | `02 Briefs/` | `azimuth-curator` | weekly cross-linked meta-briefs; evolve in place, every claim sourced |

L1 is written by the daily GitHub-Actions ingest (`ingest/pull.py`). L2 is written by the
`azimuth-curator` fleet role (`synthesis/azimuth-curator.md`) and gated by the blocking
synthesis lint (`synthesis/lint.py` via `scripts/check_synthesis.py`).
