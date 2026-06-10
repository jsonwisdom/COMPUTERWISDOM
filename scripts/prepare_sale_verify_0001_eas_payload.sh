#!/usr/bin/env bash
set -euo pipefail
SALE_FILE="receipts/sales/SALE_VERIFY_0001.canonical.json"
ENVELOPE="anchors/sales/SALE_VERIFY_0001_ANCHOR_ENVELOPE.candidate.json"
OUT="anchors/sales/SALE_VERIFY_0001_EAS_PAYLOAD.candidate.json"
SALE_SHA="$(sha256sum "$SALE_FILE" | cut -d' ' -f1)"
ENVELOPE_SHA="$(sha256sum "$ENVELOPE" | cut -d' ' -f1)"
ROUTER_COMMIT="$(git rev-parse HEAD)"
cat > "$OUT" <<JSON
{
  "payload_type": "EAS_ATTESTATION_CANDIDATE",
  "sale_id": "SALE-VERIFY-0001",
  "sku": "verification_pack",
  "sale_receipt_sha256": "$SALE_SHA",
  "anchor_envelope_sha256": "$ENVELOPE_SHA",
  "router_commit": "$ROUTER_COMMIT",
  "identity": "jaywisdom.base.eth",
  "payment_status": "NOT_ROUTED",
  "attestation_status": "PENDING_REAL_EAS_UID",
  "zora_status": "PENDING_REAL_ZORA_ID",
  "claim_boundary": "candidate only; not anchored until real EAS UID or Zora ID is recorded"
}
JSON
sha256sum "$OUT"
cat "$OUT"
