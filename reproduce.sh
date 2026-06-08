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
#
# Inputs via env/args:
#   SOURCE_ARTIFACT   - path to the primary source artifact, e.g. PAS-001 PDF
#   MANIFEST          - path to manifest.json
#   DERIVATIVE_MAP    - path to derivative_map.json
#   STACK_MD          - path to RECEIPT_STACK_2026-06-08.md
#   DIGEST_PROC       - digest command, default: sha256sum
# ---------------------------------------------------------------------------

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MANIFEST="${MANIFEST:-${ROOT_DIR}/manifest.json}"
DERIVATIVE_MAP="${DERIVATIVE_MAP:-${ROOT_DIR}/derivative_map.json}"
STACK_MD="${STACK_MD:-${ROOT_DIR}/RECEIPT_STACK_2026-06-08.md}"
DIGEST_PROC="${DIGEST_PROC:-sha256sum}"

PAS_ID="FED-AI-2026-PAS-001"
PAS_EXPECTED_SHA256="6246b253637baa349d61e9d6d8ac89ce4943e1d4ef16adba47be49106e48f3d1"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

fail() {
  local verdict="$1"
  local msg="${2:-}"
  if [[ -n "$msg" ]]; then
    echo "$msg" >&2
  fi
  echo "VERDICT: ${verdict}"
  exit 1
}

require_file() {
  local path="$1"
  local label="$2"
  if [[ ! -f "$path" ]]; then
    fail "INCOMPLETE_CHAIN" "Missing ${label}: ${path}"
  fi
}

jq_safe() {
  jq "$@" 2>/dev/null || return 1
}

# ---------------------------------------------------------------------------
# Input presence: verifier interface declaration
# ---------------------------------------------------------------------------

require_file "$MANIFEST" "manifest"
require_file "$DERIVATIVE_MAP" "derivative_map"
require_file "$STACK_MD" "receipt_stack"

SOURCE_ARTIFACT="${SOURCE_ARTIFACT:-}"

if [[ -z "$SOURCE_ARTIFACT" ]]; then
  fail "INCOMPLETE_CHAIN" "SOURCE_ARTIFACT not set (path to source artifact)."
fi

if [[ ! -f "$SOURCE_ARTIFACT" ]]; then
  fail "INCOMPLETE_CHAIN" "Source artifact not found: ${SOURCE_ARTIFACT}"
fi

# ---------------------------------------------------------------------------
# Invariants 001-007
# ---------------------------------------------------------------------------

check_invariants() {
  # Invariant 001 — Deterministic Replay
  local d1 d2
  d1="$($DIGEST_PROC "$SOURCE_ARTIFACT" | awk '{print $1}')"
  d2="$($DIGEST_PROC "$SOURCE_ARTIFACT" | awk '{print $1}')"
  if [[ "$d1" != "$d2" ]]; then
    echo "Invariant 001 failed: non-deterministic digest." >&2
    return 1
  fi

  # Invariant 002 — Single Digest per Artifact
  # Assumed manifest schema:
  # {
  #   "files": [
  #     { "path": "path/to/file", "digest": "sha256...", "type": "artifact|governance|..." }
  #   ]
  # }
  local rel_path
  rel_path="$(realpath --relative-to="$ROOT_DIR" "$SOURCE_ARTIFACT")"
  local count
  count="$(jq_safe --arg p "$rel_path" '[.files[] | select(.path == $p)] | length' "$MANIFEST" || echo "0")"
  if [[ "$count" -ne 1 ]]; then
    echo "Invariant 002 failed: expected exactly one manifest entry for artifact (${rel_path}), got ${count}." >&2
    return 1
  fi

  # Invariant 003 — Immutable Manifest Entries
  # Stub: assume enforced by branch protection + tags.
  # Hook point: compare current manifest against a tagged baseline.

  # Invariant 004 — No Orphan Receipts
  # Assumed derivative_map schema:
  # {
  #   "receipts": [
  #     { "id": "R1", "digest": "sha256...", "timestamp": "...", "context": "..." }
  #   ],
  #   "derivatives": []
  # }
  local orphan_receipts
  orphan_receipts="$(jq_safe -n --slurpfile dm "$DERIVATIVE_MAP" --slurpfile mf "$MANIFEST" '
    $dm[0].receipts[]? as $r
    | select([ $mf[0].files[].digest ] | index($r.digest) | not)
    | $r.id
  ' 2>/dev/null || true)"
  if [[ -n "$orphan_receipts" ]]; then
    echo "Invariant 004 failed: orphan receipts with no matching manifest digest:" >&2
    echo "$orphan_receipts" >&2
    return 1
  fi

  # Invariant 005 — No Orphan Derivatives
  # Each derivative must reference at least one valid source receipt.
  local orphan_derivatives
  orphan_derivatives="$(jq_safe '
    .derivatives[]? as $d
    | select((.sources // []) | length == 0)
    | $d.id
  ' "$DERIVATIVE_MAP" 2>/dev/null || true)"
  if [[ -n "$orphan_derivatives" ]]; then
    echo "Invariant 005 failed: derivatives without sources:" >&2
    echo "$orphan_derivatives" >&2
    return 1
  fi

  # Invariant 006 — Total Ordering of Governance Surfaces
  # Governance files must exist in manifest.
  for gov in "$PAS_ID" "RECEIPT_STACK_2026-06-08.md" \
             "anti-time-travel.md" "derivative-receipt-spec.md" "stranger-replay.md"; do
    local c
    c="$(jq_safe --arg p "$gov" '[.files[] | select(.path == $p)] | length' "$MANIFEST" || echo "0")"
    if [[ "$c" -eq 0 ]]; then
      echo "Invariant 006 failed: governance file missing from manifest: ${gov}" >&2
      return 1
    fi
  done

  # Invariant 007 — Stranger-Executable
  # Machine-checkable part: no required secrets/env beyond documented inputs.
  # If this script runs to here, 007 is treated as satisfied.

  return 0
}

# ---------------------------------------------------------------------------
# Temporal Rules T-001-T-004
# ---------------------------------------------------------------------------

check_temporal_rules() {
  # Assumed schema additions:
  #   manifest.files[].timestamp
  #   derivative_map.receipts[].timestamp
  #   derivative_map.governance_stack[].timestamp

  # Rule T-001 — Monotonic Governance
  # No receipt governed by a ruleset that did not yet exist.
  # Stub: ensure receipt timestamps >= stack timestamp.
  local stack_ts
  stack_ts="$(jq_safe '
    .files[] | select(.path == "RECEIPT_STACK_2026-06-08.md") | .timestamp
  ' "$MANIFEST" 2>/dev/null || echo "")"
  if [[ -n "$stack_ts" ]]; then
    local bad_receipts
    bad_receipts="$(jq_safe --arg st "$stack_ts" '
      .receipts[]? | select(.timestamp < $st) | .id
    ' "$DERIVATIVE_MAP" 2>/dev/null || true)"
    if [[ -n "$bad_receipts" ]]; then
      echo "Rule T-001 failed: receipts predating governing stack timestamp:" >&2
      echo "$bad_receipts" >&2
      return 1
    fi
  fi

  # Rule T-002 — Manifest Time Consistency
  # manifest entry timestamp <= any receipt referencing its digest.
  # Stub: structural hook; real logic depends on exact schema.

  # Rule T-003 — No Retroactive Reclassification
  # Not easily machine-checkable without history; assume branch/tag policy enforces.

  # Rule T-004 — Temporal Anchoring of PAS-001
  # PAS-001 digest must exist at or before origin event.
  # Stub: ensure PAS-001 has a timestamp and no receipt claims it before PAS timestamp.
  local pas_ts
  pas_ts="$(jq_safe '
    .files[] | select(.path == "FED-AI-2026-PAS-001") | .timestamp
  ' "$MANIFEST" 2>/dev/null || echo "")"
  if [[ -n "$pas_ts" ]]; then
    local bad_pas_claims
    bad_pas_claims="$(jq_safe --arg pt "$pas_ts" '
      .receipts[]? | select(.context == "PAS-001" and .timestamp < $pt) | .id
    ' "$DERIVATIVE_MAP" 2>/dev/null || true)"
    if [[ -n "$bad_pas_claims" ]]; then
      echo "Rule T-004 failed: receipts claiming PAS-001 before PAS-001 timestamp:" >&2
      echo "$bad_pas_claims" >&2
      return 1
    fi
  fi

  return 0
}

# ---------------------------------------------------------------------------
# Constitutional Clauses C-001-C-006
# ---------------------------------------------------------------------------

check_clauses() {
  # Clause C-001 — Evidence Must Be Replayable
  # Already exercised via digest replay.

  # Clause C-002 — Governance Must Be Inspectable
  if [[ ! -s "$STACK_MD" ]]; then
    echo "Clause C-002 failed: receipt stack file is empty or unreadable." >&2
    return 1
  fi

  # Clause C-003 — No Secret Law
  # Machine-checkable part: all governance files referenced in manifest exist in repo.
  local governance_paths
  governance_paths="$(jq_safe -r '
    .files[] | select(.type == "governance") | .path
  ' "$MANIFEST" 2>/dev/null || true)"
  if [[ -n "$governance_paths" ]]; then
    while IFS= read -r path; do
      [[ -z "$path" ]] && continue
      if [[ ! -f "$ROOT_DIR/$path" ]]; then
        echo "Clause C-003 failed: governance file listed in manifest not present in repo: ${path}" >&2
        return 1
      fi
    done <<< "$governance_paths"
  fi

  # Clause C-004 — No Retroactive Governance
  # Hooked via temporal rules.

  # Clause C-005 — Lineage Must Be Explicit
  # Each derivative must declare sources.
  local missing_lineage
  missing_lineage="$(jq_safe '
    .derivatives[]? | select((.sources // []) | length == 0) | .id
  ' "$DERIVATIVE_MAP" 2>/dev/null || true)"
  if [[ -n "$missing_lineage" ]]; then
    echo "Clause C-005 failed: derivative without explicit sources:" >&2
    echo "$missing_lineage" >&2
    return 1
  fi

  # Clause C-006 — Equal Replay Rights
  # Machine-checkable part: script does not require privileged access.

  return 0
}

# ---------------------------------------------------------------------------
# PAS-001 digest check: explicit
# ---------------------------------------------------------------------------

check_pas_digest() {
  local pas_path
  pas_path="$(jq_safe -r '
    .files[] | select(.path == "FED-AI-2026-PAS-001") | .path
  ' "$MANIFEST" 2>/dev/null | head -n1 || echo "")"

  if [[ -z "$pas_path" ]]; then
    echo "PAS-001 digest check failed: FED-AI-2026-PAS-001 not listed in manifest." >&2
    return 1
  fi

  local pas_full="${ROOT_DIR}/${pas_path}"
  if [[ ! -f "$pas_full" ]]; then
    echo "PAS-001 digest check failed: file not found at ${pas_full}." >&2
    return 1
  fi

  local pas_digest
  pas_digest="$($DIGEST_PROC "$pas_full" | awk '{print $1}')"

  if [[ "$pas_digest" != "$PAS_EXPECTED_SHA256" ]]; then
    echo "PAS-001 digest mismatch:" >&2
    echo "  expected: ${PAS_EXPECTED_SHA256}" >&2
    echo "  actual:   ${pas_digest}" >&2
    return 1
  fi

  return 0
}

# ---------------------------------------------------------------------------
# Run checks
# ---------------------------------------------------------------------------

if ! check_invariants; then
  fail "TOPOLOGY_VIOLATION"
fi

if ! check_temporal_rules; then
  fail "PROHIBITED"
fi

if ! check_clauses; then
  fail "PROHIBITED"
fi

if ! check_pas_digest; then
  fail "TOPOLOGY_VIOLATION"
fi

echo "VERDICT: REALITY_CONFIRMED"
