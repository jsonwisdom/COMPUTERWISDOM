# Citizen Banking Burden Flip — v0.1

**Verification date:** 2026-08-17  
**Parent:** Congress 3.0 Congressional Systems Accountability  
**Classification:** `BOUNDED_BANKING_STATUTORY_BURDEN_REPLAY`  
**Legal advice:** `false`  
**Authority created:** `false`

## Research question

At what point does federal law legitimately require information or action from an individual, and at what later statutory or regulatory trigger does a covered institution acquire its own duty to explain, verify, reinvestigate, correct, delete, or pause collection?

This architecture does not assume that every private-bank action is constitutional state action. Constitutional analysis and statutory consumer-finance analysis remain separate lanes.

## Constitutional boundary

Article I, Section 8 grants Congress enumerated powers including borrowing, interstate commerce, bankruptcy, and coinage. It does not contain a general constitutional command that an individual must endlessly re-prove identity, debt, or credit facts to participate in banking.

The Fifth Amendment prohibits federal deprivation of life, liberty, or property without due process. Constitution Annotated describes due process as a limitation on government power. Private conduct is not government action merely because it occurs in a heavily regulated industry; a separate state/government-action nexus analysis is required when constitutional attribution is asserted.

```text
CITIZENSHIP != AUTOMATIC_CONSTITUTIONAL_CLAIM
PRIVATE_BANK_ACTION != GOVERNMENT_ACTION_BY_DEFAULT
FEDERAL_REGULATION_OF_BANK != EVERY_BANK_ACTION_ATTRIBUTABLE_TO_GOVERNMENT
STATUTORY_DUTY != CONSTITUTIONAL_DUTY
CONSTITUTIONAL_QUESTION != CONSTITUTIONAL_VIOLATION_PROVEN
```

## Trigger 1 — account opening / customer identification

31 U.S.C. § 5318(l) requires Treasury regulations establishing minimum identity-verification standards for financial institutions and customers in connection with opening accounts. The banking CIP rule requires a covered bank to obtain identifying information, use risk-based identity-verification procedures, keep records, and describe resolution of substantive discrepancies.

```text
ACCOUNT_OPENING
  -> CUSTOMER_IDENTIFYING_INFORMATION
  -> BANK_VERIFICATION_PROCEDURE
  -> BANK_RECORDKEEPING / DISCREPANCY_RESOLUTION
```

This is **not** a complete burden flip. The customer has an initial information burden, while the bank has independent verification and recordkeeping duties. The audit may require a bank-side provenance receipt to prove the system acted as required, but v0.1 does not claim CIP generally requires the bank to give that internal receipt to the customer.

## Trigger 2 — ECOA / Regulation B adverse action

15 U.S.C. § 1691(d) and 12 CFR 1002.9 apply to covered credit adverse action. A creditor must provide the required adverse-action notification and either give specific reasons or disclose the applicant's right to obtain specific reasons under the applicable procedure. Regulation B states that vague references to internal standards or policies are insufficient as the statement of specific reasons.

```text
CREDIT_APPLICATION / COVERED_EXISTING_CREDIT
  -> ECOA_ADVERSE_ACTION
  -> CREDITOR_NOTICE_DUTY
  -> SPECIFIC_REASONS OR RIGHT_TO_REQUEST_SPECIFIC_REASONS
```

```text
BANK_ACTION != ECOA_ADVERSE_ACTION
DEPOSIT_ACCOUNT_ACTION != AUTOMATIC_ECOA_TRIGGER
INTERNAL_POLICY_ONLY_REASON != SPECIFIC_REASON_COMPLIANCE_PROVEN
```

## Trigger 3 — FCRA consumer reporting agency dispute

15 U.S.C. § 1681i requires a consumer reporting agency, after a qualifying dispute, to conduct a reasonable reinvestigation generally within 30 days. If disputed information is inaccurate, incomplete, or cannot be verified, the CRA must delete or modify it as appropriate. Statutory extensions and exceptions remain case-specific.

```text
QUALIFYING_CRA_DISPUTE
  -> REASONABLE_REINVESTIGATION
  -> RESULT
  -> MODIFY / DELETE IF INACCURATE_INCOMPLETE_OR_UNVERIFIABLE
```

## Trigger 4 — FCRA furnisher direct dispute

12 CFR 1022.43 requires a furnisher to reasonably investigate qualifying direct disputes that satisfy the rule's scope, address, content, and other conditions, subject to listed exceptions. If reported information is found inaccurate, the furnisher must notify the CRAs to which it supplied the inaccurate information and provide the necessary correction.

```text
ANY_DISPUTE != QUALIFYING_DIRECT_FURNISHER_DISPUTE
QUALIFYING_DIRECT_FURNISHER_DISPUTE
  -> FURNISHER_REASONABLE_INVESTIGATION
  -> RESULT_TO_CONSUMER
  -> CORRECTION_TO_CRA_IF_INACCURATE
```

## Trigger 5 — FDCPA validation / disputed debt

15 U.S.C. § 1692g applies to a covered `debt collector`. Under subsection (b), when the consumer provides the qualifying written dispute within the statutory 30-day period, the debt collector must cease collection of the disputed debt or portion until it obtains verification (or other specified information) and mails the required material to the consumer.

```text
DEBT_CLAIM != FDCPA_SCOPE_PROVEN
CREDITOR != DEBT_COLLECTOR_BY_DEFAULT
QUALIFYING_WRITTEN_DISPUTE_WITHIN_30_DAYS
  -> COLLECTION_PAUSE_DUTY
  -> VERIFICATION
  -> MAIL_VERIFICATION
  -> COLLECTION_MAY_RESUME_SUBJECT_TO_LAW
```

## Burden-state machine

```text
B0 = CITIZEN_INITIAL_INFORMATION
B1 = INSTITUTION_ACTION
B2 = TRIGGER_CLASSIFICATION
B3 = TRIGGER_CONDITIONS_BOUND
B4 = INSTITUTION_STATUTORY_DUTY
B5 = INSTITUTION_RECEIPT
B6 = REPLAY
```

The key rule is:

```text
IF TRIGGER_CONDITIONS_BOUND
AND INSTITUTION_DUTY_REQUIRED
THEN MISSING_INSTITUTION_RECEIPT -> HOLD
NOT -> PUSH_PROOF_BACK_TO_CITIZEN_FOREVER
```

A `receipt` means evidence sufficient for this audit architecture to establish the required action occurred. It is not automatically a document the institution is legally required to disclose to the consumer.

## Recursive re-proof detector

```text
CITIZEN_SUPPLIED_REQUIRED_PROOF
+ QUALIFYING_TRIGGER_BOUND
+ INSTITUTION_DUTY_NOW_ACTIVE
+ SAME_PROOF_REQUESTED_AGAIN
+ NO_INSTITUTION_DUTY_RECEIPT
-> RECURSIVE_BANKING_BURDEN_SIGNAL
-> HOLD
```

The signal does not itself establish a statutory violation, constitutional violation, discrimination, damages, fraud, intent, or misconduct.

## Primary public sources

- Constitution, Article I: https://constitution.congress.gov/constitution/article-1/
- Constitution Annotated, Fifth Amendment Due Process: https://constitution.congress.gov/browse/essay/amdt5-5-1/ALDE_00013721/
- Constitution Annotated, State Action Doctrine: https://constitution.congress.gov/browse/essay/amdt14-2/ALDE_00000810/
- 31 U.S.C. § 5318(l), Customer Identification Programs: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title31-section5318
- Federal Reserve Regulations Reference, 31 CFR 1020.220: https://www.federalreserve.gov/frrs/regulations/section-1020220-customer-identification-program-requirements-for-banks.htm
- 15 U.S.C. § 1691(d), ECOA adverse action: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1691
- CFPB Regulation B, 12 CFR 1002.9: https://www.consumerfinance.gov/rules-policy/regulations/1002/9/
- 15 U.S.C. § 1681i, FCRA reinvestigation: https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section1681i
- CFPB Regulation V, 12 CFR 1022.43: https://www.consumerfinance.gov/rules-policy/regulations/1022/43/
- 15 U.S.C. § 1692g, FDCPA validation: https://uscode.house.gov/view.xhtml?req=(title:15%20section:1692g%20edition:prelim)
- Constitution Annotated, Bankruptcy uniformity: https://constitution.congress.gov/browse/essay/artI-S8-C4-2-5/ALDE_00013184/

## Uniform bankruptcy correction

The Bankruptcy Clause requires geographic uniformity, not identical personal treatment of every debtor. That doctrine is therefore not a general equal-treatment rule for all banking interactions.

## Terminal boundary

```text
STATUTORY_TRIGGER_CLASSIFIED = POSSIBLE
LEGAL_VIOLATION_PROVEN = FALSE
CONSTITUTIONAL_VIOLATION_PROVEN = FALSE
PRIVATE_ACTOR_STATE_ACTION_PROVEN = FALSE
GOVERNMENT_SUBMISSION_PERFORMED = FALSE
AUTHORITY_CREATED = FALSE
```
