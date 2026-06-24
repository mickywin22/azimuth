#!/usr/bin/env python3
"""Backfill OKF reference-impl keys (`resource` + `tags`) onto existing vault notes (G6).

The OKF *spec* mandates only `type`; the Google reference *agent* (GA4 / Stack Overflow /
Bitcoin example bundles) also carries `resource` + `tags` on every concept. azimuth targets
that richer "reads like Google's own bundle" bar — see docs/strategy/okf-and-knowledge-graph.md.

This one-shot, idempotent migration walks every markdown note with a `---` frontmatter block
under ``vault/`` and adds the two keys when missing, inferred from the note's layer:

  * ``resource``: true for L1 source notes (they wrap a live external data endpoint, so the
    note *is* the resource), false for L2 briefs and L3 rules (synthesis / doctrine).
  * ``tags``: an inline YAML list (matching the existing ``sources: [...]`` style). Inferred
    from ``source_key`` / ``theme`` / layer where obvious, else an empty list ``[]``.

Notes that already carry both keys are left untouched (idempotent). New L1 notes get the keys
from ``ingest/pull.py`` directly; new L2 briefs are enforced by ``synthesis/lint.py``.

Pure stdlib. Run from the repo root:  ``python scripts/backfill_okf_frontmatter.py``
Add ``--check`` to fail (exit 1) if any note is still missing a key — wire-able into CI.
"""

from __future__ import annotations

import argparse
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VAULT = _REPO_ROOT / "vault"

# Coarse topical tag per L1 source key (kept in sync with ingest/pull.py _TAG_CATEGORY).
_TAG_CATEGORY: dict[str, str] = {
    "crude-oil-inventories": "energy",
    "natural-gas-storage-eu": "energy",
    "fuel-prices": "energy",
    "energy-prices": "energy",
    "earthquakes": "geophysical",
    "prediction-markets": "markets",
}
# Tags per L2 brief theme.
_THEME_TAGS: dict[str, list[str]] = {
    "energy-supply": ["energy", "supply"],
    "geophysical": ["geophysical", "hazards"],
}


def _parse_frontmatter(text: str) -> tuple[list[str], int] | None:
    """Return (frontmatter lines without fences, index of closing '---') or None."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], i
    return None


def _fm_get(fm_lines: list[str], key: str) -> str | None:
    for ln in fm_lines:
        k, sep, v = ln.partition(":")
        if sep and k.strip() == key:
            return v.strip().strip('"')
    return None


def _infer_resource(fm_lines: list[str]) -> str:
    return "true" if (_fm_get(fm_lines, "type") == "L1-source") else "false"


def _infer_tags(fm_lines: list[str], path: Path) -> str:
    note_type = _fm_get(fm_lines, "type")
    if note_type == "L1-source":
        key = _fm_get(fm_lines, "source_key") or path.stem
        tags = [key]
        category = _TAG_CATEGORY.get(key)
        if category and category != key:
            tags.append(category)
        return "[" + ", ".join(tags) + "]"
    if note_type == "L2-brief":
        theme = _fm_get(fm_lines, "theme") or ""
        return "[" + ", ".join(_THEME_TAGS.get(theme, [])) + "]"
    if note_type == "L3-rule":
        return "[okf, doctrine]" if path.name == "OKF.md" else "[doctrine]"
    return "[]"


def backfill_file(path: Path, *, write: bool) -> bool:
    """Add missing resource/tags to one note. Returns True if it needed a change."""
    text = path.read_text(encoding="utf-8")
    parsed = _parse_frontmatter(text)
    if parsed is None:
        return False  # no frontmatter (README/log) — nothing to enforce
    fm_lines, close_idx = parsed
    additions: list[str] = []
    if _fm_get(fm_lines, "resource") is None:
        additions.append(f"resource: {_infer_resource(fm_lines)}")
    if _fm_get(fm_lines, "tags") is None:
        additions.append(f"tags: {_infer_tags(fm_lines, path)}")
    if not additions:
        return False
    if write:
        lines = text.splitlines()
        lines[close_idx:close_idx] = additions  # insert just before closing '---'
        trailing = "\n" if text.endswith("\n") else ""
        path.write_text("\n".join(lines) + trailing, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill OKF resource/tags keys (G6)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit 1 if any note still misses a key",
    )
    args = parser.parse_args()

    notes = sorted(_VAULT.rglob("*.md"))
    changed = [p for p in notes if backfill_file(p, write=not args.check)]
    rel = [str(p.relative_to(_REPO_ROOT)) for p in changed]

    if args.check:
        if changed:
            print(f"backfill-okf: FAIL — {len(changed)} note(s) missing resource/tags:")
            for r in rel:
                print(f"  - {r}")
            return 1
        print("backfill-okf: all notes carry resource + tags (clean).")
        return 0

    if changed:
        print(f"backfill-okf: backfilled {len(changed)} note(s):")
        for r in rel:
            print(f"  + {r}")
    else:
        print("backfill-okf: nothing to do — every note already has resource + tags.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
