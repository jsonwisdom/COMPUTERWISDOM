# AGENT_PAY_PREVIEW_RECEIPT_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Pay for Developers  
Depends on:
- AGENT_PAY_FOR_DEVELOPERS_V0_1
- AGENT_ACTION_RECEIPT_V1
- REPLAY_TRACE_FORMAT_V1
- TREASURY_GATE_V0_2

## 1. Purpose

An Agent Pay preview receipt is emitted before any developer payment is executed.

It is the object a human reviewer approves or rejects.

No preview receipt means no pay approval surface.

## 2. Core Rule

```text
Developer work + replay PASS + proposed payment
  → preview receipt
  → human approval decision
```

The preview receipt does not prove payment. It proves that a payment was proposed under declared rules.

## 3. Canonical JSON Shape

```json
{
  "receipt_type": "AGENT_PAY_PREVIEW_RECEIPT_V1",
  "agent_action_receipt_hash": "<sha256>",
  "replay_trace_hash": "<sha256>",
  "proposed_payment": {
    "amount": "<decimal>",
    "asset": "USDC",
    "network": "base-mainnet",
    "recipient": "<wallet-address>",
    "reason": "<human-readable>"
  },
  "work_reference": {
    "repository": "jsonwisdom/COMPUTERWISDOM",
    "pr_number": "<int|null>",
    "issue_number": "<int|null>",
    "commit_sha": "<sha>"
  },
  "generated_at": "<iso8601>",
  "preview_hash": "<sha256>"
}
```

## 4. Required Conditions

A preview receipt may only be emitted when:

```text
agent_action_receipt_hash exists
replay_trace_hash exists
replay verdict is PASS
proposed payment amount is declared
recipient is declared
asset and network are declared
```

## 5. Prohibited Claims

A preview receipt may not claim:

```text
payment executed
funds moved
transaction confirmed
Coinbase endorsement
Base endorsement
GitHub endorsement
legal approval
```

## 6. Boss Brenda Lock

```text
No work receipt, no preview.
No replay PASS, no preview.
No declared recipient, no preview.
No preview hash, no approval surface.
No payment claim before transaction witness.
No fake green.
```
