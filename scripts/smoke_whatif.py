#!/usr/bin/env python3
"""Live Playwright smoke for the demonstrator 'what-if' panel (KR-B acceptance gate).

Serves the built ``site/`` over a local HTTP server, opens ``answers.html`` in a real
Chromium, and proves the interactive proof works end-to-end:

  1. each what-if panel starts on the REAL verdict (the counterfactual block is hidden);
  2. clicking "Flip the input" hides the real verdict and reveals the precomputed
     counterfactual — and the rendered verdict TEXT actually changes;
  3. the truth-table branch label changes with it.

A screenshot of the first (Q2) panel in both states is written to ``_smoke/`` so the
visual proof is banked. Exit code 0 = pass.

Usage:  python scripts/smoke_whatif.py
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
    if not (_SITE / "answers.html").is_file():
        print(
            "FAIL: site/answers.html not built — run scripts/build_site.py first", file=sys.stderr
        )
        return 1
    _SHOTS.mkdir(exist_ok=True)
    httpd, port = _serve(_SITE)
    failures: list[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 900, "height": 1400})
            page.goto(f"http://127.0.0.1:{port}/answers.html", wait_until="networkidle")

            panels = page.locator(".whatif")
            n = panels.count()
            if n < 2:
                failures.append(f"expected >=2 what-if panels, found {n}")

            for i in range(n):
                panel = panels.nth(i)
                qid = panel.get_attribute("data-qid") or f"#{i}"
                verdict = panel.locator(".whatif-verdict")
                branch = panel.locator(".whatif-branch")

                real_text = verdict.inner_text().strip()
                real_branch = branch.inner_text().strip()
                # counterfactual block must start hidden
                if panel.locator(".whatif-verdict .wf-show-cf").is_visible():
                    failures.append(f"{qid}: counterfactual visible before toggle")

                panel.locator('.wf-btn[data-mode="cf"]').click()
                page.wait_for_timeout(120)

                cf_text = verdict.inner_text().strip()
                cf_branch = branch.inner_text().strip()
                if cf_text == real_text:
                    failures.append(f"{qid}: verdict text did NOT change on flip")
                if cf_branch == real_branch:
                    failures.append(f"{qid}: branch label did NOT change on flip")
                if not panel.locator(".whatif-verdict .wf-show-cf").is_visible():
                    failures.append(f"{qid}: counterfactual not visible after toggle")

                print(
                    f"{qid}: real={real_branch!r} -> flipped={cf_branch!r} | verdict changed: {cf_text != real_text}"
                )

                if i == 0:
                    panel.locator('.wf-btn[data-mode="real"]').click()
                    page.wait_for_timeout(120)
                    panel.screenshot(path=str(_SHOTS / "whatif-real.png"))
                    panel.locator('.wf-btn[data-mode="cf"]').click()
                    page.wait_for_timeout(120)
                    panel.screenshot(path=str(_SHOTS / "whatif-flipped.png"))

            browser.close()
    finally:
        httpd.shutdown()

    if failures:
        print("\nSMOKE FAIL:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"\nSMOKE PASS — {n} panels flip the verdict; screenshots in {_SHOTS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
