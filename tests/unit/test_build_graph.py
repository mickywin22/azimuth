"""Tests for the cross-channel knowledge-graph builder (scripts/build_graph.py).

The load-bearing guarantee: the graph is CROSS-channel. A shared entity that the live
data mentions under two different themes must produce a node that bridges both themes,
with the connecting edges flagged ``cross_theme: true``. That is the visible proof the
demonstrator rests on, so it gets a regression test.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "build_graph", _REPO_ROOT / "scripts" / "build_graph.py"
)
assert _spec and _spec.loader
build_graph_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_graph_mod)

_REGISTRY = {
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
        {
            "key": "fuel-prices",
            "theme": "energy-supply",
            "surfaced": True,
            "upstream_source": "WorldMonitor fuel-price feed",
        },
        {
            "key": "earthquakes",
            "theme": "geophysical",
            "surfaced": True,
            "upstream_source": "USGS",
        },
        {"key": "prediction-markets", "theme": "prediction-markets", "surfaced": True},
    ],
}


def _make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "02 Briefs").mkdir(parents=True)
    (vault / "02 Briefs" / "Energy Supply Weekly.md").write_text(
        "---\ntitle: Energy Supply Weekly\ntheme: energy-supply\n---\n"
        "# Energy Supply Weekly\nGerman diesel and the EU panel ([[fuel-prices]]).\n",
        encoding="utf-8",
    )
    (vault / "02 Briefs" / "Geophysical Weekly.md").write_text(
        "---\ntitle: Geophysical Weekly\ntheme: geophysical\n---\n"
        "# Geophysical Weekly\nA quake near Palu, Indonesia ([[earthquakes]]).\n",
        encoding="utf-8",
    )
    d = vault / "01 Sources" / "2026-06-23"
    d.mkdir(parents=True)
    # "Greece" appears under BOTH themes -> a genuine cross-theme bridge.
    (d / "fuel-prices.md").write_text(
        "---\nsource: Fuel prices\n---\n# Fuel\nPump panel: Germany, France, Greece, Mexico.\n",
        encoding="utf-8",
    )
    (d / "earthquakes.md").write_text(
        "---\nsource: USGS\n---\n# Quakes\nEvents recorded off Indonesia, Japan and Greece.\n",
        encoding="utf-8",
    )
    (d / "prediction-markets.md").write_text(
        "---\nsource: Polymarket\n---\n# PM\nA market mentioning Greece.\n", encoding="utf-8"
    )
    return vault


def _build(tmp_path: Path) -> dict:
    vault = _make_vault(tmp_path)
    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    return build_graph_mod.build_graph(vault_dir=vault, registry_path=reg)


def test_cross_theme_edge_exists(tmp_path: Path) -> None:
    """ACCEPTANCE: graph.json has >=1 edge flagged cross_theme that joins two themes."""
    graph = _build(tmp_path)
    cross = [e for e in graph["edges"] if e.get("cross_theme")]
    assert cross, "no cross-theme edges were generated"

    # the cross edges must originate from a shared-entity node spanning >=2 themes
    entities = {n["id"]: n for n in graph["nodes"] if n["kind"] == "entity"}
    assert entities, "no shared-entity nodes were generated"
    bridge = next(n for n in entities.values() if len(n.get("themes", [])) >= 2)
    assert "energy-supply" in bridge["themes"]
    assert "geophysical" in bridge["themes"]

    # every cross edge connects that entity to a brief of one of its themes
    brief_ids = {n["id"]: n for n in graph["nodes"] if n["kind"] == "brief"}
    for e in cross:
        assert e["source"] in entities
        assert e["target"] in brief_ids


def test_held_theme_excluded_from_graph(tmp_path: Path) -> None:
    """A held theme contributes no brief, source, or entity edge — even if it shares a name."""
    graph = _build(tmp_path)
    themes_present = {n["theme"] for n in graph["nodes"] if n["kind"] in ("brief", "source")}
    assert "prediction-markets" not in themes_present
    # the shared entity must bridge only the two surfaced themes, never the held one
    for n in graph["nodes"]:
        if n["kind"] == "entity":
            assert "prediction-markets" not in n["themes"]


def test_within_theme_edges_not_flagged_cross(tmp_path: Path) -> None:
    """brief -> source structural edges stay cross_theme: false."""
    graph = _build(tmp_path)
    src_ids = {n["id"] for n in graph["nodes"] if n["kind"] == "source"}
    within = [e for e in graph["edges"] if e["target"] in src_ids]
    assert within, "expected within-theme brief->source edges"
    assert all(e["cross_theme"] is False for e in within)
