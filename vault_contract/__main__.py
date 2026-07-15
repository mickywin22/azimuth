"""CLI: ``vault-contract <notes-dir> --rules rules.toml [--sources-root DIR] [--diff-base REF]``.

Exit 0 = every note satisfies the declared contract; exit 1 = violations (printed per note).
Pure stdlib. ``python -m vault_contract`` and the ``vault-contract`` console script are the
same entry point.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from vault_contract import RuleSet, check_diff_guard, lint_tree


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vault-contract", description=__doc__)
    ap.add_argument("notes_dir", help="directory of L2 notes to lint (e.g. 'vault/02 Briefs')")
    ap.add_argument("--rules", required=True, help="TOML rules file declaring the contract")
    ap.add_argument("--sources-root", default="", help="L1 root that links must resolve into")
    ap.add_argument(
        "--diff-base",
        default="",
        help="git ref; when set, changed paths vs the ref are checked against the diff rules",
    )
    args = ap.parse_args(argv)

    rules = RuleSet.from_toml(Path(args.rules))
    sources_root = Path(args.sources_root) if args.sources_root else None
    notes_dir = Path(args.notes_dir)
    if not notes_dir.is_dir():
        print(f"vault-contract: notes dir not found: {notes_dir}", file=sys.stderr)
        return 2

    results = lint_tree(notes_dir, rules, sources_root)

    if args.diff_base:
        proc = subprocess.run(
            ["git", "diff", "--name-only", args.diff_base, "--"],
            capture_output=True,
            text=True,
            check=False,
        )
        changed = [ln for ln in proc.stdout.splitlines() if ln.strip()]
        dv = check_diff_guard(changed, rules.diff_allowed_prefixes, rules.diff_forbidden_prefixes)
        if dv:
            results["<diff>"] = dv

    if not results:
        print(f"vault-contract: OK - every note under '{notes_dir}' satisfies the contract.")
        return 0
    for note, violations in results.items():
        for v in violations:
            print(f"vault-contract: FAIL [{note}] {v}")
    print(f"vault-contract: {sum(len(v) for v in results.values())} violation(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
