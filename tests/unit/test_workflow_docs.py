"""Regression guard: the docs CI table must list every shipped workflow (docs/README.md).

azimuth's public front door for "how is this repo guarded?" is the **Continuous integration
& gates** table in `docs/README.md`. A public visitor reads it to trust that the engine is
watched. When a workflow ships but the table is not updated, that trust silently rots — which
is exactly what happened when `synthesis-freshness.yml` (the L2 heartbeat) went live and the
table still said "Four GitHub Actions workflows" and omitted the row.

This test turns that class of doc-drift into a build failure. It discovers the real workflow
surface (`.github/workflows/*.yml`) rather than hard-coding it, then asserts:

  1. every workflow file is named in the docs CI table, and
  2. the prose count word ("Five GitHub Actions workflows …") matches the actual count.

Same discipline as the CLI-surface guard (`tests/integration/test_cli_surface.py`): the docs
that tell the public how the repo works cannot describe a surface that no longer matches disk.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOWS = _REPO_ROOT / ".github" / "workflows"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"

# Enough range to cover any plausible workflow count without a dependency.
_NUMBER_WORDS = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
}


def _workflow_files() -> list[Path]:
    return sorted(
        p
        for p in _WORKFLOWS.glob("*.y*ml")
        if p.suffix in {".yml", ".yaml"}
    )


def test_workflow_surface_is_non_empty() -> None:
    # Guard the guard: a moved dir or glob typo must fail loud, not pass zero cases.
    files = _workflow_files()
    assert len(files) >= 4, f"expected the .github/workflows surface, found {files!r}"


def test_every_workflow_is_listed_in_docs_index() -> None:
    """Each `.github/workflows/*.yml` file name must appear in the docs CI table."""
    text = _DOCS_INDEX.read_text(encoding="utf-8")
    missing = [wf.name for wf in _workflow_files() if wf.name not in text]
    assert not missing, (
        "docs/README.md CI & gates table is out of date — these shipped workflows are "
        f"not documented: {missing}. Add a row for each."
    )


def test_docs_index_workflow_count_word_matches() -> None:
    """The prose count ("Five GitHub Actions workflows …") must match the real count."""
    count = len(_workflow_files())
    word = _NUMBER_WORDS.get(count)
    assert word is not None, f"unexpected workflow count {count}; extend _NUMBER_WORDS"
    text = _DOCS_INDEX.read_text(encoding="utf-8")
    expected = f"{word} GitHub Actions workflows"
    assert expected in text, (
        f"docs/README.md should say '{expected}' (there are {count} workflow files) — "
        "the count prose drifted from the .github/workflows surface."
    )
