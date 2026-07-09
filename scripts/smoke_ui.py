#!/usr/bin/env python3
"""Live Playwright smoke for the AZ-KR1 "incredible UI" surface.

The token-presence unit tests prove the markup + CSS + scripts are emitted; this proves
they actually WORK in a real browser — the runtime boundary those tests can't cross:

  1. landing centerpiece: the hero <canvas> draws a non-blank mini knowledge-graph from
     graph.json and its "N nodes / M bridges" badge fills in;
  2. build-time sparklines: the hero "vault pulse" + one sparkline per brief card render as
     real inline SVG on the page;
  3. mobile nav: at a phone viewport the flat nav is behind a burger — hidden until tapped,
     revealed on tap (the overflow bug the burger fixes);
  4. graph story mode: the guided tour opens, drives a real Trace on each of its three steps
     (qout names live bridges), and Finish / Escape exit cleanly.

Screenshots are banked to ``_smoke/`` so the visual proof travels with the repo. Exit 0 = all
checks passed; exit 1 = at least one failed (with a printed FAIL line naming which).

Usage:  python scripts/smoke_ui.py            # builds the site first, then smokes it
        python scripts/smoke_ui.py --no-build # smoke the already-built ./site
"""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SITE = _REPO_ROOT / "site"
_SHOTS = _REPO_ROOT / "_smoke"

# Non-transparent canvas pixels below this = a blank/broken centerpiece, not a drawn graph.
_MIN_CANVAS_PIXELS = 1500


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler with the per-request logging silenced."""

    def log_message(self, *args: object) -> None:
        pass


def _serve(directory: Path) -> tuple[socketserver.TCPServer, int]:
    handler = functools.partial(_QuietHandler, directory=str(directory))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


class Checks:
    """Tiny pass/fail collector — prints each check and remembers if any failed."""

    def __init__(self) -> None:
        self.failed = 0

    def ok(self, cond: bool, label: str) -> bool:
        print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        if not cond:
            self.failed += 1
        return cond


def _canvas_pixels(page: Page, selector: str) -> int:
    """Count non-transparent pixels on a canvas — the proof it actually drew something."""
    return int(
        page.evaluate(
            """(sel) => {
      const c = document.querySelector(sel);
      if (!c || !c.getContext) return 0;
      const ctx = c.getContext('2d');
      const d = ctx.getImageData(0, 0, c.width, c.height).data;
      let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 0) n++;
      return n;
    }""",
            selector,
        )
    )


def smoke(base: str, checks: Checks) -> None:
    _SHOTS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- 1 + 2: landing centerpiece + sparklines (desktop) -----------------
        print("landing (desktop): centerpiece + sparklines")
        page = browser.new_page(viewport={"width": 1100, "height": 1000})
        page.goto(f"{base}/index.html")
        page.wait_for_selector(".hero-graph.is-live", timeout=10000)
        px = _canvas_pixels(page, "#herograph")
        checks.ok(px >= _MIN_CANVAS_PIXELS, f"hero graph canvas is non-blank ({px} px drawn)")
        badge = page.locator("#hero-graph-count").inner_text()
        checks.ok("nodes" in badge, f"hero graph badge filled from graph.json ('{badge}')")
        n_spark = page.locator("svg.spark").count()
        checks.ok(n_spark >= 6, f"build-time sparklines rendered (>=6: hero + cards) — {n_spark}")
        checks.ok(page.locator(".pulse").is_visible(), "hero 'vault pulse' strip is visible")
        page.locator(".hero-graph").screenshot(path=str(_SHOTS / "landing-hero-graph.png"))
        page.screenshot(path=str(_SHOTS / "landing-desktop.png"))

        # --- 3: mobile nav (phone viewport) ------------------------------------
        print("landing (mobile): hamburger nav")
        m = browser.new_page(viewport={"width": 390, "height": 780})
        m.goto(f"{base}/index.html")
        m.wait_for_selector("header.nav")
        burger, nav = m.locator(".nav-burger"), m.locator("header.nav nav")
        checks.ok(burger.is_visible(), "burger visible at phone width")
        checks.ok(not nav.is_visible(), "nav collapsed (hidden) before tap")
        burger.click()
        checks.ok(nav.is_visible(), "nav revealed after tapping the burger")
        m.screenshot(path=str(_SHOTS / "landing-mobile-nav.png"))

        # --- 4: graph story mode -----------------------------------------------
        print("graph: story mode drives three live traces")
        g = browser.new_page(viewport={"width": 1100, "height": 1000})
        g.goto(f"{base}/graph.html")
        g.wait_for_selector("#g")
        g.locator("#qstory").click()
        g.wait_for_selector("#gstory:not([hidden])", timeout=5000)
        traced = 0
        for i in range(3):
            step = g.locator("#story-step").inner_text()
            has_bridge = "shared bridge" in g.locator("#qout").inner_text()
            if has_bridge:
                traced += 1
            if i == 0:
                g.locator(".content").screenshot(path=str(_SHOTS / "graph-story.png"))
            checks.ok(step == f"STORY {i + 1} OF 3", f"story step {i + 1} labelled + shown")
            g.locator("#story-next").click()
        checks.ok(traced == 3, f"all three story steps ran a real Trace ({traced}/3)")
        checks.ok(g.locator("#gstory").is_hidden(), "Finish exits story mode")
        # Escape also exits after re-open
        g.locator("#qstory").click()
        g.wait_for_selector("#gstory:not([hidden])")
        g.keyboard.press("Escape")
        checks.ok(g.locator("#gstory").is_hidden(), "Escape exits story mode")

        browser.close()


def main(argv: list[str] | None = None) -> int:
    # No argparse on purpose: like the sibling browser smokes (smoke_graph.py / smoke_whatif.py)
    # this stays off the argparse-driven public CLI surface, so the browser-free CLI-help CI job
    # never tries to import Playwright. Only flag is `--no-build`.
    args = sys.argv[1:] if argv is None else argv
    no_build = "--no-build" in args

    if not no_build:
        # Build fresh so the smoke can never pass against a stale site.
        sys.path.insert(0, str(_REPO_ROOT))
        from scripts.build_graph import build as build_graph
        from synthesis.site_build import build_site

        build_site(_SITE)
        build_graph(_SITE)
        print(f"Built site into {_SITE}")

    httpd, port = _serve(_SITE)
    base = f"http://127.0.0.1:{port}"
    checks = Checks()
    try:
        smoke(base, checks)
    finally:
        httpd.shutdown()

    print()
    if checks.failed:
        print(f"UI SMOKE FAILED — {checks.failed} check(s) failed.")
        return 1
    print("UI SMOKE PASSED — landing centerpiece, sparklines, mobile nav, story mode all live.")
    print(f"Screenshots banked in {_SHOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
