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
    "source",
    "source_key",
    "endpoint",
    "retrieved",
    "license",
    "attribution",
)


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
        "source": entry.upstream_source or entry.key,
        "source_key": entry.key,
        "endpoint": entry.endpoint,
        "retrieved": retrieved.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "license": entry.license,
        "attribution": entry.attribution,
    }


def _render_frontmatter(fields: dict[str, str]) -> str:
    lines = ["---"]
    lines.extend(f"{key}: {_yaml_quote(fields[key])}" for key in FRONTMATTER_KEYS)
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


@dataclass(frozen=True)
class CapInfo:
    """How a payload cap was applied (for the honest caption). ``capped`` False = verbatim."""

    capped: bool = False
    total: int = 0
    shown: int = 0
    by: str | None = None


def _list_path(payload: object) -> tuple[str | None, list[dict[str, object]]] | None:
    """Locate the row list to cap: the payload itself, or the single list-of-objects value
    of a one-list wrapper dict (e.g. ``{"fireDetections": [...]}``). Returns (key, rows) with
    key=None when the payload IS the list, or None when there is no single cappable list."""
    if isinstance(payload, list) and payload and all(isinstance(r, dict) for r in payload):
        return None, [r for r in payload if isinstance(r, dict)]
    if isinstance(payload, dict):
        list_keys = [
            k
            for k, v in payload.items()
            if isinstance(v, list) and v and all(isinstance(r, dict) for r in v)
        ]
        if len(list_keys) == 1:
            key = list_keys[0]
            return key, [r for r in payload[key] if isinstance(r, dict)]
    return None


def _frp_sort_key(row: dict[str, object], field_name: str) -> float:
    """Numeric sort key for top-N truncation; non-numeric / missing sorts last (-inf)."""
    value = row.get(field_name)
    if isinstance(value, bool):  # bools are ints in Python; never a magnitude here
        return float("-inf")
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return float("-inf")


def cap_payload(
    payload: object, max_rows: int | None, truncate_by: str | None
) -> tuple[object, CapInfo]:
    """Cap a row payload to ``max_rows`` rows (server-agnostic), keeping the top-N by
    ``truncate_by`` when given, else the first N. Returns the (possibly rewrapped) payload and
    a ``CapInfo``. No cap / no list / under the cap -> the payload is returned unchanged.

    Pure: the caption records exactly what this did, so the truncation is never silent.
    """
    if not max_rows or max_rows <= 0:
        return payload, CapInfo()
    located = _list_path(payload)
    if located is None:
        return payload, CapInfo()
    key, rows = located
    total = len(rows)
    if total <= max_rows:
        return payload, CapInfo()
    if truncate_by:
        rows = sorted(rows, key=lambda r: _frp_sort_key(r, truncate_by), reverse=True)
    capped_rows = rows[:max_rows]
    info = CapInfo(capped=True, total=total, shown=len(capped_rows), by=truncate_by)
    if key is None:
        return capped_rows, info
    rewrapped = dict(payload) if isinstance(payload, dict) else {}
    rewrapped[key] = capped_rows
    return rewrapped, info


def render_note(entry: SourceEntry, payload: object, retrieved: datetime) -> str:
    """Render the full L1 markdown note for one source.

    When the entry declares a ``max_rows`` cap and the live payload exceeds it, the note
    renders only the capped rows and the caption states — honestly — how many of how many
    rows are shown and the field they were ranked by. The full set stays at the endpoint.
    """
    fm = frontmatter_for(entry, retrieved)
    payload, cap = cap_payload(payload, entry.max_rows, entry.truncate_by)
    title = f"# {entry.upstream_source or entry.key}"
    caption = (
        f"> L1 source pull — `{entry.key}` from `{entry.endpoint}` "
        f"at {fm['retrieved']}. Verbatim transform; never edit by hand."
    )
    if cap.capped:
        ranked = f"top {cap.shown} by `{cap.by}`" if cap.by else f"first {cap.shown}"
        caption += (
            f"\n> **Payload cap (azimuth-side, recorded for honesty):** showing {ranked} of "
            f"{cap.total} rows. The endpoint ignores limit params and returns the full set; "
            f"azimuth caps the L1 note to keep the repo lean. Full set lives at the endpoint."
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
