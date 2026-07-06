#!/usr/bin/env python3
"""Build the azimuth autonomy counters (``site/autonomy.json`` + ``site/autonomy.html``).

The single most important thing azimuth demonstrates is not any one brief — it is that
the whole **L1 → L2 → L3** pipeline *runs itself*: a daily GitHub-Actions job pulls the
WorldMonitor subsets into dated L1 notes, a weekly fleet curator evolves the L2 briefs,
and CI enforces the doctrine — hands-off, for cents a week. This surfaces that claim as
hard, checkable counters instead of a marketing sentence.

**Every counter is derived purely from committed data** — the dated L1 day directories,
the L1 note files, the L2 briefs, and ``sources/registry.json`` — and **never from the
wall clock**. That is deliberate: it makes the output byte-reproducible, so
``build_autonomy.py --check`` on any checkout of a given commit yields the same numbers,
exactly like ``build_graph.py --check`` and ``build_brief_index.py --check``. The daily
ingest workflow regenerates this in the same run that commits a new L1 day, so the live
counters advance one day at a time while ``--check`` stays green on ``main``.

The one figure that cannot be read out of the repo — the LLM spend — is an explicit,
**labelled estimate** (weeks of operation x a documented ~$0.60/week order-of-magnitude
cost for the single small weekly synthesis job), never a fake-precise metered number.

Usage:
    python scripts/build_autonomy.py            # write site/autonomy.json + autonomy.html
    python scripts/build_autonomy.py --check     # exit 1 if either committed file is stale
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VAULT = _REPO_ROOT / "vault"
_SOURCES = _VAULT / "01 Sources"
_BRIEFS = _VAULT / "02 Briefs"
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"
_OUT_DIR = _REPO_ROOT / "site"

_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Order-of-magnitude estimate for the weekly synthesis cost. The weekly L2 curator is a
# single small LLM job over a handful of briefs; this is NOT metered spend, it is a
# labelled estimate so the "runs itself for cents" claim is quantified honestly. Michael
# can correct this one constant if real billing data ever lands.
_EST_WEEKLY_SPEND_USD = 0.60
_SPEND_BASIS = (
    "order-of-magnitude estimate — one small weekly LLM synthesis job; "
    "not metered billing data"
)


def _day_dirs() -> list[str]:
    """Dated ``YYYY-MM-DD`` L1 day directories, sorted ascending. Committed data only."""
    if not _SOURCES.is_dir():
        return []
    return sorted(p.name for p in _SOURCES.iterdir() if p.is_dir() and _DAY_RE.match(p.name))


def _l1_note_count() -> int:
    if not _SOURCES.is_dir():
        return 0
    return sum(1 for d in _day_dirs() for _ in (_SOURCES / d).glob("*.md"))


def _brief_count() -> int:
    if not _BRIEFS.is_dir():
        return 0
    return sum(1 for p in _BRIEFS.glob("*.md") if p.name.lower() != "readme.md")


def _surfaced_channels() -> int:
    if not _REGISTRY.is_file():
        return 0
    data = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    return sum(1 for s in data.get("sources", []) if s.get("surfaced"))


def _days_between(first: str, latest: str) -> int:
    """Inclusive span in days between two ``YYYY-MM-DD`` strings (wall-clock independent)."""
    a = _dt.date.fromisoformat(first)
    b = _dt.date.fromisoformat(latest)
    return (b - a).days + 1


def counters() -> dict[str, Any]:
    """Compute every autonomy counter from committed repo data. No wall-clock reads."""
    days = _day_dirs()
    first = days[0] if days else ""
    latest = days[-1] if days else ""
    span = _days_between(first, latest) if days else 0
    weeks = round(span / 7, 1) if span else 0.0
    est_spend = round(weeks * _EST_WEEKLY_SPEND_USD, 2)
    return {
        "generated_from": "committed vault data (wall-clock independent)",
        "first_l1_day": first,
        "latest_l1_day": latest,
        "days_operating": span,
        "weeks_operating": weeks,
        "l1_ingests_committed": len(days),
        "l1_source_notes": _l1_note_count(),
        "l2_briefs": _brief_count(),
        "channels_surfaced": _surfaced_channels(),
        "est_weekly_spend_usd": _EST_WEEKLY_SPEND_USD,
        "est_llm_spend_usd": est_spend,
        "spend_basis": _SPEND_BASIS,
    }


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


# --- HTML card grid ---------------------------------------------------------

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Autonomy · azimuth</title>
<style>
:root{{--bg:#0c1118;--panel:#141a23;--border:#2a3a4d;--text:#e7edf5;--muted:#8a97a8;
--accent:#4cc2ff;--accent2:#4a90d9}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);
font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding:2rem 1.1rem 3rem}}
a{{color:var(--accent2)}}
.kick{{text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;color:var(--accent);
font-weight:700;margin:0 0 .3rem}}
h1{{margin:.1rem 0 .5rem;font-size:1.9rem}}
.lede{{color:var(--muted);max-width:64ch;margin:.2rem 0 1.4rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.8rem}}
.card{{background:var(--panel);border:1px solid var(--border);border-radius:12px;
padding:1.1rem 1rem}}
.card .n{{font-size:2.05rem;font-weight:800;line-height:1.05;color:var(--text)}}
.card .n.est{{color:var(--accent)}}
.card .lab{{margin-top:.25rem;font-size:.82rem;color:var(--muted)}}
.foot{{margin-top:1.6rem;font-size:.82rem;color:var(--muted);max-width:70ch}}
.foot code{{background:var(--panel);border:1px solid var(--border);border-radius:5px;
padding:.05rem .35rem;font-size:.9em}}
.range{{margin:.1rem 0 1.2rem;font-size:.86rem;color:var(--muted)}}
.range b{{color:var(--text);font-weight:600}}
</style></head><body>
<div class="wrap">
<p class="kick">Proof it runs itself</p>
<h1>azimuth autonomy counters</h1>
<p class="lede">azimuth is not a snapshot — it is a knowledge system that operates on its
own. A daily GitHub-Actions job pulls the sources, a weekly fleet curator evolves the
briefs, and CI enforces the doctrine. Every number below is computed straight from the
committed vault, not typed in by hand.</p>
<p class="range">Operating <b>{first}</b> → <b>{latest}</b>.</p>
<div class="grid">
{cards}
</div>
<p class="foot">Counters regenerate automatically with each daily ingest
(<code>scripts/build_autonomy.py</code>) and are guarded in CI by
<code>build_autonomy.py --check</code>, so they can never drift from the data. Spend is an
{spend_basis} — the hard counters (days, ingests, notes, briefs, channels) are read
directly from the repository and are byte-reproducible. Machine-readable: <a
href="autonomy.json">autonomy.json</a>.</p>
</div></body></html>
"""


def _card(number: str, label: str, *, est: bool = False) -> str:
    cls = "n est" if est else "n"
    return (
        f'  <div class="card"><div class="{cls}">{html.escape(number)}</div>'
        f'<div class="lab">{html.escape(label)}</div></div>'
    )


def render_html(data: dict[str, Any]) -> str:
    cards = "\n".join(
        [
            _card(str(data["days_operating"]), "days operating autonomously"),
            _card(str(data["l1_ingests_committed"]), "daily L1 ingests committed"),
            _card(f"{data['l1_source_notes']:,}", "L1 source notes written"),
            _card(str(data["l2_briefs"]), "L2 briefs maintained"),
            _card(str(data["channels_surfaced"]), "data channels surfaced"),
            _card(f"~${data['est_llm_spend_usd']:.2f}", "estimated LLM spend, all-time", est=True),
        ]
    )
    return _HTML_TEMPLATE.format(
        first=html.escape(data["first_l1_day"] or "—"),
        latest=html.escape(data["latest_l1_day"] or "—"),
        cards=cards,
        spend_basis=html.escape(data["spend_basis"]),
    )


def _targets(out_dir: Path, data: dict[str, Any]) -> list[tuple[Path, str]]:
    return [
        (out_dir / "autonomy.json", render_json(data)),
        (out_dir / "autonomy.html", render_html(data)),
    ]


def build(out_dir: Path = _OUT_DIR) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    data = counters()
    for path, text in _targets(out_dir, data):
        path.write_text(text, encoding="utf-8")


def stale(out_dir: Path = _OUT_DIR) -> list[str]:
    """Names of committed autonomy files that disagree with a fresh build. Empty = in sync."""
    data = counters()
    out: list[str] = []
    for path, text in _targets(out_dir, data):
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != text:
            out.append(path.name)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="build the azimuth autonomy counters")
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if committed autonomy files are stale"
    )
    args = parser.parse_args(argv)

    if args.check:
        drift = stale()
        if drift:
            print(
                f"autonomy: STALE ({', '.join(drift)}) — run "
                "`python scripts/build_autonomy.py` and commit."
            )
            return 1
        print("autonomy: up to date.")
        return 0

    build()
    print(f"autonomy: wrote site/autonomy.json + site/autonomy.html ({counters()['days_operating']} days)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
