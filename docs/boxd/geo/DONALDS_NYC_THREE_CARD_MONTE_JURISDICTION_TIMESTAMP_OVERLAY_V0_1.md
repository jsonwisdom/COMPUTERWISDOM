# DONALD'S NYC THREE CARD MONTE — Jurisdiction + Timestamp Overlay v0.1

**Class:** BoxD public-record jurisdiction / venue / timestamp replay  
**Story label:** `THREE_CARD_MONTE` is satire / visualization language only  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Prime correction

```text
VENUE_OF_INTERVIEW != TRANSFER_OF_PROSECUTORIAL_JURISDICTION
USAO OFFICE != FEDERAL COURT
EXECUTIVE PROFFER != COURT HEARING
DOJ RELEASE != JUDICIAL FINDING
JURISDICTION_SWITCH != CORRUPTION
GEO_MATCH != CAUSATION
```

The signed Maxwell proffer agreement states that Ghislaine Maxwell, her counsel, and Deputy Attorney General Todd Blanche would meet at the Office of the United States Attorney for the Northern District of Florida on **July 24 and 25, 2025**. It expressly says the meeting was **not a cooperation agreement** and was for the Government to evaluate Maxwell's information and responses in making prosecutive decisions.

That source establishes the meeting venue and executive-branch purpose. It does **not** establish that the Northern District of Florida assumed jurisdiction over the SDNY Maxwell criminal case, does not identify a judge or docket event, and does not explain why DOJ selected that venue.

## Three-surface overlay

### CARD 1 — NEW YORK / SDNY

```text
SURFACE = USAO-SDNY / federal criminal-investigative record
TIME    = 2019-2020 review period for Epstein/Maxwell records
OBJECT  = flight records / investigative material
```

A DOJ-released SDNY AUSA email dated January 2020 states that recently received flight records listed Donald Trump on at least eight flights between 1993 and 1996, including at least four flights on which Ghislaine Maxwell was also present. The email says the team had finished reviewing the full records, described as more than 100 pages.

```text
SDNY_AUSA_REVIEW_OF_FLIGHT_RECORDS = BOUND_TO_OFFICIAL_EMAIL
TRUMP_FLIGHTS_1993_1996 >= 8       = BOUND_TO_OFFICIAL_EMAIL
MAXWELL_COPRESENCE >= 4            = BOUND_TO_OFFICIAL_EMAIL
ROW_LEVEL_EQUIVALENCE               = HOLD_PENDING_MANIFEST_MATCH
```

### CARD 2 — FLORIDA / NDFL OFFICE

```text
SURFACE = Department of Justice executive interview / proffer
DATE_1  = 2025-07-24
DATE_2  = 2025-07-25
VENUE   = Office of the U.S. Attorney for the Northern District of Florida
ACTOR   = Deputy Attorney General Todd Blanche
OBJECT  = Maxwell proffer / interview
```

```text
BLANCHE_INTERVIEWED_MAXWELL                = PROVEN
NDFL_OFFICE_WAS_MEETING_VENUE              = PROVEN
COURT_HEARING_OCCURRED                      = REJECT
NDFL_ASSUMED_SDNY_CASE_JURISDICTION         = HOLD / NOT ESTABLISHED
REASON_FOR_NDFL_VENUE                       = HOLD
```

Do not infer the exact building, city, or coordinates unless a released source binds the interview to a specific NDFL office address.

### CARD 3 — WASHINGTON / DOJ PUBLICATION LAYER

DOJ's January 30, 2026 Epstein Files Transparency Act release states that the released corpus was collected from multiple source sets, including Florida and New York cases against Epstein, the New York case against Maxwell, New York cases investigating Epstein's death, a Florida case involving a former butler, multiple FBI investigations, and the OIG investigation into Epstein's death.

```text
MULTI-JURISDICTION_SOURCE_COLLECTION = PROVEN
BLANCHE_PERSONALLY_REVIEWED_EVERY_SOURCE = HOLD
PATEL_PERSONALLY_REVIEWED_EVERY_SOURCE   = HOLD
PATEL_AND_BLANCHE_MADE_A_SINGLE_CASE_DECISION_FROM_ALL_SOURCES = HOLD
```

Collection into one disclosure corpus does not prove that every source was used in a single prosecutive decision.

## Timestamp overlay

```text
1993-1996  = underlying flight-record window described by SDNY AUSA
2020-01    = SDNY internal email summarizing review of newly received flight records
2025-07-24 = Maxwell proffer Day 1 at USAO-NDFL venue
2025-07-25 = Maxwell proffer Day 2 at USAO-NDFL venue
2025-08-22 = DOJ public Maxwell Interview page updated with transcripts/audio
2026-01-30 = DOJ publishes large EFTA corpus from multiple source sets
2026-07-17 = DOJ Epstein Library latest-update date visible on public hub at time of this replay
```

Hard temporal rule:

```text
LATER_PROFFER != EARLIER_FLIGHT_RECORD
LATER_DOJ_RELEASE != EARLIER_PROSECUTORIAL_KNOWLEDGE
PUBLIC_NOW != PUBLIC_THEN
```

## GeoJSON overlay rules

A public geospatial feature may be emitted only when the source binds a place to the event.

```text
{
  "event_id": "MAXWELL_PROFFER_2025_DAY_1",
  "event_date": "2025-07-24",
  "authority_surface": "DOJ",
  "venue_type": "USAO_OFFICE",
  "district": "Northern District of Florida",
  "city": null,
  "coordinates": null,
  "location_precision": "DISTRICT_ONLY",
  "court_event": false,
  "jurisdiction_transfer_inferred": false,
  "corruption_inferred": false
}
```

Do not convert organization identity into a physical coordinate.

```text
SDNY_AUSA != PROOF_EMAIL_WAS_WRITTEN_IN_MANHATTAN
NDFL_USAO != PROOF_INTERVIEW_OCCURRED_AT_A_SPECIFIC_BUILDING
DOJ_HQ_RELEASE != PROOF_DECISION_WAS_MADE_AT_MAIN_JUSTICE
```

## Maxwell proffer PDF receipt manifest

DOJ's Maxwell Proffer index publicly lists these five PDFs:

```text
EFTA02846680.pdf
EFTA02846943.pdf
EFTA02847046.pdf
EFTA02847203.pdf
EFTA02847269.pdf
```

Current byte state for this BoxD replay:

```text
RAW_BYTES_ACQUIRED = false
SHA256_STATE       = HOLD_NOT_ACQUIRED
BYTE_DIFF_STATE    = WAITING
```

Do **not** invent SHA-256 values from parsed/search text. A digest is promoted only after the exact PDF bytes are acquired.

Suggested manifest:

```json
[
  {"document_id":"EFTA02846680","sha256":null,"byte_state":"HOLD_NOT_ACQUIRED"},
  {"document_id":"EFTA02846943","sha256":null,"byte_state":"HOLD_NOT_ACQUIRED"},
  {"document_id":"EFTA02847046","sha256":null,"byte_state":"HOLD_NOT_ACQUIRED"},
  {"document_id":"EFTA02847203","sha256":null,"byte_state":"HOLD_NOT_ACQUIRED"},
  {"document_id":"EFTA02847269","sha256":null,"byte_state":"HOLD_NOT_ACQUIRED"}
]
```

## Redaction edge

The DOJ Maxwell Proffer page says victim names and other identifying information were redacted. That establishes a redaction policy/result at the publication layer, but not the identity of the individual reviewer who made each redaction decision.

```text
REDACTIONS_EXIST                    = PROVEN
VICTIM_ID_PROTECTION_POLICY          = PROVEN_GENERAL
SPECIFIC_REDACTION_DECISION_MAKER    = HOLD
SPECIFIC_REASON_FOR_EACH_REDACTION   = HOLD_UNLESS_MARKED_OR_LOGGED
```

The useful missing receipt is the review/redaction log, routing sheet, or release-workflow metadata for the specific PDFs — not a presumption that a named DOJ official personally drew the redactions.

## Corpus-equivalence membrane

```text
SAME_TOPIC != SAME_BYTES
SAME_FLIGHT_COUNT != SAME_ROWS
DOJ_2026_CORPUS != AUTOMATICALLY_IDENTICAL_TO_SDNY_2020_SOURCE_SET
DUPLICATE_DOCUMENTS_MAY_EXIST != ALL_DOCUMENTS_ARE_DUPLICATES
```

A byte-for-byte diff can only be run after both versions of the purportedly same source object are acquired.

## Standing order

> **Freeze the date. Name the custodian. Separate court from prosecutor. Separate venue from jurisdiction. Hash the exact bytes. Then draw the line.**
