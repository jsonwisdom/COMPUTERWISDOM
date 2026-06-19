# AGENT_PAY_PREVIEW_HUMAN_APPROVAL_GATE_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Pay / Human Approval / Preview Receipts

## Purpose

Defines the human approval gate required after an Agent Pay preview receipt is generated and before any payment adapter can become eligible.

This gate governs the transition:

```text
PREVIEW_GENERATED
  → HUMAN_APPROVED
  → PAYMENT_ADAPTER_ELIGIBLE
```

It does not execute payment.  
It does not call a payment adapter.  
It does not touch Base, Coinbase, EAS, or any treasury surface.

## Approval Command

Approval must be explicit and human-authored:

```text
/approve-agent-pay
```

The command must appear in one of the following approved surfaces:

```text
GitHub issue comment
GitHub PR comment
designated approval receipt file
```

Automated systems may not issue this command on behalf of the human.

## Required Inputs

```yaml
preview_receipt_path: projects/cwaas/receipts/preview-dispatch/PREVIEW_1_V2.json
preview_receipt_hash: 9a9ffe769241b85b2561917988c56454437eed786286317bce94a1ff3a32344b
preview_replay_trace: PREVIEW_1_V2_REPLAY_TRACE.md
developer_basename: jaywisdom.base.eth
github_identity: jsonwisdom
human_review_required: true
external_action: false
```

## Gate Checks

```yaml
preview_receipt_present: true
preview_hash_valid: true
preview_replay_pass: true
human_review_required: true
external_action: false
payment_execution_claimed: false
chain_action_claimed: false
settlement_claimed: false
```

If any required check fails, the gate output must be `BLOCKED`.

## Gate Output

If `/approve-agent-pay` is present and valid:

```yaml
approval_status: HUMAN_APPROVED
transition: PREVIEW_GENERATED_TO_PAYMENT_ADAPTER_ELIGIBLE
payment_executed: false
chain_action: false
```

If rejected:

```yaml
approval_status: REJECTED
transition: PREVIEW_GENERATED_TO_BLOCKED
payment_executed: false
chain_action: false
```

## Boundary Conditions

This gate does not:

```text
execute payment
submit transaction
call Coinbase
call Base
call EAS
create settlement
confirm payment
verify legal identity
imply endorsement
```

It only proves that the preview receipt has a human approval target.

## Boss Bre / Boss Brenda Lock

```text
No preview receipt, no approval target.
No replay PASS, no approval target.
No human approval, no payment adapter eligibility.
No payment adapter eligibility, no execution path.
No transaction witness, no confirmed payment.
No fake green.
```
