#!/usr/bin/env python3
"""Generate docs/assets/hero.gif — an animated walkthrough of the azimuth site.

Uses Playwright to drive a headless browser through three scenes:
  1. The home page (brief cards + autonomy counters)
  2. The knowledge graph (hexagon layout, two channels highlighted)
  3. A Trace path between two channels

The frames are stitched into an animated GIF at docs/assets/hero.gif.

Requirements (not part of the default runtime):
    uv pip install -e ".[demo]"
    playwright install chromium

Usage:
    python scripts/record_hero_gif.py            # write docs/assets/hero.gif
    python scripts/record_hero_gif.py --width 1280 --height 720
    python scripts/record_hero_gif.py --fps 2    # slower playback (default: 3)
    python scripts/record_hero_gif.py --serve    # build site first, then record
"""

from __future__ import annotations

import argparse
import http.server
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SITE_DIR = _REPO_ROOT / "site"
_OUT = _REPO_ROOT / "docs" / "assets" / "hero.gif"

# Seconds each frame is shown (1 / fps rounded to centiseconds).
_DEFAULT_FPS = 3
# Default viewport
_DEFAULT_W, _DEFAULT_H = 1280, 720


# ---------------------------------------------------------------------------
# Lightweight static file server for the built site
# ---------------------------------------------------------------------------


class _SilentHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args: object) -> None:
        pass


def _serve(directory: Path, port: int) -> None:
    os.chdir(directory)
    httpd = http.server.HTTPServer(("127.0.0.1", port), _SilentHandler)
    httpd.serve_forever()


def _find_free_port() -> int:
    import socket

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


# ---------------------------------------------------------------------------
# Frame capture
# ---------------------------------------------------------------------------


def _capture_frames(base_url: str, width: int, height: int) -> list[Path]:
    """Drive Playwright through the site and return a list of screenshot paths."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: playwright is not installed.\n"
            "Run:  uv pip install -e '.[demo]' && playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)

    tmpdir = Path(tempfile.mkdtemp(prefix="azimuth-gif-"))
    frames: list[Path] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})

        def shot(name: str) -> Path:
            p = tmpdir / f"{name}.png"
            page.screenshot(path=str(p), full_page=False)
            frames.append(p)
            return p

        # --- Scene 1: home page ---
        page.goto(f"{base_url}/index.html", wait_until="networkidle")
        page.wait_for_timeout(600)
        shot("home-01-load")

        # Scroll down to show brief cards
        page.evaluate("window.scrollTo(0, 400)")
        page.wait_for_timeout(400)
        shot("home-02-briefs")

        # --- Scene 2: graph page ---
        page.goto(f"{base_url}/graph.html", wait_until="networkidle")
        page.wait_for_timeout(800)
        shot("graph-01-load")

        # Click the first channel node (the canvas is interactive; try Find)
        try:
            find_input = page.locator("#find-input")
            if find_input.count():
                find_input.fill("energy")
                page.wait_for_timeout(400)
                shot("graph-02-find-energy")
                find_input.fill("")
        except Exception:
            pass

        # --- Scene 3: Trace between two channels ---
        try:
            ch_a = page.locator("#channel-a")
            ch_b = page.locator("#channel-b")
            trace_btn = page.locator("#trace-btn")
            if ch_a.count() and ch_b.count() and trace_btn.count():
                ch_a.select_option(index=0)
                ch_b.select_option(index=1)
                trace_btn.click()
                page.wait_for_timeout(600)
                shot("graph-03-trace")
        except Exception:
            pass

        # --- Scene 4: autonomy counters page ---
        page.goto(f"{base_url}/autonomy.html", wait_until="networkidle")
        page.wait_for_timeout(500)
        shot("autonomy-01")

        browser.close()

    return frames


# ---------------------------------------------------------------------------
# GIF assembly (requires Pillow)
# ---------------------------------------------------------------------------


def _frames_to_gif(frames: list[Path], out: Path, fps: int) -> None:
    try:
        from PIL import Image
    except ImportError:
        print(
            "ERROR: Pillow is not installed.\nRun:  uv pip install -e '.[demo]'",
            file=sys.stderr,
        )
        sys.exit(1)

    delay_cs = max(1, round(100 / fps))  # centiseconds per frame

    images = [Image.open(str(f)).convert("P", palette=Image.ADAPTIVE) for f in frames]
    out.parent.mkdir(parents=True, exist_ok=True)

    images[0].save(
        str(out),
        format="GIF",
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=delay_cs * 10,  # Pillow duration is in milliseconds
        optimize=True,
    )
    size_kb = out.stat().st_size // 1024
    print(f"hero GIF: {out}  ({len(frames)} frames, {size_kb} KB)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="record the azimuth hero GIF")
    parser.add_argument("--width", type=int, default=_DEFAULT_W, help="viewport width")
    parser.add_argument("--height", type=int, default=_DEFAULT_H, help="viewport height")
    parser.add_argument("--fps", type=int, default=_DEFAULT_FPS, help="frames per second")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="run build_site.py first to ensure site/ is up to date",
    )
    args = parser.parse_args(argv)

    if args.serve:
        print("building site…")
        result = subprocess.run(
            [sys.executable, str(_REPO_ROOT / "scripts" / "build_site.py")],
            cwd=str(_REPO_ROOT),
        )
        if result.returncode != 0:
            print("build_site.py failed — aborting", file=sys.stderr)
            return 1

    port = _find_free_port()
    t = threading.Thread(target=_serve, args=(_SITE_DIR, port), daemon=True)
    t.start()
    time.sleep(0.4)

    base_url = f"http://127.0.0.1:{port}"
    frames = _capture_frames(base_url, args.width, args.height)

    if not frames:
        print("no frames captured — is the site built? try --serve", file=sys.stderr)
        return 1

    _frames_to_gif(frames, _OUT, args.fps)
    return 0


if __name__ == "__main__":
    sys.exit(main())
