"""Guards the Flip Readiness workflow: the public-flip go/no-go must stay a wired,
non-blocking CI surface.

`scripts/check_flip_readiness.py` aggregates every fleet-owned readiness gate into one
go/no-go verdict. Before this workflow it was a LOCAL-only script -- the S2 pre-flip clause
("the flip-readiness CI go/no-go job is present") was unmet, and a rotted gate would have been
invisible in CI. `flip-readiness.yml` wires it as a continuously-visible Actions check.

Two properties must never silently regress:

  1. the job actually runs the aggregator (not some stale copy), and
  2. it stays NON-BLOCKING -- a decision surface for Michael, not a merge gate. The aggregate
     is red-by-design during the whole pre-flip window (the FLIP gate is held), so hard-failing
     the build on it would re-create the exact anti-pattern secret-scan.yml's C1b split removed.
     The individual blocking gates (secret scan, guardrail, freshness) keep their own teeth.

Pure stdlib (text assertions over the workflow file) to match the repo's no-new-dependency
scanners -- no PyYAML, same discipline as test_secret_scan_workflow.py.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "flip-readiness.yml"


def _text() -> str:
    assert _WORKFLOW.exists(), "flip-readiness.yml is missing from .github/workflows/"
    return _WORKFLOW.read_text(encoding="utf-8")


def test_workflow_runs_the_readiness_aggregator() -> None:
    """The job must invoke scripts/check_flip_readiness.py -- the real go/no-go tool."""
    assert "scripts/check_flip_readiness.py" in _text(), (
        "flip-readiness.yml must run scripts/check_flip_readiness.py"
    )


def test_workflow_has_manual_dispatch() -> None:
    """`workflow_dispatch` is the deliberate pre-flip re-verify Michael/the fleet triggers."""
    assert "workflow_dispatch" in _text(), (
        "flip-readiness.yml must expose workflow_dispatch for the deliberate pre-flip check"
    )


def test_workflow_is_non_blocking() -> None:
    """The aggregator's exit code must not fail the build (decision surface, not a gate).

    The `|| true` guard pins the non-blocking contract, exactly as test_secret_scan_workflow.py
    pins `continue-on-error: true` on the C1b history step. Drop it and the roll-up goes
    red-by-design until the flip.
    """
    text = _text()
    assert "|| true" in text, (
        "the aggregator step must be non-blocking (`|| true`) so the held-FLIP verdict never "
        "reddens the build"
    )
    # Honesty must still be surfaced: a RED verdict raises a visible warning annotation.
    assert "::warning" in text, (
        "a RED fleet-gate verdict must surface a warning annotation, not fail silently"
    )


def test_workflow_scans_full_history() -> None:
    """`fetch-depth: 0` -- the C1 secret scan reads full history; a shallow clone false-GREENs."""
    assert "fetch-depth: 0" in _text(), (
        "flip-readiness.yml must checkout full history (fetch-depth: 0) so the C1 secret scan "
        "sees historical blobs instead of returning a shallow false GREEN"
    )
