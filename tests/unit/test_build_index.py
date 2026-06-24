"""Unit tests for the OKF reserved per-folder ``index.md`` generator.

Guards the three OKF Tier-1 G2 acceptance criteria: an ``index.md`` exists at every
``vault/`` level, the ``--check`` flag detects drift, and no generated index carries a
broken link or any frontmatter.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.build_index import (  # noqa: E402
    _INDEX_NAME,
    _all_dirs,
    _broken_links,
    main,
    render,
)


def test_index_exists_at_every_vault_level() -> None:
    for folder in _all_dirs():
        index = folder / _INDEX_NAME
        assert index.is_file(), f"missing OKF index at {folder}"


def test_index_in_sync_and_links_resolve() -> None:
    # Mirrors the CI guard: regenerated content must match what is on disk, byte for byte.
    for folder in _all_dirs():
        index = folder / _INDEX_NAME
        assert index.read_text(encoding="utf-8") == render(folder), (
            f"{index} is stale — run `python scripts/build_index.py` and commit"
        )
        assert _broken_links(folder, render(folder)) == []


def test_index_has_no_frontmatter() -> None:
    # OKF §6: the reserved index.md is navigation, not a concept note → no YAML frontmatter.
    for folder in _all_dirs():
        text = (folder / _INDEX_NAME).read_text(encoding="utf-8")
        assert not text.startswith("---"), f"{folder / _INDEX_NAME} must not carry frontmatter"


def test_check_returns_zero_when_in_sync() -> None:
    assert main(["--check"]) == 0
