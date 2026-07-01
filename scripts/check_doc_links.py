#!/usr/bin/env python3
"""CI gate: no dead relative links in the repository's Markdown.

azimuth is a public-grade demonstrator with ~200 Markdown files that cross-link
heavily (docs index, changelog, license split, the generated brief index). A dead
link on that public front door is a credibility bug -- and until now they were caught
by hand (see the 2026-07-01 changelog entry that manually fixed a dead `docs/README.md`
link). This gate makes that class of defect a build failure instead of a manual catch.

Scope + robustness (kept deliberately narrow to avoid false positives):

* Only **inline** Markdown links / images -- ``[text](target)`` and ``![alt](target)``.
* Fenced code blocks (```` ``` ````) and inline code spans (`` `...` ``) are stripped
  first, so ``[x](/path.md)`` written as an *example* inside backticks is never flagged.
* External schemes (``http``, ``https``, ``mailto``, ``tel``, ``ftp``, protocol-relative
  ``//``) and pure anchors (``#section``) are skipped -- this gate only proves *local*
  files exist, not that the network is up.
* ``<...>`` angle-bracket targets (Markdown's spaces-in-path form, emitted by the brief
  index) are unwrapped; ``%20``-style percent-encoding is decoded.
* A ``/``-rooted target resolves against the repo root (GitHub semantics); anything else
  resolves against the linking file's directory. A trailing ``#anchor`` / ``?query`` is
  dropped before the existence check.
* Obsidian ``[[wikilinks]]`` are intentionally NOT checked -- they are not standard
  Markdown, GitHub does not resolve them, and migrating away from them is tracked
  separately (docs/strategy/okf-and-knowledge-graph.md, G4).

Exits non-zero (failing the build) if any checked link points at a missing path. Run
locally with::

    python scripts/check_doc_links.py

See docs/doc-links.md for the rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

_REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories that are build output, caches, or virtualenvs -- never source docs.
_EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".benchmarks",
        "__pycache__",
        "node_modules",
        "_site",
        "_smoke",
        "site",  # generated static site (build_site.py output)
    }
)

_EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://", "//")

# Inline links and images: optional leading '!', a '[...]' label, then '(target)'.
# The target is captured lazily up to the first unescaped ')'.
_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]*)\)")

_FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
# Inline code span (CommonMark): a run of N backticks, content, then a *closing
# run of the same length N*. Matching the run length (via the \1 backreference)
# rather than a single backtick is what keeps double/quad-backtick spans -- e.g.
# ``` `` `[x](/path.md)` `` ``` used to show link syntax verbatim -- from
# mis-pairing and leaking the example link back into the scan.
_INLINE_CODE_RE = re.compile(r"(`+)[^\n]*?\1")


@dataclass
class DeadLink:
    """One Markdown link whose local target does not exist."""

    source: Path
    line: int
    target: str


@dataclass
class LinkCheckResult:
    files_scanned: int = 0
    links_checked: int = 0
    dead: list[DeadLink] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.dead


def _strip_code(text: str) -> str:
    """Blank out fenced blocks + inline spans, preserving line count.

    Newlines inside a fenced block are kept so per-line reporting stays accurate;
    only the non-newline characters are replaced.
    """

    def _blank(match: re.Match[str]) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    text = _FENCED_CODE_RE.sub(_blank, text)
    return _INLINE_CODE_RE.sub(_blank, text)


def _normalise_target(raw: str) -> str | None:
    """Return the local path portion of a link target, or None if not local."""
    target = raw.strip()
    if not target:
        return None
    # Markdown allows <...> around a target to permit spaces.
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    # A "url title" form -- drop the optional title in quotes.
    if " " in target and (target.rstrip().endswith('"') or '"' in target):
        target = target.split(" ", 1)[0]
    if not target or target.startswith("#"):
        return None
    if target.lower().startswith(_EXTERNAL_SCHEMES):
        return None
    # Drop anchor / query, then percent-decode (%20 -> space).
    path_part = target.split("#", 1)[0].split("?", 1)[0]
    path_part = unquote(path_part)
    return path_part or None


def _resolve(source: Path, path_part: str) -> Path:
    if path_part.startswith("/"):
        return (_REPO_ROOT / path_part.lstrip("/")).resolve()
    return (source.parent / path_part).resolve()


def _iter_markdown(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in _EXCLUDED_DIRS for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def check_links(root: Path = _REPO_ROOT) -> LinkCheckResult:
    result = LinkCheckResult()
    for md in _iter_markdown(root):
        result.files_scanned += 1
        text = _strip_code(md.read_text(encoding="utf-8", errors="replace"))
        for lineno, line in enumerate(text.splitlines(), start=1):
            for raw in _LINK_RE.findall(line):
                path_part = _normalise_target(raw)
                if path_part is None:
                    continue
                result.links_checked += 1
                if not _resolve(md, path_part).exists():
                    result.dead.append(DeadLink(md, lineno, raw.strip()))
    return result


def main() -> int:
    result = check_links()
    if result.ok:
        print(
            f"doc-links: PASS - {result.links_checked} local link(s) across "
            f"{result.files_scanned} Markdown file(s), all resolve."
        )
        return 0
    print(
        f"doc-links: FAIL - {len(result.dead)} dead link(s) across "
        f"{result.files_scanned} Markdown file(s):"
    )
    for dead in result.dead:
        rel = dead.source.relative_to(_REPO_ROOT)
        print(f"  {rel}:{dead.line} -> {dead.target}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
