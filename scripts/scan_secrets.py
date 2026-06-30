#!/usr/bin/env python3
"""Pure-stdlib secret scanner — the Azimuth public-flip HARD gate (C1).

Scans the **full git history** (every blob ever committed, reachable from any
ref) **and** the current working tree for leaked credentials: API keys, tokens,
private keys, webhooks, real DB connection strings. Exits non-zero on any real
finding so it can block CI and a public flip.

Why a stdlib scanner *in addition to* the gitleaks GitHub Action
(`.github/workflows/secret-scan.yml`): the Action enforces the gate on every
push once the repo is public, but it needs the gitleaks binary + network. This
script runs anywhere Python runs (no install, no download), so the gate stays
reproducible from a developer box or a fleet worker that can't fetch a binary.
The two are belt-and-suspenders; both must be CLEAN before the flip.

Usage:
    python scripts/scan_secrets.py            # scan history + working tree
    python scripts/scan_secrets.py --history  # history only
    python scripts/scan_secrets.py --worktree # working tree only
    python scripts/scan_secrets.py --json     # machine-readable findings
    python scripts/scan_secrets.py --report   # markdown verdict to stdout

Exit code: 0 = CLEAN (no real secret), 1 = leak(s) found, 2 = usage/git error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field

# --- Detection rules --------------------------------------------------------
# Each rule is high-signal: anchored prefixes + realistic lengths so a literal
# placeholder ("sk-ant-...", "your-anon-key") does NOT match. The generic
# assignment rule is the only entropy-based one and is the most allowlist-prone.


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    note: str = ""


RULES: list[Rule] = [
    Rule(
        "anthropic-api-key",
        re.compile(r"sk-ant-(?:api03|admin01)-[A-Za-z0-9_\-]{32,}"),
        "Anthropic API/admin key",
    ),
    Rule(
        "openai-api-key",
        re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}\b"),
        "OpenAI-style secret key",
    ),
    Rule("aws-access-key-id", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    Rule(
        "aws-secret-access-key",
        re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+]{40}['\"]?"),
        "AWS secret access key",
    ),
    Rule(
        "private-key-block",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
        "PEM/OpenSSH private key block",
    ),
    Rule(
        "slack-webhook",
        re.compile(
            r"https://hooks\.slack\.com/services/T[A-Za-z0-9]+/B[A-Za-z0-9]+/[A-Za-z0-9]{16,}"
        ),
        "Slack incoming-webhook URL (with real token segment)",
    ),
    Rule("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Slack API token"),
    Rule("github-pat", re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub personal access token"),
    Rule(
        "github-fine-pat",
        re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b"),
        "GitHub fine-grained PAT",
    ),
    Rule("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "Google API key"),
    Rule(
        "jwt",
        re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"),
        "JSON Web Token (e.g. Supabase service_role key)",
    ),
    Rule(
        "db-url-credentials",
        re.compile(
            r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s:/@]+:[^\s:/@]+@[^\s/]+"
        ),
        "Database URL with embedded username:password",
    ),
    Rule(
        "generic-assigned-secret",
        re.compile(
            r"""(?ix)
            \b(?:api[_-]?key|secret|token|passwd|password|access[_-]?key|client[_-]?secret)\b
            \s*[:=]\s*
            ['"]([^'"\s]{16,})['"]
            """
        ),
        "High-entropy value assigned to a secret-named variable",
    ),
]

# --- Allowlist --------------------------------------------------------------
# Substrings that mark a match as a known-safe placeholder / example / doc ref.
# Case-insensitive. If the matched text (or its captured value) contains any of
# these, the finding is dropped.
ALLOW_SUBSTRINGS: tuple[str, ...] = (
    "example",
    "placeholder",
    "your-",
    "your_",
    "youranon",
    "changeme",
    "change-me",
    "dummy",
    "fake",
    "sample",
    "redacted",
    "xxxx",
    "...",
    "<",
    "user:password@host",
    "postgres:postgres@",
    "user:pass@",
    "dbname",
    "abc123",
    "test_",
    "_test",
    "sk-ant-...",
    "sk-...",
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
)

# Paths whose *entire* content is documentation / templates and never holds a
# real secret. Matches are suppressed for these (suffix match on the path).
ALLOW_PATH_SUFFIXES: tuple[str, ...] = (
    ".env.example",
    "scan_secrets.py",  # this file's own rule strings
    ".gitleaks.toml",  # the allowlist config carries example patterns
    "docs/security/public-flip-readiness.md",
)

# Path suffixes that are pure prose docs — only the strong rules (real key
# prefixes, private-key blocks) fire here; the generic-assignment rule is muted
# because architecture docs legitimately discuss "ANTHROPIC_API_KEY" by name.
DOC_PATH_SUFFIXES: tuple[str, ...] = (".md", ".txt", ".rst")
DOC_MUTED_RULES: frozenset[str] = frozenset({"generic-assigned-secret"})


@dataclass
class Finding:
    rule: str
    note: str
    where: str  # "history@<sha>" or "worktree"
    path: str
    line: int
    redacted: str
    findings_meta: dict[str, str] = field(default_factory=dict)


def _redact(text: str) -> str:
    text = text.strip()
    if len(text) <= 12:
        return text[0:2] + "***"
    return text[:6] + "***" + text[-4:]


def _is_allowed(matched: str, path: str, rule: Rule) -> bool:
    low = matched.lower()
    if any(sub in low for sub in ALLOW_SUBSTRINGS):
        return True
    if any(path.endswith(suf) for suf in ALLOW_PATH_SUFFIXES):
        return True
    return rule.name in DOC_MUTED_RULES and any(path.endswith(suf) for suf in DOC_PATH_SUFFIXES)


def _scan_text(text: str, where: str, path: str) -> list[Finding]:
    out: list[Finding] = []
    lines = text.splitlines()
    for rule in RULES:
        for m in rule.pattern.finditer(text):
            matched = m.group(0)
            if _is_allowed(matched, path, rule):
                continue
            line_no = text.count("\n", 0, m.start()) + 1
            ctx = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
            out.append(
                Finding(
                    rule=rule.name,
                    note=rule.note,
                    where=where,
                    path=path,
                    line=line_no,
                    redacted=_redact(matched),
                    findings_meta={"context": _redact(ctx)},
                )
            )
    return out


def _git(args: list[str]) -> str:
    res = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout


def _git_bytes(args: list[str]) -> bytes:
    res = subprocess.run(["git", *args], capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed")
    return res.stdout


def scan_history() -> tuple[list[Finding], int]:
    """Scan every unique blob reachable from any ref. Returns (findings, blobs)."""
    out = _git(["rev-list", "--all", "--objects"])
    # lines: "<sha> [path]" — only blobs have a path; commits/trees we skip.
    blob_paths: dict[str, str] = {}
    for ln in out.splitlines():
        parts = ln.split(" ", 1)
        if len(parts) != 2:
            continue
        sha, path = parts
        blob_paths.setdefault(sha, path)
    findings: list[Finding] = []
    scanned = 0
    for sha, path in blob_paths.items():
        # type-check: only scan blobs, skip trees
        try:
            otype = _git(["cat-file", "-t", sha]).strip()
        except RuntimeError:
            continue
        if otype != "blob":
            continue
        try:
            raw = _git_bytes(["cat-file", "blob", sha])
        except RuntimeError:
            continue
        if b"\x00" in raw[:8192]:  # binary blob, skip
            continue
        text = raw.decode("utf-8", errors="replace")
        scanned += 1
        findings.extend(_scan_text(text, f"history@{sha[:10]}", path))
    return findings, scanned


def scan_worktree() -> tuple[list[Finding], int]:
    """Scan tracked + untracked-not-ignored files in the working tree."""
    out = _git(["ls-files", "--cached", "--others", "--exclude-standard"])
    findings: list[Finding] = []
    scanned = 0
    for path in out.splitlines():
        path = path.strip()
        if not path:
            continue
        try:
            with open(path, "rb") as fh:
                raw = fh.read()
        except (OSError, IsADirectoryError):
            continue
        if b"\x00" in raw[:8192]:
            continue
        text = raw.decode("utf-8", errors="replace")
        scanned += 1
        findings.extend(_scan_text(text, "worktree", path))
    return findings, scanned


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Azimuth public-flip secret-scan gate (C1).")
    ap.add_argument("--history", action="store_true", help="scan git history only")
    ap.add_argument("--worktree", action="store_true", help="scan working tree only")
    ap.add_argument("--json", action="store_true", help="emit findings as JSON")
    ap.add_argument("--report", action="store_true", help="emit a markdown verdict block")
    args = ap.parse_args(argv)

    do_history = args.history or not args.worktree
    do_worktree = args.worktree or not args.history

    findings: list[Finding] = []
    hist_blobs = wt_files = 0
    try:
        if do_history:
            f, hist_blobs = scan_history()
            findings.extend(f)
        if do_worktree:
            f, wt_files = scan_worktree()
            findings.extend(f)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    clean = not findings

    if args.json:
        print(
            json.dumps(
                {
                    "clean": clean,
                    "history_blobs_scanned": hist_blobs,
                    "worktree_files_scanned": wt_files,
                    "findings": [
                        {
                            "rule": x.rule,
                            "note": x.note,
                            "where": x.where,
                            "path": x.path,
                            "line": x.line,
                            "redacted": x.redacted,
                        }
                        for x in findings
                    ],
                },
                indent=2,
            )
        )
        return 0 if clean else 1

    if args.report:
        verdict = "CLEAN -- gate PASSED" if clean else "LEAK(S) FOUND -- gate BLOCKED"
        print(f"## Secret-scan verdict: {verdict}")
        print()
        print(f"- history blobs scanned: **{hist_blobs}**")
        print(f"- working-tree files scanned: **{wt_files}**")
        print(f"- findings: **{len(findings)}**")
        if findings:
            print()
            print("| rule | where | path | line | match |")
            print("|------|-------|------|------|-------|")
            for x in findings:
                print(f"| {x.rule} | {x.where} | `{x.path}` | {x.line} | `{x.redacted}` |")
        return 0 if clean else 1

    # default: human summary
    print(f"Scanned {hist_blobs} history blobs + {wt_files} working-tree files.")
    if clean:
        print("CLEAN -- no secrets detected. Public-flip secret gate (C1) PASSED.")
        return 0
    print(f"LEAK(S) FOUND: {len(findings)} -- public flip BLOCKED.")
    for x in findings:
        print(f"  [{x.rule}] {x.where} {x.path}:{x.line} -> {x.redacted}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
