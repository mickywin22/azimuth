#!/usr/bin/env python3
"""CI entry point for the azimuth per-source license guardrail.

Exits non-zero (failing the build) if any surfaced WorldMonitor subset breaches the
guardrail. Run locally with:

    python scripts/check_sources.py

See docs/source-guardrail.md for the rule.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running as a plain script (python scripts/check_sources.py) from repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.backend.guardrail import check_registry  # noqa: E402


def main() -> int:
    registry_path = _REPO_ROOT / "sources" / "registry.json"
    credits_path = _REPO_ROOT / "CREDITS.md"

    if not registry_path.exists():
        print(f"source-guardrail: FAIL — registry not found at {registry_path}")
        return 2

    result = check_registry(registry_path, credits_path)

    print(f"source-guardrail: checked {result.checked} source(s), {result.surfaced} surfaced.")
    if result.ok:
        print(
            "source-guardrail: PASS — every surfaced source is licensed, "
            "attributed, credited, and editorially allowed."
        )
        return 0

    print(f"source-guardrail: FAIL — {len(result.violations)} violation(s):")
    for violation in result.violations:
        print(f"  - {violation}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
