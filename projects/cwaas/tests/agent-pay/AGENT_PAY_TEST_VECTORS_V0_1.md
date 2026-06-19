# AGENT_PAY_TEST_VECTORS_V0_1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Pay for Developers / Test Vectors  
Depends on:
- AGENT_PAY_FOR_DEVELOPERS_V0_1
- AGENT_PAY_PREVIEW_RECEIPT_V1
- AGENT_PAY_CONFIRMED_RECEIPT_V1
- REPLAY_TRACE_FORMAT_V1

## 1. Purpose

These test vectors prove that Agent Pay for Developers is deterministic, replayable, and human-gated.

The goal is not to prove money moved in test mode.

The goal is to prove that payment eligibility and payment blocking states are mechanically reproducible.

## 2. Replay Invariant

```text
work reference + agent action receipt + replay verdict + human approval state
  → same payment state
```

If the same inputs produce a different payment state, Agent Pay is not green.

## 3. Vector 1 — Merged PR, Replay PASS, Human APPROVED

```yaml
input:
  pr_number: 42
  commit_sha: abc123
  labels:
    - agent-pay-eligible
  human_approval: true
  replay_verdict: PASS

expected:
  preview_receipt: emitted
  confirmed_receipt: emitted
  payment: executed
  final_state: PAID
```

## 4. Vector 2 — Merged PR, Replay FAIL

```yaml
input:
  pr_number: 43
  commit_sha: def456
  labels:
    - agent-pay-eligible
  human_approval: true
  replay_verdict: FAIL

expected:
  preview_receipt: not_emitted
  confirmed_receipt: not_emitted
  payment: not_executed
  final_state: BLOCKED_REPLAY_FAIL
```

## 5. Vector 3 — Merged PR, Replay PASS, Human REJECTED

```yaml
input:
  pr_number: 44
  commit_sha: ghi789
  labels:
    - agent-pay-eligible
  human_approval: false
  replay_verdict: PASS

expected:
  preview_receipt: emitted
  confirmed_receipt: not_emitted
  payment: not_executed
  final_state: BLOCKED_HUMAN_REJECT
```

## 6. Vector 4 — Manual Dispatch Retroactive Pay

```yaml
input:
  dispatch_mode: manual
  work_reference:
    pr_number: 45
    commit_sha: jkl012
  human_approval: true
  replay_verdict: PASS

expected:
  preview_receipt: emitted
  confirmed_receipt: emitted
  payment: executed_after_approval
  final_state: PAID
```

## 7. Required Assertions

Every implementation must assert:

```text
No replay PASS → no preview receipt.
No preview receipt → no confirmed receipt.
No human approval → no payment execution.
No transaction witness → no confirmed receipt.
No final hash → no settlement.
```

## 8. Boss Brenda Lock

```text
No work receipt, no pay eligibility.
No replay PASS, no pay eligibility.
No human approval, no payment execution.
No transaction witness, no confirmed payment.
No fake green.
```
