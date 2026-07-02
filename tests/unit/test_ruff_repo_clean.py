"""Pins that a plain ``ruff check .`` stays clean repo-wide.

The public repo should read as a polished artifact: someone who clones it and runs
the obvious ``ruff check .`` must see "All checks passed!", not lint errors. The one
file that broke that is ``scripts/Build-Graphify-AST-Only.py`` -- a template-inherited,
Apex-targeting graphify tool that imports the ``graphify`` package (not an azimuth
dependency) and cannot run in this repo. It is out of CI's explicit ruff scope and is
kept pending Michael's keep-vs-delete call, so it is excluded from ruff traversal via
``[tool.ruff] extend-exclude``.

This test pins that exclude so a future "just lint everything" edit can't silently
re-redden the repo-wide ``ruff check .`` (the recurring KR-C wart). Pure stdlib text
assertions over pyproject.toml -- no tomllib parse needed, matches the repo's other
config-guard tests.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PYPROJECT = _REPO_ROOT / "pyproject.toml"
_FOREIGN_SCRIPT = "scripts/Build-Graphify-AST-Only.py"


def test_foreign_graphify_script_is_ruff_excluded() -> None:
    """The off-topic graphify tool stays out of ruff traversal so `ruff check .` is clean."""
    text = _PYPROJECT.read_text(encoding="utf-8")
    assert "extend-exclude" in text, (
        "pyproject lost its [tool.ruff] extend-exclude -- `ruff check .` will re-redden "
        f"on {_FOREIGN_SCRIPT}"
    )
    assert _FOREIGN_SCRIPT in text, (
        f"{_FOREIGN_SCRIPT} is no longer excluded from ruff; either re-add the exclude or, "
        "if the file was deleted, drop this test with it"
    )


def test_excluded_script_either_present_or_test_removed() -> None:
    """The exclude only makes sense while the file exists.

    If the file is deleted (the Michael keep-vs-delete call resolved to delete), the
    exclude line and this whole test should go with it -- so tie them together: as long
    as the exclude names the script, the script must exist.
    """
    text = _PYPROJECT.read_text(encoding="utf-8")
    if _FOREIGN_SCRIPT in text:
        assert (_REPO_ROOT / _FOREIGN_SCRIPT).exists(), (
            f"pyproject excludes {_FOREIGN_SCRIPT} but the file is gone -- remove the "
            "stale extend-exclude entry (and this test)"
        )
