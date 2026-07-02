# Google Cloud Minimal Control Plane

## Project

```text
project_id: jaywisdom-boardroom
purpose: cheap minimal control room
runtime_dependency: false
authority: false
truth_claim: false
```

## Purpose

The `jaywisdom-boardroom` Google Cloud project should remain a low-cost control room for Cloud Shell and GitHub-oriented workflows.

Google Cloud is permitted to support lightweight operational coordination, but it must not become a hidden runtime dependency, billing trap, secret authority layer, or substitute for replayable receipts.

## Enabled API Analysis

The current project should be reviewed for enabled APIs and separated into two groups: runtime-cost candidates and minimum control-room services.

### Potential High-Cost / Runtime Services

These services may create unwanted runtime or analytics cost and are candidates for disabling if no active receipt-backed dependency exists:

- `sql-component.googleapis.com` — Cloud SQL
- `run.googleapis.com` — Cloud Run
- `bigquery.googleapis.com` and related BigQuery services
- `cloudaicompanion.googleapis.com` — Gemini for Google Cloud
- `dataform.googleapis.com` — Dataform
- `dataplex.googleapis.com` — Dataplex
- `datastore.googleapis.com` — Datastore / Firestore mode dependency surface

### Minimal Control-Room Services

These services may be acceptable if they are required for Cloud Shell, GitHub automation, or basic project management:

- `iam.googleapis.com` — identity and access management
- `cloudbuild.googleapis.com` — only if GitHub automation requires it
- `artifactregistry.googleapis.com` — only if image or package storage is required
- `storage.googleapis.com` — only for explicit low-cost storage needs
- `serviceusage.googleapis.com` — API management
- `logging.googleapis.com` — logs, budgeted and bounded
- `monitoring.googleapis.com` — monitoring, budgeted and bounded

## Billing and Budget Check

Billing and budget verification should be performed manually when CLI access is blocked or returns authenticator errors.

Manual budget checklist:

1. Open Google Cloud Console Billing.
2. Select **Budgets & alerts**.
3. Confirm a budget exists for `jaywisdom-boardroom`.
4. Use a low ceiling such as `$1`, `$5`, or `$10`.
5. Configure alerts at 50%, 90%, and 100%.

## Operating Rule

```text
Cloud Shell = terminal
GCP project = cheap control room
No paid runtime unless explicitly approved
No Gemini/API spend unless explicitly approved
No hidden infrastructure
No authority elevation
```

## Disable Strategy

Do not blindly disable services until active resources are identified.

Preferred sequence:

1. List enabled APIs.
2. Identify active resources for runtime APIs.
3. Confirm no workflow dependency exists.
4. Disable nonessential APIs.
5. Preserve receipts of each disable action.

## Command Surface

Read-only discovery commands:

```bash
gcloud config set project jaywisdom-boardroom
gcloud services list --enabled
gcloud billing projects describe jaywisdom-boardroom || true
gcloud alpha billing budgets list 2>/dev/null || true
```

Runtime resource discovery commands:

```bash
gcloud sql instances list 2>/dev/null || true
gcloud run services list --platform=managed --region=us-central1 2>/dev/null || true
gcloud bigquery datasets list 2>/dev/null || true
gcloud artifacts repositories list 2>/dev/null || true
gcloud storage buckets list 2>/dev/null || true
```

## Negotiation Boundary

Google Cloud remains in the architecture only if it stays cheap, bounded, and operationally useful.

Google Cloud should be removed from the critical path if it becomes:

- a runtime dependency
- a billing trap
- a secret holder
- an authority layer
- a non-replayable source of operational claims

## Final Rule

```text
Use Google Cloud as a control room, not a cathedral.
Receipts first. Runtime last.
```
