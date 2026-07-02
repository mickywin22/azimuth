"""Docs-completeness gate: every ``docs/**/*.md`` page is listed in the docs index.

``docs/README.md`` opens with the promise "Everything under ``docs/`` in one map."
On a public repo that promise is load-bearing — the index is the deep-dive front door,
and a doc that exists on disk but is absent from the map is invisible to a visitor
(``security/secret-scan-2026-06-30.md`` sat unindexed until the 2026-07-03 sweep).
This test turns that drift class into a build failure, the same way
``check_doc_links.py`` did for dead links and ``test_cli_doc_coverage.py`` did for
undocumented CLIs.

The rule is deliberately narrow: the page's docs-relative POSIX path (e.g.
``security/public-flip-readiness.md``) must appear somewhere in the index text.
That catches "a whole page is missing" without policing wording or table layout.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DOCS_DIR = _REPO_ROOT / "docs"
_INDEX = _DOCS_DIR / "README.md"


def _doc_pages() -> list[Path]:
    """Every Markdown page under docs/ that the index must map — excludes the index itself."""
    return sorted(p for p in _DOCS_DIR.rglob("*.md") if p != _INDEX)


def test_docs_index_exists() -> None:
    assert _INDEX.is_file(), f"missing docs index at {_INDEX}"


def test_every_doc_page_is_indexed() -> None:
    index_text = _INDEX.read_text(encoding="utf-8")
    missing = [
        p.relative_to(_DOCS_DIR).as_posix()
        for p in _doc_pages()
        if p.relative_to(_DOCS_DIR).as_posix() not in index_text
    ]
    assert not missing, (
        "docs/README.md promises 'Everything under docs/ in one map' but these pages "
        "are not in the index: " + ", ".join(missing)
    )


def test_docs_dir_is_not_empty() -> None:
    # Guard the guard: if the glob ever silently matches nothing, the coverage
    # test above would vacuously pass. Fail loudly instead.
    assert _doc_pages(), "no docs/**/*.md found — coverage test would be vacuous"
