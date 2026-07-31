"""Tests for the Outlook Tier-A series extractor (outlook/series.py) — design doc §6 P1.

The extractor is the data foundation of the whole prediction layer: it must turn the four
Tier-A L1 notes into clean, chronological, deterministic ``(period, value)`` series, and it
must fail SOFT (a broken feed yields None, never a crash) and honor the Tier-A allow-list
that doubles as the forecaster's hazard interlock.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from outlook.series import (
    FORECASTABLE_KEYS,
    SPEC_BY_KEY,
    TIER_A,
    extract_all,
    extract_latest,
    extract_series,
    is_forecastable,
    latest_day,
)

if TYPE_CHECKING:
    from pathlib import Path

# Repo-relative committed L1 tree, for the real-data smoke test at the bottom.
from pathlib import Path as _Path

_REPO = _Path(__file__).resolve().parents[2]
_SOURCES = _REPO / "vault" / "01 Sources"


def _note(field: str, value: object) -> str:
    """Render one L1 note body the way ingest writes it: a single | field | value | row."""
    blob = json.dumps(value) if not isinstance(value, str) else value
    return (
        "---\nsource: X\nsource_key: k\n---\n# X\n\n"
        "| field | value |\n| --- | --- |\n"
        f"| {field} | {blob} |\n"
    )


def _make_day(tmp_path: Path) -> Path:
    """A synthetic L1 day carrying all four Tier-A series in their real note shapes."""
    d = tmp_path / "vault" / "01 Sources" / "2026-07-30"
    d.mkdir(parents=True)
    # CO2: object -> trend12m[], oldest->newest, key ppm.
    (d / "co2-monitoring.md").write_text(
        _note(
            "monitoring",
            {
                "currentPpm": 429.0,
                "trend12m": [
                    {"month": "2026-05", "ppm": 432.34},
                    {"month": "2026-06", "ppm": 431.44},
                    {"month": "2026-04", "ppm": 431.12},  # deliberately out of order
                ],
            },
        ),
        encoding="utf-8",
    )
    # Sea-ice: object -> iceTrend12m[], key extentMkm2.
    (d / "sea-ice-extent.md").write_text(
        _note(
            "data",
            {
                "iceTrend12m": [
                    {"month": "2026-06", "extentMkm2": 9.1},
                    {"month": "2026-07", "extentMkm2": 6.57},
                ]
            },
        ),
        encoding="utf-8",
    )
    # EU gas: the field IS the list, newest-first, key storBcf.
    (d / "natural-gas-storage-eu.md").write_text(
        _note(
            "weeks",
            [
                {"period": "2026-07-17", "storBcf": 3056},
                {"period": "2026-07-10", "storBcf": 3024},
                {"period": "2026-07-03", "storBcf": 2983},
            ],
        ),
        encoding="utf-8",
    )
    # US crude: field is the list, key stocksMb (thousand-barrels -> scaled to Mb, /1000).
    (d / "crude-oil-inventories.md").write_text(
        _note(
            "weeks",
            [
                {"period": "2026-07-24", "stocksMb": 712158},
                {"period": "2026-07-17", "stocksMb": 723122},
            ],
        ),
        encoding="utf-8",
    )
    return d


# ── happy path ────────────────────────────────────────────────────────────────────────────
def test_extract_all_four_series(tmp_path: Path) -> None:
    day = _make_day(tmp_path)
    series = extract_all(day)
    assert set(series) == {"co2-ppm", "arctic-sea-ice", "eu-gas-storage", "us-crude-stocks"}


def test_periods_are_sorted_chronologically(tmp_path: Path) -> None:
    day = _make_day(tmp_path)
    co2 = extract_all(day)["co2-ppm"]
    # The fixture fed 2026-05, 2026-06, 2026-04 out of order -> must come back sorted.
    assert co2.periods == ["2026-04", "2026-05", "2026-06"]
    assert co2.values == [431.12, 432.34, 431.44]
    assert co2.latest == ("2026-06", 431.44)


def test_crude_is_scaled_to_million_barrels(tmp_path: Path) -> None:
    day = _make_day(tmp_path)
    crude = extract_all(day)["us-crude-stocks"]
    assert crude.unit == "Mb"
    # 712158 thousand-barrels -> 712.158 Mb, and sorted oldest->newest.
    assert crude.periods == ["2026-07-17", "2026-07-24"]
    assert crude.values == [723.122, 712.158]


def test_weekly_series_have_expected_metadata(tmp_path: Path) -> None:
    day = _make_day(tmp_path)
    gas = extract_all(day)["eu-gas-storage"]
    assert gas.cadence == "weekly"
    assert gas.season == 52
    assert gas.values == [2983.0, 3024.0, 3056.0]


def test_extraction_is_deterministic(tmp_path: Path) -> None:
    day = _make_day(tmp_path)
    assert extract_all(day) == extract_all(day)


# ── upsert-by-period (a revised week overrides the earlier value) ───────────────────────────
def test_upsert_latest_value_wins_for_a_period(tmp_path: Path) -> None:
    d = tmp_path / "vault" / "01 Sources" / "2026-07-30"
    d.mkdir(parents=True)
    (d / "natural-gas-storage-eu.md").write_text(
        _note(
            "weeks",
            [
                {"period": "2026-07-17", "storBcf": 3056},
                {
                    "period": "2026-07-17",
                    "storBcf": 3099,
                },  # a later, revised row for the SAME week
                {"period": "2026-07-10", "storBcf": 3024},
            ],
        ),
        encoding="utf-8",
    )
    gas = extract_series(d, SPEC_BY_KEY["eu-gas-storage"])
    assert gas is not None
    assert dict(gas.points)["2026-07-17"] == 3099.0  # the revised value, not 3056


# ── fail-soft ───────────────────────────────────────────────────────────────────────────────
def test_missing_day_yields_empty(tmp_path: Path) -> None:
    assert extract_all(tmp_path / "does" / "not" / "exist") == {}


def test_missing_field_yields_none(tmp_path: Path) -> None:
    d = tmp_path / "vault" / "01 Sources" / "2026-07-30"
    d.mkdir(parents=True)
    (d / "co2-monitoring.md").write_text(_note("wrongfield", {"x": 1}), encoding="utf-8")
    assert extract_series(d, SPEC_BY_KEY["co2-ppm"]) is None


def test_malformed_json_yields_none(tmp_path: Path) -> None:
    d = tmp_path / "vault" / "01 Sources" / "2026-07-30"
    d.mkdir(parents=True)
    (d / "co2-monitoring.md").write_text(
        "| field | value |\n| --- | --- |\n| monitoring | {not json} |\n", encoding="utf-8"
    )
    assert extract_series(d, SPEC_BY_KEY["co2-ppm"]) is None


def test_rows_with_bad_values_are_skipped_individually(tmp_path: Path) -> None:
    d = tmp_path / "vault" / "01 Sources" / "2026-07-30"
    d.mkdir(parents=True)
    (d / "co2-monitoring.md").write_text(
        _note(
            "monitoring",
            {
                "trend12m": [
                    {"month": "2026-05", "ppm": 432.34},
                    {"month": "2026-06", "ppm": "n/a"},  # non-numeric -> skipped
                    {"month": "bad-period", "ppm": 430.0},  # non-ISO period -> skipped
                    {"ppm": 429.0},  # missing period -> skipped
                ]
            },
        ),
        encoding="utf-8",
    )
    co2 = extract_series(d, SPEC_BY_KEY["co2-ppm"])
    assert co2 is not None
    assert co2.periods == ["2026-05"]


# ── the allow-list / hazard interlock contract ─────────────────────────────────────────────
def test_allow_list_is_exactly_the_four_tier_a_keys() -> None:
    assert {"co2-ppm", "arctic-sea-ice", "eu-gas-storage", "us-crude-stocks"} == FORECASTABLE_KEYS
    assert len(TIER_A) == 4


def test_hazards_are_not_forecastable() -> None:
    for key in ("earthquakes", "wildfire-detections", "prediction-markets", "conflict-events"):
        assert not is_forecastable(key)


# ── real committed L1 data (production shape smoke) ─────────────────────────────────────────
def test_extract_latest_from_committed_l1() -> None:
    """The four series must parse out of the newest committed L1 day with sane shapes."""
    day = latest_day(_SOURCES)
    assert day is not None, "no committed L1 day found"
    series = extract_latest(_SOURCES)
    # All four Tier-A feeds are in the daily bundle, so all four must extract.
    assert set(series) == FORECASTABLE_KEYS
    assert len(series["co2-ppm"]) >= 6  # ~12 monthly points
    assert len(series["eu-gas-storage"]) >= 4  # ~8 weekly points
    for s in series.values():
        assert s.periods == sorted(s.periods)  # chronological
        assert all(v == v for v in s.values)  # no NaN
