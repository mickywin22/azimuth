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
