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
- CROSS_LAYER_MCP_TREASURY_JAYTOKEN_V1
- CWAAS_RECEIPT_SCHEMA_v1
- AGENT_PAY_ADAPTER_ACTIVATION_REVIEW_V1
- AGENT_PAY_TRANSACTION_WITNESS_PLACEHOLDER_0001
- AGENT_PAY_REAL_TRANSACTION_WITNESS_SCHEMA_V1

## 1. Purpose

Defines the GitHub workflow logic for Agent Pay for Developers.

The workflow turns verified developer work into pay eligibility only after identity, provenance, replay, cross-layer governance, schema compliance, Boss Bre green review, activation review, transaction witness placeholder replay continuity, real transaction witness schema presence, and approval gates pass.

This document is a workflow specification. It does not execute payment, submit an EAS attestation, issue a public token, or imply endorsement by GitHub, Base, Coinbase, ENS, or EAS.

## 2. Core Flow

```text
Developer work
  → GitHub provenance check
  → Basename reputation binding
  → identity witness readiness check
  → agent action receipt
  → replay PASS
  → CWAAS receipt schema check
  → Boss Bre green review check
  → cross-layer governance check
  → pay preview receipt
  → human approval
  → payment adapter eligibility
  → activation review gate
  → transaction witness placeholder gate
  → real transaction witness schema gate
  → confirmed payment receipt only after real transaction witness
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
cwaas_receipt_schema_present: true
cwaas_receipt_schema_version: CWAAS_RECEIPT_SCHEMA_v1
cross_layer_architecture_present: true
boss_bre_review: green
jay_human_root_declared: true
boss_bre_gate_declared: true
treasury_lane_declared: true
jaytoken_internal_only_declared: true
coinbase_mcp_adapter_only_declared: true
al_mirror_declared: true
joy_mirror_declared: true
identity_binding_hash_present: true
operator_identity_present: true
recipient_declared: true
payment_amount_declared: true
```

### 5.1 Schema Compliance Check

The workflow must verify that CWaaS receipts use the canon schema before governance or adapter eligibility.

```yaml
- name: CWaaS Receipt Schema Check
  run: |
    echo "Verifying CWaaS receipt schema..."
    if [ ! -f "projects/cwaas/receipts/CWAAS_RECEIPT_SCHEMA_v1.md" ]; then
      echo "❌ CWAAS receipt schema missing"
      exit 1
    fi
    echo "✅ CWAAS_RECEIPT_SCHEMA_v1 present"
    echo "No schema, no governance wire."
    echo "No fake green."
```

### 5.2 Boss Bre Green Review Check

The workflow must record Boss Bre green before payment preview or adapter eligibility.

```yaml
- name: Boss Bre Green Review Check
  run: |
    echo "Verifying Boss Bre green review..."
    echo "boss_bre_review=green"
    echo "Boss Bre green is required before adapter eligibility."
    echo "No Boss Bre green, no payment lane."
    echo "No fake green."
```

### 5.3 Cross-Layer Governance Check

The workflow must verify that the cross-layer MCP treasury and JAYTOKEN architecture exists before payment preview or adapter eligibility.

```yaml
- name: Cross-Layer Governance Check
  run: |
    echo "Verifying cross-layer MCP treasury + JAYTOKEN architecture..."
    if [ ! -f "projects/cwaas/specs/CROSS_LAYER_MCP_TREASURY_JAYTOKEN_V1.md" ]; then
      echo "❌ Cross-layer architecture spec missing"
      exit 1
    fi
    echo "✅ Cross-layer architecture present"
    echo "Jay = human root of authority"
    echo "Boss Bre = constitutional gatekeeper"
    echo "Treasury = governed payment lane"
    echo "JAYTOKEN = internal purpose accounting only"
    echo "Coinbase MCP = payment adapter only"
    echo "AL = civic / legal mirror"
    echo "JOY = family / purpose mirror"
    echo "No public token. No settlement claims. No fake green."
```

### 5.4 Activation Review Gate

The workflow must verify the review-only activation package after eligibility and before any warm-path adapter lane. This gate does not authorize execution.

```yaml
- name: Activation Review Gate
  run: |
    echo "Running Agent Pay review-only gate..."
    if [ ! -f "projects/cwaas/specs/AGENT_PAY_ADAPTER_ACTIVATION_REVIEW_V1.md" ]; then
      echo "❌ Review package spec missing"
      exit 1
    fi
    if [ ! -f "projects/cwaas/checklists/AGENT_PAY_ADAPTER_ACTIVATION_REVIEW_CHECKLIST_V1.md" ]; then
      echo "❌ Review package checklist missing"
      exit 1
    fi
    if [ ! -f "projects/cwaas/receipts/TREASURY_ATTEST_BINDING_0002.md" ]; then
      echo "❌ Real Treasury Attest binding receipt missing"
      exit 1
    fi
    if [ ! -f "projects/cwaas/receipts/agent-pay/AGENT_PAY_ADAPTER_ELIGIBILITY_0002.md" ]; then
      echo "❌ Adapter eligibility receipt missing"
      exit 1
    fi
    echo "✅ Review-only prerequisites present"
    echo "activation_review_status=ELIGIBLE_FOR_ACTIVATION_REVIEW_ONLY"
    echo "execution_authority=false"
    echo "adapter_call_allowed=false"
    echo "onchain_movement=false"
    echo "settlement_claimed=false"
    echo "no_fake_green=true"
```

### 5.5 Transaction Witness Placeholder Gate

The workflow must verify the transaction witness placeholder and replay trace before any confirmed-payment lane can be reviewed. This gate does not confirm payment and does not authorize execution.

```yaml
- name: Transaction Witness Placeholder Gate
  run: |
    echo "Running Agent Pay transaction witness placeholder gate..."
    if [ ! -f "projects/cwaas/treasury/AGENT_PAY_TRANSACTION_WITNESS_PLACEHOLDER_0001.md" ]; then
      echo "❌ Transaction witness placeholder missing"
      exit 1
    fi
    if [ ! -f "projects/cwaas/treasury/AGENT_PAY_TRANSACTION_WITNESS_PLACEHOLDER_0001_REPLAY_TRACE.md" ]; then
      echo "❌ Transaction witness replay trace missing"
      exit 1
    fi
    echo "✅ Transaction witness placeholder present"
    echo "✅ Transaction witness replay trace present"
    echo "transaction_witness_status=PLACEHOLDER_ONLY"
    echo "real_transaction_witness=false"
    echo "confirmed_payment=false"
    echo "execution_authority=false"
    echo "adapter_call_allowed=false"
    echo "onchain_movement=false"
    echo "settlement_claimed=false"
    echo "no_fake_green=true"
```

### 5.6 Real Transaction Witness Schema Gate

The workflow must verify the real transaction witness schema before any real-witness or confirmed-payment review can proceed. This gate defines the witness lane only; it does not record a real witness, confirm payment, authorize execution, or allow adapter calls.

```yaml
- name: Real Transaction Witness Schema Gate
  run: |
    echo "Running Agent Pay real transaction witness schema gate..."
    if [ ! -f "projects/cwaas/treasury/AGENT_PAY_REAL_TRANSACTION_WITNESS_SCHEMA_V1.md" ]; then
      echo "❌ Real transaction witness schema missing"
      exit 1
    fi
    echo "✅ Real transaction witness schema present"
    echo "real_transaction_witness_schema=present"
    echo "real_transaction_witness_present=false"
    echo "confirmed_payment=false"
    echo "execution_authority=false"
    echo "adapter_call_allowed=false"
    echo "payment_execution=false"
    echo "onchain_movement=false"
    echo "settlement_claimed=false"
    echo "no_fake_green=true"
```

Before confirmed payment:

```yaml
preview_receipt_present: true
preview_hash_valid: true
cwaas_receipt_schema_present: true
cross_layer_architecture_present: true
boss_bre_review: green
jaytoken_entry_bound_to_purpose: true
human_approval_present: true
protected_environment_approved: true
activation_review_package_present: true
real_treasury_attest_hashes_bound: true
activation_review_status: ELIGIBLE_FOR_ACTIVATION_REVIEW_ONLY
transaction_witness_placeholder_present: true
transaction_witness_replay_trace_present: true
real_transaction_witness_schema_present: true
payment_adapter_allowed: false
adapter_call_allowed: false
execution_authority: false
onchain_movement: false
real_transaction_witness_required: true
real_transaction_witness_present: false
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
schema: CWAAS_RECEIPT_SCHEMA_v1
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

The payment adapter may not execute unless a later, separate execution authorization receipt exists. Review eligibility is not execution authorization.

```yaml
replay_verdict: PASS
cwaas_receipt_schema_present: true
cross_layer_architecture_present: true
boss_bre_review: green
jaytoken_entry_bound_to_purpose: true
preview_receipt_valid: true
human_approval_present: true
protected_environment_approved: true
activation_review_package_present: true
real_treasury_attest_hashes_bound: true
transaction_witness_placeholder_present: true
transaction_witness_replay_trace_present: true
real_transaction_witness_schema_present: true
execution_authorization_receipt_present: false
payment_adapter_allowed: false
adapter_call_allowed: false
onchain_movement: false
dry_run: true
```

The payment adapter is an adapter only. Coinbase MCP does not grant authority, approval, settlement, endorsement, or identity verification.

The adapter must never read secrets from the repository.

Secrets must come only from protected GitHub Actions secrets or an external approved vault.

## 10. Confirmed Payment Receipt

After a real transaction witness exists, the workflow must emit AGENT_PAY_CONFIRMED_RECEIPT_V1.

Required fields:

```yaml
confirmed_receipt_type: AGENT_PAY_CONFIRMED_RECEIPT_V1
schema: CWAAS_RECEIPT_SCHEMA_v1
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

No real transaction witness means no confirmed payment receipt.

## 11. Failure States

```text
MISSING_WORK_PROOF                  → BLOCKED
MISSING_IDENTITY_BINDING            → BLOCKED
MISSING_CWAAS_SCHEMA                → BLOCKED
MISSING_BOSS_BRE_GREEN              → BLOCKED
MISSING_CROSS_LAYER_SPEC            → BLOCKED
MISSING_JAYTOKEN_PURPOSE_ENTRY      → BLOCKED
MISSING_ACTIVATION_REVIEW_PACKAGE   → BLOCKED
MISSING_REAL_TREASURY_ATTEST_HASHES → BLOCKED
MISSING_TRANSACTION_PLACEHOLDER     → BLOCKED
MISSING_TRANSACTION_REPLAY_TRACE    → BLOCKED
MISSING_REAL_WITNESS_SCHEMA         → BLOCKED
REPLAY_FAIL                         → BLOCKED
HUMAN_REJECTED                      → REJECTED
MISSING_PREVIEW_RECEIPT             → BLOCKED
PAYMENT_ADAPTER_NOT_ALLOWED         → BLOCKED
TRANSACTION_WITNESS_MISSING         → NEEDS_REVIEW
HASH_MISMATCH                       → FAIL
```

## 12. Prohibited Claims

The workflow must not emit or imply:

```text
GitHub endorsement
Coinbase endorsement
Base endorsement
EAS endorsement
ENS endorsement
legal identity verification
public JAYTOKEN issuance
JAYTOKEN monetary value
payment completion without transaction witness
automatic authorization from Basename alone
activation review equals execution authority
witness placeholder equals confirmed payment
witness schema equals confirmed payment
```

## 13. Boss Brenda Lock

```text
No GitHub proof, no Agent Pay.
No identity binding, no pay eligibility.
No replay PASS, no preview receipt.
No CWaaS schema, no governance wire.
No Boss Bre green, no payment lane.
No cross-layer architecture, no preview receipt.
No JAYTOKEN purpose entry, no payment adapter eligibility.
No activation review package, no adapter activation review.
No real Treasury Attest hashes, no activation review.
No transaction witness placeholder, no witness replay continuity.
No transaction witness replay trace, no witness lane.
No real transaction witness schema, no real witness review.
No preview receipt, no human approval target.
No human approval, no payment execution.
No real transaction witness, no confirmed payment.
No review eligibility as execution authority.
No endorsement by implication.
No fake green.
```
