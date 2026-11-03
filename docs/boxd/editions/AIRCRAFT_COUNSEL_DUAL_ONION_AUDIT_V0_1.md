# Aircraft / Counsel Dual Onion Audit v0.1

**Class:** public-record relationship mapping / non-authority  
**Search alias:** `FUCK_PLANE` = aircraft-with-sleeping-accommodations query tag only  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Search-label membrane

The query alias does **not** assert sexual activity, trafficking, misconduct, criminal purpose, or any other onboard conduct. Aircraft configuration and passenger presence are separate facts.

```text
AIRCRAFT_WITH_BED != SEXUAL_PURPOSE
PASSENGER != PARTICIPANT_IN_MISCONDUCT
LAWYER_ON_PLANE != LEGAL_WORK_ON_PLANE
LAWYER_FOR_OWNER != PASSENGER
SAME_CLIENT != SAME_MATTER
GOVERNMENT_AIRCRAFT != PERSONAL_BENEFIT
PRIVATE_JET != ILLEGAL_ACTIVITY
UNKNOWN_PASSENGER = UNKNOWN
```

## Stack A — Aircraft / Travel

Required fields:

- aircraft_id
- registration_or_tail
- owner
- operator
- configuration_source
- sleeping_accommodation_status
- flight_date
- origin
- destination
- manifest_source
- passenger_name
- passenger_role_on_date
- travel_purpose_if_officially_stated
- source_kind
- raw_bytes_or_hash_status
- evidence_state

## Stack B — Lawyer / Authority

Required fields:

- lawyer_id
- lawyer_name
- bar_or_official_role
- specialty
- client_or_office
- matter
- relationship_to_aircraft
- relationship_type
- source_id
- evidence_state
- causal_claim_state

Allowed relationship types:

`ONBOARD | MANAGED_OR_ARRANGED | PROVIDED_FLIGHT_RECORDS | REVIEWED_TRAVEL_AUTHORITY | GOVERNMENT_TRAVELER | COUNSEL_TO_PASSENGER`

## Join rule

A lawyer/aircraft relationship is promoted only when Stack A and Stack B share a dated source-bound edge.

```text
JOIN_KEY = person + date + aircraft/flight + source
```

Output states:

`PROVEN | BOUND | HOLD | CONFLICT | REJECT`

## Verified seed — Epstein aircraft

### Alan Dershowitz

Public court records document that Dershowitz stated he had been on Epstein's plane on several occasions. Court records also identify him as an Epstein attorney and record Palm Beach detective testimony that Dershowitz provided flight logs to police.

```text
ONBOARD = PROVEN_FROM_PUBLIC_COURT_RECORD
COUNSEL_RELATIONSHIP = PROVEN
PROVIDED_FLIGHT_RECORDS = PROVEN
ONBOARD_MISCONDUCT = NOT_INFERRED
```

## Verified seed — Trump aircraft

### Boris Epshteyn

Contemporaneous photographic/reporting records document Epshteyn boarding Trump's airplane with Trump after the June 13, 2023 Miami federal arraignment.

```text
ONBOARD = BOUND/PROVEN_PHOTO_RECORD
LAWYER_ADVISER_ROLE = BOUND
```

### Alina Habba

Contemporaneous reporting documents Habba among people stepping off Trump's jet in Philadelphia in September 2024.

```text
ONBOARD = BOUND
LAWYER_ROLE = BOUND
```

### Michael Cohen

Reporting records former Trump campaign aide Sam Nunberg saying Cohen handled an engine issue/deal involving the 'famous Trump plane.'

```text
AIRCRAFT_OPERATIONS_ASSOCIATION = BOUND_SECONDARY
ONBOARD_FOR_SPECIFIC_FLIGHT = HOLD_UNLESS_SEPARATELY_SOURCED
```

## Verified seed — Government aircraft

### William Barr

A FOIA-produced DOJ travel authorization for an October 2019 trip states Barr would travel via government aircraft and that part of the trip was combined official/personal travel with reimbursement rules.

```text
GOVERNMENT_TRAVELER = PROVEN_FROM_PRODUCED_AUTHORIZATION
IMPROPRIETY = NOT_INFERRED
```

### C. Boyden Gray

A 1991 White House travel policy states that the White House Counsel's Office would review requests for military-aircraft travel case by case, based on recommendations by Counsel to the President C. Boyden Gray.

```text
REVIEWED_TRAVEL_AUTHORITY = PROVEN
ONBOARD = HOLD_UNLESS_SEPARATELY_SOURCED
```

### Bruce Lindsey

Historical reporting describes the deputy White House counsel as a near-constant Clinton traveling companion aboard Air Force One.

```text
ONBOARD = BOUND_SECONDARY
EXACT_MANIFEST_BY_MANIFEST_PROOF = HOLD
```

### Jeff Sessions

A 2017 FOIA request sought Sessions travel records in the context of cabinet use of military/chartered aircraft. The request itself does not prove Sessions used such aircraft.

```text
GOVERNMENT_AIRCRAFT_USE = HOLD
```

## Search queues

1. Epstein aircraft: enumerate lawyers appearing in official Maxwell flight logs and distinguish passenger from counsel/legal-team references.
2. Trump aircraft: enumerate lawyers with photo, manifest, itinerary, campaign-travel, or aircraft-operations receipts.
3. Government aircraft: enumerate lawyers who were passengers, approving officials, or travel-policy reviewers; keep those edge types separate.
4. Aircraft capability: verify beds/sleeping quarters from manufacturer, operator, government, or aircraft-interior records; never infer purpose.

## Standing order

> Freeze the plane. Freeze the date. Freeze the lawyer role. Then join the stacks.
