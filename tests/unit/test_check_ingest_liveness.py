"""Tests for the ingest liveness heartbeat (scripts/check_ingest_liveness.py).

The load-bearing guarantee: a daily L1 ingest that silently stops must become *visible*.
The check finds the newest committed L1 day and fails when it is older than tolerance, so a
dead cron turns into a non-zero exit (which the workflow turns into an alarm) instead of an
invisible gap. Date handling is pinned via ``today`` so the verdict is deterministic.
"""

from __future__ import annotations

import importlib.util
from datetime import date
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_ingest_liveness", _REPO_ROOT / "scripts" / "check_ingest_liveness.py"
)
assert _spec and _spec.loader
cil = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cil)


def _sources(tmp_path: Path, days: list[str]) -> Path:
    root = tmp_path / "01 Sources"
    root.mkdir()
    for d in days:
        (root / d).mkdir()
    (root / "README.md").write_text("index", encoding="utf-8")  # must be ignored
    return root


def test_latest_l1_day_picks_newest_and_ignores_non_dates(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-23", "2026-06-25", "2026-06-18"])
    assert cil.latest_l1_day(src) == date(2026, 6, 25)


def test_l1_days_returns_only_valid_dates_sorted(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-25", "2026-06-20"])
    (src / "not-a-day").mkdir()
    assert cil.l1_days(src) == [date(2026, 6, 20), date(2026, 6, 25)]


def test_liveness_healthy_within_tolerance(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-25"])
    r = cil.liveness(src, today=date(2026, 6, 26), max_age_days=2)
    assert r["healthy"] is True
    assert r["age_days"] == 1
    assert r["latest_l1_day"] == "2026-06-25"


def test_liveness_stale_beyond_tolerance(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-20"])
    r = cil.liveness(src, today=date(2026, 6, 26), max_age_days=2)
    assert r["healthy"] is False
    assert r["age_days"] == 6


def test_liveness_no_days_is_unhealthy(tmp_path: Path) -> None:
    empty = tmp_path / "01 Sources"
    empty.mkdir()
    r = cil.liveness(empty, today=date(2026, 6, 26))
    assert r["healthy"] is False
    assert r["latest_l1_day"] is None
    assert r["day_count"] == 0


def test_check_exit_code_healthy(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-26"])
    assert cil.main(["--check", "--sources", str(src), "--today", "2026-06-26"]) == 0


def test_check_exit_code_stale(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-10"])
    assert cil.main(["--check", "--sources", str(src), "--today", "2026-06-26"]) == 1


def test_invalid_today_returns_2(tmp_path: Path) -> None:
    src = _sources(tmp_path, ["2026-06-26"])
    assert cil.main(["--check", "--sources", str(src), "--today", "not-a-date"]) == 2
