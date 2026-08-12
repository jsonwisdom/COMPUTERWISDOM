# COMPUTERWISDOM Asset Migration Planner v0.1

Class: `COMPUTERWISDOM_INSTRUMENT`

## Purpose

Turn a read-only asset inventory into a provenance-bound migration review plan without moving files.

```text
INVENTORY -> BLOB_BINDING -> CLASS_REVIEW -> TARGET_PROPOSAL -> HOLD/REVIEW_REQUIRED
```

The planner binds each tracked source path to its Git blob SHA. It never treats a heuristic classification as final authority.

## Fail-closed states

- `REVIEW_REQUIRED` — one buried class, tracked source blob known, no target collision detected.
- `HOLD_MULTI_CLASS` — more than one buried semantic class is plausible.
- `HOLD_SOURCE_BLOB_UNKNOWN` — source path is not bound to a tracked Git blob.
- `HOLD_TARGET_COLLISION` — suggested canonical target already exists.

Every emitted record begins with:

```text
dependencies_updated=false
semantic_review_passed=false
tests_passed=false
move_authorized=false
```

## Boundary

The planner proposes review records only. It performs no relocation, deletion, promotion, merge, or authority creation.

```text
MOVES_PERFORMED=false
AUTHORITY_CREATED=false
```

Canonical executable: `executables/asset_migration_plan_v0_1.py`
