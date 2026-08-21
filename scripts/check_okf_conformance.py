#!/usr/bin/env python3
"""OKF-conformance gate for the azimuth ``vault/`` bundle (Open Knowledge Format v0.1).

azimuth's public bundle is, by construction, ~70% of an OKF Knowledge Bundle already: a
directory tree of Markdown files with YAML frontmatter, distributed as a git repo (the whole
OKF thesis). This gate is the machine-readable proof of the remaining, buildable slice — the
**SPEC-minimal** conformance bar from ``docs/strategy/okf-and-knowledge-graph.md`` — so
"the azimuth public bundle is OKF-conformant in frontmatter and filenames" stops being a
prose claim and becomes a green/red check the flip runbook and CI can trust.

What OKF v0.1 SPEC-minimal actually requires (audited against the real ``SPEC.md`` in the
strategy doc), and what this gate enforces:

  * **``type`` on every concept (SPEC §4/§5, the ONLY mandatory frontmatter key).** Every
    concept note carries a ``type`` whose value matches the layer its folder declares —
    ``01 Sources`` -> ``L1-source``, ``02 Briefs`` -> ``L2-brief``, ``00 Rules`` ->
    ``L3-rule``. This is the same folder->layer mapping the RDF exporter (``build_rdf.py``,
    SPEC §5.4 step 5) already uses, so a green gate here means the frontmatter and the
    linked-data export agree on every note's class.
  * **Reserved ``index.md`` (SPEC §6).** A directory-listing / progressive-disclosure file at
    the bundle root and at each layer folder. Coexists with ``README.md`` (the human landing
    page); OKF consumers read ``index.md``, humans read ``README.md``.
  * **Reserved ``log.md`` (SPEC §7).** A chronological, newest-first update history at the
    bundle root, ISO ``YYYY-MM-DD`` date headings.
  * **Reserved-file hygiene.** ``index.md`` carries NO frontmatter (SPEC §6 — it is a plain
    listing, not a concept); the reserved names are used only for their reserved purpose.

Deliberately OUT of scope (documented, not silently skipped):
  * The wikilink -> standard-markdown-link migration (OKF §5 relationship form, gap **G4**) is
    the expensive **Tier-2** clause entangled with the synthesis lint + curator role. It is
    deferred behind the graph work (see the strategy doc) and is NOT gated here.
  * Filename *style* (kebab-case concept ids). The reserved names are enforced; existing
    brief filenames with spaces/capitals ("World Watch Weekly.md") are valid OKF concept ids
    (the id is the path, spaces percent-encode) and are NOT force-renamed — a rename would
    break every site/RDF/link consumer for zero conformance gain.

Pure stdlib — the azimuth runtime carries no third-party deps, so neither does its gate. The
frontmatter parser is reused from ``synthesis.lint`` (the same dependency-free scalar parser
the rest of the vault is written against), so this gate reads every note exactly as the
export and lint do.

Usage:
    python scripts/check_okf_conformance.py            # human report, exit 0 iff conformant
    python scripts/check_okf_conformance.py --json     # machine-readable verdict
    python scripts/check_okf_conformance.py --vault <path>   # explicit bundle root
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from synthesis.lint import split_frontmatter  # noqa: E402

DEFAULT_VAULT = _REPO_ROOT / "vault"

# folder (relative to the bundle root) -> the OKF `type` every concept in it must declare.
# This is the SPEC §5.4-step-5 folder->layer mapping the RDF exporter uses, kept in one place.
LAYER_BY_FOLDER: dict[str, str] = {
    "00 Rules": "L3-rule",
    "01 Sources": "L1-source",
    "02 Briefs": "L2-brief",
}

# Reserved OKF filenames — never treated as concept notes.
RESERVED_INDEX = "index.md"
RESERVED_LOG = "log.md"
RESERVED_NAMES: frozenset[str] = frozenset({RESERVED_INDEX, RESERVED_LOG, "readme.md"})

# Where the reserved files must exist (relative to the bundle root; "." == root).
INDEX_DIRS: tuple[str, ...] = (".", "00 Rules", "01 Sources", "02 Briefs")
LOG_DIRS: tuple[str, ...] = (".",)

# How many offending paths to name in the human report before collapsing to a count.
_SAMPLE = 5


@dataclass
class CheckResult:
    """Outcome of one conformance check."""

    check_id: str
    name: str
    passed: bool
    detail: str
    violations: list[str] = field(default_factory=list)


@dataclass
class Report:
    """Aggregate OKF-conformance verdict over the bundle."""

    vault: str
    concepts_scanned: int = 0
    results: list[CheckResult] = field(default_factory=list)

    @property
    def conformant(self) -> bool:
        return all(r.passed for r in self.results)


def _concept_files(vault: Path, folder: str) -> list[Path]:
    """Every concept ``.md`` under one layer folder (recursive), reserved names excluded."""
    root = vault / folder
    if not root.is_dir():
        return []
    return sorted(
        p for p in root.rglob("*.md") if p.is_file() and p.name.lower() not in RESERVED_NAMES
    )


def _rel(vault: Path, path: Path) -> str:
    """Bundle-relative POSIX path for stable, platform-independent reporting."""
    try:
        return path.relative_to(vault).as_posix()
    except ValueError:
        return path.as_posix()


def _sampled(violations: list[str]) -> str:
    """`n items: a, b, c, ...` — a bounded, deterministic sample for the human report."""
    if not violations:
        return "none"
    head = ", ".join(violations[:_SAMPLE])
    extra = len(violations) - _SAMPLE
    return f"{len(violations)}: {head}" + (f", +{extra} more" if extra > 0 else "")


def _check_type_on_concepts(vault: Path) -> tuple[CheckResult, int]:
    """Every concept declares a ``type`` matching its folder's OKF layer (SPEC §4/§5)."""
    violations: list[str] = []
    scanned = 0
    for folder, expected in LAYER_BY_FOLDER.items():
        for path in _concept_files(vault, folder):
            scanned += 1
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
            got = (fm or {}).get("type")
            if got is None:
                violations.append(f"{_rel(vault, path)} (missing type, want {expected})")
            elif got != expected:
                violations.append(f"{_rel(vault, path)} (type={got!r}, want {expected!r})")
    passed = not violations
    detail = (
        f"all {scanned} concepts carry a folder-correct type"
        if passed
        else f"{len(violations)}/{scanned} concepts miss or mismatch type -> {_sampled(violations)}"
    )
    return CheckResult(
        "type", "type on every concept (SPEC 4/5)", passed, detail, violations
    ), scanned


def _check_reserved_present(
    vault: Path, filename: str, dirs: tuple[str, ...], spec: str
) -> CheckResult:
    """A reserved OKF file exists in every directory that must carry it."""
    missing = [
        (f"{d}/{filename}" if d != "." else filename)
        for d in dirs
        if not (vault / (filename if d == "." else f"{d}/{filename}")).is_file()
    ]
    passed = not missing
    where = ", ".join(dirs)
    detail = (
        f"reserved {filename} present in all {len(dirs)} location(s) ({where})"
        if passed
        else f"missing {filename} in: {', '.join(missing)}"
    )
    return CheckResult(
        f"reserved-{Path(filename).stem}", f"reserved {filename} ({spec})", passed, detail, missing
    )


def _check_index_hygiene(vault: Path) -> CheckResult:
    """Reserved ``index.md`` files carry NO frontmatter (SPEC §6 — a listing, not a concept)."""
    violations: list[str] = []
    for path in vault.rglob(RESERVED_INDEX):
        if not path.is_file():
            continue
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        if fm is not None:
            violations.append(_rel(vault, path))
    passed = not violations
    detail = (
        "every index.md is a plain listing (no frontmatter)"
        if passed
        else f"index.md with illegal frontmatter -> {_sampled(violations)}"
    )
    return CheckResult(
        "index-hygiene", "index.md carries no frontmatter (SPEC 6)", passed, detail, violations
    )


def evaluate(vault: Path = DEFAULT_VAULT) -> Report:
    """Run every OKF-conformance check over the bundle and assemble the verdict."""
    report = Report(vault=_rel(vault, vault) or str(vault))
    type_result, scanned = _check_type_on_concepts(vault)
    report.concepts_scanned = scanned
    report.results.append(type_result)
    report.results.append(_check_reserved_present(vault, RESERVED_INDEX, INDEX_DIRS, "SPEC 6"))
    report.results.append(_check_reserved_present(vault, RESERVED_LOG, LOG_DIRS, "SPEC 7"))
    report.results.append(_check_index_hygiene(vault))
    return report


def render(report: Report) -> str:
    lines = ["", "azimuth OKF-conformance (SPEC-minimal profile)", "=" * 62]
    lines.append(f"  bundle: {report.vault}   concepts scanned: {report.concepts_scanned}")
    lines.append("-" * 62)
    for r in report.results:
        lines.append(f"  [{'PASS' if r.passed else 'FAIL'}] {r.check_id:<16} {r.name}")
        lines.append(f"          {r.detail}")
    lines.append("=" * 62)
    if report.conformant:
        lines.append("RESULT: CONFORMANT -- the bundle meets the OKF v0.1 SPEC-minimal bar.")
    else:
        failed = ", ".join(r.check_id for r in report.results if not r.passed)
        lines.append(f"RESULT: NON-CONFORMANT -- fix: {failed}")
    lines.append("")
    return "\n".join(lines)


def _to_dict(report: Report) -> dict[str, object]:
    return {
        "conformant": report.conformant,
        "vault": report.vault,
        "concepts_scanned": report.concepts_scanned,
        "checks": [
            {
                "id": r.check_id,
                "name": r.name,
                "passed": r.passed,
                "detail": r.detail,
                "violation_count": len(r.violations),
                "violations": r.violations[:_SAMPLE],
            }
            for r in report.results
        ],
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="azimuth OKF v0.1 conformance gate.")
    ap.add_argument(
        "--vault", type=Path, default=DEFAULT_VAULT, help="bundle root (default: ./vault)"
    )
    ap.add_argument("--json", action="store_true", help="emit the verdict as JSON")
    ns = ap.parse_args(argv)

    if not ns.vault.is_dir():
        print(f"error: bundle root not found: {ns.vault}", file=sys.stderr)
        return 2

    report = evaluate(ns.vault)
    print(json.dumps(_to_dict(report), indent=2) if ns.json else render(report))
    return 0 if report.conformant else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
