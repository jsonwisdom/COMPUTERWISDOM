# Shock Gloves Supply-Chain Router Extension v0.1

Status: DRAFT / REVIEW-ONLY / UNMERGED

```text
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
DEVICE_IDENTITY_PROVEN = FALSE
DEPLOYMENT_PROVEN = FALSE
USE_PROVEN = FALSE
```

## Lineage

This extension preserves the prior PR #495 safety membrane: **“Shock Gloves” is a symbolic/non-contact civic-audit label unless and until documentary receipts identify a real device.**

It adds a supply-chain path capable of promoting a bounded physical-device claim only when the required evidence exists.

## Public-question trigger

```text
PUBLIC QUESTION
→ Q-OBJECT
→ SHOCK_GLOVES_EXTENSION
→ RECORD ONION
→ POWER ONION
→ SUPPLY-CHAIN EDGES
→ VISIBILITY / NATIONAL-SECURITY EDGES
→ OIG / CONGRESS / COURT ROUTING
→ RECEIPT
→ REPLAY
→ PASS | HOLD | CONFLICT | REJECT
```

## Record Onion — what exists / what happened?

```text
IDEATION
→ PATENT / PRODUCT CLAIM
→ MANUFACTURER
→ MODEL / SKU
→ TECHNICAL SPEC
→ PROCUREMENT LISTING
→ CONTRACT / AWARD
→ TASK ORDER / PURCHASE ORDER
→ INVOICE
→ PAYMENT
→ RECEIVING REPORT
→ POLICY / TRAINING
→ UNIT ASSIGNMENT
→ LOCATION
→ USE-OF-FORCE / INCIDENT
→ MEDICAL / VIDEO / WITNESS RECORD
→ OVERSIGHT RECORD
→ RECEIPT
```

Required promotion rules:

```text
CONDUCTED_ENERGY_WEAPON_CLASS_EXISTS != SHOCK_GLOVE_EXISTS
PATENT != PROCUREMENT
APPROPRIATION != PURCHASE
PURCHASE != DEPLOYMENT
DEPLOYMENT != USE
USE != LAWFUL_USE
NIST_MEASUREMENT != FEDERAL_PROCUREMENT
```

## Power Onion — who had authority?

```text
ACTOR / OFFICE
→ CLAIMED AUTHORITY
→ GRANTING TEXT
→ JURISDICTION
→ APPROPRIATION AUTHORITY
→ PROCUREMENT AUTHORITY
→ CONTRACTING / GRANT AUTHORITY
→ POLICY AUTHORITY
→ USE-OF-FORCE AUTHORITY
→ OVERSIGHT JURISDICTION
→ REVIEW / CORRECTION PATH
→ RECEIPT
```

```text
TITLE != AUTHORITY
BADGE != LAWFULNESS
PRESIDENTIAL_ACTION != APPROPRIATION
APPROPRIATION != CONTRACT AWARD
CONTRACT AWARD != OPERATIONAL AUTHORIZATION
```

## Current source-bound state

### NIST technology class

NIST publicly documents electroshock weapons / conducted-energy weapons as a law-enforcement and military technology class and publishes measurement work for electrical output.

Status:

```text
CONDUCTED_ENERGY_WEAPON_CLASS = SOURCE_BOUND
SHOCK_GLOVE_PRODUCT_IDENTITY = HOLD
FEDERAL_SHOCK_GLOVE_VENDOR = HOLD
FEDERAL_SHOCK_GLOVE_SKU = HOLD
FEDERAL_SHOCK_GLOVE_PURCHASE = HOLD
```

Official anchors:

- https://www.nist.gov/mml/mmsd/security-technologies-group/electroshock-weapon-esw
- https://www.nist.gov/publications/test-method-measuring-electrical-output-electroshock-weapons

### Congressional spending authority

Congressional appropriations text for FY2026 includes law-enforcement technology / interoperable communications / public-safety equipment funding. This proves an appropriation/program edge only; it does not prove acquisition of a shock glove.

Official anchor:

- https://www.congress.gov/bill/119th-congress/house-bill/6938/text/pcs

```text
LAW_ENFORCEMENT_TECH_APPROPRIATION = SOURCE_BOUND
SHOCK_GLOVE_LINE_ITEM = HOLD
SHOCK_GLOVE_INVOICE = HOLD
```

## National-security / public-access lane

```text
NATIONAL_SECURITY CLAIM
→ EXACT AUTHORITY
→ CLASSIFICATION / FOIA EXEMPTION / EXCLUSION
→ CUSTODIAN
→ RECORD WITHHELD?
→ PARTIAL RELEASE POSSIBLE?
→ SEGREGABILITY
→ APPEAL / REVIEW
→ DECLASSIFICATION / RELEASE EVENT
→ RECEIPT
```

DOJ/OIP publicly describes FOIA exemptions, three narrow statutory exclusions, and the requirement to segregate and release reasonably segregable non-exempt information.

Official anchors:

- https://www.justice.gov/oip/department-justice-freedom-information-act-reference-guide
- https://www.justice.gov/oip/freedom-information-act-5-usc-552

```text
NATIONAL_SECURITY != AUTOMATIC_SECRECY
CLASSIFIED != UNREVIEWABLE
WITHHELD != NONEXISTENT
FOIA_EXCLUSION != UNIVERSAL_RECORD_ERASURE
```

## OIG router

The official DOJ term is **OIG — Office of the Inspector General**. This extension does not promote `OOG` as an official DOJ entity unless separately source-bound.

```text
OOG = HOLD_TERM_UNRESOLVED
DOJ_OIG = SOURCE_BOUND_ENTITY
```

DOJ OIG currently describes its role as independent oversight of DOJ and publishes audits, inspections/evaluations, investigations, reviews, and open recommendations.

Official anchor:

- https://oig.justice.gov/

## Presidential Public Audit lane — current office holder

The White House currently identifies Donald J. Trump as the 45th & 47th President of the United States.

Official anchor:

- https://www.whitehouse.gov/administration/donald-j-trump/

A named presidential audit question is an office/authority query, not an allegation.

```text
PRESIDENT_TRUMP
→ SPECIFIC PRESIDENTIAL ACTION / ORDER / MEMORANDUM
→ CLAIMED ARTICLE II / STATUTORY / DELEGATED AUTHORITY
→ AGENCY IMPLEMENTATION
→ APPROPRIATION
→ PROGRAM
→ CONTRACT / GRANT / TASK ORDER
→ VENDOR / PRODUCT / SKU
→ DEPLOYMENT / USE, IF ANY
→ RECORD VISIBILITY
→ OIG / GAO / CONGRESS / COURT REVIEW
→ REPLAY
```

No edge may be inferred merely from political responsibility or chain-of-command proximity.

```text
PRESIDENT != EVERY AGENCY ACTION
POLICY SUPPORT != PURCHASE
PUBLIC RHETORIC != EXECUTION RECEIPT
EXECUTIVE AUTHORITY != APPROPRIATION AUTHORITY
```

## Router questions

For every claimed device / funding / authority path, ask:

1. What exact object or device is claimed?
2. Who manufactured it?
3. What model/SKU identifies it?
4. What technical specification binds the identity?
5. What appropriation authorized the relevant spending program?
6. What award, contract, grant, task order, or purchase order connects funds to the vendor?
7. What invoice/payment/receiving record proves acquisition?
8. What policy and training records prove deployment authority?
9. What unit/location records prove assignment?
10. What incident/use-of-force record proves use?
11. What classification, exemption, or exclusion is asserted for withheld records?
12. What segregability, appeal, OIG, congressional, or judicial review exists?

## Core rule

**Treat “Shock Gloves” as a question label until a device identity is receipt-bound. Follow money and authority independently. HOLD every missing edge.**
