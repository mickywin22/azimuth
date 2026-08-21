#!/usr/bin/env python3
"""Done-test: azimuth is at the **explorable-RDF concept level** — the Career publish-gate precondition.

The W34 Azimuth KR1 stop_when has two halves, and its whole point is the gate it opens:
azimuth must stand *"at the same concept level as Emi v3"* before Career's publish
**double-gate** (Emi v3 working AND Azimuth at concept level) can open. This one command is
the machine-readable proof of the azimuth half — so *"Azimuth is at concept level"* stops
being a prose claim and becomes a green/red verdict the Career gate (and a human) can trust.

It rolls up, exit 0 iff every clause is GREEN:

  * **C1 OKF-conformant** — the ``vault/`` bundle meets OKF v0.1 SPEC-minimal in **frontmatter
    and filenames** (``type`` on every concept + reserved ``index.md`` / ``log.md``), via
    ``check_okf_conformance``. The "queryable" substrate the explorer sits on.
  * **C2 explorer present** — ``site/linked-data.html`` + ``site/linked-data.json`` are
    committed (the served surface), not deploy-only.
  * **C3 explorer in sync** — ``build_linked_data.py --check`` is green: the committed
    explorer matches the live vault (no stale concept counts).
  * **C4 concept-level shape** — the projection carries the RDF **concept** model: the 3 OKF
    layer classes, the 10 typed properties, ≥1 walkable ``rests-on`` edge and ≥1 cross-brief
    bridge, with the census internally consistent (per-class subjects sum to the total).
  * **C5 discoverable** — the explorer carries the site nav (its own entry marked current) and
    the site shell links to it, so it is not a hidden URL.
  * **C6 RDF substrate committed** — the Vault-LD composed context
    (``vault/context.jsonld`` + the ontology context) ships in the repo, so the graph is
    self-describing and the ``.ttl`` / SPARQL "queryable" half is reproducible.

This is azimuth-repo-scoped by design: it proves the fleet-owned Azimuth precondition. It does
**not** assert Emi v3's own half of the double-gate, and it never touches the Career track's
state — opening the gate stays the Career/PM lane.

Usage:
    python scripts/check_explorable.py           # human report, exit 0 iff at concept level
    python scripts/check_explorable.py --json     # machine-readable verdict
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT), str(_SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import build_linked_data  # noqa: E402  (sibling script)
import check_okf_conformance  # noqa: E402  (sibling script)

_VAULT = _REPO_ROOT / "vault"
_SITE = _REPO_ROOT / "site"
_SITE_BUILD = _REPO_ROOT / "synthesis" / "site_build.py"
_LD_HTML = _SITE / "linked-data.html"
_LD_JSON = _SITE / "linked-data.json"


@dataclass
class Clause:
    cid: str
    name: str
    passed: bool
    detail: str


@dataclass
class Verdict:
    clauses: list[Clause] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.passed for c in self.clauses)


def _c1_okf() -> Clause:
    report = check_okf_conformance.evaluate(_VAULT)
    failed = [r.check_id for r in report.results if not r.passed]
    return Clause(
        "C1",
        "OKF-conformant frontmatter + filenames",
        report.conformant,
        (
            f"CONFORMANT — {report.concepts_scanned} concepts, type + reserved index.md/log.md"
            if report.conformant
            else f"NON-CONFORMANT — fix: {', '.join(failed)}"
        ),
    )


def _c2_present() -> Clause:
    missing = [p.name for p in (_LD_HTML, _LD_JSON) if not p.is_file()]
    return Clause(
        "C2",
        "explorer committed (served surface)",
        not missing,
        "site/linked-data.html + .json present"
        if not missing
        else f"missing: {', '.join(missing)}",
    )


def _c3_in_sync() -> Clause:
    stale = build_linked_data.check(_SITE)
    return Clause(
        "C3",
        "explorer in sync with the live vault",
        not stale,
        "build_linked_data --check green"
        if not stale
        else f"STALE ({', '.join(stale)}) — run build_linked_data.py",
    )


def _c4_concept_level() -> Clause:
    if not _LD_JSON.is_file():
        return Clause("C4", "concept-level RDF shape", False, "linked-data.json absent")
    d = json.loads(_LD_JSON.read_text(encoding="utf-8"))
    counts = d.get("counts", {})
    census = d.get("census", [])
    subj_sum = sum(c.get("subjects", 0) for c in census)
    problems: list[str] = []
    if counts.get("classes") != 3:
        problems.append(f"classes={counts.get('classes')} (want 3 OKF layers)")
    if counts.get("properties") != 10:
        problems.append(f"properties={counts.get('properties')} (want 10 typed)")
    if not counts.get("restsOn_edges", 0) > 0:
        problems.append("no rests-on edges (graph is not walkable)")
    if not counts.get("bridges", 0) > 0:
        problems.append("no cross-brief bridges (USP surface missing)")
    if subj_sum != counts.get("subjects"):
        problems.append(f"census sum {subj_sum} != subjects {counts.get('subjects')}")
    return Clause(
        "C4",
        "concept-level RDF shape (classes · properties · edges · bridges)",
        not problems,
        (
            f"{counts.get('concepts_shown')} concepts · {counts.get('classes')} classes · "
            f"{counts.get('properties')} properties · {counts.get('restsOn_edges')} rests-on · "
            f"{counts.get('bridges')} bridges"
            if not problems
            else "; ".join(problems)
        ),
    )


def _c5_discoverable() -> Clause:
    problems: list[str] = []
    if _LD_HTML.is_file():
        html = _LD_HTML.read_text(encoding="utf-8")
        if '<a href="linked-data.html" aria-current="page">Linked data</a>' not in html:
            problems.append("explorer page missing its own current nav entry")
    else:
        problems.append("linked-data.html absent")
    if _SITE_BUILD.is_file():
        shell = _SITE_BUILD.read_text(encoding="utf-8")
        if "linked-data.html" not in shell:
            problems.append("site shell (site_build.py) does not link the explorer")
    else:
        problems.append("synthesis/site_build.py absent")
    return Clause(
        "C5",
        "discoverable from the site nav",
        not problems,
        "nav entry on the page + linked from the site shell"
        if not problems
        else "; ".join(problems),
    )


def _c6_substrate() -> Clause:
    ctx = _VAULT / "context.jsonld"
    ont = _VAULT / "ontology" / "azimuth.context.jsonld"
    missing = [p.name for p in (ctx, ont) if not p.is_file()]
    return Clause(
        "C6",
        "RDF substrate committed (self-describing context)",
        not missing,
        "context.jsonld + azimuth.context.jsonld present"
        if not missing
        else f"missing: {', '.join(missing)}",
    )


def evaluate() -> Verdict:
    v = Verdict()
    v.clauses.extend(
        [
            _c1_okf(),
            _c2_present(),
            _c3_in_sync(),
            _c4_concept_level(),
            _c5_discoverable(),
            _c6_substrate(),
        ]
    )
    return v


def render(v: Verdict) -> str:
    lines = [
        "",
        "azimuth — explorable-RDF concept level (Career publish-gate Azimuth precondition)",
        "=" * 78,
    ]
    for c in v.clauses:
        lines.append(f"  [{'GREEN' if c.passed else 'RED  '}] {c.cid} {c.name}")
        lines.append(f"          {c.detail}")
    lines.append("=" * 78)
    if v.ok:
        lines.append(
            "RESULT: AT CONCEPT LEVEL — the Azimuth precondition of Career's publish "
            "double-gate is demonstrably met."
        )
    else:
        red = ", ".join(c.cid for c in v.clauses if not c.passed)
        lines.append(f"RESULT: NOT YET — {red} red; the Azimuth publish precondition is not met.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Prove azimuth is at the explorable-RDF concept level (Career publish precondition)."
    )
    ap.add_argument("--json", action="store_true", help="emit the verdict as JSON")
    ns = ap.parse_args(argv)
    v = evaluate()
    if ns.json:
        print(
            json.dumps(
                {
                    "at_concept_level": v.ok,
                    "clauses": [
                        {"id": c.cid, "name": c.name, "passed": c.passed, "detail": c.detail}
                        for c in v.clauses
                    ],
                },
                indent=2,
            )
        )
    else:
        print(render(v))
    return 0 if v.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
