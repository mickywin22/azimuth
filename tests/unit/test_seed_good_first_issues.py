"""Tests for the good-first-issues seeder (scripts/seed_good_first_issues.py).

The load-bearing guarantees:
* the catalog is **generated**, so ``.github/GOOD_FIRST_ISSUES.md`` must stay byte-identical
  to ``render_markdown()`` — ``--check`` is the CI guard and this pins it;
* rendering is deterministic (no wall clock, no ordering wobble);
* the issue set stays well-formed — unique slugs/titles, every issue carries the
  ``good first issue`` label, and every label is one the seeder knows how to create.

The ``--create`` path shells out to ``gh`` and is intentionally NOT exercised here (no
network, no GitHub state in unit tests).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "seed_good_first_issues", _REPO_ROOT / "scripts" / "seed_good_first_issues.py"
)
assert _spec and _spec.loader
sgfi = importlib.util.module_from_spec(_spec)
# Register before exec: the module defines a @dataclass, and dataclass processing looks
# the module up in sys.modules (KW_ONLY sentinel resolution) — a file-path load that skips
# this raises AttributeError on 3.14.
sys.modules[_spec.name] = sgfi
_spec.loader.exec_module(sgfi)


def test_at_least_three_issues() -> None:
    # C3 asks for 3-5 seeded good-first-issues.
    assert 3 <= len(sgfi.ISSUES) <= 8


def test_slugs_and_titles_unique() -> None:
    slugs = [i.slug for i in sgfi.ISSUES]
    titles = [i.title for i in sgfi.ISSUES]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    assert len(titles) == len(set(titles)), "duplicate title"


def test_every_issue_is_a_good_first_issue() -> None:
    for issue in sgfi.ISSUES:
        assert sgfi._GOOD_FIRST in issue.labels, f"{issue.slug} missing good-first label"


def test_all_labels_are_creatable() -> None:
    # Every label used must have color/description metadata so --create can make it.
    for issue in sgfi.ISSUES:
        for label in issue.labels:
            assert label in sgfi._LABEL_META, f"label {label!r} has no metadata"


def test_required_fields_non_empty() -> None:
    for issue in sgfi.ISSUES:
        assert issue.title and issue.summary and issue.why
        assert issue.steps and issue.files and issue.acceptance and issue.verify
        assert issue.difficulty in {"Beginner", "Intermediate", "Advanced"}


def test_render_is_deterministic() -> None:
    assert sgfi.render_markdown() == sgfi.render_markdown()


def test_issue_body_contains_key_sections() -> None:
    body = sgfi._issue_body(sgfi.ISSUES[0])
    assert "Difficulty:" in body
    assert "What to do" in body
    assert "Done when" in body
    assert "```bash" in body


def test_committed_catalog_is_in_sync() -> None:
    # This is exactly what CI's `--check` step asserts; keep it green by running
    # `python scripts/seed_good_first_issues.py --write` after editing ISSUES.
    committed = sgfi._OUT.read_text(encoding="utf-8")
    assert committed == sgfi.render_markdown(), (
        ".github/GOOD_FIRST_ISSUES.md is stale — run seed_good_first_issues.py --write"
    )


def test_check_mode_returns_zero_when_in_sync() -> None:
    assert sgfi.main(["--check"]) == 0
