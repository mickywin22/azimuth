"""Unit tests for the blocking L2 synthesis lint (``synthesis/lint.py``, spec.md F2).

Each blocking clause is proven two ways: green on a clean brief, red on a planted breach.
The clean fixture is the same shape the ``azimuth-curator`` evolves; the breach fixtures
mutate exactly one clause so a failure pins the clause that broke.
"""

from __future__ import annotations

from pathlib import Path

from synthesis.lint import (
    check_claim_sourcing,
    check_diff_guard,
    check_editorial_denylist,
    check_evolve_not_duplicate,
    check_frontmatter_schema,
    check_l1_links_exist,
    find_wikilinks,
    lint_brief,
    split_frontmatter,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CLEAN_BRIEF = """---
title: Energy Supply Weekly
type: L2-brief
theme: energy-supply
week: 2026-W25
updated: 2026-06-15T06:00:00Z
sources: [natural-gas-storage-eu, crude-oil-inventories]
license: CC-BY-4.0
attribution: azimuth (HemySphere doctrine demonstrator)
---

# Energy Supply Weekly

## Storage

- EU gas storage rose to 62%, up 3 points week-on-week ([[natural-gas-storage-eu]]).

## Inventories

US crude inventories drew down 1.2M barrels this week ([[crude-oil-inventories]]).

## Changelog

- 2026-06-15 — first synthesis cycle from live L1.
"""


def _write_sources(tmp_path: Path, *keys: str) -> Path:
    root = tmp_path / "01 Sources" / "2026-06-15"
    root.mkdir(parents=True)
    for key in keys:
        (root / f"{key}.md").write_text(f"# {key}\n", encoding="utf-8")
    return tmp_path / "01 Sources"


# --- frontmatter split + wikilink extraction -----------------------------------------
def test_split_frontmatter_parses_flat_block() -> None:
    fm, body = split_frontmatter(CLEAN_BRIEF)
    assert fm is not None
    assert fm["type"] == "L2-brief"
    assert fm["license"] == "CC-BY-4.0"
    assert "# Energy Supply Weekly" in body
    assert "title:" not in body  # frontmatter stripped from body


def test_find_wikilinks_strips_alias_and_anchor() -> None:
    assert find_wikilinks("see [[crude-oil-inventories|crude]] and [[x#h]]") == [
        "crude-oil-inventories",
        "x",
    ]


# --- clean brief is green on every clause --------------------------------------------
def test_clean_brief_passes_all(tmp_path: Path) -> None:
    sources = _write_sources(tmp_path, "natural-gas-storage-eu", "crude-oil-inventories")
    assert lint_brief(CLEAN_BRIEF, changed_paths=None, sources_root=sources) == []


# --- 1. claim sourcing ---------------------------------------------------------------
def test_unsourced_claim_paragraph_fails() -> None:
    body = "## Prices\n\nFuel prices climbed sharply this week across the bloc.\n"
    violations = check_claim_sourcing(body)
    assert any("unsourced claim" in v for v in violations)


def test_unsourced_bullet_fails() -> None:
    body = "## Prices\n\n- Diesel jumped 4% with no link to back it.\n"
    assert check_claim_sourcing(body)


def test_wrapped_bullet_link_on_continuation_line_passes() -> None:
    # The [[link]] sits on the bullet's soft-wrapped continuation line, not line 1.
    body = (
        "## Storage\n\n"
        "- EU gas storage rose to 62%, comfortably ahead of the seasonal refill pace\n"
        "  this week ([[natural-gas-storage-eu]]).\n"
    )
    assert check_claim_sourcing(body) == []


def test_one_unsourced_bullet_among_sourced_still_fails() -> None:
    body = (
        "## Prices\n\n"
        "- Diesel held flat ([[fuel-prices]]).\n"
        "- Power jumped with no source to back it.\n"
    )
    violations = check_claim_sourcing(body)
    assert len(violations) == 1
    assert "no source" in violations[0]


def test_changelog_and_tables_are_not_claims() -> None:
    body = (
        "## Data\n\n| field | value |\n| --- | --- |\n| level | 62 |\n\n"
        "## Changelog\n\n- 2026-06-15 — created (no link needed here).\n"
    )
    assert check_claim_sourcing(body) == []


# --- 2. L1 links exist ---------------------------------------------------------------
def test_link_to_missing_l1_note_fails(tmp_path: Path) -> None:
    sources = _write_sources(tmp_path, "natural-gas-storage-eu")  # crude-oil missing
    violations = check_l1_links_exist(CLEAN_BRIEF, sources)
    assert any("crude-oil-inventories" in v for v in violations)


def test_links_check_skipped_without_root() -> None:
    assert check_l1_links_exist(CLEAN_BRIEF, None) == []


# --- 3. frontmatter schema -----------------------------------------------------------
def test_missing_required_key_fails() -> None:
    fm, _ = split_frontmatter(CLEAN_BRIEF.replace("theme: energy-supply\n", ""))
    assert any("theme" in v for v in check_frontmatter_schema(fm))


def test_wrong_license_fails() -> None:
    fm, _ = split_frontmatter(CLEAN_BRIEF.replace("CC-BY-4.0", "MIT"))
    assert any("license" in v for v in check_frontmatter_schema(fm))


def test_bad_week_format_fails() -> None:
    fm, _ = split_frontmatter(CLEAN_BRIEF.replace("week: 2026-W25", "week: 2026-25"))
    assert any("week" in v for v in check_frontmatter_schema(fm))


def test_no_frontmatter_fails() -> None:
    assert check_frontmatter_schema(None)


# --- 4. evolve, not duplicate --------------------------------------------------------
def test_missing_changelog_fails() -> None:
    _, body = split_frontmatter(CLEAN_BRIEF)
    no_changelog = body.split("## Changelog")[0]
    assert check_evolve_not_duplicate(no_changelog)


def test_changelog_without_date_fails() -> None:
    body = "# X\n\nclaim ([[a]]).\n\n## Changelog\n\n- created the brief.\n"
    assert check_evolve_not_duplicate(body)


def test_dated_changelog_passes() -> None:
    _, body = split_frontmatter(CLEAN_BRIEF)
    assert check_evolve_not_duplicate(body) == []


# --- 5. editorial deny-list ----------------------------------------------------------
def test_investment_advice_fails() -> None:
    assert check_editorial_denylist("Traders should buy crude now ([[crude-oil-inventories]]).")


def test_safety_prediction_fails() -> None:
    assert check_editorial_denylist(
        "An imminent disaster looms over the region ([[earthquakes]])."
    )


def test_political_opinion_fails() -> None:
    assert check_editorial_denylist("The corrupt regime is to blame for the shortfall ([[x]]).")


def test_neutral_reporting_passes() -> None:
    assert (
        check_editorial_denylist("EU gas storage rose to 62% ([[natural-gas-storage-eu]]).") == []
    )


# --- 6. diff guard -------------------------------------------------------------------
def test_diff_guard_blocks_l1_edit() -> None:
    paths = ["vault/01 Sources/2026-06-15/crude-oil-inventories.md"]
    assert any("L1 source" in v for v in check_diff_guard(paths))


def test_diff_guard_blocks_outside_briefs() -> None:
    assert any("outside" in v for v in check_diff_guard(["ingest/pull.py"]))


def test_diff_guard_allows_briefs_only() -> None:
    assert check_diff_guard(["vault/02 Briefs/Energy Supply Weekly.md"]) == []


def test_diff_guard_skipped_when_none() -> None:
    assert check_diff_guard(None) == []


# --- end-to-end planted breaches via lint_brief --------------------------------------
def test_lint_brief_catches_editorial_breach(tmp_path: Path) -> None:
    sources = _write_sources(tmp_path, "natural-gas-storage-eu", "crude-oil-inventories")
    breached = CLEAN_BRIEF.replace(
        "US crude inventories drew down 1.2M barrels this week ([[crude-oil-inventories]]).",
        "Traders should buy crude now, it will rise to $95 ([[crude-oil-inventories]]).",
    )
    violations = lint_brief(breached, changed_paths=None, sources_root=sources)
    assert any("editorial deny-list" in v for v in violations)


def test_lint_brief_catches_l1_mutation_in_commit(tmp_path: Path) -> None:
    sources = _write_sources(tmp_path, "natural-gas-storage-eu", "crude-oil-inventories")
    paths = [
        "vault/02 Briefs/Energy Supply Weekly.md",
        "vault/01 Sources/2026-06-15/crude-oil-inventories.md",
    ]
    violations = lint_brief(CLEAN_BRIEF, changed_paths=paths, sources_root=sources)
    assert any("L1 source" in v for v in violations)
