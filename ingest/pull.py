"""L1 ingest: registry-driven pull + markdown transform.

The single-source-of-truth contract
------------------------------------
There is deliberately **no** ``ingest/endpoints.json``. The endpoint to pull, the
``license`` to stamp into the L1 note, and the attribution line all come from the same
``sources/registry.json`` entry the source-guardrail validates. Ingest reuses the
guardrail's ``load_registry`` + ``check_source`` so that:

* a subset's endpoint/license/attribution is defined in exactly one place; and
* a surfaced source that does **not** pass the guardrail (missing/disallowed license,
  missing attribution/credit, editorial-exclusion class) never produces an L1 note —
  ingest refuses it for the same reason CI would fail the build.

Pure stdlib, fully typed for mypy --strict. The HTTP fetch is injected (``Fetcher``)
so the transform + frontmatter logic is testable offline and degraded-mode (a failing
fetch skips that source, logs, and never crashes the run).
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from guardrail import check_source, load_registry, parse_credited_keys

if TYPE_CHECKING:
    from guardrail import Registry, SourceEntry

logger = logging.getLogger("azimuth.ingest")

# Frontmatter keys every L1 note carries (spec.md F1: source, endpoint, retrieved,
# license). ``source_key`` + ``attribution`` are added so the note ↔ registry join stays
# machine-checkable and the CC-BY / ToS attribution obligation travels with the data.
FRONTMATTER_KEYS: tuple[str, ...] = (
    "type",
    "source",
    "source_key",
    "endpoint",
    "retrieved",
    "license",
    "attribution",
    # OKF reference-impl-aligned keys (G6): every concept carries `resource` (does it
    # wrap an external data resource — true for L1 source pulls) + `tags` (topical
    # inline list). Enforced by synthesis/lint.py check_frontmatter_schema.
    "resource",
    "tags",
)

# Keys whose value is a YAML scalar boolean / inline list, emitted RAW (unquoted) so the
# frontmatter parser reads `resource: true` and `tags: [a, b]`, not quoted strings.
RAW_FRONTMATTER_KEYS: frozenset[str] = frozenset({"resource", "tags"})

# Coarse topical tag per source key, so backfilled L1 notes read like Google's OKF
# example bundles rather than carrying an empty list. Unknown keys fall back to [].
_TAG_CATEGORY: dict[str, str] = {
    "crude-oil-inventories": "energy",
    "natural-gas-storage-eu": "energy",
    "fuel-prices": "energy",
    "energy-prices": "energy",
    "earthquakes": "geophysical",
    "prediction-markets": "markets",
}


def _infer_tags(source_key: str) -> str:
    """Inline-list tag string for an L1 source: `[<source_key>, <category>]`."""
    tags = [source_key]
    category = _TAG_CATEGORY.get(source_key)
    if category and category != source_key:
        tags.append(category)
    return "[" + ", ".join(tags) + "]"


# OKF v0.1 layer tag — every L1 source note declares its layer in frontmatter so any
# OKF-aware agent can classify it without inspecting the path. (L2 briefs -> "L2-brief",
# the editorial rule -> "L3-rule".) This is the L1 half of that contract.
L1_SOURCE_TYPE = "L1-source"


@runtime_checkable
class Fetcher(Protocol):
    """Pulls the raw decoded JSON payload for one endpoint.

    Implementations should raise on any failure (network, HTTP, decode); the ingest
    loop turns a raised exception into a logged skip (degraded mode), never a crash.
    """

    def fetch(self, endpoint: str) -> object: ...


@dataclass(frozen=True)
class L1Note:
    """One rendered L1 source note ready to write."""

    source_key: str
    relative_path: Path
    text: str


@dataclass
class IngestOutcome:
    """Result of one ingest run."""

    written: list[L1Note] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """True when nothing errored. An empty run (all skipped) is still ok."""
        return not self.errors


def _yaml_quote(value: str) -> str:
    """Double-quote a scalar for the simple flat frontmatter block we emit."""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def frontmatter_for(entry: SourceEntry, retrieved: datetime) -> dict[str, str]:
    """Build the L1 frontmatter for one source — every field sourced from the registry.

    ``license`` and ``attribution`` are read straight off the registry ``entry``; this is
    the wire that makes ingest and the guardrail share one source of truth.
    """
    return {
        "type": L1_SOURCE_TYPE,
        "source": entry.upstream_source or entry.key,
        "source_key": entry.key,
        "endpoint": entry.endpoint,
        "retrieved": retrieved.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "license": entry.license,
        "attribution": entry.attribution,
        # An L1 source note IS the external data resource (it wraps a live API endpoint).
        "resource": "true",
        "tags": _infer_tags(entry.key),
    }


def _render_frontmatter(fields: dict[str, str]) -> str:
    lines = ["---"]
    for key in FRONTMATTER_KEYS:
        value = fields[key]
        rendered = value if key in RAW_FRONTMATTER_KEYS else _yaml_quote(value)
        lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


def _render_payload(payload: object) -> str:
    """Verbatim-faithful markdown for the decoded JSON. Zero synthesis.

    * list of flat objects -> a markdown table (column union, deterministic order)
    * single object        -> a key/value table
    * anything else        -> a fenced ```json block
    """
    if isinstance(payload, list) and payload and all(isinstance(row, dict) for row in payload):
        rows: list[dict[str, object]] = [row for row in payload if isinstance(row, dict)]
        columns: list[str] = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(str(key))
        header = "| " + " | ".join(columns) + " |"
        divider = "| " + " | ".join("---" for _ in columns) + " |"
        body = [
            "| " + " | ".join(_cell(row.get(col, "")) for col in columns) + " |" for row in rows
        ]
        return "\n".join([header, divider, *body])

    if isinstance(payload, dict):
        header = "| field | value |"
        divider = "| --- | --- |"
        body = [f"| {key} | {_cell(value)} |" for key, value in payload.items()]
        return "\n".join([header, divider, *body])

    return (
        "```json\n" + json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n```"
    )


def _cell(value: object) -> str:
    """One table cell — scalar verbatim, nested JSON inlined, pipes escaped."""
    if isinstance(value, (dict, list)):
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    elif isinstance(value, bool):
        rendered = "true" if value else "false"
    elif value is None:
        rendered = ""
    else:
        rendered = str(value)
    return rendered.replace("|", "\\|").replace("\n", " ")


def render_note(entry: SourceEntry, payload: object, retrieved: datetime) -> str:
    """Render the full L1 markdown note for one source."""
    fm = frontmatter_for(entry, retrieved)
    title = f"# {entry.upstream_source or entry.key}"
    caption = (
        f"> L1 source pull — `{entry.key}` from `{entry.endpoint}` "
        f"at {fm['retrieved']}. Verbatim transform; never edit by hand."
    )
    return "\n".join(
        [_render_frontmatter(fm), "", title, "", caption, "", _render_payload(payload), ""]
    )


def eligible_sources(registry: Registry, credited_keys: frozenset[str]) -> list[SourceEntry]:
    """Surfaced sources that also pass the guardrail.

    A surfaced-but-non-compliant source (missing license, editorial exclusion, etc.) is
    excluded here for the exact reason CI would block it — keeping ingest honest to the
    same registry the guardrail enforces.
    """
    eligible: list[SourceEntry] = []
    for entry in registry.sources:
        if not entry.surfaced:
            continue
        violations = check_source(
            entry,
            allowed_content_classes=registry.allowed_content_classes,
            license_allowlist=registry.license_allowlist,
            credited_keys=credited_keys,
        )
        if violations:
            logger.warning(
                "ingest: skipping surfaced source %s — guardrail violations: %s",
                entry.key,
                "; ".join(str(v) for v in violations),
            )
            continue
        eligible.append(entry)
    return eligible


def pull(
    *,
    registry_path: Path,
    credits_path: Path,
    fetcher: Fetcher,
    out_dir: Path,
    now: datetime | None = None,
    write: bool = True,
) -> IngestOutcome:
    """Pull every eligible surfaced source and write dated L1 notes.

    Notes land under ``out_dir / YYYY-MM-DD / <key>.md``. A fetch that raises is logged
    and recorded as an error for that source; the run continues (degraded mode).
    """
    moment = now or datetime.now(UTC)
    day_dir = out_dir / moment.astimezone(UTC).strftime("%Y-%m-%d")
    registry = load_registry(registry_path)
    credited = (
        parse_credited_keys(credits_path.read_text(encoding="utf-8"))
        if credits_path.exists()
        else frozenset()
    )

    outcome = IngestOutcome()
    sources = eligible_sources(registry, credited)
    surfaced_keys = {e.key for e in registry.sources if e.surfaced}
    for skipped_key in sorted(surfaced_keys - {e.key for e in sources}):
        outcome.skipped[skipped_key] = "failed guardrail (not surfaced as L1)"

    for entry in sources:
        try:
            payload = fetcher.fetch(entry.endpoint)
        except Exception as exc:
            logger.warning("ingest: fetch failed for %s (%s) — skipping", entry.key, exc)
            outcome.errors[entry.key] = str(exc)
            continue

        note_text = render_note(entry, payload, moment)
        relative_path = Path(day_dir.name) / f"{entry.key}.md"
        if write:
            day_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / relative_path).write_text(note_text, encoding="utf-8")
        outcome.written.append(
            L1Note(source_key=entry.key, relative_path=relative_path, text=note_text)
        )

    logger.info(
        "ingest: %d written, %d skipped, %d errored",
        len(outcome.written),
        len(outcome.skipped),
        len(outcome.errors),
    )
    return outcome
