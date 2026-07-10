"""Guards the Cloudflare Pages deploy path (Azimuth KR3, the convince-me package).

The Cloudflare Pages workflow publishes the built ``_site/`` to a public
``azimuth.pages.dev`` URL from a still-private repo, so the demonstrator is
mobile-viewable before the separate public-flip decision. Two invariants matter and
are easy to break with a well-meaning edit, so they are pinned here:

  1. **Skip-not-fail.** The deploy must run only when BOTH Cloudflare secrets are set,
     via a preflight step output — never red-fail an unconfigured repo (the same design
     as ``pages.yml`` skipping while the repo is private). An edit that drops the gate
     would fail every push on a repo with no Cloudflare secrets.
  2. **Deploy target + headers.** It must deploy ``_site`` to the ``azimuth`` Pages
     project and copy ``cloudflare/_headers`` into the output root, or the site ships
     without its security headers / to the wrong project.

Pure stdlib (text assertions over the workflow + config files) to match the repo's
no-new-dependency scanners — no PyYAML.
"""

from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_WORKFLOW = _REPO_ROOT / ".github" / "workflows" / "deploy-cloudflare.yml"
_WRANGLER = _REPO_ROOT / "wrangler.toml"
_HEADERS = _REPO_ROOT / "cloudflare" / "_headers"
_DOCS_INDEX = _REPO_ROOT / "docs" / "README.md"
_RUNBOOK = _REPO_ROOT / "docs" / "deploy-cloudflare.md"


def test_all_deploy_files_exist() -> None:
    for path in (_WORKFLOW, _WRANGLER, _HEADERS, _RUNBOOK):
        assert path.is_file(), f"missing Cloudflare Pages deploy file: {path}"


def test_deploy_is_skip_not_fail_on_missing_secrets() -> None:
    """The deploy must gate on a preflight output, not run unconditionally.

    Without the gate, a repo with no Cloudflare secrets would red-fail on every push —
    the red-by-design regression this guards against.
    """
    text = _WORKFLOW.read_text(encoding="utf-8")
    assert "id: preflight" in text, "no preflight step to gate the deploy on"
    # The preflight must emit both configured states so the gate can go either way.
    assert "configured=true" in text and "configured=false" in text, (
        "preflight must set configured=true/false from the presence of the CF secrets"
    )
    # Both secrets participate in the gate (either missing -> skip).
    assert "CLOUDFLARE_API_TOKEN" in text, "CLOUDFLARE_API_TOKEN not referenced"
    assert "CLOUDFLARE_ACCOUNT_ID" in text, "CLOUDFLARE_ACCOUNT_ID not referenced"


def test_real_steps_are_all_gated_on_the_preflight() -> None:
    """Every step that does real work must carry the configured=='true' guard."""
    text = _WORKFLOW.read_text(encoding="utf-8")
    gate = "steps.preflight.outputs.configured == 'true'"
    assert gate in text, "the preflight gate expression is missing"
    # The deploy step in particular must never run ungated.
    deploy_idx = text.find("cloudflare/wrangler-action")
    assert deploy_idx != -1, "no cloudflare/wrangler-action deploy step"
    # The gate must appear before the deploy action within its step block.
    block_start = text.rfind("- name:", 0, deploy_idx)
    assert block_start != -1 and gate in text[block_start:deploy_idx], (
        "the wrangler deploy step is not gated on the preflight output"
    )


def test_deploy_targets_the_azimuth_pages_project() -> None:
    text = _WORKFLOW.read_text(encoding="utf-8")
    assert "pages deploy _site" in text, "deploy must publish the built _site directory"
    assert "--project-name=azimuth" in text, "deploy must target the 'azimuth' Pages project"


def test_site_is_built_and_headers_copied() -> None:
    text = _WORKFLOW.read_text(encoding="utf-8")
    assert "scripts/build_site.py --out _site" in text, "site build step missing / wrong out dir"
    assert "cp cloudflare/_headers _site/_headers" in text, (
        "the security _headers file must be copied into the Pages output root"
    )


def test_wrangler_config_names_the_project_and_output() -> None:
    text = _WRANGLER.read_text(encoding="utf-8")
    assert 'name = "azimuth"' in text, "wrangler.toml must name the project 'azimuth'"
    assert 'pages_build_output_dir = "_site"' in text, "wrangler.toml must point at _site"


def test_headers_file_sets_the_baseline_security_headers() -> None:
    text = _HEADERS.read_text(encoding="utf-8")
    assert "/*" in text, "the _headers rule must apply to all paths (/*)"
    for header in (
        "X-Content-Type-Options: nosniff",
        "X-Frame-Options: DENY",
        "Referrer-Policy:",
        "Permissions-Policy:",
    ):
        assert header in text, f"missing baseline security header: {header}"


def test_runbook_is_indexed_in_the_docs_index() -> None:
    """The runbook must be linked from docs/README.md (doc-orphan gate parity)."""
    index = _DOCS_INDEX.read_text(encoding="utf-8")
    assert "deploy-cloudflare.md" in index, (
        "docs/README.md must link the Cloudflare deploy runbook so it isn't an orphan"
    )
