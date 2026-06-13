#!/usr/bin/env bash
set -euo pipefail

CONFIG="${1:-config.example.json}"
OUT_ROOT="${OUT_ROOT:-dumps}"
STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DATE_STAMP="$(date -u +%Y-%m-%d)"
RUN_ID="${RUN_ID:-$DATE_STAMP}"
RUN_DIR="$OUT_ROOT/$RUN_ID"

mkdir -p "$RUN_DIR"

write_manifest_state() {
  local state="$1"
  local reason="${2:-}"
  local now
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  jq -n \
    --arg service "COMPUTER_WISDOM_AS_A_SERVICE" \
    --arg mode "READ_ONLY_COLLECTION" \
    --arg state "$state" \
    --arg reason "$reason" \
    --arg started_at "$STARTED_AT" \
    --arg updated_at "$now" \
    --arg run_id "$RUN_ID" \
    --arg run_dir "$RUN_DIR" \
    '{service:$service,mode:$mode,posture_state:$state,reason:$reason,started_at:$started_at,updated_at:$updated_at,run_id:$run_id,run_dir:$run_dir,mutation_allowed:false,outputs_are_candidates_until_replayed:true,authority:false,no_fake_green:true}' > "$RUN_DIR/run_manifest.json"
}

fail_with_state() {
  local state="$1"
  local reason="$2"
  write_manifest_state "$state" "$reason"
  echo "$reason" >&2
  exit 1
}

if [ ! -f "$CONFIG" ]; then
  fail_with_state "BLOCKED" "missing config: $CONFIG"
fi

if ! command -v jq >/dev/null 2>&1; then
  fail_with_state "BLOCKED" "missing dependency: jq"
fi

if ! command -v gh >/dev/null 2>&1; then
  fail_with_state "BLOCKED" "missing dependency: gh"
fi

cp "$CONFIG" "$RUN_DIR/config.snapshot.json"

if ! jq -e '.repositories and (.repositories | type == "array") and (.repositories | length > 0)' "$CONFIG" >/dev/null; then
  fail_with_state "BLOCKED" "config requires non-empty repositories array"
fi

write_manifest_state "COLLECTION_RUNNING" "collection started"

jq -r '.repositories[]' "$CONFIG" | while read -r REPO; do
  SAFE_REPO="${REPO//\//__}"
  REPO_DIR="$RUN_DIR/$SAFE_REPO"
  mkdir -p "$REPO_DIR"

  echo "collecting $REPO"

  if ! gh repo view "$REPO" --json name,owner,defaultBranchRef,isPrivate,url,pushedAt,createdAt,updatedAt > "$REPO_DIR/repo.json"; then
    fail_with_state "FAILED" "gh repo view failed for $REPO"
  fi

  if ! gh pr list --repo "$REPO" --state all --limit 100 --json number,title,state,isDraft,mergeable,reviewDecision,headRefName,baseRefName,updatedAt,createdAt,author,url > "$REPO_DIR/prs.json"; then
    fail_with_state "FAILED" "gh pr list failed for $REPO"
  fi

  jq -r '.[].number' "$REPO_DIR/prs.json" | while read -r PR; do
    if ! gh pr view "$PR" --repo "$REPO" --json number,title,state,isDraft,mergeable,reviewDecision,headRefName,baseRefName,commits,files,comments,reviews,statusCheckRollup,url > "$REPO_DIR/pr_${PR}.json"; then
      fail_with_state "FAILED" "gh pr view failed for $REPO PR $PR"
    fi
  done
done

COMPLETED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

jq \
  --arg completed_at "$COMPLETED_AT" \
  '.posture_state="DUMPS_PRESERVED" | .reason="collection completed" | .completed_at=$completed_at | .updated_at=$completed_at' \
  "$RUN_DIR/run_manifest.json" > "$RUN_DIR/run_manifest.tmp.json"
mv "$RUN_DIR/run_manifest.tmp.json" "$RUN_DIR/run_manifest.json"

if [ ! -f "$RUN_DIR/run_manifest.json" ]; then
  fail_with_state "MISSING_RECEIPT" "run_manifest.json missing after collection"
fi

jq -n \
  --arg service "COMPUTER_WISDOM_AS_A_SERVICE" \
  --arg mode "READ_ONLY_COLLECTION" \
  --arg run_id "$RUN_ID" \
  --arg run_dir "$RUN_DIR" \
  --arg completed_at "$COMPLETED_AT" \
  '{service:$service,mode:$mode,run_id:$run_id,run_dir:$run_dir,completed_at:$completed_at,posture_state:"DUMPS_PRESERVED",mutation_allowed:false,outputs_are_candidates_until_replayed:true,authority:false,no_fake_green:true}' > "$RUN_DIR/run_receipt.json"

if [ ! -f "$RUN_DIR/run_receipt.json" ]; then
  fail_with_state "MISSING_RECEIPT" "run_receipt.json missing after collection"
fi

echo "CWaaS collection complete: $RUN_DIR"
