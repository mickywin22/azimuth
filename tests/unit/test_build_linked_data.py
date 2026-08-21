"""Tests for the linked-data explorer generator (scripts/build_linked_data.py).

The load-bearing guarantees this pins:

1. **Faithful to the RDF, no drift from the .ttl.** The concept projection's class census,
   its typed-property set and its ``az:restsOn`` triple total equal what ``build_rdf.py``'s
   actual rdflib graph emits over the *same* bundle — so the explorable face and the queryable
   face can never diverge (the whole point of reusing build_rdf's own helpers).
2. **The editorial guarantee holds here too.** A held theme's brief + its L1 source notes are
   excluded from the concept model — the same exclusion the site build and RDF export enforce.
3. **Concept-level collapse is honest.** Many dated L1 snapshots of one source key collapse to
   ONE concept carrying the time-series count + date span, while the census still reports the
   full subject count.
4. **The page is a self-contained, discoverable, XSS-safe surface.** It carries the site nav
   (its own entry marked current), embeds the projection as inert JSON with no markup
   breakout, and its ``--check`` guard detects staleness.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load(name: str) -> object:
    """Load a scripts/*.py module by file, registering it before exec (3.14 dataclass introspection)."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, _REPO_ROOT / "scripts" / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# build_linked_data imports build_rdf by bare name at module load; make sure both resolve.
_bld = _load("build_rdf")
bld_ld = _load("build_linked_data")


_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "geophysical": {"title": "Geophysical Weekly", "brief": "Geophysical Weekly.md"},
        "held-theme": {
            "title": "Held Weekly",
            "brief": "Held Weekly.md",
            "brief_held": True,
            "hold_reason": "test held theme",
        },
    },
    "sources": [
        {"key": "fuel-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "earthquakes", "theme": "geophysical", "surfaced": True},
        {"key": "held-key", "theme": "held-theme", "surfaced": True},
    ],
}


def _l1(source: str, key: str) -> str:
    return (
        "---\n"
        f'source: "{source}"\n'
        f'source_key: "{key}"\n'
        f'endpoint: "/api/{key}"\n'
        'retrieved: "2026-07-02T06:00:00Z"\n'
        'license: "CC-BY-4.0"\n'
        'attribution: "Data: WorldMonitor"\n'
        f"---\n# {key}\nBody.\n"
    )


# energy-supply rests on fuel-prices + earthquakes; geophysical rests on fuel-prices too, so
# fuel-prices feeds TWO briefs -> exactly one cross-brief bridge.
_BRIEF_ENERGY = (
    "---\ntitle: Energy Supply Weekly\ntype: L2-brief\ntheme: energy-supply\nweek: 2026-W27\n"
    "updated: 2026-07-02T22:40:00Z\nsources: [fuel-prices, earthquakes]\n"
    "license: CC-BY-4.0\nattribution: azimuth\n---\n# Energy Supply Weekly\nBody.\n"
)
_BRIEF_GEO = (
    "---\ntitle: Geophysical Weekly\ntype: L2-brief\ntheme: geophysical\nweek: 2026-W27\n"
    "updated: 2026-07-02T22:40:00Z\nsources: [fuel-prices]\n"
    "license: CC-BY-4.0\nattribution: azimuth\n---\n# Geophysical Weekly\nBody.\n"
)
_BRIEF_HELD = (
    "---\ntitle: Held Weekly\ntype: L2-brief\ntheme: held-theme\nweek: 2026-W27\n"
    "updated: 2026-07-02T22:40:00Z\nsources: [held-key]\n---\n# Held Weekly\nHidden.\n"
)
_RULE = (
    "---\ntitle: Editorial Line\ntype: L3-rule\nlicense: CC-BY-4.0\nattribution: azimuth\n"
    "---\n# Editorial Line\nFacts in, opinions out.\n"
)


def _make_vault(tmp_path: Path) -> tuple[Path, Path]:
    """A minimal real OKF bundle: the committed context + two L1 days + two briefs + a held theme."""
    vault = tmp_path / "vault"
    (vault / "ontology").mkdir(parents=True)
    (vault / "context.jsonld").write_text(
        (_REPO_ROOT / "vault" / "context.jsonld").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (vault / "ontology" / "azimuth.context.jsonld").write_text(
        (_REPO_ROOT / "vault" / "ontology" / "azimuth.context.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (vault / "00 Rules").mkdir()
    (vault / "00 Rules" / "editorial.md").write_text(_RULE, encoding="utf-8")
    # fuel-prices on two days -> two subjects, one concept, instances == 2.
    for day in ("2026-07-01", "2026-07-02"):
        (vault / "01 Sources" / day).mkdir(parents=True)
        (vault / "01 Sources" / day / "fuel-prices.md").write_text(
            _l1("WorldMonitor fuel-price feed", "fuel-prices"), encoding="utf-8"
        )
    (vault / "01 Sources" / "2026-07-02" / "earthquakes.md").write_text(
        _l1("USGS earthquakes", "earthquakes"), encoding="utf-8"
    )
    (vault / "01 Sources" / "2026-07-02" / "held-key.md").write_text(
        _l1("Held feed", "held-key"), encoding="utf-8"
    )
    (vault / "02 Briefs").mkdir()
    (vault / "02 Briefs" / "Energy Supply Weekly.md").write_text(_BRIEF_ENERGY, encoding="utf-8")
    (vault / "02 Briefs" / "Geophysical Weekly.md").write_text(_BRIEF_GEO, encoding="utf-8")
    (vault / "02 Briefs" / "Held Weekly.md").write_text(_BRIEF_HELD, encoding="utf-8")

    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    return vault, registry


def _project(tmp_path: Path) -> dict:
    vault, registry = _make_vault(tmp_path)
    return bld_ld.build_projection(vault, registry)  # type: ignore[attr-defined]


# --- structure + editorial-exclusion ------------------------------------------------------


def test_projection_census_and_concept_collapse(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    census = {c["class"]: c for c in proj["census"]}
    # 3 L1 subjects (2 fuel days + 1 quake), collapsed to 2 concepts (fuel, quake).
    assert census["L1-source"]["subjects"] == 3
    assert census["L1-source"]["concepts"] == 2
    assert census["L2-brief"]["subjects"] == 2 and census["L2-brief"]["concepts"] == 2
    assert census["L3-rule"]["subjects"] == 1 and census["L3-rule"]["concepts"] == 1
    assert proj["counts"]["concepts_shown"] == 5  # 2 keys + 2 briefs + 1 rule


def test_held_theme_is_excluded(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    labels = {c["label"] for c in proj["concepts"]}
    assert "held-key" not in labels
    assert "Held Weekly" not in labels


def test_time_series_collapse_is_honest(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    fuel = next(c for c in proj["concepts"] if c["id"] == "key:fuel-prices")
    assert fuel["series"]["instances"] == 2
    assert fuel["series"]["first"] == "2026-07-01"
    assert fuel["series"]["last"] == "2026-07-02"


def test_restson_edges_forward_and_reverse(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    energy = next(c for c in proj["concepts"] if c["id"] == "brief:energy-supply-weekly")
    out_targets = {e["target"] for e in energy["edges"] if e["dir"] == "out"}
    assert out_targets == {"key:fuel-prices", "key:earthquakes"}
    fuel = next(c for c in proj["concepts"] if c["id"] == "key:fuel-prices")
    in_targets = {e["target"] for e in fuel["edges"] if e["dir"] == "in"}
    assert in_targets == {"brief:energy-supply-weekly", "brief:geophysical-weekly"}


def test_cross_brief_bridge_surfaces(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    # fuel-prices feeds both briefs -> exactly one bridge naming both.
    assert proj["counts"]["bridges"] == 1
    bridge = proj["bridges"][0]
    assert bridge["label"] == "fuel-prices"
    assert bridge["briefs"] == ["Energy Supply Weekly", "Geophysical Weekly"]


def test_typed_facts_carry_datatypes(tmp_path: Path) -> None:
    proj = _project(tmp_path)
    energy = next(c for c in proj["concepts"] if c["id"] == "brief:energy-supply-weekly")
    facts = {f["pred"]: f for f in energy["facts"]}
    assert facts["updated"]["datatype"] == "dateTime"
    assert facts["theme"]["datatype"] == "string" and facts["theme"]["value"] == "energy-supply"
    # the object property (sources -> restsOn) is an edge, never a literal fact
    assert "sources" not in facts


# --- faithfulness to the RDF export (the anti-drift guarantee) ----------------------------


def test_projection_matches_build_rdf_graph(tmp_path: Path) -> None:
    """Census, property set and restsOn/data-triple totals equal build_rdf's actual RDF graph."""
    pytest.importorskip("rdflib")
    from rdflib import URIRef
    from rdflib.namespace import RDF

    vault, registry = _make_vault(tmp_path)
    proj = bld_ld.build_projection(vault, registry)  # type: ignore[attr-defined]
    data, _flagged = _bld.build_data_graph(vault, registry)  # type: ignore[attr-defined]
    az = _bld.ONT_BASE  # type: ignore[attr-defined]

    # class census
    for c in proj["census"]:
        rdf_subjects = len(set(data.subjects(RDF.type, URIRef(az + c["class"]))))
        assert c["subjects"] == rdf_subjects, f"census drift for {c['class']}"

    # restsOn triple total + data-triple total (the projection computes these in stdlib)
    rdf_restson = len(list(data.triples((None, URIRef(az + "restsOn"), None))))
    assert proj["counts"]["restsOn_edges"] == rdf_restson
    assert proj["counts"]["data_triples"] == len(data)

    # the typed-property set is exactly the ontology's
    assert {p["id"] for p in proj["properties"]} == {p.localname for p in _bld._PROPS}  # type: ignore[attr-defined]
    assert proj["counts"]["schema_triples"] == len(_bld.build_schema_graph())  # type: ignore[attr-defined]


# --- the rendered page: discoverable, self-contained, XSS-safe ----------------------------


def test_page_carries_site_nav_with_current_entry(tmp_path: Path) -> None:
    html = bld_ld.render_html(_project(tmp_path))  # type: ignore[attr-defined]
    assert '<a href="linked-data.html" aria-current="page">Linked data</a>' in html
    for href, label in (
        ("answers.html", "Ask the data"),
        ("benchmark.html", "Benchmark"),
        ("graph.html", "Knowledge graph"),
        ("index.html", "Briefs"),
        ("editorial.html", "Editorial line"),
    ):
        assert f'<a href="{href}">{label}</a>' in html, f"nav link missing: {label}"


def test_embedded_json_is_inert(tmp_path: Path) -> None:
    """The projection is embedded as JSON with markup chars escaped (no <script> breakout)."""
    html = bld_ld.render_html(_project(tmp_path))  # type: ignore[attr-defined]
    start = html.index('<script id="ld-data" type="application/json">') + len(
        '<script id="ld-data" type="application/json">'
    )
    end = html.index("</script>", start)
    block = html[start:end]
    assert "<" not in block and ">" not in block  # hardened to < / >
    parsed = json.loads(
        block.replace("\\u003c", "<").replace("\\u003e", ">").replace("\\u0026", "&")
    )
    assert parsed["counts"]["concepts_shown"] == 5


def test_check_guard_detects_staleness(tmp_path: Path) -> None:
    vault, registry = _make_vault(tmp_path)
    out = tmp_path / "site"
    bld_ld.build(out, vault, registry)  # type: ignore[attr-defined]
    assert bld_ld.check(out, vault, registry) == []  # type: ignore[attr-defined]
    (out / "linked-data.json").write_text("stale\n", encoding="utf-8")
    assert "linked-data.json" in bld_ld.check(out, vault, registry)  # type: ignore[attr-defined]
