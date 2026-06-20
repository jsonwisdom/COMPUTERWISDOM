# RISK_MATRIX_TEMPLATE_V1.md

**Receipt-First Agent Workflow Audit — Risk Matrix Template**

## Header

```text
workflow_or_lane:
date:
auditor: jaywisdom.base.eth
status: DRAFT_REVIEW
no_fake_green: true
```

## Risk Categories

| Risk | Severity | Evidence Status | Fake-Green Potential | Recommendation |
|------|----------|-----------------|----------------------|----------------|
| Missing Receipt | High | TBD | High | Require receipt and hash |
| No Replay Trace | High | TBD | High | Add replay trace |
| Authority Bleed | Critical | TBD | Critical | Enforce human gate |
| Adapter vs Authority | Medium | TBD | Medium | Adapter remains tool only |
| Payment Claim Without Witness | Critical | TBD | Critical | Block until real witness |
| No Human Approval Gate | High | TBD | High | Add approval gate |
| Public Claim Without Evidence | High | TBD | High | Bind public claim to receipt |

## Overall Fake-Green Score

```text
score: TBD / 10
status: NOT_GREEN | REVIEW_GREEN | BLOCKED
```

## Boss Bre Lock

```text
No receipt, no green.
No replay, no authority.
No witness, no confirmed payment.
No fake green.
```

## Boundary

This matrix is an audit aid. It does not provide legal, financial, custody, settlement, payment, or endorsement claims.
