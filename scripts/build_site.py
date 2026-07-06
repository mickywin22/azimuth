#!/usr/bin/env python3
"""Build + (optionally) serve the azimuth public static site.

Renders the ``vault/`` tree into a browsable read-only HTML site (see
``synthesis/site_build.py`` for the engine + the held-theme exclusion rule).
This is the F3 public-flip build artifact and a local preview Michael can open.

Usage:
    python scripts/build_site.py                 # build into ./site
    python scripts/build_site.py --out _site      # custom output dir
    python scripts/build_site.py --serve          # build, then serve on :8099
    python scripts/build_site.py --serve --port 9000
"""

from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.build_autonomy import build as build_autonomy  # noqa: E402
from scripts.build_graph import build as build_graph  # noqa: E402
from synthesis.site_build import build_site  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the azimuth public static site.")
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    parser.add_argument("--serve", action="store_true", help="serve after building")
    parser.add_argument("--port", type=int, default=8099, help="serve port (default: 8099)")
    args = parser.parse_args(argv)

    out_dir = (_REPO_ROOT / args.out).resolve()
    model = build_site(out_dir)
    n_pages = len(model.briefs) + len(model.sources) + len(model.rules) + 1
    print(
        f"Built {n_pages} pages into {out_dir}: "
        f"{len(model.briefs)} briefs, {len(model.sources)} source notes, "
        f"{len(model.rules)} rule page(s). Held themes excluded."
    )

    # The cross-channel knowledge graph (graph.json + graph.html). build_site clears
    # the output dir first, so the graph is (re)generated here, after the pages exist.
    graph = build_graph(out_dir)
    n_cross = sum(1 for e in graph["edges"] if e.get("cross_theme"))
    n_entity = sum(1 for n in graph["nodes"] if n["kind"] == "entity")
    print(
        f"Built cross-channel graph: {len(graph['nodes'])} nodes, "
        f"{len(graph['edges'])} edges ({n_entity} shared entities, "
        f"{n_cross} cross-theme edges)."
    )

    # The autonomy counters (autonomy.json + autonomy.html) — the "proof it runs itself"
    # surface. Emitted into the site root so the published site (and the README's dynamic
    # shields.io badges, which read /autonomy.json) resolve after the Pages flip.
    build_autonomy(out_dir)
    print("Built autonomy counters: autonomy.json + autonomy.html.")

    if args.serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(out_dir))
        with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
            print(f"Serving at http://127.0.0.1:{args.port}/  (Ctrl+C to stop)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
