# MaxwellMatchMax — Employee GeoJSON Standard v0.1

**Class:** public-record work-role geospatial replay  
**Scope:** employees, officials, contractors, offices, programs, and official work events  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Prime rule

> Map the **employment / official-duty edge**, not the private person.

```text
EMPLOYEE != PRIVATE-LIFE TARGET
PUBLIC OFFICE != PRIVATE HOME
OFFICIAL TRAVEL != PERSONAL TRAVEL
WORK EXPENSE != PERSONAL PURCHASE
EMPLOYMENT RELATIONSHIP != MISCONDUCT
GEO MATCH != CAUSATION
```

## Eligible GeoJSON nodes

A feature may represent:

- employer / agency / company;
- office / duty station / publicly listed workplace;
- employee or official **in a work role**;
- title / rank / position;
- contract or program assignment;
- official meeting;
- official travel event;
- public hearing / court appearance / filing;
- procurement / award / grant execution site;
- public campaign or government event;
- public work-related communication tied to a documented event;
- publicly released case exhibit where location is materially relevant.

## Excluded nodes

Do not create GeoJSON from:

- private home addresses;
- inferred intimate relationships;
- sexual-life claims;
- personal purchases unrelated to an official case record;
- personal payment-account activity;
- precise private location data;
- family-member location inference;
- rumor-only coordinates.

If an otherwise private fact is explicitly material in an official public court or investigative record, store only the minimum public-record abstraction required for the proposition and never add extra private-location detail.

## Required properties

```json
{
  "employee_id": "stable project identifier",
  "actor_name": "public name",
  "employer": "agency/company/office",
  "role": "title on event date",
  "employment_state": "EMPLOYEE|OFFICIAL|CONTRACTOR|FORMER|HOLD",
  "event_type": "OFFICIAL_MEETING|DUTY_TRAVEL|COURT|CONTRACT|PROGRAM|HEARING|OTHER_WORK",
  "event_time_start": "ISO-8601 or null",
  "event_time_end": "ISO-8601 or null",
  "place_name": "public work/event location",
  "place_precision": "VENUE|CITY|STATE|COUNTRY|HOLD",
  "authority_source": "source URI or null",
  "record_source": "source URI",
  "source_date": "YYYY-MM-DD",
  "evidence_state": "PROVEN|BOUND|HOLD|CONFLICT|REJECT",
  "misconduct_inferred": false,
  "private_location_inferred": false
}
```

## CrissCrossBoxD match

Matches are calculated only across work/public-record features:

```text
EMPLOYEE ROLE @ TIME
        +
PUBLIC WORK LOCATION
        +
OFFICIAL EVENT / PROGRAM / CONTRACT
        +
SOURCE RECEIPT
        ↓
CANDIDATE WORK OVERLAP
        ↓
RECEIPT GATE
        ↓
BOUND | HOLD | CONFLICT | REJECT
```

A match never promotes to wrongdoing by itself.

## MaxwellMatchMax

For Maxwell/Epstein/Trump or any other corpus, the matcher may compare:

- documented employee/official roles;
- official meeting locations;
- agency/court/contract locations;
- dated public travel records;
- public work events;
- released records that identify a work-role presence.

It must not expand those records into private-life surveillance.

## Standing order

> **Map the job. Map the office. Map the official event. Map the authority. Leave the private person alone.**
