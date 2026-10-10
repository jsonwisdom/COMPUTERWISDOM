# APPLE BLOSSOM AWESOME DEEP PURPOSE AUDIT V1

OBJECT = REPOSITORY_PROJECT_IDENTITY
ENGINE = SUPREME_SEYMOUR
SYNTAX = SEYMOUR_SUPREME_SYNTAX_V1
STOP_ON_LABEL = FALSE
STOP_ON_README = FALSE
STOP_ON_REPO_NAME = FALSE
NO_FAKE_GREEN = TRUE

## Trigger law

The audit continues while ANY required layer is unresolved.

TRIGGER_A — ROOT_UNKNOWN
No verified default-branch head/tree snapshot.

TRIGGER_B — TREE_UNKNOWN
No recursive tree inventory proving what files/directories exist.

TRIGGER_C — PURPOSE_UNKNOWN
No source-backed project purpose.

TRIGGER_D — PURPOSE_CONFLICT
README/docs/code/history imply materially different project purposes.

TRIGGER_E — LINEAGE_UNKNOWN
Current project cannot be connected to its meaningful versions/commits.

TRIGGER_F — IDENTITY_UNKNOWN
Named operator/identity/anchor claim lacks a bounded receipt.

TRIGGER_G — EXECUTION_UNKNOWN
Repo claims to perform work but executable surface is not identified.

TRIGGER_H — EXTERNAL_POINTER_UNKNOWN
Repo points to another repo/Drive/chain/service and the pointer is material to project identity.

TRIGGER_I — SNAPSHOT_MISSING
No frozen manifest exists for the resolved project state.

TRIGGER_J — DELTA_UNCLASSIFIED
Current tree/head differs from last frozen snapshot and changes are not classified.

## Deepening loop

OBSERVE_REPO
→ PIN_DEFAULT_BRANCH
→ PIN_HEAD_COMMIT
→ CAPTURE_RECURSIVE_TREE
→ HASH_CANONICAL_TREE_MANIFEST
→ IDENTIFY_HIGH_SIGNAL_FILES
→ READ_HIGH_SIGNAL_FILES
→ RECONSTRUCT_PROJECT_PURPOSE
→ CROSSCHECK_COMMIT_LINEAGE
→ CROSSCHECK_IDENTITY / EXTERNAL POINTERS WHEN MATERIAL
→ TEST FOR CONFLICTS / GAPS
→ REPEAT DEEPER IF ANY TRIGGER REMAINS
→ FREEZE PROJECT SNAPSHOT
→ DELTA MODE

## High-signal files

README*
PURPOSE*
MISSION*
CHARTER*
CONSTITUTION*
ARCHITECTURE*
MANIFEST*
package.json
pyproject.toml
requirements*.txt
Cargo.toml
go.mod
Dockerfile
.github/workflows/*
schemas/*
src/*
docs/* only as needed after root evidence

File names are locators, not purpose proof.

## Snapshot completeness

A PROJECT_SNAPSHOT may be frozen only when it carries:

REPO
DEFAULT_BRANCH
HEAD_COMMIT
TREE_SHA / TREE_RECEIPT
TREE_ENTRY_COUNT
CANONICAL_TREE_DIGEST
HIGH_SIGNAL_FILES_READ[]
PROJECT_PURPOSE
PURPOSE_RECEIPTS[]
EXECUTION_SURFACES[]
IDENTITY_POINTERS[]
EXTERNAL_POINTERS[]
OPEN_GAPS[]
SNAPSHOT_STATE

SNAPSHOT_STATE = COMPLETE only when OPEN_GAPS affecting project identity = [].
Otherwise SNAPSHOT_STATE = PARTIAL and audit continues.

## Delta law

After a COMPLETE snapshot:

CURRENT_HEAD == SNAPSHOT_HEAD
→ NO_PROJECT_DATA_MOVEMENT
→ NO_CHANGE

CURRENT_HEAD != SNAPSHOT_HEAD
→ COMPARE SNAPSHOT_HEAD...CURRENT_HEAD
→ READ ONLY CHANGED HIGH-SIGNAL FILES + NEW/REMOVED TREE EDGES
→ CLASSIFY PURPOSE_DELTA | EXECUTION_DELTA | IDENTITY_DELTA | EVIDENCE_DELTA | NONMATERIAL_DELTA
→ UPDATE SNAPSHOT ONLY AFTER RECEIPT

FULL_RESCAN is triggered only by:
- history rewrite / non-fast-forward
- snapshot corruption
- high-signal structural change
- purpose conflict
- unexplained external pointer change
- Jason request

## No corner law

ACTIVE / ARCHIVE / KEEP / FREEZE / RETIRE are optional operator decisions AFTER project reconstruction.
They are NOT substitutes for reconstruction and they do not terminate the audit.
