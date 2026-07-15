"""vault_contract — the reusable contract engine (green fixture + one planted breach per clause)."""

from __future__ import annotations

from pathlib import Path

from vault_contract import (
    RuleSet,
    check_changelog,
    check_claim_sourcing,
    check_denylist,
    check_diff_guard,
    check_frontmatter,
    check_tool_artifacts,
    lint_note,
    lint_tree,
    split_frontmatter,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

CLEAN = """---
title: Energy Supply Weekly
type: L2-brief
license: CC-BY-4.0
updated: 2026-07-15T14:00:00Z
---

# Energy Supply Weekly

## Storage

- US crude inventories drew 3.2M barrels ([[crude-oil-inventories]]).
- EU gas storage built to 2,983 Bcf ([[natural-gas-storage-eu]]).

## Changelog

- 2026-07-15 — refreshed from the live ingest.
"""

RULES = RuleSet(
    frontmatter_required=["title", "type", "license", "updated"],
    claim_link_pattern=r"\[\[[^\]]+\]\]",
    changelog_required=True,
    denylist=[r"(?i)\byou should (buy|sell)\b"],
    artifact_markers=["</content>", "</invoke>"],
    diff_allowed_prefixes=["vault/02 Briefs/"],
    diff_forbidden_prefixes=["vault/01 Sources/"],
)


def test_clean_note_passes() -> None:
    assert lint_note(CLEAN, RULES) == []


def test_frontmatter_missing_key() -> None:
    fm, _ = split_frontmatter(CLEAN.replace("license: CC-BY-4.0\n", ""))
    assert check_frontmatter(fm, ["license"]) == ["frontmatter missing required key: 'license'"]


def test_unsourced_claim_fails() -> None:
    breached = CLEAN.replace(" ([[crude-oil-inventories]])", "")
    v = check_claim_sourcing(split_frontmatter(breached)[1], RULES.claim_link_pattern)
    assert any("unsourced claim" in x for x in v)


def test_changelog_bullets_are_exempt_from_sourcing() -> None:
    # the dated changelog line carries no wikilink and must not count as a claim
    v = check_claim_sourcing(split_frontmatter(CLEAN)[1], RULES.claim_link_pattern)
    assert v == []


def test_changelog_required_and_dated() -> None:
    assert check_changelog("# x\n", True) == ["missing '## Changelog' section"]
    assert check_changelog("## Changelog\n\nno dates here\n", True)
    assert check_changelog(split_frontmatter(CLEAN)[1], True) == []


def test_denylist_blocks_investment_framing() -> None:
    v = check_denylist("you should buy crude now", RULES.denylist)
    assert v and "denylist hit" in v[0]


def test_tool_artifacts_blocked() -> None:
    v = check_tool_artifacts("fine text\n</content>\n</invoke>", RULES.artifact_markers)
    assert len(v) == 2


def test_diff_guard_allowed_and_forbidden() -> None:
    v = check_diff_guard(
        ["vault/01 Sources/2026-07-15/x.md", "ingest/pull.py", "vault/02 Briefs/ok.md"],
        RULES.diff_allowed_prefixes,
        RULES.diff_forbidden_prefixes,
    )
    assert any("forbidden" in x for x in v)
    assert any("outside the allowed" in x for x in v)
    assert not any("ok.md" in x for x in v)


def test_rules_from_toml_roundtrip(tmp_path: Path) -> None:
    rules = RuleSet.from_toml(REPO_ROOT / "rules" / "azimuth.toml")
    assert "title" in rules.frontmatter_required
    assert rules.changelog_required is True
    assert rules.diff_forbidden_prefixes == ["vault/01 Sources/"]


def test_lint_tree_on_fixture(tmp_path: Path) -> None:
    (tmp_path / "good.md").write_text(CLEAN, encoding="utf-8")
    (tmp_path / "bad.md").write_text(CLEAN + "\n</invoke>\n", encoding="utf-8")
    results = lint_tree(tmp_path, RULES)
    assert "bad.md" in results and "good.md" not in results


def test_dogfood_live_azimuth_briefs_pass() -> None:
    """The generic engine must hold on the real corpus (the CI dogfood in unit form)."""
    rules = RuleSet.from_toml(REPO_ROOT / "rules" / "azimuth.toml")
    results = lint_tree(
        REPO_ROOT / "vault" / "02 Briefs", rules, REPO_ROOT / "vault" / "01 Sources"
    )
    assert results == {}, f"live briefs violate the declared contract: {results}"
