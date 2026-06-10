"""Per-source license + content guardrail for azimuth.

Validates every WorldMonitor-derived data subset against the azimuth L3 rule set
(license present + recognised, attribution present, content class allowed, surfaced
sources credited) BEFORE the subset may be surfaced as L1 source data.

See docs/source-guardrail.md for the human-readable rule.
"""

from src.backend.guardrail.source_guardrail import (
    DENIED_CONTENT_CLASSES,
    GuardrailResult,
    SourceEntry,
    Violation,
    check_registry,
    check_source,
    load_registry,
)

__all__ = [
    "DENIED_CONTENT_CLASSES",
    "GuardrailResult",
    "SourceEntry",
    "Violation",
    "check_registry",
    "check_source",
    "load_registry",
]
