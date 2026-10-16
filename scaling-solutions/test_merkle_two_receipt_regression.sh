#!/usr/bin/env bash
# Synthetic two-receipt Merkle regression for verify.sh
# Essential assertion:
#   - two valid leaves + null last_merkle_root → FAIL
#   - two valid leaves + correctly computed root → PASS
# Tree rule is the script's own duplicate-last construction.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing $1"; exit 1; }; }
need jq
need sha256sum
need python3

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Build a minimal workspace that verify.sh can run against
mkdir -p "$TMP/_truth" "$TMP/os"
cp verify.sh "$TMP/"
cp os/signer.py "$TMP/os/"
cp os/agent_inventory.json "$TMP/os/"

# Generate two receipts with correct hashes and local ed25519 signatures
python3 - << PY
import json, hashlib, sys
from pathlib import Path
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

tmp = Path("$TMP")

# Simple receipt bodies (fields other than receipt_hash and signature)
def make_receipt(idx: int, sk: SigningKey) -> dict:
    body = {
        "agent_id": "audit.os.jaywisdom.eth",
        "idx": idx,
        "payload": f"synthetic-{idx}"
    }
    canon = json.dumps(body, sort_keys=True, separators=(",", ":"))
    receipt_hash = hashlib.sha256(canon.encode()).hexdigest()
    sig = sk.sign(receipt_hash.encode()).signature.hex()
    pub = sk.verify_key.encode(encoder=HexEncoder).decode()
    return {
        **body,
        "receipt_hash": receipt_hash,
        "signature": {
            "signing_scheme": "ed25519",
            "signer": "os.jaywisdom.eth",
            "public_key": pub,
            "signature": sig
        }
    }

sk = SigningKey.generate()
r1 = make_receipt(1, sk)
r2 = make_receipt(2, sk)

# Compute Merkle root with the same duplicate-last rule
leaves = [bytes.fromhex(r["receipt_hash"]) for r in (r1, r2)]
level = leaves[:]
while len(level) > 1:
    if len(level) % 2 == 1:
        level.append(level[-1])
    nxt = []
    for i in range(0, len(level), 2):
        nxt.append(hashlib.sha256(level[i] + level[i+1]).digest())
    level = nxt
correct_root = level[0].hex()

base_state = {
    "agents": [
        "audit.os.jaywisdom.eth",
        "mcp.os.jaywisdom.eth",
        "sentiment.os.jaywisdom.eth",
        "treasury-01.os.jaywisdom.eth",
        "treasury-02.os.jaywisdom.eth",
        "treasury-03.os.jaywisdom.eth"
    ],
    "anchor_status": None,
    "gateway": "app.jaywisdom.eth",
    "identity_root": "os.jaywisdom.eth",
    "last_anchor_tx": None,
    "last_updated": None,
    "owner_ens": "jaywisdom.base.eth",
    "policy": {
        "default_max_spend_per_agent_usd": 25,
        "human_approval_required_for_first_live_trade": True,
        "kms_required": True,
        "merkle_batching": True,
        "receipts_required": True
    },
    "receipts": [r1, r2],
    "settlement": "jaywisdom.base.eth",
    "system": "scaling-solutions",
    "vault": "data.jaywisdom.eth",
    "version": "0.1.0"
}

# Null-root case
null_state = {**base_state, "last_merkle_root": None}
(tmp / "_truth" / "state.json").write_text(json.dumps(null_state, indent=2))
(tmp / "expected_null_fail").write_text("1")

# Correct-root case will be written later
(tmp / "correct_root.txt").write_text(correct_root)
print(f"correct_root={correct_root}")
PY

# --- Assertion 1: null root must fail ---
echo "=== null root must fail ==="
set +e
(cd "$TMP" && ./verify.sh)
rc=$?
set -e
if [[ $rc -eq 0 ]]; then
  echo "FAIL: null root was accepted"
  exit 1
fi
echo "PASS: null root rejected (rc=$rc)"

# --- Assertion 2: correct root must pass ---
CORRECT=$(cat "$TMP/correct_root.txt")
python3 - << PY
import json
from pathlib import Path
tmp = Path("$TMP")
state = json.loads((tmp / "_truth" / "state.json").read_text())
state["last_merkle_root"] = "$CORRECT"
(tmp / "_truth" / "state.json").write_text(json.dumps(state, indent=2))
PY

echo "=== correct root must pass ==="
(cd "$TMP" && ./verify.sh)
echo "PASS: correct root accepted"

echo "OK: two-receipt Merkle regression passed"
