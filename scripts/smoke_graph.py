#!/usr/bin/env python3
"""Live smoke for the knowledge-graph layer (Azimuth KR-B acceptance gate).

KR-B's done-criterion asks for a queryable OR visually rendered graph on real
ingested L1, with at least one cross-source relation demonstrated, plus a
``smoke/screenshot``. ``smoke_whatif.py`` already covers the what-if proof on
``answers.html``; this is its sibling for the *graph* half — it proves both
halves of the KG layer end-to-end against the committed ``site/graph.json``:

  1. QUERYABLE half (pure, no browser) — the ``query_graph.py`` engine answers
     over the live graph: headline stats, the typed-relation breakdown, the
     flagship cross-channel ``connect`` (energy-supply <-> geophysical must
     surface >=1 evidence-ranked bridge), the bridge roster, and the hubs.
  2. VISUAL half (real Chromium) — ``graph.html`` renders the canvas, the Trace
     control is populated with channels, and tracing two channels writes a
     real "shared bridge(s)" answer into ``#qout``. Screenshots of the default
     and traced states are banked to ``_smoke/`` so the visual proof exists.

Exit code 0 = pass. Run:  python scripts/smoke_graph.py
"""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SITE = _REPO_ROOT / "site"
_SHOTS = _REPO_ROOT / "_smoke"

sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import query_graph as qg  # noqa: E402

# The flagship cross-source pair the KR exists to demonstrate. Both channels are
# clean (non-held) and the live graph records shared bridge regions between them.
_CONNECT_A = "energy-supply"
_CONNECT_B = "geophysical"


def _serve(directory: Path) -> tuple[socketserver.TCPServer, int]:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def _smoke_queryable(failures: list[str]) -> None:
    """The query engine answers over the live graph (no browser)."""
    graph = qg.load_graph()

    st = qg.stats(graph)
    print(f"stats        : {st['nodes']} nodes / {st['edges']} edges")
    if st["nodes"] < 1 or st["edges"] < 1:
        failures.append("graph is empty (0 nodes or 0 edges)")

    rels = qg.relation_counts(graph)
    print(f"relations    : {', '.join(f'{k}={v}' for k, v in sorted(rels.items())) or '(none)'}")
    if not rels:
        failures.append("no typed relations on the graph (untyped edges)")

    a = qg.resolve_theme(graph, _CONNECT_A)
    b = qg.resolve_theme(graph, _CONNECT_B)
    if not a or not b:
        failures.append(f"flagship channels not in graph: {_CONNECT_A}={a} {_CONNECT_B}={b}")
    else:
        conn = qg.connect_themes(graph, a, b)
        n_bridges = len(conn.get("bridges", []))
        top = conn["bridges"][0] if n_bridges else None
        top_label = top.get("label") if top else "(none)"
        print(
            f"connect      : {_CONNECT_A} <-> {_CONNECT_B} -> {n_bridges} bridge(s), strongest {top_label!r}"
        )
        if n_bridges < 1:
            failures.append(
                f"flagship connect {_CONNECT_A}<->{_CONNECT_B} found NO cross-source bridge"
            )
        # Evidence ranking must be present (the indispensable-layer angle).
        if top is not None and "evidence" not in top:
            failures.append("connect bridges carry no evidence block (ranking lost)")

    br = qg.bridge_entities(graph)
    print(f"bridges      : {len(br)} cross-channel bridge entit(ies)")
    if not br:
        failures.append("no cross-channel bridge entities (graph not cross-source)")

    hubs = qg.hubs(graph, top=5)
    pretty = ", ".join(f"{qg._label(qg.node_index(graph), nid)}({d})" for nid, d in hubs)
    print(f"hubs (top 5) : {pretty or '(none)'}")
    if not hubs:
        failures.append("no hubs returned")


def _smoke_visual(failures: list[str]) -> None:
    """graph.html renders + the Trace control answers in a real browser."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        failures.append("playwright not installed — cannot run the visual half")
        return

    _SHOTS.mkdir(exist_ok=True)
    httpd, port = _serve(_SITE)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 960, "height": 1000})
            page.goto(f"http://127.0.0.1:{port}/graph.html", wait_until="networkidle")

            if not page.locator("#g").is_visible():
                failures.append("graph canvas #g not visible")

            qa, qb = page.locator("#qa"), page.locator("#qb")
            if qa.locator("option").count() < 2 or qb.locator("option").count() < 2:
                failures.append("Trace channel selects not populated with >=2 channels")

            page.screenshot(path=str(_SHOTS / "graph-default.png"), full_page=True)

            # Trace the flagship pair (fall back to first two distinct channels).
            try:
                qa.select_option(_CONNECT_A)
                qb.select_option(_CONNECT_B)
            except Exception:
                opts = qa.locator("option").all()
                qa.select_option(index=0)
                qb.select_option(index=min(1, len(opts) - 1))
            page.locator("#qgo").click()
            page.wait_for_timeout(200)

            out = page.locator("#qout").inner_text().strip()
            print(f"trace #qout  : {out!r}")
            if "bridge" not in out.lower():
                failures.append(f"Trace produced no bridge answer (#qout={out!r})")

            page.screenshot(path=str(_SHOTS / "graph-traced.png"), full_page=True)
            browser.close()
    finally:
        httpd.shutdown()


def main() -> int:
    # Bridge labels carry non-ASCII (e.g. the "<->" glyph); keep the console safe
    # on Windows cp1252 so a print can't fail the smoke after the work passed.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")

    if not (_SITE / "graph.json").is_file():
        print("FAIL: site/graph.json missing — run scripts/build_graph.py first", file=sys.stderr)
        return 1
    if not (_SITE / "graph.html").is_file():
        print("FAIL: site/graph.html missing — run scripts/build_graph.py first", file=sys.stderr)
        return 1

    failures: list[str] = []
    print("== queryable half (query_graph.py over live graph.json) ==")
    _smoke_queryable(failures)
    print("\n== visual half (graph.html Trace control in Chromium) ==")
    _smoke_visual(failures)

    if failures:
        print("\nKG SMOKE FAIL:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"\nKG SMOKE PASS — graph queryable + visually traced; screenshots in {_SHOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
