#!/usr/bin/env python3
"""Seed azimuth's *good first issues* — the contributor on-ramp.

A public repo converts visitors into contributors through a handful of well-scoped,
self-contained starter tasks. This script is the single source of truth for that set:
the :data:`ISSUES` list below defines each one, and the script both

  * **renders** the human-readable ``.github/GOOD_FIRST_ISSUES.md`` catalog (so the list
    is discoverable without a GitHub account and reviewable in a PR), and
  * **seeds** the live issue tracker at the public flip via ``gh`` — creating the
    ``good first issue`` label set and one tracking issue per entry, idempotently.

Because the catalog is *generated* from :data:`ISSUES`, it is byte-reproducible and
CI-guarded exactly like ``build_graph.py`` / ``build_autonomy.py``: ``--check`` fails if
the committed markdown drifts from the canonical list, so the doc can never rot away from
what the flip-time seeding would actually create.

Usage:
    python scripts/seed_good_first_issues.py            # print the seeding plan (dry run)
    python scripts/seed_good_first_issues.py --write     # (re)write .github/GOOD_FIRST_ISSUES.md
    python scripts/seed_good_first_issues.py --check      # exit 1 if the committed doc is stale
    python scripts/seed_good_first_issues.py --create     # create labels + issues via `gh` (flip)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_OUT = _REPO_ROOT / ".github" / "GOOD_FIRST_ISSUES.md"

_GOOD_FIRST = "good first issue"

# GitHub label -> (6-hex color, description). Colors follow GitHub's default palette so
# the seeded labels look native. ``gh label create --force`` is idempotent.
_LABEL_META: dict[str, tuple[str, str]] = {
    _GOOD_FIRST: ("7057ff", "Good for newcomers — well-scoped and self-contained"),
    "help wanted": ("008672", "Extra attention is welcome"),
    "documentation": ("0075ca", "Improvements or additions to documentation"),
    "enhancement": ("a2eeef", "New feature or request"),
    "tests": ("bfdadc", "Adds or improves test coverage"),
}


@dataclass(frozen=True)
class Issue:
    """One seeded good-first-issue. ``slug`` is stable; ``title`` is what GitHub shows."""

    slug: str
    title: str
    labels: tuple[str, ...]
    difficulty: str
    estimate: str
    summary: str
    why: str
    steps: tuple[str, ...]
    files: tuple[str, ...]
    acceptance: tuple[str, ...]
    verify: tuple[str, ...]


# --------------------------------------------------------------------------------------
# The canonical set. Every task is real, open today, and scoped so a newcomer can finish
# it without knowing the ingest/synthesis internals. Referenced files are named as they
# exist in the repo so the issue never sends someone at already-done work.
# --------------------------------------------------------------------------------------
ISSUES: tuple[Issue, ...] = (
    Issue(
        slug="add-data-channel",
        title="Add a new WorldMonitor data channel",
        labels=(_GOOD_FIRST, "enhancement", "help wanted"),
        difficulty="Beginner",
        estimate="~15 min",
        summary=(
            "Surface one more clean, free-tier WorldMonitor subset by adding a single "
            "entry to `sources/registry.json` (+ its `CREDITS.md` attribution)."
        ),
        why=(
            "The whole point of the registry-driven design is that a new source is a "
            "one-file change, not a code change — this issue proves it and grows the graph."
        ),
        steps=(
            "Read the 15-minute walkthrough in CONTRIBUTING.md.",
            "Pick a WorldMonitor subset that clears the editorial + license bar "
            "(free anonymous tier, compatible license, factual content class).",
            "Append the entry to `sources/registry.json` and its attribution line to `CREDITS.md`.",
            "Run `python scripts/check_sources.py` then `python scripts/run_ingest.py` to pull a sample L1 day.",
        ),
        files=("sources/registry.json", "CREDITS.md"),
        acceptance=(
            "`python scripts/check_sources.py` passes with the new source surfaced.",
            "A sample `vault/01 Sources/<day>/<key>.md` note is produced and looks factual.",
            "The new theme (if any) renders in the brief index and site.",
        ),
        verify=(
            "python scripts/check_sources.py",
            "python scripts/build_brief_index.py --check",
        ),
    ),
    Issue(
        slug="docs-glossary",
        title="Add a docs/glossary.md of the L1/L2/L3 doctrine terms",
        labels=(_GOOD_FIRST, "documentation", "help wanted"),
        difficulty="Beginner",
        estimate="~20 min",
        summary=(
            "First-time visitors meet 'L1 source', 'L2 brief', 'L3 rule', 'editorial line', "
            "'guardrail', 'source registry' with no single definition list. Add one."
        ),
        why=(
            "A short glossary is the fastest onboarding win and the friendliest first PR — "
            "it lowers the bar for everyone who comes after."
        ),
        steps=(
            "Create `docs/glossary.md` with a short definition for each core term.",
            "Pull the exact meanings from `docs/architecture.md` and `CONTRIBUTING.md` — do not invent new ones.",
            "Link the glossary from `docs/README.md` so it is not orphaned (CI enforces this).",
        ),
        files=("docs/glossary.md", "docs/README.md"),
        acceptance=(
            "`docs/glossary.md` defines at least the six core doctrine terms.",
            "It is linked from `docs/README.md` (the docs index).",
            "`python scripts/check_doc_orphans.py` and `check_doc_links.py` both pass.",
        ),
        verify=(
            "python scripts/check_doc_links.py",
            "python scripts/check_doc_orphans.py",
        ),
    ),
    Issue(
        slug="query-graph-timeline",
        title="Add a `timeline` query mode to scripts/query_graph.py",
        labels=(_GOOD_FIRST, "enhancement"),
        difficulty="Intermediate",
        estimate="~1 hr",
        summary=(
            "The graph query CLI has stats / relations / neighbors / path / connect / "
            "provenance / evidence / bridges / hubs — but no way to list an entity's "
            "mentions ordered by the L1 source day. Add a `timeline <entity>` subcommand."
        ),
        why=(
            "Time is the one axis the graph does not yet expose on the CLI; a timeline turns "
            "'where is X mentioned' into 'when did X show up', a real analyst question."
        ),
        steps=(
            "Add a `timeline` subparser next to the existing ones in `scripts/query_graph.py`.",
            "Walk the `named-in` edges for the entity, resolve each to its dated L1 note, sort by day.",
            "Support the shared `--json` flag like the other subcommands.",
            "Add a unit test mirroring the existing `test_query_graph.py` cases.",
        ),
        files=("scripts/query_graph.py", "tests/unit/test_query_graph.py", "docs/cli.md"),
        acceptance=(
            '`python scripts/query_graph.py timeline "Greece"` prints the dated mentions in order.',
            "`--json` yields a machine-readable list.",
            "A new unit test covers the happy path and the unknown-entity path.",
        ),
        verify=(
            'python scripts/query_graph.py timeline "Greece"',
            "pytest tests/unit/test_query_graph.py -q",
        ),
    ),
    Issue(
        slug="ingest-http-tests",
        title="Add unit tests for ingest/http.py",
        labels=(_GOOD_FIRST, "tests", "help wanted"),
        difficulty="Intermediate",
        estimate="~1 hr",
        summary=(
            "The anonymous-session fetcher `ingest/http.py` (stdlib urllib) has no dedicated "
            "unit test. Add one that exercises the session mint + fetch against a local stub."
        ),
        why=(
            "It is the one network seam in the ingest path; a focused test protects it from "
            "silent regressions and lifts coverage on the riskiest module."
        ),
        steps=(
            "Create `tests/unit/test_http.py`.",
            "Stand up a `http.server` stub (see `scripts/record_hero_gif.py` for the pattern) "
            "that returns a session cookie then a JSON payload.",
            "Assert the fetcher mints a session, sends the cookie, and parses the body — "
            "with no real network call.",
        ),
        files=("ingest/http.py", "tests/unit/test_http.py"),
        acceptance=(
            "New tests cover the session-mint and the authenticated fetch path.",
            "`pytest tests/unit/test_http.py -v` is green with no outbound network.",
            "Coverage on `ingest/http.py` rises.",
        ),
        verify=(
            "pytest tests/unit/test_http.py -v",
            "pytest tests/ --cov=ingest --cov-report=term-missing",
        ),
    ),
    Issue(
        slug="synthesis-lint-superlatives",
        title="Add a synthesis-lint rule for unattributed superlatives",
        labels=(_GOOD_FIRST, "enhancement"),
        difficulty="Intermediate",
        estimate="~1.5 hr",
        summary=(
            "The editorial line forbids un-sourced claims. Add a `synthesis/lint.py` check "
            "that flags superlatives ('largest', 'worst', 'record') in an L2 brief unless the "
            "same sentence cites an L1 source."
        ),
        why=(
            "Superlatives are exactly where a neutral fact quietly becomes an editorial claim; "
            "catching them in CI keeps the briefs honest at scale."
        ),
        steps=(
            "Add a new check function to `synthesis/lint.py` following the existing rule pattern.",
            "Match a small superlative word list; pass only if the sentence carries an L1 link/citation.",
            "Wire it into the lint run and add fixtures to `tests/unit/test_lint.py`.",
        ),
        files=("synthesis/lint.py", "tests/unit/test_lint.py"),
        acceptance=(
            "A brief with an unattributed superlative fails `python scripts/check_synthesis.py`.",
            "The same superlative with an adjacent L1 citation passes.",
            "New unit tests cover both directions.",
        ),
        verify=(
            "python scripts/check_synthesis.py",
            "pytest tests/unit/test_lint.py -q",
        ),
    ),
)


# --------------------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------------------
def _issue_body(issue: Issue) -> str:
    """The GitHub issue body — also embedded verbatim in the markdown catalog."""
    lines: list[str] = []
    lines.append(f"**Difficulty:** {issue.difficulty} · **Estimate:** {issue.estimate}")
    lines.append("")
    lines.append(issue.summary)
    lines.append("")
    lines.append(f"**Why it matters.** {issue.why}")
    lines.append("")
    lines.append("**What to do**")
    lines.append("")
    for i, step in enumerate(issue.steps, 1):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("**Files you'll touch**")
    lines.append("")
    for f in issue.files:
        lines.append(f"- `{f}`")
    lines.append("")
    lines.append("**Done when**")
    lines.append("")
    for a in issue.acceptance:
        lines.append(f"- [ ] {a}")
    lines.append("")
    lines.append("**Verify locally**")
    lines.append("")
    lines.append("```bash")
    lines.extend(issue.verify)
    lines.append("```")
    return "\n".join(lines)


def render_markdown() -> str:
    """Render the full `.github/GOOD_FIRST_ISSUES.md` catalog from :data:`ISSUES`."""
    out: list[str] = []
    out.append("# Good first issues")
    out.append("")
    out.append(
        "> **Generated file — do not edit by hand.** This catalog is rendered from "
        "`scripts/seed_good_first_issues.py` and CI fails if it drifts. To change an "
        "issue, edit the `ISSUES` list in that script and run "
        "`python scripts/seed_good_first_issues.py --write`."
    )
    out.append("")
    out.append(
        "These are the starter tasks a newcomer can pick up without knowing the ingest or "
        "synthesis internals. Each is small, self-contained, and real (open today). New to "
        "the repo? Read [CONTRIBUTING.md](../CONTRIBUTING.md) first — especially the "
        "15-minute *add a data channel* walkthrough."
    )
    out.append("")
    out.append(
        "At the public flip these are seeded onto the tracker in one command "
        "(`python scripts/seed_good_first_issues.py --create`), each tagged "
        f"`{_GOOD_FIRST}` so the "
        "[label filter](https://github.com/mickywin22/azimuth/issues?q=label%3A%22good+first+issue%22) "
        "returns them. Until then, this page IS the list — comment on the repo to claim one."
    )
    out.append("")
    out.append("| # | Task | Difficulty | Labels |")
    out.append("|---|------|-----------|--------|")
    for i, issue in enumerate(ISSUES, 1):
        labels = ", ".join(f"`{lbl}`" for lbl in issue.labels)
        out.append(f"| {i} | [{issue.title}](#{issue.slug}) | {issue.difficulty} | {labels} |")
    out.append("")
    for i, issue in enumerate(ISSUES, 1):
        out.append(f'<a id="{issue.slug}"></a>')
        out.append("")
        out.append(f"## {i}. {issue.title}")
        out.append("")
        out.append(_issue_body(issue))
        out.append("")
        out.append("---")
        out.append("")
    out.append(
        "*Unsure which to pick? Start with the **glossary** or a **docs clarity** task — "
        "the fastest path to a merged PR and a feel for the codebase.*"
    )
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------------------
# gh seeding (flip-time)
# --------------------------------------------------------------------------------------
def _run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=capture, text=True, check=False)


def _ensure_labels(labels: set[str]) -> None:
    for label in sorted(labels):
        color, desc = _LABEL_META.get(label, ("ededed", ""))
        print(f"  label: {label}")
        _run(
            ["gh", "label", "create", label, "--color", color, "--description", desc, "--force"],
        )


def _existing_titles() -> set[str]:
    """Titles of issues that already exist (any state), so --create is idempotent."""
    proc = _run(
        ["gh", "issue", "list", "--state", "all", "--limit", "500", "--json", "title"],
        capture=True,
    )
    if proc.returncode != 0:
        print(f"WARNING: could not list existing issues:\n{proc.stderr}", file=sys.stderr)
        return set()
    try:
        rows = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return set()
    return {str(r.get("title", "")) for r in rows}


def create() -> int:
    """Create the label set + one issue per entry via `gh`. Idempotent."""
    if _run(["gh", "--version"], capture=True).returncode != 0:
        print("ERROR: the GitHub CLI `gh` is not available on PATH.", file=sys.stderr)
        return 1

    all_labels = {lbl for issue in ISSUES for lbl in issue.labels}
    print("Ensuring labels exist…")
    _ensure_labels(all_labels)

    existing = _existing_titles()
    created = 0
    for issue in ISSUES:
        if issue.title in existing:
            print(f"  skip (exists): {issue.title}")
            continue
        cmd = ["gh", "issue", "create", "--title", issue.title, "--body", _issue_body(issue)]
        for lbl in issue.labels:
            cmd += ["--label", lbl]
        proc = _run(cmd, capture=True)
        if proc.returncode == 0:
            print(f"  created: {issue.title}\n    {proc.stdout.strip()}")
            created += 1
        else:
            print(f"  FAILED: {issue.title}\n    {proc.stderr.strip()}", file=sys.stderr)
    print(f"Done — {created} issue(s) created, {len(ISSUES) - created} skipped/failed.")
    return 0


def _print_plan() -> None:
    print(f"azimuth good-first-issues — {len(ISSUES)} issue(s) defined:\n")
    for i, issue in enumerate(ISSUES, 1):
        print(f"  {i}. [{issue.difficulty}] {issue.title}")
        print(f"     labels: {', '.join(issue.labels)}")
    print(
        "\nDry run. Use --write to regenerate the catalog, "
        "or --create to seed the tracker at the public flip."
    )


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="seed azimuth good first issues")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="(re)write the markdown catalog")
    group.add_argument("--check", action="store_true", help="exit 1 if the catalog is stale")
    group.add_argument("--create", action="store_true", help="create labels + issues via gh")
    args = parser.parse_args(argv)

    rendered = render_markdown()

    if args.check:
        current = _OUT.read_text(encoding="utf-8") if _OUT.exists() else ""
        if current != rendered:
            print(
                "ERROR: .github/GOOD_FIRST_ISSUES.md is stale.\n"
                "Run: python scripts/seed_good_first_issues.py --write",
                file=sys.stderr,
            )
            return 1
        print("good-first-issues catalog is in sync.")
        return 0

    if args.write:
        _OUT.parent.mkdir(parents=True, exist_ok=True)
        _OUT.write_text(rendered, encoding="utf-8")
        print(f"wrote {_OUT.relative_to(_REPO_ROOT)} ({len(ISSUES)} issues)")
        return 0

    if args.create:
        return create()

    _print_plan()
    return 0


if __name__ == "__main__":
    sys.exit(main())
