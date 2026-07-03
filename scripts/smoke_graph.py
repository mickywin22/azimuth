#!/usr/bin/env python3
"""Live Playwright smoke for the knowledge-graph view (KR-B state-of-the-art viz gate).

Serves the built ``site/`` over a local HTTP server, opens ``graph.html`` in a real
Chromium, and proves the SOTA visualization works end-to-end — the browser-render gate
the token-presence unit tests can't reach:

  1. the canvas renders a non-blank graph (real pixels, not a frozen blank frame);
  2. the flagship queryable layer answers over the rendered graph — Trace
     ``energy-supply ↔ geophysical`` returns the evidence-ranked cross-source bridges
     (the indispensable-layer proof a static bundle cannot give), with every bridge
     labelled ``[N+M src]`` and the strongest bridge named (the evidence-rank mirror
     of ``query_graph.py connect``);
  3. mobile: on a touch device with a phone viewport the graph renders responsively,
     and a one-finger touch-drag actually pans the view (canvas pixels change).

Screenshots are written to ``_smoke/`` so the visual proof is banked. The desktop
overview + Trace shots are copied into ``docs/proof/`` by the caller (the whatif
convention). Exit code 0 = pass.

Usage:  python scripts/smoke_graph.py
"""

from __future__ import annotations

import functools
import http.server
import re
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SITE = _REPO_ROOT / "site"
_SHOTS = _REPO_ROOT / "_smoke"

# The Trace answer must join these two clean channels with at least one shared bridge
# region — the same energy↔geophysical link the CLI + docs advertise.
_TRACE_A = "energy-supply"
_TRACE_B = "geophysical"
_KNOWN_BRIDGES = ("Greece", "Mexico", "New Zealand")


def _serve(directory: Path) -> tuple[socketserver.TCPServer, int]:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def main() -> int:
    # The graph's Trace answer contains a "↔" — keep it printable on a legacy
    # (cp1252) Windows console; CI is already UTF-8.
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")
    if not (_SITE / "graph.html").is_file():
        print(
            "FAIL: site/graph.html not built — run scripts/build_graph.py first", file=sys.stderr
        )
        return 1
    _SHOTS.mkdir(exist_ok=True)
    httpd, port = _serve(_SITE)
    url = f"http://127.0.0.1:{port}/graph.html"
    failures: list[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()

            # --- desktop: render + queryable Trace ---------------------------------
            page = browser.new_page(viewport={"width": 1100, "height": 820})
            page.goto(url, wait_until="networkidle")

            canvas = page.locator("#g")
            if canvas.count() == 0:
                failures.append("no #g canvas in graph.html")
            else:
                box = canvas.bounding_box()
                if not box or box["width"] < 100 or box["height"] < 100:
                    failures.append(f"canvas has no real size: {box}")

            page.wait_for_timeout(1800)  # let the force layout settle before we look/shoot
            overview = _SHOTS / "graph-overview.png"
            canvas.screenshot(path=str(overview))
            if overview.stat().st_size < 2000:
                failures.append("graph overview screenshot is suspiciously tiny (blank canvas?)")

            # drive the flagship Trace query over the rendered graph
            page.select_option("#qa", _TRACE_A)
            page.select_option("#qb", _TRACE_B)
            page.click("#qgo")
            page.wait_for_timeout(200)
            qout = page.locator("#qout").inner_text().strip()
            print(f"Trace {_TRACE_A} <-> {_TRACE_B}: {qout!r}")
            if "bridge" not in qout.lower():
                failures.append(f"Trace answer names no bridge: {qout!r}")
            if not any(b in qout for b in _KNOWN_BRIDGES):
                failures.append(
                    f"Trace answer names none of the known bridges {_KNOWN_BRIDGES}: {qout!r}"
                )
            # evidence ranking must survive to the live browser answer: every bridge
            # labelled [N+M src] and the strongest named — not a bare entity list.
            if not re.search(r"\[\d+\+\d+ src\]", qout):
                failures.append(f"Trace answer carries no [N+M src] evidence labels: {qout!r}")
            if "strongest" not in qout:
                failures.append(f"Trace answer does not name the strongest bridge: {qout!r}")
            page.screenshot(path=str(_SHOTS / "graph-trace.png"))

            # --- keyboard: the interactive graph is operable without a mouse (WCAG 2.1.1) ---
            # Focus the canvas, walk one node with an arrow key, and prove BOTH the polite
            # live region announced a node AND the canvas actually redrew (view re-centred) —
            # the keyboard-nav gate the token-presence unit test can't reach.
            page.eval_on_selector("#qclear", "el => el.click()")  # clear the trace first
            page.wait_for_timeout(150)
            page.locator("#g").focus()
            before_kb = canvas.screenshot()
            page.keyboard.press("ArrowRight")
            page.wait_for_timeout(300)
            kb_status = page.locator("#gstatus").inner_text().strip()
            print(f"Keyboard focus status: {kb_status!r}")
            if "node" not in kb_status.lower() or " of " not in kb_status.lower():
                failures.append(f"ArrowRight did not announce a focused node: {kb_status!r}")
            after_kb = canvas.screenshot()
            if before_kb == after_kb:
                failures.append("ArrowRight did not move/redraw the graph (keyboard nav is dead)")
            page.screenshot(path=str(_SHOTS / "graph-keyboard.png"))

            # --- shareable view state: a legend filter round-trips through the URL -----
            # Toggle the commodity layer ON, prove the #hash captured it (layers=...), reload
            # from that same URL, and prove the layer stayed ON. This is the "the whole view
            # is a URL" guarantee — a bare trace link can't reproduce which layers a reader
            # had open; a shared link now can (KR-B full-view-state share proof).
            page.eval_on_selector("#legend .lg[data-cls='commodity']", "el => el.click()")
            page.wait_for_timeout(150)
            hash_after_toggle = page.evaluate("() => location.hash")
            print(f"Hash after commodity toggle: {hash_after_toggle!r}")
            if "layers=" not in hash_after_toggle:
                failures.append(
                    f"legend toggle did not write layers= into the URL: {hash_after_toggle!r}"
                )
            page.reload(wait_until="networkidle")
            page.wait_for_timeout(400)
            chip_off = page.eval_on_selector(
                "#legend .lg[data-cls='commodity']", "el => el.classList.contains('off')"
            )
            if chip_off:
                failures.append(
                    "commodity layer did not survive a reload from the shared URL (view state lost)"
                )
            else:
                print("filter state round-tripped through the URL on reload OK")
            page.close()

            # --- mobile: responsive render + touch-drag pans -----------------------
            ctx = browser.new_context(
                viewport={"width": 390, "height": 780}, has_touch=True, is_mobile=True
            )
            mpage = ctx.new_page()
            mpage.goto(url, wait_until="networkidle")
            mpage.wait_for_timeout(1800)
            mcanvas = mpage.locator("#g")
            mbox = mcanvas.bounding_box()
            if not mbox or mbox["width"] > 390:
                failures.append(f"graph canvas not responsive on a 390px viewport: {mbox}")
            mpage.screenshot(path=str(_SHOTS / "graph-mobile.png"))

            # touch-drag: dispatch a real one-finger pan and prove the view moved
            # (canvas pixels change). Fail-soft: if this Chromium build can't synthesize
            # a TouchEvent we NOTE it rather than red the whole gate.
            if mbox:
                before = mcanvas.screenshot()
                cx, cy = mbox["x"] + mbox["width"] / 2, mbox["y"] + mbox["height"] / 2
                panned = _touch_pan(mpage, cx, cy)
                mpage.wait_for_timeout(200)
                after = mcanvas.screenshot()
                if panned and before == after:
                    failures.append(
                        "touch-drag did not change the canvas (pan is broken on mobile)"
                    )
                elif not panned:
                    print(
                        "NOTE: could not synthesize a TouchEvent in this environment — "
                        "touch-pan not exercised (token guard + node --check still cover it)"
                    )
                else:
                    print("touch-drag panned the view (canvas pixels changed) OK")
            ctx.close()
            browser.close()
    finally:
        httpd.shutdown()

    if failures:
        print("\nSMOKE FAIL:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(
        f"\nSMOKE PASS — graph renders, Trace answers, mobile responsive; screenshots in {_SHOTS}"
    )
    return 0


def _touch_pan(page: object, cx: float, cy: float) -> bool:
    """Dispatch a synthetic one-finger drag on the canvas. Returns False if the
    environment can't build a TouchEvent (then the caller treats it as a NOTE)."""
    js = """
    ([cx, cy]) => {
      const cv = document.getElementById('g');
      if (!cv) return false;
      const mk = (type, x, y) => {
        try {
          const t = new Touch({identifier: 1, target: cv, clientX: x, clientY: y});
          const ev = new TouchEvent(type, {cancelable: true, bubbles: true,
            touches: type === 'touchend' ? [] : [t],
            targetTouches: type === 'touchend' ? [] : [t],
            changedTouches: [t]});
          cv.dispatchEvent(ev);
          return true;
        } catch (e) { return false; }
      };
      if (!mk('touchstart', cx, cy)) return false;
      mk('touchmove', cx + 130, cy + 40);
      mk('touchend', cx + 130, cy + 40);
      return true;
    }
    """
    try:
        return bool(page.evaluate(js, [cx, cy]))  # type: ignore[attr-defined]
    except Exception:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
