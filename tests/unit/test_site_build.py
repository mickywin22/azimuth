"""Tests for the static-site generator (synthesis/site_build.py).

The load-bearing guarantees:
* HELD themes (brief_held: true) never appear — not their brief, not their L1 notes;
* wikilinks in a brief resolve to the latest-day L1 source page;
* a wikilink to a held / unknown target degrades to plain text (no dangling link).
"""

from __future__ import annotations

import json
from pathlib import Path

from synthesis.site_build import (
    build_site,
    discover,
    held_source_keys,
    held_themes,
    latest_source_day,
    resolve_wikilinks,
)

_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "prediction-markets": {
            "title": "Prediction Markets Weekly",
            "brief": "Prediction Markets Weekly.md",
            "brief_held": True,
            "hold_reason": "single politically-charged market",
        },
    },
    "sources": [
        {"key": "fuel-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "prediction-markets", "theme": "prediction-markets", "surfaced": True},
    ],
}


def _make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    (vault / "00 Rules").mkdir(parents=True)
    (vault / "00 Rules" / "editorial.md").write_text(
        "---\ntitle: Editorial Line\n---\n# Editorial Line\nNo advice.\n", encoding="utf-8"
    )
    (vault / "02 Briefs").mkdir(parents=True)
    (vault / "02 Briefs" / "Energy Supply Weekly.md").write_text(
        "---\ntitle: Energy Supply Weekly\ntheme: energy-supply\n"
        "updated: 2026-06-19T04:00:00Z\n---\n"
        "# Energy Supply Weekly\n- Diesel ticked up ([[fuel-prices]]).\n"
        "- Odds moved ([[prediction-markets]]).\n",
        encoding="utf-8",
    )
    # held brief file present on disk — must still be skipped
    (vault / "02 Briefs" / "Prediction Markets Weekly.md").write_text(
        "---\ntitle: Prediction Markets Weekly\n---\n# held\n", encoding="utf-8"
    )
    for day in ("2026-06-18", "2026-06-20"):
        d = vault / "01 Sources" / day
        d.mkdir(parents=True)
        (d / "fuel-prices.md").write_text(
            f"---\nsource: Fuel prices\n---\n# Fuel {day}\n", encoding="utf-8"
        )
        (d / "prediction-markets.md").write_text(
            f"---\nsource: Polymarket\n---\n# PM {day}\n", encoding="utf-8"
        )
    return vault


def test_held_theme_detection() -> None:
    assert held_themes(_REGISTRY) == {"prediction-markets"}
    assert held_source_keys(_REGISTRY) == {"prediction-markets"}


def test_discover_excludes_held(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path)
    model = discover(vault, _REGISTRY)

    brief_titles = {b.title for b in model.briefs}
    assert brief_titles == {"Energy Supply Weekly"}  # held brief skipped

    src_keys = {Path(s.out_path).stem for s in model.sources}
    assert "fuel-prices" in src_keys
    assert "prediction-markets" not in src_keys  # held L1 notes skipped

    # link map points fuel-prices at its LATEST day
    assert model.link_map["fuel-prices"] == "sources/2026-06-20/fuel-prices.html"
    assert "prediction-markets" not in model.link_map


def test_wikilink_resolution_and_dead_link() -> None:
    link_map = {"fuel-prices": "sources/2026-06-20/fuel-prices.html"}
    body = "- up ([[fuel-prices]]) and ([[prediction-markets]])"
    out = resolve_wikilinks(body, "briefs/energy-supply-weekly.html", link_map)
    # resolved link is relative from the brief page up to the source page
    assert "(../sources/2026-06-20/fuel-prices.html)" in out
    # held/unknown target degrades to bare text, no link
    assert "[prediction-markets]" not in out
    assert "prediction-markets" in out


def test_build_site_writes_files_and_omits_held(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path)
    out = tmp_path / "site"
    (tmp_path / "registry.json").write_text(json.dumps(_REGISTRY), encoding="utf-8")
    build_site(out, vault_dir=vault, registry_path=tmp_path / "registry.json")

    assert (out / "index.html").is_file()
    assert (out / "assets" / "style.css").is_file()
    assert (out / "briefs" / "energy-supply-weekly.html").is_file()
    assert (out / "sources" / "2026-06-20" / "fuel-prices.html").is_file()
    # no held theme artifacts anywhere
    assert not (out / "sources" / "2026-06-20" / "prediction-markets.html").exists()
    assert not list(out.glob("briefs/prediction*.html"))
    index_text = (out / "index.html").read_text(encoding="utf-8")
    assert "Prediction Markets" not in index_text


def test_latest_source_day(tmp_path: Path) -> None:
    """The freshness date is the newest YYYY-MM-DD folder under 01 Sources/."""
    vault = _make_vault(tmp_path)
    assert latest_source_day(vault) == "2026-06-20"
    # non-date dirs / files are ignored, empty tree degrades to ""
    (vault / "01 Sources" / "not-a-date").mkdir()
    assert latest_source_day(vault) == "2026-06-20"
    assert latest_source_day(tmp_path / "missing") == ""


def test_index_carries_freshness_badge(tmp_path: Path) -> None:
    """AZ-KR2: index hero shows 'Data as of <latest ingest day>' computed, not hardcoded."""
    vault = _make_vault(tmp_path)
    out = tmp_path / "site"
    (tmp_path / "registry.json").write_text(json.dumps(_REGISTRY), encoding="utf-8")
    build_site(out, vault_dir=vault, registry_path=tmp_path / "registry.json")

    index_text = (out / "index.html").read_text(encoding="utf-8")
    assert "Data as of 2026-06-20" in index_text

    # the brief card + brief page carry the per-brief `updated:` signal at page entry
    assert "Updated 2026-06-19" in index_text
    brief_text = (out / "briefs" / "energy-supply-weekly.html").read_text(encoding="utf-8")
    assert "updated 2026-06-19" in brief_text
    # every page header carries the site-wide badge too
    assert "Data as of 2026-06-20" in brief_text


def test_graph_is_discoverable_from_the_site(tmp_path: Path) -> None:
    """KR-B: the knowledge graph is reachable from every page, not a hidden URL.

    graph.html sat orphaned — rendered next to the site but linked from nowhere, so a
    visitor landing on index.html could never find the flagship KG visualization. Guard
    both discovery surfaces: the site-wide nav link (root-relative on subdir pages) and
    the index CTA card with its live-count fill from the published graph.json.
    """
    vault = _make_vault(tmp_path)
    out = tmp_path / "site"
    (tmp_path / "registry.json").write_text(json.dumps(_REGISTRY), encoding="utf-8")
    build_site(out, vault_dir=vault, registry_path=tmp_path / "registry.json")

    index_text = (out / "index.html").read_text(encoding="utf-8")
    assert '<a href="graph.html">Knowledge graph</a>' in index_text
    # the index CTA card: gold graph card + the progressive live-count enhancement
    assert 'class="demo-cta graph-cta" href="graph.html"' in index_text
    assert 'id="graph-cta-stats"' in index_text
    assert 'fetch("graph.json")' in index_text

    # subdir pages prefix the nav with {root} — a brief page must link ../graph.html
    brief_text = (out / "briefs" / "energy-supply-weekly.html").read_text(encoding="utf-8")
    assert '<a href="../graph.html">Knowledge graph</a>' in brief_text


def test_nav_is_mobile_responsive(tmp_path: Path) -> None:
    """AZ-KR1 'incredible UI': the 6-link nav collapses behind a pure-CSS hamburger.

    On a phone the flat nav overflowed the header; the fix is a checkbox+label burger
    (no JS, so it works on the static file:// preview and in reduced-JS environments).
    Guard both halves: the markup on every page and the toggle CSS in the shared sheet.
    """
    vault = _make_vault(tmp_path)
    out = tmp_path / "site"
    (tmp_path / "registry.json").write_text(json.dumps(_REGISTRY), encoding="utf-8")
    build_site(out, vault_dir=vault, registry_path=tmp_path / "registry.json")

    # the burger markup rides on the shared page template — on the index and subdir pages
    for page in ("index.html", "briefs/energy-supply-weekly.html"):
        text = (out / page).read_text(encoding="utf-8")
        assert 'type="checkbox" id="nav-toggle" class="nav-toggle"' in text
        assert 'class="nav-burger"' in text

    css = (out / "assets" / "style.css").read_text(encoding="utf-8")
    # burger hidden on desktop, revealed + wired to the checkbox inside the mobile query
    assert ".nav-burger{display:none" in css
    assert ".nav-toggle:checked~nav{display:flex}" in css
    assert "@media(max-width:720px)" in css


def test_landing_has_graph_centerpiece(tmp_path: Path) -> None:
    """AZ-KR1 'incredible UI': the knowledge graph IS the landing hero.

    A canvas centerpiece draws a settled mini-graph from graph.json and links through to the
    full interactive view. Guard the markup + the drawing script + its CSS; the live paint
    (non-blank canvas) is proven separately by the Playwright smoke.
    """
    vault = _make_vault(tmp_path)
    out = tmp_path / "site"
    (tmp_path / "registry.json").write_text(json.dumps(_REGISTRY), encoding="utf-8")
    build_site(out, vault_dir=vault, registry_path=tmp_path / "registry.json")

    index_text = (out / "index.html").read_text(encoding="utf-8")
    # the clickable centerpiece: canvas + live-count badge + a link to the full graph
    assert '<canvas id="herograph"' in index_text
    assert 'class="hero-graph" href="graph.html"' in index_text
    assert 'id="hero-graph-count"' in index_text
    # the drawing script fetches the published graph and reveals the canvas on success
    assert 'document.getElementById("herograph")' in index_text
    assert 'classList.add("is-live")' in index_text

    css = (out / "assets" / "style.css").read_text(encoding="utf-8")
    assert ".hero-graph{position:relative" in css
    assert ".hero-graph.is-live canvas{opacity:1}" in css
