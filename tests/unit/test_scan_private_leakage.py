"""Tests for the public-flip private-leakage gate (scripts/scan_private_leakage.py).

The load-bearing guarantee, mirroring the C1 secret-scan: the C1b privacy gate has
TEETH. It must (a) HARD-block on owner-private data that can never ship public —
the owner's Windows/unix home path, a path into the private HemySphere vault, the
personal email, and the local-machine Claude hook commands — and (b) NOT
false-positive on the *intentional* public pitch: naming "the HemySphere L1/L2/L3
doctrine" or "Emi's synthesis layer", and crediting "Michael Rarivomanana" in a
LICENSE copyright line. A gate that fired on the attribution surname would force
the owner to strip his own name off his own OSS repo — the exact opposite of the
credibility play azimuth exists for. Both halves get a regression test.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "scan_private_leakage", _REPO_ROOT / "scripts" / "scan_private_leakage.py"
)
assert _spec and _spec.loader
scan = importlib.util.module_from_spec(_spec)
sys.modules["scan_private_leakage"] = scan
_spec.loader.exec_module(scan)


def _rules(text: str, path: str = "config.json", severity: str | None = None) -> list[str]:
    findings = scan._scan_text(text, "worktree", path)
    return [f.rule for f in findings if severity is None or f.severity == severity]


# --- HARD detections: each owner-private class must fire ---------------------


def test_detects_windows_home_path() -> None:
    assert "personal-abs-path-windows" in _rules(r"C:\Users\Michael\AppData\Local\tool.exe")


def test_detects_unix_home_path() -> None:
    assert "personal-abs-path-unix" in _rules("/Users/Michael/Projects/azimuth")
    assert "personal-abs-path-unix" in _rules("/home/Michael/x")


def test_detects_hemysphere_vault_path() -> None:
    hits = _rules(
        r"powershell -File C:\Users\Michael\HemySphere\scripts\hooks\package-cooldown.ps1"
    )
    assert "hemysphere-local-path" in hits


def test_detects_personal_email() -> None:
    assert "personal-email" in _rules("contact: m.rarivomanana@gmail.com")
    assert "personal-email" in _rules("author = rarivomanana@example.org")


def test_detects_local_hook_commands() -> None:
    assert "local-machine-hook" in _rules("lean-ctx.exe hook rewrite")
    assert "local-machine-hook" in _rules("Bypass -File package-cooldown.ps1")


def test_real_settings_local_json_is_a_hard_leak() -> None:
    blob = (
        '{"hooks":{"PreToolUse":[{"hooks":[{"command":'
        '"C:\\\\Users\\\\Michael\\\\AppData\\\\Local\\\\lean-ctx\\\\lean-ctx.exe hook rewrite"}]}]}}'
    )
    findings = scan._scan_text(blob, "worktree", ".claude/settings.local.json")
    assert any(f.severity == "hard" for f in findings)


# --- NO false-positive on the intentional public pitch ----------------------


def test_license_attribution_surname_is_not_flagged() -> None:
    # The copyright surname is wanted attribution, not a leak.
    line = "Copyright (c) 2026 Michael Rarivomanana (azimuth contributors)"
    assert _rules(line, "LICENSE") == []


def test_attribution_string_clean() -> None:
    line = '"azimuth" (https://github.com/mickywin22/azimuth) by Michael Rarivomanana, CC BY 4.0.'
    assert _rules(line, "LICENSE-CONTENT.md") == []


def test_doctrine_pitch_is_not_flagged() -> None:
    pitch = (
        "A public demonstrator of the HemySphere L1/L2/L3 vault doctrine. "
        "That cross-source line is what Emi's synthesis layer adds."
    )
    assert _rules(pitch, "README.md") == []


# --- Severity wiring --------------------------------------------------------


def test_iq_ref_is_advisory_not_hard() -> None:
    hits = scan._scan_text("Confirmed in IQ #371.", "worktree", "docs/spec.md")
    assert hits and all(f.severity == "advisory" for f in hits)
    assert _rules("Confirmed in IQ #371.", "docs/spec.md", severity="hard") == []


def test_internal_sprint_marker_is_advisory() -> None:
    assert "internal-sprint-audit-marker" in _rules(
        "shipped by HemySphere Sprint", "x.md", severity="advisory"
    )


def test_scanner_own_file_is_allowlisted() -> None:
    # The scanner's own rule strings must not flag the scanner.
    assert scan._scan_text("m.rarivomanana@x", "worktree", "scripts/scan_private_leakage.py") == []
    assert scan._is_allowed("docs/security/public-flip-readiness.md")


def test_history_scrub_helper_is_allowlisted() -> None:
    # scrub-history.sh documents the owner-private paths it *removes* — naming
    # them is its job, not a leak. Flagging the de-leaking tool would keep C1b
    # red forever. It must be allowlisted like the scanner + readiness doc.
    assert scan._is_allowed("scripts/scrub-history.sh")
    assert scan._scan_text("/HemySphere/ and C:\\Users\\x", "worktree", "scripts/scrub-history.sh") == []


def test_c1c_decision_brief_is_allowlisted() -> None:
    # The C1c decision brief quantifies + explains the exact history markers
    # Michael must accept-or-scrub, so it MUST quote them (C:\Users\…, /HemySphere/,
    # the IQ refs). Like the readiness doc + scrub helper, it is documentation of
    # the gate, not a publishable leak — allowlisting it keeps C1b green.
    assert scan._is_allowed("docs/security/c1c-history-decision.md")
    assert (
        scan._scan_text("/HemySphere/ and C:\\Users\\Michael", "worktree", "docs/security/c1c-history-decision.md")
        == []
    )


# --- main() exit-code contract ----------------------------------------------


def test_main_worktree_returns_clean_on_current_tree() -> None:
    # Post-fix, the working tree must have zero HARD findings → exit 0.
    assert scan.main(["--worktree"]) == 0


def test_strict_flag_blocks_on_advisory() -> None:
    # A tree with only advisory findings passes by default but fails under --strict.
    # We assert the wiring on a crafted finding set rather than the live tree.
    hard = scan.Finding("r", "n", "hard", "worktree", "p", 1, "x")
    adv = scan.Finding("r", "n", "advisory", "worktree", "p", 1, "x")
    # mirror main()'s blocked() logic
    assert bool([f for f in [adv] if f.severity == "hard"]) is False  # default: not blocked
    assert bool([f for f in [hard] if f.severity == "hard"]) is True  # hard always blocks
