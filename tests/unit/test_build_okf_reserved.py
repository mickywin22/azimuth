"""Tests for the reserved-OKF-file generator (scripts/build_okf_reserved.py).

The generator writes the two filenames OKF v0.1 reserves — ``index.md`` (per level) and
``log.md`` (root) — purely from committed data (layer folders, dated L1 day dirs, note
frontmatter), never the wall clock. The tests pin the two properties that keep it honest:

  (a) the ``--check`` gate has TEETH — a missing, stale, or hand-mutated reserved file turns
      it RED (exit 1), so the daily ingest can never let these drift silently; and
  (b) the output is DETERMINISTIC and OKF-hygienic — the same bundle yields byte-identical
      files on repeat (no clock), every generated ``index.md`` carries NO frontmatter (SPEC §6,
      the exact rule check_okf_conformance.py enforces), and ``log.md`` derives its headings
      from the dated day folders.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, _REPO_ROOT / rel)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


okfr = _load("build_okf_reserved", "scripts/build_okf_reserved.py")
okf = _load("check_okf_conformance", "scripts/check_okf_conformance.py")


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _make_bundle(root: Path) -> None:
    """A minimal bundle: 2 dated L1 days, 2 briefs (one themed), 1 rule."""
    _write(root, "00 Rules/editorial.md", "---\ntitle: Editorial Line\ntype: L3-rule\n---\n\n# Editorial\n")
    _write(root, "00 Rules/README.md", "# Rules readme\n")
    for day in ("2026-01-01", "2026-01-02"):
        _write(root, f"01 Sources/{day}/quakes.md", '---\ntype: "L1-source"\nsource_key: "quakes"\n---\n\n# Quakes\n')
        _write(root, f"01 Sources/{day}/energy.md", '---\ntype: "L1-source"\nsource_key: "energy"\n---\n\n# Energy\n')
    _write(root, "02 Briefs/Energy Supply Weekly.md", "---\ntitle: Energy Supply Weekly\ntype: L2-brief\ntheme: energy-supply\n---\n\n# Energy\n")
    _write(root, "02 Briefs/Geophysical Weekly.md", "---\ntitle: Geophysical Weekly\ntype: L2-brief\ntheme: geophysical\n---\n\n# Geo\n")
    _write(root, "02 Briefs/README.md", "# Briefs readme\n")
    _write(root, "README.md", "# azimuth (human landing page)\n")


def test_generate_produces_the_five_reserved_files(tmp_path: Path) -> None:
    _make_bundle(tmp_path)
    files = okfr.generate(tmp_path)
    got = {p.relative_to(tmp_path).as_posix() for p in files}
    assert got == {
        "index.md",
        "00 Rules/index.md",
        "01 Sources/index.md",
        "02 Briefs/index.md",
        "log.md",
    }


def test_check_passes_after_write(tmp_path: Path) -> None:
    _make_bundle(tmp_path)
    assert okfr.main(["--vault", str(tmp_path)]) == 0  # write
    assert okfr.main(["--check", "--vault", str(tmp_path)]) == 0  # in sync


def test_check_is_red_when_a_reserved_file_is_missing(tmp_path: Path) -> None:
    _make_bundle(tmp_path)
    okfr.main(["--vault", str(tmp_path)])
    (tmp_path / "log.md").unlink()
    assert okfr.main(["--check", "--vault", str(tmp_path)]) == 1


def test_check_is_red_when_a_reserved_file_is_stale(tmp_path: Path) -> None:
    """Hand-mutating a listing (or a new ingest day landing) must fail --check."""
    _make_bundle(tmp_path)
    okfr.main(["--vault", str(tmp_path)])
    (tmp_path / "01 Sources" / "index.md").write_text("# tampered\n", encoding="utf-8")
    assert okfr.main(["--check", "--vault", str(tmp_path)]) == 1


def test_check_is_red_after_a_new_ingest_day(tmp_path: Path) -> None:
    """A genuinely new L1 day must move log.md + the sources index — the ingest-drift case."""
    _make_bundle(tmp_path)
    okfr.main(["--vault", str(tmp_path)])
    _write(tmp_path, "01 Sources/2026-01-03/quakes.md", '---\ntype: "L1-source"\nsource_key: "quakes"\n---\n\n# Q\n')
    assert okfr.main(["--check", "--vault", str(tmp_path)]) == 1
    okfr.main(["--vault", str(tmp_path)])  # regenerate
    assert okfr.main(["--check", "--vault", str(tmp_path)]) == 0


def test_output_is_deterministic_no_clock(tmp_path: Path) -> None:
    _make_bundle(tmp_path)
    first = okfr.generate(tmp_path)
    second = okfr.generate(tmp_path)
    assert {p: c for p, c in first.items()} == {p: c for p, c in second.items()}


def test_generated_indexes_carry_no_frontmatter(tmp_path: Path) -> None:
    """The generator's own output must satisfy the conformance gate's index-hygiene rule."""
    _make_bundle(tmp_path)
    okfr.main(["--vault", str(tmp_path)])
    report = okf.evaluate(tmp_path)
    assert report.conformant, [(r.check_id, r.detail) for r in report.results if not r.passed]


def test_log_headings_are_iso_days_newest_first(tmp_path: Path) -> None:
    _make_bundle(tmp_path)
    log = okfr.generate(tmp_path)[tmp_path / "log.md"]
    assert log.index("## 2026-01-02") < log.index("## 2026-01-01")


def test_root_index_lists_layers_and_bundle_files(tmp_path: Path) -> None:
    _make_bundle(tmp_path)
    root = okfr.generate(tmp_path)[tmp_path / "index.md"]
    assert "00 Rules" in root and "01 Sources" in root and "02 Briefs" in root
    assert "log.md" in root and "README.md" in root
    # source count folds in both days (4 notes across 2 ingest days)
    assert "4 notes across 2 ingest days" in root
