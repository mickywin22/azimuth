"""Tests for the Markdown dead-link gate (scripts/check_doc_links.py).

Two load-bearing halves, same shape as the secret-scan gate:
  (a) the gate has TEETH -- a link to a missing file is flagged; and
  (b) it does NOT false-positive on the legitimate constructs this repo uses --
      external URLs, pure anchors, ``<spaces in path>`` targets, ``%20`` encoding,
      and link syntax that appears only *inside* code spans as an example.
A link checker that passes because it can't parse anything is worse than none.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_doc_links", _REPO_ROOT / "scripts" / "check_doc_links.py"
)
assert _spec and _spec.loader
cdl = importlib.util.module_from_spec(_spec)
sys.modules["check_doc_links"] = cdl
_spec.loader.exec_module(cdl)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- teeth: real dead links must be caught ----------------------------------


def test_flags_dead_relative_link(tmp_path: Path) -> None:
    _write(tmp_path, "index.md", "See [the plan](plan.md).")
    result = cdl.check_links(tmp_path)
    assert not result.ok
    assert len(result.dead) == 1
    assert result.dead[0].target == "plan.md"


def test_flags_dead_image_link(tmp_path: Path) -> None:
    _write(tmp_path, "doc.md", "![diagram](assets/missing.png)")
    result = cdl.check_links(tmp_path)
    assert not result.ok
    assert result.dead[0].target == "assets/missing.png"


def test_reports_line_number(tmp_path: Path) -> None:
    _write(tmp_path, "doc.md", "intro\n\n[gone](nope.md)\n")
    result = cdl.check_links(tmp_path)
    assert result.dead[0].line == 3


# --- resolution: valid links pass -------------------------------------------


def test_valid_relative_link_passes(tmp_path: Path) -> None:
    _write(tmp_path, "plan.md", "# plan")
    _write(tmp_path, "index.md", "See [the plan](plan.md).")
    result = cdl.check_links(tmp_path)
    assert result.ok
    assert result.links_checked == 1


def test_valid_link_into_subdir(tmp_path: Path) -> None:
    _write(tmp_path, "docs/spec.md", "# spec")
    _write(tmp_path, "index.md", "[spec](docs/spec.md)")
    assert cdl.check_links(tmp_path).ok


def test_parent_relative_link(tmp_path: Path) -> None:
    _write(tmp_path, "SECURITY.md", "# security")
    _write(tmp_path, "docs/README.md", "[security](../SECURITY.md)")
    assert cdl.check_links(tmp_path).ok


def test_angle_bracket_and_percent_encoding(tmp_path: Path) -> None:
    _write(tmp_path, "vault/00 Rules/editorial.md", "# editorial")
    # brief-index style spaces-in-path + a percent-encoded sibling path
    _write(
        tmp_path,
        "vault/briefs.md",
        "[rules](<00 Rules/editorial.md>) and [enc](00%20Rules/editorial.md)",
    )
    result = cdl.check_links(tmp_path)
    assert result.ok
    assert result.links_checked == 2


def test_root_relative_link(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cdl, "_REPO_ROOT", tmp_path)
    _write(tmp_path, "LICENSE", "MIT")
    _write(tmp_path, "docs/deep/note.md", "[license](/LICENSE)")
    assert cdl.check_links(tmp_path).ok


# --- no false positives ------------------------------------------------------


def test_external_and_anchor_links_skipped(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "doc.md",
        "[web](https://worldmonitor.app) [mail](mailto:a@b.co) [top](#intro)",
    )
    result = cdl.check_links(tmp_path)
    assert result.ok
    assert result.links_checked == 0


def test_link_inside_inline_code_ignored(tmp_path: Path) -> None:
    # The OKF strategy doc writes `[x](/path.md)` as an example -- must not flag.
    _write(tmp_path, "doc.md", "Use `[x](/path.md)` for relationships.")
    result = cdl.check_links(tmp_path)
    assert result.ok
    assert result.links_checked == 0


def test_link_inside_fenced_code_ignored(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "doc.md",
        "```md\n[example](does-not-exist.md)\n```\n",
    )
    result = cdl.check_links(tmp_path)
    assert result.ok


def test_double_backtick_span_does_not_leak_example_link(tmp_path: Path) -> None:
    # doc-links.md shows link syntax verbatim inside a double-backtick span:
    # `` `[x](/path.md)` ``. A single-backtick stripper mis-pairs the run and leaks
    # the example target back into the scan. Runs must be matched by length.
    _write(tmp_path, "doc.md", "An example link like `` `[x](/path.md)` `` is skipped.")
    result = cdl.check_links(tmp_path)
    assert result.ok
    assert result.links_checked == 0


def test_anchor_stripped_before_existence(tmp_path: Path) -> None:
    _write(tmp_path, "spec.md", "# spec")
    _write(tmp_path, "index.md", "[jump](spec.md#section-3)")
    assert cdl.check_links(tmp_path).ok


# --- scope -------------------------------------------------------------------


def test_excluded_dirs_not_scanned(tmp_path: Path) -> None:
    _write(tmp_path, "site/generated.md", "[dead](missing.md)")
    _write(tmp_path, ".venv/pkg.md", "[dead](missing.md)")
    result = cdl.check_links(tmp_path)
    assert result.ok
    assert result.files_scanned == 0


def test_repo_itself_has_no_dead_links() -> None:
    # Regression guard: the live repository must stay link-clean.
    result = cdl.check_links(_REPO_ROOT)
    assert result.ok, "dead links: " + "; ".join(
        f"{d.source.relative_to(_REPO_ROOT)}:{d.line} -> {d.target}" for d in result.dead
    )
