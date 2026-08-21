# Linked data — the azimuth vault as an RDF graph (Vault-LD OKF profile)

azimuth's `vault/` is already an **OKF-style Markdown bundle**: a directory of notes, each
with YAML frontmatter, one required `type` per concept. That is *exactly* the physical shape a
[Vault-LD](https://github.com/The-Knowledge-Graph-Guys/vault-ld) vault has. What an OKF bundle
lacks is the **context** that gives its field names shared meaning. azimuth adds that context —
and nothing else — so the public vault becomes a real, queryable **RDF knowledge graph** at
near-zero authoring cost.

This is the lift defined by **Vault-LD SPEC Appendix B, the OKF compatibility profile**: an
untouched OKF bundle plus one composed context is already valid linked data.

> **Not just a shape — formal semantics.** `vault-graph` and the on-site knowledge graph
> ([build_graph.py](cli.md)) show link *topology*. The RDF lift adds *typed* semantics: every
> note is a subject with a declared class (`az:L1-source` / `az:L2-brief` / `az:L3-rule`), every
> frontmatter field is a typed predicate, and the whole thing speaks a vendor-neutral W3C
> standard (RDF / Turtle) any triple store or SPARQL engine can consume.

## What ships

| Artifact | Where | What it is |
|---|---|---|
| `context.jsonld` | `vault/context.jsonld` (source, committed) | The **root** composed context: the data `@base` + `@vocab`, the `type → @type` keyword alias (SPEC Appendix B step 1), the standard prefixes (`rdfs` `owl` `skos` `xsd` `dcterms` `sdo` `vld`), and the structural terms. Composes the ontology context below by reference. |
| `azimuth.context.jsonld` | `vault/ontology/azimuth.context.jsonld` (source, committed) | The **azimuth domain ontology** context: its namespace (`az:`) and the term definition for every azimuth frontmatter key (`retrieved → az:retrieved` typed `xsd:dateTime`, `sources → az:restsOn`, …). |
| `schema.ttl` | `site/schema.ttl` (generated, beside the site) | The **ontology / definitions** layer — the three layer classes and the typed properties (`rdfs:domain` / `rdfs:range` / labels / comments). |
| `data.ttl` | `site/data.ttl` (generated, beside the site) | The **instance** layer — every surfaced L1 source note, L2 brief and L3 rule as a typed subject, its frontmatter facts as triples, each note's true bundle path as a `vld:path` literal (so the export is a faithful roundtrip face, SPEC §5.4 step 7). |
| `linked-data.json` + `linked-data.html` | `site/linked-data.json` + `site/linked-data.html` (committed, `--check`-guarded) | The **explorable** face of the graph — a human-navigable concept explorer over the same typed model. See "The explorer" below. |

## The explorer — from queryable to explorable

The `.ttl` above make the bundle **queryable** (any SPARQL engine can consume them; the
vault-side bench proves 8 typed queries green). What they do not give a human visitor is a way
to *walk* the graph. [`scripts/build_linked_data.py`](cli.md) closes that: it projects the same
typed model into `site/linked-data.json` and renders a self-contained dark explorer
(`site/linked-data.html`, linked from every page's nav) where you browse the **ontology** (the 3
layer classes + 10 typed properties, itself queryable RDF), walk each OKF class, open a concept
to read its **typed triples**, and traverse the `az:restsOn` edges (brief ⇄ its L1 sources) and
the cross-brief bridges. This is the *concept* layer above the
[knowledge-graph topology](cli.md) — the same concept level Emi's own vault self-navigation
surface stands at.

**Faithful by construction.** The projection reuses `build_rdf.py`'s own stdlib helpers (the
ontology `_CLASSES`/`_PROPS`, the committed-context term map, the bundle walk, the
latest-source-per-key resolver), so it sees exactly the subjects, classes, predicates and
`restsOn` edges the RDF exporter emits — with **no rdflib dependency**, so it runs on the daily
ingest path and is committed + `--check`-guarded like the knowledge graph.
`tests/unit/test_build_linked_data.py` pins its class census, property set and `restsOn` triple
total against `build_rdf`'s actual rdflib graph, so the two faces can never diverge.

The exporter — [`scripts/build_rdf.py`](cli.md) — is a **conforming Vault-LD exporter** (SPEC
§5.4): it reads the mapping from the *committed context* (not from hard-coded knowledge), decides
each note's layer from its folder, mints one subject per note from the file name (SPEC §4.5), and
emits the two Turtle files split by layer. The composed context is copied beside the `.ttl` so the
published graph is **self-describing** — a consumer needs nothing but the three files.

## How to run it

```bash
# One-time: install the CI-only linked-data extra (rdflib). The runtime stays pure-stdlib.
uv pip install -e ".[ld]"

python scripts/build_rdf.py                 # export into ./site (beside the static site)
python scripts/build_rdf.py --out _site      # the Pages build uses _site
python scripts/build_rdf.py --check          # build + validate in-memory, write nothing (the CI gate)
```

## Design guarantees

- **No new runtime dependency.** `rdflib` lives only in the `ld` optional-dependency extra and is
  imported lazily inside the build functions. The ingest / guardrail / synthesis runtime stays
  pure standard library (`pyproject` `dependencies = []`). The export runs in the `linked-data` CI
  job and the (flip-gated) Pages build only — never on the daily ingest path.
- **The editorial line holds in RDF too.** A held theme (`brief_held: true` in
  `sources/registry.json`) — its brief and every L1 source note that feeds it — is excluded from
  the graph, the same guarantee the [static-site build](site.md) and the knowledge graph enforce.
  The RDF graph never surfaces what the site hides.
- **Flag, never drop.** A frontmatter key with no term in the context is *flagged* on export, not
  silently emitted and not silently lost (SPEC §5.6) — the same telemetry-integrity instinct the
  fleet retention rules follow. Promoting it is a one-line context edit.
- **The ontology can't drift from the context.** `tests/unit/test_build_rdf.py` pins every `az:`
  property the exporter emits to a definition in the committed ontology context, and vice-versa.

## Honest scope (what this lift does and does not do)

- It captures the **frontmatter** facts. Vault-LD's triples live in frontmatter only; a brief's
  in-body `[[wikilinks]]` stay navigational (SPEC §5.3, Appendix B step 5). Promoting body links to
  first-class edges is the deferred **Tier-2** step (the wikilink → standard-markdown-link
  migration in the [OKF strategy](strategy/okf-and-knowledge-graph.md)); it is intentionally *not*
  part of this lift.
- The Markdown vault stays the **source of truth**; the `.ttl` are a read-only generated face
  (SPEC §5.4). Edit the notes and regenerate — never patch the export.
- **Publishing waits for the public flip.** Building and committing the context in the repo is done
  now; the `.ttl` only appear on the public site once the Pages build runs post-flip (it is gated
  on the repo being public). Nothing here touches the flip gates.

See also: [cli.md](cli.md) for the command surface, [architecture.md](architecture.md) for how the
export sits beside the ingest → synthesis → site pipeline, and the
[OKF + knowledge-graph strategy](strategy/okf-and-knowledge-graph.md) for the two-tier conformance
plan this realises.
