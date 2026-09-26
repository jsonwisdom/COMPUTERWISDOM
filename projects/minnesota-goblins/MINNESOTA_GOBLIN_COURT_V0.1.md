# MINNESOTA GOBLIN COURT DOCKETS v0.1

Status: PROPOSAL / PUBLIC-GAME LAYER
Authority: false
Purpose: satirical replay of public Minnesota court metadata with explicit separation between real records and fictional characters.

## Core Stack

```text
MINNESOTA COURT RECORD
        ↓
CASE NUMBER
COUNTY / DISTRICT
REAL JUDICIAL OFFICER
FILED EVENTS
PUBLIC DOCUMENTS
        ↓
GOBLIN COURT CARD
        ↓
CLAIM → RECEIPT → REPLAY
        ↓
MATCH / DELTA / HOLD
```

## Separation Rule

REAL JUDGE != GOBLIN
REAL LITIGANT != GOBLIN
ALLEGATION != FACT
NOT FOUND ONLINE != NO CASE

The Goblin is a fictional/satirical game character. Real judges, parties, attorneys, allegations, findings, and case outcomes remain attributed only to the underlying public court record.

Artwork, captions, rankings, and game mechanics must not convert an allegation, filing, charge, or incomplete record into a factual accusation.

## Card Fields

- GOBLIN: fictional/satirical character
- JUDGE: actual public docket metadata when available
- COURT: actual Minnesota court
- CASE #: actual public case number
- EVENT: actual docket event
- RECEIPT: public source document or official record page
- REPLAY: previous docket event → next docket event
- RESULT: MATCH / DELTA / HOLD

## Result Logic

### MATCH
The game claim matches the cited public record.

### DELTA
The cited record differs from the prior state, prior event, or displayed claim. Show the difference without inferring motive.

### HOLD
Evidence is unavailable, incomplete, inaccessible online, ambiguous, sealed/confidential, outside the selected court system, or otherwise insufficient to score MATCH or DELTA.

HOLD is not an accusation and not an exoneration.

## Minnesota Source Rails

### District / Trial Courts
Minnesota Court Records Online (MCRO) provides online access to many public Minnesota state district-court records and documents. Courthouse public-access terminals can provide more complete electronic district-court access than MCRO.

Official source: Minnesota Judicial Branch — Access Case Records
https://mncourts.gov/access-case-records

### Appellate Courts
Minnesota Supreme Court and Court of Appeals records use the public view of the Minnesota Appellate Courts Case Management System (P-MACS).

Official source: Minnesota Judicial Branch — Access Case Records / Clerk of Appellate Courts
https://mncourts.gov/access-case-records
https://mncourts.gov/clerk-of-appellate-courts/help

## MCRO HOLD Conditions

The Minnesota Judicial Branch states that MCRO cannot be used to find pending criminal matters by defendant-name search. Pending criminal matters require other search keys such as case number, citation number, attorney name, or attorney bar number. Exact-name behavior and unavailable/older case records can also cause searches to return no result.

Therefore:

```text
NO MCRO RESULT
    ≠
NO CASE
```

A missing online result must become HOLD unless another authoritative record establishes the state.

Official source: MCRO Frequently Asked Questions
https://mncourts.gov/access-case-records/mcro/faqs

## Replay Invariant

Every published Goblin Court card must preserve this order:

```text
SOURCE → EXTRACT → CLAIM → RECEIPT → REPLAY → RESULT
```

No meme layer may overwrite the source layer.
No result may be upgraded from HOLD without a new receipt.
No fictional character may be represented as a real judicial officer or party.

## Minimal Machine Record

```json
{
  "game": "minnesota-goblin-court",
  "version": "0.1",
  "authority": false,
  "source_system": "MCRO|P-MACS|COURTHOUSE|OTHER_OFFICIAL",
  "case_number": null,
  "court": null,
  "county_or_district": null,
  "judicial_officer": null,
  "event_date": null,
  "event_label": null,
  "receipt_uri": null,
  "previous_event": null,
  "next_event": null,
  "goblin_character": null,
  "claim": null,
  "result": "HOLD",
  "notes": []
}
```

## Public Tagline

**Minnesota Goblin Court: where every meme has to survive the docket.** 👹🧾⚖️
