# Collider v0.2 Provenance Addendum

**Binding:** PROPOSED  
**Captured:** NO  
**Authority created:** NONE  
**Parent:** `MERIDIAN/Collider_v0.md`  
**Supersedes:** `MERIDIAN/Collider_v0_1_PROVENANCE_ADDENDUM.md`

This is a child artifact. It does not mutate frozen Collider v0 or the prior v0.1 addendum in place.

## Addendum object

```yaml
collider_result_addendum:
  schema_version: "0.2.0"
  kind: collider_result_addendum
  id: null                       # content-addressed when captured
  collider_result_id: "sha256:..."
  supersedes: null               # prior addendum id for this collider result

  input_source_classes:
    - ref: "receipt-or-input-id"
      source_class: captured | operator_relayed | migrated_legacy

  confidence: legacy_unverified | provisional | confirmed | strong
```

## Seam A — per-input provenance

`input_source_classes` is a per-input list, not an aggregate set.

Each entry binds:
- one input ref;
- one explicit source class.

The derived set of classes is read-only and non-canonical:

```text
derived_source_class_set = unique(input_source_classes[*].source_class)
```

Multiplicity and input identity remain recoverable from the canonical addendum body.

## Seam B — confidence domain

`invalid_input` is NOT a confidence value.

The only confidence values are totally ordered:

```text
legacy_unverified < provisional < confirmed < strong
```

Unknown confidence values fail schema validation with `CONFIDENCE_VALUE_INVALID`.

## Seam C — non-captured promotion rule

Non-captured means:

```text
source_class IN {operator_relayed, migrated_legacy}
```

If ANY supporting input is non-captured, the maximum allowed addendum confidence is:

```text
provisional
```

Therefore:

```text
ANY non-captured input
AND confidence IN {confirmed, strong}
-> FAIL NON_CAPTURED_CONFIDENCE_PROMOTION
```

This rule is provenance-only. It does not change event verification state, graph edges, legal authority, or canonical Collider output.

## Seam D — failure-code registry binding

The expected promotion failure is registered as:

```yaml
code: NON_CAPTURED_CONFIDENCE_PROMOTION
class: provenance
emit_site: check_collider_addendum
promoted_by: null
blocked_by: null
```

The old `OPERATOR_RELAYED_CONFIDENCE_PROMOTION` code remains in the append-only registry as deprecated and is superseded by the new code.

## Seam E — addendum chain

There may be multiple addenda for one `collider_result_id`.

Rules:
- first addendum: `supersedes: null`;
- later addendum: `supersedes: <prior addendum id>`;
- addenda are never deleted or rewritten in place;
- no self-supersede;
- no direct or transitive supersession cycle;
- consumers derive the current addendum head from the chain.

## Cardinality / identity

One collider result may have zero or more addenda.

An addendum id becomes content-addressed only when the addendum bytes are captured. Until then, proposed addenda remain non-binding and may use `id: null` in fixture material.

## V13 boundary

V13 is split into paired fixtures:

```text
V13a: non-captured input + strong confidence      -> FAIL
V13b: non-captured input + provisional confidence -> PASS
```

That pair pins the boundary without adding confidence to canonical Collider v0.
