"""Source-guardrail logic.

A *standing* guardrail: it runs in CI (scripts/check_sources.py) on every push and
blocks the build if any surfaced WorldMonitor subset is missing a license, missing
attribution, carries a denied content class / risk flag, or is surfaced without a
credit line in CREDITS.md.

Pure-stdlib (json), fully typed for mypy --strict.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

# The azimuth editorial exclusions (spec.md "L3 rule set"). A surfaced source whose
# content_class is one of these — or that carries one of these as a risk flag — is a
# hard guardrail violation.
DENIED_CONTENT_CLASSES: frozenset[str] = frozenset(
    {"investment-advice", "safety-prediction", "political-opinion"}
)


@dataclass(frozen=True)
class SourceEntry:
    """One registered WorldMonitor-derived data subset."""

    key: str
    endpoint: str
    upstream_source: str
    license: str
    attribution: str
    content_class: str
    surfaced: bool
    risk_flags: tuple[str, ...] = ()
    synthesis_cautions: tuple[str, ...] = ()

    @staticmethod
    def from_dict(raw: dict[str, Any]) -> SourceEntry:
        missing = [
            field_name
            for field_name in ("key", "endpoint", "content_class")
            if not raw.get(field_name)
        ]
        if missing:
            raise ValueError(f"source entry missing required field(s): {', '.join(missing)}")
        return SourceEntry(
            key=str(raw["key"]),
            endpoint=str(raw["endpoint"]),
            upstream_source=str(raw.get("upstream_source", "")),
            license=str(raw.get("license", "")),
            attribution=str(raw.get("attribution", "")),
            content_class=str(raw["content_class"]),
            surfaced=bool(raw.get("surfaced", False)),
            risk_flags=tuple(str(flag) for flag in raw.get("risk_flags", [])),
            synthesis_cautions=tuple(str(c) for c in raw.get("synthesis_cautions", [])),
        )


@dataclass(frozen=True)
class Violation:
    """A single guardrail breach for one source."""

    source_key: str
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.source_key}] {self.rule}: {self.detail}"


@dataclass
class GuardrailResult:
    """Outcome of checking the whole registry."""

    violations: list[Violation] = field(default_factory=list)
    checked: int = 0
    surfaced: int = 0

    @property
    def ok(self) -> bool:
        return not self.violations


@dataclass(frozen=True)
class Registry:
    """Parsed registry.json."""

    allowed_content_classes: frozenset[str]
    license_allowlist: frozenset[str]
    sources: tuple[SourceEntry, ...]


def load_registry(path: Path) -> Registry:
    """Load and shallow-validate sources/registry.json."""
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    policy: dict[str, Any] = data.get("content_class_policy", {})
    allowed = frozenset(str(c) for c in policy.get("allowed", []))
    license_allowlist = frozenset(str(lic) for lic in data.get("license_allowlist", []))
    sources = tuple(SourceEntry.from_dict(item) for item in data.get("sources", []))
    return Registry(
        allowed_content_classes=allowed,
        license_allowlist=license_allowlist,
        sources=sources,
    )


def check_source(
    entry: SourceEntry,
    *,
    allowed_content_classes: frozenset[str],
    license_allowlist: frozenset[str],
    credited_keys: frozenset[str],
) -> list[Violation]:
    """Return every guardrail breach for one source.

    Non-surfaced (staged) sources are schema-checked only — they may legitimately carry
    an ``unknown`` license / denied class while awaiting review. The hard rules fire only
    once a source is marked ``surfaced: true``.
    """
    violations: list[Violation] = []

    # A denied content class or risk flag is a violation regardless of surfaced state for
    # the content_class itself only matters when surfaced; but a surfaced denied source is
    # the dangerous case we must block.
    denied_class = entry.content_class in DENIED_CONTENT_CLASSES
    denied_flags = sorted(set(entry.risk_flags) & DENIED_CONTENT_CLASSES)

    if not entry.surfaced:
        # Staged source: only assert it is honestly NOT pretending to be safe — if it has
        # a denied class/flag it must stay unsurfaced (which it is). Nothing to block.
        return violations

    if denied_class:
        violations.append(
            Violation(
                entry.key,
                "denied-content-class",
                f"content_class '{entry.content_class}' is an editorial exclusion; "
                "must not be surfaced",
            )
        )
    if denied_flags:
        violations.append(
            Violation(
                entry.key,
                "denied-risk-flag",
                f"risk_flags {denied_flags} are editorial exclusions; must not be surfaced",
            )
        )
    if entry.content_class not in allowed_content_classes:
        violations.append(
            Violation(
                entry.key,
                "unlisted-content-class",
                f"content_class '{entry.content_class}' is not in the allowed policy list",
            )
        )
    if not entry.license:
        violations.append(Violation(entry.key, "missing-license", "no license recorded"))
    elif entry.license not in license_allowlist:
        violations.append(
            Violation(
                entry.key,
                "unrecognised-license",
                f"license '{entry.license}' is not in the allowlist "
                "(per-source license review required before surfacing)",
            )
        )
    if not entry.attribution:
        violations.append(
            Violation(entry.key, "missing-attribution", "no attribution string recorded")
        )
    if entry.key not in credited_keys:
        violations.append(
            Violation(
                entry.key,
                "missing-credit",
                "surfaced source is not credited in CREDITS.md",
            )
        )

    return violations


def parse_credited_keys(credits_text: str) -> frozenset[str]:
    """Extract source keys credited in CREDITS.md.

    Convention: each credited source is tagged with its registry key in backticks,
    e.g. ``- `natural-gas-storage-eu` — GIE AGSI+ — CC-BY-4.0``. Keeping the key explicit
    keeps the credit/registry join machine-checkable rather than fuzzy name-matching.
    """
    keys: set[str] = set()
    for line in credits_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and "`" in stripped:
            first = stripped.find("`")
            second = stripped.find("`", first + 1)
            if second > first:
                keys.add(stripped[first + 1 : second])
    return frozenset(keys)


def check_registry(registry_path: Path, credits_path: Path) -> GuardrailResult:
    """Check the whole registry against CREDITS.md. CI entry point."""
    registry = load_registry(registry_path)
    credited_keys = (
        parse_credited_keys(credits_path.read_text(encoding="utf-8"))
        if credits_path.exists()
        else frozenset()
    )
    result = GuardrailResult()
    for entry in registry.sources:
        result.checked += 1
        if entry.surfaced:
            result.surfaced += 1
        result.violations.extend(
            check_source(
                entry,
                allowed_content_classes=registry.allowed_content_classes,
                license_allowlist=registry.license_allowlist,
                credited_keys=credited_keys,
            )
        )
    return result
