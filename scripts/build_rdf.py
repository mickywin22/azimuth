#!/usr/bin/env python3
"""Lift the azimuth ``vault/`` OKF bundle into RDF (``schema.ttl`` + ``data.ttl``).

This is the **linked-data export face** of the public demonstrator. The azimuth vault is
already an OKF-style Markdown bundle — a directory of notes with YAML frontmatter — which
is exactly the physical shape a `Vault-LD <https://github.com/The-Knowledge-Graph-Guys/vault-ld>`_
vault has. What an OKF bundle lacks is the *context* that gives its field names shared
meaning. ``vault/context.jsonld`` (composed with ``vault/ontology/azimuth.context.jsonld``)
supplies exactly that, following **Vault-LD SPEC Appendix B — the OKF compatibility profile** —
*without modifying a single bundle file*. This script is the conforming exporter (SPEC §5.4):
it walks the bundle, resolves each short frontmatter field to its full predicate through the
committed context, mints one subject per note, and emits two Turtle files split **by layer**:

* ``schema.ttl`` — the azimuth ontology: the ``az:L1-source`` / ``az:L2-brief`` / ``az:L3-rule``
  classes and the typed properties (``az:retrieved`` → ``xsd:dateTime``, ``az:restsOn`` →
  ``az:L1-source`` …). This is the *definitions* layer.
* ``data.ttl`` — the instances: every surfaced L1 source note, L2 brief and L3 rule as a
  typed RDF subject, its frontmatter facts as triples, and each note's true bundle path as a
  ``vld:path`` literal so the export is a faithful roundtrip face (SPEC §5.4 step 7).

**Pure-stdlib doctrine (why this is a DEV/CI tool, not runtime):** azimuth's runtime is
pure standard library — no third-party runtime dependency (``pyproject`` ``dependencies = []``).
``rdflib`` is imported *lazily* inside the build functions and is declared only in the CI-only
``ld`` optional-dependency extra, so importing this module (for its constants / a ``--check``
that touches no graph) never requires it and the runtime stays clean. The export runs in the
``linked-data`` CI job and in the (flip-gated) Pages build, never on the ingest path.

**Editorial guarantee:** a held theme (``brief_held: true`` in ``sources/registry.json``) —
its brief and every L1 source note that feeds it — is excluded from the graph, the same
guarantee the static-site build (``synthesis/site_build.py``) and the knowledge graph
(``scripts/build_graph.py``) enforce. The RDF graph never surfaces what the site hides.

Usage::

    python scripts/build_rdf.py                 # export into ./site (beside the static site)
    python scripts/build_rdf.py --out _site      # custom output dir (the Pages build uses _site)
    python scripts/build_rdf.py --check          # validate the export in-memory, write nothing (CI gate)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

if TYPE_CHECKING:
    from rdflib import Graph

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import split_frontmatter  # noqa: E402
from synthesis.site_build import (  # noqa: E402
    DEFAULT_REGISTRY,
    DEFAULT_VAULT,
    held_brief_files,
    held_source_keys,
)

# --- namespaces (single source of truth; the committed context mirrors these) -------------
DATA_BASE = "https://mickywin22.github.io/azimuth/data/"
ONT_BASE = "https://mickywin22.github.io/azimuth/ontology#"
VLD_BASE = "https://github.com/The-Knowledge-Graph-Guys/vault-ld#"
DCTERMS = "http://purl.org/dc/terms/"
XSD = "http://www.w3.org/2001/XMLSchema#"

ROOT_CONTEXT = "context.jsonld"  # vault-relative; composes ontology/azimuth.context.jsonld
SPEC_URL = "https://github.com/The-Knowledge-Graph-Guys/vault-ld/blob/main/SPEC.md"

README = "README.md"


@dataclass(frozen=True)
class _ClassDef:
    localname: str
    label: str
    comment: str


@dataclass(frozen=True)
class _PropDef:
    localname: str
    label: str
    comment: str
    is_object: bool
    # range: an ``xsd:`` datatype localname for datatype properties, or an ``az:`` class
    # localname for the one object property (``restsOn`` → ``L1-source``).
    range_local: str
    domain_local: str | None  # az: class localname, or None when the property spans layers


# The azimuth ontology emitted into schema.ttl. Pinned to vault/ontology/azimuth.context.jsonld
# by tests/unit/test_build_rdf.py (every az: property here MUST be defined in that context and
# vice-versa), so the authoring surface (the context) and the schema export can never drift.
_CLASSES: tuple[_ClassDef, ...] = (
    _ClassDef(
        "L1-source",
        "L1 source note",
        "A dated, raw open-data source note — Layer 1 (raw source Claude reads, never edits).",
    ),
    _ClassDef(
        "L2-brief",
        "L2 brief",
        "A weekly synthesis brief — Layer 2 (Claude-owned synthesis evolved over L1 sources).",
    ),
    _ClassDef(
        "L3-rule",
        "L3 rule",
        "An editorial / synthesis-contract rule — Layer 3 (the doctrine the curator writes inside).",
    ),
)

_PROPS: tuple[_PropDef, ...] = (
    _PropDef(
        "upstreamSource",
        "upstream source",
        "The named upstream open-data provider the L1 note pulls from.",
        False,
        "string",
        "L1-source",
    ),
    _PropDef(
        "sourceKey",
        "source key",
        "The sources/registry.json key identifying the WorldMonitor subset.",
        False,
        "string",
        "L1-source",
    ),
    _PropDef(
        "endpoint",
        "endpoint",
        "The WorldMonitor API path the L1 note was retrieved from.",
        False,
        "string",
        "L1-source",
    ),
    _PropDef(
        "retrieved",
        "retrieved at",
        "UTC timestamp the L1 note was pulled from the upstream feed.",
        False,
        "dateTime",
        "L1-source",
    ),
    _PropDef(
        "license",
        "license",
        "The content licence the note is published under.",
        False,
        "string",
        None,
    ),
    _PropDef(
        "attribution",
        "attribution",
        "Human-readable upstream credit line for the note.",
        False,
        "string",
        None,
    ),
    _PropDef(
        "theme",
        "theme",
        "The registry theme / channel the brief synthesises.",
        False,
        "string",
        "L2-brief",
    ),
    _PropDef(
        "week",
        "week",
        "The ISO week the brief covers (YYYY-Www).",
        False,
        "string",
        "L2-brief",
    ),
    _PropDef(
        "updated",
        "updated at",
        "UTC timestamp the brief was last evolved.",
        False,
        "dateTime",
        "L2-brief",
    ),
    _PropDef(
        "restsOn",
        "rests on",
        "Links an L2 brief to the L1 source note(s) its claims rest on.",
        True,
        "L1-source",
        "L2-brief",
    ),
)


# NOTE ON THE LAZY ``rdflib`` IMPORTS BELOW: every function that touches rdflib imports it
# *inside* the function body, never at module top. This mirrors ``synthesis.site_build._md``:
# rdflib lives in the CI-only ``ld`` optional-dependency extra, so importing this module (for
# its constants, CLI wiring, or the tests that pin the ontology against the context) must not
# require it. Only the graph-building / validating paths do — and those run only in CI + the
# Pages build. The module-level ``TYPE_CHECKING`` import of ``Graph`` types the signatures.


# --- context loading (the exporter honours the committed composed context) ----------------


def _resolve_curie(value: str, prefixes: dict[str, str]) -> str:
    """Expand a ``prefix:local`` CURIE to a full IRI using ``prefixes`` (verbatim if none)."""
    if ":" in value:
        pfx, _, local = value.partition(":")
        if pfx in prefixes:
            return prefixes[pfx] + local
    return value


def load_context_terms(vault_dir: Path = DEFAULT_VAULT) -> dict[str, tuple[str, str | None]]:
    """Build ``frontmatter-key -> (predicate IRI, datatype IRI | "@id" | None)`` from the
    committed composed context (``vault/context.jsonld`` + the ontology context it references).

    This is what makes the exporter a *conforming* Vault-LD tool (SPEC §4): the mapping from
    short field names to predicates comes from the context that ships with the bundle, not
    from hard-coded knowledge. A key absent from the context is not part of the shared
    vocabulary and is flagged, never silently emitted (SPEC §5.6).
    """
    root = json.loads((vault_dir / ROOT_CONTEXT).read_text(encoding="utf-8"))
    entries = root["@context"]
    if not isinstance(entries, list):
        entries = [entries]

    prefixes: dict[str, str] = {}
    term_defs: dict[str, Any] = {}
    for entry in entries:
        obj = entry
        if isinstance(entry, str):  # a referenced context document (composition) — resolve it
            ref = json.loads((vault_dir / entry).read_text(encoding="utf-8"))
            obj = ref["@context"]
        if not isinstance(obj, dict):
            continue
        for key, val in obj.items():
            if key.startswith("@") or key == "//":
                continue
            if isinstance(val, str) and val.endswith(("#", "/")):  # a prefix declaration
                prefixes[key] = val
            else:
                term_defs[key] = val

    terms: dict[str, tuple[str, str | None]] = {}
    for key, val in term_defs.items():
        if isinstance(val, str):
            iri = _resolve_curie(val, prefixes)
            dt: str | None = None
        elif isinstance(val, dict) and "@id" in val:
            iri = _resolve_curie(str(val["@id"]), prefixes)
            raw_type = val.get("@type")
            dt = (
                "@id"
                if raw_type == "@id"
                else (_resolve_curie(str(raw_type), prefixes) if raw_type else None)
            )
        else:
            continue
        # Only keep terms that name an azimuth or dcterms predicate (skip the structural
        # RDFS/OWL/SKOS terms the root declares for schema authoring — label, domain, …).
        if iri.startswith((ONT_BASE, DCTERMS)):
            terms[key] = (iri, dt)
    return terms


# --- vault walk helpers -------------------------------------------------------------------


def _parse_list(raw: str) -> list[str]:
    """Parse a naive-frontmatter list value (``[a, b, c]``) into stripped items.

    ``synthesis.lint.split_frontmatter`` is a dependency-free scalar parser, so a YAML flow
    sequence arrives as the literal string ``"[a, b, c]"``; this recovers the items.
    """
    inner = raw.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    return [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]


def _mint(local: str) -> str:
    """Mint a data-layer subject IRI from a bundle-stable name (percent-encoded, SPEC §4.5)."""
    return DATA_BASE + quote(local, safe="/")


def _latest_source_iri_by_key(vault_dir: Path, skip_keys: set[str]) -> dict[str, str]:
    """Map each surfaced source key -> the subject IRI of its NEWEST dated L1 note.

    ``az:restsOn`` points a brief at the latest source note per key, mirroring the
    ``rests-on`` relation the knowledge graph draws (``scripts/build_graph.py``).
    """
    out: dict[str, str] = {}
    sources_dir = vault_dir / "01 Sources"
    if not sources_dir.is_dir():
        return out
    for day_dir in sorted((d for d in sources_dir.iterdir() if d.is_dir()), reverse=True):
        for path in sorted(day_dir.glob("*.md")):
            key = path.stem
            if key == "README" or key in skip_keys or key in out:
                continue
            out[key] = _mint(f"sources/{day_dir.name}/{key}")
    return out


@dataclass
class _Note:
    """One participating vault note, resolved to its subject + typed frontmatter."""

    iri: str
    class_local: str  # az: class localname
    fm: dict[str, str]
    rel_path: str  # bundle-relative posix path, for vld:path


def _discover_notes(vault_dir: Path, skip_keys: set[str], skip_briefs: set[str]) -> list[_Note]:
    """Walk the bundle → the participating notes.

    Layer is decided by folder (SPEC §5.4 step 5): ``01 Sources`` → L1, ``02 Briefs`` → L2,
    ``00 Rules`` → L3. Held source keys / briefs and READMEs are excluded.
    """
    notes: list[_Note] = []

    # L1 source notes (dated) — each (day, key) is its own time-series subject.
    sources_dir = vault_dir / "01 Sources"
    if sources_dir.is_dir():
        for day_dir in sorted(d for d in sources_dir.iterdir() if d.is_dir()):
            for path in sorted(day_dir.glob("*.md")):
                if path.name == README or path.stem in skip_keys:
                    continue
                fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
                notes.append(
                    _Note(
                        _mint(f"sources/{day_dir.name}/{path.stem}"),
                        "L1-source",
                        fm or {},
                        f"01 Sources/{day_dir.name}/{path.name}",
                    )
                )

    # L2 briefs.
    briefs_dir = vault_dir / "02 Briefs"
    if briefs_dir.is_dir():
        for path in sorted(briefs_dir.glob("*.md")):
            if path.name == README or path.name in skip_briefs:
                continue
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            notes.append(_Note(_mint(path.stem), "L2-brief", fm or {}, f"02 Briefs/{path.name}"))

    # L3 rules.
    rules_dir = vault_dir / "00 Rules"
    if rules_dir.is_dir():
        for path in sorted(rules_dir.glob("*.md")):
            if path.name == README:
                continue
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            notes.append(_Note(_mint(path.stem), "L3-rule", fm or {}, f"00 Rules/{path.name}"))

    return notes


# --- the two graphs ----------------------------------------------------------------------


def _bind_namespaces(g: Graph) -> None:
    from rdflib import Namespace
    from rdflib.namespace import OWL, RDFS, XSD

    g.bind("az", Namespace(ONT_BASE))
    g.bind("data", Namespace(DATA_BASE))
    g.bind("vld", Namespace(VLD_BASE))
    g.bind("dcterms", Namespace(DCTERMS))
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)


def build_schema_graph() -> Graph:
    """The ontology (definitions) layer → ``schema.ttl``, emitted from ``_CLASSES`` / ``_PROPS``."""
    from rdflib import Graph, Literal, URIRef
    from rdflib.namespace import OWL, RDF, RDFS

    g: Graph = Graph()
    _bind_namespaces(g)

    def az(local: str) -> URIRef:
        return URIRef(ONT_BASE + local)

    ont = URIRef(ONT_BASE.rstrip("#"))
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, RDFS.label, Literal("azimuth vault ontology")))
    g.add(
        (
            ont,
            RDFS.comment,
            Literal(
                "The L1/L2/L3 vault-doctrine ontology for azimuth: the classes and properties "
                "that lift the OKF-style Markdown bundle into linked data via the Vault-LD "
                "OKF compatibility profile (SPEC Appendix B)."
            ),
        )
    )
    g.add((ont, RDFS.seeAlso, URIRef(SPEC_URL)))
    g.add((ont, URIRef(DCTERMS + "license"), Literal("CC-BY-4.0")))

    for c in _CLASSES:
        subj = az(c.localname)
        g.add((subj, RDF.type, OWL.Class))
        g.add((subj, RDFS.label, Literal(c.label)))
        g.add((subj, RDFS.comment, Literal(c.comment)))
        g.add((subj, RDFS.isDefinedBy, ont))

    for p in _PROPS:
        subj = az(p.localname)
        g.add((subj, RDF.type, OWL.ObjectProperty if p.is_object else OWL.DatatypeProperty))
        g.add((subj, RDFS.label, Literal(p.label)))
        g.add((subj, RDFS.comment, Literal(p.comment)))
        g.add((subj, RDFS.isDefinedBy, ont))
        if p.domain_local:
            g.add((subj, RDFS.domain, az(p.domain_local)))
        g.add(
            (subj, RDFS.range, az(p.range_local) if p.is_object else URIRef(XSD + p.range_local))
        )

    return g


def build_data_graph(
    vault_dir: Path = DEFAULT_VAULT, registry_path: Path = DEFAULT_REGISTRY
) -> tuple[Graph, list[tuple[str, list[str]]]]:
    """The instance layer → ``data.ttl``. Returns ``(graph, flagged-unmapped-keys)``.

    Every surfaced note becomes a typed subject; each frontmatter field mapped by the context
    becomes a triple (datatype supplied by the context, ``sources`` → ``az:restsOn`` object
    links to the L1 notes); the note's true path travels as ``vld:path`` (roundtrip face).
    Unmapped keys are collected and flagged by the caller, never dropped silently (SPEC §5.6).
    """
    from rdflib import Graph, Literal, URIRef
    from rdflib.namespace import RDF

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    skip_keys = held_source_keys(registry)
    skip_briefs = held_brief_files(registry)

    terms = load_context_terms(vault_dir)
    source_iri_by_key = _latest_source_iri_by_key(vault_dir, skip_keys)
    notes = _discover_notes(vault_dir, skip_keys, skip_briefs)

    g: Graph = Graph()
    _bind_namespaces(g)
    vld_path = URIRef(VLD_BASE + "path")
    flagged: list[tuple[str, list[str]]] = []

    for note in notes:
        subj = URIRef(note.iri)
        g.add((subj, RDF.type, URIRef(ONT_BASE + note.class_local)))
        g.add((subj, vld_path, Literal(note.rel_path)))

        unmapped: list[str] = []
        for key, raw in note.fm.items():
            if key in (
                "type",
                "id",
            ):  # the type is the class edge (already asserted); id is identity
                continue
            mapping = terms.get(key)
            if mapping is None:
                unmapped.append(key)
                continue
            pred_iri, datatype = mapping
            pred = URIRef(pred_iri)
            if datatype == "@id":  # object property — resolve each referenced note to its IRI
                for ref_key in _parse_list(raw):
                    target = source_iri_by_key.get(ref_key)
                    if target is None:  # dangling reference (held / absent) — preserve the edge
                        target = _mint(f"sources/{ref_key}")
                    g.add((subj, pred, URIRef(target)))
            elif datatype:  # typed literal (e.g. xsd:dateTime)
                g.add((subj, pred, Literal(raw, datatype=URIRef(datatype))))
            else:  # plain string literal
                g.add((subj, pred, Literal(raw)))
        if unmapped:
            flagged.append((note.rel_path, unmapped))

    return g, flagged


# --- export + validate --------------------------------------------------------------------


def _validate(schema: Graph, data: Graph) -> None:
    """Re-serialise + re-parse both graphs (well-formedness) and assert non-empty layers."""
    from rdflib import Graph

    if len(schema) == 0:
        raise ValueError("schema graph is empty — the ontology failed to emit")
    if len(data) == 0:
        raise ValueError("data graph is empty — no participating notes were lifted")
    for g in (schema, data):  # a malformed serialization raises on re-parse
        Graph().parse(data=g.serialize(format="turtle"), format="turtle")


def export(
    out_dir: Path,
    vault_dir: Path = DEFAULT_VAULT,
    registry_path: Path = DEFAULT_REGISTRY,
    *,
    write: bool = True,
) -> tuple[Graph, Graph, list[tuple[str, list[str]]]]:
    """Build (and optionally write) ``schema.ttl`` + ``data.ttl`` + the composed context.

    Returns ``(schema_graph, data_graph, flagged)``. With ``write=False`` nothing touches
    disk — the ``--check`` gate builds + validates in-memory only.
    """
    schema = build_schema_graph()
    data, flagged = build_data_graph(vault_dir, registry_path)
    _validate(schema, data)

    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "schema.ttl").write_text(schema.serialize(format="turtle"), encoding="utf-8")
        (out_dir / "data.ttl").write_text(data.serialize(format="turtle"), encoding="utf-8")
        # Ship the composed context beside the .ttl so the published graph is self-describing.
        (out_dir / "ontology").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(vault_dir / ROOT_CONTEXT, out_dir / ROOT_CONTEXT)
        shutil.copyfile(
            vault_dir / "ontology" / "azimuth.context.jsonld",
            out_dir / "ontology" / "azimuth.context.jsonld",
        )
    return schema, data, flagged


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lift the azimuth OKF bundle into RDF (schema.ttl + data.ttl) via Vault-LD."
    )
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="build + validate the export in-memory, write nothing (CI gate)",
    )
    args = parser.parse_args(argv)
    out_dir = (_REPO_ROOT / args.out).resolve()

    try:
        schema, data, flagged = export(out_dir, write=not args.check)
    except (
        Exception
    ) as exc:  # surface any export failure (incl. missing rdflib) as a non-zero gate
        print(f"linked-data export FAILED: {exc}")
        return 1

    for rel_path, keys in flagged:  # SPEC §5.6 — flag unmapped constructs, never drop
        print(
            f"  flagged (not emitted; add to the context to promote): {rel_path}: {', '.join(keys)}"
        )

    where = "validated (no write)" if args.check else f"written to {out_dir}"
    n_inst = sum(1 for _ in data.subjects(unique=True))
    print(
        f"linked-data export {where}: schema.ttl {len(schema)} triples "
        f"({len(_CLASSES)} classes, {len(_PROPS)} properties), "
        f"data.ttl {len(data)} triples across {n_inst} note subjects."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
