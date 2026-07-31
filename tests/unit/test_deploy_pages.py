"""Guards the GitHub Pages deploy path (Azimuth KR1, the guaranteed-daily-update package).

``pages.yml`` publishes the built ``_site/`` to GitHub Pages on every push to ``main``.
It must never red-fail a repo where Pages is not yet enabled — otherwise it floods every
push (and every daily-ingest commit) with a red X. Two invariants matter and are easy to
break with a well-meaning edit, so they are pinned here:

  1. **Skip-not-fail via a Pages-*enablement* probe.** The deploy must run only when GitHub
     Pages is actually enabled, decided by probing the Pages REST API in a ``preflight`` job
     whose ``enabled`` output the build + deploy jobs gate on. ``actions/deploy-pages`` 404s
     ("Ensure GitHub Pages has been enabled") when Pages is off, so gating on enablement is
     what keeps an un-provisioned repo GREEN doing nothing.
  2. **No stale visibility gate.** The old gate keyed on repository *visibility*
     (``!github.event.repository.private``). That went stale the instant the repo flipped
     public: build+deploy then ran and 404'd because Pages was still not enabled. The real
     blocker is enablement, not visibility — the visibility gate must be gone.

Pure stdlib (text assertions over the workflow file) to match the repo's no-new-dependency
scanners — no PyYAML. Mirrors ``test_deploy_cloudflare.py``.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "pages.yml"


def test_pages_workflow_exists() -> None:
    assert _WORKFLOW.is_file(), f"missing GitHub Pages deploy workflow: {_WORKFLOW}"


def test_deploy_is_skip_not_fail_via_an_enablement_preflight() -> None:
    """A preflight job must probe Pages enablement and emit an ``enabled`` verdict."""
    text = _WORKFLOW.read_text(encoding="utf-8")
    assert "preflight:" in text, "no preflight job to gate the deploy on"
    # The probe must hit the Pages REST API for this repo.
    assert "/pages" in text and "api.github.com/repos/" in text, (
        "preflight must probe the GitHub Pages REST API (…/repos/<repo>/pages)"
    )
    # It must emit both enabled states so the gate can go either way.
    assert "enabled=true" in text and "enabled=false" in text, (
        "preflight must set enabled=true/false from the Pages-enabled probe"
    )


def test_build_and_deploy_jobs_gate_on_the_enablement_output() -> None:
    """Both the build and deploy jobs must gate on the preflight ``enabled`` output."""
    text = _WORKFLOW.read_text(encoding="utf-8")
    gate = "needs.preflight.outputs.enabled == 'true'"
    # Appears at least twice: once for build, once for deploy.
    assert text.count(gate) >= 2, (
        "the build AND deploy jobs must each gate on needs.preflight.outputs.enabled == 'true'"
    )


def test_no_stale_repository_visibility_gate() -> None:
    """The stale ``!repository.private`` gate must be gone as an active gate.

    Checks ``if:`` gate lines only — a comment documenting the retired gate (why it was
    removed) is allowed and useful; an active ``if:`` keyed on visibility is the bug.
    """
    gate_lines = [
        line
        for line in _WORKFLOW.read_text(encoding="utf-8").splitlines()
        if line.lstrip().startswith("if:")
    ]
    offenders = [line for line in gate_lines if "repository.private" in line]
    assert not offenders, (
        "pages.yml must not gate on repository visibility — the repo is public but Pages may "
        f"still be disabled, so a visibility gate red-floods every push (KR1). Found: {offenders}"
    )


def test_deploy_still_publishes_the_site_via_deploy_pages() -> None:
    """The deploy must still build ``_site`` and publish it through actions/deploy-pages."""
    text = _WORKFLOW.read_text(encoding="utf-8")
    assert "scripts/build_site.py --out _site" in text, "site build step missing / wrong out dir"
    assert "actions/upload-pages-artifact" in text, "must upload the _site Pages artifact"
    assert "actions/deploy-pages" in text, "must publish via actions/deploy-pages"
