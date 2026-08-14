"""Direct World Bank Open Data (``api.worldbank.org``) macro source — pure core.

Why a *direct* source (not a WorldMonitor channel)
--------------------------------------------------
WorldMonitor's ``world-bank-indicators`` channel is a dead free-tier stub: it returned an
empty ``{"data":[]}`` on every committed L1 day of its life and then began failing HTTP 400,
so it was de-surfaced (drop commit — see ``sources/registry.json`` ``surfaced_reason``). The
genuinely-free path for macro indicators is the **World Bank Open Data API directly**: no key,
no session, CC-BY-4.0. This module is that source's PURE core — URL build, envelope parse, and
the latest-per-country flatten — kept offline and unit-tested; the thin network edge lives in
``ingest.http.WorldBankFetcher`` (mirrors how ``HttpFetcher`` is the WorldMonitor edge).

Endpoint convention
-------------------
A macro source's registry ``endpoint`` is the sentinel ``worldbank:<INDICATOR_CODE>``
(e.g. ``worldbank:NY.GDP.MKTP.CD``). ``ingest.http.CompositeFetcher`` routes that prefix
here; every WorldMonitor source keeps its ``/api/...`` path and its session-minted fetcher.
Nothing else in the ingest core parses ``endpoint`` — it is display/registry metadata only.

Pure stdlib (json), fully typed for mypy --strict.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

# The WorldBank Indicators API v2. Multi-country + a date range is the free, keyless call
# (``mrnev=1`` is NOT compatible with a multi-country request — it 500s — so we pull a
# rolling window and keep the latest non-null observation per country in ``latest_per_country``).
WB_BASE = "https://api.worldbank.org/v2"
ENDPOINT_PREFIX = "worldbank:"

# A few key economies (ISO-2): the largest advanced + emerging economies, incl. Germany
# (Michael's economy). Extend this tuple to widen coverage — every source shares it.
COUNTRIES: tuple[str, ...] = ("US", "CN", "JP", "DE", "IN", "GB", "FR")

# The three headline macro indicators -> their World Bank series codes. Each maps to one
# registry source (world-bank-gdp / -cpi / -unemployment) via its ``worldbank:<CODE>`` endpoint.
INDICATORS: dict[str, str] = {
    "NY.GDP.MKTP.CD": "GDP (current US$)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force, modeled ILO)",
}

# Rolling look-back so every country resolves at least one recent non-null observation
# (some series lag a year for some countries); ``latest_per_country`` keeps only the newest.
LOOKBACK_YEARS = 8
# 7 countries x (LOOKBACK_YEARS + 1) years = a few dozen rows — one page, never paginate.
PER_PAGE = 400

# The flat L1 row shape this module emits (so the generic renderer tables it — no nested objects).
ROW_KEYS: tuple[str, ...] = ("country", "iso3", "indicator", "indicator_code", "date", "value")


def indicator_code(endpoint: str) -> str:
    """Extract the WB series code from a ``worldbank:<CODE>`` sentinel endpoint."""
    if not endpoint.startswith(ENDPOINT_PREFIX):
        raise ValueError(f"not a world-bank endpoint: {endpoint!r}")
    code = endpoint[len(ENDPOINT_PREFIX) :].strip()
    if not code:
        raise ValueError(f"world-bank endpoint missing an indicator code: {endpoint!r}")
    return code


def build_url(
    endpoint: str,
    *,
    now: datetime | None = None,
    countries: tuple[str, ...] = COUNTRIES,
) -> str:
    """Build the live WB API URL for a ``worldbank:<CODE>`` endpoint.

    The date range is a rolling ``[year-LOOKBACK_YEARS : year]`` window derived from ``now``
    (injected so the URL is deterministic under test).
    """
    code = indicator_code(endpoint)
    moment = now or datetime.now(UTC)
    end_year = moment.astimezone(UTC).year
    start_year = end_year - LOOKBACK_YEARS
    country_path = ";".join(countries)
    return (
        f"{WB_BASE}/country/{country_path}/indicator/{code}"
        f"?format=json&per_page={PER_PAGE}&date={start_year}:{end_year}"
    )


def parse_payload(raw: bytes | str) -> list[dict[str, object]]:
    """Decode the WB response (BOM-tolerant) and return its observation rows.

    The WB envelope is ``[meta, rows]``. On an empty/absent result the second element is
    ``null`` or missing; on an API error the payload is ``[{"message":[...]}]`` (length 1).
    Any non-conforming shape yields an empty list — degraded, never a crash.
    """
    text = raw.decode("utf-8-sig") if isinstance(raw, bytes) else raw.lstrip("﻿")
    decoded: object = json.loads(text)
    if not isinstance(decoded, list) or len(decoded) < 2:
        return []
    rows = decoded[1]
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _nested_value(row: dict[str, object], key: str, field: str) -> str:
    """Read ``row[key][field]`` when ``row[key]`` is a dict (WB nests ``indicator``/``country``)."""
    nested = row.get(key)
    if isinstance(nested, dict):
        value = nested.get(field, "")
        return str(value) if value is not None else ""
    return ""


def latest_per_country(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Flatten WB rows to one latest non-null observation per country, sorted by country name.

    Each output row is flat (``country``, ``iso3``, ``indicator``, ``indicator_code``, ``date``,
    ``value``) so the generic L1 renderer emits a clean markdown table with no nested objects.
    """
    latest: dict[str, dict[str, object]] = {}
    for row in rows:
        if row.get("value") is None:
            continue
        iso3 = str(row.get("countryiso3code") or "")
        if not iso3:
            continue
        date = str(row.get("date") or "")
        current = latest.get(iso3)
        if current is None or date > str(current.get("date") or ""):
            latest[iso3] = row

    flat: list[dict[str, object]] = [
        {
            "country": _nested_value(row, "country", "value"),
            "iso3": row.get("countryiso3code", ""),
            "indicator": _nested_value(row, "indicator", "value"),
            "indicator_code": _nested_value(row, "indicator", "id"),
            "date": row.get("date", ""),
            "value": row.get("value"),
        }
        for row in latest.values()
    ]
    flat.sort(key=lambda entry: str(entry["country"]))
    return flat


def transform(raw: bytes | str) -> list[dict[str, object]]:
    """Full pure pipeline: raw WB bytes/str -> flat latest-per-country observation rows."""
    return latest_per_country(parse_payload(raw))
