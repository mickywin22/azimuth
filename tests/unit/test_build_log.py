"""Tests for the OKF bundle-log generator (scripts/build_log.py).

The load-bearing guarantees:
* the log is newest-first with ISO ``## YYYY-MM-DD`` headings;
* it is built from ingest folders + brief changelogs;
* HELD themes (brief_held: true) never leak — neither their L1 ingest count nor their brief;
* it is deterministic / idempotent (re-render of the same bundle is byte-identical).
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "build_log.py"
_spec = importlib.util.spec_from_file_location("build_log", _SCRIPT)
assert _spec and _spec.loader
build_log = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_log)


_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "prediction-markets": {
            "title": "Prediction Markets Weekly",
            "brief": "Prediction Markets Weekly.md",
            "brief_held": True,
        },
    },
    "sources": [
        {"key": "fuel-prices", "theme": "energy-supply"},
        {"key": "prediction-markets", "theme": "prediction-markets"},
    ],
}


def _make_vault(root: Path) -> None:
    vault = root / "vault"
    sources = vault / "01 Sources"
    briefs = vault / "02 Briefs"
    briefs.mkdir(parents=True)
    for day in ("2026-06-18", "2026-06-20"):
        d = sources / day
        d.mkdir(parents=True)
        (d / "fuel-prices.md").write_text("---\nsource: Fuel\n---\n# f\n", encoding="utf-8")
        # held theme L1 note — must NOT be counted in the log's ingest line
        (d / "prediction-markets.md").write_text("---\nsource: PM\n---\n# p\n", encoding="utf-8")
    (briefs / "Energy Supply Weekly.md").write_text(
        "---\ntitle: Energy Supply Weekly\n---\n# Energy Supply Weekly\n\n"
        "## Changelog\n\n"
        "- 2026-06-18 — first cycle: wrote the sections from the live day.\n"
        "- 2026-06-20 — refresh: storage advanced one week\n  on the continuation line.\n",
        encoding="utf-8",
    )
    # held brief present on disk — its changelog must be excluded
    (briefs / "Prediction Markets Weekly.md").write_text(
        "---\ntitle: Prediction Markets Weekly\n---\n# held\n\n## Changelog\n\n"
        "- 2026-06-20 — held theme cycle.\n",
        encoding="utf-8",
    )
    (root / "sources").mkdir()
    (root / "sources" / "registry.json").write_text(json.dumps(_REGISTRY), encoding="utf-8")


def _wire_paths(root: Path) -> None:
    vault = root / "vault"
    build_log._VAULT = vault
    build_log._SOURCES_DIR = vault / "01 Sources"
    build_log._BRIEFS_DIR = vault / "02 Briefs"
    build_log._REGISTRY = root / "sources" / "registry.json"
    build_log._LOG = vault / "log.md"


def test_render_structure_newest_first(tmp_path: Path) -> None:
    _make_vault(tmp_path)
    _wire_paths(tmp_path)
    out = build_log.render()

    assert out.startswith("# azimuth — Bundle Log")
    headings = re.findall(r"^## (\d{4}-\d{2}-\d{2})$", out, flags=re.MULTILINE)
    assert headings == ["2026-06-20", "2026-06-18"]  # newest first


def test_held_theme_excluded(tmp_path: Path) -> None:
    _make_vault(tmp_path)
    _wire_paths(tmp_path)
    out = build_log.render()

    # held theme leaks nowhere: not in an ingest line, not as a brief, not as a changelog
    assert "prediction" not in out.lower()
    # each ingest line counts only the single non-held source note
    assert "1 L1 source note: fuel-prices." in out
    # the surfaced brief's changelog text is present
    assert "**Energy Supply Weekly** — first cycle" in out
    # multi-line changelog entries are collapsed onto one line
    assert "storage advanced one week on the continuation line." in out


def test_idempotent_write_and_check(tmp_path: Path) -> None:
    _make_vault(tmp_path)
    _wire_paths(tmp_path)

    first = build_log.render()
    build_log._LOG.write_text(first, encoding="utf-8")
    # re-render of the unchanged bundle is byte-identical
    assert build_log.render() == first
    # and the file on disk equals the freshly rendered output (what --check verifies)
    assert build_log._LOG.read_text(encoding="utf-8") == build_log.render()
