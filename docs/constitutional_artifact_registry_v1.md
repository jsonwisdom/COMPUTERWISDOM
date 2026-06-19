# CONSTITUTIONAL_ARTIFACT_REGISTRY_V1

Authority: false  
Purpose: Single source of truth for every constitutional artifact in PR #202  
Invariant: Every constitutional artifact must exist in exactly one registry row

---

## Registry Summary

| Metric | Count |
|---|---:|
| Total Artifacts | 18 |
| DOCUMENTED_ONLY | 17 |
| IMPLEMENTED | 1 |
| VERIFIED | 0 |
| DEPLOYED | 0 |
| ANCHORED | 0 |
| Receipt Coverage | 18/18 have Git commit receipt references or ledger path |
| Promotion Coverage | 18/18 tracked by status class |

Status boundary:

```json
{
  "documented_only": "committed docs/specs without runtime proof",
  "implemented": "machine artifact exists, but CI/runtime verification not claimed here",
  "verified": "requires test and CI receipts",
  "deployed": "requires deployment receipt",
  "anchored": "requires cross-repo anchor receipt",
  "authority": false
}
```

---

## 1. Artifact Inventory

| artifact_id | artifact_name | artifact_path | repo | status | anchor_status | receipt_status | promotion_status | authority |
|---|---|---|---|---|---|---|---|---|
| ADN-001 | REPLAY_ENGINE_SPEC_V1 | `docs/anti_drift_news/replay_engine_spec_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-002 | UI_WIREFRAME_SPEC_V1 | `docs/anti_drift_news/ui_wireframe_spec_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-003 | OPEN_SOURCE_REPLAY_CLIENT_SPEC_V1 | `docs/anti_drift_news/open_source_replay_client_spec_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-004 | CONSISTENCY_CONSTITUTIONAL_BUILD_V1 | `docs/anti_drift_news/consistency_constitutional_build_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-005 | REPLAY_ANOMALY_SCHEMA_V1 | `schemas/replay_anomaly.v1.schema.json` | COMPUTERWISDOM | IMPLEMENTED | NONE | GIT_SCHEMA_RECEIPT | TRACKED | false |
| ADN-006 | INTERNAL_DRIFT_ALERT_RESPONSE_PROTOCOL_V1 | `docs/anti_drift_news/internal_drift_alert_response_protocol_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-007 | CONSTITUTIONAL_INDEX_V1 | `docs/constitutional_index_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-008 | REPO_CONSTITUTIONAL_GRAPH_V1 | `docs/repo_constitutional_graph_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-009 | DISCOVERY_PATH_V1 | `docs/discovery_path_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-010 | README_CONSTITUTIONAL_DISCOVERY_ENTRY | `README.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-011 | CONSTITUTIONAL_RECEIPT_LEDGER_V1 | `docs/constitutional_receipt_ledger_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-012 | CONSTITUTIONAL_STATUS_DASHBOARD_V1 | `docs/constitutional_status_dashboard_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-013 | PR202_CLOSEOUT_REPORT_V1 | `docs/pr202_closeout_report_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-014 | CONSTITUTIONAL_IMPLEMENTATION_GAP_REPORT_V1 | `docs/constitutional_implementation_gap_report_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-015 | CONSTITUTIONAL_BUILD_QUEUE_V1 | `docs/constitutional_build_queue_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-016 | CONSTITUTIONAL_EXECUTION_PLAN_V1 | `docs/constitutional_execution_plan_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-017 | CONSTITUTIONAL_RECEIPT_REQUIREMENTS_V1 | `docs/constitutional_receipt_requirements_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |
| ADN-018 | CONSTITUTIONAL_PROMOTION_LEDGER_V1 | `docs/constitutional_promotion_ledger_v1.md` | COMPUTERWISDOM | DOCUMENTED_ONLY | NONE | GIT_DOC_RECEIPT | TRACKED | false |

---

## 2. Artifact Classification

### By Type

| Type | Artifacts | Count |
|---|---|---:|
| Documentation | ADN-001, ADN-002, ADN-003, ADN-004, ADN-006, ADN-007, ADN-008, ADN-009, ADN-010, ADN-011, ADN-012, ADN-013, ADN-014, ADN-015, ADN-016, ADN-017, ADN-018 | 17 |
| Schema | ADN-005 | 1 |
| Code | none verified in this registry | 0 |
| Deployment | none verified in this registry | 0 |

### By Status

| Status | Artifacts | Count |
|---|---|---:|
| DOCUMENTED_ONLY | ADN-001, ADN-002, ADN-003, ADN-004, ADN-006, ADN-007, ADN-008, ADN-009, ADN-010, ADN-011, ADN-012, ADN-013, ADN-014, ADN-015, ADN-016, ADN-017, ADN-018 | 17 |
| IMPLEMENTED | ADN-005 | 1 |
| VERIFIED | none | 0 |
| DEPLOYED | none | 0 |
| ANCHORED | none | 0 |

---

## 3. Constitutional Lineage

```txt
AL -> COMPUTERWISDOM -> JOY -> ENS -> ALMS
```

This registry tracks COMPUTERWISDOM artifacts in PR #202.

Cross-repo lineage is documented but not promoted to anchored status without independent `ANCHOR_RECEIPT`.

---

## 4. Repository Distribution

| Repository | DOCUMENTED_ONLY | IMPLEMENTED | VERIFIED | DEPLOYED | ANCHORED | Total |
|---|---:|---:|---:|---:|---:|---:|
| COMPUTERWISDOM | 17 | 1 | 0 | 0 | 0 | 18 |

Referenced but not registered as verified artifacts in this PR:

- `jsonwisdom/AL`
- `jsonwisdom/JOY`
- `jsonwisdom/layered-proofing-state-level-alms`
- ENS display layer

---

## 5. Receipt Coverage

| Receipt Status | Count | Meaning |
|---|---:|---|
| GIT_DOC_RECEIPT | 17 | document committed on PR branch |
| GIT_SCHEMA_RECEIPT | 1 | schema committed on PR branch |
| CODE_RECEIPT | 0 | no runtime code receipt claimed here |
| TEST_RECEIPT | 0 | no test pass receipt claimed here |
| CI_RECEIPT | 0 | no CI pass receipt claimed here |
| DEPLOYMENT_RECEIPT | 0 | no deployment receipt claimed here |
| ANCHOR_RECEIPT | 0 | no cross-repo anchor receipt claimed here |

---

## 6. Promotion Coverage

Current promotion state:

```json
{
  "tracked_artifacts": 18,
  "promoted_to_implemented": 1,
  "promoted_to_verified": 0,
  "promoted_to_deployed": 0,
  "promoted_to_anchored": 0,
  "authority": false
}
```

Only `ADN-005 REPLAY_ANOMALY_SCHEMA_V1` is currently `IMPLEMENTED` because it is a machine-readable schema file with a Git receipt.

No artifact is marked `VERIFIED` because test and CI receipts are not included in this registry.

---

## 7. Missing Artifact Detection

Expected PR #202 registry invariant:

```txt
Every constitutional artifact created in this branch appears exactly once.
```

Manual audit command:

```bash
for path in \
  docs/anti_drift_news/replay_engine_spec_v1.md \
  docs/anti_drift_news/ui_wireframe_spec_v1.md \
  docs/anti_drift_news/open_source_replay_client_spec_v1.md \
  docs/anti_drift_news/consistency_constitutional_build_v1.md \
  docs/anti_drift_news/internal_drift_alert_response_protocol_v1.md \
  schemas/replay_anomaly.v1.schema.json \
  docs/constitutional_index_v1.md \
  docs/repo_constitutional_graph_v1.md \
  docs/discovery_path_v1.md \
  docs/constitutional_receipt_ledger_v1.md \
  docs/constitutional_status_dashboard_v1.md \
  docs/pr202_closeout_report_v1.md \
  docs/constitutional_implementation_gap_report_v1.md \
  docs/constitutional_build_queue_v1.md \
  docs/constitutional_execution_plan_v1.md \
  docs/constitutional_receipt_requirements_v1.md \
  docs/constitutional_promotion_ledger_v1.md; do
  test -f "$path" && echo "FOUND $path" || echo "MISSING $path"
done
```

---

## 8. Audit Commands

Check authority posture:

```bash
grep -R "authority.*true" docs schemas || true
```

Expected:

```txt
No unsafe authority:true claims.
```

Check for fake receipt placeholders:

```bash
grep -R "rec_[a-z0-9]\{6\}" docs || true
```

Expected:

```txt
No placeholder receipt hashes.
```

Check for silent verified claims:

```bash
grep -R "VERIFIED" docs/constitutional_artifact_registry_v1.md docs/constitutional_promotion_ledger_v1.md
```

Expected:

```txt
No artifact status is VERIFIED without test and CI receipts.
```

---

## Appendix A: Registry JSON Export

```json
{
  "version": "V1",
  "authority": false,
  "artifacts": [
    {
      "artifact_id": "ADN-001",
      "artifact_name": "REPLAY_ENGINE_SPEC_V1",
      "artifact_path": "docs/anti_drift_news/replay_engine_spec_v1.md",
      "repo": "COMPUTERWISDOM",
      "status": "DOCUMENTED_ONLY",
      "anchor_status": "NONE",
      "receipt_status": "GIT_DOC_RECEIPT",
      "promotion_status": "TRACKED",
      "authority": false
    },
    {
      "artifact_id": "ADN-005",
      "artifact_name": "REPLAY_ANOMALY_SCHEMA_V1",
      "artifact_path": "schemas/replay_anomaly.v1.schema.json",
      "repo": "COMPUTERWISDOM",
      "status": "IMPLEMENTED",
      "anchor_status": "NONE",
      "receipt_status": "GIT_SCHEMA_RECEIPT",
      "promotion_status": "TRACKED",
      "authority": false
    }
  ],
  "note": "Full table above is the human-readable source for PR #202. Future machine registry may be split into JSON file."
}
```

---

## Canon

Artifacts are observable.  
Receipts are verifiable.  
Promotion is traceable.  
Authority is false.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
