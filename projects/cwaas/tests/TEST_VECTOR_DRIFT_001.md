# TEST_VECTOR_DRIFT_001

**CWaaS DRIFT Vector — Lineage Mismatch**

type: CWaaS_TEST_VECTOR_V1  
category: DRIFT  
vector_id: TEST_VECTOR_DRIFT_001  
receipt_id: EVENT_DRIFT_001  
trace_id: TRACE_DRIFT_001  
status: DRAFT_LOCKED  
lane: CWaaS / Replay Infrastructure  

Depends on:
- RECEIPT_SCHEMA_V1
- TREASURY_GATE_V0_2
- REPLAY_TRACE_FORMAT_V1
- TEST_VECTOR_SET_V1

---

## 1. Purpose

This vector demonstrates a **deterministic DRIFT** replay outcome.

DRIFT occurs when:

```text
receipt is schema-valid
receipt hash is valid
BUT previous_receipt_hash does not match lineage
```

This proves CWaaS can detect **lineage divergence** without misclassifying it as FAIL.

---

## 2. Inputs

### Receipt — Intentionally Divergent

```yaml
receipt_path: projects/cwaas/receipts/EVENT_DRIFT_001.md
receipt_hash: <valid_sha256>
previous_receipt_hash: <incorrect_sha256>
```

The receipt is **valid**, but its declared lineage does not match the actual previous hash.

### Replay Trace — Expected

```yaml
trace_path: projects/cwaas/replay/TRACE_DRIFT_001.md
trace_hash: <sha256>
```

### Schema + Gate

```yaml
schema: RECEIPT_SCHEMA_V1
treasury_gate: TREASURY_GATE_V0_2
```

### GitHub Provenance

```yaml
github_commit: <commit_sha>
timestamp_utc: <iso8601>
```

---

## 3. Expected Checks

```yaml
schema_valid: true
hash_valid: true
previous_hash_valid: false
treasury_gate_valid: true
human_approval_valid: true
execution_state_valid: true
```

Only **previous_hash_valid** must fail.

---

## 4. Expected Verdict

```text
DRIFT
```

---

## 5. Expected Disposition

```text
NEEDS_REVIEW
```

DRIFT is not a failure. It is a **review-required divergence**.

---

## 6. Expected Failure Class

```text
PREVIOUS_HASH_MISMATCH
```

---

## 7. Expected Replay Output

```yaml
verdict: DRIFT
disposition: NEEDS_REVIEW
failure_class: PREVIOUS_HASH_MISMATCH
```

Replay must reproduce this verdict **deterministically**.

---

## 8. Prohibited Claims

This DRIFT vector does **not** assert:

```text
funds moved
trade executed
legal approval
financial advice
Coinbase endorsement
Base endorsement
GitHub endorsement
```

It is a **lineage test**, not an attestation.

---

## 9. Boss Brenda Lock

```text
No schema, no green.
No receipt hash, no authority.
No lineage match, no PASS.
DRIFT is not FAIL.
No endorsement by implication.
No fake green.
```
