#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-config.example.json}"
OUT_ROOT="${OUT_ROOT:-dumps}"
DATE_STAMP="$(date -u +%Y-%m-%d)"
RUN_DIR="$OUT_ROOT/$DATE_STAMP"

mkdir -p "$RUN_DIR"

if [ ! -f "$CONFIG" ]; then
  echo "missing config: $CONFIG" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "missing dependency: jq" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "missing dependency: gh" >&2
  echo "install GitHub CLI or export dumps manually" >&2
  exit 1
fi

cp "$CONFIG" "$RUN_DIR/config.snapshot.json"

jq -r '.repositories[]' "$CONFIG" | while read -r REPO; do
  SAFE_REPO="${REPO//\//__}"
  REPO_DIR="$RUN_DIR/$SAFE_REPO"
  mkdir -p "$REPO_DIR"

  echo "collecting $REPO"

  gh repo view "$REPO" --json name,owner,defaultBranchRef,isPrivate,url,pushedAt,createdAt,updatedAt > "$REPO_DIR/repo.json"
  gh pr list --repo "$REPO" --state all --limit 100 --json number,title,state,isDraft,mergeable,reviewDecision,headRefName,baseRefName,updatedAt,createdAt,author,url > "$REPO_DIR/prs.json"

  jq -r '.[].number' "$REPO_DIR/prs.json" | while read -r PR; do
    gh pr view "$PR" --repo "$REPO" --json number,title,state,isDraft,mergeable,reviewDecision,headRefName,baseRefName,commits,files,comments,reviews,statusCheckRollup,url > "$REPO_DIR/pr_${PR}.json"
  done

done

jq -n \
  --arg service "COMPUTER_WISDOM_AS_A_SERVICE" \
  --arg mode "READ_ONLY_COLLECTION" \
  --arg date "$DATE_STAMP" \
  --arg run_dir "$RUN_DIR" \
  '{service:$service,mode:$mode,date:$date,run_dir:$run_dir,mutation_allowed:false,authority:false,no_fake_green:true}' > "$RUN_DIR/run_receipt.json"

echo "CWaaS collection complete: $RUN_DIR"
