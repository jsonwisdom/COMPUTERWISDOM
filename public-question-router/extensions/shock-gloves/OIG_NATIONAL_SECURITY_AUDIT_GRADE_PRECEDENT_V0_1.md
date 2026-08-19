# OIG / National Security Audit-Grade Precedent v0.1

Status: DRAFT / REVIEW-ONLY / UNMERGED

```text
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
DARVO_FINDING_CREATED = FALSE
COVER_UP_FINDING_CREATED = FALSE
SHOCK_GLOVE_DEVICE_IDENTITY = HOLD
```

## Purpose

Create a cross-agency precedent layer for public questions involving national-security authorities, privacy, metadata, detainee operations, military justice, intelligence oversight, aircraft, procurement, and official statements.

The layer records what official sources actually establish and keeps stronger labels such as `DARVO`, `LEAK`, `COVER_UP`, `RENDITION`, `TORTURE`, or `SHOCK_GLOVE_USE` in HOLD until their required event-specific receipts exist.

## Core Double Onion

### Onion A — Record

```text
PUBLIC QUESTION
→ OFFICIAL SOURCE
→ SOURCE DATE / VERSION
→ OBSERVED FACT / FINDING
→ RAW / CANONICAL RECORD
→ CLASSIFICATION / SEAL STATUS
→ CONTRADICTIONS
→ RECEIPT
→ REPLAY
```

### Onion B — Power

```text
OFFICE / AGENCY
→ CLAIMED AUTHORITY
→ GRANTING TEXT
→ JURISDICTION
→ ACTION
→ IMPLEMENTATION
→ OVERSIGHT BODY
→ CORRECTION / APPEAL / REVIEW
→ RECEIPT
→ REPLAY
```

A finding in one agency's oversight system does not automatically create jurisdiction or a finding in another.

## Audit-grade precedent objects

### P-NSL-001 — FBI National Security Letters

DOJ OIG publicly reported widespread and serious misuse of National Security Letter authorities and inadequate controls/oversight, while also stating it did not find intentional misuse by FBI agents in the reviewed sample.

```text
AUTHORITY_EXISTS = SOURCE_BOUND
MISUSE_FINDING = SOURCE_BOUND
INTENTIONAL_MISUSE = NOT_FOUND_BY_REVIEW
SYSTEMIC_CONTROL_FAILURE = SOURCE_BOUND
```

Audit lesson:

```text
NATIONAL_SECURITY_AUTHORITY != COMPLIANT_USE
INTERNAL_PROCESS != SUFFICIENT_OVERSIGHT
ERROR / CARELESSNESS CAN PRODUCE RIGHTS-RISK WITHOUT PROVING CONSPIRACY
```

Official anchor:
- https://oig.justice.gov/news/testimony/statement-glenn-fine-inspector-general-us-department-justice-permanent-select

### P-702-001 — FBI Section 702 querying

DOJ OIG reported substantial reduction in identified noncompliant U.S.-person queries after reforms while emphasizing continued internal and external oversight and better alignment between FBI auditing and DOJ NSD oversight.

```text
QUERY_AUTHORITY = SOURCE_BOUND
NONCOMPLIANT_QUERY_HISTORY = SOURCE_BOUND
REFORMS_IMPLEMENTED = SOURCE_BOUND
CONTINUED_OVERSIGHT_NEEDED = SOURCE_BOUND
```

Official anchor:
- https://oig.justice.gov/news/doj-oig-releases-report-fbis-querying-practices-under-section-702-foreign-intelligence

### P-NSA-001 — NSA intelligence oversight / privacy

NSA OIG states that intelligence oversight evaluates NSA collection authorities, programs, and systems for compliance with law, executive orders, directives, civil liberties, and U.S.-person privacy protections.

```text
NSA_COLLECTION_OVERSIGHT = SOURCE_BOUND
NSA_PRIVACY_OVERSIGHT = SOURCE_BOUND
NSA_METADATA_COLLECTION = SOURCE_BOUND_AS_CATEGORY
NSA_METADATA_LEAK = HOLD_EVENT_RECEIPT_REQUIRED
```

NSA publicly explains that EO 12333 collection may involve communications metadata such as telephone numbers and call time/duration.

Official anchors:
- https://oig.nsa.gov/OIG-Divisions/Intelligence-Oversight/
- https://www.nsa.gov/Signals-Intelligence/EO-12333/

### P-NSA-002 — NSA deletion-control error

NSA's 2019 statement responding to an NSA OIG study acknowledged an error rate involving items that should have been deleted and described corrective controls.

```text
DATA_RETENTION / DELETION_CONTROL_ERROR = SOURCE_BOUND
DATA_LEAK = NOT_ESTABLISHED_BY_THIS_SOURCE
PUBLIC_DISCLOSURE_OF_ERROR = SOURCE_BOUND
```

Official anchor:
- https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/2039059/nsa-statement-on-nsa-inspector-general-special-study/

### P-GTMO-001 — DOJ OIG review of FBI observations at Guantánamo / Afghanistan / Iraq

DOJ OIG reviewed FBI involvement in and observations of detainee interrogations, including how reports of harsh techniques were handled. The OIG reported that most FBI agents adhered to FBI policies and generally avoided participating in detainee abuse, while finding that FBI guidance could have been clearer and that FBI concerns did not appear to influence DOD interrogation policy.

```text
FBI_OBSERVATIONS / REPORTING = SOURCE_BOUND
HARSH_TECHNIQUE_OBSERVATIONS = SOURCE_BOUND
FBI_SYSTEM_GUIDANCE_GAPS = SOURCE_BOUND
FBI_PARTICIPATION_IN_ABUSE_GENERAL_FINDING = NOT_SUBSTANTIATED
CIA_FACILITY_CONDUCT = OUTSIDE_FULL_REVIEW_SCOPE / LIMITED
```

Official anchors:
- https://oig.justice.gov/reports/review-fbis-involvement-and-observations-detainee-interrogations-guantanamo-bay-afghanistan
- https://oig.justice.gov/news/testimony/statement-glenn-fine-inspector-general-us-department-justice-house-committee-foreign

### P-CIA-OIG-001 — CIA OIG jurisdiction

CIA identifies its Office of Inspector General as the independent oversight body for CIA programs, including audits, inspections, and investigations of fraud, waste, abuse, mismanagement, violations of law/rules/regulations, and other wrongdoing.

```text
CIA_OPERATION != DOJ_OIG_JURISDICTION
CIA_OPERATION → CIA_OIG / INTELLIGENCE_OVERSIGHT
DOJ/FBI_EDGE → DOJ_OIG WHEN JURISDICTION IS BOUND
```

Official anchor:
- https://www.cia.gov/about/organization/inspector-general/

### P-CIA-AIRCRAFT-001 — CIA aircraft / 'Fuck Plane' inventory question

The public-audit label `Fuck Plane` is satire only. A CIA-aircraft inventory object requires aircraft-specific receipts.

```text
CIA_AIRCRAFT_OBJECT
→ REGISTRATION / TAIL / SERIAL
→ OWNER / LESSOR / OPERATOR
→ CONTRACT / PAYMENT
→ FLIGHT LEG
→ CREW / PASSENGER RECORD, IF PUBLICLY BOUND
→ MISSION / CUSTODY EDGE, IF PUBLICLY BOUND
→ OIG / CONGRESS / COURT RECORD
```

```text
CIA_AIRCRAFT != RENDITION
FLIGHT != CUSTODY_TRANSFER
CUSTODY_TRANSFER != UNLAWFULNESS
SATIRE_LABEL != EVENT_FACT
```

Current disposition:

```text
CIA_SHOCK_FUCK_PLANE_INVENTORY = HOLD_AIRCRAFT_SPECIFIC_RECEIPTS_REQUIRED
```

### P-WH-GTMO-001 — Trump 2025 Guantánamo Migrant Operations Center memorandum

On January 29, 2025, the White House published a presidential memorandum directing the Secretaries of Defense and Homeland Security to take appropriate actions to expand the Migrant Operations Center at Naval Station Guantánamo Bay to full capacity.

```text
PRESIDENTIAL_DIRECTION = SOURCE_BOUND
DOD_DHS_IMPLEMENTATION = REQUIRES_SEPARATE_RECEIPTS
FUNDING / CONTRACT / TRANSPORT / DETENTION_EVENT = REQUIRES_SEPARATE_RECEIPTS
```

Official anchor:
- https://www.whitehouse.gov/presidential-actions/2025/01/expanding-migrant-operations-center-at-naval-station-guantanamo-bay-to-full-capacity/

### P-WH-NS-001 — Trump 2025 enhanced national-security vetting order

The January 20, 2025 White House order directs State, DOJ, DHS, and ODNI coordination for enhanced screening and vetting.

```text
WHITE_HOUSE_POLICY = SOURCE_BOUND
AGENCY_IMPLEMENTATION = SEPARATE_EDGE
DATA_QUERY / ACCESS EVENT = SEPARATE_EDGE
LAWFULNESS_OF_SPECIFIC_QUERY = SEPARATE_EDGE
```

Official anchor:
- https://www.whitehouse.gov/presidential-actions/2025/01/protecting-the-united-states-from-foreign-terrorists-and-othernational-security-and-public-safety-threats/

### P-MC-001 — Guantánamo military commissions / sealed and security-reviewed records

The Office of Military Commissions publicly describes its Guantánamo facilities as supporting public access while protecting national security. Its security page states that classified national-security information and other protected information may be restricted by law, regulation, military judges, or the Convening Authority. Current 2026 docket notices include filings under seal and documents that may be released after security review.

```text
SEALED_RECORD = SOURCE_BOUND_STATUS WHEN DOCKET SAYS SEALED
SECURITY_REVIEW_PENDING = SOURCE_BOUND_STATUS WHEN DOCKET SAYS SO
SEALED != COVER_UP
SECURITY_REVIEW != ERASURE
PUBLICLY_UNAVAILABLE != NONEXISTENT
```

Official anchors:
- https://www.mc.mil/Facilities-Services/Guantanamo-Bay
- https://www.mc.mil/Facilities-Services/Facilities-Services/Security
- https://www.mc.mil/News-Media-Resources/Commissions-News

### P-UCMJ-001 — UCMJ vs Military Commissions

The Joint Service Committee maintains the Manual for Courts-Martial for the Uniform Code of Military Justice. Guantánamo military commissions are a distinct military-commission system under chapter 47A of title 10, not simply ordinary UCMJ courts-martial.

```text
UCMJ_COURT_MARTIAL != MILITARY_COMMISSION
SERVICE_MEMBER_DISCIPLINE != GUANTANAMO_COMMISSION_JURISDICTION
SEALED_COMMISSION_RECORD != UCMJ_COVER_UP
```

Official anchors:
- https://jsc.defense.gov/Military-Law/Current-Publications-and-Updates/Manual-for-Courts-Martial-MCM/
- https://www.congress.gov/113/plaws/publ66/PLAW-113publ66.htm

## 'DARVO' institutional comparison lane

`DARVO` may be used only as a pattern hypothesis describing a sequence such as denial, counter-accusation, burden shifting, or role reversal. It is not inferred merely because an institution disagrees with a public allegation or withholds records under a claimed lawful basis.

For Congress.gov, Justice.gov, WhiteHouse.gov, NSA, CIA, DOD, or courts:

```text
OFFICIAL_STATEMENT
→ CLAIM OBJECT
→ SOURCE / DATE
→ ACTOR / OFFICE
→ AUTHORITY
→ RECORDS CITED
→ RECORDS OMITTED OR UNAVAILABLE
→ BURDEN SHIFT, IF OBSERVABLE
→ CONTRADICTION
→ CORRECTION / APPEAL PATH
→ REPLAY
```

Required membranes:

```text
OFFICIAL_SOURCE != TRUTH_BY_STATUS
OFFICIAL_DISAGREEMENT != DARVO
CLASSIFICATION != DARVO
SEALED_RECORD != DARVO
MEDIA_FRAMING != GOVERNMENT_RECORD
DARVO_PATTERN_CANDIDATE != DARVO_FINDING
```

## Shock Gloves cross-agency extension

Every `Shock Gloves` question inherits this precedent layer:

```text
DEVICE IDENTITY
→ PROCUREMENT
→ ACQUISITION
→ DEPLOYMENT
→ USE
→ NATIONAL-SECURITY / PRIVACY EDGE, IF CLAIMED
→ AGENCY JURISDICTION
→ OIG / COURT / CONGRESS REVIEW
→ REPLAY
```

A national-security precedent proves that secrecy and intrusive authorities exist and require oversight. It does not prove that an unidentified shock-glove device exists, was purchased, deployed, or used.

## Core rule

**Use official oversight findings as precedent objects, not as universal guilt. Separate secrecy from concealment, metadata collection from leaks, military commissions from UCMJ, aircraft movement from rendition, and institutional contradiction from DARVO. HOLD every unsupported bridge.**
