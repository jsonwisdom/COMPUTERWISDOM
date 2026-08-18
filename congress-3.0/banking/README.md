# Congress 3.0 — Citizen Banking Burden Flip

**Operator label:** `jaywisdom.base.eth`  
**Parent lane:** `congress-3.0`  
**Classification:** `BOUNDED_BANKING_STATUTORY_BURDEN_REPLAY`  
**Authority created:** `false`

## Purpose

Model the point at which a federal banking or consumer-finance rule initially permits or requires information from an individual, and the later statutory or regulatory trigger that places a specific duty on a bank, creditor, consumer reporting agency, furnisher, or debt collector to explain, verify, reinvestigate, correct, delete, or pause collection.

```text
CITIZEN_PROOF_REQUEST
  -> CITIZEN_RESPONSE
  -> INSTITUTION_ACTION
  -> QUALIFYING_STATUTORY_TRIGGER?
  -> INSTITUTION_DUTY
  -> INSTITUTION_RECEIPT
  -> REPLAY
```

## Core membrane

```text
CITIZENSHIP != AUTOMATIC_CONSTITUTIONAL_CLAIM
PRIVATE_BANK_ACTION != GOVERNMENT_ACTION_BY_DEFAULT
BANK_ACTION != ECOA_ADVERSE_ACTION
DISPUTE != FCRA_TRIGGER_UNLESS_APPLICABLE_CONDITIONS_BOUND
DEBT_CLAIM != FDCPA_DEBT_COLLECTOR
PERMISSION_TO_REQUEST_ID != UNLIMITED_RECURSIVE_REPROOF
STATUTORY_DUTY_TRIGGERED != STATUTORY_VIOLATION_PROVEN
MISSING_INSTITUTION_RECEIPT != MISCONDUCT_PROVEN
```

## v0.1 trigger families

1. `CIP_ACCOUNT_OPENING` — 31 U.S.C. § 5318(l) / 31 CFR 1020.220.
2. `ECOA_ADVERSE_ACTION` — 15 U.S.C. § 1691(d) / Regulation B, 12 CFR 1002.9.
3. `FCRA_CRA_DISPUTE` — 15 U.S.C. § 1681i.
4. `FCRA_FURNISHER_DIRECT_DISPUTE` — Regulation V, 12 CFR 1022.43.
5. `FDCPA_WRITTEN_DISPUTE_30D` — 15 U.S.C. § 1692g(b).

## Terminal meanings

```text
PASS     = trigger conditions and required institutional receipt reconcile
HOLD     = trigger may exist but a required condition or receipt is missing
CONFLICT = valid bound records disagree
REJECT   = case attempts an invalid semantic promotion
```

The verifier classifies the supplied evidence packet. It does not determine legal liability, damages, constitutional violations, or regulatory enforcement outcomes.
