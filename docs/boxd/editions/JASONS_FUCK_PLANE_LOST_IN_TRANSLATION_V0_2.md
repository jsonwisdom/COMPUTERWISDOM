# Jason's FUCK_PLANE — Lost in Translation v0.2

**Internal query alias:** `FUCK_PLANE`  
**Public label:** `AIRCRAFT_TRAVEL_REPLAY`  
**Codename:** `Lost in Translation / 迷失翻译 / Míshī Fānyì`  
**Class:** public-record aircraft / authority / GeoJSON replay  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Primary receipt — EFTA00016732

DOJ source:
`https://www.justice.gov/epstein/files/DataSet%208/EFTA00016732.pdf`

The one-page document is an SDNY email chain titled `RE: Epstein flight records`.

Temporal membrane:

```text
TOP_REPLY_TIMESTAMP       = 2020-01-08T01:29:20Z
INTERMEDIATE_REPLY        = 2020-01-07T20:28 local display
KEY_AUSA_MESSAGE          = 2020-01-07T19:56 local display
```

The key AUSA message states that flight records received the prior day reflected that Donald Trump was listed on **at least eight flights between 1993 and 1996**, including **at least four flights on which Ghislaine Maxwell was also present**. It also says that on one 1993 flight Trump and Epstein were the only two listed passengers, and describes additional passenger-composition observations.

Important: **EFTA00016732 does not enumerate all eight dates, tail numbers, or routes.** It is an aggregate prosecutorial review statement, not the row-level flight manifest itself.

```text
TRUMP_FLIGHTS_1993_1996 >= 8              = BOUND_TO_OFFICIAL_DOJ_EMAIL
MAXWELL_COPRESENCE_1993_1996 >= 4          = BOUND_TO_OFFICIAL_DOJ_EMAIL
ONE_1993_EPSTEIN_TRUMP_ONLY_FLIGHT         = BOUND_TO_OFFICIAL_DOJ_EMAIL
ALL_8_DATES_FROM_EMAIL                     = NOT_PRESENT
ALL_8_TAILS_FROM_EMAIL                     = NOT_PRESENT
ALL_8_ROUTES_FROM_EMAIL                    = NOT_PRESENT
```

## Public log-row index currently located

A separate public/court-log corpus contains eight Trump flight **segments** if the May 15, 1994 Washington stop is counted as two legs:

| Segment | Date | Route | Tail as publicly indexed | Maxwell | State |
|---|---|---|---|---|---|
| P1 | 1993-04-23 | TEB → PBI | N108JE | no | BOUND_ROW_POINTER |
| P2 | 1993-04-26 | PBI → TEB | N108JE | no | BOUND_ROW_POINTER |
| P3 | 1993-10-11 | PBI → TEB | N108JE | yes | BOUND_ROW_POINTER |
| P4 | 1993-10-17 | PBI → TEB | N108JE | yes | BOUND_ROW_POINTER |
| P5 | 1994-05-15 | PBI → DCA | N988JE | no | BOUND_ROW_POINTER |
| P6 | 1994-05-15 | DCA → TEB | N988JE | no | BOUND_ROW_POINTER |
| P7 | 1995-08-13 | PBI → TEB | N908JC in indexed/OCR record | yes | BOUND_ROW_POINTER |
| P8 | 1997-01-05 | PBI → EWR | N908JE in indexed/OCR record | yes | BOUND_ROW_POINTER |

These rows are useful for replay but **do not close the EFTA00016732 eight-flight proposition**, because P8 is in 1997 while the AUSA email says its at-least-eight count is between 1993 and 1996.

```text
PUBLIC_INDEXED_SEGMENTS_FOUND              = 8
PUBLIC_INDEXED_SEGMENT_WINDOW              = 1993-1997
EFTA_EMAIL_WINDOW                          = 1993-1996
CORPUS_EQUIVALENCE                         = HOLD
MISSING_OR_DIFFERENT_1993_1996_ROWS        = HOLD
```

This is a corpus-resolution problem, not permission to invent a missing flight.

## Candidate row bridge

The April 26, 1993 public row is a strong candidate for the email's statement that one 1993 flight listed only Epstein and Trump, because the indexed row is PBI → TEB with those two passengers. It remains a **candidate bridge** until the exact row source reviewed by the AUSA is bound byte-for-byte.

```text
EFTA_1993_TWO_PASSENGER_NOTE
↔ 1993-04-26 PBI→TEB INDEXED ROW
= CANDIDATE_MATCH / BOUND_NOT_PROVEN_SAME_SOURCE_ROW
```

## Tail-number / airframe membrane

Aircraft registrations can be reassigned or reused over time. DOJ/FBI records concerning later years identify `N908JE` as a Boeing 727, while older flight-log material can associate the same registration string with a Gulfstream-era record.

Therefore:

```text
TAIL_NUMBER != AIRFRAME_ID
SAME_TAIL_DIFFERENT_YEAR != SAME_AIRFRAME
AIRCRAFT_TYPE_REQUIRES_DATE + REGISTRATION_HISTORY + SERIAL_NUMBER
```

GeoJSON must never use the tail number alone as a permanent aircraft node ID.

Recommended aircraft identity:

```json
{
  "aircraft_event_id": "stable project event id",
  "tail_number": "registration on event date",
  "event_date": "YYYY-MM-DD",
  "airframe_serial": "source-bound serial or null",
  "aircraft_type": "source-bound type or HOLD",
  "registration_effective_state": "BOUND|HOLD|CONFLICT",
  "registration_source": "URI or null"
}
```

## Hard membrane

```text
PASSENGER != PARTICIPANT_IN_MISCONDUCT
AIRCRAFT_WITH_BED != SEXUAL_PURPOSE
FLIGHT_TO_PALM_BEACH != FLIGHT_TO_USVI
FLIGHT_TO_USVI != PROOF_OF_CRIME
DOJ_RECORD != CRIMINAL_FINDING
GOVERNMENT_ALLEGATION != FINAL_JUDGMENT
SEARCH_FAILURE != RECORD_ABSENCE
NAME_ABSENT_FROM_ONE_LOG != NEVER_FLEW
GEO_MATCH != CAUSATION
TAIL_NUMBER != AIRFRAME_ID
AGGREGATE_COUNT != ROW_LEVEL_MANIFEST
SAME_COUNT != SAME_CORPUS
```

## CrissCrossBoxD v0.2

```text
FORWARD
AIRFRAME / REGISTRATION@DATE
→ LOG ROW
→ DATE
→ ROUTE
→ PASSENGER
→ SOURCE BYTES
→ HASH

REVERSE
EFTA00016732 AGGREGATE CLAIM
→ 1993-1996 WINDOW
→ CANDIDATE LOG CORPUS
→ ROW MATCH
→ AIRFRAME / REGISTRATION@DATE
→ ROUTE
→ SOURCE BYTES
→ HASH
```

The pincer closes only when the forward and reverse paths resolve to the **same source-bound row**, not merely the same name/date/count.

## Current state

```text
EFTA00016732_PRIMARY_RECEIPT                = PROVEN_EXISTS
EFTA_KEY_MESSAGE_DATE                       = 2020-01-07
DOCUMENT_TOP_REPLY_DATE                     = 2020-01-08
TRUMP_FLIGHTS_1993_1996 >= 8                = BOUND
MAXWELL_COPRESENCE >= 4                     = BOUND
PUBLIC_INDEXED_8_SEGMENTS_1993_1997         = BOUND
EFTA_8_ROWS_EXACTLY_IDENTIFIED              = HOLD
CORPUS_EQUIVALENCE                          = HOLD
ROW_LEVEL_PRIMARY_BYTE_HASHES               = HOLD
GEOJSON_PROMOTION                           = PARTIAL / HOLD
MISCONDUCT_INFERRED                         = FALSE
```

## Standing order

> **Same number does not mean same corpus. Freeze the year, freeze the registration, hash the row, then draw the line.**
