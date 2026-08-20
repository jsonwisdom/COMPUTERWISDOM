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
congress.gov = legislative authority / release-law surface
quantum.gov  = technology-policy surface only
```

`quantum.gov` does not create DOJ, FBI, prosecutorial, judicial, evidentiary, or congressional authority for this replay.

## Official seed receipts

1. DOJ-released SDNY email dated 2020-01-08 states that flight records reviewed by prosecutors listed Donald Trump on **at least eight flights between 1993 and 1996**, including **at least four flights on which Ghislaine Maxwell was also present**. The email is an official released prosecution record describing the prosecutors' review; it is not itself the row-level manifest.
2. DOJ hosts the released `U.S. v. Maxwell` flight logs and related court records.
3. Public Law 119-38, the Epstein Files Transparency Act, requires DOJ to publish unclassified Epstein-related records, expressly including flight logs and travel records, subject to statutory withholding/redaction provisions.
4. DOJ's Epstein Library warns that portions of handwritten/scanned material may not be reliably electronically searchable. Therefore OCR/search failure is never promoted to `NAME_ABSENT` or `FLIGHT_ABSENT`.

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

## Trump 8-flight replay state

The 2020 SDNY email supports the aggregate proposition:

```text
TRUMP_FLIGHTS_1993_1996 >= 8                  = BOUND_TO_OFFICIAL_EMAIL
MAXWELL_COPRESENCE_ON_THOSE_FLIGHTS >= 4      = BOUND_TO_OFFICIAL_EMAIL
ROW_LEVEL_DATES                                = HOLD_PENDING_LOG_MATCH
ROW_LEVEL_TAILS                                = HOLD_PENDING_LOG_MATCH
ROW_LEVEL_ORIGIN_DESTINATION                   = HOLD_PENDING_LOG_MATCH
ROW_LEVEL_GEOJSON                              = HOLD_PENDING_LOG_MATCH
```

The extractor must not manufacture eight rows from the aggregate email. Promotion occurs only when a flight-log row is matched to the aggregate statement.

## CrissCrossBoxD

```text
FORWARD
AIRCRAFT → REGISTRATION → LOG ROW → DATE → ROUTE → PASSENGER → DOJ/COURT SOURCE

REVERSE
DOJ/SDNY CLAIM → SOURCE DOCUMENT → DATE WINDOW → FLIGHT LOG → ROW → AIRCRAFT → ROUTE
```

The pincer closes only where both directions resolve to the same source-bound row.

## Standing order

> **Names are cheap. Rows are expensive. Hash the row, freeze the date, bind the route, then draw the line.**
