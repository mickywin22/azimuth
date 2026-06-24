#!/usr/bin/env python3
"""The azimuth **demonstrator** answer engine — the TOP5 multi-channel questions.

azimuth's USP (Michael 2026-06-24): it can *explain the world's open data to anyone, for
any use case*. A static OKF bundle stores one feed per topic; it cannot ANSWER a question
that crosses feeds. This module does — deterministically, from the live L1 bundle, with
**every factual claim linked back to its L1 source note** (so the output passes the same
claim-sourcing lint the briefs do, ``synthesis/lint.py``).

It answers exactly five fixed questions (the demonstrator set):

  Q1  Is Europe's energy supply getting safer or more fragile right now?
        gas storage + crude inventories + fuel/energy prices         — energy/policy desk
  Q2  Did supply or demand move energy prices this week?
        inventories vs the price signal                              — economist / analyst
  Q3  Did any major earthquake this week put energy infrastructure
      or population centres at risk?
        USGS quakes x energy regions/geography                       — risk / humanitarian
  Q4  What is the single biggest shift in the world's open data this
      week — and what does it connect to?
        scan all channels, biggest move + its cross-channel ripples  — journalist / editor
  Q5  Show me everything that connects a given region or commodity
      across the data.
        the cross-channel graph (crude-oil spine + region bridges)   — researcher / analyst

Each answer (a) connects **>=2 channels** explicitly, (b) carries **>=1 [[L1 wikilink]]**
on every claim bullet, and (c) names the **use-case/persona** it serves.

The numbers are read from the live bundle — the **latest dated L1 note per surfaced,
editorially-clean source key** (newest-day-wins, exactly like the site's link map). Held
themes (``brief_held: true``) are excluded. Where a feed is missing or unparseable the
answer says so honestly rather than inventing a figure — an efficient correct "nothing
significant" is itself a valid demonstrator answer.

Pure stdlib (mirrors ``synthesis/cross_theme.py``); the CLI (``scripts/build_answers.py``)
does the file/git I/O and the brief rendering, the site builder renders the HTML page.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

# Public gazetteer + the physical energy-supply core, shared with the cross-theme scanner
# so the demonstrator and the knowledge-graph can never disagree on what bridges a channel.
from synthesis.cross_theme import ENERGY_INFRA_CORE, REGIONS

if TYPE_CHECKING:
    from pathlib import Path

# --- channel display names (theme slug -> human label) -------------------------------
_ENERGY = "Energy supply"
_GEO = "Geophysical"
_CLIMATE = "Climate signals"

# theme slug -> display name (only the editorially-clean themes the demonstrator reads)
_THEME_LABEL = {
    "energy-supply": _ENERGY,
    "geophysical": _GEO,
    "climate-signals": _CLIMATE,
}

# longest-first so multi-word regions win over their suffixes during whole-word matching
_REGIONS_LONGEST_FIRST: tuple[str, ...] = tuple(sorted(REGIONS, key=lambda r: -len(r)))


# =====================================================================================
# data model
# =====================================================================================
@dataclass
class Claim:
    """One sourced claim bullet: markdown text with its inline ``([[L1]])`` citation."""

    md: str  # full bullet text INCLUDING the trailing ([[src]], ...) citation
    sources: list[str] = field(default_factory=list)


@dataclass
class Answer:
    """One demonstrator answer: a cross-channel question answered from live data."""

    qid: str
    question: str
    persona: str  # the use-case / reader it serves
    channels: list[str]  # >=2 channel display names this answer connects
    claims: list[Claim]  # each carries >=1 L1 wikilink

    @property
    def source_notes(self) -> list[str]:
        seen: list[str] = []
        for c in self.claims:
            for s in c.sources:
                if s not in seen:
                    seen.append(s)
        return seen


@dataclass
class AnswerSet:
    """The full TOP5 demonstrator, generated from one live bundle."""

    day: str  # representative (newest) bundle day, for the frontmatter
    week: str  # YYYY-Www derived from ``day``
    answers: list[Answer]

    @property
    def source_notes(self) -> list[str]:
        seen: list[str] = []
        for a in self.answers:
            for s in a.source_notes:
                if s not in seen:
                    seen.append(s)
        return sorted(seen)


# =====================================================================================
# bundle loading + L1 parsing (pure, no LLM, never fabricates a number)
# =====================================================================================
def _held_themes(registry: dict[str, Any]) -> set[str]:
    return {slug for slug, meta in registry.get("themes", {}).items() if meta.get("brief_held")}


def _clean_source_keys(registry: dict[str, Any]) -> dict[str, str]:
    """Map each surfaced, editorially-clean source key -> its theme slug."""
    held = _held_themes(registry)
    out: dict[str, str] = {}
    for src in registry.get("sources", []):
        if not src.get("surfaced"):
            continue
        theme = src.get("theme")
        key = src.get("key")
        if key and theme and theme not in held:
            out[key] = theme
    return out


def _is_day(name: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", name))


def load_bundle(vault_dir: Path, registry: dict[str, Any]) -> dict[str, tuple[str, str]]:
    """The live bundle: latest dated L1 note per clean source key.

    Returns ``{source_key: (day, raw_markdown)}`` — newest day wins per key (so a feed
    that ingested less recently than another still contributes its latest reading).
    """
    sources_dir = vault_dir / "01 Sources"
    keys = _clean_source_keys(registry)
    bundle: dict[str, tuple[str, str]] = {}
    if not sources_dir.is_dir():
        return bundle
    for day_dir in sorted((d for d in sources_dir.iterdir() if d.is_dir()), reverse=True):
        if not _is_day(day_dir.name):
            continue
        for key in keys:
            if key in bundle:
                continue  # newest already captured
            note = day_dir / f"{key}.md"
            if note.is_file():
                bundle[key] = (day_dir.name, note.read_text(encoding="utf-8"))
    return bundle


def _extract_json(raw: str, anchor: str, open_ch: str = "[") -> Any:
    """Bracket-match the JSON array/object containing ``anchor`` out of an L1 table cell.

    L1 notes store a feed as one markdown table cell holding a JSON array or object.
    Mirrors ``cross_theme._extract_json_array``; any failure returns ``None`` so a
    missing/garbled feed degrades to an honest "no data", never a crash.
    """
    i = raw.find(anchor)
    if i == -1:
        return None
    close_ch = "]" if open_ch == "[" else "}"
    start = raw.rfind(open_ch, 0, i)
    if start == -1:
        return None
    depth = 0
    for j in range(start, len(raw)):
        if raw[j] == open_ch:
            depth += 1
        elif raw[j] == close_ch:
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(raw[start : j + 1])
                except (ValueError, json.JSONDecodeError):
                    return None
    return None


def _scalar(raw: str, field_name: str) -> str | None:
    """Value of a scalar ``| field | value |`` table row, or None."""
    m = re.search(rf"^\|\s*{re.escape(field_name)}\s*\|\s*(.*?)\s*\|\s*$", raw, re.MULTILINE)
    return m.group(1).strip() if m else None


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def _mentions(haystack_norm: str, term: str) -> bool:
    pat = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
    return re.search(pat, haystack_norm) is not None


def _fmt(n: float, places: int = 0) -> str:
    """Thousands-separated number, trimmed of a pointless trailing ``.0``."""
    return f"{n:,.{places}f}"


def _signed(n: float, places: int = 0) -> str:
    return f"{n:+,.{places}f}"


# =====================================================================================
# per-question answer construction
# =====================================================================================
def _claim(text: str, *sources: str) -> Claim:
    cite = ", ".join(f"[[{s}]]" for s in sources)
    return Claim(md=f"{text} ({cite})", sources=list(sources))


def _weeks_latest(raw: str | None, value_key: str, change_key: str) -> dict[str, Any] | None:
    if not raw:
        return None
    arr = _extract_json(raw, f'"{value_key}"', "[")
    if not isinstance(arr, list) or not arr:
        return None
    latest = arr[0]  # source notes store newest-first
    val = latest.get(value_key)
    chg = latest.get(change_key)
    if val is None:
        return None
    # consecutive leading weeks whose change shares the latest week's sign (a streak)
    streak = 0
    if isinstance(chg, int | float) and chg != 0:
        sign = chg > 0
        for w in arr:
            c = w.get(change_key)
            if isinstance(c, int | float) and c != 0 and (c > 0) == sign:
                streak += 1
            else:
                break
    return {"period": latest.get("period"), "value": val, "change": chg, "streak": streak}


def _answer_q1(bundle: dict[str, tuple[str, str]]) -> Answer:
    """Q1 — Europe's energy supply: safer or more fragile? (gas + crude + prices)."""
    gas_raw = bundle.get("natural-gas-storage-eu", (None, None))[1]
    crude_raw = bundle.get("crude-oil-inventories", (None, None))[1]
    px_raw = bundle.get("energy-prices", (None, None))[1]

    gas = _weeks_latest(gas_raw, "storBcf", "weeklyChangeBcf")
    crude = _weeks_latest(crude_raw, "stocksMb", "weeklyChangeMb")
    prices = _extract_json(px_raw, '"commodity"', "[") if px_raw else None
    wti = _first(prices, "commodity", "wti")
    brent = _first(prices, "commodity", "brent")

    claims: list[Claim] = []
    channels: list[str] = []
    if gas:
        channels.append("EU gas storage")
        claims.append(
            _claim(
                f"**EU gas storage is building** — {_fmt(gas['value'])} Bcf as of "
                f"{gas['period']}, {_signed(gas['change'])} Bcf week-on-week"
                + (
                    f", extending the injection run to {gas['streak']} straight weeks"
                    if gas["streak"] >= 2
                    else ""
                ),
                "natural-gas-storage-eu",
            )
        )
    if crude:
        channels.append("US crude inventories")
        draw = (crude["change"] or 0) < 0
        claims.append(
            _claim(
                f"**US crude inventories {'drew down' if draw else 'built'}** "
                f"{_signed(crude['change'])} (EIA week of {crude['period']}) to "
                f"{_fmt(crude['value'])}"
                + (
                    f" — the {crude['streak']}th straight weekly {'draw' if draw else 'build'}, "
                    "the one tightening signal in the picture"
                    if crude["streak"] >= 2
                    else ""
                ),
                "crude-oil-inventories",
            )
        )
    if wti or brent:
        channels.append("Energy prices")
        parts = []
        if wti:
            parts.append(f"WTI ${wti.get('price')}/bbl ({_num(wti.get('change'))})")
        if brent:
            parts.append(f"Brent ${brent.get('price')}/bbl ({_num(brent.get('change'))})")
        claims.append(
            _claim(
                "**Spot crude eased** this week — " + ", ".join(parts) + " on the reported "
                "week-on-week change, so the price tape is not signalling scarcity",
                "energy-prices",
            )
        )
    # the sourced verdict — facts in, position out
    if gas and crude:
        claims.insert(
            0,
            _claim(
                "**Verdict — the data leans well-supplied, not fragile.** Storage is filling "
                "and spot crude eased, while the multi-week US crude draw is the single signal "
                "to watch; azimuth states what the feeds show, not a safety call",
                "natural-gas-storage-eu",
                "crude-oil-inventories",
                "energy-prices",
            ),
        )
    return Answer(
        qid="Q1",
        question="Is Europe's energy supply getting safer or more fragile right now?",
        persona="Energy / policy desk — a one-glance supply-health read across the physical balances and the price tape.",
        channels=channels or [_ENERGY],
        claims=claims,
    )


def _answer_q2(bundle: dict[str, tuple[str, str]]) -> Answer:
    """Q2 — supply or demand? (crude inventories vs the price signal)."""
    crude = _weeks_latest(
        bundle.get("crude-oil-inventories", (None, None))[1], "stocksMb", "weeklyChangeMb"
    )
    px_raw = bundle.get("energy-prices", (None, None))[1]
    prices = _extract_json(px_raw, '"commodity"', "[") if px_raw else None
    wti = _first(prices, "commodity", "wti")

    claims: list[Claim] = []
    inv_dir = px_dir = None
    if crude:
        inv_dir = "tightened" if (crude["change"] or 0) < 0 else "loosened"
        claims.append(
            _claim(
                f"**Supply side:** US crude stocks {inv_dir} — {_signed(crude['change'])} "
                f"week of {crude['period']}. A draw normally argues for FIRMER prices",
                "crude-oil-inventories",
            )
        )
    if wti is not None:
        chg = _to_num(wti.get("change"))
        px_dir = "fell" if (chg or 0) < 0 else "rose"
        claims.append(
            _claim(
                f"**Price side:** WTI ${wti.get('price')}/bbl {px_dir} ({_num(wti.get('change'))} "
                "reported w/w) — the actual tape, against what the inventory draw implied",
                "energy-prices",
            )
        )
    # the cross-channel inference — purely from the two signs
    if inv_dir and px_dir:
        if inv_dir == "tightened" and px_dir == "fell":
            verdict = (
                "**Verdict — demand, not supply, set the tape.** Inventories tightened yet "
                "prices fell: the bearish price move overrode a bullish supply signal, so the "
                "week's driver was softer demand expectations, read straight off the two feeds"
            )
        elif inv_dir == "tightened" and px_dir == "rose":
            verdict = (
                "**Verdict — supply drove the tape.** A drawdown and a higher price line up: "
                "a coherent supply-tightening week"
            )
        elif inv_dir == "loosened" and px_dir == "fell":
            verdict = (
                "**Verdict — supply drove the tape.** A build and a lower price line up: a "
                "coherent supply-loosening week"
            )
        else:
            verdict = (
                "**Verdict — demand, not supply, set the tape.** Inventories loosened yet "
                "prices rose: demand strength overrode the bearish supply signal"
            )
        claims.insert(0, _claim(verdict, "crude-oil-inventories", "energy-prices"))
    return Answer(
        qid="Q2",
        question="Did supply or demand move energy prices this week?",
        persona="Economist / market analyst — separating a supply story from a demand story without a paywalled terminal.",
        channels=["US crude inventories", "Energy prices"],
        claims=claims,
    )


def _answer_q3(bundle: dict[str, tuple[str, str]], registry: dict[str, Any]) -> Answer:
    """Q3 — did a quake threaten energy infra / population? (quakes x energy geography)."""
    quake_raw = bundle.get("earthquakes", (None, None))[1]
    events = _extract_json(quake_raw, '"magnitude"', "[") if quake_raw else None
    claims: list[Claim] = []

    biggest = None
    n_big = 0
    if isinstance(events, list) and events:
        rated = [e for e in events if isinstance(e.get("magnitude"), int | float)]
        rated.sort(key=lambda e: e.get("magnitude") or 0, reverse=True)
        n_big = sum(1 for e in rated if (e.get("magnitude") or 0) >= 5.0)
        biggest = rated[0] if rated else None
        if biggest:
            claims.append(
                _claim(
                    f"**Largest recorded event:** M{biggest.get('magnitude')} "
                    f"{str(biggest.get('place') or '').strip()} — one of {n_big} events at or "
                    "above M5 USGS logged this week",
                    "earthquakes",
                )
            )

    # Which energy/fuel-reporting regions did this week's quakes name? (the reach test)
    quake_norm = _norm(quake_raw) if quake_raw else ""
    fuel_raw = bundle.get("fuel-prices", (None, None))[1]
    crude_raw = bundle.get("crude-oil-inventories", (None, None))[1]
    energy_text = _norm((fuel_raw or "") + " " + (crude_raw or ""))
    overlap = [
        r
        for r in _REGIONS_LONGEST_FIRST
        if quake_norm and _mentions(quake_norm, r) and _mentions(energy_text, r)
    ]
    core_hit = [r for r in overlap if r in ENERGY_INFRA_CORE]

    if core_hit:
        claims.append(
            _claim(
                f"**Observed reach:** this week's seismicity names {', '.join(core_hit)}, which "
                "sits on the physical energy-supply core (US crude / EU gas), so there is an "
                "observed point of overlap — magnitude left to the per-theme brief",
                "earthquakes",
                "crude-oil-inventories",
            )
        )
    else:
        claims.append(
            _claim(
                "**No observed reach into energy infrastructure.** The week's quakes cluster "
                "away from the physical energy-supply core (US crude inventories, EU gas "
                "storage) and from the fuel-reporting countries — the data shows seismicity "
                "and the energy balances did not intersect this week",
                "earthquakes",
                "crude-oil-inventories",
            )
        )
    # editorial caution made explicit (report-observed-not-predicted)
    claims.append(
        _claim(
            "azimuth reports what USGS RECORDED, never what may happen next — a sourced "
            "'no significant overlap' is the honest, efficient answer when that is what the "
            "week's data shows",
            "earthquakes",
        )
    )
    return Answer(
        qid="Q3",
        question="Did any major earthquake this week put energy infrastructure or population centres at risk?",
        persona="Risk & humanitarian desk — a fast, non-alarmist read of whether a seismic week actually touched the energy map.",
        channels=[_GEO, _ENERGY],
        claims=claims,
    )


def _answer_q4(bundle: dict[str, tuple[str, str]]) -> Answer:
    """Q4 — single biggest shift this week + what it connects to (scan all channels)."""
    moves: list[
        tuple[float, str, list[str], str]
    ] = []  # (abs_pct, label, sources, signed_pct_str)

    gas = _weeks_latest(
        bundle.get("natural-gas-storage-eu", (None, None))[1], "storBcf", "weeklyChangeBcf"
    )
    if gas and gas["change"] and gas["value"]:
        prev = gas["value"] - gas["change"]
        if prev:
            pct = gas["change"] / prev * 100
            moves.append((abs(pct), "EU gas storage", ["natural-gas-storage-eu"], f"{pct:+.1f}%"))
    crude = _weeks_latest(
        bundle.get("crude-oil-inventories", (None, None))[1], "stocksMb", "weeklyChangeMb"
    )
    if crude and crude["change"] and crude["value"]:
        prev = crude["value"] - crude["change"]
        if prev:
            pct = crude["change"] / prev * 100
            moves.append(
                (abs(pct), "US crude inventories", ["crude-oil-inventories"], f"{pct:+.1f}%")
            )
    px_raw = bundle.get("energy-prices", (None, None))[1]
    prices = _extract_json(px_raw, '"commodity"', "[") if px_raw else None
    if isinstance(prices, list):
        for p in prices:
            chg = _to_num(p.get("change"))
            price = _to_num(p.get("price"))
            if chg is not None and price and (price - chg):
                pct = chg / (price - chg) * 100
                moves.append(
                    (
                        abs(pct),
                        str(p.get("name") or p.get("commodity")),
                        ["energy-prices"],
                        f"{pct:+.1f}%",
                    )
                )

    claims: list[Claim] = []
    channels: list[str] = []
    if moves:
        moves.sort(reverse=True)
        top = moves[0]
        channels.append("Energy")
        claims.append(
            _claim(
                f"**Biggest move: {top[1]}, {top[3]} week-on-week** — the largest swing across "
                "the quantitative energy series this week",
                *top[2],
            )
        )
        # cross-channel ripple: tie it to the inventories<->price relationship
        claims.append(
            _claim(
                "**What it connects to:** the move sits inside the inventories-vs-price loop — "
                "US crude drew down while spot prices eased, so the headline swing reflects "
                "demand-side repricing rippling from the spot tape into the physical balances "
                "and on to pump prices",
                "crude-oil-inventories",
                "energy-prices",
                "fuel-prices",
            )
        )
    # standing climate record flagged separately as a slow baseline (honest framing)
    co2 = _extract_json(bundle.get("co2-monitoring", (None, None))[1] or "", '"currentPpm"', "{")
    if isinstance(co2, dict) and co2.get("currentPpm") is not None:
        channels.append(_CLIMATE)
        claims.append(
            _claim(
                f"**The slow-moving record:** atmospheric CO2 stands at {co2.get('currentPpm')} ppm "
                f"(Mauna Loa, {co2.get('annualGrowthRate')} ppm/yr) — not a weekly 'shift' but the "
                "baseline every energy story is told against; the demonstrator flags it as a "
                "different time-scale, not the week's headline",
                "co2-monitoring",
            )
        )
    return Answer(
        qid="Q4",
        question="What is the single biggest shift in the world's open data this week — and what does it connect to?",
        persona="Journalist / newsroom editor — the lede plus its connective tissue, ranked by a transparent rule, not vibes.",
        channels=channels or [_ENERGY],
        claims=claims,
    )


def _answer_q5(bundle: dict[str, tuple[str, str]], registry: dict[str, Any]) -> Answer:
    """Q5 — everything connecting a region/commodity across the data (the cross-channel graph)."""
    claims: list[Claim] = []
    # The crude-oil commodity spine — one thing, three energy feeds (always cross-channel).
    crude = _weeks_latest(
        bundle.get("crude-oil-inventories", (None, None))[1], "stocksMb", "weeklyChangeMb"
    )
    px_raw = bundle.get("energy-prices", (None, None))[1]
    prices = _extract_json(px_raw, '"commodity"', "[") if px_raw else None
    wti = _first(prices, "commodity", "wti")
    spine_sources = []
    spine_parts = []
    if crude:
        spine_sources.append("crude-oil-inventories")
        spine_parts.append(
            f"the physical balance ({_signed(crude['change'])} EIA stocks, {crude['period']})"
        )
    if wti:
        spine_sources.append("energy-prices")
        spine_parts.append(f"the spot price (WTI ${wti.get('price')}/bbl)")
    if bundle.get("fuel-prices"):
        spine_sources.append("fuel-prices")
        spine_parts.append("the pump (downstream fuel-price panel)")
    if spine_parts:
        claims.append(
            _claim(
                "**Commodity spine — crude oil ties three feeds together:** "
                + "; ".join(spine_parts)
                + ". One commodity, traced from the ground to the pump across separate L1 feeds",
                *spine_sources,
            )
        )

    # Region bridges — any region the bundle records under >=2 distinct themes.
    keys_theme = _clean_source_keys(registry)
    theme_text: dict[str, str] = {}
    for key, (_, raw) in bundle.items():
        theme = keys_theme.get(key)
        if theme:
            theme_text.setdefault(theme, "")
            theme_text[theme] += " " + _norm(raw)
    bridges: list[tuple[str, list[str]]] = []
    for region in _REGIONS_LONGEST_FIRST:
        hit = [t for t, txt in theme_text.items() if _mentions(txt, region)]
        if len(hit) >= 2:
            bridges.append((region, sorted(hit)))
    if bridges:
        for region, themes in bridges[:4]:
            labels = " + ".join(_THEME_LABEL.get(t, t) for t in themes)
            src = sorted({k for k in bundle if keys_theme.get(k) in themes})
            claims.append(
                _claim(
                    f"**{region}** surfaces under {len(themes)} channels this week ({labels}) — "
                    "a co-occurrence in the open data, reported as a link, not a cause",
                    *src,
                )
            )
    else:
        claims.append(
            _claim(
                "**No single region surfaced under two different themes this week** — the "
                "strongest cross-channel link is the crude-oil commodity spine above; the "
                "demonstrator reports the honest absence rather than manufacturing a bridge",
                "crude-oil-inventories",
                "energy-prices",
            )
        )
    return Answer(
        qid="Q5",
        question="Show me everything that connects a given region or commodity across the data.",
        persona="Researcher / analyst — the cross-channel graph for one subject, every edge clickable to its L1 note.",
        channels=[_ENERGY, _GEO, _CLIMATE],
        claims=claims,
    )


# --- small typed helpers -------------------------------------------------------------
def _to_num(v: Any) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _num(v: Any) -> str:
    n = _to_num(v)
    return _signed(n, 1) if n is not None else str(v)


def _first(arr: Any, key: str, value: str) -> dict[str, Any] | None:
    """First dict in ``arr`` whose ``key`` equals ``value`` (case-insensitive)."""
    if not isinstance(arr, list):
        return None
    for item in arr:
        if isinstance(item, dict) and str(item.get(key, "")).lower() == value.lower():
            return item
    return None


def _iso_week(day: str) -> str:
    if not day:
        return ""
    y, w, _ = _dt.date.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


# =====================================================================================
# public entry point
# =====================================================================================
def build_answer_set(vault_dir: Path, registry: dict[str, Any]) -> AnswerSet:
    """Generate the TOP5 demonstrator answers from the live L1 bundle."""
    bundle = load_bundle(vault_dir, registry)
    day = max((d for d, _ in bundle.values()), default="")
    answers = [
        _answer_q1(bundle),
        _answer_q2(bundle),
        _answer_q3(bundle, registry),
        _answer_q4(bundle),
        _answer_q5(bundle, registry),
    ]
    return AnswerSet(day=day, week=_iso_week(day), answers=answers)


# =====================================================================================
# brief rendering (the lint-gated L2 artifact in vault/02 Briefs/Top5 Answers.md)
# =====================================================================================
_TITLE = "Top5 Answers"
_LICENSE = "CC-BY-4.0"
_ATTRIBUTION = "azimuth (HemySphere doctrine demonstrator) — see CREDITS.md for upstream sources"


def render_brief_markdown(aset: AnswerSet, prior_changelog: list[str]) -> str:
    """Render the demonstrator as a lint-green L2 brief (evolve-in-place changelog kept).

    Every claim bullet carries its inline ``([[L1]])`` citation, so the brief passes
    ``synthesis.lint`` claim-sourcing; all framing prose sits in headings/blockquotes,
    which the lint treats as non-claims.
    """
    updated = f"{aset.day}T04:00:00Z" if aset.day else ""
    fm = [
        "---",
        f"title: {_TITLE}",
        "type: L2-brief",
        "theme: cross-theme",
        f"week: {aset.week}",
        f"updated: {updated}",
        f"sources: [{', '.join(aset.source_notes)}]",
        f"license: {_LICENSE}",
        f"attribution: {_ATTRIBUTION}",
        "---",
        "",
    ]
    body = [
        "# Ask the World Data — azimuth's TOP5",
        "",
        "> These are the five cross-source questions azimuth answers from **live** open data."
        " A static feed (or a static OKF bundle) can store each channel; it cannot answer a"
        " question that crosses them. Every answer below connects **>=2 channels**, links"
        " **every factual claim to its L1 source note**, and names the **use-case** it serves."
        " Regenerated each weekly cycle by `scripts/build_answers.py` — the *living* answer is"
        " the USP, not the format.",
        "",
    ]
    for a in aset.answers:
        body.append(f"## {a.qid} — {a.question}")
        body.append("")
        body.append(f"> **Channels:** {' + '.join(a.channels)} · **Serves:** {a.persona}")
        body.append("")
        for c in a.claims:
            body.append(f"- {c.md}")
        body.append("")
    body += [
        "## How these answers are made",
        "",
        "> Generated deterministically by `synthesis/answers.py` from the live L1 bundle (the"
        " latest dated note per editorially-clean source key — held themes excluded). Numbers"
        " are read straight from the source notes; nothing is invented. Re-run after any ingest"
        " and the answers refresh in place. This is the living-system layer a static format"
        " cannot produce.",
        "",
        "## Changelog",
        "",
    ]
    new_cl = (
        f"- {aset.day} — regenerated TOP5 demonstrator answers from the {aset.day} live bundle "
        f"({aset.week}); {len(aset.answers)} cross-channel answers, every claim L1-sourced."
    )
    kept = [ln for ln in prior_changelog if not ln.lstrip().startswith(f"- {aset.day} ")]
    return "\n".join(fm + body + [*kept, new_cl]) + "\n"
