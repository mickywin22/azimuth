# Demonstrator "what-if" proof (Azimuth KR-B, IQ #887)

The `answers.html` demonstrator carries an interactive **"show your work / what if the data
were different?"** panel on the cross-channel verdicts (Q1 supply-health, Q2 supply-vs-demand).

The verdict is a **pure function of the live L1 bundle** (`synthesis/answers.py`). At build
time we feed that same function the **sign-flipped input** and bake the recomputed
counterfactual next to the real one. A pure client-side toggle swaps which is shown — no
verdict logic runs in the browser. Flip the input, the truth-table branch changes, and the
verdict changes with it: proof the answer is **computed, not canned**.

These two screenshots are the banked visual proof (Q1 panel), regenerated any time by
`python scripts/smoke_whatif.py`:

| State | File | Verdict shown |
|-------|------|---------------|
| Real data | `whatif-real.png` | gas storage **building** → *leans well-supplied* |
| Flipped input | `whatif-flipped.png` | gas storage **drawing down** → *leans fragile* |

Acceptance gates (all green): unit test (counterfactual differs for ≥2 Qs,
`tests/unit/test_answers.py`) · `ruff` + `mypy` clean · live Playwright smoke
(`scripts/smoke_whatif.py`) · screenshots above.

---

# Knowledge-graph proof (Azimuth KR-B — smoke/screenshot gate)

KR-B asks for a **queryable OR visually rendered** knowledge graph over the briefs +
L1 sources, with ≥1 cross-source relation demonstrated, plus a `smoke/screenshot`. The
KG layer delivers **both** halves, and `scripts/smoke_graph.py` proves them end-to-end
against the committed `site/graph.json` (live `2026-06-27` ingest: **48 nodes / 92 edges**,
typed relations `has-brief · rests-on · mentioned-in · reported-in · located-in · named-in`).

**Queryable half** — `query_graph.py` answers over the live graph. The flagship cross-source
query is evidence-ranked, the answer a static OKF bundle cannot give:

```
connect energy-supply geophysical
  -> 3 shared bridge(s), strongest Greece (1+1 src) — Greece, Mexico, New Zealand
  -> Path: Energy Supply Weekly -> Greece -> Geophysical Weekly
```

**Visual half** — `graph.html` renders the cross-channel canvas; the in-browser **Trace**
control reproduces that same answer client-side and highlights the bridges + path:

| State | File | What it shows |
|-------|------|---------------|
| Default | `graph-default.png` | the full cross-channel graph (channels · briefs · L1 sources · bridge regions) |
| Traced | `graph-traced.png` | `energy-supply ↔ geophysical` traced — 3 bridges (Greece/Mexico/New Zealand) + path highlighted, rest dimmed |

Regenerate any time with `python scripts/smoke_graph.py` (exit 0 = pass; screenshots land in
`_smoke/`, the banked copies above live here).

Acceptance gates (all green): headless regression test on the committed graph
(`tests/unit/test_smoke_graph.py`) · the full `query_graph` suite
(`tests/unit/test_query_graph.py`) · `ruff` + `mypy --strict` clean · live Chromium smoke
(`scripts/smoke_graph.py`) · screenshots above.
