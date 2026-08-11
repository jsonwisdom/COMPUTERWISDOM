# COMPUTERWISDOM Mission Migration v0.2

v0.2 performs provenance-preserving **copies** from reviewed source commits into the canonical mission scaffold. It does not create institutional, legal, operational, or epistemic authority.

## Required sequence

```text
v0.1 DISCOVERY
  -> CLASSIFICATION
  -> INDEX
  -> VALIDATION
  -> ARTIFACT-LEVEL REVIEW
  -> SCAFFOLD
  -> v0.2 PLAN
  -> EXPLICIT MIGRATION AUTHORIZATION
  -> COPY
  -> HASH VERIFICATION
  -> PROVENANCE RECEIPT
```

## Reviewed artifact contract

A migration-eligible row must have:

```text
MIGRATION_STATUS = REVIEWED
REVIEW_REQUIRED = FALSE
CLASSIFICATION_AMBIGUOUS = FALSE
AUTHORITY_CREATED = FALSE
MISSION_ID = explicit
ARTIFACT_ID = explicit filesystem-safe id
SOURCE_SHA = immutable commit
SOURCE_PATHS = explicit non-empty selectors
DESTINATION_SUBDIR = explicit approved scaffold class
```

A branch containing multiple artifacts must be represented by multiple artifact rows. The branch itself is not the migration unit.

## Plan-only default

```powershell
.\tools\mission_control\migrate_v0_2.ps1
```

This writes `missions/_MIGRATION_PLAN_v0.2.json` and copies nothing.

## Execution gate

Execution requires all three conditions:

1. The reviewed index explicitly has `MIGRATION_AUTHORIZED = true`.
2. The runtime environment has `CW_MIGRATION_AUTHORIZED=TRUE`.
3. The operator invokes the explicit execution path.

```powershell
$env:CW_MIGRATION_AUTHORIZED='TRUE'
.\tools\mission_control\migrate_v0_2.ps1 -Execute
```

If any gate is missing, execution fails closed.

## Destination behavior

Files are copied beneath:

```text
missions/<MISSION_ID>/<DESTINATION_SUBDIR>/<ARTIFACT_ID>/<original-source-path>
```

This preserves original source-path identity and prevents unrelated artifacts from silently overwriting each other. Existing destination files with different bytes cause a hard failure.

## Receipts

Successful copies write:

```text
missions/<MISSION_ID>/receipts/migration-v0.2/<ARTIFACT_ID>.provenance.json
```

The receipt binds the original branch, immutable source SHA, explicit selectors, destination, file hashes, and copy event.

It always records:

```text
EVENT = COPY_HASH_VERIFIED
AUTHORITY_CREATED = FALSE
AUTHORITY_GRANT = null
ORIGINAL_BRANCH_DELETED = FALSE
```

## Invariants

```text
COPY != AUTHORITY
PROVENANCE_RECEIPT != AUTHORITY_GRANT
HANDOFF != EVIDENCE
BRANCH != ARTIFACT
MIGRATION != PROMOTION
ORIGINAL_BRANCHES remain untouched
```

Branch archival/deletion, corpus admission, authority establishment, and mission promotion are separate future operations and are intentionally outside v0.2.
