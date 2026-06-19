# TEST_VECTOR_SET_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Replay Infrastructure  
Depends on:
- RECEIPT_SCHEMA_V1
- TREASURY_GATE_V0_2
- REPLAY_TRACE_FORMAT_V1
- BASE_ATTESTATION_FLOW_V1
- AGENT_ACTION_RECEIPT_V1

## 1. Purpose

Test vectors allow independent reviewers to:

- verify replay determinism
- confirm schema enforcement
- validate treasury gate logic
- detect drift
- detect invalid receipts
- confirm that CWaaS does not produce fake green

These vectors are non-narrative, non-endorsement, and non-execution.

## 2. Replay Invariant

```text
RECEIPT + INPUTS + HASH RULES + VERIFIER VERSION
  -> SAME VERDICT
```

If any vector produces a different verdict under the same declared rules, the system is not green.

## 3. Test Vector Categories

CWaaS v0.1 requires five categories:

1. PASS — valid receipt, valid gate, valid replay
2. FAIL — schema or hash invalid
3. DRIFT — valid receipt but lineage mismatch
4. BLOCKED — constitutional violation
5. REJECTED — human explicitly rejected

Each category must be reproducible.

## 4. Vector 1 — PASS

Receipt:

```text
EVENT_001_TREASURY_ATTEST_V0.md
```

Replay Trace:

```text
TRACE_0001_REPLAY_EVENT_001.md
```

Expected Checks:

```yaml
schema_valid: true
hash_valid: true
treasury_gate_valid: true
execution_state_valid: true
human_approval_valid: true
```

Expected Verdict:

```text
PASS
```

Expected Disposition:

```text
SETTLED
```

This is the canonical PASS vector.

## 5. Vector 2 — FAIL

Receipt:

```text
EVENT_FAIL_001_INVALID_SCHEMA.md
```

Failure Condition:

```yaml
schema_valid: false
```

or

```yaml
hash_valid: false
```

Expected Verdict:

```text
FAIL
```

Expected Disposition:

```text
QUARANTINED
```

This proves schema enforcement is real.

## 6. Vector 3 — DRIFT

Receipt:

```text
EVENT_DRIFT_001_VALID_BUT_MISMATCH.md
```

Failure Condition:

```yaml
previous_receipt_hash: <value>
previous_hash_valid: false
```

Expected Verdict:

```text
DRIFT
```

Expected Disposition:

```text
NEEDS_REVIEW
```

This proves CWaaS detects replay divergence.

## 7. Vector 4 — BLOCKED

Receipt:

```text
EVENT_BLOCKED_001_UNAPPROVED_EXECUTION.md
```

Failure Condition:

```yaml
execution_state: EXECUTED
human_approval_valid: false
```

Expected Verdict:

```text
BLOCKED
```

Expected Failure Class:

```text
MISSING_HUMAN_APPROVAL
```

Expected Disposition:

```text
BLOCKED
```

This proves the treasury constitution is enforced.

## 8. Vector 5 — REJECTED

Receipt:

```text
EVENT_REJECTED_001_HUMAN_DECLINED.md
```

Failure Condition:

```yaml
human_approval: REJECTED
```

Expected Verdict:

```text
REJECTED
```

Expected Disposition:

```text
REJECTED
```

This proves CWaaS respects human governance.

## 9. Required Files for Test Vector Set

Each vector must include:

- receipt file
- expected replay trace
- expected verdict
- expected disposition
- expected failure class, if any
- expected hash

This ensures full reproducibility.

## 10. Boss Brenda Lock

```text
No schema, no green.
No receipt hash, no authority.
No replay trace, no settlement.
No human approval, no treasury execution.
No deterministic verdict, no green.
No endorsement by implication.
No fake green.
```
