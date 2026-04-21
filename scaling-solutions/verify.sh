#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE="$ROOT/_truth/state.json"
INV="$ROOT/os/agent_inventory.json"

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing $1"; exit 1; }; }
need jq
need sha256sum

# 1) JSON validity
jq -e . "$STATE" >/dev/null
jq -e . "$INV" >/dev/null

# 2) Policy checks: treasury cap <= 25
jq -e '.agents.treasury[] | select(.cap_usd > 25) | halt_error(1)' "$INV" || true
if jq -e '.agents.treasury[] | select(.cap_usd > 25)' "$INV" >/dev/null; then
  echo "treasury cap violation (>25)"; exit 1
fi

# 3) Agents list in state must match inventory ids (set equality)
inv_ids=$(jq -r '.agents | to_entries[] | .value[]?.id' "$INV" | sort -u)
state_ids=$(jq -r '.agents[]?' "$STATE" | sort -u)
if [[ "$inv_ids" != "$state_ids" ]]; then
  echo "agent set mismatch between state and inventory"; exit 1
fi

# 4) Receipt hash integrity
# Recompute receipt_hash for each receipt and compare
jq -c '.receipts[]?' "$STATE" | while read -r r; do
  # remove receipt_hash field then recompute
  canon=$(echo "$r" | jq 'del(.receipt_hash)' | jq -cS .)
  calc=$(printf "%s" "$canon" | sha256sum | awk '{print $1}')
  given=$(echo "$r" | jq -r '.receipt_hash')
  if [[ "$calc" != "$given" ]]; then
    echo "receipt hash mismatch"; exit 1
  fi
done

# 5) Merkle root integrity
# Build leaf list and recompute merkle root via python one-liner
leafs=$(jq -r '.receipts[]?.receipt_hash' "$STATE")
calc_root=$(python3 - << 'PY'
import hashlib, sys
leaves=[l.strip() for l in sys.stdin if l.strip()]
if not leaves:
  print("")
  raise SystemExit(0)
level=[bytes.fromhex(x) for x in leaves]
while len(level)>1:
  if len(level)%2==1:
    level.append(level[-1])
  nxt=[]
  for i in range(0,len(level),2):
    nxt.append(hashlib.sha256(level[i]+level[i+1]).digest())
  level=nxt
print(level[0].hex())
PY
)
state_root=$(jq -r '.last_merkle_root // ""' "$STATE")
if [[ "$calc_root" != "$state_root" ]]; then
  echo "merkle root mismatch"; exit 1
fi

echo "OK: verify passed"
