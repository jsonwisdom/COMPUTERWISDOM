#!/usr/bin/env bash
set -euo pipefail

ASSET_PATH="${1:-}"
TICKET_ID="${2:-SUPPORT-JW-001}"
ENTRY_ID="${3:-CWAAS-FLYWHEEL-001}"

if [ -z "$ASSET_PATH" ] || [ ! -f "$ASSET_PATH" ]; then
  echo "ERROR: asset file required"
  echo "Usage: $0 path/to/cutscene.png [ticket_id] [entry_id]"
  exit 1
fi

if [ -z "${PINATA_JWT:-}" ]; then
  echo "ERROR: PINATA_JWT not set"
  exit 1
fi

ASSET_NAME="$(basename "$ASSET_PATH")"
ASSET_SHA="$(sha256sum "$ASSET_PATH" | awk '{print $1}')"

echo "== OPTION D ASSET HASH =="
echo "$ASSET_SHA  $ASSET_PATH"

UPLOAD_RESPONSE="$(curl -sS --request POST \
  --url https://api.pinata.cloud/pinning/pinFileToIPFS \
  --header "Authorization: Bearer ${PINATA_JWT}" \
  --form "file=@${ASSET_PATH}" \
  --form "pinataMetadata={\"name\":\"${ASSET_NAME}\"}" \
  --form 'pinataOptions={"cidVersion":1}')"

ASSET_CID="$(echo "$UPLOAD_RESPONSE" | jq -r '.IpfsHash // empty')"

if [ -z "$ASSET_CID" ]; then
  echo "ERROR: pin failed"
  echo "$UPLOAD_RESPONSE"
  exit 1
fi

META_PATH="metadata/zora/CWAAS_FLYWHEEL_ENTRY_001_SUPPORT_JW_MASTER_GREEN.metadata.json"

cat > "$META_PATH" <<META
{
  "name": "SUPPORT-JW-001 MASTER_GREEN — Desk Dungeon Boss Cutscene",
  "description": "Computer Wisdom as a Service Option D visual replay artifact for SUPPORT-JW-001. The receipt is proof. The image is presentation. The replay is memory.",
  "image": "ipfs://${ASSET_CID}",
  "external_url": "https://github.com/jsonwisdom/COMPUTERWISDOM/pull/335",
  "cwaas_ticket_id": "${TICKET_ID}",
  "entry_id": "${ENTRY_ID}",
  "attributes": [
    { "trait_type": "Engine", "value": "CWaaS" },
    { "trait_type": "Quest Tier", "value": "D_FULL_SEND_VISUAL_REPLAY" },
    { "trait_type": "Technician", "value": "Jay Wisdom" },
    { "trait_type": "State", "value": "PR_GREEN_PENDING_MASTER_VERIFY" },
    { "trait_type": "No Fake Green", "value": "true" }
  ],
  "properties": {
    "authority": false,
    "no_fake_green": true,
    "asset_filename": "${ASSET_NAME}",
    "asset_sha256": "${ASSET_SHA}",
    "asset_ipfs_uri": "ipfs://${ASSET_CID}"
  }
}
META

META_SHA="$(sha256sum "$META_PATH" | awk '{print $1}')"

echo "== OPTION D BIND RESULT =="
echo "ASSET_URI=ipfs://${ASSET_CID}"
echo "ASSET_SHA256=${ASSET_SHA}"
echo "METADATA_PATH=${META_PATH}"
echo "METADATA_SHA256=${META_SHA}"
echo "NO_FAKE_GREEN=true"
