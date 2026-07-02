"""Docs-completeness gate: every ``scripts/*.py`` CLI is documented in docs/cli.md.

``docs/cli.md`` opens with the promise "Every command under ``scripts/`` in one map."
On a public repo that promise is load-bearing — a contributor reads it to learn the whole
surface, and a silently-undocumented script tells them the docs are stale. Until this test
existed the completeness was checked by eye (the 2026-07-02 sweep found ``smoke_graph.py``
and ``Build-Graphify-AST-Only.py`` missing). This test turns that drift class into a build
failure, the same way ``check_doc_links.py`` did for dead links.

The rule is deliberately narrow: the script's *filename* must appear somewhere in cli.md.
That is enough to catch "a whole command is missing" without policing exact wording.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS_DIR = _REPO_ROOT / "scripts"
_CLI_DOC = _REPO_ROOT / "docs" / "cli.md"


def _cli_scripts() -> list[Path]:
    """Every runnable CLI under scripts/ — excludes package plumbing."""
    return sorted(
        p
        for p in _SCRIPTS_DIR.glob("*.py")
        if p.name != "__init__.py" and not p.name.startswith("_")
    )


def test_cli_doc_exists() -> None:
    assert _CLI_DOC.is_file(), f"missing docs/cli.md at {_CLI_DOC}"


def test_every_script_is_documented() -> None:
    doc = _CLI_DOC.read_text(encoding="utf-8")
    missing = [p.name for p in _cli_scripts() if p.name not in doc]
    assert not missing, (
        "docs/cli.md promises 'Every command under scripts/' but these are undocumented: "
        + ", ".join(missing)
    )


def test_scripts_dir_is_not_empty() -> None:
    # Guard the guard: if the glob ever silently matches nothing, the coverage
    # test above would vacuously pass. Fail loudly instead.
    assert _cli_scripts(), "no scripts/*.py found — coverage test would be vacuous"
