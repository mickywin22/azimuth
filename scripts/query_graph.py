#!/usr/bin/env python3
"""Query the azimuth knowledge graph (``site/graph.json``).

The graph builder (``scripts/build_graph.py``) makes the cross-channel relationships
*visible*. This module makes them *queryable* — the second half of the KR's
"queryable/visual graph" goal. A static OKF bundle can publish briefs and source notes;
what it cannot do is answer *"show me everything connecting energy prices to geophysical
events"*. This module answers exactly that, deterministically, over the same data-backed
graph the site renders — no LLM, no inference.

It mirrors the HemySphere ``vault-graph`` skill (neighbours, shortest path, hubs) but
adds the cross-channel primitive azimuth is built to demonstrate: ``connect`` — given two
channels, return every shared entity that bridges them plus the shortest path joining
their briefs.

Edges are treated as **undirected** for traversal: the graph is a relationship map, and
"is energy connected to geophysical?" does not depend on which way an edge was written.

Usage:
    python scripts/query_graph.py stats
    python scripts/query_graph.py connect energy geophysical   # the flagship query
    python scripts/query_graph.py path "Greece" "Energy Supply"
    python scripts/query_graph.py neighbors geophysical
    python scripts/query_graph.py bridges
    python scripts/query_graph.py hubs --top 8
    python scripts/query_graph.py <any-cmd> --json            # machine-readable output
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRAPH = _REPO_ROOT / "site" / "graph.json"

Graph = dict[str, list[dict[str, Any]]]


# --- loading + indexing -----------------------------------------------------
def load_graph(path: Path = DEFAULT_GRAPH) -> Graph:
    """Load the graph JSON. Falls back to an in-memory build if no file is present."""
    if path.exists():
        data: Graph = json.loads(path.read_text(encoding="utf-8"))
        return data
    # No committed artifact (fresh checkout / CI before build): build in memory.
    from build_graph import build_graph

    return build_graph()


def node_index(graph: Graph) -> dict[str, dict[str, Any]]:
    """Map node id -> node dict."""
    return {n["id"]: n for n in graph["nodes"]}


def adjacency(graph: Graph) -> dict[str, set[str]]:
    """Undirected adjacency map: node id -> set of neighbouring node ids."""
    adj: dict[str, set[str]] = {n["id"]: set() for n in graph["nodes"]}
    for e in graph["edges"]:
        s, t = e["source"], e["target"]
        if s in adj and t in adj:
            adj[s].add(t)
            adj[t].add(s)
    return adj


# --- resolution: turn a user string into a node / theme ---------------------
def resolve_node(graph: Graph, term: str) -> str | None:
    """Resolve a user term to a node id (exact id > exact label > theme > substring)."""
    nodes = graph["nodes"]
    low = term.strip().lower()
    by_id = {n["id"]: n for n in nodes}
    if term in by_id:
        return term
    for n in nodes:  # exact label
        if str(n.get("label", "")).lower() == low:
            return str(n["id"])
    # exact theme on a concept/brief node (so "energy-supply" -> its concept)
    for kind in ("concept", "brief"):
        for n in nodes:
            if n.get("kind") == kind and str(n.get("theme", "")).lower() == low:
                return str(n["id"])
    # substring on label, then on id
    for n in nodes:
        if low in str(n.get("label", "")).lower():
            return str(n["id"])
    for n in nodes:
        if low in str(n["id"]).lower():
            return str(n["id"])
    return None


def resolve_theme(graph: Graph, term: str) -> str | None:
    """Resolve a user term to a theme key (matches concept/brief theme or label)."""
    low = term.strip().lower()
    concepts = [n for n in graph["nodes"] if n.get("kind") == "concept"]
    for n in concepts:  # exact theme key
        if str(n.get("theme", "")).lower() == low:
            return str(n["theme"])
    for n in concepts:  # label or substring (e.g. "energy" -> "energy-supply")
        if low in str(n.get("label", "")).lower() or low in str(n.get("theme", "")).lower():
            return str(n["theme"])
    return None


def theme_brief_id(graph: Graph, theme: str) -> str | None:
    """Return the brief node id for a theme, or ``None``."""
    for n in graph["nodes"]:
        if n.get("kind") == "brief" and n.get("theme") == theme:
            return str(n["id"])
    return None


# --- core graph queries -----------------------------------------------------
def neighbors(graph: Graph, node_id: str) -> list[str]:
    """Sorted neighbouring node ids of ``node_id``."""
    return sorted(adjacency(graph).get(node_id, set()))


def shortest_path(graph: Graph, src: str, dst: str) -> list[str] | None:
    """Breadth-first shortest path (list of node ids) from ``src`` to ``dst``.

    Returns ``None`` when either endpoint is unknown or no path exists. Neighbours are
    expanded in sorted order so the chosen path is deterministic across runs.
    """
    adj = adjacency(graph)
    if src not in adj or dst not in adj:
        return None
    if src == dst:
        return [src]
    prev: dict[str, str] = {src: src}
    q: deque[str] = deque([src])
    while q:
        cur = q.popleft()
        for nxt in sorted(adj[cur]):
            if nxt in prev:
                continue
            prev[nxt] = cur
            if nxt == dst:
                path = [dst]
                while path[-1] != src:
                    path.append(prev[path[-1]])
                return list(reversed(path))
            q.append(nxt)
    return None


def bridge_entities(graph: Graph) -> list[dict[str, Any]]:
    """Entity nodes that span >=2 themes (the cross-channel bridges), richest first."""
    out = [
        n for n in graph["nodes"] if n.get("kind") == "entity" and len(n.get("themes", [])) >= 2
    ]
    return sorted(out, key=lambda n: (-len(n.get("themes", [])), str(n.get("label", ""))))


def hubs(graph: Graph, top: int = 10) -> list[tuple[str, int]]:
    """The ``top`` most-connected node ids with their undirected degree."""
    adj = adjacency(graph)
    ranked = sorted(adj.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return [(nid, len(nbrs)) for nid, nbrs in ranked[:top]]


def connect_themes(graph: Graph, theme_a: str, theme_b: str) -> dict[str, Any]:
    """The flagship cross-channel query: how are two channels connected?

    Returns the shared **bridge entities** that touch both channels' briefs and the
    shortest path joining the two briefs. This is the legible, data-backed answer to
    *"what connects energy supply to geophysical activity?"*.
    """
    brief_a = theme_brief_id(graph, theme_a)
    brief_b = theme_brief_id(graph, theme_b)
    result: dict[str, Any] = {
        "theme_a": theme_a,
        "theme_b": theme_b,
        "brief_a": brief_a,
        "brief_b": brief_b,
        "bridges": [],
        "path": None,
    }
    if not brief_a or not brief_b:
        return result
    adj = adjacency(graph)
    idx = node_index(graph)
    a_nbrs, b_nbrs = adj.get(brief_a, set()), adj.get(brief_b, set())
    shared = a_nbrs & b_nbrs  # nodes adjacent to BOTH briefs
    bridges = [idx[nid] for nid in shared if idx.get(nid, {}).get("kind") == "entity"]
    result["bridges"] = sorted(
        bridges, key=lambda n: (n.get("entity_kind", ""), str(n.get("label", "")))
    )
    result["path"] = shortest_path(graph, brief_a, brief_b)
    return result


def stats(graph: Graph) -> dict[str, int]:
    """Headline counts for the graph."""
    nodes, edges = graph["nodes"], graph["edges"]

    def count(pred: Any) -> int:
        return sum(1 for n in nodes if pred(n))

    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "concepts": count(lambda n: n.get("kind") == "concept"),
        "briefs": count(lambda n: n.get("kind") == "brief"),
        "sources": count(lambda n: n.get("kind") == "source"),
        "entities": count(lambda n: n.get("kind") == "entity"),
        "bridges": len(bridge_entities(graph)),
        "cross_theme_edges": sum(1 for e in edges if e.get("cross_theme")),
    }


# --- CLI --------------------------------------------------------------------
def _label(idx: dict[str, dict[str, Any]], node_id: str) -> str:
    n = idx.get(node_id)
    return str(n.get("label", node_id)) if n else node_id


def _print_human(cmd: str, payload: Any, graph: Graph) -> None:
    idx = node_index(graph)
    if cmd == "stats":
        for k, v in payload.items():
            print(f"  {k:>18}: {v}")
    elif cmd == "neighbors":
        node_id, nbrs = payload
        print(f"{_label(idx, node_id)} ({node_id}) — {len(nbrs)} neighbour(s):")
        for nid in nbrs:
            print(f"  · {_label(idx, nid)}  [{nid}]")
    elif cmd == "path":
        if not payload:
            print("No path found.")
            return
        print(" -> ".join(_label(idx, nid) for nid in payload))
    elif cmd == "connect":
        a, b = payload["theme_a"], payload["theme_b"]
        bridges = payload["bridges"]
        if not bridges and not payload["path"]:
            print(f"No connection found between '{a}' and '{b}'.")
            return
        names = ", ".join(str(n.get("label", n["id"])) for n in bridges) or "none"
        print(f"{a} <-> {b}: {len(bridges)} shared bridge(s) — {names}")
        if payload["path"]:
            print("  path: " + " -> ".join(_label(idx, nid) for nid in payload["path"]))
    elif cmd == "bridges":
        print(f"{len(payload)} cross-channel bridge(s):")
        for n in payload:
            print(f"  · {n.get('label')} — {' <-> '.join(n.get('themes', []))}")
    elif cmd == "hubs":
        for nid, deg in payload:
            print(f"  {deg:>3}  {_label(idx, nid)}  [{nid}]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Query the azimuth knowledge graph.")
    parser.add_argument("--graph", default=str(DEFAULT_GRAPH), help="path to graph.json")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("stats", help="headline node/edge counts")
    p_nb = sub.add_parser("neighbors", help="direct neighbours of a node")
    p_nb.add_argument("term")
    p_pa = sub.add_parser("path", help="shortest path between two nodes")
    p_pa.add_argument("a")
    p_pa.add_argument("b")
    p_co = sub.add_parser("connect", help="how two channels are connected (flagship)")
    p_co.add_argument("a")
    p_co.add_argument("b")
    sub.add_parser("bridges", help="all cross-channel bridge entities")
    p_hu = sub.add_parser("hubs", help="most-connected nodes")
    p_hu.add_argument("--top", type=int, default=10)
    args = parser.parse_args(argv)

    graph = load_graph(Path(args.graph))
    payload: Any
    if args.cmd == "stats":
        payload = stats(graph)
    elif args.cmd == "neighbors":
        node_id = resolve_node(graph, args.term)
        if not node_id:
            print(f"Unknown node: {args.term!r}", file=sys.stderr)
            return 2
        payload = (node_id, neighbors(graph, node_id))
    elif args.cmd == "path":
        a, b = resolve_node(graph, args.a), resolve_node(graph, args.b)
        if not a or not b:
            print(f"Unknown node: {args.a!r} or {args.b!r}", file=sys.stderr)
            return 2
        payload = shortest_path(graph, a, b)
    elif args.cmd == "connect":
        ta, tb = resolve_theme(graph, args.a), resolve_theme(graph, args.b)
        if not ta or not tb:
            print(f"Unknown channel: {args.a!r} or {args.b!r}", file=sys.stderr)
            return 2
        payload = connect_themes(graph, ta, tb)
    elif args.cmd == "bridges":
        payload = bridge_entities(graph)
    elif args.cmd == "hubs":
        payload = hubs(graph, args.top)
    else:  # pragma: no cover — argparse 'required' guards this
        parser.error("no command")

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        _print_human(args.cmd, payload, graph)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
