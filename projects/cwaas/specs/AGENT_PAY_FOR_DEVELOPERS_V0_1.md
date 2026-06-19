# AGENT_PAY_FOR_DEVELOPERS_V0_1

Status: DRAFT_LOCKED  
Lane: CWaaS / Developer Payments  
Mode: Receipt-first, human-approved, no autonomous treasury execution

## 1. Purpose

Agent Pay for Developers defines a GitHub-native workflow where verified developer contributions can become pay-eligible events.

This is not automatic payroll.
This is not an endorsement by GitHub, Coinbase, Base, or any payment provider.
This is not financial advice.

It is a replayable payment eligibility layer for developer work.

## 2. Core Thesis

```text
Developers should be paid from verifiable work receipts, not vague promises.
```

CWaaS turns developer work into a replayable chain:

```text
ISSUE / TASK
  → PULL REQUEST
  → REVIEW / MERGE
  → WORK RECEIPT
  → REPLAY VERDICT
  → PAY ELIGIBILITY RECEIPT
  → HUMAN APPROVAL
  → PAYMENT ADAPTER
  → PAYMENT RECEIPT
```

## 3. Required Inputs

A developer payment cannot become eligible unless these exist:

```yaml
repo: <owner/repo>
issue_id: <github_issue_or_task_id>
pull_request_id: <github_pr_number|null>
commit_sha: <git_commit_sha>
work_receipt_id: <receipt_id>
work_receipt_hash: <sha256>
replay_trace_id: <trace_id>
replay_verdict: PASS
review_status: APPROVED|MERGED|MAINTAINER_ACCEPTED
payee_identifier: <github_user|wallet|email|basename>
payment_amount: <amount>
payment_asset: USD|USDC|ETH|OTHER
human_approval: REQUIRED
```

## 4. Payment States

Allowed states:

```text
DRAFT
WORK_VERIFIED
PAY_ELIGIBLE
APPROVAL_REQUIRED
APPROVED_FOR_PAYMENT
PAYMENT_SUBMITTED
PAYMENT_CONFIRMED
BLOCKED
REJECTED
```

## 5. Non-Negotiable Gates

```text
No merged/reviewed work, no pay eligibility.
No work receipt hash, no pay eligibility.
No replay PASS, no pay eligibility.
No human approval, no payment execution.
No payment transaction witness, no payment confirmed.
```

## 6. GitHub Workflow Role

GitHub Actions may:

- detect completed work
- verify required files
- compute hashes
- emit pay eligibility receipts
- request protected environment approval
- prepare a payment adapter command
- commit payment receipts back to the repo

GitHub Actions may not silently execute payments in v0.1.

## 7. Coinbase / CDP / Base Role

A payment adapter may later route through Coinbase, CDP, Base, USDC, or another approved rail.

However, CWaaS v0.1 treats payment execution as blocked unless:

```yaml
human_approval: true
protected_environment: passed
receipt_hash_present: true
replay_verdict: PASS
payment_adapter_reviewed: true
```

## 8. Pay Eligibility Receipt Shape

```yaml
type: AGENT_PAY_ELIGIBILITY_RECEIPT_V0_1
receipt_id: PAY_ELIGIBLE_0001
repo: jsonwisdom/COMPUTERWISDOM
issue_id: <issue_or_task>
pull_request_id: <pr_number|null>
commit_sha: <sha>
work_receipt_hash: <sha256>
replay_trace_id: <trace_id>
replay_verdict: PASS
payee: <developer_identifier>
amount: <amount>
asset: <asset>
state: PAY_ELIGIBLE
human_approval_required: true
payment_executed: false
```

## 9. Payment Confirmation Receipt Shape

```yaml
type: AGENT_PAYMENT_CONFIRMED_RECEIPT_V0_1
receipt_id: PAYMENT_CONFIRMED_0001
pay_eligibility_receipt_id: PAY_ELIGIBLE_0001
payment_rail: <coinbase|cdp|base|manual|other>
payment_tx_hash: <tx_or_provider_reference>
amount: <amount>
asset: <asset>
payee: <developer_identifier>
confirmed_at_utc: <iso8601>
operator: <github_user_or_agent>
```

## 10. Prohibited Claims

Agent Pay for Developers may not claim:

```text
GitHub endorsement
Coinbase endorsement
Base endorsement
guaranteed income
employment relationship
automatic payroll
legal approval
tax compliance
```

unless independently proven by a separate receipt.

## 11. Boss Brenda Lock

```text
No work receipt, no pay eligibility.
No replay PASS, no pay eligibility.
No human approval, no payment execution.
No transaction witness, no confirmed payment.
No endorsement by implication.
No fake green.
```
