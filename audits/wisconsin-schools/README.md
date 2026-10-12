# Southwest Wisconsin School Budget BitBot v0.1

Status: REVIEW_OPEN  
Mode: CHAOS_AUDIT  
Geographic scope: CESA 3 / southwest Wisconsin  
Authority created: false

## Mission

Test public school-budget claims by following each material number backward to source bytes and authorization, and forward to certified levy, debt, expenditure, audit, and DPI reporting where available.

```text
CHAOS_ENABLED = TRUE
ASSUME_FRAUD = FALSE
SEARCH_FOR_ANOMALIES = TRUE
AUTOMATIC_FRAUD_LABEL = FALSE
PROMOTION_REQUIRES_EVIDENCE = TRUE
AUTHORITY_CREATED = FALSE
```

## BitBot chain

```text
PUBLIC SOURCE
→ FETCH / BYTE IDENTITY
→ TYPE CLASSIFICATION
→ OWNER + FISCAL YEAR
→ FUND / KIND
→ MEETING / MOTION / VOTE / CERTIFICATION
→ LEVY / REFERENDUM / DEBT
→ ACTUAL EXPENDITURE
→ INDEPENDENT AUDIT
→ DPI REPORT
→ CRISSCROSS
→ HOLD | SUPPORT | CONTRADICT | ANOMALY_CANDIDATE
```

BitBot verifies source identity and replayable changes. Ziggy/LeahPrime classify and explain. Gray Baby names missing edges. Human review decides what any anomaly means.

## Mandatory guardrails

- `LEVY != BUDGET`
- `PROPOSAL != VOTE`
- `VOTE != CERTIFICATION`
- `CERTIFICATION != SPEND`
- `SOURCE_FOUND != TRAIL_CLOSED`
- `ANOMALY != FRAUD`
- `ACCOUNTING_ERROR_CANDIDATE != MISCONDUCT`
- `RECEIPT != TRUTH`
- `OBSERVATION != AUTHORITY`
- `EVIDENCE_OF_RECORDING_STATE != EVIDENCE_OF_WORLD_STATE`

No automated output may accuse a person, district, board, employee, vendor, or institution of fraud or criminal conduct.

## Primary public-source rails

1. CESA 3 — geographic/member-district boundary.
2. Wisconsin DPI WiSFPR — tax levy, referenda, debt service, reporting status, shared-cost comparison, comparative revenue/cost.
3. Individual district official sites — budgets, notices, board packets/minutes, referendum materials, audited financial statements.
4. Independent audit reports and source documents — exact bytes preserved or hash-bound when captured.

## Compatibility gate

Before comparing districts or years:

```text
SAME_TYPE + SAME_FISCAL_YEAR + SAME_UNIT
```

Then expose differences in fund, accounting scope, district, enacted/proposed state, debt structure, enrollment/valuation context, and provenance.

## Review posture

This branch is a review surface. It does not authorize GitHub merge, district contact, law-enforcement contact, publication of accusations, wallet/signing actions, or institutional authority.
