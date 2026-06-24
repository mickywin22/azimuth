#!/usr/bin/env python3
"""Generate the azimuth **demonstrator** — the TOP5 multi-channel answers — from live data.

This is the centerpiece of azimuth's USP: it *answers* five fixed cross-source questions
from the live L1 bundle, every claim linked to its L1 source note, regenerated on the weekly
cadence so the answers stay current (the *living* answer a static format can't match). The
verdict/scan logic lives in ``synthesis/answers.py`` (unit-tested in isolation); this CLI does
the file/git I/O and renders the lint-green L2 brief ``vault/02 Briefs/Top5 Answers.md``.

Re-runnable: run it again after a fresh L1 ingest and it regenerates the brief from current
data, preserving the dated ``## Changelog`` history (evolve-in-place, never fork). The HTML
demonstrator page (``site/answers.html``) is rendered from the same engine by the site build.

Usage:
    python scripts/build_answers.py            # (re)write the Top5 Answers brief
    python scripts/build_answers.py --check     # exit 1 if the brief is stale vs the bundle
    python scripts/build_answers.py --json       # emit the answer set as JSON
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

from synthesis.answers import AnswerSet, build_answer_set, render_brief_markdown  # noqa: E402

_VAULT = _REPO_ROOT / "vault"
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"
_BRIEF = _VAULT / "02 Briefs" / "Top5 Answers.md"
_CHANGELOG_DATED_RE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2})\b")


def _existing_changelog(text: str) -> list[str]:
    """Pull prior ``## Changelog`` dated lines so regeneration evolves, not forks."""
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


def _load() -> AnswerSet:
    registry = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    return build_answer_set(_VAULT, registry)


def main() -> int:
    parser = argparse.ArgumentParser(description="build the azimuth TOP5 demonstrator answers")
    parser.add_argument("--check", action="store_true", help="exit 1 if the brief is stale")
    parser.add_argument("--json", action="store_true", help="emit the answer set as JSON")
    args = parser.parse_args()

    aset = _load()

    if args.json:
        print(
            json.dumps(
                {
                    "day": aset.day,
                    "week": aset.week,
                    "source_notes": aset.source_notes,
                    "answers": [
                        {
                            "qid": a.qid,
                            "question": a.question,
                            "persona": a.persona,
                            "channels": a.channels,
                            "claims": [{"md": c.md, "sources": c.sources} for c in a.claims],
                        }
                        for a in aset.answers
                    ],
                },
                indent=2,
            )
        )
        return 0

    prior = _existing_changelog(_BRIEF.read_text(encoding="utf-8")) if _BRIEF.exists() else []
    new = render_brief_markdown(aset, prior)

    if args.check:
        current = _BRIEF.read_text(encoding="utf-8") if _BRIEF.exists() else ""
        if current != new:
            print("answers: STALE — run `python scripts/build_answers.py` and commit.")
            return 1
        print("answers: up to date.")
        return 0

    _BRIEF.write_text(new, encoding="utf-8")
    n_claims = sum(len(a.claims) for a in aset.answers)
    print(
        f"answers: wrote {_BRIEF.relative_to(_REPO_ROOT)} "
        f"({len(aset.answers)} answers, {n_claims} sourced claims, bundle day {aset.day})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
