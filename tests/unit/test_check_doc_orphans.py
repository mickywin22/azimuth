"""Tests for the orphan-doc gate (scripts/check_doc_orphans.py).

Same two load-bearing halves as its sibling dead-link gate:
  (a) TEETH -- a doc that no root front door can reach is flagged as an orphan; and
  (b) NO false positives -- a doc reachable directly, transitively, or via any of the
      repo-root community files (CONTRIBUTING/SECURITY/...) is NOT flagged.
A reachability check that passes because it can't parse links is worse than none.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _REPO_ROOT / "scripts" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# check_doc_orphans imports check_doc_links at module load, so load that first.
_load("check_doc_links")
cdo = _load("check_doc_orphans")


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- teeth: unreachable docs must be caught ---------------------------------


def test_flags_unlinked_doc(tmp_path: Path) -> None:
    _write(tmp_path, "README.md", "welcome, no doc links here")
    _write(tmp_path, "docs/orphan.md", "# nobody links me")
    result = cdo.check_orphans(tmp_path)
    assert not result.ok
    assert [p.name for p in result.orphans] == ["orphan.md"]
    assert result.docs_total == 1
    assert result.docs_reachable == 0


def test_flags_mutually_linking_island(tmp_path: Path) -> None:
    # Two docs that link each other but that no root reaches are still invisible.
    _write(tmp_path, "README.md", "welcome")
    _write(tmp_path, "docs/a.md", "[b](b.md)")
    _write(tmp_path, "docs/b.md", "[a](a.md)")
    result = cdo.check_orphans(tmp_path)
    assert not result.ok
    assert {p.name for p in result.orphans} == {"a.md", "b.md"}


# --- no false positives: reachable docs pass --------------------------------


def test_directly_linked_doc_passes(tmp_path: Path) -> None:
    _write(tmp_path, "README.md", "See [the spec](docs/spec.md).")
    _write(tmp_path, "docs/spec.md", "# spec")
    assert cdo.check_orphans(tmp_path).ok


def test_transitively_linked_doc_passes(tmp_path: Path) -> None:
    _write(tmp_path, "README.md", "[index](docs/README.md)")
    _write(tmp_path, "docs/README.md", "[deep](deep/note.md)")
    _write(tmp_path, "docs/deep/note.md", "# reached via two hops")
    result = cdo.check_orphans(tmp_path)
    assert result.ok
    assert result.docs_total == 2
    assert result.docs_reachable == 2


def test_reachable_via_community_root_file_passes(tmp_path: Path) -> None:
    # A doc linked only from CONTRIBUTING.md (not README) is still discoverable.
    _write(tmp_path, "README.md", "welcome")
    _write(tmp_path, "CONTRIBUTING.md", "[style](docs/style.md)")
    _write(tmp_path, "docs/style.md", "# style guide")
    assert cdo.check_orphans(tmp_path).ok


def test_no_docs_dir_is_ok(tmp_path: Path) -> None:
    _write(tmp_path, "README.md", "no docs directory at all")
    result = cdo.check_orphans(tmp_path)
    assert result.ok
    assert result.docs_total == 0


def test_excluded_trees_are_not_counted(tmp_path: Path) -> None:
    # A generated/cache doc under docs/ must not be required-reachable.
    _write(tmp_path, "README.md", "welcome")
    _write(tmp_path, "docs/__pycache__/junk.md", "# build noise")
    result = cdo.check_orphans(tmp_path)
    assert result.ok
    assert result.docs_total == 0


def test_the_real_repo_has_no_orphans() -> None:
    # The live repo must ship zero orphaned docs -- this is the gate doing its job.
    result = cdo.check_orphans(_REPO_ROOT)
    assert result.ok, f"orphaned docs: {[str(p) for p in result.orphans]}"
