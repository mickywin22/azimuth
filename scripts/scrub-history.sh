#!/usr/bin/env bash
# Azimuth public-flip C1c gate — git-history scrub for owner-private context.
#
# WHAT IT REMOVES
#   Every blob, on ALL refs / all history, of the paths that the private-leakage
#   scanner (scripts/scan_private_leakage.py) flags HARD but that are already
#   gone from the working tree — they survive only in old commits and would leak
#   the moment the repo goes public. As of 2026-06-30 that is four paths:
#
#     .claude/                              local-dev config — settings.local.json
#                                           held this box's absolute hook paths
#                                           (e.g. C:\Users\<you>\...\lean-ctx.exe)
#                                           + dependency-cooldown-policy.md
#                                           (HemySphere-internal scaffold doctrine)
#     docs/security/secret-scan-2026-06-30.md   old blob leaked C:\Users\<owner>\...
#                                           (folded into public-flip-readiness.md;
#                                           the live HEAD copy was already clean)
#     docs/security/gitleaks-2026-06-24.md  old gitleaks report — leaked C:\Users\...
#     docs/coolify-deploy.md                deploy note — leaked the /HemySphere/ path
#
#   NO product code or public content lives at any of these paths — they are all
#   already absent from HEAD. Keep this list in lock-step with the scanner: run
#   `python scripts/scan_private_leakage.py --history --report` and every HARD
#   `history@…` path that is gone from HEAD belongs here.
#
# WHY A REWRITE IS NEEDED
#   A file removed in a later commit still lives in every commit before the
#   removal. Only a history rewrite (filter-repo / filter-branch) purges the old
#   blobs. That is destructive + needs a force-push, so:
#
#       THE FORCE-PUSH IS A MICHAEL / REVIEWER GATE. This script NEVER pushes.
#
# MODES
#   verify   (default) Clone the repo to a temp dir, run the strip there, re-run
#            the private-leakage history scan on the rewrite, assert 0 HARD
#            findings. Proves the scrub works WITHOUT touching the real repo.
#   execute  Run the strip IN PLACE on this repo (after a safety backup branch +
#            tag). Leaves the rewritten history staged for Michael to inspect and
#            force-push manually. Still does NOT push.
#
# USAGE
#   bash scripts/scrub-history.sh            # verify (safe, non-destructive)
#   bash scripts/scrub-history.sh verify
#   bash scripts/scrub-history.sh execute    # rewrite THIS repo (no push)
#
# EXIT: 0 = scrub produced a clean history (0 HARD findings); 1 = still dirty /
#       error. In verify mode a non-zero exit means the strip is NOT ready.
set -euo pipefail

MODE="${1:-verify}"

# Paths to purge from ALL history. Edit this list (and the header note above)
# whenever the history scan surfaces a new HARD path that is gone from HEAD.
SCRUB_PATHS=(
  ".claude"
  "docs/security/secret-scan-2026-06-30.md"
  "docs/security/gitleaks-2026-06-24.md"
  "docs/coolify-deploy.md"
)

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

say() { printf '\n=== %s ===\n' "$*"; }

# ---------------------------------------------------------------------------
# strip_history <workdir>
#   Rewrites ALL refs in <workdir> to drop every path in SCRUB_PATHS, then drops
#   the filter-branch backup refs + expires the reflog + gc so the purged blobs
#   become truly unreachable (otherwise `git rev-list --all` still sees them via
#   refs/original/ and the scan would false-fail).
# ---------------------------------------------------------------------------
strip_history() {
  local wd="$1"
  cd "$wd"
  if command -v git-filter-repo >/dev/null 2>&1 || git filter-repo --version >/dev/null 2>&1; then
    say "stripping ${#SCRUB_PATHS[@]} path(s) with git filter-repo"
    local fr_args=()
    local p
    for p in "${SCRUB_PATHS[@]}"; do
      fr_args+=(--path "$p")
    done
    git filter-repo --force --invert-paths "${fr_args[@]}"
  else
    say "stripping ${#SCRUB_PATHS[@]} path(s) with git filter-branch (filter-repo not installed)"
    # Build one `git rm -r --cached --ignore-unmatch <p1> <p2> …` index filter so
    # all paths are dropped in a single history pass.
    local rm_cmd="git rm -r --cached --ignore-unmatch"
    local p
    for p in "${SCRUB_PATHS[@]}"; do
      rm_cmd+=" '$p'"
    done
    FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force \
      --index-filter "$rm_cmd" \
      --prune-empty --tag-name-filter cat -- --all
    # Drop the backup refs filter-branch leaves behind, then make the old blobs
    # unreachable so the verification scan reflects the true post-push state.
    git for-each-ref --format='%(refname)' refs/original/ \
      | while read -r ref; do git update-ref -d "$ref"; done
    git reflog expire --expire=now --all
    git gc --prune=now --quiet
  fi
  cd "$REPO_ROOT"
}

# Count HARD findings in <workdir>'s history. Prints an integer.
# The scanner exits 1 when it FINDS leaks (that is its gate signal, not an error),
# so `|| true` keeps that expected non-zero from tripping `set -e`/`pipefail` —
# we only care about the JSON it prints, not its exit code.
count_hard() {
  local wd="$1"
  ( cd "$wd" && python scripts/scan_private_leakage.py --history --json 2>/dev/null || true ) \
    | python -c "import json,sys;d=json.load(sys.stdin);f=d.get('findings',d) if isinstance(d,dict) else d;print(sum(1 for x in f if str(x.get('severity','')).upper()=='HARD'))"
}

case "$MODE" in
  verify)
    TMP="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/azimuth-scrub-$$")"
    mkdir -p "$TMP"
    CLONE="$TMP/azimuth"
    say "cloning current repo -> $CLONE (non-destructive)"
    git clone --quiet --no-local "$REPO_ROOT" "$CLONE"

    say "history leakage scan BEFORE strip (expect HARD > 0)"
    BEFORE=$(count_hard "$CLONE")
    echo "HARD findings before strip: $BEFORE"

    strip_history "$CLONE"

    say "history leakage scan AFTER strip (expect HARD == 0)"
    AFTER=$(count_hard "$CLONE")
    echo "HARD findings after strip:  $AFTER"

    say "secret scan AFTER strip (must stay CLEAN, exit 0)"
    if (cd "$CLONE" && python scripts/scan_secrets.py >/dev/null 2>&1); then
      echo "secret scan: CLEAN"
      SECRET_OK=1
    else
      echo "secret scan: LEAK FOUND"
      SECRET_OK=0
    fi

    say "cleanup temp clone"
    rm -rf "$TMP"

    if [ "$AFTER" = "0" ] && [ "$SECRET_OK" = "1" ]; then
      say "VERIFY PASS — scrub removes all $BEFORE HARD history findings, secret gate stays clean. Ready for Michael to execute + force-push."
      exit 0
    else
      say "VERIFY FAIL — rewrite did NOT reach a clean state (HARD after=$AFTER, secretOK=$SECRET_OK). Do NOT force-push."
      exit 1
    fi
    ;;

  execute)
    say "EXECUTE — rewriting THIS repo in place (no push)"
    STAMP="$(git rev-parse --short HEAD)"
    BACKUP="backup/pre-scrub-${STAMP}"
    say "safety backup branch + tag: $BACKUP"
    git branch -f "$BACKUP" HEAD
    git tag -f "pre-scrub-${STAMP}" HEAD

    strip_history "$REPO_ROOT"

    say "post-strip history leakage scan"
    AFTER=$(count_hard "$REPO_ROOT")
    echo "HARD findings after strip: $AFTER"

    cat <<EOF

History rewritten in place. Backup kept at branch '$BACKUP' / tag 'pre-scrub-${STAMP}'.
This script does NOT push. When Michael approves the flip, force-push manually:

    git push origin --force --all
    git push origin --force --tags

Roll back at any time before the push with:

    git reset --hard $BACKUP

EOF
    [ "$AFTER" = "0" ] && exit 0 || exit 1
    ;;

  *)
    echo "usage: bash scripts/scrub-history.sh [verify|execute]" >&2
    exit 2
    ;;
esac
