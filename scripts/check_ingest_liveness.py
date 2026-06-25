#!/usr/bin/env python3
"""Report whether the daily L1 ingest is still alive — the ingest-cadence heartbeat.

The daily L1 ingest (``.github/workflows/ingest.yml``) is the engine the whole demonstrator
rests on: pull every surfaced WorldMonitor subset, write dated notes under
``vault/01 Sources/YYYY-MM-DD/``, commit. But the workflow only *commits* when the bytes
change, and a cron that silently stops firing leaves **no trace at all** — so "no recent
commit" is ambiguous and a dead engine is invisible. This tool makes the engine's liveness
observable and machine-checkable: it finds the newest committed L1 day and measures its age
against today.

It is the liveness counterpart to ``check_synthesis_freshness.py``: that one asks "did the
weekly L2 synthesis run after the last ingest"; this one asks the upstream question "did the
daily L1 ingest run at all, recently". Together they cover the full L1-daily / L2-weekly
cadence the KR-C operate objective is responsible for.

``--max-age-days`` is the tolerance (default 2 — a daily cron plus one missed run of slack).
``--today`` pins the reference date so the check is deterministic in tests and CI; it
defaults to the system UTC date.

Pure stdlib. No network — it reads only what is already committed, so it is a safe CI gate.

Usage:
    python scripts/check_ingest_liveness.py            # print the liveness report
    python scripts/check_ingest_liveness.py --check    # exit 1 if the latest L1 day is stale
    python scripts/check_ingest_liveness.py --json      # machine-readable report
    python scripts/check_ingest_liveness.py --max-age-days 3 --today 2026-06-26
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES = _REPO_ROOT / "vault" / "01 Sources"
DEFAULT_MAX_AGE_DAYS = 2


def _parse_day(name: str) -> date | None:
    """Parse a ``YYYY-MM-DD`` directory name into a date, or ``None`` if it is not one."""
    try:
        return datetime.strptime(name, "%Y-%m-%d").date()
    except ValueError:
        return None


def l1_days(sources_dir: Path = DEFAULT_SOURCES) -> list[date]:
    """All dated L1 ingest days present under ``sources_dir``, oldest-first."""
    if not sources_dir.is_dir():
        return []
    days = [d for p in sources_dir.iterdir() if p.is_dir() and (d := _parse_day(p.name))]
    return sorted(days)


def latest_l1_day(sources_dir: Path = DEFAULT_SOURCES) -> date | None:
    """The newest committed L1 ingest day, or ``None`` when none exist."""
    days = l1_days(sources_dir)
    return days[-1] if days else None


def liveness(
    sources_dir: Path = DEFAULT_SOURCES,
    today: date | None = None,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
) -> dict[str, Any]:
    """Assess ingest liveness: latest L1 day, its age in days, and a healthy/stale verdict."""
    ref = today or datetime.now(UTC).date()
    latest = latest_l1_day(sources_dir)
    age = (ref - latest).days if latest else None
    # No days at all, or the newest is older than tolerance, is unhealthy.
    healthy = latest is not None and age is not None and age <= max_age_days
    return {
        "today": ref.isoformat(),
        "latest_l1_day": latest.isoformat() if latest else None,
        "age_days": age,
        "max_age_days": max_age_days,
        "day_count": len(l1_days(sources_dir)),
        "healthy": healthy,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report whether the daily L1 ingest is still alive (ingest heartbeat)."
    )
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if the latest L1 day is stale"
    )
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=DEFAULT_MAX_AGE_DAYS,
        help=f"staleness tolerance in days (default: {DEFAULT_MAX_AGE_DAYS})",
    )
    parser.add_argument("--today", help="reference date YYYY-MM-DD (default: system UTC date)")
    parser.add_argument(
        "--sources", default=str(DEFAULT_SOURCES), help="path to vault/01 Sources/"
    )
    args = parser.parse_args(argv)

    ref: date | None = None
    if args.today:
        parsed = _parse_day(args.today)
        if parsed is None:
            print(f"Invalid --today date: {args.today!r}", file=sys.stderr)
            return 2
        ref = parsed

    report = liveness(Path(args.sources), today=ref, max_age_days=args.max_age_days)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if report["latest_l1_day"] is None:
            print("ingest liveness: NO L1 days found — the ingest has never produced data.")
        else:
            verdict = "alive" if report["healthy"] else "STALE"
            print(
                f"ingest liveness: {verdict} — latest L1 day {report['latest_l1_day']} "
                f"({report['age_days']}d old, tolerance {report['max_age_days']}d, "
                f"{report['day_count']} day(s) on record, as of {report['today']})."
            )
            if not report["healthy"]:
                print(
                    "  The daily L1 ingest (.github/workflows/ingest.yml) has not landed a "
                    "fresh day within tolerance — check the workflow runs."
                )

    if args.check and not report["healthy"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
