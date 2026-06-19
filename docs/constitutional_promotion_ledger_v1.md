# CONSTITUTIONAL_PROMOTION_LEDGER_V1

Authority: false  
Purpose: Track every artifact promotion across `DOCUMENTED_ONLY`, `IMPLEMENTED`, `VERIFIED`, `DEPLOYED`, and `ANCHORED`  
Invariant: Every promotion must be reconstructable from receipts alone

---

## Promotion State Machine

```txt
DOCUMENTED_ONLY --[DOC_RECEIPT + SCHEMA_RECEIPT/CODE_RECEIPT]--> IMPLEMENTED
IMPLEMENTED     --[TEST_RECEIPT + CI_RECEIPT]------------------> VERIFIED
VERIFIED        --[DEPLOYMENT_RECEIPT]--------------------------> DEPLOYED
ANY_STATE       --[ANCHOR_RECEIPT]------------------------------> ANCHORED_MODIFIER
ANY_STATE       --[DEMOTION_RECEIPT]----------------------------> PRIOR_STATUS
```

Rules:

- `ANCHORED` is a modifier, not a replacement for implementation status.
- A document committed to Git is `DOCUMENTED_ONLY` unless it is itself a schema or code artifact with applicable receipt.
- Fake receipt hashes are not valid receipts.
- No artifact may promote without a receipt recorded in `CONSTITUTIONAL_RECEIPT_LEDGER_V1` or a future CI/deployment artifact.

---

## 1. Promotion Registry

### Current State Summary

| artifact_id | artifact_name | current_status | anchor_modifier | receipt_basis | authority |
|---|---|---|---|---|---|
| ADN-001 | REPLAY_ENGINE_SPEC_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-002 | UI_WIREFRAME_SPEC_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-003 | OPEN_SOURCE_REPLAY_CLIENT_SPEC_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-004 | CONSISTENCY_CONSTITUTIONAL_BUILD_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-005 | REPLAY_ANOMALY_SCHEMA_V1 | IMPLEMENTED | false | git schema receipt | false |
| ADN-006 | INTERNAL_DRIFT_ALERT_RESPONSE_PROTOCOL_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-007 | CONSTITUTIONAL_INDEX_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-008 | REPO_CONSTITUTIONAL_GRAPH_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-009 | DISCOVERY_PATH_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-010 | README_CONSTITUTIONAL_DISCOVERY_ENTRY | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-011 | CONSTITUTIONAL_RECEIPT_LEDGER_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-012 | CONSTITUTIONAL_STATUS_DASHBOARD_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-013 | PR202_CLOSEOUT_REPORT_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-014 | CONSTITUTIONAL_IMPLEMENTATION_GAP_REPORT_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-015 | CONSTITUTIONAL_BUILD_QUEUE_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-016 | CONSTITUTIONAL_EXECUTION_PLAN_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |
| ADN-017 | CONSTITUTIONAL_RECEIPT_REQUIREMENTS_V1 | DOCUMENTED_ONLY | false | git doc receipt | false |

### Promotion Registry Table

| promotion_id | artifact_id | previous_status | new_status | receipt_types | receipt_hashes | issued_by | issued_at | authority |
|---|---|---|---|---|---|---|---|---|
| P-001 | ADN-005 | DOCUMENTED_ONLY | IMPLEMENTED | DOC_RECEIPT, SCHEMA_RECEIPT | `a0c6da10c8fe27b9e036f61afb6b5e0b0dd97fc7` | repo commit | 2026-06-02 | false |

No other artifact is promoted beyond `DOCUMENTED_ONLY` in this ledger until implementation, test, CI, deployment, or anchor receipts exist.

---

## 2. Promotion Event Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Constitutional Promotion Event V1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "promotion_id",
    "artifact_id",
    "artifact_name",
    "previous_status",
    "new_status",
    "receipt_types",
    "receipt_hashes",
    "issued_by",
    "issued_at",
    "authority"
  ],
  "properties": {
    "promotion_id": { "type": "string", "pattern": "^[PD]-[0-9]{3}$" },
    "artifact_id": { "type": "string", "pattern": "^ADN-[0-9]{3}$" },
    "artifact_name": { "type": "string", "minLength": 1 },
    "previous_status": {
      "type": "string",
      "enum": ["NONE", "DOCUMENTED_ONLY", "IMPLEMENTED", "VERIFIED", "DEPLOYED"]
    },
    "new_status": {
      "type": "string",
      "enum": ["DOCUMENTED_ONLY", "IMPLEMENTED", "VERIFIED", "DEPLOYED"]
    },
    "anchor_modifier": { "type": "boolean", "default": false },
    "receipt_types": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "enum": [
          "DOC_RECEIPT",
          "SCHEMA_RECEIPT",
          "CODE_RECEIPT",
          "TEST_RECEIPT",
          "CI_RECEIPT",
          "DEPLOYMENT_RECEIPT",
          "ANCHOR_RECEIPT",
          "DEMOTION_RECEIPT"
        ]
      }
    },
    "receipt_hashes": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string", "minLength": 1 }
    },
    "issued_by": { "type": "string", "minLength": 1 },
    "issued_at": { "type": "string", "format": "date-time" },
    "authority": { "type": "boolean", "const": false },
    "evidence_links": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

---

## 3. Promotion History Rules

### 3.1 Immutability

- Once recorded, a promotion event cannot be deleted.
- Corrections require a demotion event followed by a new promotion.
- History must be append-only.

### 3.2 Receipt Binding

- Every promotion must reference at least one receipt hash.
- Receipt hash must be verifiable against `CONSTITUTIONAL_RECEIPT_LEDGER_V1`, CI artifacts, deployment logs, or cross-repo anchor receipts.
- Receipt must predate or equal promotion timestamp.

### 3.3 Sequential Ordering

- `DOCUMENTED_ONLY` cannot skip to `VERIFIED`.
- `IMPLEMENTED` cannot skip to `DEPLOYED`.
- `VERIFIED` requires both test and CI evidence.

### 3.4 Authority Verification

- Every promotion event must have `authority:false`.
- A receipt may describe verification, but it does not create authority.
- Self-issued final verification is invalid without independent receipt.

---

## 4. Demotion Rules

| Reason | Required Receipt | Effect |
|---|---|---|
| schema validation failure | DEMOTION_RECEIPT + SCHEMA_FAILURE_REPORT | return to DOCUMENTED_ONLY |
| code divergence | DEMOTION_RECEIPT + REVIEW_REPORT | return to DOCUMENTED_ONLY |
| test failure | DEMOTION_RECEIPT + TEST_FAILURE_REPORT | return to IMPLEMENTED |
| CI failure | DEMOTION_RECEIPT + CI_FAILURE_REPORT | return to IMPLEMENTED |
| deployment rollback | DEMOTION_RECEIPT + ROLLBACK_LOG | return to VERIFIED |
| anchor mismatch | DEMOTION_RECEIPT + BROKEN_ANCHOR_REPORT | remove anchor modifier |

Current demotions: none.

---

## 5. Cross-Repo Promotion Tracking

`ANCHORED` is a modifier, not a replacement status.

Cross-repo anchor requirements:

- source artifact documented
- target artifact exists
- target SHA or content hash recorded
- authority false posture visible in target
- reference direction documented

Current cross-repo anchor status:

```json
{
  "anchors_recorded": 0,
  "cross_repo_lineage_documented": true,
  "cross_repo_anchors_verified": false,
  "authority": false
}
```

---

## 6. Receipt Binding Rules

Receipt hashes may be:

- Git commit SHAs
- content hashes
- CI artifact hashes
- deployment receipt hashes
- anchor receipt hashes

Rules:

- invented `rec_abc123` placeholders are invalid.
- every receipt hash must point to retrievable evidence.
- if the evidence cannot be retrieved, the promotion must not proceed.

---

## 7. Audit Queries

Find artifacts stuck in `DOCUMENTED_ONLY`:

```bash
grep "DOCUMENTED_ONLY" docs/constitutional_promotion_ledger_v1.md
```

Find invalid fake receipt hashes:

```bash
grep -E "rec_[a-z0-9]{6}" docs/constitutional_promotion_ledger_v1.md && echo "placeholder receipt found"
```

Find promoted artifacts:

```bash
grep "| P-" docs/constitutional_promotion_ledger_v1.md
```

Verify authority false posture:

```bash
grep -i "authority" docs/constitutional_promotion_ledger_v1.md
```

---

## 8. Promotion State Machine Diagram

```txt
[DOCUMENTED_ONLY]
   | requires DOC_RECEIPT + CODE_RECEIPT/SCHEMA_RECEIPT
   v
[IMPLEMENTED]
   | requires TEST_RECEIPT + CI_RECEIPT
   v
[VERIFIED]
   | requires DEPLOYMENT_RECEIPT
   v
[DEPLOYED]

[ANY_STATE]
   | requires ANCHOR_RECEIPT
   v
[ANCHOR_MODIFIER]
```

---

## Appendix A: Promotion Ledger JSON

```json
{
  "version": "V1",
  "authority": false,
  "promotions": [
    {
      "promotion_id": "P-001",
      "artifact_id": "ADN-005",
      "artifact_name": "REPLAY_ANOMALY_SCHEMA_V1",
      "previous_status": "DOCUMENTED_ONLY",
      "new_status": "IMPLEMENTED",
      "receipt_types": ["DOC_RECEIPT", "SCHEMA_RECEIPT"],
      "receipt_hashes": ["a0c6da10c8fe27b9e036f61afb6b5e0b0dd97fc7"],
      "issued_by": "repo commit",
      "issued_at": "2026-06-02T00:00:00Z",
      "authority": false
    }
  ]
}
```

---

## Canon

Status is claimed.  
Promotion is receipted.  
Verification is replayable.  
Authority is false.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
