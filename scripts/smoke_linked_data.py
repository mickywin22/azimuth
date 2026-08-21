#!/usr/bin/env python3
"""Live Playwright smoke for the linked-data explorer (Azimuth KR1 explorable-surface gate).

Serves the built ``site/`` over a local HTTP server, opens ``linked-data.html`` in a real
Chromium, and proves the RDF concept explorer works end-to-end — the browser-render gate the
token-presence unit tests can't reach:

  1. the stat tiles + ontology panel render (the self-describing schema layer: 3 classes,
     10 typed properties);
  2. filtering by an OKF layer class narrows the concept list to that class;
  3. opening a concept renders its **typed triples** and its ``rests-on`` edges;
  4. clicking a ``rests-on`` edge **traverses** to the linked concept (the graph is walkable,
     not a static list) — the indispensable-layer move a flat OKF bundle can't offer;
  5. the cross-brief bridges section renders (a shared L1 source two briefs both rest on).

Screenshots are written to ``_smoke/``; the overview + a concept-detail shot are copied into
``docs/proof/`` by the caller (the graph/whatif proof convention). Exit code 0 = pass.

Usage:  python scripts/smoke_linked_data.py
"""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SITE = _REPO_ROOT / "site"
_SHOTS = _REPO_ROOT / "_smoke"


def _serve(directory: Path) -> tuple[socketserver.TCPServer, int]:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def main() -> int:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")
    if not (_SITE / "linked-data.html").is_file():
        print(
            "FAIL: site/linked-data.html not built — run scripts/build_linked_data.py first",
            file=sys.stderr,
        )
        return 1
    _SHOTS.mkdir(exist_ok=True)
    httpd, port = _serve(_SITE)
    url = f"http://127.0.0.1:{port}/linked-data.html"
    failures: list[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1100, "height": 900})
            page.goto(url, wait_until="networkidle")

            # 1) stat tiles + ontology (schema) panel -------------------------------------
            n_tiles = page.locator("#tiles .tile").count()
            if n_tiles < 4:
                failures.append(f"expected >=4 stat tiles, found {n_tiles}")
            page.click("#schema > summary")  # open the ontology panel for the shot
            page.wait_for_timeout(150)
            n_classes = page.locator("#schema-body .classrow").count()
            n_props = page.locator("#schema-body table.props tbody tr").count()
            print(f"ontology: {n_classes} classes, {n_props} properties")
            if n_classes != 3:
                failures.append(f"ontology should list the 3 OKF layer classes, found {n_classes}")
            if n_props != 10:
                failures.append(f"ontology should list the 10 typed properties, found {n_props}")
            page.screenshot(path=str(_SHOTS / "linked-data-overview.png"), full_page=False)

            # 2) filter by class narrows the list -----------------------------------------
            total_cards = page.locator("#clist .card").count()
            # click the L2-brief filter button (its label starts "L2-brief")
            page.click("#filters .fbtn:has-text('L2-brief')")
            page.wait_for_timeout(150)
            brief_cards = page.locator("#clist .card").count()
            print(f"concepts: {total_cards} total, {brief_cards} after L2-brief filter")
            if not 0 < brief_cards < total_cards:
                failures.append(
                    f"class filter did not narrow the list (total={total_cards}, briefs={brief_cards})"
                )
            chips = page.locator("#clist .card .chip").all_inner_texts()
            if any(c.strip() != "L2-brief" for c in chips):
                failures.append(f"L2-brief filter left a non-brief card: {chips}")

            # 3) open a concept -> typed triples + rests-on edges -------------------------
            page.click("#clist .card:first-child")
            page.wait_for_timeout(150)
            n_triples = page.locator("#detail table.triples tbody tr").count()
            n_edges = page.locator("#detail .edge").count()
            title = page.locator("#detail h2").inner_text().strip()
            print(f"opened concept {title!r}: {n_triples} typed triples, {n_edges} edges")
            if n_triples < 1:
                failures.append(f"concept {title!r} rendered no typed triples")
            if n_edges < 1:
                failures.append(f"brief {title!r} rendered no rests-on edges")
            page.screenshot(path=str(_SHOTS / "linked-data-concept.png"), full_page=False)

            # 4) traverse a rests-on edge to the linked concept --------------------------
            edge_label = page.locator("#detail .edge button").first.inner_text().strip()
            page.locator("#detail .edge button").first.click()
            page.wait_for_timeout(150)
            new_title = page.locator("#detail h2").inner_text().strip()
            print(f"traversed edge -> {new_title!r}")
            if new_title == title:
                failures.append("clicking a rests-on edge did not traverse to a new concept")
            target_label = edge_label.split("[")[0].strip()  # drop the " [L1-source]" class tag
            if target_label and target_label not in new_title:
                failures.append(f"edge target {target_label!r} did not open concept {new_title!r}")

            # 5) cross-brief bridges render ----------------------------------------------
            n_bridges = page.locator("#bridges .bridge").count()
            print(f"cross-brief bridges rendered: {n_bridges}")
            if n_bridges < 1:
                failures.append("no cross-brief bridge rendered (USP surface missing)")

            # mobile: the two-column layout collapses + nav burger appears ---------------
            mpage = browser.new_context(
                viewport={"width": 390, "height": 780}, has_touch=True, is_mobile=True
            ).new_page()
            mpage.goto(url, wait_until="networkidle")
            mpage.wait_for_timeout(300)
            if mpage.locator("#clist .card").count() < 1:
                failures.append("no concept cards on a 390px viewport")
            mpage.screenshot(path=str(_SHOTS / "linked-data-mobile.png"), full_page=False)

            browser.close()
    finally:
        httpd.shutdown()

    if failures:
        print("\nSMOKE FAIL:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(
        f"\nSMOKE PASS — explorer renders, filters, opens + traverses concepts; shots in {_SHOTS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
