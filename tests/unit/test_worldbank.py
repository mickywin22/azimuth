"""Unit tests for the direct World Bank Open Data source.

Covers the pure core (``ingest.worldbank``: endpoint parse, URL build, BOM-tolerant envelope
parse, latest-per-country flatten, full transform) and the network-edge routing
(``ingest.http.CompositeFetcher`` / ``WorldBankFetcher``) with injected fakes — no network.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from ingest import worldbank as wb
from ingest.http import CompositeFetcher, FetchError, HttpFetcher, WorldBankFetcher

FIXED = datetime(2026, 8, 14, 3, 0, 0, tzinfo=UTC)


# --- a realistic World Bank envelope: [meta, rows] with nested indicator/country ----------
def _wb_envelope() -> list[object]:
    def row(iso3: str, country: str, date: str, value: object) -> dict[str, object]:
        return {
            "indicator": {"id": "NY.GDP.MKTP.CD", "value": "GDP (current US$)"},
            "country": {"id": iso3[:2], "value": country},
            "countryiso3code": iso3,
            "date": date,
            "value": value,
            "unit": "",
            "obs_status": "",
            "decimal": 0,
        }

    return [
        {"page": 1, "pages": 1, "per_page": 400, "total": 5, "lastupdated": "2026-07-13"},
        [
            row("USA", "United States", "2025", 30769700000000),
            row("USA", "United States", "2024", 29184890000000),  # older, must lose
            row("DEU", "Germany", "2025", 5050922925047.05),
            row("CHN", "China", "2025", 19498039388042.6),
            row("JPN", "Japan", "2024", None),  # null latest -> falls back to 2023
            row("JPN", "Japan", "2023", 4212945000000),
        ],
    ]


# --- indicator_code -----------------------------------------------------------------------
def test_indicator_code_extracts() -> None:
    assert wb.indicator_code("worldbank:NY.GDP.MKTP.CD") == "NY.GDP.MKTP.CD"


def test_indicator_code_rejects_non_worldbank() -> None:
    with pytest.raises(ValueError, match="not a world-bank endpoint"):
        wb.indicator_code("/api/economic/v1/list-world-bank-indicators")


def test_indicator_code_rejects_empty() -> None:
    with pytest.raises(ValueError, match="missing an indicator code"):
        wb.indicator_code("worldbank:")


# --- build_url ----------------------------------------------------------------------------
def test_build_url_shape_and_rolling_window() -> None:
    url = wb.build_url("worldbank:FP.CPI.TOTL.ZG", now=FIXED)
    assert url.startswith("https://api.worldbank.org/v2/country/")
    assert "/indicator/FP.CPI.TOTL.ZG?" in url
    assert "format=json" in url and f"per_page={wb.PER_PAGE}" in url
    # rolling [year - LOOKBACK_YEARS : year] window derived from the injected clock
    assert f"date={FIXED.year - wb.LOOKBACK_YEARS}:{FIXED.year}" in url
    # the shared key-economy set is joined with ';'
    assert ";".join(wb.COUNTRIES) in url


def test_build_url_custom_countries() -> None:
    url = wb.build_url("worldbank:NY.GDP.MKTP.CD", now=FIXED, countries=("US", "DE"))
    assert "/country/US;DE/indicator/NY.GDP.MKTP.CD?" in url


# --- parse_payload (BOM-tolerant, degrade-not-crash) --------------------------------------
def test_parse_payload_strips_bom_bytes() -> None:
    raw = ("﻿" + json.dumps(_wb_envelope())).encode("utf-8")
    rows = wb.parse_payload(raw)
    assert len(rows) == 6 and all(isinstance(r, dict) for r in rows)


def test_parse_payload_strips_bom_str() -> None:
    rows = wb.parse_payload("﻿" + json.dumps(_wb_envelope()))
    assert len(rows) == 6


@pytest.mark.parametrize(
    "payload",
    [
        [{"page": 1}, None],  # WB returns [meta, null] when a query matches no data
        [{"message": [{"id": "120", "value": "Invalid format"}]}],  # error payload, length 1
        {"data": []},  # not a list at all
        [],  # empty list
        [{"page": 1}, {"not": "a list"}],  # rows slot is not a list
    ],
)
def test_parse_payload_degrades_to_empty(payload: object) -> None:
    assert wb.parse_payload(json.dumps(payload)) == []


# --- latest_per_country -------------------------------------------------------------------
def test_latest_per_country_flattens_and_dedupes() -> None:
    flat = wb.latest_per_country(wb.parse_payload(json.dumps(_wb_envelope())))
    # one row per country (USA deduped to 2025; Japan falls back past the null 2024 to 2023)
    by_iso = {r["iso3"]: r for r in flat}
    assert set(by_iso) == {"USA", "DEU", "CHN", "JPN"}
    assert by_iso["USA"]["date"] == "2025" and by_iso["USA"]["value"] == 30769700000000
    assert by_iso["JPN"]["date"] == "2023" and by_iso["JPN"]["value"] == 4212945000000
    # flat shape: exactly ROW_KEYS, no nested objects (so the generic renderer tables it)
    for r in flat:
        assert tuple(r.keys()) == wb.ROW_KEYS
        assert not any(isinstance(v, (dict, list)) for v in r.values())
    # nested indicator/country were extracted to scalars
    assert by_iso["DEU"]["country"] == "Germany"
    assert by_iso["DEU"]["indicator"] == "GDP (current US$)"
    assert by_iso["DEU"]["indicator_code"] == "NY.GDP.MKTP.CD"


def test_latest_per_country_sorted_by_country() -> None:
    flat = wb.latest_per_country(wb.parse_payload(json.dumps(_wb_envelope())))
    names = [r["country"] for r in flat]
    assert names == sorted(names)


def test_latest_per_country_skips_rows_without_iso3() -> None:
    rows: list[dict[str, object]] = [
        {"countryiso3code": "", "date": "2025", "value": 1, "country": {}, "indicator": {}},
        {"countryiso3code": None, "date": "2025", "value": 2, "country": {}, "indicator": {}},
    ]
    assert wb.latest_per_country(rows) == []


def test_latest_per_country_handles_non_dict_nested() -> None:
    # a malformed row where country/indicator are not dicts must not crash -> "" scalars
    rows: list[dict[str, object]] = [
        {"countryiso3code": "USA", "date": "2025", "value": 1, "country": "x", "indicator": None}
    ]
    out = wb.latest_per_country(rows)
    assert out[0]["country"] == "" and out[0]["indicator"] == "" and out[0]["iso3"] == "USA"


# --- transform (end-to-end pure pipeline) -------------------------------------------------
def test_transform_end_to_end() -> None:
    flat = wb.transform(json.dumps(_wb_envelope()).encode("utf-8"))
    assert [r["iso3"] for r in flat] == ["CHN", "DEU", "JPN", "USA"]  # sorted by country name


def test_transform_empty_on_error_payload() -> None:
    assert wb.transform(json.dumps([{"message": [{"id": "120"}]}])) == []


# --- CompositeFetcher routing (offline, injected fakes) -----------------------------------
class _RecordingFetcher:
    def __init__(self, tag: str) -> None:
        self.tag = tag
        self.calls: list[str] = []

    def fetch(self, endpoint: str) -> object:
        self.calls.append(endpoint)
        return self.tag


def test_composite_routes_worldbank_to_direct() -> None:
    wm = _RecordingFetcher("wm")
    bank = _RecordingFetcher("wb")
    composite = CompositeFetcher(wm, bank)  # type: ignore[arg-type]
    assert composite.fetch("worldbank:NY.GDP.MKTP.CD") == "wb"
    assert bank.calls == ["worldbank:NY.GDP.MKTP.CD"] and wm.calls == []


def test_composite_routes_worldmonitor_to_session() -> None:
    wm = _RecordingFetcher("wm")
    bank = _RecordingFetcher("wb")
    composite = CompositeFetcher(wm, bank)  # type: ignore[arg-type]
    assert composite.fetch("/api/economic/v1/get-crude-inventories") == "wm"
    assert wm.calls == ["/api/economic/v1/get-crude-inventories"] and bank.calls == []


def test_composite_is_a_fetcher_over_real_edges() -> None:
    # smoke: construct with the real edge classes (no network touched, no fetch called)
    composite = CompositeFetcher(HttpFetcher(), WorldBankFetcher())
    assert hasattr(composite, "fetch")


# --- WorldBankFetcher edge (network _request stubbed) -------------------------------------
def test_worldbank_fetcher_wires_build_and_transform(monkeypatch: pytest.MonkeyPatch) -> None:
    fetcher = WorldBankFetcher(now=FIXED)
    captured: dict[str, str] = {}

    def fake_request(url: str) -> bytes:
        captured["url"] = url
        return ("﻿" + json.dumps(_wb_envelope())).encode("utf-8")

    monkeypatch.setattr(fetcher, "_request", fake_request)
    rows = fetcher.fetch("worldbank:NY.GDP.MKTP.CD")
    assert isinstance(rows, list) and len(rows) == 4  # 4 distinct countries, flattened
    assert "/indicator/NY.GDP.MKTP.CD?" in captured["url"]


def test_worldbank_fetcher_rejects_bad_endpoint() -> None:
    with pytest.raises(FetchError, match="bad world-bank endpoint"):
        WorldBankFetcher().fetch("worldbank:")
