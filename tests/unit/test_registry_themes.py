"""Multi-theme registry + brief-index integrity tests.

These guard the W26 multi-theme expansion contract:

* every surfaced source declares a ``theme``;
* every theme a surfaced source points at exists in the registry ``themes`` map;
* every excluded (``surfaced: false``) source carries a ``surfaced_reason`` (so a skipped
  channel always has a logged reason, per the KR acceptance criteria);
* every active (non-held) surfaced theme has an L2 brief file on disk;
* the generated brief index (``vault/02 Briefs/README.md``) is in sync with the briefs.
"""

from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_REGISTRY = _REPO_ROOT / "sources" / "registry.json"
_BRIEFS_DIR = _REPO_ROOT / "vault" / "02 Briefs"


def _registry() -> dict[str, object]:
    return json.loads(_REGISTRY.read_text(encoding="utf-8"))


def test_surfaced_sources_declare_a_known_theme() -> None:
    data = _registry()
    themes = data["themes"]
    assert isinstance(themes, dict)
    for source in data["sources"]:
        assert isinstance(source, dict)
        if source.get("surfaced"):
            theme = source.get("theme")
            assert theme, f"surfaced source {source['key']} has no theme"
            assert theme in themes, f"surfaced source {source['key']} -> unknown theme {theme}"


def test_excluded_sources_log_a_reason() -> None:
    data = _registry()
    for source in data["sources"]:
        assert isinstance(source, dict)
        if not source.get("surfaced"):
            reason = source.get("surfaced_reason", "")
            assert reason, f"excluded source {source['key']} has no surfaced_reason"


def test_active_themes_have_a_brief_file() -> None:
    data = _registry()
    themes = data["themes"]
    assert isinstance(themes, dict)
    surfaced_themes = {
        s["theme"]
        for s in data["sources"]
        if isinstance(s, dict) and s.get("surfaced") and s.get("theme")
    }
    for slug in surfaced_themes:
        meta = themes[slug]
        assert isinstance(meta, dict)
        if meta.get("brief_held"):
            assert meta.get("hold_reason"), f"held theme {slug} has no hold_reason"
            continue
        brief = _BRIEFS_DIR / str(meta["brief"])
        assert brief.exists(), f"active theme {slug} has no brief file {brief.name}"


def test_brief_index_is_in_sync() -> None:
    from scripts.build_brief_index import render  # local import: scripts is not a package dep

    index = _BRIEFS_DIR / "README.md"
    assert index.exists(), "brief index README.md is missing"
    assert index.read_text(encoding="utf-8") == render(), (
        "brief index is stale — run `python scripts/build_brief_index.py` and commit"
    )
