# THREE PRESIDENTS, THREE-RING CIRCUS — Zero Trust Epstein Release Overlay v0.1

**Public-facing lens:** How the rich, famous, prosecutors, courts, executive officials, and Congress interact with records the public ultimately pays to create, preserve, litigate, review, redact, and release.  
**Class:** BoxD public-record / jurisdiction / release-process replay  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Prime rule

> **The receipts are the ringmaster.**

```text
OFFICIAL DOMAIN != SELF-PROVING FACT
NAME IN FILE != MISCONDUCT
PASSENGER != PARTICIPANT_IN_MISCONDUCT
NO VERIFIED EDGE FOUND != PROVEN NEGATIVE
PRESS RELEASE != COURT FINDING
CONGRESSIONAL SUBPOENA != COMPLETE PRODUCTION
CASE CUSTODY != PUBLIC BYTE-FOR-BYTE AUDIT
```

## Corrected public state

### Donald Trump

```text
SDNY_AUSA_EMAIL_2020
= OFFICIAL DOJ-RELEASED RECORD

EMAIL_SAYS_TRUMP_LISTED_ON_AT_LEAST_8_FLIGHTS_1993_1996
= BOUND_TO_OFFICIAL_EMAIL

EMAIL_SAYS_MAXWELL_PRESENT_ON_AT_LEAST_4
= BOUND_TO_OFFICIAL_EMAIL

TRUMP_CHARGED_IN_EPSTEIN_OR_MAXWELL_CASES
= NO PUBLIC CHARGE IDENTIFIED IN THIS REPLAY

ROW_LEVEL_8_FLIGHT_EQUIVALENCE
= HOLD_PENDING_MANIFEST_MATCH
```

The official email is a prosecutor's summary of flight records reviewed by SDNY. It is not itself the complete row-level manifest corpus.

### Joseph R. Biden Jr.

The Epstein Files Transparency Act became law on 2025-11-19, after the Biden presidency. Therefore `BIDEN_NONPUBLISHER` is not an evidentiary misconduct state under that Act.

```text
BIDEN_EFTA_PUBLICATION_DUTY_DURING_PRESIDENCY
= NOT_APPLICABLE

VERIFIED_DIRECT_BIDEN_EPSTEIN_MISCONDUCT_EDGE_IN_THIS_REPLAY
= NONE ESTABLISHED

PROVEN_NEGATIVE_ACROSS_ENTIRE_CORPUS
= NOT CLAIMED
```

### Barack Obama

```text
VERIFIED_DIRECT_OBAMA_EPSTEIN_MISCONDUCT_EDGE_IN_THIS_REPLAY
= NONE ESTABLISHED

PROVEN_NOT_NAMED_ANYWHERE_IN_RELEASED_CORPUS
= NOT CLAIMED
```

A debunked forged list does not prove that a name never appears anywhere in millions of pages, and DOJ warns that portions of the library are not reliably electronically searchable.

### Kash Patel / FBI leadership

```text
PATEL_FBI_LEADERSHIP_DURING_2026_RELEASE_ERA
= BOUND

PATEL_SINGLE_POINT_OF_FAILURE_FOR_EPSTEIN_RELEASE
= REJECT / UNSUPPORTED
```

DOJ states that more than 500 attorneys and reviewers participated in the 2026 production and that USAO-SDNY used an additional review protocol tied to a court order protecting victim-identifying information. No single-person raw-file custody/control model is established by the public record.

### Ghislaine Maxwell / Todd Blanche

```text
MAXWELL_PROFFER_INTERVIEW_DAY_1
= 2025-07-24

MAXWELL_PROFFER_INTERVIEW_DAY_2
= 2025-07-25

LOCATION
= U.S. ATTORNEY'S OFFICE, NORTHERN DISTRICT OF FLORIDA

TODD_BLANCHE_PARTICIPATED_AS_DOJ_INTERVIEWER
= PROVEN_TO_RELEASED_TRANSCRIPTS

INTERVIEW_TYPE
= EXECUTIVE_BRANCH_DOJ_PROFFER / NOT A COURT HEARING
```

The Maxwell criminal prosecution itself was in SDNY. Do not merge NDFL interview location with SDNY prosecution jurisdiction.

### Courts / jurisdiction overlay

```text
SDFL
= FLORIDA EPSTEIN FEDERAL CASE / PRIOR NPA-ERA JURISDICTION

SDNY
= 2019 EPSTEIN FEDERAL PROSECUTION / MAXWELL PROSECUTION / RELATED COURT ORDERS

NDFL
= 2025 MAXWELL DOJ PROFFER INTERVIEW LOCATION

D.D.C. / OTHER COURTS
= SEPARATE FOIA / RELEASE LITIGATION AS CASE-SPECIFIC
```

`NO_ARTICLE_III_ON_THIS_RELEASE` is rejected. DOJ says SDNY used an additional review protocol to comply with a court order requiring U.S. Attorney Jay Clayton to certify that victim-identifying information would not be released unredacted.

`FISC` is not established as an authority surface for the public Epstein-library release and is not used as a generic secrecy bucket.

### Congress

```text
HOUSE_OVERSIGHT_SUBPOENA_TO_DOJ_FOR_EPSTEIN_RECORDS
= PROVEN (2025-08-05)

DOJ_PRODUCTION_TO_HOUSE_OVERSIGHT
= PROVEN (33,295 PAGES PUBLICLY RELEASED 2025-09-02; ADDITIONAL PRODUCTION DESCRIBED)

EPSTEIN_ESTATE_SUBPOENA
= PROVEN

BANK_RECORD_SUBPOENAS
= PROVEN

RAW_BYTE_FOR_BYTE_INDEPENDENT_HASH_AUDIT_OF_COMPLETE_DOJ_CORPUS
= HOLD / NOT PUBLICLY ESTABLISHED IN THIS REPLAY
```

Therefore `RAW_FILES_NOT_SUBPOENAED` is rejected. The narrower unresolved question is whether Congress or another independent body possesses and has publicly authenticated a complete, byte-for-byte corpus sufficient to reproduce DOJ's deduplication, redaction, withholding, and release decisions.

## DOJ release architecture

DOJ stated on 2026-01-30 that it had published nearly 3.5 million pages, more than 2,000 videos, and 180,000 images. It described source collections including Florida and New York Epstein cases, the New York Maxwell case, Epstein-death investigations, multiple FBI investigations, and the OIG investigation.

DOJ also stated that some non-produced material fell into categories including duplicates between SDNY and SDFL investigations, privilege, statutory exceptions, and material unrelated to the case files.

That creates the reproducibility stack:

```text
SOURCE CORPUS
→ COLLECTION
→ DUPLICATE DETECTION
→ PRIVILEGE / STATUTORY WITHHOLDING
→ VICTIM-PRIVACY REVIEW
→ SDNY COURT-COMPLIANCE PROTOCOL
→ REDACTION
→ RELEASE PACKAGE
→ CONGRESSIONAL PRODUCTION
→ PUBLIC LIBRARY
```

## Remaining replay gaps

The unresolved set is broader than three items:

```text
REDUCTION / REDACTION SIGN-OFF LOGS         = PARTIAL / HOLD
COMPLETE DUPLICATE MAP                      = HOLD_PUBLIC
BYTE-FOR-BYTE PRE/POST RELEASE HASH DIFF    = HOLD_PUBLIC
WITHHOLDING / PRIVILEGE ITEMIZATION         = PARTIAL / HOLD
COURT-COMPLIANCE CERTIFICATION SET          = PARTIAL / CASE-SPECIFIC
DECLINATION / CHARGING MEMOS                = CASE-SPECIFIC HOLD
COMPLETE CHAIN OF CUSTODY ACROSS DATASETS   = HOLD_PUBLIC
INDEPENDENT COMPLETE-CORPUS REPRODUCTION    = HOLD
```

## GeoJSON + timestamp overlay

Public geospatial replay is allowed only for source-bound official or public-event locations:

```text
EVENT_DATE
→ JURISDICTION
→ COURT / USAO / DOJ OFFICE
→ DOCUMENT
→ CUSTODIAN
→ RELEASE DATE
→ PUBLIC LOCATION PRECISION
```

Hard rules:

```text
COURT_LOCATION != ACTOR_LOCATION
OFFICE_LOCATION != PRIVATE_PERSON_LOCATION
SAME_CITY != SAME_EVENT
SAME_EVENT != MISCONDUCT
GEO_MATCH != CAUSATION
```

## Three-ring lens

```text
RING 1 — EXECUTIVE
DOJ / FBI / WHITE HOUSE
→ collection, prosecution, declination, review, release

RING 2 — JUDICIAL
SDFL / SDNY / OTHER ARTICLE III COURTS
→ warrants, pleas, trials, sealing, unsealing, privacy orders, FOIA disputes

RING 3 — LEGISLATIVE
CONGRESS
→ statute, subpoena, oversight, appropriation, public production
```

No ring inherits authority from another.

## Standing order

> **Do not ask which politician owns the circus. Ask which institution possessed the record, which rule controlled it, which clock was running, who reviewed it, what changed between versions, and whether another observer can reproduce the same result from the same bytes.**

And:

> **Names are cheap. Rows are expensive. Releases are not self-auditing.**
