# Project Governance Baseline: jaywisdom-boardroom

**Date:** 2026-07-02  
**Tag:** `boardroom-baseline-2026-07-02`  
**Identity:** `jaywisdom.base.eth`  
**Repository Responsibility:** `jsonwisdom/COMPUTERWISDOM`  
**Objective:** Absolute minimal cost, zero-residue control room for GitHub and Cloud Shell operations.

## 1. Scope

This document records the governance responsibility for the Google Cloud project `jaywisdom-boardroom` inside the broader COMPUTERWISDOM operational map.

It is not a live credential, secret store, or billing account record. It is a baseline control document for repeatable audits, drift detection, and post-hardening verification.

## 2. Scorecard: Hardened State

| Vector | Status | Verified Method |
| :--- | :--- | :--- |
| Cloud Run Security | PRIVATE | No `allUsers` bindings; IAM authentication required. |
| Storage Hygiene | CLEAN | Four zombie ledger buckets purged; zero detached ledger residue. |
| Artifact Lifecycle | AUTOMATED | Seven-day cleanup policy for untagged images. |
| Compute Billing | ON-DEMAND | No BigQuery reservations or capacity commitments; Cloud Run has no minimum instance binding shown. |
| Truth Layer | WIRING | `gcp_billing_export` dataset created; Billing Console export wiring pending. |
| Guardrails | PENDING | One-dollar monthly budget alert planned. |

## 3. Governing Variable

The governing variable for this project is:

> Keep `jaywisdom-boardroom` as a minimal, authenticated, auditable control room with no orphaned resources, no public runtime exposure unless explicitly intended, and no unobserved cost surfaces.

Any future infrastructure change should be evaluated against this variable before deployment.

## 4. Residual API Cleanup: Phase 4

Only disable APIs after confirming they are not needed for current workflows.

```bash
gcloud services list --enabled \
  --filter="name:(cloudaicompanion.googleapis.com OR analyticshub.googleapis.com OR sql-component.googleapis.com OR datastore.googleapis.com)"
```

If confirmed unused:

```bash
gcloud services disable cloudaicompanion.googleapis.com
gcloud services disable analyticshub.googleapis.com
gcloud services disable sql-component.googleapis.com
gcloud services disable datastore.googleapis.com
```

## 5. Post-Hardening Verification

Run monthly or after any major automation change.

```bash
PROJECT_ID="jaywisdom-boardroom"
REGION="us-central1"

gcloud config set project "$PROJECT_ID"

# Check for new storage orphans
gcloud storage buckets list --project "$PROJECT_ID"

# Check for public Cloud Run bindings
gcloud run services get-iam-policy boardroom-core \
  --region="$REGION" \
  --project="$PROJECT_ID"

gcloud run services get-iam-policy jaywisdom-boardroom \
  --region="$REGION" \
  --project="$PROJECT_ID"

# Check Artifact Registry policy
gcloud artifacts repositories describe cloud-run-source-deploy \
  --location="$REGION" \
  --project="$PROJECT_ID" \
  --format="yaml(cleanupPolicies)"
```

## 6. Cost Truth Layer Verification

After Billing Console export wiring and propagation delay, find the exact billing export table:

```sql
SELECT table_name
FROM `jaywisdom-boardroom.gcp_billing_export.INFORMATION_SCHEMA.TABLES`
WHERE table_name LIKE 'gcp_billing_export_v1_%';
```

Then query recent cost rows using the discovered table name:

```sql
SELECT
  service.description AS service_name,
  sku.description AS sku_name,
  usage_start_time,
  cost,
  currency
FROM
  `jaywisdom-boardroom.gcp_billing_export.gcp_billing_export_v1_YOUR_BILLING_ID`
ORDER BY
  usage_start_time DESC
LIMIT 20;
```

## 7. Baseline Archive

A local Cloud Shell baseline archive was created during the hardening cycle:

```text
~/audit/jaywisdom-boardroom-baseline-20260702.tar.gz
```

Known contents:

```text
storage.txt
artifact-registry.yaml
project.yaml
```

If this archive is preserved externally, use a private or controlled-access location. Do not store credentials, secrets, private keys, billing account identifiers, or sensitive IAM dumps in public repositories.

## 8. Responsibility Placement

`COMPUTERWISDOM` owns the governance responsibility because this project is part of the broader operational identity/control-plane map.

Implementation scripts and operator tools may live in `jsonwisdom/receipts-engine-v1`, but COMPUTERWISDOM records the constitutional baseline and accountability layer.

## 9. Final Verdict

`jaywisdom-boardroom` is closed for this audit cycle once these final manual console actions are completed:

1. Enable Detailed Usage Cost export into `jaywisdom-boardroom:gcp_billing_export`.
2. Configure budget alerts at 50%, 90%, and 100% against a one-dollar monthly threshold.
3. Confirm first billing rows appear in BigQuery after propagation.

Until those are confirmed, the project is hardened but the cost truth layer remains in wiring status.
