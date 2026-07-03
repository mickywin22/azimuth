# LESSONS

Per-product lessons-learned log. One pattern per entry, captured the moment a
non-obvious failure or a hard-won fix shows up — so the *next* phase of THIS
product (and, via the cross-product doc, the next product) doesn't repeat it.

> **Cross-product canonical lessons** live in the Coding Factory master:
> `05 Projects/Coding Factory/LESSONS.md` in the HemySphere vault, fed by the
> weekly reviewer-concerns digest + sprint reviews and audited monthly. When a
> lesson here is general enough to matter for *other* products, promote it there.

## Entry schema

```
### N. <short title>
**What happened.** <the failure / surprise, concretely>
**Why it matters.** <the cost; why it's not obvious>
**Pattern to keep.** <what to do next time>
**Pattern to drop.** <the anti-pattern that bit us>
**Evidence.** <commit SHA · PR · screenshot · runbook recipe>
```

## When to add an entry

- A green build / green tests shipped something that was actually broken at runtime
  (the four-gate lesson — see the master doc §1).
- A fix only worked after also changing its probe/smoke/test (master §2).
- A deploy/DNS/migration step cost >30 min to re-figure-out — write the recipe AND
  the lesson, then lift the recipe into the runbook.
- Any Reviewer `concerns` verdict on this product that you don't want to see twice.

## Audit

Reviewed at each phase retro and at the monthly Coding Factory review. Stale
entries are retired (don't delete history — mark `~~retired YYYY-MM-DD~~`).

---

## Lessons

### 1. The HemySphere fleet Reviewer does not push azimuth branches — push is a manual step

**What happened.** When a HemySphere fleet Worker builds on azimuth it commits to a
`fleet/<name>` branch, but the fleet Reviewer's auto-push only covers the HemySphere
(vault) repo. azimuth fleet branches sit unpushed until a manual/Michael push, so the
work is invisible on GitHub and never opens a PR on its own.

**Why it matters.** A "done + committed" fleet report on azimuth does NOT mean the work
is on the remote or reviewable — it's banked locally only. Easy to assume it shipped
when it hasn't left the box.

**Pattern to keep.** For any azimuth fleet work, treat push + PR as an explicit
follow-up step (surfaced to Michael via IQ), not something the reviewer handles.

**Pattern to drop.** Assuming the cross-repo reviewer-push behaves like it does on the
vault repo.

**Evidence.** Internal review records (W24).

### 2. CI runs `pytest tests/integration/` but the dir doesn't exist (pre-existing)

**What happened.** `ci.yml`'s `test` job invokes `pytest tests/integration/`, but no
`tests/integration/` directory exists in the repo. This is pre-existing and unrelated to
any single change, so it surfaces as a CI failure on otherwise-clean branches.

**Why it matters.** It's a standing red that makes every branch look broken and masks a
*real* test regression. It also blocks any "merge only on green CI" gate from ever being
satisfiable.

**Pattern to keep.** Resolve it deliberately — either add a real (or stub) `tests/integration/`
dir, or drop the integration step from `ci.yml` — rather than working around it per branch.
Decision is michael_dep (same class as the open integration-tests IQ).

**Pattern to drop.** Re-discovering this red on every new branch and treating it as new.

**Evidence.** `ci.yml` `test` job · internal review records.
