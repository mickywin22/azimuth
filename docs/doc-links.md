# Documentation link gate

azimuth ships ~200 Markdown files that cross-link heavily — the [docs index](README.md),
the [changelog](changelog.md), the split-license front door, and the auto-generated
[brief index](../vault/02%20Briefs/README.md). On a **public** repository a dead link is a
credibility bug: it tells a first-time visitor the docs are not maintained. Until this gate
existed those breaks were caught by hand (the 2026-07-01 changelog entry manually fixed a
dead `docs/README.md` link). This gate turns that class of defect into a **build failure**.

## The rule

`scripts/check_doc_links.py` walks every `.md` file in the repo, extracts each **inline**
Markdown link and image, and fails the build (exit 1) if a *local* target does not exist.

It is deliberately narrow so it never false-positives on the constructs this repo genuinely
uses:

| Construct | Handling |
|-----------|----------|
| `[text](plan.md)` / `![alt](img.png)` | checked — must resolve on disk |
| Fenced blocks and `inline code` | **stripped first** — an example link like `[x](/path.md)` is never flagged |
| `https://…`, `mailto:…`, `tel:…`, `//host` | skipped — this gate proves local files exist, not that the network is up |
| `#section` (pure anchor) | skipped |
| `[rules](<00 Rules/editorial.md>)` | angle brackets unwrapped (Markdown's spaces-in-path form) |
| `00%20Rules/editorial.md` | percent-decoded before the existence check |
| `/LICENSE` (leading slash) | resolved against the **repo root** (GitHub semantics) |
| `spec.md#section-3` | anchor/query dropped, then the file part is checked |
| `[[wikilink]]` | **not** checked — not standard Markdown; migration tracked in [strategy/okf-and-knowledge-graph.md](strategy/okf-and-knowledge-graph.md) (G4) |

Generated / vendored trees (`site/`, `_site/`, `.venv/`, caches, `__pycache__`) are excluded.

## Where it runs

- **CI** — the `Synthesis Lint` job in [`ci.yml`](../.github/workflows/ci.yml) runs it on every
  push / PR to `main`. Pure-stdlib, no dependency install.
- **pre-commit** — the local `doc-links` hook in [`.pre-commit-config.yaml`](../.pre-commit-config.yaml)
  fires whenever a `.md` file (or the checker) changes.

## Run it locally

```bash
python scripts/check_doc_links.py
# doc-links: PASS - 75 local link(s) across 204 Markdown file(s), all resolve.
```

A failure prints one `path:line -> target` per dead link, so the fix is always obvious.

See `tests/unit/test_check_doc_links.py` for the teeth-and-no-false-positives regression suite.
