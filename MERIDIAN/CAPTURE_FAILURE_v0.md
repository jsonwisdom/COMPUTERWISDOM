# CAPTURE_FAILURE_v0

**Status:** FROZEN  
**Version:** 0.1.0  
**Kind:** capture_failure  
**Purpose:** Content-addressed receipt that a required byte capture did not complete.

## Schema

```yaml
capture_failure:
  schema_version: "0.1.0"
  id: "sha256:<JCS-body-hash>"
  kind: capture_failure
  target_label: ""
  url_intended: null
  reported_by: operator
  stage: fetch | tls | redirect | auth | parse | integrity | unavailable
  reason: ""
  receipt_of_absence: true
  observed_at: "ISO8601"
  supersedes: null
```

## Identity rule

Repository convention is preserved:

```text
id = "sha256:" + SHA256(RFC8785-JCS(capture_failure body excluding id))
```

The hash scope is every schema field except `id`, with no hidden metadata.

## Invariants

- A failure receipt proves only that the capture path failed or lacked bytes at the recorded observation.
- It does not prove the target document/event does not exist.
- `url_intended` remains null when no URL was supplied to the operator.
- Re-emitting an identical canonical body yields the same id.
- A retry with changed observations is a new object and may set `supersedes` to the prior failure id.
- Failure receipts never normalize into Meridian events.
- Failure receipts never populate Collider.
- Failure receipts never advance verification status.
