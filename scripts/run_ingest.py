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

Exit codes: 0 = the run is healthy enough to commit — at least one note written and errors
a minority (<= 1/4) of the sources attempted, so a single flaky upstream never blackholes the
day's good notes (an all-skipped run is still 0). 1 = the run is unhealthy — nothing written,
or a broad outage past tolerance — so the daily workflow fails loudly and its alarm + liveness
gate fire.

Because a healthy-but-degraded run exits 0, the workflow's ``if: failure()`` alarm would
skip and the errored source(s) would vanish silently. To keep the ``ingest-alarm`` issue
firing for a tolerated failure too, this CLI publishes the errored source keys as GitHub
Actions step outputs (``errored`` / ``errored_count`` / ``written_count``) that ``ingest.yml``
keys its alarm off. Off CI (no ``GITHUB_OUTPUT``) that emission is a no-op.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ingest import IngestOutcome, pull  # noqa: E402
from ingest.http import CompositeFetcher, HttpFetcher, WorldBankFetcher  # noqa: E402


def _emit_step_outputs(outcome: IngestOutcome) -> None:
    """Publish the run's errored source keys as GitHub Actions step outputs.

    A *healthy* run that tolerated a minority of source errors exits 0, so the workflow's
    ``if: failure()`` alarm step is skipped and the dead source would be committed *around*
    silently. Emitting the errored keys here lets ``ingest.yml`` raise the ``ingest-alarm``
    issue on a committed-but-degraded run too (``steps.ingest.outputs.errored != ''``), while
    the good notes still commit. A clean run emits an empty ``errored`` so the alarm stays
    quiet. No-op when not running under GitHub Actions (``GITHUB_OUTPUT`` unset).

    ``GITHUB_OUTPUT`` is the runner-owned, append-only step-output file — append, never
    truncate, so a prior step's outputs survive.
    """
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    errored = ",".join(sorted(outcome.errors))
    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(f"errored={errored}\n")
        handle.write(f"errored_count={len(outcome.errors)}\n")
        handle.write(f"written_count={len(outcome.written)}\n")


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

    # WorldMonitor sources (``/api/...``) go through the session-minting HttpFetcher; direct
    # World Bank sources (``worldbank:<CODE>``) go through the keyless WorldBankFetcher. The
    # CompositeFetcher routes per endpoint, so ``--base-url`` still stubs only WorldMonitor.
    worldmonitor = HttpFetcher(args.base_url) if args.base_url else HttpFetcher()
    fetcher = CompositeFetcher(worldmonitor, WorldBankFetcher())
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
    if outcome.errors and outcome.healthy:
        print(
            f"ingest: {len(outcome.errors)} source(s) errored but the run is healthy "
            f"({len(outcome.written)} written) — committing the good notes; the failed "
            f"source(s) are surfaced above and the liveness gate still guards a dead engine."
        )
    # Publish errored keys as step outputs so ingest.yml alarms on a tolerated failure too
    # (exit 0 would otherwise skip its `if: failure()` alarm). No-op off CI.
    _emit_step_outputs(outcome)
    return 0 if outcome.healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
