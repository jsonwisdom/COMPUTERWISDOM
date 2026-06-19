# AGENT_PAY_CONFIRMED_RECEIPT_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Pay for Developers  
Depends on:
- AGENT_PAY_PREVIEW_RECEIPT_V1
- AGENT_PAY_FOR_DEVELOPERS_V0_1
- AGENT_ACTION_RECEIPT_V1
- REPLAY_TRACE_FORMAT_V1
- TREASURY_GATE_V0_2

## 1. Purpose

An Agent Pay confirmed receipt records that a human-approved, replay-verified developer work event resulted in a real payment transaction.

This receipt is emitted only after a transaction witness exists.

No transaction witness means no confirmed payment receipt.

## 2. Core Rule

```text
preview receipt + human approval + payment transaction witness
  → confirmed payment receipt
  → final hash
```

## 3. Canonical JSON Shape

```json
{
  "receipt_type": "AGENT_PAY_CONFIRMED_RECEIPT_V1",
  "agent_action_receipt_hash": "<sha256>",
  "replay_trace_hash": "<sha256>",
  "human_approval": {
    "approved": true,
    "approver": "<github_username>",
    "approval_timestamp": "<iso8601>"
  },
  "payment": {
    "payment_adapter": "coinbase-mcp-v1",
    "preview_hash": "<sha256>",
    "transaction_hash": "<tx_hash>",
    "transaction_timestamp": "<iso8601>",
    "amount": "<decimal>",
    "asset": "USDC",
    "network": "base-mainnet"
  },
  "witness": {
    "adapter_response": "<opaque-json>",
    "anchor_tx_hash": "<optional-base-anchor>"
  },
  "repository": "jsonwisdom/COMPUTERWISDOM",
  "work_reference": {
    "pr_number": "<int|null>",
    "issue_number": "<int|null>",
    "commit_sha": "<sha>"
  },
  "final_hash": "<sha256-of-entire-receipt>"
}
```

## 4. Required Conditions

A confirmed receipt may only be emitted when:

```text
agent action receipt exists
replay verdict is PASS
preview receipt exists
human approval is true
payment transaction hash exists
transaction witness exists
final hash is computed
```

## 5. Rejection Rule

If human approval is false or rejected:

```text
confirmed_receipt: not emitted
payment: not executed
final_state: BLOCKED_HUMAN_REJECT
```

## 6. Prohibited Claims

A confirmed receipt may not claim:

```text
Coinbase endorsement
Base endorsement
GitHub endorsement
legal approval
employment relationship
financial advice
```

unless a separate receipt proves the claim.

## 7. Boss Brenda Lock

```text
No preview receipt, no confirmed receipt.
No replay PASS, no payment.
No human approval, no payment.
No transaction witness, no confirmed payment.
No final hash, no settlement.
No fake green.
```
