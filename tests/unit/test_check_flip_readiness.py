"""Tests for the public-flip go/no-go aggregator (scripts/check_flip_readiness.py).

The load-bearing guarantee: the aggregate exit code is GREEN iff **every blocking fleet
gate** passes, and the Michael-gated decisions (C1c / C5 / C6 / C7 / FLIP) are listed for
context but NEVER run and NEVER move the exit code. We test the aggregation logic directly
(stubbing the per-gate runner) so the test does not depend on the live repo state.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_flip_readiness", _REPO_ROOT / "scripts" / "check_flip_readiness.py"
)
assert _spec and _spec.loader
cfr = importlib.util.module_from_spec(_spec)
# Register before exec so @dataclass can resolve the module via sys.modules (3.12+ frozen=True).
sys.modules[_spec.name] = cfr
_spec.loader.exec_module(cfr)


def test_all_fleet_gates_green_exits_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfr, "_run_script", lambda script, args: (True, f"{script} ok"))
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (True, "licenses present"))
    assert cfr.main([]) == 0


def test_any_red_fleet_gate_exits_one(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(script: str, args: list[str]) -> tuple[bool, str]:
        # The secret scan is the one that fails — must turn the whole verdict RED.
        if script == "scan_secrets.py":
            return False, "LEAK FOUND -- public flip BLOCKED."
        return True, f"{script} ok"

    monkeypatch.setattr(cfr, "_run_script", fake_run)
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (True, "licenses present"))
    readiness = cfr.evaluate()
    assert not readiness.all_fleet_green
    assert cfr.main([]) == 1


def test_missing_license_blocks_the_flip(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfr, "_run_script", lambda script, args: (True, "ok"))
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (False, "missing: LICENSE"))
    assert cfr.main([]) == 1


def test_michael_gates_are_advisory_and_never_block(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfr, "_run_script", lambda script, args: (True, "ok"))
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (True, "ok"))
    readiness = cfr.evaluate()
    michael = [r for r in readiness.results if r.owner == "Michael"]
    # The flip + spot-reviews are present but none of them are blocking or "ran".
    assert {"C1c", "C5", "C6", "C7", "FLIP"} <= {r.gate_id for r in michael}
    assert all(not r.blocking and not r.ran for r in michael)
    # Even though every Michael gate is "not passed", the fleet verdict is still GREEN.
    assert readiness.all_fleet_green


def test_fleet_gates_are_exactly_the_blocking_five(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cfr, "_run_script", lambda script, args: (True, "ok"))
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (True, "ok"))
    readiness = cfr.evaluate()
    assert {r.gate_id for r in readiness.fleet_gates} == {"C1", "C1b", "C2", "C3", "C4"}


def test_history_flag_adds_c1c_as_nonblocking(monkeypatch: pytest.MonkeyPatch) -> None:
    # C1c history scan reports HARD findings (exit non-zero) — must NOT flip the verdict RED.
    def fake_run(script: str, args: list[str]) -> tuple[bool, str]:
        if script == "scan_private_leakage.py" and "--history" in args:
            return False, "6 HARD findings in history"
        return True, "ok"

    monkeypatch.setattr(cfr, "_run_script", fake_run)
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (True, "ok"))
    readiness = cfr.evaluate(include_history=True)
    c1c = next(r for r in readiness.results if r.gate_id == "C1c")
    assert c1c.ran and not c1c.passed and not c1c.blocking
    assert readiness.all_fleet_green  # C1c being red does not block
    assert cfr.main(["--history"]) == 0


def test_json_output_is_wellformed(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import json

    monkeypatch.setattr(cfr, "_run_script", lambda script, args: (True, "ok"))
    monkeypatch.setattr(cfr, "_check_licenses", lambda: (True, "ok"))
    cfr.main(["--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["all_fleet_green"] is True
    assert {g["id"] for g in payload["gates"]} >= {"C1", "C1b", "C2", "C3", "C4", "FLIP"}
