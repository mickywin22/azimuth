"""Unit tests for the deterministic wildfire country tally (IQ #1161).

The contract under test: exact per-country attribution comes from the feed's own
``region`` field — ranked count-desc/name-asc, honest about rows it cannot attribute,
and never guessing a country from coordinates.
"""

from __future__ import annotations

from synthesis.fire_geo import FireGeo, country_tally


def _det(region: object, frp: float = 1.0) -> dict[str, object]:
    """A minimal fireDetections-shaped row with a region field."""
    return {"frp": frp, "location": {"latitude": 60.0, "longitude": 90.0}, "region": region}


def test_tally_ranks_count_desc_then_name_asc() -> None:
    fires = [_det("Russia"), _det("Iran"), _det("Russia"), _det("Ukraine"), _det("Iran")]
    geo = country_tally(fires)
    # Russia 2, Iran 2, Ukraine 1 -> count desc, ties broken by name asc (Iran before Russia)
    assert geo.counts == (("Iran", 2), ("Russia", 2), ("Ukraine", 1))
    assert geo.total == 5
    assert geo.attributed == 5
    assert geo.unattributed == 0


def test_dominant_is_the_top_country() -> None:
    fires = [_det("Russia")] * 243 + [_det("Iran")] * 5 + [_det("Ukraine")] * 2
    geo = country_tally(fires)
    assert geo.dominant == ("Russia", 243)
    assert geo.total == 250
    assert geo.attributed == 250


def test_missing_region_is_unattributed_never_guessed() -> None:
    fires = [_det("Russia"), _det(None), _det(""), _det("   "), {"frp": 5.0}]
    geo = country_tally(fires)
    # Only the one real "Russia" row attributes; blanks/None/absent -> unattributed, no guessing.
    assert geo.counts == (("Russia", 1),)
    assert geo.total == 5
    assert geo.attributed == 1
    assert geo.unattributed == 4


def test_region_is_trimmed() -> None:
    geo = country_tally([_det("  Russia  "), _det("Russia")])
    assert geo.counts == (("Russia", 2),)


def test_non_dict_and_non_list_payloads_degrade_to_empty() -> None:
    assert country_tally("not a list") == FireGeo(counts=(), total=0, attributed=0, unattributed=0)
    assert country_tally(None) == FireGeo(counts=(), total=0, attributed=0, unattributed=0)
    mixed = country_tally([_det("Russia"), "junk", 42, None])
    assert mixed.counts == (("Russia", 1),)
    assert mixed.total == 1  # non-dict rows are dropped before tallying


def test_empty_payload() -> None:
    geo = country_tally([])
    assert geo.dominant is None
    assert geo.summary() == "no active-fire detections"


def test_summary_formats_top_and_remainder() -> None:
    fires = [_det("Russia")] * 243 + [_det("Iran")] * 5 + [_det("Ukraine")] * 2
    assert country_tally(fires).summary() == "Russia 243 / Iran 5 / Ukraine 2"


def test_summary_flags_more_countries_and_unattributed() -> None:
    fires = (
        [_det("Russia")] * 10
        + [_det("Iran")] * 4
        + [_det("Ukraine")] * 3
        + [_det("Turkey")] * 2
        + [_det(None)] * 6
    )
    summary = country_tally(fires).summary(top=2)
    assert summary == "Russia 10 / Iran 4 (+2 more countries) (+6 unattributed)"


def test_summary_singular_more_country() -> None:
    fires = [_det("Russia")] * 3 + [_det("Iran")] * 2
    assert country_tally(fires).summary(top=1) == "Russia 3 (+1 more country)"


def test_all_unattributed_summary() -> None:
    geo = country_tally([_det(None), _det(None)])
    assert geo.dominant is None
    assert geo.summary() == "no country attribution (2 detections carry no region field)"
