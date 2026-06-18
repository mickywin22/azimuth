"""Tests for the L2 synthesis freshness gate (``scripts/check_synthesis_freshness.py``).

Guards the weekly-cadence trigger/verifier contract:

* a brief is STALE when a newer L1 ingest day exists for its theme's sources;
* a brief is fresh when its ``updated`` date is >= the latest L1 day;
* held themes are excluded entirely (a newer L1 day must never mark a held brief stale);
* a clean theme with L1 data but no brief on disk is stale (missing brief);
* ``--check`` exits non-zero iff at least one clean brief is stale.

The pure-logic tests build a throwaway repo tree and point the module's path constants at it,
so they never depend on the live vault state. One integration test asserts the real repo is
internally consistent (no clean brief older than its latest L1 day right now).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType

    import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPT = _REPO_ROOT / "scripts" / "check_synthesis_freshness.py"


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_synthesis_freshness", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _build_tree(
    tmp: Path,
    *,
    registry: dict,
    l1_days: dict[str, list[str]],
    briefs: dict[str, str],
) -> None:
    """Write a minimal azimuth tree: registry + dated L1 notes + brief files."""
    (tmp / "sources").mkdir(parents=True)
    (tmp / "sources" / "registry.json").write_text(json.dumps(registry), encoding="utf-8")

    src_dir = tmp / "vault" / "01 Sources"
    src_dir.mkdir(parents=True)
    for day, keys in l1_days.items():
        day_dir = src_dir / day
        day_dir.mkdir()
        for key in keys:
            (day_dir / f"{key}.md").write_text("---\nsource_key: x\n---\n", encoding="utf-8")

    briefs_dir = tmp / "vault" / "02 Briefs"
    briefs_dir.mkdir(parents=True)
    for fname, updated in briefs.items():
        (briefs_dir / fname).write_text(
            f"---\ntitle: T\ntheme: x\nupdated: {updated}\n---\n# T\n", encoding="utf-8"
        )


def _point_module_at(mod: ModuleType, tmp: Path) -> None:
    mod._SOURCES_DIR = tmp / "vault" / "01 Sources"
    mod._BRIEFS_DIR = tmp / "vault" / "02 Briefs"
    mod._REGISTRY = tmp / "sources" / "registry.json"


_BASE_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "geophysical": {"title": "Geophysical Weekly", "brief": "Geophysical Weekly.md"},
        "prediction-markets": {
            "title": "Prediction Markets Weekly",
            "brief": "Prediction Markets Weekly.md",
            "brief_held": True,
            "hold_reason": "single politically-charged market",
        },
    },
    "sources": [
        {"key": "energy-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "earthquakes", "theme": "geophysical", "surfaced": True},
        {"key": "prediction-markets", "theme": "prediction-markets", "surfaced": True},
        {"key": "conflict", "theme": None, "surfaced": False},
    ],
}


def test_brief_fresh_when_updated_matches_latest_l1(tmp_path: Path) -> None:
    mod = _load_module()
    _build_tree(
        tmp_path,
        registry=_BASE_REGISTRY,
        l1_days={"2026-06-18": ["energy-prices", "earthquakes", "prediction-markets"]},
        briefs={
            "Energy Supply Weekly.md": "2026-06-18T12:00:00Z",
            "Geophysical Weekly.md": "2026-06-18T12:30:00Z",
        },
    )
    _point_module_at(mod, tmp_path)
    rows = {r["theme"]: r for r in mod.assess()}
    assert rows["energy-supply"]["stale"] is False
    assert rows["geophysical"]["stale"] is False


def test_brief_stale_when_newer_l1_day_exists(tmp_path: Path) -> None:
    mod = _load_module()
    _build_tree(
        tmp_path,
        registry=_BASE_REGISTRY,
        l1_days={
            "2026-06-18": ["energy-prices", "earthquakes"],
            "2026-06-25": ["energy-prices"],  # newer day touches energy only
        },
        briefs={
            "Energy Supply Weekly.md": "2026-06-18T12:00:00Z",
            "Geophysical Weekly.md": "2026-06-18T12:30:00Z",
        },
    )
    _point_module_at(mod, tmp_path)
    rows = {r["theme"]: r for r in mod.assess()}
    assert rows["energy-supply"]["stale"] is True  # has a 2026-06-25 L1 it hasn't absorbed
    assert rows["energy-supply"]["latest_l1"] == "2026-06-25"
    assert rows["geophysical"]["stale"] is False  # no newer geophysical L1


def test_held_theme_never_appears(tmp_path: Path) -> None:
    mod = _load_module()
    _build_tree(
        tmp_path,
        registry=_BASE_REGISTRY,
        l1_days={"2026-06-25": ["prediction-markets"]},  # fresh L1 for the held theme
        briefs={},
    )
    _point_module_at(mod, tmp_path)
    themes = {r["theme"] for r in mod.assess()}
    assert "prediction-markets" not in themes


def test_missing_brief_with_l1_is_stale(tmp_path: Path) -> None:
    mod = _load_module()
    _build_tree(
        tmp_path,
        registry=_BASE_REGISTRY,
        l1_days={"2026-06-18": ["earthquakes"]},
        briefs={},  # no Geophysical brief on disk yet
    )
    _point_module_at(mod, tmp_path)
    rows = {r["theme"]: r for r in mod.assess()}
    assert rows["geophysical"]["stale"] is True
    assert rows["geophysical"]["brief_updated"] == "(missing)"


def test_check_exit_code(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mod = _load_module()
    _build_tree(
        tmp_path,
        registry=_BASE_REGISTRY,
        l1_days={
            "2026-06-18": ["energy-prices", "earthquakes"],
            "2026-06-25": ["energy-prices"],
        },
        briefs={
            "Energy Supply Weekly.md": "2026-06-18T12:00:00Z",
            "Geophysical Weekly.md": "2026-06-18T12:30:00Z",
        },
    )
    _point_module_at(mod, tmp_path)
    monkeypatch.setattr("sys.argv", ["check_synthesis_freshness.py", "--check"])
    assert mod.main() == 1  # energy-supply is stale

    # Make everything fresh -> exit 0.
    (tmp_path / "vault" / "02 Briefs" / "Energy Supply Weekly.md").write_text(
        "---\ntitle: T\ntheme: x\nupdated: 2026-06-25T09:00:00Z\n---\n# T\n", encoding="utf-8"
    )
    assert mod.main() == 0


def test_live_repo_is_internally_consistent() -> None:
    """The real repo must not ship a clean brief older than its latest L1 day."""
    mod = _load_module()
    rows = mod.assess()
    stale = [r["theme"] for r in rows if r["stale"]]
    assert not stale, f"clean briefs lagging latest L1 (run the curator): {stale}"
