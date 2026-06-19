# AGENT_PAY_GITHUB_WORKFLOW_V0_1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Pay / GitHub Workflow  
Depends on:
- AGENT_PAY_FOR_DEVELOPERS_V0_1
- AGENT_PAY_IDENTITY_REPUTATION_V0_1
- AGENT_PAY_PREVIEW_RECEIPT_V1
- AGENT_PAY_CONFIRMED_RECEIPT_V1
- IDENTITY_ATTESTATION_SCHEMA_V1
- IDENTITY_WITNESS_HUMAN_APPROVAL_GATE_V1
- REPLAY_TRACE_FORMAT_V1

## 1. Purpose

Defines the GitHub workflow logic for Agent Pay for Developers.

The workflow turns verified developer work into pay eligibility only after identity, provenance, replay, and approval gates pass.

This document is a workflow specification. It does not execute payment, submit an EAS attestation, or imply endorsement by GitHub, Base, Coinbase, ENS, or EAS.

## 2. Core Flow

```text
Developer work
  → GitHub provenance check
  → Basename reputation binding
  → identity witness readiness check
  → agent action receipt
  → replay PASS
  → pay preview receipt
  → human approval
  → payment adapter eligibility
  → confirmed payment receipt after transaction witness
```

## 3. Identity and Reputation Requirement

Agent Pay must bind pay eligibility to the identity lattice:

```text
JAYWISDOM.eth
  → jaywisdom.base.eth
  → GitHub: jsonwisdom
  → CWaaS receipts
  → EAS witness layer
  → Base settlement surface
```

A raw wallet address alone is not sufficient for developer pay eligibility.

Required identity fields:

```yaml
identity_root: JAYWISDOM.eth
operator_identity: jaywisdom.base.eth
github_identity: jsonwisdom
binding_hash: a934eb17ce56014155802c2df566f68b878511e71c41c8d722370ed703480be7
identity_binding_status: DECLARED_PENDING_EXTERNAL_WITNESS
```

## 4. Workflow Triggers

Allowed triggers:

```yaml
workflow_dispatch: true
pull_request.closed: merged_only
issue_comment: explicit_command_only
```

Disallowed in v0.1:

```text
scheduled auto-pay
auto-pay on label alone
auto-pay on merge alone
auto-pay from bot approval alone
```

## 5. Required Checks

Before pay preview receipt emission:

```yaml
github_work_present: true
commit_sha_present: true
agent_action_receipt_present: true
replay_trace_present: true
replay_verdict: PASS
identity_binding_hash_present: true
operator_identity_present: true
recipient_declared: true
payment_amount_declared: true
```

Before confirmed payment:

```yaml
preview_receipt_present: true
preview_hash_valid: true
human_approval_present: true
protected_environment_approved: true
payment_adapter_allowed: true
transaction_witness_present: true
```

## 6. Identity Witness Gate

Identity witness readiness may strengthen pay eligibility, but it does not automatically authorize payment.

Allowed states:

```text
DECLARED_PENDING_EXTERNAL_WITNESS
DRY_RUN_REPLAY_VERIFIED
HUMAN_APPROVED_PENDING_SUBMISSION
WITNESSED_CONFIRMED
```

Payment eligibility may proceed in v0.1 only when the workflow records which identity state was used.

```yaml
identity_state_used_for_pay: <state>
identity_witness_required: true|false
identity_witness_reason: <text>
```

## 7. Pay Preview Receipt

The workflow must emit an AGENT_PAY_PREVIEW_RECEIPT_V1 before any payment execution attempt.

Preview receipt minimum fields:

```yaml
receipt_type: AGENT_PAY_PREVIEW_RECEIPT_V1
agent_action_receipt_hash: <sha256>
replay_trace_hash: <sha256>
identity_binding_hash: <sha256>
recipient_basename: <basename|null>
recipient_wallet: <address>
amount: <decimal>
asset: USDC
network: base-mainnet
reason: <human-readable>
preview_hash: <sha256>
```

## 8. Human Approval Command

Payment approval must be explicit:

```text
/approve-agent-pay
```

Approval must come from:

- GitHub issue comment
- GitHub PR comment
- designated approval file
- protected GitHub environment approval

Bot-only approval is not valid in v0.1.

## 9. Payment Adapter Boundary

The payment adapter may not execute unless:

```yaml
replay_verdict: PASS
preview_receipt_valid: true
human_approval_present: true
protected_environment_approved: true
dry_run: false
```

The adapter must never read secrets from the repository.

Secrets must come only from protected GitHub Actions secrets or an external approved vault.

## 10. Confirmed Payment Receipt

After a real transaction witness exists, the workflow must emit AGENT_PAY_CONFIRMED_RECEIPT_V1.

Required fields:

```yaml
confirmed_receipt_type: AGENT_PAY_CONFIRMED_RECEIPT_V1
preview_hash: <sha256>
transaction_hash: <tx_hash>
transaction_timestamp: <iso8601>
amount: <decimal>
asset: USDC
network: base-mainnet
recipient_wallet: <address>
identity_binding_hash: <sha256>
final_hash: <sha256>
```

No transaction witness means no confirmed payment receipt.

## 11. Failure States

```text
MISSING_WORK_PROOF           → BLOCKED
MISSING_IDENTITY_BINDING     → BLOCKED
REPLAY_FAIL                  → BLOCKED
HUMAN_REJECTED               → REJECTED
MISSING_PREVIEW_RECEIPT      → BLOCKED
PAYMENT_ADAPTER_NOT_ALLOWED  → BLOCKED
TRANSACTION_WITNESS_MISSING  → NEEDS_REVIEW
HASH_MISMATCH                → FAIL
```

## 12. Prohibited Claims

The workflow may not claim:

```text
GitHub endorsement
Coinbase endorsement
Base endorsement
EAS endorsement
ENS endorsement
legal identity verification
payment completion without transaction witness
automatic authorization from Basename alone
```

## 13. Boss Brenda Lock

```text
No GitHub proof, no Agent Pay.
No identity binding, no pay eligibility.
No replay PASS, no preview receipt.
No preview receipt, no human approval target.
No human approval, no payment execution.
No transaction witness, no confirmed payment.
No endorsement by implication.
No fake green.
```
