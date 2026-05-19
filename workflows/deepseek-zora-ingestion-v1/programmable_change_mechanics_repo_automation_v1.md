# Programmable Change Mechanics — Repo Automation V1

## Purpose

Automate JSONWISDOM repo workflow so every folder becomes a measurable state node, every change becomes a logged transition, and every promotion requires replayable receipts.

This is a software governance metaphor inspired by quantum mechanics, not a physics claim.

## Core Law

- No receipt → no state entry.
- No source → no public post.
- No canon without replay.
- Publication surfaces are mirrors, not judges.
- Machine speed sorts; receipts decide.
- Every folder has a state.
- Every change has a transition receipt.

## Repo State Model

Each folder is treated as a state-space node:

```json
{
  "folder_id": "PENDING",
  "path": "PENDING",
  "state": "CANDIDATE",
  "last_observed_commit": "PENDING_HASH",
  "folder_digest": "PENDING_HASH",
  "transition_count": 0,
  "open_receipts": [],
  "blocked_by": [],
  "zora_visibility": "NOT_MINTED"
}
```

## Canonical States

- `CANDIDATE` — folder/artifact exists but is not fully verified.
- `HELD` — unresolved contradiction, missing receipt, or invalid transition.
- `REJECTED` — disproven, unsafe, or invalid.
- `VERIFIED_RECEIPT` — receipt validated, not full canon.
- `CANON` — replayable, receipt-backed, contradiction-cleared, time-anchored.

## Change Mechanics

A repo change is a transition:

```text
PREVIOUS_STATE + CHANGE_EVENT + RECEIPT = NEXT_STATE
```

Change events include:

- file added
- file modified
- file deleted
- folder created
- folder reorganized
- receipt appended
- status changed
- Zora publication reference added
- contradiction logged
- superseding receipt appended

## Transition Receipt Schema

```json
{
  "receipt_type": "REPO_TRANSITION_RECEIPT_V1",
  "repo": "jsonwisdom/COMPUTERWISDOM",
  "branch": "PENDING",
  "folder_path": "PENDING",
  "event_type": "PENDING",
  "previous_commit": "PENDING_HASH",
  "new_commit": "PENDING_HASH",
  "previous_folder_digest": "PENDING_HASH",
  "new_folder_digest": "PENDING_HASH",
  "state_before": "CANDIDATE",
  "state_after": "CANDIDATE",
  "reason": "PENDING",
  "contradiction_scan_hash": "PENDING_HASH",
  "timestamp_utc": "PENDING",
  "operator": "jaywisdom.base.eth"
}
```

## Automation Loop

1. Scan repository tree.
2. Create or update folder state map.
3. Compute folder digest for every folder.
4. Detect changes since prior commit.
5. Create transition receipt per changed folder.
6. Run contradiction scan.
7. Apply state transition rules.
8. Update `PUBLIC_INDEX.json`.
9. Generate Game Master Board summary.
10. Queue Zora-safe captions only from public state.

## Folder State Map

Target file:

```text
workflows/deepseek-zora-ingestion-v1/folder_state_map_v1.json
```

Required fields:

- folder_id
- path
- state
- last_observed_commit
- folder_digest
- receipt_refs
- contradiction_refs
- children
- parent
- zora_visibility
- promotion_gate

## GitHub Actions Plan

Target workflow:

```text
.github/workflows/json_live_repo_state_audit.yml
```

Jobs:

1. checkout repo
2. compute folder digests
3. validate JSON files
4. scan protocol state names
5. detect forbidden placeholders in CANON artifacts
6. generate transition receipts
7. update audit artifact
8. fail if CANON references `PENDING_HASH`

## Quantum Mechanics Metaphor Layer

- Superposition = CANDIDATE state before receipts resolve.
- Measurement = receipt binding and hash computation.
- Collapse = state transition into HELD, REJECTED, VERIFIED_RECEIPT, or CANON.
- Entanglement = dependency tree between folders/artifacts.
- Decoherence = contradiction, stale source, or broken dependency.
- Observer effect = every audit creates a replay log entry.

## Safety Boundary

This workflow is repo governance automation only. It does not imply scientific quantum computation, government authority, surveillance, classified access, or external targeting.

## Next Implementation Files

```text
folder_state_map_v1.json
repo_transition_receipt_schema_v1.json
json_live_repo_state_audit.yml
compute_folder_digests.mjs
validate_public_index.mjs
scan_for_state_drift.mjs
```

## Final Line

Programmable change means every mutation leaves a receipt, every folder has a state, and every canon claim survives replay.
