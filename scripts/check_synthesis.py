#!/usr/bin/env python3
"""CI + pre-commit entry point for the azimuth synthesis lint (spec.md F2).

Lints every L2 brief under ``vault/02 Briefs/`` against the blocking synthesis contract
(claim-sourcing, L1-link existence, frontmatter schema, evolve-not-duplicate, editorial
deny-list) and — when given a git ref — enforces the diff guard (a synthesis commit may
touch ``vault/02 Briefs/`` only; editing an L1 note fails the build).

Pure verdict logic lives in ``synthesis/lint.py``; this script only does file/git I/O.
Exit 0 when every brief is clean, 1 otherwise (printing one line per violation).

Usage:
    python scripts/check_synthesis.py                      # lint all briefs
    python scripts/check_synthesis.py --diff-base origin/main   # + diff guard vs a ref
    python scripts/check_synthesis.py --brief "vault/02 Briefs/Energy Supply Weekly.md"
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import lint_brief  # noqa: E402


def _changed_paths(diff_base: str) -> list[str] | None:
    """Paths changed vs ``diff_base`` (committed + working tree). None if git fails."""
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", diff_base],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"synthesis-lint: WARN — could not compute diff vs {diff_base}: {exc}")
        return None
    return [line for line in out.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="azimuth L2 synthesis lint (spec.md F2)")
    parser.add_argument("--briefs-root", default="vault/02 Briefs")
    parser.add_argument("--sources-root", default="vault/01 Sources")
    parser.add_argument("--brief", action="append", help="lint only this brief (repeatable)")
    parser.add_argument("--diff-base", help="git ref to enforce the diff guard against")
    args = parser.parse_args()

    briefs_root = (_REPO_ROOT / args.briefs_root).resolve()
    sources_root = (_REPO_ROOT / args.sources_root).resolve()

    if args.brief:
        briefs = [Path(b) if Path(b).is_absolute() else _REPO_ROOT / b for b in args.brief]
    else:
        briefs = sorted(p for p in briefs_root.glob("*.md") if p.name.lower() != "readme.md")

    # The diff guard is a repo-level check (which paths the commit touched), enforced once.
    changed_paths = _changed_paths(args.diff_base) if args.diff_base else None

    if not briefs:
        print(f"synthesis-lint: no briefs under {briefs_root} — nothing to lint (ok).")

    total = 0
    diff_done = False
    for brief in briefs:
        if not brief.exists():
            print(f"synthesis-lint: FAIL — brief not found: {brief}")
            total += 1
            continue
        text = brief.read_text(encoding="utf-8")
        violations = lint_brief(
            text,
            changed_paths=None if diff_done else changed_paths,
            sources_root=sources_root,
        )
        diff_done = True  # diff guard is repo-wide; attribute it to the first brief only
        rel = brief.relative_to(_REPO_ROOT)
        if violations:
            for v in violations:
                print(f"synthesis-lint: FAIL [{rel}] — {v}")
            total += len(violations)
        else:
            print(f"synthesis-lint: ok [{rel}]")

    if total:
        print(f"synthesis-lint: {total} violation(s).")
        return 1
    print("synthesis-lint: all briefs clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
