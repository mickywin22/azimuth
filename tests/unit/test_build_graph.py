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
        "---\nsource: Fuel prices\n---\n# Fuel\nPump panel: Germany, France, Greece, "
        "Mexico. Brent and WTI benchmarks softened.\n",
        encoding="utf-8",
    )
    (d / "earthquakes.md").write_text(
        "---\nsource: USGS\n---\n# Quakes\nEvents recorded off Indonesia, Japan and Greece.\n\n"
        '| earthquakes | [{"id": "q1", "magnitude": 6.5, "place": "5 km S of Athens, Greece"}, '
        '{"id": "q2", "magnitude": 5.2, "place": "Off Japan"}] |\n',
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


def test_concept_nodes_present(tmp_path: Path) -> None:
    """RICHER: a concept (channel) node per surfaced theme feeds its brief (spine top)."""
    graph = _build(tmp_path)
    concepts = {n["id"]: n for n in graph["nodes"] if n["kind"] == "concept"}
    assert "concept:energy-supply" in concepts
    assert "concept:geophysical" in concepts
    # held theme never gets a concept node
    assert "prediction-markets" not in {n["theme"] for n in concepts.values()}
    briefs = {n["id"] for n in graph["nodes"] if n["kind"] == "brief"}
    for cid in concepts:
        assert any(
            e["source"] == cid and e["target"] in briefs and e["cross_theme"] is False
            for e in graph["edges"]
        ), f"concept {cid} is not wired to a brief"


def test_commodity_entity_single_theme(tmp_path: Path) -> None:
    """RICHER: commodities surface even when confined to one theme (per-channel texture)."""
    graph = _build(tmp_path)
    comms = [n for n in graph["nodes"] if n.get("entity_kind") == "commodity"]
    assert comms, "expected commodity entity nodes"
    brent = next((n for n in comms if n["label"].lower() == "brent"), None)
    assert brent is not None, "Brent should surface as a commodity entity"
    assert brent["theme"] == "energy-supply"
    # a single-theme commodity edge is within-theme, never a cross-theme bridge
    edge = next(e for e in graph["edges"] if e["source"] == brent["id"])
    assert edge["cross_theme"] is False


def test_event_nodes_from_quakes(tmp_path: Path) -> None:
    """RICHER: the largest live earthquakes become event entity nodes (events layer)."""
    graph = _build(tmp_path)
    events = [n for n in graph["nodes"] if n.get("entity_kind") == "event"]
    assert events, "expected earthquake event entity nodes"
    top = events[0]  # nodes are appended largest-magnitude first
    assert top["kind"] == "entity"
    assert top["label"].startswith("M6.5")
    geo_brief = "brief:" + build_graph_mod._slug("Geophysical Weekly")
    assert any(e["source"] == top["id"] and e["target"] == geo_brief for e in graph["edges"]), (
        "event is not wired to the geophysical brief"
    )
    # the Athens quake links to the surfaced Greece region entity (event -> region)
    greece = "entity:" + build_graph_mod._slug("Greece")
    assert any(e["source"] == top["id"] and e["target"] == greece for e in graph["edges"]), (
        "event did not link to the region it occurred in"
    )


def test_every_edge_is_typed_with_a_known_relation(tmp_path: Path) -> None:
    """RICHER: every edge carries a ``rel`` from the fixed vocabulary (no untyped edges)."""
    graph = _build(tmp_path)
    known = {"has-brief", "rests-on", "mentioned-in", "named-in", "reported-in", "located-in"}
    assert graph["edges"], "expected edges"
    for e in graph["edges"]:
        assert e.get("rel") in known, f"edge missing/unknown rel: {e}"
    # the spine relations are present
    rels = {e["rel"] for e in graph["edges"]}
    assert {"has-brief", "rests-on", "mentioned-in"} <= rels


def test_mentioned_in_edges_carry_a_source_weight(tmp_path: Path) -> None:
    """RICHER: entity->brief edges carry weight = count of backing L1 source notes."""
    graph = _build(tmp_path)
    # Greece is named in the fuel-prices L1 note under energy-supply -> weight >= 1.
    greece = "entity:" + build_graph_mod._slug("Greece")
    energy = "brief:" + build_graph_mod._slug("Energy Supply Weekly")
    edge = next(e for e in graph["edges"] if e["source"] == greece and e["target"] == energy)
    assert edge["rel"] == "mentioned-in"
    assert edge["weight"] >= 1
    # every mentioned-in edge has an integer weight; spine/event edges never do
    for e in graph["edges"]:
        if e["rel"] == "mentioned-in":
            assert isinstance(e.get("weight"), int)
        else:
            assert "weight" not in e


def test_event_edges_use_reported_and_located_relations(tmp_path: Path) -> None:
    """RICHER: an earthquake is ``reported-in`` the geo brief and ``located-in`` a region."""
    graph = _build(tmp_path)
    geo = "brief:" + build_graph_mod._slug("Geophysical Weekly")
    greece = "entity:" + build_graph_mod._slug("Greece")
    events = [n["id"] for n in graph["nodes"] if n.get("entity_kind") == "event"]
    assert events
    assert any(
        e["source"] in events and e["target"] == geo and e["rel"] == "reported-in"
        for e in graph["edges"]
    )
    assert any(
        e["source"] in events and e["target"] == greece and e["rel"] == "located-in"
        for e in graph["edges"]
    )


def test_named_in_edges_link_entity_to_the_l1_source(tmp_path: Path) -> None:
    """RICHER: an entity gets a ``named-in`` edge to each L1 source note that names it.

    The graph must reach the L1 sources, not just the briefs: Greece is named in the
    fuel-prices L1 note, so a Greece -> source:fuel-prices edge exists.
    """
    graph = _build(tmp_path)
    greece = "entity:" + build_graph_mod._slug("Greece")
    fuel_src = "source:fuel-prices"
    named = [
        e
        for e in graph["edges"]
        if e["source"] == greece and e["rel"] == "named-in" and e["target"] == fuel_src
    ]
    assert named, "Greece should be named-in the fuel-prices L1 source note"
    e = named[0]
    assert e["cross_theme"] is False
    assert "weight" not in e  # the per-source unit; weight lives on mentioned-in only


def test_named_in_edge_count_matches_mentioned_in_weight(tmp_path: Path) -> None:
    """RICHER: a mentioned-in weight N is backed by exactly N named-in edges in that theme.

    The weight is a count; ``named-in`` is the provenance it counts — they must agree.
    """
    graph = _build(tmp_path)
    src_theme = {n["id"]: n.get("theme") for n in graph["nodes"] if n["kind"] == "source"}
    for me in graph["edges"]:
        if me["rel"] != "mentioned-in":
            continue
        entity, brief = me["source"], me["target"]
        theme = next(n["theme"] for n in graph["nodes"] if n["id"] == brief)
        named_in_theme = [
            e
            for e in graph["edges"]
            if e["source"] == entity
            and e["rel"] == "named-in"
            and src_theme.get(e["target"]) == theme
        ]
        assert len(named_in_theme) == me["weight"], (
            f"{entity} -> {theme}: weight {me['weight']} but {len(named_in_theme)} named-in edges"
        )


def test_named_in_edges_only_target_real_source_nodes(tmp_path: Path) -> None:
    """RICHER: every named-in edge points at a source node that actually exists."""
    graph = _build(tmp_path)
    source_ids = {n["id"] for n in graph["nodes"] if n["kind"] == "source"}
    named = [e for e in graph["edges"] if e["rel"] == "named-in"]
    assert named, "expected named-in provenance edges"
    for e in named:
        assert e["target"] in source_ids, f"named-in edge points at a non-source: {e}"


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


def test_check_passes_when_committed_artifacts_fresh(tmp_path: Path) -> None:
    """GUARD: --check returns [] when site/graph.{json,html} match a fresh build.

    Mirrors the brief-index sync guard: a freshly written graph dir is, by definition,
    in sync with the same vault, so check() reports nothing stale.
    """
    vault = _make_vault(tmp_path)
    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    out = tmp_path / "site"
    build_graph_mod.build(out, vault_dir=vault, registry_path=reg)
    stale = build_graph_mod.check(out, vault_dir=vault, registry_path=reg)
    assert stale == [], f"freshly built graph reported stale: {stale}"


def test_check_detects_stale_json(tmp_path: Path) -> None:
    """GUARD: an out-of-date committed graph.json is flagged by --check."""
    vault = _make_vault(tmp_path)
    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    out = tmp_path / "site"
    build_graph_mod.build(out, vault_dir=vault, registry_path=reg)
    # Simulate a vault/brief edit that was committed WITHOUT regenerating the graph.
    (out / "graph.json").write_text('{"nodes": [], "edges": []}\n', encoding="utf-8")
    stale = build_graph_mod.check(out, vault_dir=vault, registry_path=reg)
    assert "graph.json" in stale


def test_check_detects_missing_artifact(tmp_path: Path) -> None:
    """GUARD: a never-built (missing) graph.html is reported stale, not crashed on."""
    vault = _make_vault(tmp_path)
    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    out = tmp_path / "site"
    build_graph_mod.build(out, vault_dir=vault, registry_path=reg)
    (out / "graph.html").unlink()
    stale = build_graph_mod.check(out, vault_dir=vault, registry_path=reg)
    assert "graph.html" in stale


def test_gazetteer_includes_live_backed_bridge_regions() -> None:
    """GUARD (2026-06-27 coverage audit): the regions proven present in the live
    clean-theme corpus that BRIDGE >=2 themes must stay in the gazetteer.

    Each of these was whole-word present in the latest live L1/L2 text under two
    distinct clean themes, but was missing from the curated gazetteer, so its
    cross-theme bridge was being silently dropped. They are pinned here so a future
    gazetteer trim cannot drop a real bridge without a test going red.
    """
    for region in ("Venezuela", "California", "Ukraine", "Papua New Guinea"):
        assert region in build_graph_mod._REGIONS, f"{region} dropped from gazetteer"


def test_newly_added_region_bridges_two_themes(tmp_path: Path) -> None:
    """ACCEPTANCE: a region added in the coverage audit (Venezuela) becomes a
    cross-theme bridge node when the live data names it under two clean themes.

    Before the gazetteer addition the scanner could not see Venezuela at all, so
    no bridge could form however often the feeds named it. This proves the new
    entry is wired end-to-end, not just listed.
    """
    vault = tmp_path / "vault"
    (vault / "02 Briefs").mkdir(parents=True)
    (vault / "02 Briefs" / "Energy Supply Weekly.md").write_text(
        "---\ntitle: Energy Supply Weekly\ntheme: energy-supply\n---\n"
        "# Energy Supply Weekly\nCrude exports from Venezuela ([[fuel-prices]]).\n",
        encoding="utf-8",
    )
    (vault / "02 Briefs" / "Geophysical Weekly.md").write_text(
        "---\ntitle: Geophysical Weekly\ntheme: geophysical\n---\n"
        "# Geophysical Weekly\nA shallow quake near Yumare, Venezuela ([[earthquakes]]).\n",
        encoding="utf-8",
    )
    d = vault / "01 Sources" / "2026-06-27"
    d.mkdir(parents=True)
    (d / "fuel-prices.md").write_text(
        "---\nsource: Fuel prices\n---\n# Fuel\nVenezuela crude grade and the EU panel.\n",
        encoding="utf-8",
    )
    (d / "earthquakes.md").write_text(
        "---\nsource: USGS\n---\n# Quakes\nEvents recorded near Venezuela.\n\n"
        '| earthquakes | [{"id": "q1", "magnitude": 7.5, "place": "10 km N of Yumare, '
        'Venezuela"}] |\n',
        encoding="utf-8",
    )
    reg = tmp_path / "registry.json"
    reg.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    graph = build_graph_mod.build_graph(vault_dir=vault, registry_path=reg)

    bridges = [
        n
        for n in graph["nodes"]
        if n["kind"] == "entity"
        and "venezuela" in n["id"].lower()
        and len(n.get("themes", [])) >= 2
    ]
    assert bridges, "Venezuela did not form a cross-theme bridge node"
    themes = bridges[0]["themes"]
    assert "energy-supply" in themes and "geophysical" in themes


def test_rendered_html_wires_the_sota_viz_features(tmp_path: Path) -> None:
    """The rendered graph.html must carry the state-of-the-art viz features (KR-B).

    These are template-only behaviours (canvas + JS), invisible to the data-shape tests
    above, so they get their own presence guard: dropping any of them silently would
    regress the public visualization without failing another test.
    """
    graph = _build(tmp_path)
    html = build_graph_mod.render_html(graph)

    # 1) typed relation on hover + evidence-weighted edge thickness
    for token in ("hoverEdge", "pickEdge", "edgeText", "REL_LABEL", "e.weight"):
        assert token in html, f"edge-legibility token missing from graph.html: {token}"

    # 2) shareable deep links (Trace/Find -> URL, replayed on load) + copy-link button
    for token in ("applyHash", "writeHash", "hashchange", "qshare", "trace=", "node="):
        assert token in html, f"deep-link token missing from graph.html: {token}"

    # the graph JSON must be injected, not left as the placeholder
    assert "__GRAPH_JSON__" not in html
    assert '"nodes"' in html and '"edges"' in html
