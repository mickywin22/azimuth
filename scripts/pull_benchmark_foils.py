#!/usr/bin/env python3
"""Capture the benchmark **foil corpus** — the compared forecast / intelligence product.

The benchmark (``synthesis/benchmark.py``) proves azimuth's USP by contrast: observed +
sourced facts vs a forecast / intelligence product's *prediction / assessment* of the same
topic. azimuth's own columns are generated live from the open-data bundle; the *foil*
columns quote WorldMonitor's forecast feed as the **compared product** (NOT an azimuth
channel — forecasts are predictions, not observed facts).

This script is the foil's "ingest": it mints an anonymous WorldMonitor session, pulls the
public forecast feed (``/api/forecast/v1/get-forecasts``), selects the best-matching forecast
per benchmark topic (by stable domain/keyword match, resilient to per-cycle id churn), trims
each to the denylist-safe quote fields, and writes a dated snapshot to
``sources/benchmark/foils.json``. Run on the weekly cadence alongside the TOP5 demonstrator so
the benchmark stays current; the benchmark generator reads the committed snapshot, so the
four-gate (build/lint/test) stays green offline.

A topic with no matching forecast is written with ``"foil": null`` + an honest absence reason
— itself a valid benchmark outcome (e.g. nobody publishes a credible earthquake forecast).

Usage:
    python scripts/pull_benchmark_foils.py                 # live pull -> write foils.json
    python scripts/pull_benchmark_foils.py --from raw.json  # offline: select from a saved feed
    python scripts/pull_benchmark_foils.py --check          # exit 1 if foils.json missing/empty
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.benchmark import FOIL_SPECS, select_foil, trim_foil  # noqa: E402

_OUT = _REPO_ROOT / "sources" / "benchmark" / "foils.json"
_FORECAST_ENDPOINT = "/api/forecast/v1/get-forecasts"
_ATTRIBUTION = "WorldMonitor (api.worldmonitor.app) — model-generated forecast/assessment product"


def _live_feed() -> dict[str, Any]:
    """Mint a WorldMonitor session and pull the forecast feed (live network)."""
    from ingest.http import HttpFetcher  # local import keeps the tested core offline

    fetcher = HttpFetcher()
    payload = fetcher.fetch(_FORECAST_ENDPOINT)
    if not isinstance(payload, dict):
        raise RuntimeError("forecast feed did not return a JSON object")
    return payload


def _build_corpus(feed: dict[str, Any], now: datetime) -> dict[str, Any]:
    forecasts = [f for f in (feed.get("forecasts") or []) if isinstance(f, dict)]
    captured = now.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    topics: dict[str, Any] = {}
    for spec in FOIL_SPECS:
        match = select_foil(spec, forecasts)
        topics[spec.topic_id] = {
            "foil": (trim_foil(match) if match else None),
            "absence_reason": (None if match else spec.absence_reason),
        }
    return {
        "$note": (
            "Captured snapshot of the COMPARED forecast/intelligence product for the azimuth "
            "benchmark (synthesis/benchmark.py). Quoted by product + capture date; NOT surfaced "
            "as an azimuth channel and NOT an L1 source. Refresh with pull_benchmark_foils.py."
        ),
        "endpoint": _FORECAST_ENDPOINT,
        "attribution": _ATTRIBUTION,
        "feed_generated_at": feed.get("generatedAt"),
        "feed_degraded": feed.get("degraded"),
        "captured_at": captured,
        "n_forecasts_seen": len(forecasts),
        "topics": topics,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="capture the azimuth benchmark foil corpus")
    parser.add_argument("--from", dest="from_file", help="offline: select from a saved feed JSON")
    parser.add_argument(
        "--out", default=str(_OUT), help="output path (default: sources/benchmark/foils.json)"
    )
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if the corpus is missing/empty"
    )
    args = parser.parse_args(argv)
    out = Path(args.out)

    if args.check:
        if not out.exists():
            print(f"benchmark-foils: MISSING — {out} does not exist.")
            return 1
        data = json.loads(out.read_text(encoding="utf-8"))
        n = len(data.get("topics", {}))
        if n == 0:
            print("benchmark-foils: EMPTY — no topics captured.")
            return 1
        n_foil = sum(1 for t in data["topics"].values() if t.get("foil"))
        print(
            f"benchmark-foils: ok — {n} topics, {n_foil} with a live foil, captured {data.get('captured_at')}."
        )
        return 0

    if args.from_file:
        feed = json.loads(Path(args.from_file).read_text(encoding="utf-8"))
    else:
        try:
            feed = _live_feed()
        except Exception as exc:  # network/HTTP/decode — never crash the cadence
            print(
                f"benchmark-foils: WARN — live pull failed ({exc}); leaving existing corpus untouched."
            )
            return 1

    corpus = _build_corpus(feed, datetime.now(UTC))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_foil = sum(1 for t in corpus["topics"].values() if t.get("foil"))
    print(
        f"benchmark-foils: wrote {out.relative_to(_REPO_ROOT) if out.is_relative_to(_REPO_ROOT) else out} "
        f"({len(corpus['topics'])} topics, {n_foil} with a live foil, {corpus['n_forecasts_seen']} forecasts seen)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
