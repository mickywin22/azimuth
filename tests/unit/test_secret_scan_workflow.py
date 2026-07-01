"""Guards the split-scope design of the C1b privacy gate in the Secret Scan workflow.

The privacy-scan CI job hard-fails on owner-private context in the WORKING TREE
(the surface a push can newly introduce) but only REPORTS owner-private context in
git HISTORY (the documented C1c accept-vs-scrub call, a Michael go-gate at the flip,
never an autonomous history rewrite). Hard-failing every push on the pre-existing
history blobs made the gate red-by-design and killed its signal.

These tests pin that design so a future well-meaning "just scan everything" edit
can't silently re-redden main. Pure stdlib (text assertions over the workflow file)
to match the repo's no-new-dependency scanners -- no PyYAML.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "secret-scan.yml"


def _privacy_run_lines() -> list[str]:
    """Return the `run:` command lines under the privacy-scan job."""
    text = _WORKFLOW.read_text(encoding="utf-8")
    assert "privacy-scan:" in text, "privacy-scan job missing from workflow"
    # Slice from the privacy-scan job to the end of the file (it is the last job).
    body = text.split("privacy-scan:", 1)[1]
    return [
        line.split("run:", 1)[1].strip()
        for line in body.splitlines()
        if line.strip().startswith("- name:") is False and "run:" in line
    ]


def test_privacy_job_scans_worktree_and_not_a_bare_full_scan() -> None:
    """The HARD gate must scope to --worktree, never a bare full scan.

    A bare ``scan_private_leakage.py --report`` (no scope) re-scans history and
    re-fails on the pre-existing C1c blobs -- the exact red-by-design regression
    this guards against.
    """
    runs = _privacy_run_lines()
    assert runs, "no run: steps found under privacy-scan"
    privacy = [r for r in runs if "scan_private_leakage.py" in r]
    assert privacy, "privacy-scan runs no scan_private_leakage.py step"

    worktree_steps = [r for r in privacy if "--worktree" in r]
    assert worktree_steps, (
        f"privacy-scan must have a --worktree-scoped blocking step; got: {privacy!r}"
    )
    # No bare full-history-inclusive scan (scope flag absent) that would re-fail
    # the whole gate on the C1c history blobs.
    bare = [r for r in privacy if "--worktree" not in r and "--history" not in r]
    assert not bare, f"privacy-scan has an unscoped scan that will red-fail on history: {bare!r}"


def test_history_privacy_step_is_non_blocking() -> None:
    """History findings (the C1c decision surface) are surfaced but never block."""
    text = _WORKFLOW.read_text(encoding="utf-8")
    body = text.split("privacy-scan:", 1)[1]
    assert "--history" in body, "no history privacy-report step found"
    # The history step must carry continue-on-error so it is non-blocking.
    assert "continue-on-error: true" in body, (
        "the history privacy step must be continue-on-error (non-blocking) so the "
        "pre-existing C1c blobs don't red-fail every push"
    )


def test_all_three_scan_jobs_present() -> None:
    text = _WORKFLOW.read_text(encoding="utf-8")
    for job in ("gitleaks:", "stdlib-scan:", "privacy-scan:"):
        assert job in text, f"missing scan job: {job}"
