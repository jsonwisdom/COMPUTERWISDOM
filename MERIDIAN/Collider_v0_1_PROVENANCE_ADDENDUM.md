# Collider v0.1 Provenance Addendum

**Decision:** ACCEPT `input_source_classes` as the provenance field needed to evaluate source-class promotion.  
**Binding:** PROPOSED  
**Captured:** NO  
**Authority created:** NONE  
**Parent:** `MERIDIAN/Collider_v0.md`

This addendum does not mutate frozen Collider v0 in place. It is a proposed child delta.

## Added field

```yaml
input_source_classes:
  - source_receipt_id: "receipt-id"
    source_class: captured | operator_relayed | migrated_legacy
```

The field is supplied to Collider from already-resolved source receipts. Collider MUST NOT infer a source class.

For replay, the exact supplied `input_source_classes` list is echoed into the immutable collider result body.

## Rules

- Each entry binds one `source_receipt_id` to one declared source class.
- `source_class` is provenance metadata only; it does not establish truth.
- Collider MUST NOT upgrade a source class.
- Collider MUST NOT create a confidence score.
- The canonical Collider result still has no `confidence` field.
- A downstream/materialized confidence-like assertion is non-canonical and MUST be checked against `input_source_classes`.
- If all supporting inputs are `operator_relayed`, no downstream assertion may claim provenance stronger than `unverified` / observed-only.
- `operator_relayed` support may still be displayed as operator-relayed; it may not be laundered into corroborated/high/strong confidence.
- Missing `input_source_classes` blocks provenance-promotion evaluation; it does not imply captured provenance.
- This field does not alter graph edges, verification state, event state, or authority.

## V13 resolution

V13 is re-scoped from "skip because provenance field absent" to an executable laundering barrier:

```text
IF all input_source_classes == operator_relayed
AND a candidate/materialized sidecar asserts confidence above unverified
THEN FAIL OPERATOR_RELAYED_CONFIDENCE_PROMOTION
```

The deliberately invalid `confidence` field in the V13 test fixture is test input only. It is not added to the canonical Collider schema.
