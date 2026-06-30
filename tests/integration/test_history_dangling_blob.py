"""Integration regression: the privacy gate must reach UNREACHABLE history blobs.

The C1c private-leakage history scan and the C1 secret history scan exist for one
reason — nothing owner-private (paths, hooks, keys) may survive in the git object
database when ``mickywin22/azimuth`` flips public. A blob that was written into the
object store but is no longer reachable from any ref (a "dangling" blob — left by an
amended commit, a deleted branch, an aborted rebase, or ``git hash-object -w``) is the
sneakiest place a leak hides: a plain ``git log`` / ``rev-list`` walk never shows it,
yet ``git fsck`` and a clone's repack can still surface it.

The old ``scan_history`` walked ``rev-list --all --objects`` (reachable only), so a
private path in a dangling blob would pass the privacy gate while the secret gate —
which already uses ``cat-file --batch-all-objects`` — caught it. This test pins the
fixed behavior: a dangling blob carrying an owner-private path IS scanned and IS
flagged HARD. It would FAIL against the reachable-only implementation.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "scan_private_leakage", _REPO_ROOT / "scripts" / "scan_private_leakage.py"
)
assert _spec and _spec.loader
scan = importlib.util.module_from_spec(_spec)
sys.modules["scan_private_leakage"] = scan
_spec.loader.exec_module(scan)


def _git(cwd: Path, *args: str) -> str:
    res = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    assert res.returncode == 0, f"git {' '.join(args)} failed: {res.stderr}"
    return res.stdout


def test_dangling_blob_is_scanned(tmp_path: Path) -> None:
    """A private path in an unreachable blob must be caught (HARD), not missed."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "ci@example.com")
    _git(repo, "config", "user.name", "ci")
    # A clean reachable commit so the repo has at least one ref + a normal blob.
    (repo / "README.md").write_text("public demonstrator\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-qm", "init")

    # Write a DANGLING blob: it lands in the object DB but is referenced by nothing.
    res = subprocess.run(
        ["git", "hash-object", "-w", "--stdin"],
        cwd=repo,
        input="hook: C:\\Users\\Michael\\HemySphere\\scripts\\hooks\\package-cooldown.ps1\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert res.returncode == 0, res.stderr
    dangling_oid = res.stdout.strip()
    # Prove it is genuinely unreachable: rev-list (what the OLD scanner used) must not list it.
    reachable = _git(repo, "rev-list", "--all", "--objects")
    assert dangling_oid not in reachable, "test setup: blob should be dangling/unreachable"

    cwd0 = Path.cwd()
    try:
        os.chdir(repo)
        findings, scanned = scan.scan_history()
    finally:
        os.chdir(cwd0)

    assert scanned >= 2, "should scan the reachable README blob + the dangling blob"
    hard = [f for f in findings if f.severity == "hard"]
    assert any(
        f.rule in {"hemysphere-local-path", "personal-abs-path-windows", "local-machine-hook"}
        for f in hard
    ), f"dangling owner-private blob was not flagged HARD; findings={[f.rule for f in findings]}"
