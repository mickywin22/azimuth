"""Tests for the Vault-LD linked-data exporter (scripts/build_rdf.py).

The load-bearing guarantees this pins:

1. **The lift is real RDF.** Every L1 source / L2 brief / L3 rule note becomes a typed
   subject; the ontology (classes + typed properties) emits into ``schema.ttl`` and the
   instances into ``data.ttl``, both well-formed Turtle.
2. **Datatypes + object links survive.** ``updated`` is an ``xsd:dateTime`` literal, and a
   brief's ``sources`` list becomes ``az:restsOn`` object links to the L1 source subjects.
3. **The editorial guarantee holds in RDF too.** A held theme's brief + its L1 source notes
   are excluded from the graph — the same exclusion the site build enforces.
4. **The ontology can't drift from the context.** Every ``az:`` property the exporter emits
   into schema.ttl is defined in the committed ``vault/ontology/azimuth.context.jsonld`` and
   vice-versa — so the authoring surface (the context) and the export stay in lock-step.
5. **Unmapped constructs are flagged, never dropped** (Vault-LD SPEC §5.6).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "build_rdf", _REPO_ROOT / "scripts" / "build_rdf.py"
)
assert _spec and _spec.loader
build_rdf = importlib.util.module_from_spec(_spec)
# Register before exec so the module's dataclasses can introspect their own __module__
# (Python 3.14's dataclasses._is_type looks the module up in sys.modules).
sys.modules["build_rdf"] = build_rdf
_spec.loader.exec_module(build_rdf)

_AZ = build_rdf.ONT_BASE
_VLD = build_rdf.VLD_BASE


_REGISTRY = {
    "themes": {
        "energy-supply": {"title": "Energy Supply Weekly", "brief": "Energy Supply Weekly.md"},
        "held-theme": {
            "title": "Held Weekly",
            "brief": "Held Weekly.md",
            "brief_held": True,
            "hold_reason": "test held theme",
        },
    },
    "sources": [
        {"key": "fuel-prices", "theme": "energy-supply", "surfaced": True},
        {"key": "held-key", "theme": "held-theme", "surfaced": True},
    ],
}

_L1 = (
    "---\n"
    'source: "WorldMonitor fuel-price feed"\n'
    'source_key: "fuel-prices"\n'
    'endpoint: "/api/economic/v1/get-fuel-prices"\n'
    'retrieved: "2026-07-01T06:00:00Z"\n'
    'license: "CC-BY-4.0"\n'
    'attribution: "Data: WorldMonitor"\n'
    "---\n# Fuel prices\nBody text (not part of the graph).\n"
)
_L1_HELD = (
    "---\n"
    'source: "Held feed"\n'
    'source_key: "held-key"\n'
    'retrieved: "2026-07-01T06:00:00Z"\n'
    'license: "CC-BY-4.0"\n'
    "---\n# Held source\nBody.\n"
)
_BRIEF = (
    "---\n"
    "title: Energy Supply Weekly\n"
    "type: L2-brief\n"
    "theme: energy-supply\n"
    "week: 2026-W27\n"
    "updated: 2026-07-01T22:40:00Z\n"
    "sources: [fuel-prices]\n"
    "license: CC-BY-4.0\n"
    "attribution: azimuth\n"
    "---\n# Energy Supply Weekly\nDiesel eased ([[fuel-prices]]).\n"
)
_BRIEF_HELD = (
    "---\ntitle: Held Weekly\ntype: L2-brief\ntheme: held-theme\nweek: 2026-W27\n"
    "updated: 2026-07-01T22:40:00Z\nsources: [held-key]\n---\n# Held Weekly\nHidden.\n"
)
_RULE = (
    "---\n"
    "title: Editorial Line\n"
    "type: L3-rule\n"
    "license: CC-BY-4.0\n"
    "attribution: azimuth\n"
    "mood: neutral\n"  # an intentionally-unmapped key: must be flagged, never emitted
    "---\n# Editorial Line\nFacts in, opinions out.\n"
)


def _make_vault(tmp_path: Path) -> tuple[Path, Path]:
    """A minimal but real OKF bundle: the committed composed context + one note per layer."""
    vault = tmp_path / "vault"
    (vault / "ontology").mkdir(parents=True)
    # Reuse the REAL committed composed context so the test exercises the shipped mapping.
    (vault / "context.jsonld").write_text(
        (_REPO_ROOT / "vault" / "context.jsonld").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (vault / "ontology" / "azimuth.context.jsonld").write_text(
        (_REPO_ROOT / "vault" / "ontology" / "azimuth.context.jsonld").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (vault / "00 Rules").mkdir()
    (vault / "00 Rules" / "editorial.md").write_text(_RULE, encoding="utf-8")
    (vault / "01 Sources" / "2026-07-01").mkdir(parents=True)
    (vault / "01 Sources" / "2026-07-01" / "fuel-prices.md").write_text(_L1, encoding="utf-8")
    (vault / "01 Sources" / "2026-07-01" / "held-key.md").write_text(_L1_HELD, encoding="utf-8")
    (vault / "02 Briefs").mkdir()
    (vault / "02 Briefs" / "Energy Supply Weekly.md").write_text(_BRIEF, encoding="utf-8")
    (vault / "02 Briefs" / "Held Weekly.md").write_text(_BRIEF_HELD, encoding="utf-8")

    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps(_REGISTRY), encoding="utf-8")
    return vault, registry


def _export(tmp_path: Path) -> tuple[Graph, Graph, list[tuple[str, list[str]]], Path]:
    vault, registry = _make_vault(tmp_path)
    out = tmp_path / "site"
    schema, data, flagged = build_rdf.export(out, vault, registry, write=True)
    return schema, data, flagged, out


def test_schema_declares_the_three_layer_classes(tmp_path: Path) -> None:
    schema, _, _, _ = _export(tmp_path)
    for local in ("L1-source", "L2-brief", "L3-rule"):
        assert (URIRef(_AZ + local), RDF.type, OWL.Class) in schema


def test_schema_typed_properties(tmp_path: Path) -> None:
    schema, _, _, _ = _export(tmp_path)
    # a datatype property carries its xsd range; the one object property links to a class
    assert (URIRef(_AZ + "retrieved"), RDF.type, OWL.DatatypeProperty) in schema
    assert (URIRef(_AZ + "retrieved"), RDFS.range, XSD.dateTime) in schema
    assert (URIRef(_AZ + "restsOn"), RDF.type, OWL.ObjectProperty) in schema
    assert (URIRef(_AZ + "restsOn"), RDFS.range, URIRef(_AZ + "L1-source")) in schema


def test_instances_are_typed_by_layer(tmp_path: Path) -> None:
    _, data, _, _ = _export(tmp_path)
    kinds = {str(o).rsplit("#", 1)[-1] for _, _, o in data.triples((None, RDF.type, None))}
    assert {"L1-source", "L2-brief", "L3-rule"} <= kinds


def test_updated_is_a_typed_datetime_literal(tmp_path: Path) -> None:
    _, data, _, _ = _export(tmp_path)
    updates = list(data.objects(None, URIRef(_AZ + "updated")))
    assert updates, "brief az:updated triple missing"
    assert all(isinstance(o, Literal) and o.datatype == XSD.dateTime for o in updates)


def test_rests_on_links_brief_to_its_source_subject(tmp_path: Path) -> None:
    _, data, _, _ = _export(tmp_path)
    targets = {str(o) for o in data.objects(None, URIRef(_AZ + "restsOn"))}
    assert any(t.endswith("/sources/2026-07-01/fuel-prices") for t in targets), targets
    # object property → the target is itself a typed L1 subject in the graph
    for t in targets:
        assert (URIRef(t), RDF.type, URIRef(_AZ + "L1-source")) in data


def test_every_subject_carries_its_bundle_path(tmp_path: Path) -> None:
    _, data, _, _ = _export(tmp_path)
    subjects = set(data.subjects(RDF.type, None))
    for s in subjects:
        assert (s, URIRef(_VLD + "path"), None) in data or list(
            data.objects(s, URIRef(_VLD + "path"))
        ), f"{s} has no vld:path"


def test_held_theme_is_excluded_from_the_graph(tmp_path: Path) -> None:
    _, data, _, _ = _export(tmp_path)
    serialized = data.serialize(format="turtle")
    assert "held-key" not in serialized
    assert "Held Weekly" not in serialized
    assert "held-theme" not in serialized


def test_unmapped_key_is_flagged_not_emitted(tmp_path: Path) -> None:
    _, data, flagged, _ = _export(tmp_path)
    flagged_keys = {key for _, keys in flagged for key in keys}
    assert "mood" in flagged_keys, f"expected 'mood' flagged, got {flagged}"
    assert not list(data.subject_objects(URIRef(_AZ + "mood")))  # never emitted as a triple


def test_output_files_and_context_written(tmp_path: Path) -> None:
    _, _, _, out = _export(tmp_path)
    for rel in ("schema.ttl", "data.ttl", "context.jsonld", "ontology/azimuth.context.jsonld"):
        assert (out / rel).is_file(), f"missing {rel}"
    # both .ttl re-parse (well-formed Turtle)
    for name in ("schema.ttl", "data.ttl"):
        Graph().parse(out / name, format="turtle")


def test_ontology_export_is_pinned_to_the_committed_context(tmp_path: Path) -> None:
    """Every az: property the exporter emits must be defined in the shipped context (no drift)."""
    ctx = json.loads(
        (_REPO_ROOT / "vault" / "ontology" / "azimuth.context.jsonld").read_text(encoding="utf-8")
    )["@context"]
    az_localnames_in_context = {
        str(v["@id"]).split(":", 1)[1]
        for v in ctx.values()
        if isinstance(v, dict) and str(v.get("@id", "")).startswith("az:")
    }
    prop_localnames = {p.localname for p in build_rdf._PROPS}
    assert prop_localnames == az_localnames_in_context, (
        "scripts/build_rdf.py _PROPS and vault/ontology/azimuth.context.jsonld disagree: "
        f"only-in-exporter={prop_localnames - az_localnames_in_context}, "
        f"only-in-context={az_localnames_in_context - prop_localnames}"
    )
