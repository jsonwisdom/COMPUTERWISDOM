# Jason's FUCK_PLANE — Lost in Translation v0.1

**Internal query alias:** `FUCK_PLANE`  
**Public label:** `AIRCRAFT_TRAVEL_REPLAY`  
**Codename:** `Lost in Translation / 迷失翻译 / Míshī Fānyì`  
**Class:** public-record aircraft / authority / GeoJSON replay  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Source authority split

```text
justice.gov  = primary DOJ disclosure / court-record surface
congress.gov = legislative authority / congressional oversight surface
quantum.gov  = technology-policy surface only
```

`quantum.gov` does not create DOJ, FBI, prosecutorial, judicial, evidentiary, or congressional authority for this replay.

## Primary SDNY receipt — corrected identifier

**DOJ artifact:** `EFTA00028716`  
**Subject:** `RE: Epstein flight records`  
**Timestamp:** `2020-01-08 00:56:36 UTC` (`2020-01-07 19:56:36 ET`)  
**Publisher:** U.S. Department of Justice Epstein Library / Data Set 8

The released SDNY AUSA email states that newly received flight records reflected Donald Trump listed as a passenger on **at least eight flights between 1993 and 1996**, including **at least four flights on which Ghislaine Maxwell was also present**. It also states that on one 1993 flight Trump and Epstein were the only two listed passengers.

The email says the team had finished reviewing the full records, described as more than 100 pages of small script. This is an official released prosecutorial review statement. It is **not** the row-level manifest for all eight flights.

```text
EFTA_EMAIL_RECEIPT = EFTA00028716
TRUMP_FLIGHTS_1993_1996 >= 8 = BOUND_TO_OFFICIAL_SDNY_EMAIL
MAXWELL_COPRESENCE_ON_THOSE_FLIGHTS >= 4 = BOUND_TO_OFFICIAL_SDNY_EMAIL
ROW_LEVEL_DATES = HOLD_PENDING_LOG_MATCH
ROW_LEVEL_TAILS = HOLD_PENDING_LOG_MATCH
ROW_LEVEL_ORIGIN_DESTINATION = HOLD_PENDING_LOG_MATCH
ROW_LEVEL_GEOJSON = HOLD_PENDING_LOG_MATCH
```

## Maxwell / Blanche executive interview

DOJ's published Maxwell interview materials establish recorded proffer sessions on **July 24 and July 25, 2025** involving Deputy Attorney General Todd Blanche and Ghislaine Maxwell. The proffer occurred at the Office of the U.S. Attorney for the Northern District of Florida.

```text
MAXWELL_BLANCHE_PROFFER_DATES = 2025-07-24 / 2025-07-25
MAXWELL_BLANCHE_PROFFER_VENUE = USAO_NDFL
BLANCHE_INTERVIEWED_MAXWELL = PROVEN
EXECUTIVE_PROFFER != COURT_HEARING
NDFL_VENUE != TRANSFER_OF_SDNY_JURISDICTION
REASON_FOR_NDFL_VENUE = HOLD
```

## 2026 DOJ release-process receipt

DOJ's January 2026 release statement says **more than 500 attorneys and reviewers** contributed to the Epstein Files Transparency Act production. It also says USAO-SDNY used an **additional review protocol** to comply with a court order requiring certification that victim-identifying information would not be produced unredacted.

Therefore the public release process is not modeled as a one-person review system.

```text
DOJ_2026_RELEASE_REVIEWERS = 500_PLUS / BOUND_TO_DOJ_RELEASE
SDNY_ADDITIONAL_COURT_ORDER_REDACTION_PROTOCOL = PROVEN_TO_DOJ_RELEASE
SINGLE_POINT_OF_FAILURE_PATEL = REJECTED_AS_RELEASE_PROCESS_MODEL
PATEL_PERSONALLY_REVIEWED_EVERY_SOURCE = HOLD
COURT_ORDER_PROTOCOL != PROOF_OF_EACH_REDACTION_DECISION
```

## Congressional production receipt

The House Oversight Committee publicly states that Chairman Comer issued an Epstein-records subpoena on **2025-08-05** and that the Committee released **33,295 pages** of DOJ-provided Epstein-related records on **2025-09-02**.

```text
HOUSE_OVERSIGHT_SUBPOENA_DATE = 2025-08-05
HOUSE_OVERSIGHT_RELEASE_DATE = 2025-09-02
HOUSE_OVERSIGHT_RELEASED_PAGES = 33295
CONGRESSIONAL_PRODUCTION = PROVEN_TO_COMMITTEE_RELEASE
```

## Corpus-integrity membrane

A large public production, a court-order review protocol, and a congressional production do not establish byte-for-byte identity across every source set.

```text
FULL_RELEASE_BYTE_FOR_BYTE_AUTHENTICATION = HOLD
FULL_CORPUS_SHA256_MANIFEST = HOLD_NOT_PUBLICLY_ACQUIRED
CORPUS_EQUIVALENCE_SDNY_2020_TO_DOJ_2026 = HOLD
SAME_TOPIC != SAME_BYTES
SAME_FLIGHT_COUNT != SAME_ROWS
OFFICIAL_RELEASE != FULL_CORPUS_AUTHENTICATION
```

## Other actor gates

```text
BIDEN_EFTA_STATUTE_EDGE = NOT_APPLICABLE_TO_PRESIDENTIAL_TERM_TIMING
OBAMA_VERIFIED_MISCONDUCT_EDGE = NOT_ESTABLISHED
ELECTRONIC_SEARCH_COMPLETENESS = HOLD
```

DOJ warns that handwritten/scanned material may not be reliably electronically searchable. Search failure is therefore never promoted to `NAME_ABSENT` or `FLIGHT_ABSENT`.

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
AGGREGATE_COUNT != ROW_LEVEL_MANIFEST
TAIL_NUMBER != AIRFRAME_ID
```

## Privacy membrane

The ETL may emit named passenger fields only for public figures or other names explicitly approved for publication. Private persons, victims, witnesses, minors, and non-public passengers are reduced to counts or stable redacted tokens. The public GeoJSON must not reproduce sensitive identifying information merely because a source PDF contains it.

## Row schema

```json
{
  "flight_id": "TRUMP_1993_01",
  "date": "YYYY-MM-DD",
  "tail_number": "N908JE | N909JE | N212JE | UNKNOWN",
  "origin": {
    "code": "IATA/ICAO/UNKNOWN",
    "city": "city or null",
    "country": "country or null"
  },
  "destination": {
    "code": "IATA/ICAO/UNKNOWN",
    "city": "city or null",
    "country": "country or null"
  },
  "public_passengers": {
    "donald_trump": false,
    "ghislaine_maxwell": false,
    "jeffrey_epstein": false
  },
  "other_passenger_count": 0,
  "source_uri": "https://www.justice.gov/...",
  "source_sha256": "sha256 of acquired source bytes",
  "source_page_or_line": "page / exhibit / row pointer",
  "raw_row_sha256": "sha256 of normalized raw row text",
  "edge_state": "PROVEN | BOUND | HOLD | CONFLICT | REJECT",
  "misconduct_inferred": false
}
```

## GeoJSON rule

A route becomes a `LineString` only when both endpoints are source-bound to a specific row. If only cities are known, city-centroid precision is allowed and must be labeled `CITY_APPROX`. If either endpoint is unresolved, emit a non-spatial audit row and keep the geographic edge `HOLD`.

```text
SOURCE ROW
→ DATE
→ AIRCRAFT / TAIL
→ ORIGIN
→ DESTINATION
→ PUBLIC-FIGURE PASSENGER FLAGS
→ SOURCE HASH
→ GEOJSON
```

The extractor must not manufacture eight rows from the aggregate email. Promotion occurs only when a flight-log row is matched to an acquired source row.

## CrissCrossBoxD

```text
FORWARD
AIRCRAFT → REGISTRATION → LOG ROW → DATE → ROUTE → PASSENGER → DOJ/COURT SOURCE

REVERSE
DOJ/SDNY CLAIM → SOURCE DOCUMENT → DATE WINDOW → FLIGHT LOG → ROW → AIRCRAFT → ROUTE
```

The pincer closes only where both directions resolve to the same source-bound row.

## ReceiptOS regression law

```text
SAME_ENDPOINT != SAME_HISTORY
OFFICIAL_RELEASE != FULL_CORPUS_AUTHENTICATION
COURT_ORDER_PROTOCOL != PROOF_OF_EACH_REDACTION_DECISION
500_PLUS_REVIEWERS != ONE_PERSON_CONTROLLED_EVERY_REVIEW
AGGREGATE_FLIGHT_EMAIL != ROW_LEVEL_MANIFEST
```

## Standing order

> **Names are cheap. Rows are expensive. Freeze the date, name the custodian, separate executive interview from court action, hash the exact bytes, then draw the line.**
