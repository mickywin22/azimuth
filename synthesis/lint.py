#!/usr/bin/env python3
"""Blocking synthesis lint for azimuth L2 briefs (spec.md F2 quality gate).

The L2 lane is where azimuth makes *claims* about the world from open data, so it
carries the project's editorial risk. Per the spec, "a rule without a lint line is a
TODO, not a rule" — every L3 synthesis rule is enforced here, blocking, in CI and
pre-commit. The checks (all from ``docs/spec.md`` F2 + ``vault/00 Rules/``):

  1. claim-sourcing      — every L2 claim paragraph/bullet carries >=1 ``[[wikilink]]``.
  2. l1-links-exist      — each wikilink resolves to a real L1 note under 01 Sources/.
  3. frontmatter-schema  — the brief frontmatter has the required keys + locked values
                           (type=L2-brief, license=CC-BY-4.0, ISO-Z ``updated``, ``week``).
  4. evolve-not-duplicate— the brief carries a ``## Changelog`` with >=1 dated line, the
                           edit-in-place signal (L2 evolves the prior week, never forks a
                           shallow new note).
  5. editorial-denylist  — NON-FACTUAL synthesis is rejected: investment-advice,
                           safety/forecast POSITION-taking, political propaganda, and
                           opinion/advocacy framing (``vault/00 Rules/editorial.md``,
                           2026-06-24 fact-vs-propaganda line). Sensitive TOPICS are fine;
                           only opinions/positions about them are flagged.
  6. diff-guard          — a synthesis commit may touch ``vault/02 Briefs/`` only; any
                           ``vault/01 Sources/`` mutation fails (the curator must never
                           edit L1). Operates on a list of changed paths (wired by the CLI).

Pure stdlib — the synthesis lane carries no third-party runtime, so neither does its
lint. Each check returns a list of human-readable violation strings; ``lint_brief``
aggregates. Empty list == clean.
"""

from __future__ import annotations

import re
from pathlib import Path

# --- Frontmatter contract for an L2 brief --------------------------------------------
REQUIRED_KEYS: tuple[str, ...] = (
    "title",
    "type",
    "theme",
    "week",
    "updated",
    "sources",
    "license",
    "attribution",
)
LOCKED_TYPE = "L2-brief"
LOCKED_LICENSE = "CC-BY-4.0"  # IQ #371 (A): content = CC BY 4.0

_WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
_UPDATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
_CHANGELOG_LINE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

# --- Editorial deny-list (vault/00 Rules/editorial.md enforcement) -------------------
# Rewritten to the fact-vs-propaganda line (Michael 2026-06-24): the lint flags
# NON-FACTUAL synthesis — advocacy, opinion, blame, and political-or-safety POSITION-
# taking — NOT sensitive topics. Reporting an observed fact on ANY topic is fine ("a
# conflict event was logged ([[conflict-events]])"); editorialising about it is not
# ("the regime is to blame"). Phrase-level, word-boundaried patterns stay clear of
# neutral reporting ("crude inventories rose 2%", "USGS logged a M5.8 event").
_EDITORIAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "investment-advice",
        re.compile(
            r"\b(should|recommend\w*|advise|advice to)\s+(buy|sell|short|long|invest)\b"
            r"|\bprice target\b|\bguaranteed returns?\b|\bbuy the dip\b"
            r"|\b(go|going)\s+long\b|\bshort the\b"
            r"|\bwill\s+(rise|climb|surge|jump|fall|drop|crash|plunge)\s+to\s+\$?\d",
            re.IGNORECASE,
        ),
    ),
    (
        # A safety/forecast POSITION (a prediction of harm) — not the observed event.
        "safety-position",
        re.compile(
            r"\bimminent\s+(danger|disaster|collapse|catastrophe)\b"
            r"|\b(earthquake|quake|tsunami|eruption)\s+will\s+(strike|hit|kill)\b"
            r"|\bwill\s+cause\s+\w+\s+(deaths|casualties|fatalities)\b"
            r"|\bdeath toll will\b|\byou should evacuate\b",
            re.IGNORECASE,
        ),
    ),
    (
        # Political propaganda / partisan POSITION-taking about a topic.
        "political-propaganda",
        re.compile(
            r"\b(corrupt|illegitimate|criminal|brutal)\s+(regime|government|administration)\b"
            r"|\bshould be\s+(sanctioned|overthrown|removed from power)\b"
            r"|\bis to blame for\b|\b(puppet|propaganda)\s+(regime|state)\b"
            r"|\bwar crimes?\b|\b(aggressor|oppressor)\b",
            re.IGNORECASE,
        ),
    ),
    (
        # Advocacy / opinion framing — telling the reader what ought to happen or how to
        # feel, rather than what the data shows.
        "opinion-advocacy",
        re.compile(
            r"\b(the (world|international community|we))\s+must\b"
            r"|\b(we|the world)\s+(should|need to)\s+(act|stop|condemn|intervene)\b"
            r"|\b(outrageous|unacceptable|shameful|heroic|courageous)\b"
            r"|\b(condemn|denounce)s?\b|\bin my (view|opinion)\b|\bit is clear that\b",
            re.IGNORECASE,
        ),
    ),
)


def _unquote(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def split_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Return (frontmatter dict | None, body-without-frontmatter).

    A leading flat ``---`` block of ``key: value`` lines, matching what the rest of the
    vault emits. None if absent/malformed; body is then the whole text.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    fm: dict[str, str] = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return fm, "\n".join(lines[i + 1 :])
        if ":" not in lines[i]:
            continue
        key, _, value = lines[i].partition(":")
        fm[key.strip()] = _unquote(value)
    return None, text  # no closing fence


def find_wikilinks(text: str) -> list[str]:
    """All ``[[target]]`` link targets, ``|alias`` and ``#anchor`` stripped."""
    out: list[str] = []
    for raw in _WIKILINK_RE.findall(text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            out.append(target)
    return out


def _claim_units(body: str) -> list[str]:
    """Claim-bearing prose units in the brief body.

    A claim unit is a contiguous prose paragraph OR a single list item. Headings,
    blockquote captions, table rows, blank lines, and the entire ``## Changelog``
    section are NOT claims and are skipped — the changelog is dated meta, captions
    cite the source inline, tables are verbatim data.
    """
    units: list[str] = []
    buf: list[str] = []
    in_changelog = False

    def flush() -> None:
        if buf:
            units.append(" ".join(buf))
            buf.clear()

    for raw in body.splitlines():
        s = raw.strip()
        if s.startswith("#"):
            flush()
            in_changelog = s.lstrip("#").strip().lower().startswith("changelog")
            continue
        if in_changelog:
            continue
        if not s or s.startswith(">") or s.startswith("|"):
            flush()
            continue
        if s.startswith(("- ", "* ", "+ ")) or re.match(r"^\d+\.\s", s):
            # A new list item starts a fresh claim unit; the next line(s) that are not
            # themselves a bullet are this item's soft-wrapped continuation (where the
            # [[link]] often lands), so they append to the SAME unit, not a new one.
            flush()
            buf.append(s)
            continue
        buf.append(s)  # prose line, or a bullet's wrapped continuation
    flush()
    return units


def check_claim_sourcing(body: str) -> list[str]:
    violations: list[str] = []
    for unit in _claim_units(body):
        if not _WIKILINK_RE.search(unit):
            snippet = unit if len(unit) <= 80 else unit[:77] + "..."
            violations.append(f"unsourced claim (no [[L1 link]]): {snippet!r}")
    return violations


def check_l1_links_exist(text: str, sources_root: Path | None) -> list[str]:
    """Every wikilink target must resolve to an L1 note file under 01 Sources/.

    Skipped (returns []) when ``sources_root`` is None — the pure claim-sourcing check
    still runs; this one needs the vault on disk and is wired by the CLI.
    """
    if sources_root is None:
        return []
    if not sources_root.exists():
        return [f"01 Sources root not found: {sources_root}"]
    known: set[str] = {p.stem for p in sources_root.rglob("*.md")}
    violations: list[str] = []
    for target in find_wikilinks(text):
        stem = Path(target).stem
        if stem not in known:
            violations.append(f"wikilink target has no L1 note in 01 Sources/: [[{target}]]")
    return violations


def check_frontmatter_schema(fm: dict[str, str] | None) -> list[str]:
    if fm is None:
        return ["brief has no parseable '---' frontmatter block"]
    violations: list[str] = []
    for key in REQUIRED_KEYS:
        if not fm.get(key, "").strip():
            violations.append(f"frontmatter missing/empty required key: {key}")
    if fm.get("type", "").strip() and fm["type"].strip() != LOCKED_TYPE:
        violations.append(f"frontmatter type must be '{LOCKED_TYPE}', got '{fm['type'].strip()}'")
    if fm.get("license", "").strip() and fm["license"].strip() != LOCKED_LICENSE:
        violations.append(
            f"frontmatter license must be '{LOCKED_LICENSE}' (IQ #371 A), got '{fm['license'].strip()}'"
        )
    if fm.get("week", "").strip() and not _WEEK_RE.match(fm["week"].strip()):
        violations.append(f"frontmatter week must be YYYY-Www, got '{fm['week'].strip()}'")
    if fm.get("updated", "").strip() and not _UPDATED_RE.match(fm["updated"].strip()):
        violations.append(
            f"frontmatter updated must be UTC ISO-8601 ...Z, got '{fm['updated'].strip()}'"
        )
    return violations


def check_evolve_not_duplicate(body: str) -> list[str]:
    """The brief must carry a ``## Changelog`` with >=1 dated line.

    L2 evolves the prior week's note in place (depth, changelog appended); it never
    forks a shallow new note. A present, dated changelog is the machine-checkable
    signal of edit-in-place evolution.
    """
    lines = body.splitlines()
    idx = next(
        (
            i
            for i, ln in enumerate(lines)
            if ln.strip().lstrip("#").strip().lower().startswith("changelog")
        ),
        None,
    )
    if idx is None:
        return ["brief has no '## Changelog' section (L2 must evolve-in-place, not duplicate)"]
    has_dated = any(_CHANGELOG_LINE_RE.search(ln) for ln in lines[idx + 1 :])
    if not has_dated:
        return ["'## Changelog' has no dated (YYYY-MM-DD) entry"]
    return []


def check_editorial_denylist(text: str) -> list[str]:
    violations: list[str] = []
    for label, pattern in _EDITORIAL_PATTERNS:
        m = pattern.search(text)
        if m:
            violations.append(f"editorial deny-list hit ({label}): {m.group(0)!r}")
    return violations


def check_diff_guard(changed_paths: list[str] | None) -> list[str]:
    """A synthesis commit may touch ``vault/02 Briefs/`` only.

    Any ``vault/01 Sources/`` change (the curator editing L1) or any path outside
    ``vault/02 Briefs/`` fails. Skipped (returns []) when ``changed_paths`` is None.
    """
    if changed_paths is None:
        return []
    violations: list[str] = []
    for raw in changed_paths:
        norm = raw.replace("\\", "/").strip()
        if not norm:
            continue
        if "vault/01 Sources/" in norm:
            violations.append(f"synthesis commit edits an L1 source note (forbidden): {norm}")
        elif "vault/02 Briefs/" not in norm:
            violations.append(
                f"synthesis commit touches a path outside 'vault/02 Briefs/': {norm}"
            )
    return violations


def lint_brief(
    text: str,
    *,
    changed_paths: list[str] | None = None,
    sources_root: Path | None = None,
) -> list[str]:
    """Run every blocking synthesis check. Empty list == clean."""
    fm, body = split_frontmatter(text)
    violations: list[str] = []
    violations += check_frontmatter_schema(fm)
    violations += check_claim_sourcing(body)
    violations += check_l1_links_exist(text, sources_root)
    violations += check_evolve_not_duplicate(body)
    violations += check_editorial_denylist(text)
    violations += check_diff_guard(changed_paths)
    return violations
