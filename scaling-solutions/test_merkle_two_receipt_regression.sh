#!/usr/bin/env bash
# Synthetic two-receipt Merkle regression for verify.sh
# Essential assertion:
#   - two valid leaves + null last_merkle_root → FAIL
#   - two valid leaves + correctly computed root → PASS
# Tree rule is the script's own duplicate-last construction.
# Receipt-hash and signature checks are skipped in this harness
# because the circular preimage remains under HOLD; this test
# isolates the Merkle input path only.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing $1"; exit 1; }; }
need jq
need python3

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/_truth" "$TMP/os"
cp os/agent_inventory.json "$TMP/os/"

# Local verify that keeps policy/agent checks and the Merkle block,
# but skips receipt-hash and signature integrity (HOLD items).
cat > "$TMP/verify_merkle_only.sh" << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE="$ROOT/_truth/state.json"
INV="$ROOT/os/agent_inventory.json"
need() { command -v "$1" >/dev/null 2>&1 || { echo "missing $1"; exit 1; }; }
need jq
need python3
jq -e . "$STATE" >/dev/null
jq -e . "$INV" >/dev/null
# agent set equality (same as original)
inv_ids=$(jq -r '.agents | to_entries[] | .value[]?.id' "$INV" | sort -u)
state_ids=$(jq -r '.agents[]?' "$STATE" | sort -u)
if [[ "$inv_ids" != "$state_ids" ]]; then
  echo "agent set mismatch"; exit 1
fi
# Merkle block (identical to current verify.sh)
leafs=$(jq -r '.receipts[]?.receipt_hash' "$STATE")
calc_root=$(printf "%s\n" "$leafs" | python3 -c '
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
')
state_root=$(jq -r '.last_merkle_root // ""' "$STATE")
if [[ "$calc_root" != "$state_root" ]]; then
  echo "merkle root mismatch"; exit 1
fi
echo "OK: verify passed"
EOF
chmod +x "$TMP/verify_merkle_only.sh"

# Two known leaves
LEAF1=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
LEAF2=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb

# Correct root (duplicate-last, same algorithm)
CORRECT=$(printf "%s\n%s\n" "$LEAF1" "$LEAF2" | python3 -c '
import hashlib, sys
leaves=[l.strip() for l in sys.stdin if l.strip()]
level=[bytes.fromhex(x) for x in leaves]
while len(level)>1:
  if len(level)%2==1:
    level.append(level[-1])
  nxt=[]
  for i in range(0,len(level),2):
    nxt.append(hashlib.sha256(level[i]+level[i+1]).digest())
  level=nxt
print(level[0].hex())
')
echo "correct_root=$CORRECT"

# Base state with two receipts (hashes only; other fields unused by Merkle path)
python3 - << PY
import json
from pathlib import Path
tmp = Path("$TMP")
state = {
  "agents": [
    "audit.os.jaywisdom.eth",
    "mcp.os.jaywisdom.eth",
    "sentiment.os.jaywisdom.eth",
    "treasury-01.os.jaywisdom.eth",
    "treasury-02.os.jaywisdom.eth",
    "treasury-03.os.jaywisdom.eth"
  ],
  "receipts": [
    {"receipt_hash": "$LEAF1"},
    {"receipt_hash": "$LEAF2"}
  ],
  "last_merkle_root": None
}
(tmp / "_truth" / "state.json").write_text(json.dumps(state, indent=2))
PY

# --- null root must fail ---
echo "=== null root must fail ==="
set +e
(cd "$TMP" && ./verify_merkle_only.sh)
rc=$?
set -e
if [[ $rc -eq 0 ]]; then
  echo "FAIL: null root was accepted"
  exit 1
fi
echo "PASS: null root rejected (rc=$rc)"

# --- correct root must pass ---
python3 - << PY
import json
from pathlib import Path
tmp = Path("$TMP")
state = json.loads((tmp / "_truth" / "state.json").read_text())
state["last_merkle_root"] = "$CORRECT"
(tmp / "_truth" / "state.json").write_text(json.dumps(state, indent=2))
PY

echo "=== correct root must pass ==="
(cd "$TMP" && ./verify_merkle_only.sh)
echo "PASS: correct root accepted"

echo "OK: two-receipt Merkle regression passed"
