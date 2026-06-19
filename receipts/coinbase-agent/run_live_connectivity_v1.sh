#!/usr/bin/env bash
set -euo pipefail

# Receipt Engine V1 - Live Coinbase CLI/MCP connectivity
# Doctrine: NO_FAKE_GREEN, deterministic hashes, replayable failure/success receipts.
# Safety: product read only. No order preview. No execution. No trade.

RECEIPTS_DIR="receipts/coinbase-agent"
TS="$(date -u +%Y%m%d-%H%M%S)"

mkdir -p "$RECEIPTS_DIR"

OUT="$RECEIPTS_DIR/connectivity_products_btc_usd_${TS}.json"
HASH="$RECEIPTS_DIR/connectivity_products_btc_usd_${TS}.sha256"

printf '%s\n' "== Coinbase live connectivity v1 =="
printf 'timestamp=%s\n' "$TS"
printf '%s\n' "execution=false"
printf '%s\n' "trade=false"

set +e
coinbase products get BTC-USD | tee "$OUT"
CODE=${PIPESTATUS[0]}
set -e

sha256sum "$OUT" | tee "$HASH"
BYTES=$(wc -c < "$OUT")

if [ "$CODE" -ne 0 ] || [ "$BYTES" -eq 0 ]; then
  cat > "$RECEIPTS_DIR/CONNECTIVITY_STATUS.md" <<STATUS
# Coinbase MCP Connectivity Status

Status: BLOCKED_OR_EMPTY
Exit code: $CODE
JSON bytes: $BYTES
Execution occurred: false
Trade occurred: false
Live treasury data accessed: false
No fake green: active
First live receipt: not observed
STATUS
  printf '%s\n' "FAIL: BLOCKED_OR_EMPTY_RECEIPTED"
  exit 1
fi

cp "$OUT" "$RECEIPTS_DIR/connectivity_products_btc_usd.json"
sha256sum "$RECEIPTS_DIR/connectivity_products_btc_usd.json" | tee "$RECEIPTS_DIR/connectivity_products_btc_usd.sha256"

cp "$OUT" "$RECEIPTS_DIR/event_001_attestation.json"
sha256sum "$RECEIPTS_DIR/event_001_attestation.json" | tee "$RECEIPTS_DIR/event_001_attestation.sha256"

cat > "$RECEIPTS_DIR/CONNECTIVITY_STATUS.md" <<STATUS
# Coinbase MCP Connectivity Status

Status: CONNECTIVITY_LIVE_RECEIPTED
JSON bytes: $BYTES
Execution occurred: false
Trade occurred: false
Live treasury data accessed: false
No fake green: active
First live receipt: observed
STATUS

printf '%s\n' "PASS: FIRST_LIVE_CONNECTIVITY_RECEIPT"
