"""Guards the daily-ingest deterministic-regen contract in ``.github/workflows/ingest.yml``.

The daily L1 ingest (GitHub Actions) pulls a new source day and then re-derives every
committed deterministic artifact that rests on that day, in ONE step + ONE commit, so the
public site never ships an artifact that lags the L1 underneath it. The linked-data explorer
(``site/linked-data.*``) is one of those artifacts: it projects the RDF over the same L1/L2
notes, so a new ingest day moves its counts + latest-source concepts. If ``build_linked_data``
were dropped from the regen step (or moved BEFORE ``build_graph``, whose output it rests on),
the explorer would ship stale the day after every pull and redden ``build_linked_data.py
--check`` on main -- the exact 2026-09-28 stale-artifact class this file guards.

These tests pin that contract so a future well-meaning edit to the regen step cannot silently
drop the linked-data leg (or reorder it before the graph rebuild). Pure stdlib text assertions
over the workflow file, matching the repo's no-new-dependency workflow tests -- no PyYAML.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "ingest.yml"

_REGEN_STEP_MARKER = "Regenerate deterministic artifacts"
_COMMIT_STEP_MARKER = "Commit new L1 notes"


def _step_body(marker: str) -> str:
    """Return the text of the ingest step whose ``- name:`` contains ``marker``.

    Slices from the step's name line up to the next ``- name:`` (or end of file), so the
    returned body is exactly that one step's YAML (its ``run:`` block included).
    """
    text = _WORKFLOW.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next(
        (i for i, ln in enumerate(lines) if "- name:" in ln and marker in ln),
        None,
    )
    assert start is not None, f"ingest.yml has no step named like {marker!r}"
    end = next(
        (j for j in range(start + 1, len(lines)) if "- name:" in lines[j]),
        len(lines),
    )
    return "\n".join(lines[start:end])


def _regen_commands() -> list[str]:
    """Return the ordered ``python scripts/build_*.py`` commands in the regen step."""
    body = _step_body(_REGEN_STEP_MARKER)
    return [ln.strip() for ln in body.splitlines() if ln.strip().startswith("python scripts/")]


def test_regen_step_rebuilds_the_linked_data_explorer() -> None:
    """The daily regen step must run ``build_linked_data.py`` so the explorer never ships stale."""
    cmds = _regen_commands()
    assert cmds, "regen step runs no python scripts/build_*.py commands"
    assert any("build_linked_data.py" in c for c in cmds), (
        f"regen step must rebuild the linked-data explorer; got: {cmds!r}"
    )


def test_linked_data_rebuild_follows_the_graph_rebuild() -> None:
    """``build_linked_data`` rests on the graph, so it must run AFTER ``build_graph``.

    The work-item contract is 'run build_linked_data.py immediately after the graph rebuild
    so the linked-data explorer never ships stale'. Running it BEFORE build_graph would project
    over a stale graph -- guard the ordering, not just the presence.
    """
    cmds = _regen_commands()
    graph_at = next((i for i, c in enumerate(cmds) if "build_graph.py" in c), None)
    ld_at = next((i for i, c in enumerate(cmds) if "build_linked_data.py" in c), None)
    assert graph_at is not None, f"regen step must rebuild the graph; got: {cmds!r}"
    assert ld_at is not None, f"regen step must rebuild linked-data; got: {cmds!r}"
    assert ld_at > graph_at, (
        "build_linked_data must run AFTER build_graph (it rests on the graph); "
        f"got order: {cmds!r}"
    )


def test_commit_step_stages_the_linked_data_artifacts() -> None:
    """A rebuild that is not committed still ships stale -- the commit must stage the artifacts.

    Regenerating ``site/linked-data.*`` in the same job but omitting it from the ``git add``
    would leave the committed snapshot stale despite the rebuild -- the same 'never ships
    stale' failure, one step later.
    """
    body = _step_body(_COMMIT_STEP_MARKER)
    for artifact in ("site/linked-data.json", "site/linked-data.html"):
        assert artifact in body, (
            f"commit step must stage {artifact} so the rebuilt explorer is actually committed"
        )
