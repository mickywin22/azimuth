#!/usr/bin/env python3
"""CI gate: every doc under ``docs/`` is reachable from a public front door.

The dead-link gate (``scripts/check_doc_links.py``) proves every link *points at
something real*. This gate proves the inverse for the documentation set: every
authored doc *is pointed at* -- i.e. a first-time visitor can actually navigate to
it. An orphaned ``docs/foo.md`` -- a page no index, README, or sibling doc links to
-- is invisible on a public repo: it renders on GitHub only if you already know the
URL. That is the same credibility-bug class as a dead link, one level up, so it gets
the same treatment: a build failure instead of a manual catch.

How reachability is defined (deliberately narrow, to match the link gate):

* **Front doors (roots).** Every ``*.md`` at the repository root. On GitHub these are
  all directly discoverable -- ``README.md`` is the landing page, and the community
  files (``CONTRIBUTING``, ``SECURITY``, ``SUPPORT``, ``CODE_OF_CONDUCT``,
  ``CITATION``, ``CREDITS``, ``LICENSE*``) surface via the repo file list and the
  community-profile sidebar. A doc reachable from any of them is discoverable.
* **Traversal.** From the roots we follow every *inline* Markdown link (same parser
  as the dead-link gate -- code spans stripped, external schemes and anchors skipped,
  ``<spaces>``/``%20`` handled) to any existing ``.md`` file, transitively. Passing
  *through* a non-docs file (e.g. a root README that links a doc that links another
  doc) is fine -- what matters is that the docs page is on some path from a root.
* **The universe we require reachable.** Every ``docs/**/*.md`` (excluding the
  generated / vendored / cache trees the link gate already excludes). Generated data
  trees such as the auto-built brief index under ``vault/`` are **out of scope** here
  -- they are engine output, not authored documentation, and are already link-checked.

This intentionally catches an *island* too: a cluster of docs that link only each
other but that no root reaches is still undiscoverable, and is still flagged.

Exits non-zero (failing the build) if any ``docs/`` page is unreachable. Run locally::

    python scripts/check_doc_orphans.py

See docs/doc-links.md for the rule (this gate is documented alongside its sibling).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from check_doc_links import (
    _EXCLUDED_DIRS,
    _LINK_RE,
    _REPO_ROOT,
    _normalise_target,
    _resolve,
    _strip_code,
)

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class OrphanCheckResult:
    docs_total: int = 0
    docs_reachable: int = 0
    orphans: list[Path] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.orphans


def _markdown_link_targets(source: Path) -> list[Path]:
    """Resolved, existing ``.md`` targets linked inline from ``source``."""
    text = _strip_code(source.read_text(encoding="utf-8", errors="replace"))
    targets: list[Path] = []
    for raw in _LINK_RE.findall(text):
        path_part = _normalise_target(raw)
        if path_part is None:
            continue
        resolved = _resolve(source, path_part)
        if resolved.suffix.lower() == ".md" and resolved.exists():
            targets.append(resolved.resolve())
    return targets


def _is_excluded(path: Path, root: Path) -> bool:
    return any(part in _EXCLUDED_DIRS for part in path.relative_to(root).parts)


def _reachable_markdown(root: Path) -> set[Path]:
    """Every ``.md`` reachable from the repo-root front-door files, transitively."""
    roots = [p.resolve() for p in sorted(root.glob("*.md"))]
    seen: set[Path] = set(roots)
    queue = list(roots)
    while queue:
        current = queue.pop()
        for target in _markdown_link_targets(current):
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return seen


def check_orphans(root: Path = _REPO_ROOT) -> OrphanCheckResult:
    reachable = _reachable_markdown(root)
    result = OrphanCheckResult()
    docs_dir = root / "docs"
    if not docs_dir.is_dir():
        return result
    for md in sorted(docs_dir.rglob("*.md")):
        if _is_excluded(md, root):
            continue
        result.docs_total += 1
        if md.resolve() in reachable:
            result.docs_reachable += 1
        else:
            result.orphans.append(md)
    return result


def main() -> int:
    result = check_orphans()
    if result.ok:
        print(
            f"doc-orphans: PASS - all {result.docs_total} doc(s) under docs/ "
            f"are reachable from a repo front door."
        )
        return 0
    print(
        f"doc-orphans: FAIL - {len(result.orphans)} of {result.docs_total} "
        f"doc(s) under docs/ are unreachable (no path from any root *.md):"
    )
    for orphan in result.orphans:
        print(f"  {orphan.relative_to(_REPO_ROOT)}")
    print("Fix: link each from the docs index (docs/README.md) or a relevant sibling.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
