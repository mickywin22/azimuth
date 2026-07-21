# Demonstrator "what-if" proof (Azimuth KR-B)

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
tooltips, evidence-weighted edge thickness, shareable deep links, **full keyboard
operability** (WCAG 2.1.1), and a **Trace** control that answers *"how do two
channels connect?"* directly over the rendered graph. `scripts/smoke_graph.py` opens
it in a **real Chromium** and proves all of it end-to-end (the browser-render gate the
token-presence unit tests can't reach):

| Proof | File | What it shows |
|-------|------|---------------|
| Desktop render | `graph-overview.png` | the graph renders a non-blank, laid-out node/edge canvas |
| Queryable Trace | `graph-trace.png` | Trace `energy-supply ↔ geophysical` → the **evidence-ranked** bridge list (each bridge tagged `[N+M src]`, the strongest named, the highlighted path routed through it) — the cross-source answer a static bundle cannot give. Bridges move with the live daily data; at capture: *2 bridges, strongest Mexico (1+1 src)* |
| Source-line evidence | `graph-evidence.png` | click/tap a shared entity (or walk to it and press **Enter**) and the page **quotes the literal dated L1 source line from each channel that names it**, deep-linked to the per-day source page — the in-browser `query_graph.py evidence`: a bridge is not asserted, it is proven |
| Keyboard nav | `graph-keyboard.png` | canvas focused, **ArrowRight** walks to the most-connected node, re-centres the view, and a polite live region announces it (*"…: L2 brief · 18 links — press Enter to open. Node 1 of 35."*) — the graph is usable with no mouse |
| Mobile responsive | `graph-mobile.png` | the graph fits a 390 px phone viewport (Michael's primary device) |
| Site discoverability | `site-index-graph-cta.png` | the site front door links the graph twice: the **Knowledge graph** nav entry on every page and the gold index CTA card, whose node/edge/bridge counts are filled live from the published `graph.json` (at capture: *48 nodes, 88 edges, 11 cross-channel bridges*) — verified in Chromium including the click-through landing on `graph.html` |

The smoke also **dispatches a real one-finger touch-drag** on a touch-emulated
device and asserts the canvas pixels change (mobile pan/pinch), and **presses
ArrowRight on the focused canvas** and asserts both the live region announced a node
*and* the canvas redrew — proving the keyboard-nav + touch support (added to the
`build_graph.py` template) actually work in a browser, not just in the markup.

Acceptance gates (all green): unit token guard (SOTA-viz + touch + keyboard-a11y
features present in the rendered HTML,
`tests/unit/test_build_graph.py::test_rendered_html_wires_the_sota_viz_features`)
· embedded JS `node --check` · `build_graph.py --check` in sync · `ruff` + `mypy`
clean · live Playwright smoke (`scripts/smoke_graph.py`) · screenshots above.
Regenerate any time by `python scripts/smoke_graph.py`.

---

# The "incredible UI" landing + story-mode proof (Azimuth KR1)

KR1 makes the front door itself the demonstrator. The landing (`index.html`) leads with
the **knowledge graph as the hero centerpiece** — a live canvas drawn from the published
`graph.json`, not a static screenshot — over a **build-time "vault pulse" sparkline** and
one **inline-SVG sparkline per brief card**, all baked at build time (no runtime data
call). A **responsive hamburger nav** carries the six-entry menu on a phone, and
`graph.html` gains a **story mode**: a guided three-step tour that drives a real cross-channel
**Trace** on each step, so a first-time visitor is shown *why* the graph matters instead of
facing a cold canvas. `scripts/smoke_ui.py` opens the built site in a **real Chromium** and
proves every piece end-to-end — the runtime boundary the token-presence unit tests can't
cross:

| Proof | File | What it shows |
|-------|------|---------------|
| Landing hero (desktop) | `landing-desktop.png` | the whole front door — the graph centerpiece canvas over the vault-pulse sparkline, live node/bridge badge, and brief cards each with their own sparkline |
| Hero graph centerpiece | `landing-hero-graph.png` | the hero `<canvas>` alone — a non-blank, laid-out mini knowledge-graph (smoke asserts ≥1500 non-transparent pixels) with its **"105 nodes · 45 cross-channel bridges"** badge filled live from `graph.json` (re-shot 2026-07-21 at the current live count; the badge tracks each daily ingest) |
| Mobile nav fix | `landing-mobile-nav.png` | at a 390 px phone viewport the flat nav is collapsed behind the burger, then **revealed on tap** (the overflow the burger fixes) — the six-entry menu opens cleanly over the pulse strip |
| Graph story mode | `graph-story.png` | `graph.html` story mode, **STORY 1 OF 3** — the guided tour drives a live Trace ("Energy meets the ground it sits on") whose output names the real shared bridge entities; the smoke walks all three steps and asserts each ran a real Trace, then that **Finish** and **Escape** both exit cleanly |

The smoke's checks (all **PASS** at capture): hero canvas non-blank · badge filled from
`graph.json` · ≥6 sparklines rendered (hero + cards) · vault-pulse strip visible · burger
visible at phone width · nav hidden before tap · nav revealed after tap · three story steps
labelled + each drives a real Trace (3/3) · Finish exits · Escape exits.

Acceptance gates (all green): unit token guards (hero-centerpiece + sparkline + burger-nav +
story-mode markup present in the built HTML) · `ruff` + `mypy` clean · live Playwright smoke
(`scripts/smoke_ui.py`) · screenshots above. Regenerate any time by
`python scripts/smoke_ui.py`.

# Public-launch attach set (W28 new-UI front door)

The banked screenshots the two launch posts attach when Azimuth flips public —
the LinkedIn OKF post and the Show HN pack (both in the HemySphere vault under
`05 Projects/azimuth — …`). First captured 2026-07-06 from the live new-UI front
door (graph-as-hero landing · one-click story mode · mobile nav); the two
count-bearing shots (`landing-desktop.png` + `landing-hero-graph.png`) were
**re-shot 2026-07-21 at the current live count (105 nodes · 45 bridges)** so the
visible headline matches the launch-post body. **These regenerate from
`scripts/smoke_ui.py`** (it screenshots `landing-desktop.png`,
`landing-hero-graph.png`, `landing-mobile-nav.png` + `graph-story.png` after
asserting the live badge) — re-run it whenever the front-door UI or the graph
count moves, then copy the four shots from `_smoke/` here. (On a RAM-starved box
smoke_ui's single-threaded server can stall on `wait_until="load"`; a threading
server + `wait_until="domcontentloaded"` + waiting on `.hero-graph.is-live`
captures cleanly.) They previously lived only in the git-ignored `_smoke/` scratch
dir; banked into `docs/proof/` so the flip launch is one-click and the shots can't
vanish on a `git clean`.

| Shot | File | What it shows / where it's used |
|------|------|--------------------------------|
| Front door (hero) | `landing-desktop.png` | The new landing: the cross-channel knowledge graph as the hero centrepiece over the vault-pulse sparkline + brief cards. Single-shot fallback — carries the whole thesis in one frame (LinkedIn primary / Show HN URL card). |
| Living-graph crop | `landing-hero-graph.png` | Tighter crop of the graph-as-hero centrepiece for a 2-up / carousel first frame. |
| Story mode | `graph-story.png` | Story mode, **STORY 1 OF 3** ("Energy meets the ground it sits on") driving a live cross-source Trace — the v2 body's "one-click story mode / shows its work" bullet. LinkedIn 2-up second frame. |
| Phone front door | `landing-mobile-nav.png` | The front door at a 390 px phone viewport with the hamburger nav — phone-audience alt. |
