# Dependency Cooldown Policy

> **Status:** DRAFT shipped 2026-05-21 by HemySphere Sprint 19:00 (IQ #312 audit + cooldown gate ship). Enforcement-scope decision (A / B / C below) is Michael L3 — open IQ #312 awaits answer.
>
> **Applies to:** every Coding Factory product instantiated from `project-template/` — Apex, future apps, the factory itself, and any HemySphere-fleet repo that installs npm/pnpm packages outside the curated allowlist. CI supply-chain doctrine (OIDC tokens, `pull_request_target`, SHA-pinning) is owned separately in `00 Context/Sprint Quality Gates.md § Supply-chain doctrine` (Mon 2026-05-18) — this doc covers the **install-time** vector, not the CI-runtime vector.

---

## Threat model — why this policy exists

The Mini Shai-Hulud 317 attack (npm, Tue 2026-05-19, 637 malicious versions in a 22-minute burst across 317 compromised package scopes — Learning Feed Tue 20:30) shipped three new properties that the existing 2024 Shai-Hulud post-mortem did not cover:

1. **Full-spectrum credential harvest at install-time.** Malicious `postinstall` scripts walk `~/.aws/`, `~/.config/gcloud/`, `~/.kube/`, `~/.npmrc`, `~/.docker/config.json`, `~/.ssh/`, browser cookie stores, and the entire `process.env`. They also exfiltrate any token file matching `*token*` / `*credential*` / `*.pem` / `*.p12`.
2. **Novel `.claude/settings.json` SessionStart hook injection.** Several payloads write `~/.claude/settings.json` (or repo-local `.claude/settings.json` if it exists) and add a `SessionStart` hook that fires on every Claude Code launch — silent persistence that survives package removal. Equivalent vectors observed against `~/.codex/`, VS Code `runOn:folderOpen`, and systemd / LaunchAgent units (`kitty-monitor` C2 poller).
3. **Dependency cooldown bypass.** Burst-publish in <30 min defeats any allowlist that only knows about packages older than 24 hours. By the time CISA / npm advisories index a compromised version, every CI run that did a fresh `pnpm install` in that window has already shipped the payload to the attacker's C2.

Property (3) is what this policy gates.

---

## The cooldown window — definition

A **cooldown window** is the minimum elapsed time between a package version's `time["<version>"]` value on the npm / pnpm registry **and** the moment that version is allowed to be `pnpm install`-ed inside any `project-template/`-derived product.

**Default window: 14 days.**

- Empirical fit: npm advisories for the 2024 Shai-Hulud incident took a median of 6.4 days from first publish to public flag (TanStack post-mortem, IQ #256 anchor). Mini Shai-Hulud 317 had compromised versions surfaced inside 22 hours by an independent researcher but the npm advisory landed at 9.1 days. 14 days covers both percentiles with margin.
- Industry comparator: Snyk's "Day-Zero protection" feature uses 7 days; Socket.dev's default is 14 days; Dependabot's `pause` action allows up to 30 days. We sit at the Socket.dev default.
- Acceptable override: if a *direct* dependency (not transitive) needs an urgent security patch (CVSS ≥ 9.0 with known active exploit), the 14-day window may be waived with a signed-off IQ entry recording rationale + CVE + scanning tool consulted. Transitive dependencies never get the override.

**Cooldown does NOT apply to:**
- Re-installs of an already-locked version (lockfile pin counts as prior acceptance).
- Major / minor version bumps within an already-pinned SHA-locked dependency (Renovate / Dependabot PRs already trigger human review — that IS the gate).
- Local symlinked workspace packages (`workspace:*` pnpm protocol).

**Cooldown DOES apply to:**
- Any fresh `pnpm install` / `npm install` that resolves a brand-new package not present in the lockfile.
- Any `pnpm add` / `npm install <pkg>` invocation in interactive or CI use.
- Any `pnpm update` that resolves a version published less than 14 days ago.

---

## Enforcement-scope options — Michael L3 decision (IQ #312)

The policy supports three enforcement modes. Michael picks one per product (or one global) via IQ #312:

| Mode | Behaviour at install time | Effect on dev velocity | Effect on attack surface |
|------|--------------------------|------------------------|--------------------------|
| **A — Block** | Install fails hard. Exit code 1. Error message names the rejected package + its publish time + cooldown window. Override = explicit `--cooldown-bypass <pkg>@<version>` flag with IQ entry filed. | Highest friction. Every new dependency adds 14-day lead time unless pre-staged. Pairs well with monorepo-stable products like Apex post-Phase L. | Strongest. Zero burst-publish exposure. Compromised version cannot enter the lockfile in the attack window. |
| **B — Warn-only** | Install proceeds. A warning prints to stderr + appends one line to `logs/dependency-cooldown.log` with package + version + publish age. CI parses the log and fails the job if any warning fires. | Medium friction. Local `pnpm add` works as today; CI catches the violation post-hoc. Good fit during build-out phases. | Strong on CI surface, weak on local-dev surface. Local credential harvest still possible during the window between `pnpm add` and the next CI run. |
| **C — Advisory** | Install proceeds, no exit fail. Log line is appended (same format as B). No CI gate. Status surfaces in weekly Tuning Review aggregate. | Zero friction. Doc-only signal. | Weakest. Useful as observability runway before flipping to A or B. |

**Recommended starting mode:** **B (Warn-only)** for the first 30 days post-policy-adoption to gather baseline data on how often the gate would actually fire in real workflows. Then escalate to A on a per-product basis as confidence builds. Apex (post-Phase L) is the logical first product to flip to A — the dependency tree is mature and adds are rare.

---

## Implementation surface — where the gate lives

Three insertion points, chosen for matching the modes above:

### 1. Pre-install hook (`scripts/check-dependency-cooldown.{sh,ps1}`)

Runs as a `prepnpminstall` / `preinstall` npm script. Pseudocode:

```
for each package in (resolved-graph diff lockfile.old lockfile.new):
    publish_time = npm view <pkg>@<version> time --json | jq -r .[<version>]
    age_days = (now - publish_time) / 86400
    if age_days < 14 and pkg not in cooldown_bypass_list:
        if mode == A: exit 1
        if mode == B: warn + append log
        if mode == C: append log
```

- Reads cooldown window from `project-template/.claude/dependency-cooldown.config.json` (default 14, overridable per-product).
- Reads `cooldown_bypass_list` from same config (CVE-rationale entries with IQ-link).
- Network call to npm registry uses 10s timeout. **Fail-closed semantics, mode-aware:** a timed-out lookup is treated as if the package is still inside the cooldown window — Mode A then blocks (same as cooldown-not-met), Mode B warns + appends one log line, Mode C appends one log line. This keeps each mode's stated behavior intact while preventing a silent bypass when the npm registry is unreachable.

### 2. CI gate (`.github/workflows/dependency-cooldown.yml`)

For mode B / C: a CI job runs the same script after `pnpm install` completes and fails the workflow if any cooldown warning was logged. For mode A: the pre-install hook already blocks, so this job becomes a sanity check (`grep -c "BLOCK" logs/dependency-cooldown.log` returns 0).

### 3. Weekly Tuning Review summary

The fleet's Sun 19:00 Tuning Review reads `logs/dependency-cooldown.log` across all factory products, aggregates "would-have-blocked" / "blocked" / "bypassed" counts, and surfaces a one-line summary in the weekly Scorecard Slack post. Empty log = healthy; spikes = active threat surface.

---

## What this policy explicitly does NOT cover

- **CI OIDC token / `pull_request_target` / SHA-pinning** — owned by `00 Context/Sprint Quality Gates.md § Supply-chain doctrine`. That doctrine handles the runtime vector; this doc handles the install-time vector.
- **Python / pip dependency cooldown** — out of scope until a Python-backend product needs it. Apex backend is Python but the install-time vector for pip is materially different (no `postinstall` script semantics, no equivalent `.claude/settings.json` SessionStart hook injection observed in PyPI compromise corpus). Revisit when Apex Phase B OpenF1 port lands.
- **Container base-image cooldown** — Apex / future apps deploy via Vercel + serverless; no Dockerfile dependency staging surface today. Add when Apex Phase J Hetzner provisioning lands.
- **User-global `~/.claude/settings.json`** — outside the 4-repo scope of this audit (vault + Apex + Corner + project-template). Michael owns the global; this policy lives in product `.claude/` only.

---

## Audit verdict (2026-05-21, IQ #312 ship)

Cross-repo `.claude/settings*.json` audit across all four scoped repos:

| Repo | File | Hook surface | Authorship | Verdict |
|------|------|--------------|------------|---------|
| HemySphere vault | `.claude/settings.json` | none (permissions only) | Michael / fleet | clean |
| HemySphere vault | `.claude/settings.local.json` | PreToolUse: lean-ctx rewrite + redirect | Michael (documented `~/.claude/rules/lean-ctx.md`) | clean |
| Apex | `.claude/settings.local.json` | PreToolUse: lean-ctx rewrite + redirect | Michael | clean |
| Corner | `.claude/settings.local.json` | PreToolUse: lean-ctx rewrite + redirect | Michael | clean |
| `project-template/` | `.claude/settings.local.json` | PreToolUse: lean-ctx rewrite + redirect | Michael | clean |

**Zero `SessionStart` hooks across all 4 audited repos.** Shai-Hulud 317 attack vector (novel `SessionStart` injection) does not apply to any current HemySphere-fleet surface. Pinned baseline for future regression checks: any `SessionStart` hook appearing in any of these files **without an accompanying Michael L3 doctrine entry** is the trip-wire — flag immediately, do not auto-execute.

---

## Links

- HemySphere supply-chain doctrine (CI side) → `00 Context/Sprint Quality Gates.md § Supply-chain doctrine`
- IQ #256 (parent, 2024 Shai-Hulud TanStack post-mortem anchor) → `01 Inbox/Solo Queue.md` line 79 (Bulk-20 dispatch 2026-05-13)
- IQ #312 (Shai-Hulud 317 escalation, Michael L3 enforcement-scope decision) → `01 Inbox/Input Queue.md`
- Learning Feed Tue 2026-05-19 20:30 (Mini Shai-Hulud 317 batch) → `01 Inbox/Learning Feed.md`
- lean-ctx hook authorship (proves PreToolUse entries are Michael-authored, not injected) → `~/.claude/rules/lean-ctx.md`
