#!/usr/bin/env python3
"""Broken-internal-link check for the built azimuth static site.

Crawls every ``*.html`` page under the site output dir, extracts every ``href``,
and verifies that each INTERNAL link resolves:

* the target file exists on disk (relative to the linking page), and
* any ``#fragment`` matches an ``id="..."`` / ``name="..."`` anchor in that target.

External links (``http(s)://``, ``mailto:``, protocol-relative ``//``) are skipped —
this is a *public-flip readiness* gate for the bundle's own internal navigation, the
exact "no broken internal links" acceptance criterion for the W26 USP KR.

Exit code 0 = all internal links resolve; 1 = at least one broken link (each printed).

Usage:
    python scripts/check_site_links.py            # checks ./site
    python scripts/check_site_links.py --site _site
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

_HREF_RE = re.compile(r'href\s*=\s*"([^"]*)"', re.IGNORECASE)
_ID_RE = re.compile(r'\b(?:id|name)\s*=\s*"([^"]+)"', re.IGNORECASE)
_SCRIPT_RE = re.compile(r"<script\b.*?</script>", re.IGNORECASE | re.DOTALL)
_EXTERNAL = ("http://", "https://", "mailto:", "tel:", "//", "data:")


def _strip_scripts(html: str) -> str:
    """Drop inline <script> bodies so JS template-literal hrefs (e.g. ``${n.url}``)
    are not mistaken for static links."""
    return _SCRIPT_RE.sub("", html)


def _anchors(html: str) -> set[str]:
    return set(_ID_RE.findall(html))


def check_site(site_dir: Path) -> list[str]:
    """Return a list of human-readable broken-link descriptions (empty = all good)."""
    site_dir = site_dir.resolve()
    pages = sorted(site_dir.rglob("*.html"))
    # cache anchors per resolved file so we parse each target once
    anchor_cache: dict[Path, set[str]] = {}
    broken: list[str] = []

    for page in pages:
        rel_page = page.relative_to(site_dir).as_posix()
        text = _strip_scripts(page.read_text(encoding="utf-8"))
        for raw in _HREF_RE.findall(text):
            href = raw.strip()
            if not href or href.startswith("#"):
                # pure in-page anchor — validate against this page's own ids
                frag = href[1:]
                if frag and frag not in _anchors(text):
                    broken.append(f"{rel_page}: missing in-page anchor #{frag}")
                continue
            if href.startswith(_EXTERNAL):
                continue
            path_part, _, frag = href.partition("#")
            target = (page.parent / path_part).resolve()
            if not target.exists():
                broken.append(f"{rel_page}: -> {href} (target file missing)")
                continue
            if frag:
                if target not in anchor_cache:
                    anchor_cache[target] = (
                        _anchors(target.read_text(encoding="utf-8"))
                        if target.suffix == ".html"
                        else set()
                    )
                if frag not in anchor_cache[target]:
                    broken.append(f"{rel_page}: -> {href} (anchor #{frag} not found)")
    return broken


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the built site for broken internal links.")
    parser.add_argument("--site", default="site", help="built-site dir (default: site)")
    args = parser.parse_args(argv)

    site_dir = Path(args.site)
    if not site_dir.is_absolute():
        site_dir = Path(__file__).resolve().parent.parent / site_dir
    if not site_dir.is_dir():
        print(f"FAIL: site dir not found: {site_dir} (run scripts/build_site.py first)")
        return 1

    pages = list(site_dir.rglob("*.html"))
    broken = check_site(site_dir)
    if broken:
        print(f"FAIL: {len(broken)} broken internal link(s) across {len(pages)} page(s):")
        for b in broken:
            print(f"  - {b}")
        return 1
    print(f"PASS: all internal links resolve across {len(pages)} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
