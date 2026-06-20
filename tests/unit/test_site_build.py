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
        "---\ntitle: Energy Supply Weekly\ntheme: energy-supply\n---\n"
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
