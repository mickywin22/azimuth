"""Tests for the knowledge-graph query layer (scripts/query_graph.py).

The load-bearing guarantee: the graph is not just *visible* but *answerable*. Given two
channels that the live data joins through a shared region, ``connect_themes`` must return
that bridge and a path between the two briefs — the deterministic, data-backed answer to
*"what connects energy supply to geophysical activity?"*. Traversal is undirected and the
chosen path is deterministic, so both get regression tests.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "query_graph", _REPO_ROOT / "scripts" / "query_graph.py"
)
assert _spec and _spec.loader
qg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qg)


def _graph() -> dict[str, list[dict[str, Any]]]:
    """A small, self-contained graph mirroring the real builder's shape.

    Energy and Geophysical are bridged by a shared region (Greece); Energy also carries a
    single-theme commodity (WTI). This is the minimal structure the cross-channel queries
    must handle.
    """
    return {
        "nodes": [
            {
                "id": "concept:energy-supply",
                "label": "Energy Supply",
                "kind": "concept",
                "theme": "energy-supply",
            },
            {
                "id": "concept:geophysical",
                "label": "Geophysical",
                "kind": "concept",
                "theme": "geophysical",
            },
            {
                "id": "brief:energy-supply-weekly",
                "label": "Energy Supply Weekly",
                "kind": "brief",
                "theme": "energy-supply",
            },
            {
                "id": "brief:geophysical-weekly",
                "label": "Geophysical Weekly",
                "kind": "brief",
                "theme": "geophysical",
            },
            {
                "id": "source:fuel-prices",
                "label": "Fuel prices",
                "kind": "source",
                "theme": "energy-supply",
            },
            {
                "id": "source:earthquakes",
                "label": "USGS",
                "kind": "source",
                "theme": "geophysical",
            },
            {
                "id": "entity:greece",
                "label": "Greece",
                "kind": "entity",
                "entity_kind": "region",
                "theme": "shared",
                "themes": ["energy-supply", "geophysical"],
            },
            {
                "id": "entity:wti",
                "label": "WTI",
                "kind": "entity",
                "entity_kind": "commodity",
                "theme": "energy-supply",
                "themes": ["energy-supply"],
            },
        ],
        "edges": [
            {
                "source": "concept:energy-supply",
                "target": "brief:energy-supply-weekly",
                "cross_theme": False,
            },
            {
                "source": "concept:geophysical",
                "target": "brief:geophysical-weekly",
                "cross_theme": False,
            },
            {
                "source": "brief:energy-supply-weekly",
                "target": "source:fuel-prices",
                "cross_theme": False,
            },
            {
                "source": "brief:geophysical-weekly",
                "target": "source:earthquakes",
                "cross_theme": False,
            },
            {
                "source": "entity:greece",
                "target": "brief:energy-supply-weekly",
                "cross_theme": True,
            },
            {"source": "entity:greece", "target": "brief:geophysical-weekly", "cross_theme": True},
            {"source": "entity:wti", "target": "brief:energy-supply-weekly", "cross_theme": False},
        ],
    }


def test_adjacency_is_undirected() -> None:
    adj = qg.adjacency(_graph())
    assert "brief:energy-supply-weekly" in adj["entity:greece"]
    assert "entity:greece" in adj["brief:energy-supply-weekly"]


def test_shortest_path_bridges_two_themes_via_shared_region() -> None:
    g = _graph()
    path = qg.shortest_path(g, "brief:energy-supply-weekly", "brief:geophysical-weekly")
    assert path == [
        "brief:energy-supply-weekly",
        "entity:greece",
        "brief:geophysical-weekly",
    ]


def test_shortest_path_none_for_unknown_or_disconnected() -> None:
    g = _graph()
    assert qg.shortest_path(g, "brief:energy-supply-weekly", "nope") is None
    assert qg.shortest_path(g, "x", "y") is None


def test_shortest_path_same_node() -> None:
    g = _graph()
    assert qg.shortest_path(g, "entity:greece", "entity:greece") == ["entity:greece"]


def test_connect_themes_returns_bridge_and_path() -> None:
    g = _graph()
    res = qg.connect_themes(g, "energy-supply", "geophysical")
    bridge_ids = [n["id"] for n in res["bridges"]]
    assert bridge_ids == ["entity:greece"]  # WTI is single-theme, not a bridge
    assert res["path"] == [
        "brief:energy-supply-weekly",
        "entity:greece",
        "brief:geophysical-weekly",
    ]


def test_connect_themes_unknown_theme_is_empty() -> None:
    res = qg.connect_themes(_graph(), "energy-supply", "does-not-exist")
    assert res["bridges"] == []
    assert res["path"] is None


def test_bridge_entities_sorted_richest_first() -> None:
    bridges = qg.bridge_entities(_graph())
    assert [n["label"] for n in bridges] == ["Greece"]  # only multi-theme entity


def test_hubs_ranks_the_busiest_brief_first() -> None:
    # Energy brief touches concept + source + greece + wti = degree 4, the busiest node.
    top = qg.hubs(_graph(), top=1)
    assert top[0][0] == "brief:energy-supply-weekly"
    assert top[0][1] == 4


def test_resolve_node_by_label_theme_and_substring() -> None:
    g = _graph()
    assert qg.resolve_node(g, "Greece") == "entity:greece"
    assert qg.resolve_node(g, "geophysical") == "concept:geophysical"
    assert qg.resolve_node(g, "fuel") == "source:fuel-prices"
    assert qg.resolve_node(g, "totally-absent") is None


def test_resolve_theme_accepts_partial() -> None:
    g = _graph()
    assert qg.resolve_theme(g, "energy") == "energy-supply"
    assert qg.resolve_theme(g, "geophysical") == "geophysical"
    assert qg.resolve_theme(g, "nope") is None


def test_stats_counts(tmp_path: Path) -> None:
    s = qg.stats(_graph())
    assert s["nodes"] == 8
    assert s["briefs"] == 2
    assert s["bridges"] == 1
    assert s["cross_theme_edges"] == 2


def test_load_graph_reads_committed_json(tmp_path: Path) -> None:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_graph()), encoding="utf-8")
    g = qg.load_graph(p)
    assert len(g["nodes"]) == 8
