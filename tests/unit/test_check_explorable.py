"""Tests for the concept-level done-test (scripts/check_explorable.py).

``check_explorable.py`` is the one-command roll-up that proves azimuth stands at the
**explorable-RDF concept level** — the fleet-owned Azimuth precondition of Career's publish
double-gate. It is the artifact the W34 Azimuth KR1 stop_when points at ("the Career publish
gate's Azimuth precondition demonstrably met"), so it needs the same regression teeth every
other gate carries: a future edit must not be able to silently turn the precondition RED
(or, worse, keep it green while a clause has actually broken).

Its C1 (OKF conformance) and C3 (explorer-in-sync) clauses are separately covered by
``test_check_okf_conformance`` / ``test_build_linked_data`` and are re-exercised here only via
the live-repo aggregate. The teeth below target the clauses **no other gate covers** — C2
(explorer committed), C4 (concept-level RDF shape), C5 (discoverable nav), C6 (RDF substrate) —
plus the aggregate verdict logic.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_explorable", _REPO_ROOT / "scripts" / "check_explorable.py"
)
assert _spec and _spec.loader
ce = importlib.util.module_from_spec(_spec)
sys.modules["check_explorable"] = ce
_spec.loader.exec_module(ce)


# ---------------------------------------------------------------------------------------------
# The live repo really is at concept level. This pins the delivered green state and regresses
# if ANY clause's dependency breaks (a dropped nav link, a stale explorer, a missing context).
# ---------------------------------------------------------------------------------------------
def test_live_repo_is_at_concept_level() -> None:
    v = ce.evaluate()
    assert v.ok, "RED clauses: " + "; ".join(
        f"{c.cid} {c.name} — {c.detail}" for c in v.clauses if not c.passed
    )
    # all six named clauses are present, in order — a dropped clause is a silently weaker gate
    assert [c.cid for c in v.clauses] == ["C1", "C2", "C3", "C4", "C5", "C6"]
    assert ce.main([]) == 0
    assert ce.main(["--json"]) == 0


def test_verdict_aggregation_needs_every_clause() -> None:
    green = [ce.Clause(f"C{i}", f"clause {i}", True, "ok") for i in range(1, 7)]
    assert ce.Verdict(green).ok is True
    green[3] = ce.Clause("C4", "clause 4", False, "broke")
    assert ce.Verdict(green).ok is False


# ---------------------------------------------------------------------------------------------
# C2 — the explorer must be COMMITTED (served surface), not deploy-only.
# ---------------------------------------------------------------------------------------------
def test_c2_flags_missing_explorer(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_HTML", tmp_path / "nope.html")
    monkeypatch.setattr(ce, "_LD_JSON", tmp_path / "nope.json")
    assert ce._c2_present().passed is False

    (tmp_path / "linked-data.html").write_text("x", encoding="utf-8")
    (tmp_path / "linked-data.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(ce, "_LD_HTML", tmp_path / "linked-data.html")
    monkeypatch.setattr(ce, "_LD_JSON", tmp_path / "linked-data.json")
    assert ce._c2_present().passed is True


# ---------------------------------------------------------------------------------------------
# C4 — the concept-level RDF shape: 3 OKF classes, 10 typed properties, walkable edges, ≥1
# cross-brief bridge, and a census that sums to the subject total.
# ---------------------------------------------------------------------------------------------
def _write_ld_json(path: Path, **overrides: object) -> Path:
    counts = {
        "classes": 3,
        "properties": 10,
        "restsOn_edges": 5,
        "bridges": 2,
        "subjects": 10,
        "concepts_shown": 8,
    }
    counts.update(overrides)  # type: ignore[arg-type]
    census = [{"subjects": 6}, {"subjects": 3}, {"subjects": 1}]  # sums to 10
    path.write_text(json.dumps({"counts": counts, "census": census}), encoding="utf-8")
    return path


def test_c4_passes_on_a_well_formed_shape(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_JSON", _write_ld_json(tmp_path / "ld.json"))
    assert ce._c4_concept_level().passed is True


def test_c4_flags_wrong_class_count(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_JSON", _write_ld_json(tmp_path / "ld.json", classes=2))
    c = ce._c4_concept_level()
    assert c.passed is False and "classes=2" in c.detail


def test_c4_flags_wrong_property_count(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_JSON", _write_ld_json(tmp_path / "ld.json", properties=9))
    assert ce._c4_concept_level().passed is False


def test_c4_flags_unwalkable_graph(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_JSON", _write_ld_json(tmp_path / "ld.json", restsOn_edges=0))
    c = ce._c4_concept_level()
    assert c.passed is False and "rests-on" in c.detail


def test_c4_flags_no_bridges(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_JSON", _write_ld_json(tmp_path / "ld.json", bridges=0))
    c = ce._c4_concept_level()
    assert c.passed is False and "bridge" in c.detail


def test_c4_flags_census_mismatch(tmp_path: Path, monkeypatch) -> None:
    # census sums to 10 but the count claims 99 — a projection that lost/gained subjects
    monkeypatch.setattr(ce, "_LD_JSON", _write_ld_json(tmp_path / "ld.json", subjects=99))
    c = ce._c4_concept_level()
    assert c.passed is False and "census" in c.detail


def test_c4_flags_absent_json(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_LD_JSON", tmp_path / "absent.json")
    assert ce._c4_concept_level().passed is False


# ---------------------------------------------------------------------------------------------
# C5 — the explorer must be discoverable: its own current nav entry on the page AND a link
# from the site shell, so it is never a hidden URL.
# ---------------------------------------------------------------------------------------------
_NAV = '<a href="linked-data.html" aria-current="page">Linked data</a>'


def test_c5_flags_missing_page_nav(tmp_path: Path, monkeypatch) -> None:
    html = tmp_path / "linked-data.html"
    html.write_text("<html>no nav here</html>", encoding="utf-8")
    shell = tmp_path / "site_build.py"
    shell.write_text('nav = "linked-data.html"', encoding="utf-8")
    monkeypatch.setattr(ce, "_LD_HTML", html)
    monkeypatch.setattr(ce, "_SITE_BUILD", shell)
    assert ce._c5_discoverable().passed is False


def test_c5_flags_shell_not_linking(tmp_path: Path, monkeypatch) -> None:
    html = tmp_path / "linked-data.html"
    html.write_text(f"<html>{_NAV}</html>", encoding="utf-8")
    shell = tmp_path / "site_build.py"
    shell.write_text("nav = 'graph.html'  # explorer not linked", encoding="utf-8")
    monkeypatch.setattr(ce, "_LD_HTML", html)
    monkeypatch.setattr(ce, "_SITE_BUILD", shell)
    assert ce._c5_discoverable().passed is False


def test_c5_passes_when_discoverable(tmp_path: Path, monkeypatch) -> None:
    html = tmp_path / "linked-data.html"
    html.write_text(f"<html>{_NAV}</html>", encoding="utf-8")
    shell = tmp_path / "site_build.py"
    shell.write_text('nav.append("linked-data.html")', encoding="utf-8")
    monkeypatch.setattr(ce, "_LD_HTML", html)
    monkeypatch.setattr(ce, "_SITE_BUILD", shell)
    assert ce._c5_discoverable().passed is True


# ---------------------------------------------------------------------------------------------
# C6 — the self-describing RDF substrate (the composed context) must ship in the repo.
# ---------------------------------------------------------------------------------------------
def test_c6_flags_missing_substrate(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(ce, "_VAULT", tmp_path)  # empty — no context.jsonld
    assert ce._c6_substrate().passed is False

    (tmp_path / "context.jsonld").write_text("{}", encoding="utf-8")
    (tmp_path / "ontology").mkdir()
    (tmp_path / "ontology" / "azimuth.context.jsonld").write_text("{}", encoding="utf-8")
    assert ce._c6_substrate().passed is True


# ---------------------------------------------------------------------------------------------
# The rendered report tells the truth in both directions.
# ---------------------------------------------------------------------------------------------
def test_render_names_the_red_clause() -> None:
    v = ce.Verdict(
        [
            ce.Clause("C1", "ok clause", True, "fine"),
            ce.Clause("C4", "broken clause", False, "shape wrong"),
        ]
    )
    text = ce.render(v)
    assert "NOT YET" in text and "C4" in text


def test_render_confirms_when_green() -> None:
    v = ce.Verdict([ce.Clause("C1", "ok", True, "fine")])
    assert "AT CONCEPT LEVEL" in ce.render(v)
