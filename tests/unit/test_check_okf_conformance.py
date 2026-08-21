"""Tests for the OKF-conformance gate (scripts/check_okf_conformance.py).

Two load-bearing halves, the same shape as the other gate tests:
  (a) the gate has TEETH -- a concept missing/mismatching ``type``, a missing reserved
      ``index.md`` / ``log.md``, or an ``index.md`` that illegally carries frontmatter all
      turn the verdict RED; and
  (b) it does NOT false-positive on the legitimate constructs the bundle uses -- ``README.md``
      is a human landing page, not a concept, so a README without ``type`` must never flag,
      and a bundle that meets the SPEC-minimal bar reports CONFORMANT with exit 0.
A conformance gate that passes because it scanned nothing is worse than none.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_okf_conformance", _REPO_ROOT / "scripts" / "check_okf_conformance.py"
)
assert _spec and _spec.loader
okf = importlib.util.module_from_spec(_spec)
sys.modules["check_okf_conformance"] = okf
_spec.loader.exec_module(okf)


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _make_conformant_bundle(root: Path) -> None:
    """A minimal bundle that meets the OKF SPEC-minimal bar this gate enforces."""
    # concepts -- one per layer, each with a folder-correct type
    _write(root, "00 Rules/editorial.md", "---\ntype: L3-rule\n---\n\n# Editorial\n")
    _write(
        root,
        "01 Sources/2026-01-01/quakes.md",
        '---\ntype: "L1-source"\nsource_key: "quakes"\n---\n\n# Quakes\n',
    )
    _write(
        root,
        "02 Briefs/Energy Supply Weekly.md",
        "---\ntitle: Energy Supply Weekly\ntype: L2-brief\n---\n\n# Energy\n",
    )
    # human landing pages -- NOT concepts, carry no type on purpose
    for folder in (".", "00 Rules", "01 Sources", "02 Briefs"):
        rel = "README.md" if folder == "." else f"{folder}/README.md"
        _write(root, rel, "# Readme (human landing page)\n")
    # reserved OKF files -- index.md is a plain listing (no frontmatter); log.md at root
    for folder in okf.INDEX_DIRS:
        rel = "index.md" if folder == "." else f"{folder}/index.md"
        _write(root, rel, "# Index\n\n- [a](a.md)\n")
    _write(root, "log.md", "# Changelog\n\n## 2026-01-01\n- init\n")


def test_conformant_bundle_passes(tmp_path: Path) -> None:
    _make_conformant_bundle(tmp_path)
    report = okf.evaluate(tmp_path)
    assert report.conformant, [(r.check_id, r.detail) for r in report.results if not r.passed]
    # every layer's concept was actually scanned -- the gate has something to bite on
    assert report.concepts_scanned == 3
    assert okf.main(["--vault", str(tmp_path)]) == 0


def test_readme_is_not_a_concept(tmp_path: Path) -> None:
    """A README without a type must never flag -- it is a landing page, not a concept."""
    _make_conformant_bundle(tmp_path)
    # add a second README with no frontmatter deep in the source tree
    _write(tmp_path, "01 Sources/2026-01-01/README.md", "# folder readme\n")
    report = okf.evaluate(tmp_path)
    assert report.conformant
    # readme did not inflate the concept count
    assert report.concepts_scanned == 3


def test_missing_type_flagged(tmp_path: Path) -> None:
    _make_conformant_bundle(tmp_path)
    _write(tmp_path, "01 Sources/2026-01-01/quakes.md", "---\nsource_key: q\n---\n\n# Q\n")
    report = okf.evaluate(tmp_path)
    type_result = next(r for r in report.results if r.check_id == "type")
    assert not type_result.passed
    assert not report.conformant
    assert okf.main(["--vault", str(tmp_path)]) == 1


def test_type_mismatch_flagged(tmp_path: Path) -> None:
    """A concept in the wrong folder-for-its-type is a mismatch, not just a miss."""
    _make_conformant_bundle(tmp_path)
    _write(
        tmp_path,
        "01 Sources/2026-01-01/quakes.md",
        "---\ntype: L2-brief\n---\n\n# wrong layer\n",
    )
    report = okf.evaluate(tmp_path)
    type_result = next(r for r in report.results if r.check_id == "type")
    assert not type_result.passed
    assert any("want 'L1-source'" in v for v in type_result.violations)


def test_missing_index_flagged(tmp_path: Path) -> None:
    _make_conformant_bundle(tmp_path)
    (tmp_path / "02 Briefs" / "index.md").unlink()
    report = okf.evaluate(tmp_path)
    idx = next(r for r in report.results if r.check_id == "reserved-index")
    assert not idx.passed
    assert "02 Briefs/index.md" in idx.detail


def test_missing_log_flagged(tmp_path: Path) -> None:
    _make_conformant_bundle(tmp_path)
    (tmp_path / "log.md").unlink()
    report = okf.evaluate(tmp_path)
    log = next(r for r in report.results if r.check_id == "reserved-log")
    assert not log.passed


def test_index_with_frontmatter_flagged(tmp_path: Path) -> None:
    """index.md is a plain listing (SPEC 6); frontmatter on it is a hygiene violation."""
    _make_conformant_bundle(tmp_path)
    _write(tmp_path, "index.md", "---\ntype: L2-brief\n---\n\n# not a concept\n")
    report = okf.evaluate(tmp_path)
    hygiene = next(r for r in report.results if r.check_id == "index-hygiene")
    assert not hygiene.passed


def test_json_shape(tmp_path: Path) -> None:
    _make_conformant_bundle(tmp_path)
    payload = okf._to_dict(okf.evaluate(tmp_path))
    assert payload["conformant"] is True
    assert {c["id"] for c in payload["checks"]} == {  # type: ignore[union-attr]
        "type",
        "reserved-index",
        "reserved-log",
        "index-hygiene",
    }
