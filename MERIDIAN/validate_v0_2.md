# validate_v0_2

**Status:** SPECIFIED  
**Schema target:** Meridian_Event_v0_2 / Collider_v0  
**Execution:** NOT YET IMPLEMENTED  
**Default posture:** FAIL CLOSED

## Preservation note

Vectors 1–10 are declared unchanged by the prior Meridian v0.2 validator design, but no canonical `validate_v0_2.md` containing their exact bodies exists on this branch at this time.

This file therefore does **not** invent or restate vectors 1–10.

Until those exact vectors are materialized from their canonical source:
- they are preserved by reference only;
- they are not claimed executable from this file;
- vectors 11–13 below are additive and MUST NOT weaken any prior vector.

Vector 2's `legacy_unverified` sidecar behavior remains unchanged by this addendum.

## Source-class validation

### captured

Validator MUST FAIL unless all are true:

- `source.url != null`
- `source.content_hash` matches `^sha256:[0-9a-f]{64}$`
- `source.raw_capture_id != null`
- `source.raw_capture_id` resolves to `RAW_CAPTURE_v0`
- event `source.content_hash == raw_capture.content_hash`
- event `source.url == raw_capture.url`
- `source.operator == null`

### operator_relayed

Validator MUST FAIL unless all are true:

- `source.content_hash == null`
- `source.raw_capture_id == null`
- `source.operator != null`
- `verification.status == observed`

An operator-relayed record cannot be promoted in place.

Promotion requires:

```text
NEW RAW_CAPTURE_v0
-> NEW captured Meridian event
-> explicit supersede record
```

### migrated_legacy

Validator MUST FAIL on ordinary write-path when:

```text
source.source_class == migrated_legacy
```

Only the migrator may emit this class.

The migrator MUST NOT:
- re-fetch;
- re-hash;
- re-verify;
- synthesize `content_hash`;
- synthesize `raw_capture_id`.

## Vectors 11–13 — laundering barriers

### Vector 11 — operator relay cannot corroborate

Input condition:

```text
record_operation == emit
AND source.source_class == operator_relayed
AND verification.status IN {corroborated, corrected, resolved, retracted}
```

Expected:

```text
FAIL
reason = OPERATOR_RELAY_VERIFICATION_PROMOTION_FORBIDDEN
```

### Vector 12 — operator relay cannot carry content hash

Input condition:

```text
record_operation == emit
AND source.source_class == operator_relayed
AND source.content_hash != null
```

Expected:

```text
FAIL
reason = OPERATOR_RELAY_HASH_FORBIDDEN
```

### Vector 13 — Collider cannot launder operator-relayed receipts

Input condition:

```text
collider_result expresses confidence above unverified/legacy_unverified
AND every source_receipt_id supporting that confidence resolves only to
source.source_class == operator_relayed
```

Expected:

```text
FAIL
reason = COLLIDER_OPERATOR_RELAY_CONFIDENCE_LAUNDERING
```

## Vector 13 compatibility rule

`Collider_v0` currently has no canonical `confidence` field.

Therefore the validator MUST also fail closed if any implementation, sidecar extension, materialized view, or downstream consumer introduces a confidence-like field or semantic promotion not defined by the frozen Collider schema.

In other words:

```text
UNSCHEMATIZED CONFIDENCE != AUTHORITY
OPERATOR_RELAYED RECEIPTS != CONFIDENCE PROMOTION
```

## Migration rule 9 — specification only

For v0.1 -> v0.2 migration:

```text
IF v0.1 source has:
  verified content_hash
  AND resolvable RAW_CAPTURE_v0
THEN
  source_class = captured
ELSE
  source_class = operator_relayed OR migrated_legacy
  content_hash = null
  raw_capture_id = null
  NO re-fetch
  NO re-hash
  NO re-verify
```

The migration script MUST NOT be implemented or run until this validator contract is materialized and its test vectors are executable.


## Vector provenance — v0.2

This section describes provenance of validator vectors themselves.

**Namespace rule:** `vectors[].source_class` below is validator-vector provenance. It is NOT the same field or enum as `meridian_event.source.source_class`.

All thirteen vectors are currently:

```text
content_hash = null
binding = proposed
captured = false
corroborated = false
```

No vector becomes binding merely because it is present in this specification. Binding requires its own captured/provenanced validator artifact under the same Meridian provenance rules.

```yaml
vectors:
  - id: "V1"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V1"
    content_hash: null
    expects: pass
    binding: proposed

  - id: "V2"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V2"
    content_hash: null
    expects: pass
    binding: proposed

  - id: "V3"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V3"
    content_hash: null
    expects: skip
    binding: proposed
    skip_reason: "migrate_v0_1_to_v0_2.py not implemented; skip is a receipt, not a pass"

  - id: "V4"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V4"
    content_hash: null
    expects: fail
    binding: proposed

  - id: "V5"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V5"
    content_hash: null
    expects: fail
    binding: proposed

  - id: "V6"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V6"
    content_hash: null
    expects: fail
    binding: proposed

  - id: "V7"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V7"
    content_hash: null
    expects: fail
    binding: proposed
    fixture_note: "fixture must include supersede target so capture rule, not missing-id, throws"

  - id: "V8"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V8"
    content_hash: null
    expects: fail
    binding: proposed

  - id: "V9"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V9"
    content_hash: null
    expects: fail
    binding: proposed
    subcases:
      - id: "V9a"
        note: "migrated sidecar confidence outside {legacy_unverified} must fail"
      - id: "V9b"
        note: "graph_snapshot: null must fail independently"

  - id: "V10"
    source_class: authored_in_conversation
    authored_by: "Jason"
    operator: null
    transcript_ref: "conv://meridian/vectors#V10"
    content_hash: null
    expects: pass
    binding: proposed

  - id: "V11"
    source_class: operator_relayed
    authored_by: null
    operator: "Jason"
    transcript_ref: "conv://meridian/vectors#V11"
    content_hash: null
    expects: fail
    binding: proposed

  - id: "V12"
    source_class: operator_relayed
    authored_by: null
    operator: "Jason"
    transcript_ref: "conv://meridian/vectors#V12"
    content_hash: null
    expects: fail
    binding: proposed

  - id: "V13"
    source_class: operator_relayed
    authored_by: null
    operator: "Jason"
    transcript_ref: "conv://meridian/vectors#V13"
    content_hash: null
    expects: skip
    binding: proposed
    skip_reason: "collider_provenance_field_absent; addendum for input_source_classes/confidence not yet accepted"
```

### Skip semantics

```text
SKIP != PASS
SKIP != FAIL
SKIP = dependency absent / vector not currently executable
```

- V3 MUST skip while `migrate_v0_1_to_v0_2.py` is absent.
- V13 MUST skip while the proposed Collider provenance/confidence addendum is absent from the accepted Collider schema.

### V7 fixture requirement

V7 MUST include:

1. an existing target event `e0` whose source is `captured`;
2. a resolvable `RAW_CAPTURE_v0` for `e0`;
3. a matching `content_hash` on `e0`;
4. a superseding record `e1` with `supersedes: e0.id`;
5. `e1.source.source_class != captured`.

The expected failure MUST be:

```text
SUPERSEDE_REQUIRES_CAPTURED_SOURCE
```

A failure caused by missing target id, missing target capture, or target hash mismatch does not satisfy V7.
