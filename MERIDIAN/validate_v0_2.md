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
