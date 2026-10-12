#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="$ROOT/tools/base-bootstrap/receipt_validator.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

python3 - "$TMP/valid.json" <<'PY'
import hashlib, json, sys
p=sys.argv[1]
r={
 "schema_version":"1.0.0",
 "receipt_id":"",
 "timestamp":"2026-08-23T12:00:00Z",
 "operation":{"action":"check","chain":"base-sepolia","env_name":"base-sepolia"},
 "inputs":{"address":"0x"+"a"*40,"calldata":"0x1234","value_wei":"0"},
 "outputs":{"balance_wei":"0","resolved_address":"0x"+"b"*40,"simulation_success":True,"tx_hash":"0x"+"c"*64},
 "execution":{"exit_code":0,"duration_ms":150,"tool_versions":{"python":"3.x"}},
 "integrity":{"content_hash":"","previous_receipt_hash":None},
 "authority":{"authority_created":False}
}
pre=json.loads(json.dumps(r))
pre.pop("receipt_id")
pre["integrity"].pop("content_hash")
h=hashlib.sha256(json.dumps(pre,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
r["receipt_id"]=h
r["integrity"]["content_hash"]=h
open(p,"w",encoding="utf-8").write(json.dumps(r,separators=(",",":")))
PY

python3 "$VALIDATOR" "$TMP/valid.json" >/dev/null || exit 1
python3 -O "$VALIDATOR" "$TMP/valid.json" >/dev/null || exit 1

python3 - "$TMP/valid.json" "$TMP/missing.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r.pop("execution")
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/missing.json" >/dev/null 2>&1 && exit 1

python3 - "$TMP/valid.json" "$TMP/bad-action.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["operation"]["action"]="destroy"
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/bad-action.json" >/dev/null 2>&1 && exit 1

python3 - "$TMP/valid.json" "$TMP/bad-chain.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["operation"]["chain"]="ethereum-mainnet"
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/bad-chain.json" >/dev/null 2>&1 && exit 1

python3 - "$TMP/valid.json" "$TMP/bad-content-hash.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["integrity"]["content_hash"]="0"*64
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
OUT="$(python3 "$VALIDATOR" "$TMP/bad-content-hash.json" 2>&1)"; RC=$?
[[ $RC -ne 0 ]] || exit 1
printf '%s\n' "$OUT" | grep -q CONTENT_HASH_MISMATCH || exit 1

python3 - "$TMP/valid.json" "$TMP/bad-receipt-id.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["receipt_id"]="0"*64
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
OUT="$(python3 "$VALIDATOR" "$TMP/bad-receipt-id.json" 2>&1)"; RC=$?
[[ $RC -ne 0 ]] || exit 1
printf '%s\n' "$OUT" | grep -q RECEIPT_ID_MISMATCH || exit 1

python3 - "$TMP/valid.json" "$TMP/tampered.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["operation"]["action"]="read"
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
OUT="$(python3 "$VALIDATOR" "$TMP/tampered.json" 2>&1)"; RC=$?
[[ $RC -ne 0 ]] || exit 1
printf '%s\n' "$OUT" | grep -q CONTENT_HASH_MISMATCH || exit 1

python3 - "$TMP/valid.json" "$TMP/unknown.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["rogue_field"]=1
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/unknown.json" >/dev/null 2>&1 && exit 1

python3 - "$TMP/valid.json" "$TMP/authority.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["authority"]["authority_created"]=True
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/authority.json" >/dev/null 2>&1 && exit 1

python3 - "$TMP/valid.json" "$TMP/bad-address.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["inputs"]["address"]="0x1234"
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/bad-address.json" >/dev/null 2>&1 && exit 1

python3 - "$TMP/valid.json" "$TMP/unknown-input.json" <<'PY'
import json,sys
r=json.load(open(sys.argv[1],encoding="utf-8")); r["inputs"]["unknown_input"]="x"
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),separators=(",",":"))
PY
python3 "$VALIDATOR" "$TMP/unknown-input.json" >/dev/null 2>&1 && exit 1

echo "PASS: All corrected Gate 3 receipt schema tests passed."
