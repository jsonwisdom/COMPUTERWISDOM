# ReverseReplayAzureNSA + Rendition Integration v0.1

Status: DRAFT / REVIEW-ONLY / UNMERGED

```text
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
CLAIM_PROMOTION = HUMAN_REVIEW_REQUIRED
```

## Purpose

Integrate historically documented CIA aircraft/rendition questions into the existing COMPUTERWISDOM Dual Onion / receipt-first architecture without collapsing movement, custody, authority, legality, or cloud infrastructure into one claim.

This document is an audit architecture. It does not allege that any named current person committed a crime, participated in rendition, or acted unlawfully.

## Core chain

```text
PUBLIC / DECLASSIFIED CLAIM
→ AIRCRAFT OBJECT
→ FLIGHT / TRANSFER EVENT
→ SOURCE RECORD
→ RAW BYTES / CANONICAL RECORD
→ TIME / PLACE
→ CUSTODY EDGE, IF SUPPORTED
→ AUTHORITY EDGE
→ APPROPRIATION / CONTRACT EDGE, IF RELEVANT
→ DOJ / FBI PARTICIPATION EDGE, IF SUPPORTED
→ OVERSIGHT JURISDICTION
→ RECEIPT
→ REPLAY
→ PASS | HOLD | CONFLICT | REJECT
```

## Dual Onion split

### Onion A — Record

Question: what happened according to the record?

```text
AIRCRAFT
→ REGISTRATION / TAIL IDENTIFIER, IF PUBLICLY BOUND
→ FLIGHT LEG
→ DATE / TIME
→ ORIGIN / DESTINATION
→ PASSENGER / CUSTODY RECORD, IF AVAILABLE
→ SOURCE
→ VERSION / HASH
→ CORROBORATION
→ REPLAY
```

### Onion B — Power

Question: who had authority to do what?

```text
ACTOR / AGENCY
→ OFFICE / ROLE
→ CLAIMED AUTHORITY
→ STATUTE / EXECUTIVE / POLICY BASIS
→ ACTION
→ IMPLEMENTATION
→ OVERSIGHT / NOTICE
→ CONSEQUENCE
→ RECEIPT
→ REPLAY
```

Evidence in one onion may not pay for a missing edge in the other.

## Infrastructure overlay

```text
RAW GOVERNMENT RECORD
→ COLLECTION / MISSION SYSTEM
→ AGENCY DATA STORE
→ ACCESS CONTROL
→ CLOUD / ON-PREM HOST
→ QUERY
→ EXPORT
→ GEOJSON / CSV / REPORT REPRESENTATION
→ AUDIT LOG
```

Boundaries:

```text
CLOUD_PROVIDER != DATA_OWNER
HOSTING != COLLECTION_AUTHORITY
AZURE_ACCESS != GOVERNMENT_AUTHORITY
GEOJSON_EXPORT != ORIGINAL_RECORD
GEOLOCATION_RECORD != PERSON_IDENTITY_PROVEN
COLOCATION != MEETING_PROVEN
MEETING != MISCONDUCT
```

## Aircraft / rendition boundaries

```text
AIRCRAFT_USE != AUTHORITY
FLIGHT_LOG != LEGAL_JUSTIFICATION
FLIGHT_RECORD != PASSENGER IDENTITY
PASSENGER IDENTITY != CUSTODY STATUS
CUSTODY_TRANSFER != LAWFULNESS
RENDITION_LABEL != TORTURE_FINDING
PUBLIC REPORT != COMPLETE CLASSIFIED RECORD
CLASSIFICATION != LAWFULNESS
```

## OIG / congressional jurisdiction router

DOJ OIG has stated that it does not have oversight authority over CIA operations or personnel. Therefore:

```text
CIA_OPERATION / CIA_PERSONNEL
→ CIA OIG / INTELLIGENCE OVERSIGHT / CONGRESSIONAL INTELLIGENCE COMMITTEES

DOJ / FBI PERSONNEL, FUNDS, PROGRAMS, RECORDS, QUERIES, OR PARTICIPATION
→ DOJ OIG

DOD EDGE
→ DOD OIG / ARMED SERVICES / INTELLIGENCE OVERSIGHT AS APPLICABLE

DHS EDGE
→ DHS OIG / HOMELAND SECURITY OVERSIGHT AS APPLICABLE
```

Cross-agency events may require more than one oversight lane. Jurisdiction is an edge to prove, not an assumption.

## Public-source anchors

- DOJ OIG, review of FBI handling of intelligence related to September 11: states DOJ OIG lacked oversight authority over CIA operations/personnel while examining FBI-CIA interactions.
  - https://oig.justice.gov/sites/default/files/archive/special/s0606/chapter5.htm
- DOJ OIG testimony on detainee interrogation techniques: documents limited DOJ OIG ability to assess CIA personnel while examining FBI involvement and observations.
  - https://oig.justice.gov/node/733
- DOJ OIG, Report on the President's Surveillance Program: interagency IG review involving DOD, DOJ, CIA, NSA, and ODNI.
  - https://oig.justice.gov/reports/report-presidents-surveillance-program-unclassified-prepared-offices-inspectors-general
- Congress.gov, H. Rept. 109-374: public congressional record addressing extraordinary rendition and oversight jurisdiction.
  - https://www.congress.gov/committee-report/109th-congress/house-report/374/1
- CIA, historical U-2 program monograph: public/declassified example establishing that CIA aircraft programs can be treated as source-bound historical objects without inferring unrelated operations.
  - https://www.cia.gov/resources/csi/books-monographs/the-cia-and-the-u-2-program-1954-1974/

## Promotion rule

```text
CLAIM
→ SOURCE
→ AUTHORITY
→ ACTION
→ RECEIPT
→ REPLAY

MISSING EDGE = HOLD
VALID BOUND RECORDS DISAGREE = CONFLICT
BOUND EVIDENCE CONTRADICTS SCOPED CLAIM = REJECT
MECHANICALLY SUPPORTED SCOPED CLAIM = PASS
```

## Relationship to existing surfaces

```text
FUCK PLANE EMPIRE = SATIRE / PUBLIC INTERFACE ONLY
REVERSE_REPLAY_AZURE_NSA = INFRASTRUCTURE / ACCESS / PROVENANCE LAYER
CIA_AIRCRAFT_AUDIT = OBJECT / EVENT LAYER
RENDITION_REPLAY = CUSTODY / AUTHORITY / OVERSIGHT LAYER
COMPUTERWISDOM = ARCHITECTURE + VERIFIER SURFACE
RECEIPTOS / REPLAYOS = PROMOTION / RECEIPT DISCIPLINE
```

No satire label is evidence. No aircraft object, flight record, cloud host, intelligence affiliation, or oversight gap creates a criminal conclusion.
