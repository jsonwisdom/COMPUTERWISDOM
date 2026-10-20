#!/usr/bin/env bash
# Commit DOJ CWA receipts. Two modes:
#   normal  stage receipts/doj-cwa/ and push (script succeeded; HOLD is a normal result)
#   crash   commit ONLY receipts/doj-cwa/crash/, regardless of anything already
#           staged, modified, or committed locally earlier in the job.
set -euo pipefail

MODE="${1:?usage: doj-cwa-commit.sh normal|crash}"
DIR="receipts/doj-cwa"
BR="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

case "$MODE" in
  normal)
    git add -- "$DIR/"
    if git diff --cached --quiet; then
      echo "No changes to commit."
    else
      git commit -q -m "chore(doj-cwa): rule check receipt [skip ci]"
      git push origin "HEAD:$BR"
    fi
    ;;
  crash)
    # 1. Set crash receipts aside; reset --hard would delete staged-new files.
    KEEP="$(mktemp -d)"
    if [ -d "$DIR/crash" ]; then cp -a "$DIR/crash/." "$KEEP/" 2>/dev/null || true; fi
    # 2. Return the tree to the remote tip: drops staged/modified baselines and
    #    any unpushed local commit made earlier in this job.
    git fetch -q origin "$BR"
    git reset -q --hard "origin/$BR"
    # 3. Restore only the crash receipts.
    mkdir -p "$DIR/crash"
    if [ -n "$(ls -A "$KEEP" 2>/dev/null)" ]; then cp -an "$KEEP"/. "$DIR/crash/"; fi
    rm -rf "$KEEP"
    git add -- "$DIR/crash/"
    STAGED="$(git diff --cached --name-only)"
    if [ -z "$STAGED" ]; then echo "No crash receipt to commit."; exit 0; fi
    if printf '%s\n' "$STAGED" | grep -qv "^$DIR/crash/"; then
      echo "refusing to commit: unexpected staged files:" >&2; printf '%s\n' "$STAGED" >&2
      git reset -q; exit 1
    fi
    git commit -q -m "chore(doj-cwa): crash receipt [skip ci]" -- "$DIR/crash/"
    git push origin "HEAD:$BR"
    ;;
  *) echo "unknown mode: $MODE" >&2; exit 2 ;;
esac
