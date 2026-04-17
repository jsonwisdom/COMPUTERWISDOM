#!/usr/bin/env bash
# 🔵🔨 BLUEHAMMER v1.3 - THE WATCHER CORE
set -euo pipefail

LEAF_PATH="${1:?leaf path required}"
RULES_PATH="royal-design-chess/rules/moves.json"

echo "--------------------------------------------------"
echo "🔵🔨 WATCHER_BOT: Auditing [$LEAF_PATH]"

# 0. Preconditions
if [[ ! -f "$RULES_PATH" ]]; then
  echo "❌ ERROR: rules file not found at $RULES_PATH" >&2
  exit 1
fi

# 1. Integrity Check
if [[ ! -f "$LEAF_PATH" ]]; then
  echo "❌ ERROR: Leaf file not found." >&2
  exit 1
fi

# 2. Syntax Check
if ! jq empty "$LEAF_PATH" >/dev/null 2>&1; then
  echo "❌ ERROR: Invalid JSON syntax in $LEAF_PATH." >&2
  exit 1
fi

# 3. Rule Identification
MOVE_ID=$(jq -r '.move_id // empty' "$LEAF_PATH")
if [[ -z "$MOVE_ID" ]]; then
  echo "❌ ERROR: move_id missing in leaf." >&2
  exit 1
fi

echo "♟️  Detected Move: $MOVE_ID"

# 4. Mandatory Field Validation
if ! jq -e ".moves.$MOVE_ID" "$RULES_PATH" >/dev/null 2>&1; then
  echo "❌ ERROR: Move [$MOVE_ID] not found in rules/moves.json." >&2
  exit 1
fi

mapfile -t REQUIRED_FIELDS < <(jq -r ".moves.$MOVE_ID.required_fields[]?" "$RULES_PATH")
FAIL_ID=$(jq -r ".moves.$MOVE_ID.fail_state.id // \"UNKNOWN_FAIL\"" "$RULES_PATH")

if [[ ${#REQUIRED_FIELDS[@]} -eq 0 ]]; then
  echo "❌ ERROR: No required_fields defined for move [$MOVE_ID]." >&2
  exit 1
fi

for FIELD in "${REQUIRED_FIELDS[@]}"; do
  VAL=$(jq -r ".$FIELD // empty" "$LEAF_PATH")
  if [[ -z "$VAL" ]]; then
    echo "❌ AUDIT_FAIL: [$FAIL_ID] detected." >&2
    echo "   Missing required field: $FIELD" >&2
    exit 1
  fi
done

echo "✅ SUCCESS: Move [$MOVE_ID] is legally sound."
echo "--------------------------------------------------"
exit 0
