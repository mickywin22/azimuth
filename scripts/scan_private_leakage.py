#!/usr/bin/env python3
"""Pure-stdlib private-leakage scanner — the Azimuth public-flip privacy gate (C1b).

The secret scanner (``scan_secrets.py``, C1) catches leaked *credentials* — keys,
tokens, private-key blocks. It does **not** catch the other thing that must not
ship when a private-by-design repo goes public: **owner-private context**. Azimuth
exists to demonstrate the HemySphere/Emi *pattern* on neutral public data
"without ever exposing Michael's private vault content or USP" (`05 Projects/
azimuth.md`). Naming the doctrine bundle is the public pitch and is fine; what is
NOT fine is shipping the owner's local machine paths, personal email, the private
fleet's local hook commands, or internal process bookkeeping that leaked in via
the project-template scaffold.

This scanner is the C1b counterpart to C1: same belt-and-suspenders posture
(works anywhere Python runs, no install), same full-history + working-tree reach.

Two severities:
  * HARD (exit 1) — owner-private data that NEVER belongs in a public repo:
    personal absolute paths, the owner's personal email, local-machine hook
    commands. These are high-signal and do not false-positive on the intentional
    "HemySphere doctrine / Emi pattern" public pitch.
  * ADVISORY (reported, does not fail unless --strict) — internal process refs
    (private IQ ticket numbers, internal sprint/audit markers) that read as noise
    in a public repo but are a judgement call, not a hard breach. Surfaced so the
    flip decision (a Michael go-gate) can weigh them.

Usage:
    python scripts/scan_private_leakage.py            # history + working tree
    python scripts/scan_private_leakage.py --worktree # working tree only
    python scripts/scan_private_leakage.py --history  # history only
    python scripts/scan_private_leakage.py --strict   # advisory findings also fail
    python scripts/scan_private_leakage.py --json      # machine-readable
    python scripts/scan_private_leakage.py --report    # markdown verdict

Exit code: 0 = CLEAN (no HARD finding; advisory ok unless --strict),
           1 = leak(s) found, 2 = usage/git error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field

# --- Detection rules --------------------------------------------------------
# HARD rules: owner-private data with no legitimate place in a public repo.
# Each is anchored so the intentional public pitch ("HemySphere L1/L2/L3 vault
# doctrine", "Emi synthesis layer") never matches — those carry no path, no
# email, no local command.


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    note: str
    severity: str = "hard"  # "hard" | "advisory"


HARD_RULES: list[Rule] = [
    Rule(
        "personal-abs-path-windows",
        re.compile(r"(?i)[A-Za-z]:\\Users\\Michael\b"),
        "Owner's Windows home path (exposes username + local layout)",
    ),
    Rule(
        "personal-abs-path-unix",
        re.compile(r"(?i)/(?:Users|home)/Michael\b"),
        "Owner's unix home path",
    ),
    Rule(
        "hemysphere-local-path",
        re.compile(r"(?i)[A-Za-z]:\\Users\\[^\\\s]+\\HemySphere\b|/HemySphere/"),
        "Absolute path into the private HemySphere vault",
    ),
    Rule(
        # The bare surname in a LICENSE/README copyright line is *intentional*
        # attribution (the OSS-credibility play wants Michael's real name public).
        # Only the email address itself is a leak: match the "m.rarivomanana"
        # email local-part or any "rarivomanana@" form, never " Rarivomanana".
        "personal-email",
        re.compile(r"(?i)\bm\.rarivomanana\b|rarivomanana@"),
        "Owner's personal email address (not the attribution surname)",
    ),
    Rule(
        "local-machine-hook",
        re.compile(r"(?i)lean-ctx\.exe\s+hook|package-cooldown\.ps1"),
        "Owner's local-machine Claude hook command (machine-specific, not the demo)",
    ),
]

# ADVISORY rules: internal process bookkeeping. Reported, not fatal unless
# --strict, because some of it (e.g. the LESSONS doc citing an IQ as evidence)
# is a deliberate, defensible boundary note — the flip go-gate decides.
ADVISORY_RULES: list[Rule] = [
    Rule(
        "internal-iq-ref",
        re.compile(r"\bIQ\s*#\d{2,4}\b"),
        "Private HemySphere Input-Queue ticket number",
        severity="advisory",
    ),
    Rule(
        "internal-sprint-audit-marker",
        re.compile(r"(?i)HemySphere\s+Sprint|Shai-Hulud|Tactical Dispatcher|Strategic Architect"),
        "Private-fleet internal process / audit marker",
        severity="advisory",
    ),
]

ALL_RULES: list[Rule] = HARD_RULES + ADVISORY_RULES

# --- Allowlist --------------------------------------------------------------
# This scanner's own rule strings + the readiness doc (which explains the gate
# and necessarily quotes example markers) are documentation, not leaks. So is
# the history-scrub helper, which by design *names* the owner-private paths it
# removes (e.g. the `/HemySphere/` deploy path, `C:\Users\…` example) — flagging
# the tool that purges leaks as a leak is a false positive. Keep this list tight:
# only tooling/docs with no product content; never broaden it to silence a real
# finding in a publishable file.
ALLOW_PATH_SUFFIXES: tuple[str, ...] = (
    "scan_private_leakage.py",
    "tests/unit/test_scan_private_leakage.py",
    "tests/integration/test_history_dangling_blob.py",
    "docs/security/public-flip-readiness.md",
    "scripts/scrub-history.sh",
)


@dataclass
class Finding:
    rule: str
    note: str
    severity: str
    where: str  # "history@<sha>" or "worktree"
    path: str
    line: int
    redacted: str
    findings_meta: dict[str, str] = field(default_factory=dict)


def _redact(text: str) -> str:
    text = text.strip()
    if len(text) <= 12:
        return text
    return text[:8] + "..." + text[-4:]


def _is_allowed(path: str) -> bool:
    return any(path.endswith(suf) for suf in ALLOW_PATH_SUFFIXES)


def _scan_text(text: str, where: str, path: str) -> list[Finding]:
    if _is_allowed(path):
        return []
    out: list[Finding] = []
    lines = text.splitlines()
    for rule in ALL_RULES:
        for m in rule.pattern.finditer(text):
            matched = m.group(0)
            line_no = text.count("\n", 0, m.start()) + 1
            ctx = lines[line_no - 1] if 0 < line_no <= len(lines) else ""
            out.append(
                Finding(
                    rule=rule.name,
                    note=rule.note,
                    severity=rule.severity,
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
        ["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout


def _blob_path_labels() -> dict[str, str]:
    """Best-effort sha -> a representative path, for nicer finding labels.

    Cosmetic only: a dangling blob has no path here and is still scanned. If
    rev-list fails we proceed with empty labels rather than abort the gate.
    """
    labels: dict[str, str] = {}
    try:
        out = _git(["rev-list", "--all", "--objects"])
    except RuntimeError:
        return labels
    for ln in out.splitlines():
        parts = ln.split(" ", 1)
        if len(parts) == 2:
            labels.setdefault(parts[0], parts[1])
    return labels


def scan_history() -> tuple[list[Finding], int]:
    """Scan every blob in the object database — reachable or not — for owner-private data.

    Mirrors the C1 secret gate's single streamed ``cat-file --batch-all-objects``
    pass: ONE git child instead of ~2 spawns per blob. The old ``rev-list`` +
    per-blob ``cat-file`` form spawned ~2N git processes (≈1200 here) and was slow
    enough on Windows that running the C1c history check inline (e.g. from the flip
    aggregator) was impractical. ``--batch-all-objects`` also reaches UNREACHABLE
    blobs, so owner-private content hidden in a dangling/orphaned object can no
    longer slip the privacy gate — closing the exact coverage gap the secret gate
    (``scan_secrets.py``) already covers. Returns (findings, blobs_scanned).
    """
    blob_paths = _blob_path_labels()
    res = subprocess.run(
        ["git", "cat-file", "--batch-all-objects", "--batch", "--buffer"],
        capture_output=True,
    )
    if res.returncode != 0:
        raise RuntimeError(
            f"git cat-file --batch failed: {res.stderr.decode('utf-8', 'replace').strip()}"
        )
    data = res.stdout
    findings: list[Finding] = []
    scanned = 0
    i, n = 0, len(data)
    while i < n:
        nl = data.find(b"\n", i)
        if nl == -1:
            break
        header = data[i:nl].decode("utf-8", "replace")
        i = nl + 1
        parts = header.split(" ")
        # header is "<oid> <type> <size>"; a missing object is "<oid> missing".
        if len(parts) < 3:
            continue
        oid, otype = parts[0], parts[1]
        try:
            size = int(parts[2])
        except ValueError:
            continue
        body = data[i : i + size]
        i += size + 1  # advance past the body and its trailing LF
        if otype != "blob":
            continue
        if b"\x00" in body[:8192]:  # binary blob, skip
            continue
        text = body.decode("utf-8", errors="replace")
        scanned += 1
        findings.extend(_scan_text(text, f"history@{oid[:10]}", blob_paths.get(oid, "")))
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
    ap = argparse.ArgumentParser(description="Azimuth public-flip private-leakage gate (C1b).")
    ap.add_argument("--history", action="store_true", help="scan git history only")
    ap.add_argument("--worktree", action="store_true", help="scan working tree only")
    ap.add_argument("--strict", action="store_true", help="advisory findings also fail the gate")
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

    hard = [x for x in findings if x.severity == "hard"]
    advisory = [x for x in findings if x.severity == "advisory"]
    blocked = bool(hard) or (args.strict and bool(advisory))

    if args.json:
        print(
            json.dumps(
                {
                    "clean": not blocked,
                    "hard_findings": len(hard),
                    "advisory_findings": len(advisory),
                    "history_blobs_scanned": hist_blobs,
                    "worktree_files_scanned": wt_files,
                    "findings": [
                        {
                            "rule": x.rule,
                            "note": x.note,
                            "severity": x.severity,
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
        return 1 if blocked else 0

    if args.report:
        verdict = "CLEAN -- gate PASSED" if not blocked else "LEAK(S) FOUND -- gate BLOCKED"
        print(f"## Private-leakage verdict: {verdict}")
        print()
        print(f"- history blobs scanned: **{hist_blobs}**")
        print(f"- working-tree files scanned: **{wt_files}**")
        print(f"- HARD findings: **{len(hard)}** | advisory: **{len(advisory)}**")
        if findings:
            print()
            print("| sev | rule | where | path | line | match |")
            print("|-----|------|-------|------|------|-------|")
            for x in findings:
                print(
                    f"| {x.severity} | {x.rule} | {x.where} | `{x.path}` | {x.line} "
                    f"| `{x.redacted}` |"
                )
        return 1 if blocked else 0

    # default: human summary
    print(f"Scanned {hist_blobs} history blobs + {wt_files} working-tree files.")
    if not hard and not advisory:
        print("CLEAN -- no private leakage. Public-flip privacy gate (C1b) PASSED.")
        return 0
    if hard:
        print(f"HARD LEAK(S): {len(hard)} -- public flip BLOCKED.")
        for x in hard:
            print(f"  [{x.rule}] {x.where} {x.path}:{x.line} -> {x.redacted}")
    if advisory:
        tag = "BLOCKED (--strict)" if args.strict else "advisory only"
        print(f"Advisory finding(s): {len(advisory)} -- {tag}.")
        for x in advisory:
            print(f"  [{x.rule}] {x.where} {x.path}:{x.line} -> {x.redacted}")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
