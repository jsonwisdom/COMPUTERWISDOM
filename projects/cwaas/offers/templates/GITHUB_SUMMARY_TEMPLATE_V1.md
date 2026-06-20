# GITHUB_SUMMARY_TEMPLATE_V1.md

**Receipt-First Agent Workflow Audit — GitHub PR / Issue Summary Template**

## Header

```text
review_target:
repo:
branch_or_pr:
auditor: jaywisdom.base.eth
status: DRAFT_REVIEW
no_fake_green: true
```

## Scope

Short description of the workflow, PR, issue, or integration under review.

## What Was Checked

- workflow files
- receipt files
- approval gates
- replay path
- adapter and payment boundaries
- public claims
- failure states

## Findings

```text
finding_001:
risk:
evidence:
recommended_fix:

finding_002:
risk:
evidence:
recommended_fix:
```

## Required Fixes Before Green

```text
fix_001:
fix_002:
fix_003:
```

## Final Review Status

```text
green_status: NOT_GREEN | REVIEW_GREEN | BLOCKED
execution_authority: false
payment_authority: false
settlement_claim: false
external_endorsement_claim: false
no_fake_green: true
```

## Boss Bre Note

Review before any warm-path activation. Public claims require evidence. No fake green.

## Boundary

This summary identifies workflow, receipt, replay, and claim-boundary issues. It does not provide legal, financial, custody, settlement, or endorsement claims.
