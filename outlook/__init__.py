"""outlook — the glass-box baseline-forecast L2 layer ("Outlook").

Phase-1 of the prediction layer designed in ``docs/prediction-layer-design.md``.

Three pure-stdlib, deterministic units make up the P1 engine (data -> forecast -> PI ->
success metric), each independently testable:

- :mod:`outlook.series`   -- extract the Tier-A upstream series out of the committed L1 notes.
- :mod:`outlook.forecast` -- the classical baseline ensemble + bootstrap prediction interval,
  behind a hard-coded hazard interlock (earthquakes/hazards can never be forecast).
- :mod:`outlook.backtest` -- rolling-origin MASE / sMAPE / PI-coverage scorer + the ship-bar.

No LLM anywhere on the forecast path; the same committed L1 day yields a byte-identical
forecast and score. Nothing here publishes a public brief -- that is P4/P5 and is gated on
the daily-update guarantee (Azimuth KR1) holding.
"""

from __future__ import annotations

__all__ = ["backtest", "forecast", "series"]
