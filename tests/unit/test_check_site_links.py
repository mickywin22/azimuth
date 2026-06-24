"""Tests for the broken-internal-link checker (scripts/check_site_links.py).

Guarantees:
* a clean site with only resolving internal links returns no breakages;
* a dangling file link and a missing #anchor are both caught;
* JS template-literal hrefs inside <script> (e.g. ``${n.url}``) are NOT flagged;
* external (http/mailto) links are ignored.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "check_site_links.py"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_site_links", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_clean_site_has_no_broken_links(tmp_path: Path) -> None:
    mod = _load()
    (tmp_path / "index.html").write_text(
        '<a href="okf.html">OKF</a><a href="sub/page.html#sec">deep</a>'
        '<a href="https://example.com">ext</a>'
        '<script>const u = `${x.url}`;</script>',
        encoding="utf-8",
    )
    (tmp_path / "okf.html").write_text("<h1>OKF</h1>", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "page.html").write_text('<h2 id="sec">Sec</h2>', encoding="utf-8")

    assert mod.check_site(tmp_path) == []


def test_missing_file_and_anchor_are_caught(tmp_path: Path) -> None:
    mod = _load()
    (tmp_path / "index.html").write_text(
        '<a href="gone.html">x</a><a href="okf.html#nope">y</a>',
        encoding="utf-8",
    )
    (tmp_path / "okf.html").write_text("<h1>OKF</h1>", encoding="utf-8")

    broken = mod.check_site(tmp_path)
    assert len(broken) == 2
    assert any("gone.html" in b for b in broken)
    assert any("#nope" in b for b in broken)
