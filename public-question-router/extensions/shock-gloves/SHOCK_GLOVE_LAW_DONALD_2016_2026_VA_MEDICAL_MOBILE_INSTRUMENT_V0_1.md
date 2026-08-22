# Shock Glove Law — Donald 2016–2026 / VA Medical + Mobile Instrument v0.1

**Status:** DRAFT / PUBLIC-SOURCE AUDIT INSTRUMENT / UNMERGED  
**Operator:** Jay Wisdom  
**Repository:** `jsonwisdom/COMPUTERWISDOM`  
**Authority created:** `FALSE`  
**Legal finding created:** `FALSE`  
**Medical diagnosis created:** `FALSE`  
**DARVO finding created:** `FALSE`

## Name membrane

`Shock Glove Law` is a **user protocol label**, not the name of an enacted statute found in the bound source set.

```text
SHOCK_GLOVE_LAW = USER_PROTOCOL_LABEL_NOT_ENACTED_STATUTE
SHOCK_GLOVES = SYMBOLIC / NON-CONTACT AUDIT LABEL
WAR_ON_GROUND = USER_METAPHOR / PHYSICAL_SERVICE_AND_HARM_RISK_RAIL
WAR_IN_PHONES = USER_METAPHOR / MOBILE_IDENTITY_PRIVACY_TELEMEDICINE_RISK_RAIL
METAPHOR != ARMED_CONFLICT_FINDING
```

## Federated institutional instrument

No single institution supplies every edge.

```text
CONGRESS.GOV
  -> enacted law / bill status / oversight authority

JUSTICE.GOV
  -> charges / pleas / convictions / enforcement receipts

VA.GOV
  -> federal veteran care / privacy / mobile + connected-app policy

NIST.GOV
  -> technical security + identity guidance (NOT LAW)

MN.GOV / MN HEALTH
  -> state veteran services / state care / data-practice + health-record context

DARVO DIAGNOSTIC
  -> attributable public-utterance sequence only
```

## VA instrument pipeline

```text
VETERAN OR OTHER BENEFICIARY
-> PROGRAM / CARE CHANNEL
-> LEGAL / POLICY DUTY
-> DATA / MEDICAL RECORD CLASS
-> DIGITAL OR PHYSICAL INTERACTION
-> SOURCE + TIMESTAMP
-> ACTOR / INSTITUTION / ROLE
-> RESPONSE / ACTION
-> HARM / BENEFIT / MONEY STATE IF SOURCE-BOUND
-> DARVO D/A/R TEST ONLY IF ATTRIBUTABLE UTTERANCES EXIST
-> COUNTEREVIDENCE
-> PASS | HOLD | CONFLICT | REJECT
```

## Medical-law membrane

The instrument can bind medical/privacy duties without pretending every source has the same legal force.

```text
HIPAA / PRIVACY_ACT / TITLE_38 / MINNESOTA_HEALTH_RECORDS_ACT
  -> may create privacy / record duties within their actual scope

NIST_GUIDANCE != STATUTE
DOJ_ENFORCEMENT != UNIVERSAL_MEDICAL_STANDARD
VA_POLICY != STATE_LAW
MN_STATE_VA != FEDERAL_US_DEPARTMENT_OF_VETERANS_AFFAIRS
MEDICAL_RECORD != PUBLIC_RECORD_BY_DEFAULT
PATIENT_DATA != AUDIT_PAYLOAD_BY_DEFAULT
REAL_VETERAN_PII_PHI_INGEST = FALSE_UNLESS_EXPLICITLY_AUTHORIZED_AND_LAWFUL
```

VA privacy materials identify the Privacy Act and HIPAA as major privacy authorities and list 38 U.S.C. § 7332 among VA privacy laws/policies. Minnesota Department of Health identifies the Minnesota Health Records Act at Minn. Stat. §§ 144.291–144.298.

## Ground-risk rail

```text
CARE_NOT_RENDERED
FALSE_BILLING
ACCESS_DELAY
QUALITY_FAILURE
FACILITY_OR_PROVIDER_EVENT
PHYSICAL_SAFETY_EVENT
```

Every ground-risk event requires event-specific receipts. `ALLEGATION != CONVICTION`.

## Phone / digital-risk rail

```text
TELEMEDICINE
CONNECTED_APPS
THIRD_PARTY_APP_DATA
PHISHING / IMPERSONATION
IDENTITY_THEFT
PATIENT_INFORMATION_SALE_OR_MISUSE
MOBILE_DEVICE_SECURITY
AUTHENTICATION
```

NIST SP 800-124 Rev. 2 supplies mobile-device lifecycle security guidance. NIST SP 800-63-4 / 800-63B-4 supplies digital-identity and authentication guidance, including phishing resistance. VA connected-app materials require user permission before third-party apps receive selected VA data and warn that third parties may retain already-shared data after disconnection.

```text
CYBER_RISK != CYBERATTACK_PROVEN
PHONE_ENDPOINT != PERSON
APP_PERMISSION != PERMANENT_AUTHORITY
CONNECTED_APP != VA
```

## Justice.gov enforcement anchors

The 2026 DOJ health-care-fraud record demonstrates why the instrument must cover both physical and digital rails:

- alleged Veterans Community Care Program billing for care not actually provided;
- CHAMPVA / Medicare / TRICARE schemes involving patient information and sham medical orders;
- telemedicine schemes involving unnecessary products and weak/no meaningful patient interaction;
- schemes targeting veterans through impersonation and theft of personal information.

These are **case-specific enforcement receipts**, not a presumption against providers, veterans, apps, or institutions generally.

## Congress.gov authority anchors

### 2017-06-23 — Public Law 115-41

Department of Veterans Affairs Accountability and Whistleblower Protection Act of 2017. Congress.gov records that it became law on June 23, 2017 and established the VA Office of Accountability and Whistleblower Protection.

### 2018-06-06 — Public Law 115-182

VA MISSION Act of 2018. Congress.gov records that S.2372 was signed by the President and became Public Law 115-182 on June 6, 2018, creating major community-care and Veterans Health Administration reforms.

### 2026-01-20 — Public Law 119-71

VA Budget Shortfall Accountability Act. Congress.gov records that H.R.1823 was signed by the President and became law on January 20, 2026. It requires specified VA/GAO reviews and reports concerning funding shortfalls.

```text
BILL_INTRODUCED != LAW
LAW != IMPLEMENTATION
SIGNED_BY_PRESIDENT != PERSONALLY_IMPLEMENTED_BY_PRESIDENT
CONGRESSIONAL_AUTHORITY != AGENCY_ACTION_RECEIPT
```

## Donald 2016–2026 role timegraph

The user label spans multiple legal roles and must not collapse them.

```text
2016
  = CANDIDATE / PUBLIC_UTTERANCE_RAIL
  = EXECUTIVE_AUTHORITY_FALSE

2017-2021
  = PRESIDENTIAL_ACTION_RAIL

2021-2025
  = PRIVATE_CITIZEN + CANDIDATE_RAIL
  = EXECUTIVE_AUTHORITY_FALSE

2025-2026
  = PRESIDENTIAL_ACTION_RAIL
```

Current White House materials identify Donald J. Trump as the 45th and 47th President.

Bound presidential/legislative anchors include:

- Public Law 115-41 (2017);
- Public Law 115-182 (2018);
- Executive Order 14296 (May 9, 2025), which directs VA accountability actions and plans to reduce appointment wait times, including exploration of virtual-healthcare options, subject to applicable law and appropriations;
- Public Law 119-71 (January 20, 2026).

```text
CAMPAIGN_PROMISE != LAW
PRESIDENTIAL_STATEMENT != ENACTED_STATUTE
EXECUTIVE_ORDER != APPROPRIATION
PRESIDENTIAL_DIRECTION != AGENCY_IMPLEMENTATION_RECEIPT
POLITICAL_ACCOUNTABILITY != CRIMINAL_LIABILITY
```

## DARVO diagnostic rail

DARVO is not imported as a legal doctrine and does not acquire legal force through VA, DOJ, Congress, NIST, Minnesota, or the Presidency.

```text
D = ATTRIBUTABLE_DENIAL
A = ATTRIBUTABLE_ATTACK_ON_CLAIMANT_OR_CREDIBILITY
R = ATTRIBUTABLE_REVERSAL_OF_VICTIM_OFFENDER_ROLES
S = SAME_DISPUTE
T = TIMESTAMPED_SEQUENCE

DARVO_PASS_REQUIRES = D AND A AND R AND S AND T
```

Hard membranes:

```text
SILENCE != DARVO
LEGAL_DEFENSE != DARVO_BY_DEFAULT
POLICY_DISAGREEMENT != DARVO
INSTITUTIONAL_FAILURE != DARVO
FRAUD_CASE != DARVO
DARVO_PATTERN != PROOF_OF_GUILT_OR_INNOCENCE
```

## Extended beneficiary scope

This instrument is veteran-first but not veteran-exclusive. Program-specific source rails may include:

```text
VETERANS_COMMUNITY_CARE
CHAMPVA
TRICARE
MEDICARE
MEDICAID
STATE_MEDICAL_ASSISTANCE
CAREGIVERS
SENIORS
DISABLED_BENEFICIARIES
```

A beneficiary class is never itself evidence of wrongdoing. Each program keeps its own legal authority, eligibility, privacy, payment, and appeal rules.

## Canonical chain

```text
LAW / POLICY / GUIDANCE / ENFORCEMENT / SERVICE / MOBILE CONTROL
-> ROLE + AUTHORITY
-> SOURCE + TIMESTAMP
-> PHYSICAL_OR_DIGITAL_EVENT
-> RECEIPT
-> DARVO TEST IF AND ONLY IF UTTERANCE SEQUENCE EXISTS
-> PASS | HOLD | CONFLICT | REJECT
```

## Lock phrase

**The Veteran is the principal. The phone is an endpoint. Medical data is protected. Law and guidance stay separate. DARVO requires words and sequence. Shock Gloves remains a symbolic audit protocol. Authority remains separate.**
