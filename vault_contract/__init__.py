"""vault-contract — the HemySphere L1/L2/L3 vault contract as a reusable engine.

The doctrine this enforces (see the azimuth README for the full story):

* **L1 sources** are append-only ground truth — a synthesis change never touches them.
* **L2 synthesis** evolves notes in place, and **every claim carries a link** back to the
  L1 note it rests on.
* **L3 rules** are small and machine-enforced — each clause below is a blocking check,
  not a guideline.

This package is the generalized distillation of azimuth's production lint
(``synthesis/lint.py`` — the richer, azimuth-specific reference deployment). It is
pure standard library (``tomllib`` for rules files) and has no opinion about your
corpus beyond the rules you declare::

    pip install azimuth            # ships the vault_contract package + CLI
    vault-contract "vault" --rules rules/azimuth.toml

Rules file (TOML)::

    [frontmatter]
    required = ["title", "type", "license"]

    [claims]
    # prose bullets/paragraphs in synthesis notes must carry >=1 link of this shape
    link_pattern = "\\\\[\\\\[[^\\\\]]+\\\\]\\\\]"        # wikilinks; use a md-link regex if you prefer
    sources_root = "vault/01 Sources"           # links must resolve to a real note here

    [changelog]
    required = true                              # an evolving note carries a dated changelog

    [denylist]
    patterns = ["(?i)\\\\byou should (buy|sell)\\\\b"]

    [artifacts]
    markers = ["</content>", "</invoke>"]        # LLM tool-XML must never ship

    [diff]
    allowed_prefixes = ["vault/02 Briefs/"]      # a synthesis commit touches only these
    forbidden_prefixes = ["vault/01 Sources/"]   # and never these
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

__all__ = [
    "RuleSet",
    "check_changelog",
    "check_claim_sourcing",
    "check_denylist",
    "check_diff_guard",
    "check_frontmatter",
    "check_links_resolve",
    "check_tool_artifacts",
    "lint_note",
    "lint_tree",
    "split_frontmatter",
]

_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
_DATED_RE = re.compile(r"^- \d{4}-\d{2}-\d{2}", re.M)


@dataclass
class RuleSet:
    """The declared contract. Every field optional — an empty RuleSet checks nothing."""

    frontmatter_required: list[str] = field(default_factory=list)
    claim_link_pattern: str = ""
    sources_root: str = ""
    changelog_required: bool = False
    denylist: list[str] = field(default_factory=list)
    artifact_markers: list[str] = field(default_factory=list)
    diff_allowed_prefixes: list[str] = field(default_factory=list)
    diff_forbidden_prefixes: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)

    @classmethod
    def from_toml(cls, path: Path) -> RuleSet:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
        return cls(
            exclude=list(raw.get("notes", {}).get("exclude", [])),
            frontmatter_required=list(raw.get("frontmatter", {}).get("required", [])),
            claim_link_pattern=str(raw.get("claims", {}).get("link_pattern", "")),
            sources_root=str(raw.get("claims", {}).get("sources_root", "")),
            changelog_required=bool(raw.get("changelog", {}).get("required", False)),
            denylist=list(raw.get("denylist", {}).get("patterns", [])),
            artifact_markers=list(raw.get("artifacts", {}).get("markers", [])),
            diff_allowed_prefixes=list(raw.get("diff", {}).get("allowed_prefixes", [])),
            diff_forbidden_prefixes=list(raw.get("diff", {}).get("forbidden_prefixes", [])),
        )


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter key->raw value, body). Tolerant: no frontmatter -> ({}, text)."""
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, text[m.end() :]


def check_frontmatter(fm: dict[str, str], required: list[str]) -> list[str]:
    return [f"frontmatter missing required key: {k!r}" for k in required if not fm.get(k)]


def check_claim_sourcing(body: str, link_pattern: str) -> list[str]:
    """Every prose bullet must carry >=1 link matching *link_pattern*.

    Scope mirrors the doctrine's minimum: top-level ``- `` bullets outside the
    ``## Changelog`` section are claims; a claim without a source link fails.
    """
    if not link_pattern:
        return []
    link = re.compile(link_pattern)
    violations: list[str] = []
    in_changelog = False
    bullet: list[str] = []

    def flush() -> None:
        if bullet:
            text = " ".join(bullet)
            if not link.search(text):
                violations.append(f"unsourced claim (no link matching pattern): {text[:80]!r}")
            bullet.clear()

    for line in body.splitlines():
        if line.startswith("## "):
            flush()
            in_changelog = line.strip().lower() == "## changelog"
            continue
        if in_changelog:
            continue
        if line.startswith("- "):
            flush()
            bullet.append(line[2:].strip())
        elif bullet and line.startswith("  ") and line.strip():
            bullet.append(line.strip())
        else:
            flush()
    flush()
    return violations


def check_links_resolve(text: str, link_pattern: str, sources_root: Path | None) -> list[str]:
    """Every ``[[wikilink]]``-style target must resolve to ``<sources_root>/**/<name>.md``."""
    if not sources_root or not link_pattern:
        return []
    names = {p.stem for p in sources_root.rglob("*.md")}
    violations = []
    for m in re.finditer(r"\[\[([^\]|#]+)", text):
        target = m.group(1).strip()
        if target and target not in names:
            violations.append(f"link does not resolve under sources root: [[{target}]]")
    return sorted(set(violations))


def check_changelog(body: str, required: bool) -> list[str]:
    if not required:
        return []
    if "## Changelog" not in body:
        return ["missing '## Changelog' section"]
    tail = body.split("## Changelog", 1)[1]
    if not _DATED_RE.search(tail):
        return ["'## Changelog' has no dated (YYYY-MM-DD) entry"]
    return []


def check_denylist(text: str, patterns: list[str]) -> list[str]:
    violations = []
    for p in patterns:
        m = re.search(p, text)
        if m:
            violations.append(f"denylist hit ({p!r}): {m.group(0)!r}")
    return violations


def check_tool_artifacts(text: str, markers: list[str]) -> list[str]:
    return [f"tool artifact leaked into note: {m!r}" for m in markers if m in text]


def check_diff_guard(
    changed_paths: list[str] | None, allowed: list[str], forbidden: list[str]
) -> list[str]:
    if changed_paths is None or not (allowed or forbidden):
        return []
    violations = []
    for raw in changed_paths:
        norm = raw.replace("\\", "/").strip()
        if not norm:
            continue
        if any(f in norm for f in forbidden):
            violations.append(f"change touches a forbidden path: {norm}")
        elif allowed and not any(a in norm for a in allowed):
            violations.append(f"change outside the allowed paths: {norm}")
    return violations


def lint_note(text: str, rules: RuleSet, sources_root: Path | None = None) -> list[str]:
    """Run every declared check against one note. Empty list == clean."""
    fm, body = split_frontmatter(text)
    violations: list[str] = []
    violations += check_frontmatter(fm, rules.frontmatter_required)
    violations += check_claim_sourcing(body, rules.claim_link_pattern)
    violations += check_links_resolve(text, rules.claim_link_pattern, sources_root)
    violations += check_changelog(body, rules.changelog_required)
    violations += check_denylist(text, rules.denylist)
    violations += check_tool_artifacts(text, rules.artifact_markers)
    return violations


def lint_tree(
    notes_dir: Path, rules: RuleSet, sources_root: Path | None = None
) -> dict[str, list[str]]:
    """Lint every ``*.md`` under *notes_dir*. Returns {relative path: violations}."""
    results: dict[str, list[str]] = {}
    for p in sorted(notes_dir.rglob("*.md")):
        rel = str(p.relative_to(notes_dir)).replace("\\", "/")
        if any(re.fullmatch(pat.replace("*", ".*"), rel) for pat in rules.exclude):
            continue
        v = lint_note(p.read_text(encoding="utf-8"), rules, sources_root)
        if v:
            results[rel] = v
    return results
