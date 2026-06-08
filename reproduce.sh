#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# RECEIPT_STACK_2026-06-08 verifier
#
# Verdicts:
#   REALITY_CONFIRMED
#   TOPOLOGY_VIOLATION
#   PROHIBITED
#   INCOMPLETE_CHAIN
# ---------------------------------------------------------------------------

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MANIFEST="${MANIFEST:-${ROOT_DIR}/manifest.json}"
DERIVATIVE_MAP="${DERIVATIVE_MAP:-${ROOT_DIR}/derivative_map.json}"
STACK_MD="${STACK_MD:-${ROOT_DIR}/RECEIPT_STACK_2026-06-08.md}"
DIGEST_PROC="${DIGEST_PROC:-sha256sum}"
CACHE_DIR="${CACHE_DIR:-${ROOT_DIR}/.receipt-cache}"

PAS_ID="FED-AI-2026-PAS-001"
PAS_EXPECTED_SHA256="6246b253637baa349d61e9d6d8ac89ce4943e1d4ef16adba47be49106e48f3d1"
PAS_REMOTE_URL="${PAS_REMOTE_URL:-https://raw.githubusercontent.com/jsonwisdom/AL/master/docs/proof_at_scale/PROOF_AT_SCALE_v0.1.md}"
PAS_CACHE_PATH="${PAS_CACHE_PATH:-${CACHE_DIR}/${PAS_ID}}"

fail() {
  local verdict="$1"
  local msg="${2:-}"
  if [[ -n "$msg" ]]; then echo "$msg" >&2; fi
  echo "VERDICT: ${verdict}"
  exit 1
}

require_file() {
  local path="$1"
  local label="$2"
  [[ -f "$path" ]] || fail "INCOMPLETE_CHAIN" "Missing ${label}: ${path}"
}

jq_safe() { jq "$@" 2>/dev/null || return 1; }

fetch_pas_anchor() {
  mkdir -p "$CACHE_DIR"
  if [[ ! -f "$PAS_CACHE_PATH" ]]; then
    if command -v curl >/dev/null 2>&1; then
      curl -fsSL "$PAS_REMOTE_URL" -o "$PAS_CACHE_PATH" || fail "INCOMPLETE_CHAIN" "Unable to fetch PAS-001 anchor from ${PAS_REMOTE_URL}"
    elif command -v wget >/dev/null 2>&1; then
      wget -qO "$PAS_CACHE_PATH" "$PAS_REMOTE_URL" || fail "INCOMPLETE_CHAIN" "Unable to fetch PAS-001 anchor from ${PAS_REMOTE_URL}"
    else
      fail "INCOMPLETE_CHAIN" "Neither curl nor wget available to retrieve PAS-001 anchor."
    fi
  fi
}

require_file "$MANIFEST" "manifest"
require_file "$DERIVATIVE_MAP" "derivative_map"
require_file "$STACK_MD" "receipt_stack"
fetch_pas_anchor

SOURCE_ARTIFACT="${SOURCE_ARTIFACT:-$PAS_CACHE_PATH}"
[[ -f "$SOURCE_ARTIFACT" ]] || fail "INCOMPLETE_CHAIN" "Source artifact not found: ${SOURCE_ARTIFACT}"

check_invariants() {
  local d1 d2
  d1="$($DIGEST_PROC "$SOURCE_ARTIFACT" | awk '{print $1}')"
  d2="$($DIGEST_PROC "$SOURCE_ARTIFACT" | awk '{print $1}')"
  [[ "$d1" == "$d2" ]] || { echo "Invariant 001 failed: non-deterministic digest." >&2; return 1; }

  local count
  count="$(jq_safe --arg p "$PAS_ID" '[.files[] | select(.path == $p)] | length' "$MANIFEST" || echo "0")"
  [[ "$count" -eq 1 ]] || { echo "Invariant 002 failed: expected exactly one manifest entry for ${PAS_ID}, got ${count}." >&2; return 1; }

  local orphan_receipts
  orphan_receipts="$(jq_safe -n --slurpfile dm "$DERIVATIVE_MAP" --slurpfile mf "$MANIFEST" '
    $dm[0].receipts[]? as $r
    | select([ $mf[0].files[].digest ] | index($r.digest) | not)
    | $r.id
  ' 2>/dev/null || true)"
  [[ -z "$orphan_receipts" ]] || { echo "Invariant 004 failed: orphan receipts:" >&2; echo "$orphan_receipts" >&2; return 1; }

  local orphan_derivatives
  orphan_derivatives="$(jq_safe '.derivatives[]? as $d | select((.sources // []) | length == 0) | $d.id' "$DERIVATIVE_MAP" 2>/dev/null || true)"
  [[ -z "$orphan_derivatives" ]] || { echo "Invariant 005 failed: derivatives without sources:" >&2; echo "$orphan_derivatives" >&2; return 1; }

  for gov in "$PAS_ID" "RECEIPT_STACK_2026-06-08.md" "anti-time-travel.md" "derivative-receipt-spec.md" "stranger-replay.md"; do
    local c
    c="$(jq_safe --arg p "$gov" '[.files[] | select(.path == $p)] | length' "$MANIFEST" || echo "0")"
    [[ "$c" -ne 0 ]] || { echo "Invariant 006 failed: governance file missing from manifest: ${gov}" >&2; return 1; }
  done

  return 0
}

check_temporal_rules() {
  local stack_ts bad_receipts pas_ts bad_pas_claims
  stack_ts="$(jq_safe -r '.files[] | select(.path == "RECEIPT_STACK_2026-06-08.md") | .timestamp // empty' "$MANIFEST" 2>/dev/null || true)"
  if [[ -n "$stack_ts" ]]; then
    bad_receipts="$(jq_safe --arg st "$stack_ts" '.receipts[]? | select(.timestamp < $st) | .id' "$DERIVATIVE_MAP" 2>/dev/null || true)"
    [[ -z "$bad_receipts" ]] || { echo "Rule T-001 failed: receipts predating governing stack timestamp:" >&2; echo "$bad_receipts" >&2; return 1; }
  fi

  pas_ts="$(jq_safe -r '.files[] | select(.path == "FED-AI-2026-PAS-001") | .timestamp // empty' "$MANIFEST" 2>/dev/null || true)"
  if [[ -n "$pas_ts" ]]; then
    bad_pas_claims="$(jq_safe --arg pt "$pas_ts" '.receipts[]? | select(.context == "PAS-001" and .timestamp < $pt) | .id' "$DERIVATIVE_MAP" 2>/dev/null || true)"
    [[ -z "$bad_pas_claims" ]] || { echo "Rule T-004 failed: receipts claiming PAS-001 before PAS-001 timestamp:" >&2; echo "$bad_pas_claims" >&2; return 1; }
  fi

  return 0
}

check_clauses() {
  [[ -s "$STACK_MD" ]] || { echo "Clause C-002 failed: receipt stack file is empty or unreadable." >&2; return 1; }

  local governance_paths
  governance_paths="$(jq_safe -r '.files[] | select(.type == "governance" and (.external // false | not)) | .path' "$MANIFEST" 2>/dev/null || true)"
  if [[ -n "$governance_paths" ]]; then
    while IFS= read -r path; do
      [[ -z "$path" ]] && continue
      [[ -f "$ROOT_DIR/$path" ]] || { echo "Clause C-003 failed: governance file listed in manifest not present in repo: ${path}" >&2; return 1; }
    done <<< "$governance_paths"
  fi

  local missing_lineage
  missing_lineage="$(jq_safe '.derivatives[]? | select((.sources // []) | length == 0) | .id' "$DERIVATIVE_MAP" 2>/dev/null || true)"
  [[ -z "$missing_lineage" ]] || { echo "Clause C-005 failed: derivative without explicit sources:" >&2; echo "$missing_lineage" >&2; return 1; }

  return 0
}

check_pas_digest() {
  local manifest_digest pas_digest
  manifest_digest="$(jq_safe -r '.files[] | select(.path == "FED-AI-2026-PAS-001") | .digest' "$MANIFEST" 2>/dev/null | head -n1 || true)"
  [[ -n "$manifest_digest" ]] || { echo "PAS-001 digest check failed: FED-AI-2026-PAS-001 not listed in manifest." >&2; return 1; }
  [[ "$manifest_digest" == "$PAS_EXPECTED_SHA256" ]] || { echo "PAS-001 manifest digest mismatch." >&2; return 1; }

  pas_digest="$($DIGEST_PROC "$PAS_CACHE_PATH" | awk '{print $1}')"
  if [[ "$pas_digest" != "$PAS_EXPECTED_SHA256" ]]; then
    echo "PAS-001 digest mismatch:" >&2
    echo "  expected: ${PAS_EXPECTED_SHA256}" >&2
    echo "  actual:   ${pas_digest}" >&2
    return 1
  fi

  return 0
}

check_invariants || fail "TOPOLOGY_VIOLATION"
check_temporal_rules || fail "PROHIBITED"
check_clauses || fail "PROHIBITED"
check_pas_digest || fail "TOPOLOGY_VIOLATION"

echo "VERDICT: REALITY_CONFIRMED"
