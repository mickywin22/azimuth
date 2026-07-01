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

# Knowledge-graph visualization proof (Azimuth KR-B)

`graph.html` is the state-of-the-art cross-channel knowledge-graph view — a canvas
force layout with hi-DPI rendering, pan/zoom, hover spotlight + typed-relation
tooltips, evidence-weighted edge thickness, shareable deep links, and a **Trace**
control that answers *"how do two channels connect?"* directly over the rendered
graph. `scripts/smoke_graph.py` opens it in a **real Chromium** and proves all of it
end-to-end (the browser-render gate the token-presence unit tests can't reach):

| Proof | File | What it shows |
|-------|------|---------------|
| Desktop render | `graph-overview.png` | the graph renders a non-blank, laid-out node/edge canvas |
| Queryable Trace | `graph-trace.png` | Trace `energy-supply ↔ geophysical` → **3 bridges (New Zealand, Greece, Mexico), path through Greece** — the evidence-ranked cross-source answer a static bundle cannot give |
| Mobile responsive | `graph-mobile.png` | the graph fits a 390 px phone viewport (Michael's primary device) |

The smoke also **dispatches a real one-finger touch-drag** on a touch-emulated
device and asserts the canvas pixels change — proving the mobile pan/pinch support
(added to the `build_graph.py` template) actually works in a browser, not just in
the markup.

Acceptance gates (all green): unit token guard (SOTA-viz + touch features present in
the rendered HTML, `tests/unit/test_build_graph.py::test_rendered_html_wires_the_sota_viz_features`)
· embedded JS `node --check` · `build_graph.py --check` in sync · `ruff` + `mypy`
clean · live Playwright smoke (`scripts/smoke_graph.py`) · screenshots above.
Regenerate any time by `python scripts/smoke_graph.py`.
