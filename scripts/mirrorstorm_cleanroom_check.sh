#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="mirrorstorm-genesis-v0"

MATCHES="$(grep -RIn \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  'Trigger_Deck\|Trigger Deck\|triggerdeck-canon-v1\|dcbd862c3501dfcd349aa878180fb13114c7d039' \
  "$TARGET_DIR" 2>/dev/null || true)"

STATUS="PASS"
if [ -n "$MATCHES" ]; then
  STATUS="FAIL"
fi

ROOT_HASH="$(tar --sort=name \
  --mtime='UTC 2026-01-01' \
  --owner=0 --group=0 --numeric-owner \
  -cf - "$TARGET_DIR" 2>/dev/null | sha256sum | cut -d' ' -f1)"

cat > audits/mirrorstorm/MIRRORSTORM_GENESIS_AUDIT.json <<JSON
{
  "lineage_root": "MIRRORSTORM-GENESIS-00",
  "audit_type": "CLEANROOM_ISOLATION_CHECK",
  "triggerdeck_residue_detected": $( [ "$STATUS" = "FAIL" ] && echo true || echo false ),
  "cleanroom_status": "$STATUS",
  "root_hash": "$ROOT_HASH",
  "registry_link": "MLR-CORE-001",
  "deploy_policy": "NO_PATCHING_TO_CANON"
}
JSON

sha256sum audits/mirrorstorm/MIRRORSTORM_GENESIS_AUDIT.json
cat audits/mirrorstorm/MIRRORSTORM_GENESIS_AUDIT.json
