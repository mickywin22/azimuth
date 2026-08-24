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
import os
import shutil
import socketserver
import sys
import threading
from pathlib import Path

# Default wall-clock ceiling for a full build (seconds). A healthy build is ~seconds;
# anything past this is a hang. 2026-08-23: a build hung for HOURS (pid alive, ~1 CPU-min)
# and -- before the temp+swap below -- left the live site gutted. This self-watchdog is the
# belt to the watcher's braces: even a direct/manual `python build_site.py` can never wedge
# forever. --serve runs are exempt (serve_forever is meant to block).
_DEFAULT_BUILD_TIMEOUT_S = 600


def _arm_watchdog(timeout_s: int) -> None:
    """Hard-exit the process if the build has not finished within ``timeout_s``.

    Uses os._exit from a daemon Timer so it fires even if the main thread is blocked in
    an un-interruptible C call (the classic "pid alive, ~0 CPU" hang). Exit code 2 lets the
    watcher log a killed build and, critically, keeps the temp+swap below from running -- so a
    timed-out build never touches the live site/ dir.
    """
    if timeout_s <= 0:
        return

    def _kill() -> None:  # pragma: no cover - fires only on a real hang
        sys.stderr.write(
            f"build_site.py: BUILD TIMEOUT after {timeout_s}s -- hard-exiting (site/ left untouched)\n"
        )
        sys.stderr.flush()
        os._exit(2)

    t = threading.Timer(timeout_s, _kill)
    t.daemon = True
    t.start()

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts.build_autonomy import build as build_autonomy  # noqa: E402
from scripts.build_graph import build as build_graph  # noqa: E402
from scripts.build_linked_data import build as build_linked_data  # noqa: E402
from synthesis.site_build import build_site  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the azimuth public static site.")
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    parser.add_argument("--serve", action="store_true", help="serve after building")
    parser.add_argument("--port", type=int, default=8099, help="serve port (default: 8099)")
    parser.add_argument(
        "--timeout",
        type=int,
        default=_DEFAULT_BUILD_TIMEOUT_S,
        help=(
            "hard wall-clock ceiling in seconds for the build phase; the process self-kills "
            f"past it so a hang can't wedge (default: {_DEFAULT_BUILD_TIMEOUT_S}; 0 disables)"
        ),
    )
    args = parser.parse_args(argv)

    # Arm the self-watchdog for the BUILD phase only. --serve deliberately blocks forever, so
    # don't let the timer nuke a healthy long-running preview server.
    if not args.serve:
        _arm_watchdog(args.timeout)

    final_dir = (_REPO_ROOT / args.out).resolve()
    # Build into a sibling temp dir and swap in only on FULL success (2026-08-23): build_site()
    # clears its output dir first, so a build that dies mid-run used to leave the LIVE site gutted
    # to a bare directory listing (the :8791 server kept serving the emptied folder for hours).
    # With the temp+swap, a dead build changes nothing -- the site serves yesterday, never nothing.
    out_dir = final_dir.with_name(final_dir.name + ".tmp")
    if out_dir.exists():
        shutil.rmtree(out_dir, ignore_errors=True)
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

    # The linked-data explorer (linked-data.json + linked-data.html) — the typed-RDF
    # concept surface over the same bundle. Emitted beside the .ttl the Pages build writes
    # (scripts/build_rdf.py --out _site), so schema.ttl / data.ttl resolve from its links.
    ld = build_linked_data(out_dir)
    print(
        f"Built linked-data explorer: {ld['counts']['concepts_shown']} concepts, "
        f"{ld['counts']['restsOn_edges']} rests-on edges, {ld['counts']['bridges']} bridges."
    )

    # The static landing page is authored, not generated -- carry it into every build so the
    # site root never serves a directory listing again (scripts/site_index.html is the source).
    landing = _REPO_ROOT / "scripts" / "site_index.html"
    if landing.exists():
        shutil.copy2(landing, out_dir / "index.html")
        print("Copied landing page: index.html.")

    # Atomic-ish swap: rename final -> .old, tmp -> final. The :8791 http.server holds the
    # directory as a path string (not a handle), so the swap is transparent to it. If Windows
    # refuses the rename (a pinned handle), fall back to copy-into-place -- still strictly
    # after a fully successful build, so the failure mode is "stale files linger", never "gutted".
    old_dir = final_dir.with_name(final_dir.name + ".old")
    if old_dir.exists():
        shutil.rmtree(old_dir, ignore_errors=True)
    try:
        if final_dir.exists():
            final_dir.rename(old_dir)
        out_dir.rename(final_dir)
        shutil.rmtree(old_dir, ignore_errors=True)
    except OSError:
        for item in out_dir.iterdir():
            dest = final_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        shutil.rmtree(out_dir, ignore_errors=True)
    out_dir = final_dir
    print(f"Site swapped live at {final_dir}.")

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
