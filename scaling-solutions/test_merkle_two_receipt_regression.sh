#!/usr/bin/env bash
# REVIEW-ONLY: execute the actual Merkle section from the checked-out verify.sh.
# Synthetic receipts deliberately bypass receipt hashes/signatures (separate HOLD).
# No chain, wallets, signing keys, historical roots, or network interactions.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
need() { command -v "$1" >/dev/null 2>&1 || { echo "missing $1"; exit 1; }; }
need jq
need python3
need awk

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/_truth"
STATE="$TMP/_truth/state.json"

# Extract the production Merkle block verbatim. Never maintain a second copy
# of its hashing implementation in this regression.
awk '
  /^# 6\) Merkle root integrity$/ { copying=1 }
  copying { print }
  copying && /^echo "OK: verify passed"$/ { found_end=1; exit }
  END { if (!found_end) exit 1 }
' "$ROOT/verify.sh" > "$TMP/merkle_block.sh"

cat > "$TMP/preamble.sh" <<'PREAMBLE'
#!/usr/bin/env bash
set -euo pipefail
STATE="$(cd "$(dirname "$0")" && pwd)/_truth/state.json"
PREAMBLE
cat "$TMP/preamble.sh" "$TMP/merkle_block.sh" > "$TMP/production_merkle.sh"
chmod +x "$TMP/production_merkle.sh"

# Fixture: exactly two synthetic, 32-byte prehashed leaves. This hard-coded
# root was independently checked in Wolfram and is NOT computed using the
# implementation under test.
LEAF1=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
LEAF2=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
REFERENCE=e2d80f78d79027556d6619a1400605abbdca6bb6eb24e0831e33ecd5466fa5f6

set_state() {
  python3 - "$STATE" "$LEAF1" "$LEAF2" "$1" <<'PY'
import json, sys
from pathlib import Path
root = None if sys.argv[4] == "__NULL__" else sys.argv[4]
Path(sys.argv[1]).write_text(json.dumps({
    "receipts": [{"receipt_hash": sys.argv[2]}, {"receipt_hash": sys.argv[3]}],
    "last_merkle_root": root,
}), encoding="utf-8")
PY
}

run_code() {
  local script="$1"
  set +e
  bash "$script" > "$TMP/output.log" 2>&1
  LAST_RC=$?
  set -e
}

# Required regression: the CURRENT PRODUCTION BLOCK rejects a null root.
set_state __NULL__
run_code "$TMP/production_merkle.sh"
if (( LAST_RC == 0 )) || ! grep -q 'merkle root mismatch' "$TMP/output.log"; then
  echo 'FAIL: production Merkle block did not reject two leaves + null root'
  cat "$TMP/output.log"
  exit 1
fi
echo 'PASS: production rejects two leaves + null root'

# Required regression: the CURRENT PRODUCTION BLOCK accepts the known root.
set_state "$REFERENCE"
run_code "$TMP/production_merkle.sh"
if (( LAST_RC != 0 )) || ! grep -q 'OK: verify passed' "$TMP/output.log"; then
  echo 'FAIL: production Merkle block rejected the verified two-leaf root'
  cat "$TMP/output.log"
  exit 1
fi
echo 'PASS: production accepts independent two-leaf reference root'

# Mutation/negative control: deliberately restore the historical stdin/heredoc
# bug IN A TEMPORARY EXTRACT ONLY. A good regression MUST detect it.
python3 - "$TMP/merkle_block.sh" "$TMP/merkle_block_mutant.sh" <<'PY'
from pathlib import Path
import sys
s = Path(sys.argv[1]).read_text(encoding='utf-8')
begin = "| python3 -c '"
end = "\n')\nstate_root="
if s.count(begin) != 1 or s.count(end) != 1:
    raise SystemExit('HOLD: mutation fixture cannot identify exact current input block')
s = s.replace(begin, "| python3 - <<'PY'", 1).replace(end, "\nPY\n)\nstate_root=", 1)
Path(sys.argv[2]).write_text(s, encoding='utf-8')
PY
cat "$TMP/preamble.sh" "$TMP/merkle_block_mutant.sh" > "$TMP/mutant.sh"
set_state __NULL__
run_code "$TMP/mutant.sh"
if (( LAST_RC != 0 )); then
  echo 'FAIL: heredoc mutant did not reproduce original null-root false green'
  cat "$TMP/output.log"
  exit 1
fi
set_state "$REFERENCE"
run_code "$TMP/mutant.sh"
if (( LAST_RC == 0 )); then
  echo 'FAIL: heredoc mutant unexpectedly accepted correct nonempty root'
  cat "$TMP/output.log"
  exit 1
fi
echo 'PASS: heredoc reversion mutant exposed (false green and false red)'
echo 'OK: production-bound two-receipt Merkle regression and mutation guard passed'
