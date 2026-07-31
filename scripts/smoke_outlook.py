#!/usr/bin/env python3
"""Deterministic end-to-end proof of the Outlook prediction layer — design §6 P5.

Runs the whole ``outlook`` pipeline over the committed L1 data and proves the four KR axes
the design locks (``docs/prediction-layer-design.md``) actually hold **on real data**:

    data (§2)  ->  forecast (§3)  ->  prediction interval (§4)  ->  success metric (§5)

1. **data** — extract the four Tier-A series out of the newest committed L1 day
   (``outlook.series.extract_latest``); all four must be present and sane.
2. **forecast + PI** — publish the next-period point forecast with its 80% interval for each
   series (``outlook.forecast.forecast_series``), the named method inline.
3. **success metric** — rolling-origin backtest -> per-series MASE / sMAPE / PI-coverage and
   the §5 **ship-bar** go/no-go (``outlook.backtest.score_all`` + ``ship_bar``).

The result is serialised to ``site/outlook-scorecard.json`` — a **regenerable, CI-guarded
public artifact** (the same contract as ``site/graph.json``: versioned, diff-visible, and
verifiable on a fresh checkout via ``--check``). The score is a public artifact, not an
internal check (design §5), so it ships *with* the forecast.

Nothing here publishes the public Outlook *brief* (design §6 P4) — that flexes on the D1
identity call and is deferred. This is pure, Michael-independent proof infrastructure: it
confirms the forecast/score engine is correct and reproducible before any editorial framing.

The layer is **gated behind KR1's daily-update guarantee**: the scorecard is always computed
from the *newest committed L1 day*, which the KR1 guarantee keeps fresh — a stale site can
never silently ship a stale forecast, because the artifact records the L1 day it was fit on.

Usage:
    python scripts/smoke_outlook.py            # run, print the report, write the scorecard
    python scripts/smoke_outlook.py --check    # exit 1 if the committed scorecard is stale
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

from outlook.backtest import ScoreCard, ShipBar, score_all, ship_bar  # noqa: E402
from outlook.forecast import Forecast, forecast_series  # noqa: E402
from outlook.series import (  # noqa: E402
    FORECASTABLE_KEYS,
    SPEC_BY_KEY,
    Series,
    extract_latest,
    latest_day,
)

_SOURCES = _REPO_ROOT / "vault" / "01 Sources"
_ARTIFACT = "outlook-scorecard.json"

# The design's primary horizon is one step for every Tier-A series (§3: CO2 +1mo, sea-ice
# +1mo, gas +1wk, crude +1wk) — the next-period point + interval is the published forecast.
_PRIMARY_HORIZON = 1


def _round(x: float, places: int = 4) -> float:
    """Round for byte-stable serialisation (same committed L1 -> identical artifact)."""
    return round(float(x), places)


def _forecast_block(fc: Forecast) -> dict[str, Any]:
    """The published forward forecast for one series: point + 80% PI + the named method."""
    return {
        "period": fc.periods[0],
        "point": _round(fc.point[0]),
        "lower": _round(fc.lower[0]),
        "upper": _round(fc.upper[0]),
        "pi_level": fc.pi_level,
        "method": fc.method,
        "members": list(fc.members),
    }


def _score_block(card: ScoreCard) -> dict[str, Any]:
    """The rolling-origin success metric for one series (design §5)."""
    return {
        "n_test": card.n_test,
        "mase": _round(card.mase),
        "smape": _round(card.smape, 2),
        "coverage": _round(card.coverage),
        "beats_naive": card.beats_naive,
        "coverage_ok": card.coverage_ok,
        "recommended": card.recommended,
    }


def _series_block(series: Series, fc: Forecast, card: ScoreCard) -> dict[str, Any]:
    return {
        "key": series.key,
        "label": series.label,
        "unit": series.unit,
        "cadence": series.cadence,
        "n_observations": len(series),
        "forecast": _forecast_block(fc),
        "score": _score_block(card),
    }


def build_scorecard(sources_dir: Path = _SOURCES) -> dict[str, Any]:
    """Run the full pipeline over the newest committed L1 day -> the deterministic scorecard.

    data -> forecast -> PI -> success metric, for every Tier-A series present. Sorted by key,
    floats rounded, so the same committed L1 always yields a byte-identical artifact.
    """
    day = latest_day(sources_dir)
    l1_day = day.name if day is not None else None
    series_map = extract_latest(sources_dir)
    cards = score_all(series_map)
    bar: ShipBar = ship_bar(cards)

    blocks = []
    for key in sorted(series_map):
        series = series_map[key]
        fc = forecast_series(series, _PRIMARY_HORIZON)
        blocks.append(_series_block(series, fc, cards[key]))

    return {
        "layer": "outlook",
        "design": "docs/prediction-layer-design.md",
        "gated_on": "KR1 daily-update guarantee (newest committed L1 day)",
        "l1_day": l1_day,
        "tier_a_expected": sorted(FORECASTABLE_KEYS),
        "series": blocks,
        "ship_bar": {
            "total": bar.total,
            "mase_pass": bar.mase_pass,
            "coverage_pass": bar.coverage_pass,
            "required": bar.required,
            "passed": bar.passed,
        },
    }


def _serialize(scorecard: dict[str, Any]) -> str:
    """Single source of truth for both the writer and the ``--check`` guard."""
    return json.dumps(scorecard, indent=2) + "\n"


def build(out_dir: Path, sources_dir: Path = _SOURCES) -> dict[str, Any]:
    """Build the scorecard and write ``outlook-scorecard.json`` into ``out_dir``."""
    scorecard = build_scorecard(sources_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / _ARTIFACT).write_text(_serialize(scorecard), encoding="utf-8")
    return scorecard


def check(out_dir: Path, sources_dir: Path = _SOURCES) -> bool:
    """True iff the committed scorecard is stale vs the live committed L1 (the CI guard)."""
    new_text = _serialize(build_scorecard(sources_dir))
    path = out_dir / _ARTIFACT
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    return current != new_text


def _print_report(scorecard: dict[str, Any]) -> None:
    print(f"Outlook scorecard — fit on committed L1 day {scorecard['l1_day']}\n")
    for s in scorecard["series"]:
        f, sc = s["forecast"], s["score"]
        flag = "ok" if sc["beats_naive"] and sc["coverage_ok"] else "  "
        print(
            f"  [{flag}] {s['key']:16s} n={s['n_observations']:2d}  "
            f"next {f['period']}: {f['point']:g} [{f['lower']:g}, {f['upper']:g}] {s['unit']} "
            f"via {f['method']}  |  MASE={sc['mase']:.3f} cov={sc['coverage']:.2f} "
            f"-> {sc['recommended']}"
        )
    b = scorecard["ship_bar"]
    print(
        f"\nSHIP-BAR (design §5): beats-naive {b['mase_pass']}/{b['total']}, "
        f"coverage-ok {b['coverage_pass']}/{b['total']} (need {b['required']} of each) -> "
        f"{'PASS' if b['passed'] else 'FAIL'}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic end-to-end proof of the Outlook prediction layer (design §6 P5)."
    )
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    parser.add_argument(
        "--check",
        action="store_true",
        help=f"exit 1 if committed site/{_ARTIFACT} is stale vs the live committed L1 (CI guard)",
    )
    args = parser.parse_args(argv)
    out_dir = (_REPO_ROOT / args.out).resolve()

    if args.check:
        if check(out_dir):
            print(
                "outlook scorecard: STALE — run `python scripts/smoke_outlook.py` and commit.",
                file=sys.stderr,
            )
            return 1
        print("outlook scorecard: up to date.")
        return 0

    scorecard = build(out_dir)

    # Fail loud if the pipeline itself is unhealthy: all four Tier-A series must forecast,
    # and the §5 ship-bar must pass. Either miss means the layer is not shippable.
    failures: list[str] = []
    present = {s["key"] for s in scorecard["series"]}
    missing = sorted(FORECASTABLE_KEYS - present)
    if missing:
        failures.append(f"Tier-A series failed to extract: {', '.join(missing)}")
    for key in sorted(present):
        if key not in SPEC_BY_KEY:  # defensive: only the allow-list may ever appear
            failures.append(f"non-Tier-A series leaked into the forecast path: {key}")
    if not scorecard["ship_bar"]["passed"]:
        failures.append("§5 ship-bar did NOT pass (see per-series MASE / coverage above)")

    _print_report(scorecard)
    print(f"\nscorecard written to {out_dir / _ARTIFACT}")

    if failures:
        print("\nSMOKE FAIL:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("\nSMOKE PASS — data -> forecast -> PI -> success metric proven on committed L1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
