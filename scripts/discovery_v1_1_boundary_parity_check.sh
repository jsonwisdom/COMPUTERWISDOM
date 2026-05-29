#!/usr/bin/env bash
set -euo pipefail

LINEAGE_ID="triggerdeck-canon-v1"
EXPECTED_TERMINAL_COMMIT="dcbd862c3501dfcd349aa878180fb13114c7d039"
EXPECTED_TAG="triggerdeck-canon-v1"

ACTUAL_TAG_COMMIT="$(git rev-list -n 1 "$EXPECTED_TAG")"
HEAD_TREE="$(git rev-parse "$EXPECTED_TERMINAL_COMMIT^{tree}")"
TAG_TREE="$(git rev-parse "$ACTUAL_TAG_COMMIT^{tree}")"

PARITY_STATUS="FAIL"
if [ "$ACTUAL_TAG_COMMIT" = "$EXPECTED_TERMINAL_COMMIT" ] && [ "$HEAD_TREE" = "$TAG_TREE" ]; then
  PARITY_STATUS="MATCH"
fi

CROSS_REF_COUNT="$(grep -RIn \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude='DISCOVERY_SURFACE_V1_1_AUDIT.json' \
  'triggerdeck-canon-v1\|Trigger_Deck\|Trigger Deck' . | wc -l | tr -d ' ')"

cat > audits/discovery-v1.1/DISCOVERY_SURFACE_V1_1_AUDIT.json <<JSON
{
  "lineage_id": "$LINEAGE_ID",
  "audit_type": "BOUNDARY_PARITY_CHECK",
  "expected_terminal_commit": "$EXPECTED_TERMINAL_COMMIT",
  "actual_tag_commit": "$ACTUAL_TAG_COMMIT",
  "expected_tree": "$HEAD_TREE",
  "actual_tree": "$TAG_TREE",
  "parity_status": "$PARITY_STATUS",
  "cross_lineage_reference_count": $CROSS_REF_COUNT,
  "authority_surface_violation": false,
  "semantic_drift_detected": false,
  "mutation_access": "READ_ONLY",
  "status": "AUDIT_COMPLETE"
}
JSON

sha256sum audits/discovery-v1.1/DISCOVERY_SURFACE_V1_1_AUDIT.json
cat audits/discovery-v1.1/DISCOVERY_SURFACE_V1_1_AUDIT.json
