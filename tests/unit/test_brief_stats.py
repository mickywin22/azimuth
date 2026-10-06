"""Unit tests for the key-figure band's honest wildfire cap reporting.

Context: the NASA-FIRMS feed's ``totalCount`` swings cycle-to-cycle (a curator dispatch saw
it move 500 -> 6,657). Azimuth caps the L1 note to the top-N rows by FRP, so the derived
band must state that cap against the real pre-cap row count — otherwise the capped sample is
presented as if it were the whole feed and the truncation is silent. These tests pin that the
``environmental-hazards`` chip reads the note's honesty caption and surfaces "N of M".
"""

from __future__ import annotations

from pathlib import Path

from synthesis.brief_stats import _cap_total, _hazards


def _write_fire_note(day: Path, rows: list[dict[str, object]], *, cap_total: int | None) -> None:
    """Write a minimal ``wildfire-detections.md`` L1 note the band's parsers can read.

    ``cap_total`` None -> an uncapped note (no honesty caption); an int -> a capped note whose
    caption mirrors ``ingest/pull.py`` render_note exactly ("showing top N by `frp` of M rows").
    """
    day.mkdir(parents=True, exist_ok=True)
    import json

    caption = "> L1 source pull — `wildfire-detections`. Verbatim transform; never edit by hand."
    if cap_total is not None:
        caption += (
            f"\n> **Payload cap (azimuth-side, recorded for honesty):** showing top {len(rows)} "
            f"by `frp` of {cap_total} rows. The endpoint ignores limit params; full set at source."
        )
    body = "\n".join(
        [
            "---",
            "type: L1-source",
            "---",
            "",
            "# NASA FIRMS",
            "",
            caption,
            "",
            "| field | value |",
            "| --- | --- |",
            f"| fireDetections | {json.dumps(rows)} |",
            "",
        ]
    )
    (day / "wildfire-detections.md").write_text(body, encoding="utf-8")


def _fire_chip(items: list[dict[str, object]]) -> dict[str, object]:
    """The single wildfire-count chip from a hazards band (the first chip the extractor emits)."""
    return items[0]


def _cap_total_of(text: str, tmp_path: Path) -> int | None:
    """Run the real _cap_total against a note holding ``text`` (covers the on-disk read path)."""
    note = tmp_path / "note.md"
    note.write_text(text, encoding="utf-8")
    return _cap_total(note)


def test_cap_total_parses_top_by_frp_caption(tmp_path: Path) -> None:
    assert _cap_total_of("showing top 250 by `frp` of 500 rows", tmp_path) == 500
    assert _cap_total_of("showing first 10 of 6657 rows", tmp_path) == 6657
    assert _cap_total_of("no cap caption here", tmp_path) is None
    assert _cap_total(tmp_path / "absent.md") is None  # missing file -> None, never raises


def test_hazards_states_cap_against_total_when_capped(tmp_path: Path) -> None:
    rows = [{"frp": float(i), "region": "Russia"} for i in range(3)]
    _write_fire_note(tmp_path, rows, cap_total=500)
    chip = _fire_chip(_hazards(tmp_path))
    assert chip["value"] == "3"  # the shown (capped) row count
    assert chip["caption"] == "top 3 of 500 fire detections (by FRP)"  # truncation non-silent


def test_hazards_states_big_total_with_thousands_separator(tmp_path: Path) -> None:
    rows = [{"frp": float(i), "region": "Ukraine"} for i in range(250)]
    _write_fire_note(tmp_path, rows, cap_total=6657)
    chip = _fire_chip(_hazards(tmp_path))
    assert chip["caption"] == "top 250 of 6,657 fire detections (by FRP)"


def test_hazards_uncapped_note_keeps_plain_label(tmp_path: Path) -> None:
    rows = [{"frp": 1.0, "region": "Russia"}, {"frp": 2.0, "region": "Iran"}]
    _write_fire_note(tmp_path, rows, cap_total=None)
    chip = _fire_chip(_hazards(tmp_path))
    assert chip["value"] == "2"
    assert chip["caption"] == "top fire detections by FRP"  # no cap -> no misleading "of M"


def test_hazards_total_not_greater_than_shown_keeps_plain_label(tmp_path: Path) -> None:
    # A stale/degenerate caption whose total <= shown must not produce "top 2 of 2" noise.
    rows = [{"frp": 1.0, "region": "Russia"}, {"frp": 2.0, "region": "Iran"}]
    _write_fire_note(tmp_path, rows, cap_total=2)
    chip = _fire_chip(_hazards(tmp_path))
    assert chip["caption"] == "top fire detections by FRP"
