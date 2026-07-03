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

## The companion: no orphan docs

The link gate proves every link *points at something real*. Its companion,
`scripts/check_doc_orphans.py`, proves the inverse for the documentation set: every
authored doc *is pointed at*. An orphaned `docs/foo.md` — a page no index, README, or
sibling links to — renders on GitHub only if you already know its URL. On a public repo
that is the same credibility bug as a dead link, one level up.

### The rule

A `docs/**/*.md` file **fails the build** if it is not *reachable* from a repository
front door.

| Concept | Handling |
|---------|----------|
| **Front doors (roots)** | every `*.md` at the repo root — `README.md` (the landing page) plus the community files (`CONTRIBUTING`, `SECURITY`, `SUPPORT`, `CODE_OF_CONDUCT`, `CITATION`, `CREDITS`, `LICENSE*`), all directly discoverable on GitHub |
| **Traversal** | every *inline* Markdown link is followed transitively, reusing the exact link parser of the dead-link gate (code spans stripped, external schemes / anchors skipped, `<spaces>` and `%20` handled) |
| **Required-reachable set** | every `docs/**/*.md` (the same generated / vendored / cache trees the link gate excludes are excluded here too) |
| **Islands** | a cluster of docs that link only each other but that no root reaches is still flagged — mutual links do not rescue an unreachable group |
| Generated data trees (e.g. the brief index under `vault/`) | **out of scope** — engine output, not authored docs (already link-checked) |

### Where it runs

Alongside the link gate: the `Synthesis Lint` job in [`ci.yml`](../.github/workflows/ci.yml)
(`Documentation has no orphans` step) and the `doc-orphans` [pre-commit](../.pre-commit-config.yaml)
hook. Pure stdlib, no dependency install.

### Run it locally

```bash
python scripts/check_doc_orphans.py
# doc-orphans: PASS - all 20 doc(s) under docs/ are reachable from a repo front door.
```

A failure lists each unreachable path and points you at the fix — link it from the
[docs index](README.md) or a relevant sibling. See
`tests/unit/test_check_doc_orphans.py` for the teeth-and-no-false-positives suite.
