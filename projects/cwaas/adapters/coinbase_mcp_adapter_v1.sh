#!/usr/bin/env bash
set -euo pipefail

# coinbase_mcp_adapter_v1.sh
# Status: DRY_RUN_ONLY
# Doctrine: preview-first, receipt-first, human-gated, no fake green.
# This harness does not move funds and does not perform chain actions.

MODE="${1:-dry-run}"
RECEIPTS_DIR="${RECEIPTS_DIR:-receipts/cwaas/agent-pay/coinbase-mcp}"
IDENTITY_BINDING="${IDENTITY_BINDING:-JAYWISDOM.eth}"
ASSET="${ASSET:-USDC}"
NETWORK="${NETWORK:-base-mainnet}"
AMOUNT="${AMOUNT:-0.00}"
WORK_REFERENCE="${WORK_REFERENCE:-unset}"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
SAFE_TS="$(date -u +%Y%m%d-%H%M%S)"

mkdir -p "$RECEIPTS_DIR"

case "$MODE" in
  dry-run|preview)
    ;;
  *)
    echo "ERROR: unsupported mode: $MODE" >&2
    echo "Allowed modes: dry-run, preview" >&2
    exit 64
    ;;
esac

PREVIEW_RECEIPT="$RECEIPTS_DIR/coinbase_mcp_preview_${SAFE_TS}.json"
APPROVAL_STUB="$RECEIPTS_DIR/coinbase_mcp_approval_required_${SAFE_TS}.json"

cat > "$PREVIEW_RECEIPT" <<EOF
{
  "receipt_type": "COINBASE_MCP_ADAPTER_PREVIEW_V1",
  "adapter": "coinbase-mcp-v1",
  "mode": "$MODE",
  "dry_run_only": true,
  "funds_moved": false,
  "chain_action": false,
  "identity_binding": "$IDENTITY_BINDING",
  "payment_payload": {
    "asset": "$ASSET",
    "network": "$NETWORK",
    "amount": "$AMOUNT",
    "work_reference": "$WORK_REFERENCE"
  },
  "required_gate": "human_approval",
  "created_at": "$TS"
}
EOF

sha256sum "$PREVIEW_RECEIPT" > "$PREVIEW_RECEIPT.sha256"
PREVIEW_HASH="$(cut -d ' ' -f1 "$PREVIEW_RECEIPT.sha256")"

cat > "$APPROVAL_STUB" <<EOF
{
  "receipt_type": "COINBASE_MCP_APPROVAL_REQUIRED_V1",
  "adapter": "coinbase-mcp-v1",
  "preview_receipt": "$PREVIEW_RECEIPT",
  "preview_hash": "$PREVIEW_HASH",
  "approved": false,
  "approval_route": "/approve-agent-pay",
  "status": "BLOCKED_PENDING_HUMAN_APPROVAL",
  "created_at": "$TS"
}
EOF

sha256sum "$APPROVAL_STUB" > "$APPROVAL_STUB.sha256"

echo "COINBASE_MCP_ADAPTER_V1_DRY_RUN_COMPLETE"
echo "preview_receipt=$PREVIEW_RECEIPT"
echo "preview_hash=$PREVIEW_HASH"
echo "approval_required=$APPROVAL_STUB"
echo "funds_moved=false"
echo "chain_action=false"
