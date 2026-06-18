#!/usr/bin/env python3
"""Report which L2 briefs are stale vs the latest L1 ingest — the weekly-cadence gate.

The daily L1 ingest (``.github/workflows/ingest.yml``) keeps pulling fresh dated source
notes under ``vault/01 Sources/YYYY-MM-DD/``. The L2 briefs, by contrast, are LLM-authored
narrative the ``azimuth-curator`` fleet role evolves in place once a week — they cannot be
regenerated deterministically. This tool is the deterministic *trigger* and *verifier* for
that weekly cycle: for every editorially-clean theme whose brief is NOT held, it compares the
newest L1 ingest day carrying that theme's sources against the brief's ``updated`` date and
reports STALE / fresh.

Used three ways:
  * the weekly fleet azimuth-curator dispatch runs it to learn *which* briefs need refreshing
    (and cleanly no-ops the cycle when nothing is stale);
  * ``--check`` gives a non-zero exit when any clean brief lags the latest L1 — a machine
    answer to "did the weekly synthesis actually run after the last ingest";
  * a human can run it to see coverage at a glance.

Held themes (``themes.<slug>.brief_held``) are intentionally excluded — their L2 brief is
withheld for a logged editorial reason, so a newer L1 day must NOT count as "stale".

Pure stdlib + reuse of ``synthesis.lint.split_frontmatter`` (the same parser the lint and the
index use, so the three can never disagree).

Usage:
    python scripts/check_synthesis_freshness.py            # print the freshness table
    python scripts/check_synthesis_freshness.py --check    # exit 1 if any clean brief is stale
    python scripts/check_synthesis_freshness.py --json      # machine-readable report
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import split_frontmatter  # noqa: E402

_SOURCES_DIR = _REPO_ROOT / "vault" / "01 Sources"
_BRIEFS_DIR = _REPO_ROOT / "vault" / "02 Briefs"
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"

# A day directory under vault/01 Sources/ is exactly YYYY-MM-DD.
_DAY_LEN = len("YYYY-MM-DD")


def _is_day_dir(name: str) -> bool:
    return (
        len(name) == _DAY_LEN
        and name[4] == "-"
        and name[7] == "-"
        and name.replace("-", "").isdigit()
    )


def _theme_sources(data: dict[str, Any]) -> dict[str, list[str]]:
    """Map each theme slug -> the source keys it surfaces (surfaced + guardrail-clean only)."""
    out: dict[str, list[str]] = {}
    for src in data.get("sources", []):
        if not src.get("surfaced"):
            continue
        theme = src.get("theme")
        key = src.get("key")
        if theme and key:
            out.setdefault(theme, []).append(key)
    return out


def _latest_l1_day_for(source_keys: list[str]) -> str | None:
    """Newest YYYY-MM-DD ingest day that contains an L1 note for any of these source keys."""
    if not _SOURCES_DIR.is_dir():
        return None
    best: str | None = None
    for day_dir in _SOURCES_DIR.iterdir():
        if not day_dir.is_dir() or not _is_day_dir(day_dir.name):
            continue
        if any((day_dir / f"{key}.md").exists() for key in source_keys) and (
            best is None or day_dir.name > best
        ):
            best = day_dir.name
    return best


def _brief_updated_day(theme_slug: str, brief_file: str) -> str | None:
    """The ``updated`` date (YYYY-MM-DD prefix) of a theme's brief, or None if absent."""
    path = _BRIEFS_DIR / brief_file
    if not path.exists():
        return None
    fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    if not fm:
        return None
    updated = fm.get("updated", "")
    return updated[:_DAY_LEN] if len(updated) >= _DAY_LEN else None


def assess() -> list[dict[str, object]]:
    """One row per editorially-clean, non-held theme: its L1-vs-brief freshness verdict."""
    data = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    themes: dict[str, Any] = data.get("themes", {})
    theme_sources = _theme_sources(data)

    rows: list[dict[str, object]] = []
    for slug, meta in sorted(themes.items()):
        if meta.get("brief_held"):
            continue  # held by editorial decision — a newer L1 day is not "stale"
        keys = theme_sources.get(slug, [])
        latest_l1 = _latest_l1_day_for(keys)
        brief_file = meta.get("brief", f"{meta.get('title', slug)}.md")
        brief_day = _brief_updated_day(slug, brief_file)
        brief_exists = (_BRIEFS_DIR / brief_file).exists()
        # Stale when an L1 day exists that the brief has not yet absorbed (or no brief at all
        # while L1 data is present).
        stale = latest_l1 is not None and (
            not brief_exists or brief_day is None or latest_l1 > brief_day
        )
        rows.append(
            {
                "theme": slug,
                "brief": brief_file,
                "sources": keys,
                "latest_l1": latest_l1 or "-",
                "brief_updated": brief_day or ("(missing)" if not brief_exists else "-"),
                "stale": stale,
            }
        )
    return rows


def _render_table(rows: list[dict[str, object]]) -> str:
    lines = [
        "azimuth synthesis freshness — clean themes (held briefs excluded)",
        "",
        f"{'theme':<20} {'latest L1':<12} {'brief updated':<14} {'verdict'}",
        f"{'-' * 20} {'-' * 12} {'-' * 14} {'-' * 7}",
    ]
    for r in rows:
        verdict = "STALE" if r["stale"] else "fresh"
        lines.append(
            f"{r['theme']!s:<20} {r['latest_l1']!s:<12} {r['brief_updated']!s:<14} {verdict}"
        )
    stale_n = sum(1 for r in rows if r["stale"])
    lines += ["", f"{stale_n} of {len(rows)} clean brief(s) stale."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="azimuth L2 synthesis freshness gate")
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if any clean brief lags the latest L1"
    )
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = parser.parse_args()

    rows = assess()
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print(_render_table(rows))

    if args.check:
        return 1 if any(r["stale"] for r in rows) else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
