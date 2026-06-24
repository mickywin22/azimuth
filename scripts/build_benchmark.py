#!/usr/bin/env python3
"""Generate the azimuth **benchmark** — facts vs forecast vs intelligence — from live data.

azimuth's sharpest USP proof (Michael 2026-06-24): take the same world-topic and show, side
by side, how azimuth treats it (observed facts from the live bundle, every claim linked to its
L1 source) vs a FORECAST product (a model probability) vs an INTELLIGENCE product (an analyst
assessment). The verdict/scorecard logic lives in ``synthesis/benchmark.py`` (unit-tested in
isolation); this CLI does the file/git I/O and renders the lint-green L2 brief
``vault/02 Briefs/Benchmark.md``.

azimuth's columns regenerate from the live L1 bundle each run; the forecast/intelligence
columns are read from the committed foil snapshot ``sources/benchmark/foils.json`` (refreshed
by ``scripts/pull_benchmark_foils.py`` on the weekly cadence). The HTML page
(``site/benchmark.html``) is rendered from the same engine by the site build.

Usage:
    python scripts/build_benchmark.py            # (re)write the Benchmark brief
    python scripts/build_benchmark.py --check     # exit 1 if the brief is stale vs the bundle
    python scripts/build_benchmark.py --json       # emit the benchmark as JSON
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.benchmark import Benchmark, build_benchmark, render_brief_markdown  # noqa: E402

_VAULT = _REPO_ROOT / "vault"
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"
_FOILS = _REPO_ROOT / "sources" / "benchmark" / "foils.json"
_BRIEF = _VAULT / "02 Briefs" / "Benchmark.md"
_CHANGELOG_DATED_RE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\b")


def _existing_changelog(text: str) -> list[str]:
    out: list[str] = []
    in_cl = False
    for ln in text.splitlines():
        if ln.strip().lstrip("#").strip().lower().startswith("changelog"):
            in_cl = True
            continue
        if in_cl and ln.strip().startswith("#"):
            break
        if in_cl and _CHANGELOG_DATED_RE.match(ln):
            out.append(ln.rstrip())
    return out


def _load() -> Benchmark:
    registry = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    foils = json.loads(_FOILS.read_text(encoding="utf-8")) if _FOILS.exists() else {}
    return build_benchmark(_VAULT, registry, foils)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="build the azimuth benchmark (facts vs forecast vs intel)"
    )
    parser.add_argument("--check", action="store_true", help="exit 1 if the brief is stale")
    parser.add_argument("--json", action="store_true", help="emit the benchmark as JSON")
    args = parser.parse_args()

    bench = _load()

    if args.json:
        print(
            json.dumps(
                {
                    "day": bench.day,
                    "week": bench.week,
                    "foil_captured_at": bench.foil_captured_at,
                    "source_notes": bench.source_notes,
                    "topics": [
                        {
                            "topic_id": t.topic_id,
                            "title": t.title,
                            "question": t.question,
                            "azimuth_channels": t.azimuth_channels,
                            "azimuth_claims": [
                                {"md": c.md, "sources": c.sources} for c in t.azimuth_claims
                            ],
                            "forecast_present": t.forecast.present,
                            "forecast_headline": t.forecast.headline,
                            "intelligence_present": t.intelligence.present,
                            "intelligence_headline": t.intelligence.headline,
                            "scorecard": [
                                {
                                    "dimension": r.dimension,
                                    "azimuth": r.azimuth,
                                    "forecast": r.forecast,
                                    "intelligence": r.intelligence,
                                    "azimuth_wins": r.azimuth_wins,
                                }
                                for r in t.scorecard
                            ],
                            "verdict": t.verdict.md,
                        }
                        for t in bench.topics
                    ],
                },
                indent=2,
            )
        )
        return 0

    prior = _existing_changelog(_BRIEF.read_text(encoding="utf-8")) if _BRIEF.exists() else []
    new = render_brief_markdown(bench, prior)

    if args.check:
        current = _BRIEF.read_text(encoding="utf-8") if _BRIEF.exists() else ""
        if current != new:
            print("benchmark: STALE — run `python scripts/build_benchmark.py` and commit.")
            return 1
        print("benchmark: up to date.")
        return 0

    _BRIEF.write_text(new, encoding="utf-8")
    n_foil = sum(1 for t in bench.topics if t.forecast.present)
    print(
        f"benchmark: wrote {_BRIEF.relative_to(_REPO_ROOT)} "
        f"({len(bench.topics)} topics, {n_foil} with a live foil, bundle day {bench.day})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
