#!/usr/bin/env python3
"""CLI entry point for the azimuth daily L1 ingest.

Pulls every surfaced (and guardrail-passing) WorldMonitor subset and writes dated L1
markdown notes under ``vault/01 Sources/YYYY-MM-DD/``. The endpoint set and the
``license`` / ``attribution`` frontmatter come from ``sources/registry.json`` — the same
file the source-guardrail validates, so ingest and the guardrail share one source of truth.

Usage:
    python scripts/run_ingest.py              # live pull + write
    python scripts/run_ingest.py --dry-run    # fetch + render, write nothing
    python scripts/run_ingest.py --base-url http://localhost:8080   # against a stub

Exit codes: 0 = no errors (an all-skipped run is still 0); 1 = at least one source errored.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ingest import pull  # noqa: E402
from ingest.http import HttpFetcher  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="azimuth daily L1 ingest")
    parser.add_argument("--dry-run", action="store_true", help="fetch + render, write nothing")
    parser.add_argument("--base-url", default=None, help="override WorldMonitor base URL")
    parser.add_argument(
        "--out-dir",
        default=str(_REPO_ROOT / "vault" / "01 Sources"),
        help="L1 output root (default: vault/01 Sources)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    fetcher = HttpFetcher(args.base_url) if args.base_url else HttpFetcher()
    outcome = pull(
        registry_path=_REPO_ROOT / "sources" / "registry.json",
        credits_path=_REPO_ROOT / "CREDITS.md",
        fetcher=fetcher,
        out_dir=Path(args.out_dir),
        write=not args.dry_run,
    )

    print(
        f"ingest: {len(outcome.written)} written, "
        f"{len(outcome.skipped)} skipped, {len(outcome.errors)} errored"
    )
    for key, reason in sorted(outcome.errors.items()):
        print(f"  ERROR {key}: {reason}")
    for key, reason in sorted(outcome.skipped.items()):
        print(f"  skip  {key}: {reason}")
    return 0 if outcome.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
