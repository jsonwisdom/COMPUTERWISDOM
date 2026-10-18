# Collider v0

**Status:** FROZEN  
**Version:** 0.1.0  
**Service class:** Append-only graph lookup  
**Inference authority:** NONE  
**Verification authority:** NONE  
**Mutation authority:** NONE

## Purpose

Given an existing Meridian event id plus already-resolved entity ids and a specific immutable graph snapshot, return only explicit stored graph edges relevant to the defined collision buckets.

Collider does **not** modify the Meridian event. It emits an immutable sidecar result.

## Input contract

```yaml
collider_input:
  schema_version: "0.1.0"
  event_id: "uuidv7"
  entity_ids: []
  graph_snapshot_ref: "storage://..."
  graph_snapshot_hash: "sha256:..."
  requested_at: "ISO8601"
  requested_by: operator | service
```

### Input gate

Collider MUST refuse execution if any of these are absent:

- event_id
- graph_snapshot_ref
- graph_snapshot_hash

An empty `entity_ids` list is valid and produces an empty result.

Collider MUST NOT resolve names into entity ids.

## Immutable output object

```yaml
collider_result:
  schema_version: "0.1.0"
  id: "sha256:<JCS-body-hash>"
  kind: collider_result
  event_id: "uuidv7"
  graph_snapshot_ref: "storage://..."
  graph_snapshot_hash: "sha256:..."
  looked_up_at: "ISO8601"

  matches:
    roles: []
    funding: []
    litigation: []
    lobbying: []
    appointments: []
    publications: []

  unresolved_entity_ids: []
  edge_count: 0
  collision_found: false
  authority: false
```

## Match object

Every returned edge MUST have this minimum form:

```yaml
match:
  edge_id: "graph-edge-id"
  edge_type: "stored-edge-type"
  subject_entity_id: "entity-id"
  object_entity_id: "entity-id-or-null"
  literal_value: null
  source_receipt_ids: []
  source_hashes: []
```

No match may exist without at least one `source_receipt_id`.

## Identity rule

```text
collider_result.id =
  "sha256:" + SHA256(RFC8785-JCS(collider_result body excluding id))
```

Re-running the exact same lookup against the exact same graph snapshot and lookup timestamp/body yields the same id. A new graph snapshot or changed lookup body creates a new result object.

## Frozen invariants

- LOOKUP ONLY.
- NO inference.
- NO event mutation.
- NO verification mutation.
- NO entity creation.
- NO entity resolution.
- NO fuzzy identity merge.
- NO association-by-name.
- NO edge creation from co-occurrence.
- NO confidence score may create an edge.
- NO model-generated relationship may enter `matches` unless it already exists as a sourced graph edge.
- Every returned edge references explicit graph edge id(s) and source receipt id(s).
- Missing edge means "not present in this graph snapshot", not disproven.
- `authority = false` always.
- `collision_found = true` iff `edge_count > 0`.
- `collision_found` is descriptive only.

## Forbidden semantic promotions

```text
name similarity        != identity
shared employer        != coordination
shared lawsuit         != wrongdoing
shared funding         != control
shared appointment     != improper influence
shared appearance      != collusion
collision_found        != misconduct
collision_found        != causality
collision_found        != conspiracy
collision_found        != liability
```

## Canonical event separation

Collider MUST NOT populate or rewrite canonical `meridian_event.collide` fields.

The operating picture MAY expose a derived read model:

```text
MERIDIAN_EVENT
  + latest/selected COLLIDER_RESULT(s)
  -> MATERIALIZED_COLLIDE_VIEW
```

That view is:

- derived
- non-canonical
- replayable from event id + collider result ids
- non-authoritative
- disposable/rebuildable

## Retractions / corrections

Collider operates on explicit event ids supplied to it.

If an event is later corrected, retracted, or superseded:

- the old collider result is preserved;
- it is not rewritten or deleted;
- consumers derive whether that result belongs to the current canonical head;
- a new collider run may be emitted for the new head.

## Failure object

Collider execution failures MUST be emitted separately as `collider_failure`; they MUST NOT be encoded as empty successful results when execution did not actually complete.

Minimum failure body:

```yaml
collider_failure:
  schema_version: "0.1.0"
  id: "sha256:<JCS-body-hash>"
  kind: collider_failure
  event_id: "uuidv7"
  graph_snapshot_hash: null
  stage: input | snapshot_fetch | integrity | lookup | unavailable
  reason: ""
  observed_at: "ISO8601"
  authority: false
```

## State meaning

`collision_found: true` means only:

> one or more explicit, sourced edges in the named graph snapshot matched the already-resolved entity ids for the event.

It is never a substantive finding about motive, wrongdoing, legality, coordination, causality, or liability.
