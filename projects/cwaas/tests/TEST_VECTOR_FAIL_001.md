# TEST_VECTOR_FAIL_001

Status: DRAFT_LOCKED  
Lane: CWaaS / Replay Test Vectors  
Vector Type: FAIL  
Depends on:
- RECEIPT_SCHEMA_V1
- REPLAY_TRACE_FORMAT_V1
- TEST_VECTOR_SET_V1

## 1. Purpose

This vector proves CWaaS does not emit green when a receipt is malformed or its declared hash does not match the canonical file content.

The expected outcome is deterministic failure.

## 2. Test Target

```text
EVENT_FAIL_001_INVALID_SCHEMA.md
```

## 3. Failure Condition

At least one critical validation check must fail:

```yaml
schema_valid: false
```

or

```yaml
hash_valid: false
```

## 4. Required Replay Behavior

A verifier must not repair, infer, normalize, or forgive the invalid receipt.

```text
Invalid schema or hash mismatch → FAIL
```

## 5. Expected Checks

```yaml
schema_valid: false
hash_valid: false
previous_hash_valid: null
treasury_gate_valid: null
human_approval_valid: null
execution_state_valid: null
```

Null checks are allowed only because replay stops at the failed schema/hash gate.

## 6. Expected Verdict

```text
FAIL
```

## 7. Expected Failure Class

```text
SCHEMA_INVALID
```

or

```text
HASH_MISMATCH
```

## 8. Expected Disposition

```text
QUARANTINED
```

## 9. Prohibited Outcomes

The verifier must not emit:

```text
PASS
SETTLED
ANCHOR_READY
BASE_ATTESTABLE
TREASURY_GREEN
```

## 10. Reviewer Assertion

If this vector returns `PASS`, the CWaaS replay engine is constitutionally invalid.

## 11. Boss Brenda Lock

```text
No schema, no green.
No valid hash, no authority.
No replay repair.
No inferred pass.
No fake green.
```
