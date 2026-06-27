"""Regression guard for the KG acceptance smoke (scripts/smoke_graph.py).

``smoke_graph.py`` is the KR-B ``smoke/screenshot`` gate: it proves the knowledge
graph is both queryable (the ``query_graph.py`` engine answers over the committed
``site/graph.json``) and visually traceable (``graph.html`` in a real browser).
The browser half needs Chromium and is run by hand / pre-deploy; this test runs the
*queryable* half headless against the committed live graph so a future graph regen
that silently drops the cross-source bridges, the typed relations, or the flagship
``connect`` answer reddens CI instead of slipping through to Michael's spot-review.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "smoke_graph", _REPO_ROOT / "scripts" / "smoke_graph.py"
)
assert _spec and _spec.loader
smoke = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(smoke)


def test_kg_smoke_queryable_half_passes_on_committed_graph() -> None:
    """The committed graph stays answerable: stats, relations, a cross-source bridge."""
    failures: list[str] = []
    smoke._smoke_queryable(failures)
    assert failures == [], "KG smoke (queryable half) regressed: " + "; ".join(failures)
