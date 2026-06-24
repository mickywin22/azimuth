#!/usr/bin/env python3
"""Generate the OKF reserved bundle log (``vault/log.md``) — newest-first history.

OKF v0.1 §7 reserves ``log.md`` as a knowledge bundle's chronological update history:
newest-first, with ISO ``YYYY-MM-DD`` headings. This generator builds it deterministically
from two sources of truth already inside the bundle — it invents nothing:

* **Ingest days** — every ``vault/01 Sources/<YYYY-MM-DD>/`` folder is one L1 ingest day;
  the source notes inside it are that day's pulled L1 concepts.
* **Brief changelogs** — every L2 brief's ``## Changelog`` carries dated ``- YYYY-MM-DD — …``
  lines recording what that synthesis cycle changed.

Held themes (``sources/registry.json`` ``brief_held: true``) are excluded — both their L1
source notes and their brief — so the bundle log can never leak a held theme onto the public
site, matching the site-build editorial guardrail.

Pure stdlib + reuse of ``synthesis.lint.split_frontmatter``, plus the same held-theme rule
the site-build applies (kept dependency-free here so this can run in the no-deps CI lint
job), so the log can never disagree with the lint or the rendered site. Idempotent:
re-running with no bundle change rewrites byte-identical
output (no generation timestamp is embedded — that is what keeps the CI ``--check`` honest).

Usage:
    python scripts/build_log.py            # write vault/log.md
    python scripts/build_log.py --check     # exit 1 if log.md is stale (CI guard)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import split_frontmatter  # noqa: E402

_VAULT = _REPO_ROOT / "vault"
_SOURCES_DIR = _VAULT / "01 Sources"
_BRIEFS_DIR = _VAULT / "02 Briefs"
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"
_LOG = _VAULT / "log.md"

_DATE_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A changelog entry: "- 2026-06-23 — text…" (em-dash or hyphen separator).
_CHANGELOG_RE = re.compile(r"^-\s+(\d{4}-\d{2}-\d{2})\s*[—-]\s*(.*)$")
_WS_RE = re.compile(r"\s+")


def _registry() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    return data


def _held_source_keys(reg: dict[str, Any]) -> set[str]:
    """Source keys mapping to a held theme — excluded from the public log + site."""
    held = {name for name, meta in reg.get("themes", {}).items() if meta.get("brief_held")}
    return {s["key"] for s in reg.get("sources", []) if s.get("theme") in held}


def _held_brief_files(reg: dict[str, Any]) -> set[str]:
    """Brief filenames whose theme is held — their changelog never enters the log."""
    return {
        meta["brief"]
        for meta in reg.get("themes", {}).values()
        if meta.get("brief_held") and meta.get("brief")
    }


def _ingest_days(skip_source_keys: set[str]) -> dict[str, list[str]]:
    """date -> sorted source keys ingested that day (held source keys excluded)."""
    days: dict[str, list[str]] = {}
    if not _SOURCES_DIR.is_dir():
        return days
    for day_dir in sorted(_SOURCES_DIR.iterdir()):
        if not day_dir.is_dir() or not _DATE_DIR_RE.match(day_dir.name):
            continue
        keys = sorted(
            p.stem
            for p in day_dir.glob("*.md")
            if p.name.lower() != "readme.md" and p.stem not in skip_source_keys
        )
        if keys:
            days[day_dir.name] = keys
    return days


def _changelog_entries(text: str) -> list[tuple[str, str]]:
    """Parse a brief body's ``## Changelog`` into (date, collapsed-text) entries."""
    entries: list[tuple[str, str]] = []
    in_section = False
    cur_date: str | None = None
    cur_text = ""
    for line in text.splitlines():
        if line.strip() == "## Changelog":
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("## "):  # next section ends the changelog
            break
        m = _CHANGELOG_RE.match(line)
        if m:
            if cur_date is not None:
                entries.append((cur_date, _WS_RE.sub(" ", cur_text).strip()))
            cur_date, cur_text = m.group(1), m.group(2)
        elif cur_date is not None and line.strip():
            cur_text += " " + line.strip()
    if cur_date is not None:
        entries.append((cur_date, _WS_RE.sub(" ", cur_text).strip()))
    return entries


def _brief_updates(skip_brief_files: set[str]) -> dict[str, list[tuple[str, str]]]:
    """date -> sorted [(brief title, changelog text)] (held briefs excluded)."""
    by_date: dict[str, list[tuple[str, str]]] = {}
    if not _BRIEFS_DIR.is_dir():
        return by_date
    for path in sorted(_BRIEFS_DIR.glob("*.md")):
        if path.name.lower() == "readme.md" or path.name in skip_brief_files:
            continue
        fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
        title = (fm or {}).get("title", path.stem)
        for date, body_text in _changelog_entries(body):
            by_date.setdefault(date, []).append((title, body_text))
    for date in by_date:
        by_date[date].sort()
    return by_date


def render() -> str:
    reg = _registry()
    ingest = _ingest_days(_held_source_keys(reg))
    updates = _brief_updates(_held_brief_files(reg))

    lines = [
        "# azimuth — Bundle Log",
        "",
        "Auto-generated by `scripts/build_log.py` from the bundle's ingest days and L2 brief",
        "changelogs — do not edit by hand. This is the OKF v0.1 §7 reserved `log.md`: the",
        "bundle's chronological update history, newest-first, with ISO `YYYY-MM-DD` headings.",
        "Held themes (see the editorial line) are excluded. Content is CC-BY-4.0; see",
        "`CREDITS.md` for upstream sources.",
        "",
    ]

    for date in sorted(set(ingest) | set(updates), reverse=True):
        lines.append(f"## {date}")
        lines.append("")
        keys = ingest.get(date)
        if keys:
            noun = "note" if len(keys) == 1 else "notes"
            lines.append(f"- **Ingest** — {len(keys)} L1 source {noun}: {', '.join(keys)}.")
        for title, body_text in updates.get(date, []):
            lines.append(f"- **{title}** — {body_text}")
        lines.append("")

    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="build the azimuth OKF bundle log (log.md)")
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if log.md is stale (CI guard)"
    )
    args = parser.parse_args()

    new = render()
    if args.check:
        current = _LOG.read_text(encoding="utf-8") if _LOG.exists() else ""
        if current != new:
            print("bundle-log: STALE — run `python scripts/build_log.py` and commit.")
            return 1
        print("bundle-log: up to date.")
        return 0

    _LOG.write_text(new, encoding="utf-8")
    print(f"bundle-log: wrote {_LOG.relative_to(_REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
