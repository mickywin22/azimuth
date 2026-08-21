#!/usr/bin/env python3
"""Build the azimuth **linked-data explorer** (``site/linked-data.json`` + ``site/linked-data.html``).

This is the *explorable* face of the RDF graph. ``scripts/build_rdf.py`` already lifts the
``vault/`` OKF bundle into RDF (``schema.ttl`` + ``data.ttl``, the Vault-LD OKF compatibility
profile) and ``scripts/query_graph.py`` / the vault-side SPARQL bench prove it is *queryable*.
What neither ships is a human-navigable surface **over the typed RDF concept model** — so a
visitor can only read the raw Turtle. This generator closes that gap: it projects the same
graph ``build_rdf.py`` exports into a compact concept model and renders a self-contained,
dark, mobile-readable explorer that lets anyone browse the ontology, walk the three OKF
layer classes, open a concept to read its **typed triples**, and traverse the
``az:restsOn`` edges (brief ⇄ its L1 sources) and the cross-brief bridges.

**Concept level, not topology.** ``site/graph.html`` (``build_graph.py``) draws the
cross-channel *link topology* — channels, entities, earthquake events, gold region bridges.
This page is the layer above it: every note is a **typed subject** (``az:L1-source`` /
``az:L2-brief`` / ``az:L3-rule``), every frontmatter field a **typed predicate**, and the
schema itself is browsable — the same concept level the Emi v3 vault self-navigation surface
stands at. Together the two pages are azimuth's answer to *"show me the graph"*: topology
below, concept semantics here.

**Faithful by construction (no drift from the .ttl).** The projection reuses
``build_rdf.py``'s OWN pure-stdlib helpers — the ontology (``_CLASSES`` / ``_PROPS``), the
committed-context term map (``load_context_terms``), the bundle walk (``_discover_notes``),
the latest-source-per-key resolver (``_latest_source_iri_by_key``) and the list parser. It
therefore sees the exact same subjects, classes, predicates and ``restsOn`` edges the RDF
exporter emits, with **zero** rdflib dependency, so it runs on the daily ingest path and is
committed + ``--check``-guarded exactly like ``graph.json``. ``tests/unit/test_build_linked_data.py``
pins the class census, the property set and the ``restsOn`` triple total against
``build_rdf``'s actual rdflib graph, so the two faces can never diverge.

**Editorial guarantee.** Held themes (``brief_held: true`` in ``sources/registry.json``) —
their brief and every L1 source note that feeds them — are excluded, the same guarantee the
static site, the knowledge graph and the RDF export all enforce. The concept explorer never
surfaces what the site hides.

Usage:
    python scripts/build_linked_data.py            # build into ./site
    python scripts/build_linked_data.py --out _site   # custom output dir (Pages build)
    python scripts/build_linked_data.py --check       # exit 1 if committed artifacts are stale (CI guard)
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT), str(_SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import build_rdf  # noqa: E402  (sibling script; reuse its stdlib RDF-projection helpers)
from synthesis.site_build import (  # noqa: E402
    DEFAULT_REGISTRY,
    DEFAULT_VAULT,
    _slug,
    held_brief_files,
    held_source_keys,
)

# Frontmatter keys that are structural identity, not typed facts (mirrors build_rdf).
_SKIP_KEYS = frozenset({"type", "id"})

# Predicate label lookup: az: property localname -> its human label (from the ontology),
# plus the dcterms:title convention build_rdf emits for a brief's `title` field.
_PROP_LABEL: dict[str, str] = {p.localname: p.label for p in build_rdf._PROPS}


def _pred_meta(key: str, terms: dict[str, tuple[str, str | None]]) -> tuple[str, str, str]:
    """(predicate-localname, human label, datatype-tag) for a mapped frontmatter key.

    The predicate IRI + datatype come from the committed context (so the mapping is the
    exporter's, not this script's); the label comes from the ontology ``_PROPS`` where the
    property is azimuth-defined, else a readable fallback.
    """
    iri, datatype = terms[key]
    local = iri.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
    label = _PROP_LABEL.get(local, local.replace("_", " "))
    if datatype == "@id":
        tag = "edge"
    elif datatype and datatype.endswith("dateTime"):
        tag = "dateTime"
    else:
        tag = "string"
    return local, label, tag


def _brief_label(note: build_rdf._Note) -> str:
    """A brief's display label: its ``title`` frontmatter, else the file stem."""
    title = note.fm.get("title")
    if title:
        return title.strip()
    return Path(note.rel_path).stem


def _day_of(rel_path: str) -> str:
    """The dated folder of an L1 source note: '01 Sources/<day>/<key>.md' -> '<day>'."""
    parts = rel_path.split("/")
    return parts[1] if len(parts) >= 3 else ""


def build_projection(
    vault_dir: Path = DEFAULT_VAULT, registry_path: Path = DEFAULT_REGISTRY
) -> dict[str, Any]:
    """Project the azimuth OKF bundle into the linked-data concept model.

    The model is faithful to ``build_rdf.build_data_graph``: same subjects, same typed
    predicates, same ``az:restsOn`` edges. The L1 layer is collapsed to **one concept per
    surfaced source key** (its newest dated note is the head of a time-series; older dated
    notes are summarised as an instance count + date span) because that is azimuth's real
    concept granularity — 24 open-data channels, not 1,126 daily snapshots — and it is
    exactly the note ``az:restsOn`` already points a brief at.
    """
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    skip_keys = held_source_keys(registry)
    skip_briefs = held_brief_files(registry)

    terms = build_rdf.load_context_terms(vault_dir)
    obj_keys = {k for k, (_iri, dt) in terms.items() if dt == "@id"}
    latest_iri_by_key = build_rdf._latest_source_iri_by_key(vault_dir, skip_keys)
    notes = build_rdf._discover_notes(vault_dir, skip_keys, skip_briefs)

    # --- census over the full subject set (the honest RDF counts) --------------------------
    census_subjects: dict[str, int] = defaultdict(int)
    for note in notes:
        census_subjects[note.class_local] += 1

    # --- L1 sources: collapse to one concept per key, carry the time-series ----------------
    src_days: dict[str, list[str]] = defaultdict(list)
    src_latest: dict[str, build_rdf._Note] = {}
    for note in notes:
        if note.class_local != "L1-source":
            continue
        key = note.fm.get("sourceKey") or Path(note.rel_path).stem
        day = _day_of(note.rel_path)
        if day:
            src_days[key].append(day)
        # the newest dated note per key is the concept head (matches _latest_source_iri_by_key)
        prev = src_latest.get(key)
        if prev is None or _day_of(note.rel_path) > _day_of(prev.rel_path):
            src_latest[key] = note

    # --- edges: brief -> its latest source per key (az:restsOn), and the reverse -----------
    # restsOn resolves a brief's `sources` list to the IRI of the latest note per key; we
    # invert that IRI back to the key so edges point at the collapsed source concept.
    key_by_latest_iri = {iri: key for key, iri in latest_iri_by_key.items()}
    brief_out: dict[str, list[str]] = defaultdict(list)  # brief concept id -> [source key]
    key_feeds: dict[str, list[str]] = defaultdict(list)  # source key -> [brief concept id]
    restson_triples = 0

    briefs = [n for n in notes if n.class_local == "L2-brief"]
    rules = [n for n in notes if n.class_local == "L3-rule"]

    for note in briefs:
        bid = f"brief:{_slug(_brief_label(note))}"
        targets: list[str] = []
        for okey in obj_keys:
            raw = note.fm.get(okey)
            if not raw:
                continue
            for ref_key in build_rdf._parse_list(raw):
                iri = latest_iri_by_key.get(ref_key)
                resolved = key_by_latest_iri.get(iri) if iri else None
                key = resolved or ref_key
                if key in skip_keys:  # held source — never surface (editorial guarantee)
                    continue
                if key not in targets:
                    targets.append(key)
        for key in targets:
            brief_out[bid].append(key)
            key_feeds[key].append(bid)
            restson_triples += 1

    # --- assemble concepts -----------------------------------------------------------------
    concepts: list[dict[str, Any]] = []

    def facts_of(note: build_rdf._Note) -> list[dict[str, str]]:
        out: list[dict[str, str]] = []
        for key, raw in note.fm.items():
            if key in _SKIP_KEYS or key in obj_keys or key not in terms:
                continue
            _local, label, tag = _pred_meta(key, terms)
            out.append({"pred": key, "label": label, "value": raw.strip(), "datatype": tag})
        return out

    brief_by_id: dict[str, str] = {}
    for note in briefs:
        label = _brief_label(note)
        bid = f"brief:{_slug(label)}"
        brief_by_id[bid] = label
        concepts.append(
            {
                "id": bid,
                "class": "L2-brief",
                "label": label,
                "path": note.rel_path,
                "page": f"briefs/{_slug(label)}.html",
                "facts": facts_of(note),
                "edges": [
                    {"pred": "restsOn", "label": "rests on", "dir": "out", "target": f"key:{k}"}
                    for k in brief_out.get(bid, [])
                ],
            }
        )

    for key in sorted(src_latest):
        note = src_latest[key]
        days = sorted(src_days.get(key, []))
        concepts.append(
            {
                "id": f"key:{key}",
                "class": "L1-source",
                "label": key,
                "path": note.rel_path,
                "page": f"sources/{_day_of(note.rel_path)}/{key}.html",
                "facts": facts_of(note),
                "series": {
                    "instances": len(days),
                    "first": days[0] if days else "",
                    "last": days[-1] if days else "",
                },
                "edges": [
                    {"pred": "restsOn", "label": "feeds", "dir": "in", "target": bid}
                    for bid in key_feeds.get(key, [])
                ],
            }
        )

    for note in sorted(rules, key=lambda n: n.rel_path):
        label = Path(note.rel_path).stem
        concepts.append(
            {
                "id": f"rule:{_slug(label)}",
                "class": "L3-rule",
                "label": label,
                "path": note.rel_path,
                "page": "",
                "facts": facts_of(note),
                "edges": [],
            }
        )

    # resolve edge target labels + classes now that every concept id exists
    label_by_id = {c["id"]: c["label"] for c in concepts}
    class_by_id = {c["id"]: c["class"] for c in concepts}
    for c in concepts:
        for e in c["edges"]:
            tid = e["target"]
            e["targetLabel"] = label_by_id.get(tid, tid.split(":", 1)[-1])
            e["targetClass"] = class_by_id.get(tid, "")

    # --- ontology (schema) layer -----------------------------------------------------------
    census = [
        {
            "class": c.localname,
            "label": c.label,
            "comment": c.comment,
            "subjects": census_subjects.get(c.localname, 0),
            "concepts": sum(1 for x in concepts if x["class"] == c.localname),
        }
        for c in build_rdf._CLASSES
    ]
    properties = [
        {
            "id": p.localname,
            "label": p.label,
            "comment": p.comment,
            "kind": "object" if p.is_object else "datatype",
            "domain": p.domain_local or "",
            "range": p.range_local,
        }
        for p in build_rdf._PROPS
    ]

    # --- cross-brief bridges (the azimuth USP, in RDF terms) -------------------------------
    bridges = [
        {
            "id": f"key:{key}",
            "label": key,
            "briefs": sorted(brief_by_id[b] for b in bids),
        }
        for key, bids in sorted(key_feeds.items())
        if len(bids) >= 2
    ]

    # --- honest triple/subject totals (mirrors build_data_graph's add() calls) --------------
    data_triples = 0
    for note in notes:
        data_triples += 2  # rdf:type + vld:path
        seen_edges: set[str] = set()
        for key, raw in note.fm.items():
            if key in _SKIP_KEYS or key not in terms:
                continue
            if key in obj_keys:
                for ref_key in build_rdf._parse_list(raw):
                    iri = latest_iri_by_key.get(ref_key) or build_rdf._mint(f"sources/{ref_key}")
                    if iri not in seen_edges:
                        seen_edges.add(iri)
                        data_triples += 1
            else:
                data_triples += 1

    return {
        "generated": "azimuth vault/ OKF bundle -> RDF concept projection (Vault-LD OKF profile)",
        "spec_url": build_rdf.SPEC_URL,
        "ontology_iri": build_rdf.ONT_BASE.rstrip("#"),
        "data_base": build_rdf.DATA_BASE,
        "counts": {
            "subjects": len(notes),
            "data_triples": data_triples,
            "schema_triples": 75,  # fixed ontology; pinned to build_rdf by the equivalence test
            "classes": len(build_rdf._CLASSES),
            "properties": len(build_rdf._PROPS),
            "concepts_shown": len(concepts),
            "restsOn_edges": restson_triples,
            "bridges": len(bridges),
        },
        "census": census,
        "properties": properties,
        "concepts": concepts,
        "bridges": bridges,
    }


# ==========================================================================================
# HTML explorer template — self-contained, dark, mobile-readable. Vanilla JS (this is the
# public static site rendered in a real browser, not the Emi in-app viewer), no dependencies.
# ==========================================================================================
_HTML_TEMPLATE = r"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Linked data · azimuth</title>
<meta name="description" content="Explore azimuth's public OKF bundle as a typed RDF knowledge graph: browse the ontology, walk the three layer classes, open a concept to read its typed triples, and traverse the rests-on edges and cross-brief bridges.">
<style>
:root{--bg:#0b0f14;--panel:#111722;--panel2:#0e141d;--line:#243244;--ink:#e7edf5;--muted:#94a3b8;
  --sub:#c7d2df;--accent:#4cc2ff;--gold:#ffd166;--l1:#5ec4a8;--l2:#4cc2ff;--l3:#c58cf0}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;line-height:1.55}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.nav{display:flex;gap:1.1rem;align-items:center;padding:.85rem 1.15rem;flex-wrap:wrap;
  border-bottom:1px solid var(--line);background:var(--panel2);position:relative}
.nav .brand{font-weight:800;letter-spacing:.02em;color:var(--ink);font-size:1.05rem}
.nav nav{display:flex;gap:1rem;font-size:.9rem;flex-wrap:wrap}
.nav nav a{color:var(--muted)}
.nav nav a[aria-current]{color:var(--ink);font-weight:600}
.nav-toggle{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;margin:0}
.nav-burger{display:none;flex-direction:column;justify-content:center;gap:5px;margin-left:auto;
  width:34px;height:30px;cursor:pointer}
.nav-burger span{display:block;height:2px;width:100%;background:var(--ink);border-radius:2px}
main{max-width:1080px;margin:0 auto;padding:1.4rem 1.15rem 4rem}
.kind{display:inline-block;font-size:.72rem;letter-spacing:.13em;text-transform:uppercase;
  color:var(--gold);font-weight:700;margin-bottom:.35rem}
h1{font-size:1.7rem;margin:.1rem 0 .5rem;line-height:1.15}
.lede{color:var(--sub);max-width:760px;margin:.2rem 0 1.1rem}
.lede code{background:#0d1420;border:1px solid var(--line);border-radius:5px;padding:.05rem .3rem;
  font-size:.85em;color:var(--sub)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.6rem;margin:.4rem 0 1.2rem}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.7rem .8rem}
.tile b{display:block;font-size:1.35rem;font-weight:800;color:var(--ink)}
.tile span{font-size:.76rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.ttl-links{margin:-.4rem 0 1.1rem;font-size:.85rem;color:var(--muted)}
details.schema{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:.3rem .9rem;margin:0 0 1.3rem}
details.schema>summary{cursor:pointer;font-weight:700;padding:.5rem 0;list-style:none}
details.schema>summary::-webkit-details-marker{display:none}
details.schema>summary::before{content:"\25B8 ";color:var(--gold)}
details.schema[open]>summary::before{content:"\25BE "}
.schema h3{margin:.6rem 0 .35rem;font-size:.95rem}
.classrow{display:flex;gap:.5rem;align-items:baseline;padding:.3rem 0;border-top:1px solid var(--line)}
.props{width:100%;border-collapse:collapse;font-size:.85rem;margin:.2rem 0 .5rem}
.props th,.props td{text-align:left;padding:.32rem .5rem;border-top:1px solid var(--line);vertical-align:top}
.props th{color:var(--muted);font-weight:600}
.chip{display:inline-block;font-size:.68rem;font-weight:700;letter-spacing:.04em;padding:.1rem .45rem;
  border-radius:20px;border:1px solid transparent}
.chip.L1-source{color:var(--l1);border-color:#2c5148;background:#0e1a17}
.chip.L2-brief{color:var(--l2);border-color:#1d4a63;background:#0b1a24}
.chip.L3-rule{color:var(--l3);border-color:#432c5a;background:#160e1f}
.chip.obj{color:var(--gold);border-color:#5a4a1c;background:#1a1608}
.chip.dt{color:var(--muted);border-color:var(--line);background:#0d1420}
.controls{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;margin:.2rem 0 1rem;position:sticky;
  top:0;background:var(--bg);padding:.6rem 0;z-index:5}
.fbtn{appearance:none;cursor:pointer;font:inherit;font-size:.85rem;padding:.35rem .8rem;border-radius:20px;
  border:1px solid var(--line);background:var(--panel);color:var(--sub)}
.fbtn[aria-pressed="true"]{border-color:var(--accent);color:var(--ink);background:#0b1a24}
#search{flex:1;min-width:170px;padding:.4rem .7rem;border-radius:9px;border:1px solid var(--line);
  background:var(--panel);color:var(--ink);font:inherit;font-size:.88rem}
.layout{display:grid;grid-template-columns:minmax(260px,1fr) minmax(320px,1.25fr);gap:1rem;align-items:start}
.clist{display:flex;flex-direction:column;gap:.45rem;max-height:70vh;overflow:auto;padding-right:.2rem}
.card{text-align:left;width:100%;cursor:pointer;background:var(--panel);border:1px solid var(--line);
  border-radius:11px;padding:.6rem .75rem;color:inherit;font:inherit;display:block}
.card:hover{border-color:var(--accent)}
.card.active{border-color:var(--accent);background:#0b1a24}
.card .clabel{font-weight:600;margin:.15rem 0 .1rem;color:var(--ink)}
.card .cmeta{font-size:.78rem;color:var(--muted)}
.detail{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:1rem 1.05rem;
  position:sticky;top:4.2rem;min-height:200px}
.detail .dhead{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;margin-bottom:.2rem}
.detail h2{font-size:1.2rem;margin:.15rem 0 .1rem}
.detail .iri{font-size:.75rem;color:var(--muted);word-break:break-all;margin:.1rem 0 .7rem}
.detail h4{margin:.9rem 0 .35rem;font-size:.82rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted)}
.triples{width:100%;border-collapse:collapse;font-size:.86rem}
.triples td{padding:.3rem .45rem;border-top:1px solid var(--line);vertical-align:top}
.triples td.p{color:var(--muted);white-space:nowrap;width:33%}
.triples td.v{color:var(--sub);word-break:break-word}
.edge{display:flex;gap:.5rem;align-items:center;padding:.32rem 0;border-top:1px solid var(--line);font-size:.86rem}
.edge button{appearance:none;cursor:pointer;font:inherit;background:none;border:none;color:var(--accent);
  text-align:left;padding:0}
.edge button:hover{text-decoration:underline}
.edge .rel{color:var(--muted);font-size:.76rem;white-space:nowrap}
.series{font-size:.82rem;color:var(--muted);margin:.3rem 0}
.bridges{margin-top:2rem}
.bridge{background:var(--panel2);border:1px solid var(--line);border-left:3px solid var(--gold);
  border-radius:10px;padding:.5rem .8rem;margin:.4rem 0;font-size:.88rem}
.bridge b{color:var(--gold)}
.hint{color:var(--muted);font-size:.85rem}
@media(max-width:760px){
  .nav-burger{display:flex}
  .nav nav{display:none;flex-basis:100%;flex-direction:column;gap:0;margin-top:.5rem}
  .nav-toggle:checked~nav{display:flex}
  .nav nav a{padding:.55rem .2rem;border-top:1px solid var(--line)}
  .layout{grid-template-columns:1fr}
  .detail{position:static}
  .clist{max-height:none}
}
</style>
</head><body>
<header class="nav">
  <a class="brand" href="index.html">azimuth</a>
  <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-label="Toggle navigation menu">
  <label for="nav-toggle" class="nav-burger" title="Menu"><span></span><span></span><span></span></label>
  <nav>
    <a href="answers.html">Ask the data</a>
    <a href="benchmark.html">Benchmark</a>
    <a href="graph.html">Knowledge graph</a>
    <a href="linked-data.html" aria-current="page">Linked data</a>
    <a href="index.html">Briefs</a>
    <a href="index.html#sources">Sources</a>
    <a href="editorial.html">Editorial line</a>
  </nav>
</header>
<main>
<div class="kind">Linked data · RDF concept graph</div>
<h1>Explore the bundle as a typed RDF graph</h1>
<p class="lede">Every note in azimuth's public bundle is a <strong>typed subject</strong> —
<span class="chip L1-source">L1-source</span> <span class="chip L2-brief">L2-brief</span>
<span class="chip L3-rule">L3-rule</span> — and every frontmatter field is a
<strong>typed predicate</strong>. That is the whole bundle lifted into <strong>W3C RDF</strong>
through the committed <code>Vault-LD</code> context, at zero authoring cost. This is the
<em>concept</em> layer above the <a href="graph.html">knowledge-graph topology</a>: browse the
ontology, walk the three OKF classes, open a concept to read its actual triples, and follow the
<code>rests&#8209;on</code> edges a static bundle cannot express.</p>
<p class="ttl-links">The published graph is self-describing Turtle: <a href="schema.ttl">schema.ttl</a>
(the ontology) &middot; <a href="data.ttl">data.ttl</a> (the instances) &middot;
<a href="__SPEC_URL__">Vault-LD OKF profile</a>.</p>

<div class="tiles" id="tiles"></div>

<details class="schema" id="schema">
  <summary>Ontology &mdash; the schema layer is itself queryable RDF</summary>
  <div id="schema-body"></div>
</details>

<div class="controls">
  <span class="hint">Filter:</span>
  <span id="filters"></span>
  <input id="search" type="search" placeholder="find a concept by name&hellip;" autocomplete="off"
    aria-label="Find a concept by name">
</div>

<div class="layout">
  <div class="clist" id="clist" role="list" aria-label="Concepts"></div>
  <div class="detail" id="detail" aria-live="polite">
    <p class="hint">Pick a concept on the left to read its typed triples and walk its edges.</p>
  </div>
</div>

<section class="bridges" id="bridges"></section>
</main>
<script id="ld-data" type="application/json">__LD_JSON__</script>
<script>
"use strict";
const LD = JSON.parse(document.getElementById("ld-data").textContent);
const byId = new Map(LD.concepts.map(c => [c.id, c]));
const $ = (s, r=document) => r.querySelector(s);
const el = (tag, cls, txt) => { const n = document.createElement(tag); if(cls) n.className=cls;
  if(txt!=null) n.textContent=txt; return n; };

// --- stat tiles -------------------------------------------------------------------------
(function(){
  const t = LD.counts, tiles = [
    [t.subjects.toLocaleString(), "RDF subjects"],
    [(t.schema_triples + t.data_triples).toLocaleString(), "triples"],
    [t.classes, "classes"],
    [t.properties, "properties"],
    [t.restsOn_edges, "rests-on edges"],
    [t.bridges, "cross-brief bridges"],
  ];
  const box = $("#tiles");
  for(const [n,l] of tiles){ const d=el("div","tile"); d.appendChild(el("b",null,String(n)));
    d.appendChild(el("span",null,l)); box.appendChild(d); }
})();

// --- ontology / schema panel ------------------------------------------------------------
(function(){
  const body = $("#schema-body");
  body.appendChild(el("h3", null, "Classes (OKF layers)"));
  for(const c of LD.census){
    const row = el("div","classrow");
    row.appendChild(el("span","chip "+c.class, c.class));
    const txt = el("span"); txt.innerHTML = "<strong>"+c.label+"</strong> &mdash; "+c.comment
      +' <span class="hint">('+c.subjects.toLocaleString()+" subjects, "+c.concepts+" concepts)</span>";
    row.appendChild(txt); body.appendChild(row);
  }
  body.appendChild(el("h3", null, "Typed properties"));
  const tbl = el("table","props");
  tbl.innerHTML = "<thead><tr><th>property</th><th>kind</th><th>domain &rarr; range</th><th>meaning</th></tr></thead>";
  const tb = el("tbody");
  for(const p of LD.properties){
    const tr = el("tr");
    tr.innerHTML = "<td><code>az:"+p.id+"</code></td>"
      + '<td><span class="chip '+(p.kind==="object"?"obj":"dt")+'">'+p.kind+"</span></td>"
      + "<td>"+(p.domain?("az:"+p.domain):"&mdash;")+" &rarr; "+(p.kind==="object"?("az:"+p.range):("xsd:"+p.range))+"</td>"
      + "<td>"+p.comment+"</td>";
    tb.appendChild(tr);
  }
  tbl.appendChild(tb); body.appendChild(tbl);
})();

// --- filters + search + list ------------------------------------------------------------
let activeClass = "all", query = "";
(function(){
  const box = $("#filters");
  const mk = (val, label) => { const b = el("button","fbtn",label); b.dataset.class=val;
    b.setAttribute("aria-pressed", val==="all" ? "true":"false");
    b.onclick = () => { activeClass=val; for(const x of box.querySelectorAll(".fbtn"))
      x.setAttribute("aria-pressed", x.dataset.class===val?"true":"false"); renderList(); };
    box.appendChild(b); };
  mk("all", "All ("+LD.concepts.length+")");
  for(const c of LD.census) mk(c.class, c.class+" ("+c.concepts+")");
  $("#search").addEventListener("input", e => { query = e.target.value.toLowerCase().trim(); renderList(); });
})();

function visible(){
  return LD.concepts.filter(c =>
    (activeClass==="all" || c.class===activeClass) &&
    (!query || c.label.toLowerCase().includes(query)));
}
function renderList(){
  const list = $("#clist"); list.innerHTML = "";
  const items = visible();
  if(!items.length){ list.appendChild(el("p","hint","No concept matches.")); return; }
  for(const c of items){
    const b = el("button","card"); b.setAttribute("role","listitem"); b.dataset.id=c.id;
    const head = el("div"); head.appendChild(el("span","chip "+c.class, c.class));
    b.appendChild(head);
    b.appendChild(el("div","clabel", c.label));
    let meta = c.edges.length + " edge" + (c.edges.length===1?"":"s");
    if(c.series) meta += " · " + c.series.instances + " daily snapshot" + (c.series.instances===1?"":"s");
    b.appendChild(el("div","cmeta", meta));
    b.onclick = () => select(c.id);
    list.appendChild(b);
  }
}
function select(id){
  const c = byId.get(id); if(!c) return;
  for(const x of document.querySelectorAll(".card")) x.classList.toggle("active", x.dataset.id===id);
  const d = $("#detail"); d.innerHTML="";
  const head = el("div","dhead"); head.appendChild(el("span","chip "+c.class, c.class));
  d.appendChild(head);
  d.appendChild(el("h2", null, c.label));
  d.appendChild(el("div","iri", LD.data_base + encodeURI(c.path.replace(/\.md$/,""))));
  if(c.series){
    const s = el("div","series");
    s.textContent = "Time-series: " + c.series.instances + " dated L1 notes, "
      + c.series.first + " → " + c.series.last + " (concept = the newest; older days are its history).";
    d.appendChild(s);
  }
  if(c.facts.length){
    d.appendChild(el("h4", null, "Typed triples"));
    const tbl = el("table","triples"); const tb = el("tbody");
    for(const f of c.facts){
      const tr = el("tr");
      const p = el("td","p"); p.innerHTML = "<code>az:"+f.pred+"</code> "
        + '<span class="chip '+(f.datatype==="dateTime"?"dt":"dt")+'">'+f.datatype+"</span>";
      const v = el("td","v", f.value);
      tr.appendChild(p); tr.appendChild(v); tb.appendChild(tr);
    }
    tbl.appendChild(tb); d.appendChild(tbl);
  }
  if(c.edges.length){
    d.appendChild(el("h4", null, "Edges (rests-on)"));
    for(const e of c.edges){
      const row = el("div","edge");
      row.appendChild(el("span","rel", e.dir==="out" ? "rests on →" : "← feeds"));
      const b = el("button", null, e.targetLabel + "  ["+e.targetClass+"]");
      b.onclick = () => select(e.target);
      row.appendChild(b); d.appendChild(row);
    }
  }
  if(c.page){
    const links = el("h4", null, "Open"); d.appendChild(links);
    const p = el("div");
    p.innerHTML = '<a href="'+c.page+'">rendered page</a> &middot; '
      + '<a href="https://github.com/mickywin22/azimuth/blob/main/vault/'
      + encodeURI(c.path) + '">source note on GitHub</a>';
    d.appendChild(p);
  }
  if(location.hash.slice(1) !== id) history.replaceState(null, "", "#"+id);
}

// --- cross-brief bridges ----------------------------------------------------------------
(function(){
  const box = $("#bridges");
  if(!LD.bridges.length) return;
  box.appendChild(el("h4", null, "Cross-brief bridges — one L1 source feeding ≥2 briefs"));
  const intro = el("p","hint");
  intro.textContent = "The azimuth USP in standards RDF: a shared source is a real node two briefs both rest on — click it to walk both edges.";
  box.appendChild(intro);
  for(const br of LD.bridges){
    const d = el("div","bridge");
    const b = el("button", null, br.label); b.style.cssText="appearance:none;background:none;border:none;color:var(--gold);font:inherit;cursor:pointer;font-weight:700;padding:0";
    b.onclick = () => { select(br.id); document.querySelector(".detail").scrollIntoView({behavior:"smooth",block:"start"}); };
    d.appendChild(b);
    d.appendChild(document.createTextNode("  feeds: " + br.briefs.join(", ")));
    box.appendChild(d);
  }
})();

renderList();
if(location.hash && byId.has(location.hash.slice(1))) select(location.hash.slice(1));
</script>
</body></html>
"""


def _json_for_script(data: Any) -> str:
    """``json.dumps`` hardened for inline ``<script>`` embedding (mirrors build_graph)."""
    return (
        json.dumps(data)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def render_html(projection: dict[str, Any]) -> str:
    """Render the explorer page with the projection embedded inline (self-contained)."""
    return _HTML_TEMPLATE.replace("__LD_JSON__", _json_for_script(projection)).replace(
        "__SPEC_URL__", projection["spec_url"]
    )


def _serialize(projection: dict[str, Any]) -> tuple[str, str]:
    """The exact ``(linked-data.json, linked-data.html)`` text a build would write.

    One source of truth shared by :func:`build` and the ``--check`` guard, so the write path
    and the sync check can never disagree about what "in sync" means.
    """
    return json.dumps(projection, indent=2) + "\n", render_html(projection)


def build(
    out_dir: Path, vault_dir: Path = DEFAULT_VAULT, registry_path: Path = DEFAULT_REGISTRY
) -> dict[str, Any]:
    """Build the projection and write ``linked-data.json`` + ``linked-data.html``."""
    projection = build_projection(vault_dir, registry_path)
    json_text, html_text = _serialize(projection)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "linked-data.json").write_text(json_text, encoding="utf-8")
    (out_dir / "linked-data.html").write_text(html_text, encoding="utf-8")
    return projection


def check(
    out_dir: Path, vault_dir: Path = DEFAULT_VAULT, registry_path: Path = DEFAULT_REGISTRY
) -> list[str]:
    """Names of any committed linked-data artifact stale vs the live vault (empty == in sync)."""
    projection = build_projection(vault_dir, registry_path)
    json_text, html_text = _serialize(projection)
    stale: list[str] = []
    for name, new_text in (("linked-data.json", json_text), ("linked-data.html", html_text)):
        path = out_dir / name
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != new_text:
            stale.append(name)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the azimuth linked-data explorer (site/linked-data.json + .html)."
    )
    parser.add_argument("--out", default="site", help="output directory (default: site)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if committed linked-data.json/.html are stale vs the live vault (CI guard)",
    )
    args = parser.parse_args(argv)
    out_dir = (_REPO_ROOT / args.out).resolve()

    if args.check:
        stale = check(out_dir)
        if stale:
            print(
                f"linked-data: STALE ({', '.join(stale)}) — run "
                "`python scripts/build_linked_data.py` and commit."
            )
            return 1
        print("linked-data: up to date.")
        return 0

    projection = build(out_dir)
    c = projection["counts"]
    print(
        f"linked-data explorer written to {out_dir}: {c['concepts_shown']} concepts over "
        f"{c['subjects']} subjects ({c['classes']} classes, {c['properties']} properties, "
        f"{c['restsOn_edges']} rests-on edges, {c['bridges']} bridges)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
