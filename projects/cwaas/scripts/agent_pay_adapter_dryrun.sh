#!/bin/bash
set -e

# CWaaS Agent Pay — Payment Adapter Dry-Run
# Status: TEMPLATE_ONLY / DRY_RUN
# Doctrine: no external calls, no signing, no funds moved, no settlement claim.

printf '%s\n' "CWaaS Agent Pay — Adapter Dry-Run"
printf '%s\n' "Status: PREVIEW_ONLY -> HUMAN_APPROVED_PENDING_EXECUTION (dry-run)"

PREVIEW_PATH="projects/cwaas/receipts/preview-dispatch/PREVIEW_1_V2.json"
APPROVAL_PATH="projects/cwaas/receipts/agent-pay/APPROVAL_0001.json"
PAYLOAD_PATH="projects/cwaas/agent-pay/AGENT_PAY_PAYMENT_PAYLOAD_0001.json"
OUT_DIR="projects/cwaas/receipts/agent-pay/dryrun"
OUT_PATH="$OUT_DIR/AGENT_PAY_ADAPTER_DRYRUN_0001.json"

mkdir -p "$OUT_DIR"

# Validate prerequisites. This script intentionally stops if any receipt is missing.
if [ ! -f "$PREVIEW_PATH" ]; then
  echo "BLOCKED: preview receipt missing: $PREVIEW_PATH"
  exit 1
fi

if [ ! -f "$APPROVAL_PATH" ]; then
  echo "BLOCKED: approval receipt missing: $APPROVAL_PATH"
  exit 1
fi

if [ ! -f "$PAYLOAD_PATH" ]; then
  echo "BLOCKED: payment payload missing: $PAYLOAD_PATH"
  exit 1
fi

PREVIEW_HASH=$(sha256sum "$PREVIEW_PATH" | awk '{print $1}')
APPROVAL_HASH=$(sha256sum "$APPROVAL_PATH" | awk '{print $1}')
PAYLOAD_HASH=$(sha256sum "$PAYLOAD_PATH" | awk '{print $1}')
TIMESTAMP_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat > "$OUT_PATH" <<EOF
{
  "receipt_type": "AGENT_PAY_ADAPTER_DRYRUN_RECEIPT_V1",
  "mode": "DRY_RUN",
  "status": "APPROVED_PENDING_EXECUTION_DRYRUN_ONLY",
  "adapter": "coinbase-mcp-v1",
  "network": "base-mainnet",
  "asset": "USDC",
  "preview_receipt": {
    "path": "$PREVIEW_PATH",
    "hash": "$PREVIEW_HASH"
  },
  "approval_receipt": {
    "path": "$APPROVAL_PATH",
    "hash": "$APPROVAL_HASH"
  },
  "payment_payload": {
    "path": "$PAYLOAD_PATH",
    "hash": "$PAYLOAD_HASH"
  },
  "external_action": false,
  "payment_executed": false,
  "chain_action": false,
  "adapter_called": false,
  "funds_moved": false,
  "settlement_claimed": false,
  "timestamp_utc": "$TIMESTAMP_UTC",
  "notes": [
    "This is a dry-run preview.",
    "No payment executed.",
    "No external adapter call made.",
    "No Base transaction created.",
    "No funds moved.",
    "No settlement authority implied."
  ]
}
EOF

DRYRUN_HASH=$(sha256sum "$OUT_PATH" | awk '{print $1}')

echo "DRYRUN_RECEIPT=$OUT_PATH"
echo "DRYRUN_HASH=$DRYRUN_HASH"
echo "external_action=false"
echo "payment_executed=false"
echo "chain_action=false"
echo "adapter_called=false"
echo "funds_moved=false"
echo "settlement_claimed=false"
echo "No transaction witness, no confirmed payment."
echo "No dry-run proof, no real adapter."
echo "No fake green."
