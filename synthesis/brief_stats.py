#!/usr/bin/env python3
"""Build-time key-figure bands for the L2 brief pages.

Every brief opens with the numbers it is about — chips (big number + caption) and, where
the latest L1 note already carries a series, an inline sparkline (KPI-as-curve, the same
doctrine the landing pulse follows). All of it is derived at build time from the newest
committed L1 day: no JavaScript, no fetch, byte-stable output, and any parse problem
degrades to "no band" rather than a broken page.

Series come straight from single L1 notes (the feeds ship their own history): EU gas
storage + US crude carry 8 reporting weeks, Mauna Loa CO2 + NSIDC sea-ice carry 12 months,
crypto quotes carry a 48-point intraday sparkline. Count-style themes get chips only.
"""

from __future__ import annotations

import html
import json
import re
from typing import TYPE_CHECKING, Any

from synthesis.fire_geo import country_tally

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["brief_band_html"]

_FIELD_RE = re.compile(r"^\| (\w+) \| (.*) \|$")


def _fields(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = _FIELD_RE.match(line.rstrip())
            if m and m.group(1) != "field":
                out[m.group(1)] = m.group(2)
    except OSError:
        pass
    return out


def _load(day_dir: Path, source_key: str, field_name: str) -> Any:
    raw = _fields(day_dir / f"{source_key}.md").get(field_name)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return None


def _chip(value: str, caption: str) -> dict[str, str]:
    return {"kind": "chip", "value": value, "caption": caption}


def _spark(label: str, series: list[float], latest: str) -> dict[str, Any]:
    return {"kind": "spark", "label": label, "series": series, "latest": latest}


def _num(x: Any) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


# ── per-theme extractors (each returns a list of chip/spark dicts, or []) ──────────────


def _energy(day: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    gas = _load(day, "natural-gas-storage-eu", "weeks") or []
    if gas:
        series = [_num(w.get("storBcf")) for w in reversed(gas)]
        out.append(_spark("EU gas storage, Bcf (8 wks)", series, f"{series[-1]:,.0f}"))
    crude = _load(day, "crude-oil-inventories", "weeks") or []
    if crude:
        series = [_num(w.get("stocksMb")) / 1000 for w in reversed(crude)]
        out.append(_spark("US crude stocks, Mb (8 wks)", series, f"{series[-1]:,.1f}"))
    prices = _load(day, "energy-prices", "prices") or []
    for p in prices:
        out.append(
            _chip(
                f"${_num(p.get('price')):,.2f}",
                f"{p.get('name', '?')} ({_num(p.get('change')):+.1f}%)",
            )
        )
    return out


def _climate(day: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    co2 = _load(day, "co2-monitoring", "monitoring") or {}
    trend = co2.get("trend12m") or []
    if trend:
        series = [_num(t.get("ppm")) for t in trend]
        out.append(
            _spark("CO2 ppm, Mauna Loa (12 mo)", series, f"{_num(co2.get('currentPpm')):.1f}")
        )
    ice = _load(day, "sea-ice-extent", "data") or {}
    it = ice.get("iceTrend12m") or []
    if it:
        series = [_num(t.get("extentMkm2")) for t in it]
        out.append(_spark("Arctic extent, Mkm2 (12 mo)", series, f"{series[-1]:.2f}"))
    if ice:
        out.append(_chip(f"{_num(ice.get('sstAnomalyC')):+.2f} C", "global SST anomaly"))
        out.append(_chip(f"{_num(ice.get('seaLevelMmAbove1993')):.1f} mm", "sea level vs 1993"))
    return out


def _macro(day: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    quotes = _load(day, "crypto-quotes", "quotes") or []
    for q in quotes[:2]:
        series = [_num(v) for v in (q.get("sparkline") or [])]
        if series:
            out.append(
                _spark(
                    f"{q.get('symbol', '?')} intraday, USD",
                    series,
                    f"${_num(q.get('price')):,.0f}",
                )
            )
    for q in quotes[2:6]:
        out.append(
            _chip(
                f"${_num(q.get('price')):,.2f}",
                f"{q.get('symbol')} ({_num(q.get('change')):+.1f}%)",
            )
        )
    return out


def _geo(day: Path) -> list[dict[str, Any]]:
    quakes = _load(day, "earthquakes", "earthquakes") or []
    if not quakes:
        return []
    mags = [_num(q.get("magnitude")) for q in quakes]
    return [
        _chip(str(len(quakes)), "M4.5+ events, 7-day window"),
        _chip(str(sum(1 for m in mags if m >= 5)), "of them M5+"),
        _chip(str(sum(1 for m in mags if m >= 6)), "of them M6+"),
        _chip(f"M{max(mags):.1f}", "strongest recorded"),
    ]


def _prediction(day: Path) -> list[dict[str, Any]]:
    markets = _load(day, "prediction-markets", "markets") or []
    if not markets:
        return []
    m = markets[0]
    return [
        _chip(f"{_num(m.get('yesPrice')) * 100:.1f}%", "implied probability (yes price)"),
        _chip(f"${_num(m.get('volume')) / 1e6:,.1f}M", "cumulative traded volume"),
        _chip(str(len(markets)), "market(s) listed by the feed"),
    ]


def _hazards(day: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    fires = _load(day, "wildfire-detections", "fireDetections") or []
    if fires:
        out.append(_chip(str(len(fires)), "top fire detections by FRP"))
        # Exact country attribution from the feed's own per-detection region field
        # (IQ #1161 — deterministic, no reverse-geocode). The dominant country + its share.
        geo = country_tally(fires)
        if geo.dominant is not None:
            name, count = geo.dominant
            out.append(_chip(name, f"{count} of {geo.attributed} detections (top country)"))
    thermal = _load(day, "thermal-escalations", "summary") or {}
    if thermal:
        out.append(_chip(str(thermal.get("clusterCount", "?")), "thermal escalation clusters"))
    events = _load(day, "natural-events", "events") or []
    if events:
        out.append(_chip(str(len(events)), "active GDACS/EONET events"))
    rad = _fields(day / "radiation-observations.md")
    if rad.get("anomalyCount") is not None:
        out.append(_chip(str(rad.get("anomalyCount")), "radiation anomalies"))
    return out


def _health(day: Path) -> list[dict[str, Any]]:
    obs = _load(day, "disease-outbreaks", "outbreaks") or []
    if not obs:
        return []
    levels = [str(o.get("alertLevel", "")).rsplit("_", 1)[-1].lower() for o in obs]
    diseases: dict[str, int] = {}
    for o in obs:
        d = str(o.get("disease") or "?")
        diseases[d] = diseases.get(d, 0) + 1
    top = max(diseases.items(), key=lambda kv: kv[1])
    return [
        _chip(str(len(obs)), "active outbreak notifications"),
        _chip(str(levels.count("alert") + levels.count("warning")), "at alert level or above"),
        _chip(str(top[1]), f"{top[0]} notifications (largest)"),
    ]


def _conflict(day: Path) -> list[dict[str, Any]]:
    ev = _load(day, "conflict-events-ucdp", "events") or []
    if not ev:
        return []
    deaths = sum(int(_num(e.get("deathsBest"))) for e in ev)
    countries: dict[str, int] = {}
    for e in ev:
        c = str(e.get("country") or "?")
        countries[c] = countries.get(c, 0) + 1
    top = max(countries.items(), key=lambda kv: kv[1])
    return [
        _chip(f"{len(ev):,}", "recorded events, latest UCDP window"),
        _chip(f"{deaths:,}", "summed best-estimate fatalities"),
        _chip(str(top[1]), f"events in {top[0]} (most)"),
    ]


def _cyber(day: Path) -> list[dict[str, Any]]:
    th = _load(day, "cyber-threats", "threats") or []
    if not th:
        return []
    crit = sum(1 for t in th if "CRITICAL" in str(t.get("severity", "")))
    return [
        _chip(str(len(th)), "active threat indicator(s)"),
        _chip(str(crit), "critical severity"),
    ]


def _orbital(day: Path) -> list[dict[str, Any]]:
    sats = _load(day, "orbital-satellites", "satellites") or []
    if not sats:
        return []
    owners: dict[str, int] = {}
    for s in sats:
        owners[str(s.get("country") or "?")] = owners.get(str(s.get("country") or "?"), 0) + 1
    top = max(owners.items(), key=lambda kv: kv[1])
    return [
        _chip(str(len(sats)), "tracked objects (TLE)"),
        _chip(str(top[1]), f"operated by {top[0]} (most)"),
        _chip(str(sum(1 for s in sats if str(s.get("type")) == "military")), "military-labelled"),
    ]


def _humanitarian(day: Path) -> list[dict[str, Any]]:
    s = _load(day, "displacement-flows", "summary") or {}
    tot = s.get("globalTotals") or {}
    if not tot:
        return []
    return [
        _chip(f"{_num(tot.get('total')) / 1e6:,.1f}M", "forcibly displaced (published year)"),
        _chip(f"{_num(tot.get('idps')) / 1e6:,.1f}M", "internally displaced"),
        _chip(f"{_num(tot.get('refugees')) / 1e6:,.1f}M", "refugees"),
    ]


def _infrastructure(day: Path) -> list[dict[str, Any]]:
    ou = _load(day, "internet-outages", "outages") or []
    if not ou:
        return []
    nation = sum(1 for o in ou if str(o.get("outageType")) == "NATIONWIDE")
    return [
        _chip(str(len(ou)), "active internet outages"),
        _chip(str(nation), "nationwide in scope"),
        _chip(
            str(sum(1 for o in ou if str(o.get("cause")) == "GOVERNMENT_DIRECTED")),
            "government-directed (source label)",
        ),
    ]


_EXTRACTORS = {
    "energy-supply": _energy,
    "climate-signals": _climate,
    "macro-markets": _macro,
    "geophysical": _geo,
    "prediction-markets": _prediction,
    "environmental-hazards": _hazards,
    "public-health": _health,
    "conflict-watch": _conflict,
    "cyber-watch": _cyber,
    "orbital-watch": _orbital,
    "humanitarian": _humanitarian,
    "infrastructure-watch": _infrastructure,
}


def brief_band_html(theme: str, latest_day_dir: Path) -> str:
    """The key-figures band for one brief page. Empty string when nothing extracts."""
    fn = _EXTRACTORS.get(theme)
    if not fn or not latest_day_dir.is_dir():
        return ""
    try:
        items = fn(latest_day_dir)
    except Exception:
        return ""
    if not items:
        return ""
    from synthesis.sparkline import sparkline_svg  # lazy: avoids a module-import cycle

    parts: list[str] = ['<div class="stats-band">']
    for it in items:
        if it["kind"] == "chip":
            parts.append(
                f'<div class="stat"><b>{html.escape(str(it["value"]))}</b>'
                f"<span>{html.escape(str(it['caption']))}</span></div>"
            )
        else:
            svg = sparkline_svg(it["series"], width=150, height=34)
            parts.append(
                f'<div class="stat stat-sparkline"><b>{html.escape(str(it["latest"]))}</b>'
                f"<span>{html.escape(str(it['label']))}</span>{svg}</div>"
            )
    parts.append("</div>")
    return "".join(parts)
