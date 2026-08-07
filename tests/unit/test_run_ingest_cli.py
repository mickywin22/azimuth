"""Tests for the L1 ingest CLI wrapper (scripts/run_ingest.py).

Focus: the GitHub Actions step-output emission that lets the daily ``ingest.yml`` workflow
raise the ``ingest-alarm`` issue even on a *healthy* run that tolerated a minority of source
errors. Without it, ``run_ingest`` exits 0, the job succeeds, and the workflow's
``if: failure()`` alarm step is skipped — so the errored source is committed *around* and
vanishes silently. The emitter publishes the errored source keys as a step output the alarm
step keys off (``steps.ingest.outputs.errored``), closing that gap while the run still commits
the good notes.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

from ingest import IngestOutcome, L1Note

if TYPE_CHECKING:
    import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Load the CLI by file path (not `import scripts.run_ingest`) — mirrors how the other
# script CLIs are exercised (test_build_autonomy, test_check_ingest_liveness) and keeps
# mypy from seeing the module under two names.
_spec = importlib.util.spec_from_file_location(
    "run_ingest", _REPO_ROOT / "scripts" / "run_ingest.py"
)
assert _spec is not None and _spec.loader is not None
run_ingest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_ingest)


def _note(key: str) -> L1Note:
    return L1Note(source_key=key, relative_path=Path(f"2026-06-10/{key}.md"), text="body")


def test_emit_step_outputs_is_noop_without_github_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Off CI (no GITHUB_OUTPUT) the emitter must be a silent no-op — never crash a local run.
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    run_ingest._emit_step_outputs(IngestOutcome(errors={"a": "boom"}))


def test_emit_step_outputs_lists_errored_keys_sorted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A healthy-but-degraded run: 2 good notes committed, 2 sources errored. The emitter
    # must surface the errored keys (sorted, comma-joined) so the alarm step can name them.
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    outcome = IngestOutcome(
        written=[_note("a"), _note("b")],
        errors={"world-bank-indicators": "HTTP 400", "acled": "timeout"},
    )

    run_ingest._emit_step_outputs(outcome)

    lines = out.read_text(encoding="utf-8").splitlines()
    assert "errored=acled,world-bank-indicators" in lines  # sorted, comma-joined
    assert "errored_count=2" in lines
    assert "written_count=2" in lines


def test_emit_step_outputs_empty_value_when_clean(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A clean run emits an *empty* `errored` value, so `steps.ingest.outputs.errored != ''`
    # is false and the alarm stays quiet.
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))

    run_ingest._emit_step_outputs(IngestOutcome(written=[_note("a")]))

    lines = out.read_text(encoding="utf-8").splitlines()
    assert "errored=" in lines  # empty value -> alarm skipped
    assert "errored_count=0" in lines
    assert "written_count=1" in lines


def test_emit_step_outputs_appends_never_truncates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # GITHUB_OUTPUT is a shared append-only file the runner owns; the emitter must append,
    # never clobber a prior step's outputs.
    out = tmp_path / "gh_output"
    out.write_text("prior=kept\n", encoding="utf-8")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))

    run_ingest._emit_step_outputs(IngestOutcome(written=[_note("a")], errors={"x": "boom"}))

    text = out.read_text(encoding="utf-8")
    assert text.startswith("prior=kept\n")  # earlier content survives
    assert "errored=x" in text
