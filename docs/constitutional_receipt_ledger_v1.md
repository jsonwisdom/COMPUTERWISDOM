# CONSTITUTIONAL_RECEIPT_LEDGER_V1

Authority: false  
Purpose: Single append-only registry of every receipt currently available in PR #202  
Invariant: Every promotion must reference a receipt. Every receipt must exist exactly once. Receipts are append-only.

---

## Receipt Ledger Summary

| Receipt Class | Total Issued | Valid | Expired | Revoked | Coverage |
|---|---:|---:|---:|---:|---|
| DOC_RECEIPT | 17 | 17 | 0 | 0 | Git doc receipts present |
| SCHEMA_RECEIPT | 1 | 1 | 0 | 0 | Git schema receipt present |
| CODE_RECEIPT | 0 | 0 | 0 | 0 | not present |
| TEST_RECEIPT | 0 | 0 | 0 | 0 | not present |
| CI_RECEIPT | 0 | 0 | 0 | 0 | not present |
| DEPLOYMENT_RECEIPT | 0 | 0 | 0 | 0 | not present |
| ANCHOR_RECEIPT | 0 | 0 | 0 | 0 | not present |
| DEMOTION_RECEIPT | 0 | 0 | 0 | 0 | not present |
| **TOTAL** | **18** | **18** | **0** | **0** | docs/schema only |

Ledger integrity posture:

```json
{
  "doc_receipts": 17,
  "schema_receipts": 1,
  "code_receipts": 0,
  "test_receipts": 0,
  "ci_receipts": 0,
  "deployment_receipts": 0,
  "anchor_receipts": 0,
  "authority": false
}
```

---

## 1. Receipt Inventory

### DOC_RECEIPT

| receipt_id | artifact_id | artifact_name | path | receipt_basis | status | authority |
|---|---|---|---|---|---|---|
| DOC-001 | ADN-001 | REPLAY_ENGINE_SPEC_V1 | `docs/anti_drift_news/replay_engine_spec_v1.md` | git commit | VALID | false |
| DOC-002 | ADN-002 | UI_WIREFRAME_SPEC_V1 | `docs/anti_drift_news/ui_wireframe_spec_v1.md` | git commit | VALID | false |
| DOC-003 | ADN-003 | OPEN_SOURCE_REPLAY_CLIENT_SPEC_V1 | `docs/anti_drift_news/open_source_replay_client_spec_v1.md` | git commit | VALID | false |
| DOC-004 | ADN-004 | CONSISTENCY_CONSTITUTIONAL_BUILD_V1 | `docs/anti_drift_news/consistency_constitutional_build_v1.md` | git commit | VALID | false |
| DOC-005 | ADN-006 | INTERNAL_DRIFT_ALERT_RESPONSE_PROTOCOL_V1 | `docs/anti_drift_news/internal_drift_alert_response_protocol_v1.md` | git commit | VALID | false |
| DOC-006 | ADN-007 | CONSTITUTIONAL_INDEX_V1 | `docs/constitutional_index_v1.md` | git commit | VALID | false |
| DOC-007 | ADN-008 | REPO_CONSTITUTIONAL_GRAPH_V1 | `docs/repo_constitutional_graph_v1.md` | git commit | VALID | false |
| DOC-008 | ADN-009 | DISCOVERY_PATH_V1 | `docs/discovery_path_v1.md` | git commit | VALID | false |
| DOC-009 | ADN-010 | README_CONSTITUTIONAL_DISCOVERY_ENTRY | `README.md` | git commit | VALID | false |
| DOC-010 | ADN-011 | CONSTITUTIONAL_RECEIPT_LEDGER_V1 | `docs/constitutional_receipt_ledger_v1.md` | git commit | VALID | false |
| DOC-011 | ADN-012 | CONSTITUTIONAL_STATUS_DASHBOARD_V1 | `docs/constitutional_status_dashboard_v1.md` | git commit | VALID | false |
| DOC-012 | ADN-013 | PR202_CLOSEOUT_REPORT_V1 | `docs/pr202_closeout_report_v1.md` | git commit | VALID | false |
| DOC-013 | ADN-014 | CONSTITUTIONAL_IMPLEMENTATION_GAP_REPORT_V1 | `docs/constitutional_implementation_gap_report_v1.md` | git commit | VALID | false |
| DOC-014 | ADN-015 | CONSTITUTIONAL_BUILD_QUEUE_V1 | `docs/constitutional_build_queue_v1.md` | git commit | VALID | false |
| DOC-015 | ADN-016 | CONSTITUTIONAL_EXECUTION_PLAN_V1 | `docs/constitutional_execution_plan_v1.md` | git commit | VALID | false |
| DOC-016 | ADN-017 | CONSTITUTIONAL_RECEIPT_REQUIREMENTS_V1 | `docs/constitutional_receipt_requirements_v1.md` | git commit | VALID | false |
| DOC-017 | ADN-018 | CONSTITUTIONAL_PROMOTION_LEDGER_V1 | `docs/constitutional_promotion_ledger_v1.md` | git commit | VALID | false |
| DOC-018 | ADN-019 | CONSTITUTIONAL_DEPENDENCY_REGISTRY_V1 | `docs/constitutional_dependency_registry_v1.md` | git commit | VALID | false |
| DOC-019 | ADN-020 | CONSTITUTIONAL_ARTIFACT_REGISTRY_V1 | `docs/constitutional_artifact_registry_v1.md` | git commit | VALID | false |
| DOC-020 | ADN-021 | CONSTITUTIONAL_STATE_DASHBOARD_V1 | `docs/constitutional_state_dashboard_v1.md` | git commit | VALID | false |

### SCHEMA_RECEIPT

| receipt_id | artifact_id | artifact_name | schema_path | receipt_basis | status | authority |
|---|---|---|---|---|---|---|
| SCH-001 | ADN-005 | REPLAY_ANOMALY_SCHEMA_V1 | `schemas/replay_anomaly.v1.schema.json` | git commit `a0c6da10c8fe27b9e036f61afb6b5e0b0dd97fc7` | VALID | false |

### Absent Receipt Classes

| receipt_class | status | reason |
|---|---|---|
| CODE_RECEIPT | ABSENT | no runtime code receipt verified in this ledger |
| TEST_RECEIPT | ABSENT | no test pass receipt verified in this ledger |
| CI_RECEIPT | ABSENT | no CI run receipt verified in this ledger |
| DEPLOYMENT_RECEIPT | ABSENT | no deployment receipt verified in this ledger |
| ANCHOR_RECEIPT | ABSENT | no cross-repo anchor receipt verified in this ledger |
| DEMOTION_RECEIPT | ABSENT | no demotions recorded |

---

## 2. Receipt Event Schema

Required common fields:

```json
{
  "receipt_id": "string",
  "receipt_class": "DOC_RECEIPT | SCHEMA_RECEIPT | CODE_RECEIPT | TEST_RECEIPT | CI_RECEIPT | DEPLOYMENT_RECEIPT | ANCHOR_RECEIPT | DEMOTION_RECEIPT",
  "artifact_id": "ADN-000",
  "artifact_name": "string",
  "path": "string",
  "receipt_basis": "git commit | content hash | CI artifact | deployment log | anchor receipt",
  "issued_at": "ISO-8601 or commit timestamp when available",
  "authority": false
}
```

No receipt is valid if `authority` is true.

---

## 3. Receipt Validation Rules

### 3.1 Receipt ID Uniqueness

Every receipt ID must appear exactly once.

### 3.2 Receipt Class Prefix Validation

| Receipt Class | Prefix | Pattern |
|---|---|---|
| DOC_RECEIPT | DOC | `DOC-[0-9]{3}` |
| SCHEMA_RECEIPT | SCH | `SCH-[0-9]{3}` |
| CODE_RECEIPT | COD | `COD-[0-9]{3}` |
| TEST_RECEIPT | TST | `TST-[0-9]{3}` |
| CI_RECEIPT | CI | `CI-[0-9]{3}` |
| DEPLOYMENT_RECEIPT | DEP | `DEP-[0-9]{3}` |
| ANCHOR_RECEIPT | ANC | `ANC-[0-9]{3}` |
| DEMOTION_RECEIPT | DEM | `DEM-[0-9]{3}` |

### 3.3 Issuer Validation

- DOC receipts may be created by human review plus Git commit.
- SCHEMA receipts require a schema file and, for VERIFIED status, future validation output.
- CODE, TEST, CI, DEPLOYMENT, and ANCHOR receipts require independent evidence.
- Self-issued final verification is not accepted.

### 3.4 Receipt Signature Validation

Future machine receipts should use:

```txt
receipt_hash = SHA-256(canonical_receipt_without_receipt_hash)
```

---

## 4. Receipt Expiration Rules

| Receipt Class | Valid Period | Renewal Required |
|---|---|---|
| DOC_RECEIPT | until document changes | yes on doc change |
| SCHEMA_RECEIPT | until schema changes | yes on schema change |
| CODE_RECEIPT | until code changes | yes on code change |
| TEST_RECEIPT | until test suite changes | yes on test change |
| CI_RECEIPT | until next relevant CI run or max 30 days | yes |
| DEPLOYMENT_RECEIPT | until deployment changes | yes |
| ANCHOR_RECEIPT | until target hash changes | yes |
| DEMOTION_RECEIPT | permanent | no |

---

## 5. Receipt Binding Rules

- Every promotion must reference a receipt.
- Every referenced receipt must exist in this ledger or in a linked CI/deployment/anchor artifact.
- A receipt may support only the status level it proves.
- DOC_RECEIPT cannot prove runtime implementation.
- CODE_RECEIPT cannot prove verification.
- TEST_RECEIPT without CI_RECEIPT cannot prove full VERIFIED status.
- DEPLOYMENT_RECEIPT cannot be inferred from documentation.
- ANCHOR_RECEIPT cannot be inferred from cross-repo mention alone.

---

## 6. Receipt Audit Queries

Find absent verification receipts:

```bash
grep -n "TEST_RECEIPT | ABSENT" docs/constitutional_receipt_ledger_v1.md
```

Find absent CI receipts:

```bash
grep -n "CI_RECEIPT | ABSENT" docs/constitutional_receipt_ledger_v1.md
```

Find absent anchor receipts:

```bash
grep -n "ANCHOR_RECEIPT | ABSENT" docs/constitutional_receipt_ledger_v1.md
```

Find unsafe fake receipt placeholders:

```bash
grep -R "sha256:abc\|rec_[a-z0-9]\{6\}" docs || true
```

---

## 7. Receipt Integrity Dashboard

```txt
DOC_RECEIPT        present
SCHEMA_RECEIPT     present
CODE_RECEIPT       absent
TEST_RECEIPT       absent
CI_RECEIPT         absent
DEPLOYMENT_RECEIPT absent
ANCHOR_RECEIPT     absent
DEMOTION_RECEIPT   absent
```

Integrity status:

```json
{
  "receipt_ledger_status": "DOCS_SCHEMA_ONLY",
  "promotion_safe": true,
  "runtime_verified": false,
  "deployed": false,
  "anchored": false,
  "authority": false
}
```

---

## Appendix A: Ledger JSON Sketch

```json
{
  "version": "V1",
  "authority": false,
  "receipts": [
    {
      "receipt_id": "DOC-001",
      "receipt_class": "DOC_RECEIPT",
      "artifact_id": "ADN-001",
      "artifact_name": "REPLAY_ENGINE_SPEC_V1",
      "path": "docs/anti_drift_news/replay_engine_spec_v1.md",
      "receipt_basis": "git commit",
      "authority": false
    },
    {
      "receipt_id": "SCH-001",
      "receipt_class": "SCHEMA_RECEIPT",
      "artifact_id": "ADN-005",
      "artifact_name": "REPLAY_ANOMALY_SCHEMA_V1",
      "path": "schemas/replay_anomaly.v1.schema.json",
      "receipt_basis": "git commit a0c6da10c8fe27b9e036f61afb6b5e0b0dd97fc7",
      "authority": false
    }
  ]
}
```

---

## Canon

State is observable.  
Receipts are verifiable.  
Promotion is traceable.  
Authority is false.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
