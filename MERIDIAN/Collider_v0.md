# Collider v0

**Status:** FROZEN  
**Version:** 0.1.0  
**Service class:** Lookup-only graph join  
**Inference authority:** NONE  
**Verification authority:** NONE

## Purpose

Populate `meridian_event.collide` strictly from explicit graph relationships already present in the registry.

## Input

```yaml
collider_input:
  event_id: "uuidv7"
  entity_ids: []
  graph_snapshot_ref: "storage://..."
  graph_snapshot_hash: "sha256:..."
  requested_at: "ISO8601"
```

## Output

```yaml
collider_result:
  event_id: "uuidv7"
  graph_snapshot_hash: "sha256:..."
  looked_up_at: "ISO8601"
  roles: []
  funding: []
  litigation: []
  lobbying: []
  appointments: []
  publications: []
  unresolved_entity_ids: []
  authority: false
```

## Frozen invariants

- Lookup only. No inference.
- No fuzzy identity merge.
- No association-by-name alone.
- No edge promotion from co-occurrence.
- No confidence score may create an edge.
- Every returned edge must reference a graph edge id and source receipt.
- Missing edge = absent from current graph snapshot, not disproven.
- Collider cannot change `verification.status`.
- Collider cannot create or resolve entities.
- Collider cannot alter source bytes, event fields, or prior graph state.
- Re-running on a new graph snapshot creates a new collider result object.
- `authority = false` always.

## Join rule

```text
ENTITY_ID + GRAPH_SNAPSHOT
    -> explicit stored edges only
    -> collide buckets
```

Forbidden:

```text
name similarity -> identity
shared employer -> coordination
shared lawsuit -> wrongdoing
shared funding -> control
shared appearance -> collusion
```

## Audit requirement

Every collider result must preserve:

- event id
- graph snapshot hash
- edge ids
- source receipt ids
- lookup timestamp
- unresolved entity ids

## State rule

`COLLISION_FOUND` means only that one or more explicit graph edges matched the event's referenced entities. It is not a finding of misconduct, causality, conspiracy, or legal liability.
