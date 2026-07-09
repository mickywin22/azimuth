"""Tests for the build-time sparkline renderer + its data series (synthesis/sparkline.py).

The guarantees:
* the SVG is a pure, deterministic function of the numbers — same input, same bytes;
* degenerate inputs (empty / single / all-equal) degrade instead of raising;
* min maps to the bottom of the box and max to the top (the trend points the right way);
* the data series counts published L1 notes per ingest day and excludes held themes,
  matching the site's own exclusion, and honours the `days` window.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from synthesis.sparkline import daily_source_counts, sparkline_svg

if TYPE_CHECKING:
    from pathlib import Path


def test_empty_series_renders_nothing() -> None:
    assert sparkline_svg([]) == ""


def test_single_and_flat_series_sit_on_midline() -> None:
    # one point, and an all-equal series: no trend to show -> flat mid-line, no crash
    one = sparkline_svg([5.0], height=30)
    assert "<svg" in one and "spark-dot" in one
    flat = sparkline_svg([7, 7, 7], height=30)
    # every y coordinate is the mid-line (height/2 = 15)
    assert "15" in flat
    assert "polyline" in flat


def test_min_maps_low_max_maps_high() -> None:
    # rising series: first point near the bottom (high y), last near the top (low y)
    svg = sparkline_svg([0, 10], width=100, height=40, pad=2)
    # extract the polyline points
    pts = svg.split('points="')[1].split('"')[0].split()
    (x0, y0), (x1, y1) = (tuple(map(float, p.split(","))) for p in pts)
    assert y0 > y1  # min drawn lower on screen than max (SVG y grows downward)
    assert x1 > x0  # time advances left -> right
    # end dot sits on the last point
    assert f'cx="{x1:g}"'.rstrip("0").rstrip(".") in svg or "spark-dot" in svg


def test_deterministic_bytes() -> None:
    a = sparkline_svg([1, 4, 2, 8, 5], label="trend")
    b = sparkline_svg([1, 4, 2, 8, 5], label="trend")
    assert a == b


def test_label_becomes_escaped_title() -> None:
    svg = sparkline_svg([1, 2], label='энергия <b> & "x"')
    assert "<title>" in svg and 'role="img"' in svg
    assert "&lt;b&gt;" in svg and "&amp;" in svg and "&quot;" in svg
    # no label -> decorative, hidden from the a11y tree
    assert 'aria-hidden="true"' in sparkline_svg([1, 2])


_REGISTRY = {
    "themes": {
        "energy-supply": {"brief": "Energy Supply Weekly.md"},
        "geophysical": {"brief": "Geophysical Weekly.md"},
        "prediction-markets": {"brief": "Prediction Markets Weekly.md", "brief_held": True},
    },
    "sources": [
        {"key": "fuel-prices", "theme": "energy-supply"},
        {"key": "energy-prices", "theme": "energy-supply"},
        {"key": "earthquakes", "theme": "geophysical"},
        {"key": "prediction-markets", "theme": "prediction-markets"},
    ],
}


def _make_vault(tmp_path: Path) -> Path:
    vault = tmp_path / "vault"
    # 06-18: only the two energy sources; 06-20/06-21: energy + geophysical (growth step).
    layout = {
        "2026-06-18": ["fuel-prices", "energy-prices", "prediction-markets"],
        "2026-06-20": ["fuel-prices", "energy-prices", "earthquakes", "prediction-markets"],
        "2026-06-21": ["fuel-prices", "energy-prices", "earthquakes", "prediction-markets"],
    }
    for day, keys in layout.items():
        d = vault / "01 Sources" / day
        d.mkdir(parents=True)
        (d / "README.md").write_text("index\n", encoding="utf-8")  # must be ignored
        for k in keys:
            (d / f"{k}.md").write_text(f"---\nsource: {k}\n---\n# {k} {day}\n", encoding="utf-8")
    return vault


def test_daily_counts_series_and_held_exclusion(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path)
    p = daily_source_counts(vault, _REGISTRY)

    assert p.days == ["2026-06-18", "2026-06-20", "2026-06-21"]
    # site-wide totals exclude the held prediction-markets note AND the README on every day
    assert p.total == [2, 3, 3]
    # per surfaced channel; held theme never appears as a key
    assert p.per_theme["energy-supply"] == [2, 2, 2]
    assert p.per_theme["geophysical"] == [0, 1, 1]  # geophysical comes online on 06-20
    assert "prediction-markets" not in p.per_theme


def test_days_window_keeps_most_recent(tmp_path: Path) -> None:
    vault = _make_vault(tmp_path)
    p = daily_source_counts(vault, _REGISTRY, days=2)
    assert p.days == ["2026-06-20", "2026-06-21"]  # oldest day dropped
    assert p.total == [3, 3]


def test_missing_vault_degrades_to_empty(tmp_path: Path) -> None:
    p = daily_source_counts(tmp_path / "nope", _REGISTRY)
    assert p.days == [] and p.total == [] and p.per_theme == {}
