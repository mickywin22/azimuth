"""Integration guard for the public CLI surface (docs/cli.md).

azimuth has no web-server runtime — the whole engine is a set of stdlib Python CLIs that
CI runs and that `docs/cli.md` tells the public how to use. A public-grade repo must never
ship a CLI whose parser is broken: an import error, a syntax slip, or an argparse
misconfiguration turns every documented invocation of that script into a copy-paste failure.

This test proves, for every argparse-driven script under `scripts/`, that the parser builds
and `--help` succeeds. It is the standing regression guard behind the KR-C rule that the
repo's *documented* commands actually work — the class of defect that hit
`query_graph.py <cmd> --json` and `scan_secrets.py --report OUT`.

Two scripts are intentionally out of scope: `smoke_whatif.py` (a Playwright smoke with no
argparse; needs browser deps) and `Build-Graphify-AST-Only.py` (an AST build helper, not a
documented CLI). Both are detected — not hard-coded — by the absence of `argparse`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS = _REPO_ROOT / "scripts"


def _argparse_clis() -> list[Path]:
    """Every script that drives itself with argparse — i.e. the real CLI surface."""
    out: list[Path] = []
    for path in sorted(_SCRIPTS.glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "argparse" in text:
            out.append(path)
    return out


_CLIS = _argparse_clis()


def test_cli_surface_is_non_empty() -> None:
    # Guard the guard: if discovery ever returns nothing (moved dir, glob typo), fail loud
    # rather than silently passing zero parametrized cases.
    assert len(_CLIS) >= 10, f"expected the scripts/ CLI surface, found {_CLIS!r}"


@pytest.mark.parametrize("script", _CLIS, ids=lambda p: p.name)
def test_cli_help_builds_and_exits_zero(script: Path) -> None:
    """`python scripts/<cli>.py --help` must build its parser and exit 0.

    Catches import errors, syntax breaks, and argparse misconfiguration across the whole
    documented CLI surface before any of it reaches a public reader.
    """
    proc = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        cwd=str(_REPO_ROOT),
    )
    assert proc.returncode == 0, (
        f"{script.name} --help exited {proc.returncode}\n"
        f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    )
    assert "usage:" in proc.stdout.lower(), (
        f"{script.name} --help produced no usage text:\n{proc.stdout}"
    )
