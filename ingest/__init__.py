"""azimuth L1 ingest.

Pulls each surfaced WorldMonitor subset and writes a dated, verbatim-faithful L1
markdown note. The endpoint set AND the ``license`` / ``attribution`` frontmatter are
read straight from ``sources/registry.json`` via the guardrail's ``load_registry`` —
so ingest and the source-guardrail share ONE source of truth and can never drift.

See docs/l1-ingest.md.
"""

from ingest.pull import (
    IngestOutcome,
    L1Note,
    eligible_sources,
    frontmatter_for,
    pull,
    render_note,
)

__all__ = [
    "IngestOutcome",
    "L1Note",
    "eligible_sources",
    "frontmatter_for",
    "pull",
    "render_note",
]
