# AGENT_PAY_IDENTITY_REPUTATION_V0_1

Status: DRAFT_LOCKED  
Lane: CWaaS / Agent Pay / Identity + Reputation  
Depends on:
- AGENT_PAY_FOR_DEVELOPERS_V0_1
- AGENT_PAY_PREVIEW_RECEIPT_V1
- AGENT_PAY_CONFIRMED_RECEIPT_V1
- AGENT_ACTION_RECEIPT_V1
- REPLAY_TRACE_FORMAT_V1

## 1. Purpose

Agent Pay for Developers must bind payment eligibility to a replayable identity and reputation surface.

A raw wallet address is not enough.

CWaaS uses Basenames and GitHub provenance together:

```text
basename identity
  → GitHub identity
  → repository work proof
  → replay verdict
  → pay eligibility
```

## 2. Canonical Identity Example

```yaml
basename: jaywisdom.base.eth
github_owner: jsonwisdom
github_display: JSONWisdom
repository: jsonwisdom/COMPUTERWISDOM
```

This binds the developer/product lane to a human-readable Base identity and a GitHub provenance trail.

## 3. Reputation Layer Rule

Agent Pay may use a Basename as the public reputation label, but it must not rely on name text alone.

Required evidence:

```yaml
basename: <name.base.eth>
github_owner: <github_owner>
repository: <owner/repo>
commit_sha: <sha>
work_reference:
  pr_number: <int|null>
  issue_number: <int|null>
replay_verdict: PASS
```

## 4. Payment Eligibility Rule

A developer is not pay-eligible unless all are true:

```text
GitHub work reference exists
Replay verdict = PASS
Preview receipt emitted
Human approval = true
Recipient identity is declared
Payment adapter is allowed
```

## 5. Basename Safety Rule

A Basename may identify reputation, but it does not by itself prove:

```text
wallet control
legal identity
employment status
Coinbase endorsement
Base endorsement
GitHub endorsement
payment approval
```

Those claims require separate receipts.

## 6. Agent Pay Identity Binding Shape

```yaml
identity_binding_version: AGENT_PAY_IDENTITY_REPUTATION_V0_1
basename: jaywisdom.base.eth
github_owner: jsonwisdom
github_display: JSONWisdom
repository: jsonwisdom/COMPUTERWISDOM
work_reference:
  pr_number: <int|null>
  issue_number: <int|null>
  commit_sha: <sha>
recipient:
  payment_address: <wallet_address>
  network: base-mainnet
reputation_surface:
  basename_required: true
  github_required: true
  replay_required: true
```

## 7. Boss Brenda Lock

```text
No GitHub proof, no developer pay.
No replay PASS, no pay eligibility.
No declared recipient, no preview receipt.
No human approval, no confirmed payment.
Basename is reputation, not automatic authorization.
No endorsement by implication.
No fake green.
```
