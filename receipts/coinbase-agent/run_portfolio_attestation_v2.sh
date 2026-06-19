#!/usr/bin/env bash
set -euo pipefail

RECEIPTS_DIR="receipts/coinbase-agent"
TS="$(date -u +%Y%m%d-%H%M%S)"
mkdir -p "$RECEIPTS_DIR"

PORTFOLIOS_OUT="$RECEIPTS_DIR/event_002_portfolios_${TS}.json"
BALANCE_OUT="$RECEIPTS_DIR/event_002_balance_${TS}.json"

echo "== Coinbase Portfolio Read-Only Attestation V2 =="
echo "timestamp=$TS"
echo "execution=false"
echo "trade=false"
echo "preview=false"

set +e
coinbase portfolios list | tee "$PORTFOLIOS_OUT"
CODE1=${PIPESTATUS[0]}

coinbase balance | tee "$BALANCE_OUT"
CODE2=${PIPESTATUS[0]}
set -e

sha256sum "$PORTFOLIOS_OUT" | tee "$PORTFOLIOS_OUT.sha256"
sha256sum "$BALANCE_OUT" | tee "$BALANCE_OUT.sha256"

P_BYTES=$(wc -c < "$PORTFOLIOS_OUT")
B_BYTES=$(wc -c < "$BALANCE_OUT")

if [ "$CODE1" -ne 0 ] || [ "$CODE2" -ne 0 ] || [ "$P_BYTES" -eq 0 ] || [ "$B_BYTES" -eq 0 ]; then
  cat > "$RECEIPTS_DIR/PORTFOLIO_STATUS.md" <<STATUS
# Coinbase Portfolio Attestation Status

Status: PORTFOLIO_READ_BLOCKED_OR_EMPTY
Portfolio exit code: $CODE1
Balance exit code: $CODE2
Portfolio bytes: $P_BYTES
Balance bytes: $B_BYTES
Execution occurred: false
Trade occurred: false
Preview occurred: false
No fake green: active
STATUS
  echo "FAIL: PORTFOLIO_READ_BLOCKED_OR_EMPTY_RECEIPTED"
  exit 1
fi

cp "$PORTFOLIOS_OUT" "$RECEIPTS_DIR/event_002_portfolios.json"
cp "$BALANCE_OUT" "$RECEIPTS_DIR/event_002_balance.json"

sha256sum "$RECEIPTS_DIR/event_002_portfolios.json" | tee "$RECEIPTS_DIR/event_002_portfolios.sha256"
sha256sum "$RECEIPTS_DIR/event_002_balance.json" | tee "$RECEIPTS_DIR/event_002_balance.sha256"

cat > "$RECEIPTS_DIR/PORTFOLIO_STATUS.md" <<STATUS
# Coinbase Portfolio Attestation Status

Status: PORTFOLIO_READ_ATTESTED
Portfolio bytes: $P_BYTES
Balance bytes: $B_BYTES
Execution occurred: false
Trade occurred: false
Preview occurred: false
Treasury custody attested: read-only observation only
No fake green: active
TREASURY_GATE_V2: PORTFOLIO_READ_ATTESTED
STATUS

echo "PASS: PORTFOLIO_READ_ATTESTED"
