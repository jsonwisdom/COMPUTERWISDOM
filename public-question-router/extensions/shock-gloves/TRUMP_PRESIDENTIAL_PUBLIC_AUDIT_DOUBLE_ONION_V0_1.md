# Trump Presidential Public Audit — Double Onion v0.1

Status: DRAFT / PUBLIC-AUDIT QUESTION SURFACE / UNMERGED

Current office-holder source: White House identifies Donald J. Trump as the 45th & 47th President of the United States.

Official source:
- https://www.whitehouse.gov/administration/donald-j-trump/

```text
NAMED_PUBLIC_OFFICIAL != WRONGDOING
PRESIDENTIAL_RESPONSIBILITY != PERSONAL_EXECUTION
POLITICAL_ACCOUNTABILITY != CRIMINAL_LIABILITY
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
```

## Purpose

Provide a deterministic public-question surface for auditing presidential actions that may connect to DOJ programs, national-security claims, congressional appropriations, law-enforcement technology, contracts, travel, procurement, or other executive-branch implementation.

The audit does not begin with guilt. It begins with a named office, a specific action, and a missing or disputed authority/record edge.

## Double Onion

### Onion A — Public Record

```text
PUBLIC QUESTION
→ SPECIFIC PRESIDENTIAL ACTION
→ EXECUTIVE ORDER / MEMORANDUM / PROCLAMATION / STATEMENT
→ AGENCY IMPLEMENTATION RECORD
→ APPROPRIATION / PROGRAM RECORD
→ CONTRACT / GRANT / TASK ORDER
→ INVOICE / PAYMENT / RECEIVING RECORD
→ POLICY / DEPLOYMENT / INCIDENT RECORD, IF RELEVANT
→ PUBLIC ACCESS / WITHHOLDING RECORD
→ COURT / OIG / CONGRESS RECORD
→ CONTRADICTION CHECK
→ RECEIPT
→ REPLAY
```

### Onion B — Authority

```text
PRESIDENT
→ ARTICLE II AUTHORITY, IF CLAIMED
→ STATUTORY AUTHORITY, IF CLAIMED
→ DELEGATION, IF ANY
→ APPROPRIATION BOUNDARY
→ AGENCY AUTHORITY
→ PROCUREMENT / GRANT AUTHORITY
→ OPERATIONAL AUTHORITY
→ USE-OF-FORCE / ENFORCEMENT AUTHORITY, IF RELEVANT
→ OVERSIGHT JURISDICTION
→ JUDICIAL REVIEW / CORRECTION PATH
→ RECEIPT
→ REPLAY
```

## Hard membranes

```text
EXECUTIVE_ORDER != APPROPRIATION
APPROPRIATION != PURCHASE
PURCHASE != DEPLOYMENT
DEPLOYMENT != USE
USE != LAWFUL_USE
PRESIDENTIAL_POLICY != AGENCY_RECEIPT
WHITE_HOUSE_STATEMENT != DOJ_FINDING
DOJ_STATEMENT != COURT_FINDING
CLASSIFICATION != LAWFULNESS
NATIONAL_SECURITY != AUTOMATIC_SECRECY
OIG_REVIEW != CRIMINAL_CONVICTION
COURT_FILING != FACT_PROVEN
```

## Public-question classes

A presidential question may open one or more of these lanes:

```text
PRESIDENTIAL_AUTHORITY
DOJ_IMPLEMENTATION
CONGRESSIONAL_APPROPRIATION
PROCUREMENT
LAW_ENFORCEMENT_TECHNOLOGY
NATIONAL_SECURITY
PUBLIC_RECORD_ACCESS
FOIA
OIG
COURT_RECORD
CONGRESSIONAL_OVERSIGHT
TRAVEL_LODGING
DATA_ACCESS
GEOLOCATION
CUSTODY
OTHER
```

## Shock Gloves / conducted-energy example

The phrase `Shock Gloves` remains a public-question label until device identity is proven.

```text
Q: Did any presidential or DOJ policy authorize, fund, procure, deploy, or use a specific shock-glove device?

A valid replay requires:
PRESIDENTIAL ACTION, IF ANY
→ AGENCY IMPLEMENTATION
→ APPROPRIATION
→ PROGRAM
→ CONTRACT / AWARD
→ VENDOR
→ MODEL / SKU
→ PURCHASE ORDER / INVOICE
→ RECEIVING RECORD
→ POLICY / TRAINING
→ UNIT ASSIGNMENT
→ INCIDENT / USE RECORD
→ OVERSIGHT
```

If the chain stops at general law-enforcement technology funding or a general conducted-energy-weapon standard, the device-specific claim remains HOLD.

## National-security visibility gate

If an office invokes national security, the Q-object must record:

- exact classification / exemption / exclusion authority;
- custodian;
- whether existence of records is acknowledged;
- segregability analysis or status;
- appeal/review path;
- declassification/release event, if any;
- OIG, congressional, or judicial review receipts when public.

```text
WITHHELD != NONEXISTENT
PUBLICLY_UNAVAILABLE != UNREVIEWED
INTERNAL_REVIEW != PUBLIC_REVIEW
PUBLIC_SUMMARY != FULL_RECORD
```

## DOJ OIG gate

DOJ OIG is a source-bound oversight entity for DOJ operations, personnel, grantees, contractors, and programs within its jurisdiction.

The term `OOG` is not promoted by this document:

```text
OOG = HOLD_TERM_UNRESOLVED
OIG = OFFICE_OF_INSPECTOR_GENERAL
```

## Public status clock

Every presidential public-audit question inherits the router's 24-hour portal SLA:

```text
QUESTION_ACCEPTED
→ DIRECTORY_MATERIALIZED
→ CANDIDATE_AUTHORITY_ROUTED
→ T+24 PUBLIC STATUS RECEIPT
```

The portal clock binds the portal, not the President, DOJ, Congress, OIG, or courts.

## Promotion rule

```text
SPECIFIC CLAIM
→ PRIMARY SOURCE
→ RECORD ONION PASS/HOLD/CONFLICT/REJECT
→ POWER ONION PASS/HOLD/CONFLICT/REJECT
→ CROSS-ONION CONTRADICTION TEST
→ PUBLIC REPLAY STATE
```

A green downstream record cannot repair a missing upstream authority edge.
A valid upstream authority claim does not prove that every downstream action occurred.

## Core rule

**Name the office. Name the action. Bind the text. Follow the money. Identify the object. Preserve every missing edge.**
