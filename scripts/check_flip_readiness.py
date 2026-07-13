#!/usr/bin/env python3
"""One-command public-flip go/no-go — run every fleet-owned readiness gate at once.

Taking ``mickywin22/azimuth`` from private -> public is a **Michael go-gate**: no
automation makes the repo public. But before he flips, every *fleet-owned* gate must be
GREEN, and until now re-confirming that meant running five separate commands by hand
(``scan_secrets.py``, ``scan_private_leakage.py --worktree``, a LICENSE file check,
``check_sources.py``, ``check_ingest_liveness.py --check``). The readiness doc promises the
flip is "a one-glance decision, not a re-investigation" — this script is that one glance.

It runs each fleet gate, prints a GREEN/RED go-table, and **exits 0 only if every blocking
fleet gate passes**, so it doubles as the re-verify step in the flip runbook (run it against
the exact commit being published) and as a CI job that keeps the bundle honest after the
flip. The **Michael-gated** conditions (C1c history accept-vs-scrub, C5/C6 spot-reviews, C7
editorial line, and THE FLIP itself) are listed for context but never run and never affect
this script's exit code — they are decisions, not checks.

Pure stdlib. Each gate is invoked as its own child process so one gate's import or crash
can't take down the runner.

Usage:
    python scripts/check_flip_readiness.py             # run all fleet gates, print the table
    python scripts/check_flip_readiness.py --json      # machine-readable verdict
    python scripts/check_flip_readiness.py --history    # also report C1c (history privacy) for info
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PY = sys.executable

# Full-history secret/privacy scans grow with the repo: 300s fit the 543-blob W27 surface but
# timed out on the 1382-blob 2026-07-13 surface (a false RED at flip time). 900s gives headroom.
_GATE_TIMEOUT_S = 900


@dataclass(frozen=True)
class GateResult:
    """Outcome of one readiness gate."""

    gate_id: str
    name: str
    owner: str
    passed: bool
    detail: str
    blocking: bool = True
    ran: bool = True


@dataclass
class FlipReadiness:
    """Aggregate verdict over all gates."""

    results: list[GateResult] = field(default_factory=list)

    @property
    def fleet_gates(self) -> list[GateResult]:
        return [r for r in self.results if r.blocking and r.ran]

    @property
    def all_fleet_green(self) -> bool:
        return all(r.passed for r in self.fleet_gates)


def _run_script(script: str, args: list[str]) -> tuple[bool, str]:
    """Run a repo script as a child process; return (exit-0?, first meaningful output line)."""
    path = _REPO_ROOT / "scripts" / script
    if not path.exists():
        return False, f"script not found: scripts/{script}"
    try:
        proc = subprocess.run(
            [_PY, str(path), *args],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=_GATE_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        return False, f"scripts/{script} timed out after {_GATE_TIMEOUT_S}s"
    out = (proc.stdout or "").strip().splitlines()
    err = (proc.stderr or "").strip().splitlines()
    # Prefer the verdict line: skip indented per-finding rows (e.g. "  [rule] ..."),
    # which a scanner prints AFTER its summary. The summary is the last non-finding line.
    verdict = [ln for ln in out if ln.strip() and not ln.startswith((" ", "\t"))]
    tail = verdict[-1] if verdict else (out[-1] if out else (err[-1] if err else ""))
    return proc.returncode == 0, tail


def _check_licenses() -> tuple[bool, str]:
    """C2 — both license files must be present on the publishable tree."""
    code = _REPO_ROOT / "LICENSE"
    content = _REPO_ROOT / "LICENSE-CONTENT.md"
    missing = [p.name for p in (code, content) if not p.exists()]
    if missing:
        return False, f"missing: {', '.join(missing)}"
    return True, "LICENSE (MIT) + LICENSE-CONTENT.md (CC-BY-4.0) present"


# Michael-gated conditions: shown for context, never run, never affect exit code.
_MICHAEL_GATES: list[GateResult] = [
    GateResult(
        "C1c",
        "Private-leakage scan (git history)",
        "Michael",
        passed=False,
        detail="accept-vs-scrub call on owner-private paths in history (run with --history to see)",
        blocking=False,
        ran=False,
    ),
    GateResult(
        "C5",
        "USP / positioning spot-review",
        "Michael",
        passed=False,
        detail="IQ #888 — ~15 min read of the USP & Strategy note",
        blocking=False,
        ran=False,
    ),
    GateResult(
        "C6",
        "First autonomous weekly-cycle spot-review",
        "Michael",
        passed=False,
        detail="IQ #937 — live briefs read neutral + correct",
        blocking=False,
        ran=False,
    ),
    GateResult(
        "C7",
        "prediction-markets editorial line",
        "Michael",
        passed=False,
        detail="IQ #915 — does not block flip (held source is surfaced:false for L2)",
        blocking=False,
        ran=False,
    ),
    GateResult(
        "FLIP",
        "Make the repo public",
        "Michael",
        passed=False,
        detail="IQ #898 — gh repo edit --visibility public (held until C5 + C6 green)",
        blocking=False,
        ran=False,
    ),
]


def evaluate(*, include_history: bool = False) -> FlipReadiness:
    """Run every fleet-owned gate and assemble the verdict."""
    readiness = FlipReadiness()

    c1_ok, c1_msg = _run_script("scan_secrets.py", [])
    readiness.results.append(
        GateResult("C1", "Secret scan (history + working tree)", "fleet", c1_ok, c1_msg)
    )

    c1b_ok, c1b_msg = _run_script("scan_private_leakage.py", ["--worktree"])
    readiness.results.append(
        GateResult("C1b", "Private-leakage scan (working tree)", "fleet", c1b_ok, c1b_msg)
    )

    c2_ok, c2_msg = _check_licenses()
    readiness.results.append(GateResult("C2", "License files present", "fleet", c2_ok, c2_msg))

    c3_ok, c3_msg = _run_script("check_sources.py", [])
    readiness.results.append(GateResult("C3", "Source guardrail", "fleet", c3_ok, c3_msg))

    c4_ok, c4_msg = _run_script("check_ingest_liveness.py", ["--check"])
    readiness.results.append(GateResult("C4", "Daily ingest healthy", "fleet", c4_ok, c4_msg))

    if include_history:
        # C1c is informational only — a non-zero exit here NEVER blocks the runner.
        hist_ok, hist_msg = _run_script("scan_private_leakage.py", ["--history"])
        readiness.results.append(
            GateResult(
                "C1c",
                "Private-leakage scan (git history)",
                "Michael",
                hist_ok,
                hist_msg,
                blocking=False,
            )
        )
    else:
        readiness.results.extend(r for r in _MICHAEL_GATES if r.gate_id == "C1c")

    readiness.results.extend(r for r in _MICHAEL_GATES if r.gate_id != "C1c")
    return readiness


def _icon(r: GateResult) -> str:
    if not r.ran:
        return "PENDING" if r.owner == "Michael" else "----"
    return "GREEN" if r.passed else "RED"


def render_table(readiness: FlipReadiness) -> str:
    """Human-readable go/no-go table."""
    lines = ["", "Azimuth public-flip readiness", "=" * 60]
    for r in readiness.results:
        lines.append(f"  [{_icon(r):>7}] {r.gate_id:<5} {r.owner:<7} {r.name}")
        lines.append(f"            {r.detail}")
    lines.append("=" * 60)
    if readiness.all_fleet_green:
        lines.append("FLEET GATES: all GREEN -- nothing fleet-actionable blocks the flip.")
        lines.append("Flip waits only on Michael (C5 #888, C6 #937, the C1c call, then THE FLIP).")
    else:
        red = [r.gate_id for r in readiness.fleet_gates if not r.passed]
        lines.append(f"FLEET GATES: RED -- {', '.join(red)} must be fixed before the flip.")
    lines.append("")
    return "\n".join(lines)


def _to_dict(readiness: FlipReadiness) -> dict[str, object]:
    return {
        "all_fleet_green": readiness.all_fleet_green,
        "gates": [
            {
                "id": r.gate_id,
                "name": r.name,
                "owner": r.owner,
                "status": _icon(r),
                "passed": r.passed if r.ran else None,
                "blocking": r.blocking,
                "ran": r.ran,
                "detail": r.detail,
            }
            for r in readiness.results
        ],
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit the verdict as JSON")
    ap.add_argument(
        "--history",
        action="store_true",
        help="also run the C1c git-history privacy scan (informational, never blocks)",
    )
    ns = ap.parse_args(argv)

    readiness = evaluate(include_history=ns.history)

    if ns.json:
        print(json.dumps(_to_dict(readiness), indent=2))
    else:
        print(render_table(readiness))

    return 0 if readiness.all_fleet_green else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
