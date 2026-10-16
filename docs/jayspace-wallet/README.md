# JaySpace Wallet — Purpose / Function / Public Strategy V0.1

**Disposition:** DESIGN_HOLD / REVIEW_ONLY
**Repository:** `jsonwisdom/COMPUTERWISDOM`
**Relationship:** Adjacent technical proof lane for existing `jsonwisdom/JOY/FAMILY/JAYSPACE`. The existing family-first JaySpace is not being rewritten.
**Financial operation:** None. **Public release of private ledger:** None.

## Purpose
Make wallet activity understandable and independently challengeable, preserving unknowns instead of inventing trades.

## Function
For each **asset + account + exact time window**, read two balance snapshots, classify complete transaction-history coverage, then join uniquely identified activity records from applicable trading, conversion, reward, transfer, fee, and correction surfaces. Recompute unit-consistent signed quantity deltas and preserve a residual.

```text
DELTA_QUANTITY = Q(t1) - Q(t0)
EXPLAINED_QUANTITY = SUM(VERIFIED_SIGNED_EVENT_QUANTITY)
UNEXPLAINED_RESIDUAL = DELTA_QUANTITY - EXPLAINED_QUANTITY
```

**Different asset units cannot be added.** For mixed cash/stablecoin estimates, conversion assumptions must be stated; marked portfolio value requires per-asset price/time decomposition and is not equivalent to a receipt for profit.

## Public strategy

- Publish the method, repository pointers, bounded verification/coverage state, and only redacted, explicitly approved receipts.
- Maintain the private Coinbase provider data, app history and account-level ledger outside public GitHub and static Pages.
- Do not put holdings, transaction IDs, tax lots, balance snapshots, financial account identifiers, or private exchange address associations in public files, URLs, Issues, workflow logs, or branch history.
- Require human approval for disclosure separately from human authorization for any financial execution.
- A public Git SHA or successful Pages build is software-publication evidence, **not evidence of reconciliation or money movement**.

## Existing authority and limitations

Reuses `audits/COINBASE_HISTORY_MEMBRANE_AUDIT_V0_1.md`: no claim of full history without pagination end, complete chunk inventory, stable-ID reconciliation, hash continuity, time-window overlap audit, and correct field semantics. Reuses `projects/cwaas/CWaaS_V0_1_COINBASE_ENABLED.md`: audit/preview separation, human authorization for execution. No autonomous trades.

The user-reported morning/evening quantity shifts are **not** embedded in this public repository. Advanced Trade fills and open orders are not sufficient to explain all Coinbase app activity. No new Coinbase transaction-history read was performed through this page or its build workflow.

## Acceptance tests

1. Public content contains no account-specific amounts, identifiers, API tokens, or trade rows.
2. Public page is linked from root `index.html`.
3. Contract parses as JSON and requires HOLD, no auto-trading, and explicit privacy and human approval gates.
4. Actions checks pass on reviewed branch.
5. After human merge approval, deployed route responds HTTP 200 and public bytes match the source revision actually intended for publishing.
6. Human visually confirms the page and approves any future redacted release.

```text
SOURCE_IMPLEMENTED != DEPLOYED
DEPLOYED != FINANCIAL_RECONCILED
UNRECONCILED != FRAUD
AUDIT_PUBLISHED != AUTHORITY_CREATED
```

No runtime provider credentials, wallet-connect code, payment functionality, private record ingestion, trade execution, or repository automation outside static inspection is included in this candidate.
