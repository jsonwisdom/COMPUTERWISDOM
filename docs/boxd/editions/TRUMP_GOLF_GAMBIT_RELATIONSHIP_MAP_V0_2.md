# Trump Golf Gambit — Relationship Graph / Receipt Map v0.2

**Class:** public-record relationship mapping / non-authority  
**Sack ID:** `TRUMP-GOLF-001`  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Proposition

What public records document Donald Trump's golf partners, and where do those relationships overlap with later meetings, policy actions, contracts, endorsements, or financial transactions?

## Hard membrane

```text
RELATIONSHIP_EDGE != CORRUPTION
TEMPORAL_OVERLAP != CAUSATION
GOLF_PARTNER != BUSINESS_PARTNER
CONTRACT != KICKBACK
DELAWARE_ENTITY != FRAUD
UNKNOWN_PARTNER = UNKNOWN
```

## Graph contract

Node types:

`PERSON | OFFICE | GOLF_EVENT | COURSE | PROPERTY | ENTITY | GOVERNMENT | MEETING | POLICY | CONTRACT | PAYMENT | BANK | COURT | OVERSIGHT | SOURCE`

Edge types:

`PLAYED_WITH | PRESENT_AT | HELD_OFFICE | DISCUSSED | MET_WITH | SIGNED | AWARDED_TO | IMPLEMENTED_BY | PAID | BANKED_AT | REVIEWED_BY | REPORTED_BY | OWNS_OR_CONTROLS | TEMPORAL_OVERLAP`

Every edge carries `edge_id`, `from_node`, `to_node`, `edge_type`, `event_date`, `source_id`, `source_kind`, `raw_bytes_or_hash_status`, `evidence_state`, and an independent `causal_claim_state`.

## Verified-core map

### Stubb / icebreaker rail

```text
2025-03-29
TRUMP --PLAYED_WITH--> ALEXANDER STUBB
      --PLAYED_WITH--> GARY PLAYER
      --PLAYED_WITH--> LINDSEY GRAHAM
      --PLAYED_WITH--> TREY GOWDY

same-day public statement
TRUMP/STUBB RELATIONSHIP --DISCUSSED--> U.S.-FINLAND ICEBREAKERS

+194 days
2025-10-09
TRUMP + STUBB --SIGNED--> U.S.-FINLAND ICEBREAKER MOU

+272 days
2025-12-26
U.S. COAST GUARD --AWARDED_TO--> RAUMA MARINE CONSTRUCTIONS OY
                 --AWARDED_TO--> BOLLINGER SHIPYARDS LOCKPORT, L.L.C.

+319 days
2026-02-11
FINNISH GOVERNMENT --REPORTED--> FOUR FINLAND-BUILT ICEBREAKER AGREEMENTS IN PLACE
```

**Sequence state:** BOUND / largely PROVEN as dated sequence.  
**Golf-caused-procurement:** HOLD.  
**Contract -> payment -> receiving bank:** HOLD.  
**Kickback / improper influence:** NOT PROVEN.

### PGA / LIV / Saudi-PIF rail

```text
2025-02-20 WHITE HOUSE WORKING SESSION
DONALD TRUMP
  |--> JAY MONAHAN
  |--> TIGER WOODS
  |--> ADAM SCOTT
  +--> YASIR AL-RUMAYYAN / SAUDI PIF
       \--> PGA TOUR / LIV REUNIFICATION DISCUSSION

2025-04
TRUMP NATIONAL DORAL --HOSTED_EVENT--> LIV GOLF / SAUDI-PIF-BACKED LEAGUE
```

Meeting/event edges are BOUND or PROVEN from public records. Venue-payment amount, receiving bank, and any improper-influence theory remain HOLD absent transaction receipts or findings.

### Sankey / Bevacqua / college-sports rail

```text
2025-06-08 BEDMINSTER
TRUMP --PLAYED_WITH--> GREG SANKEY
      --PLAYED_WITH--> PETE BEVACQUA
           \--> COLLEGE-SPORTS DISCUSSION

+46 days
2025-07-24
TRUMP --SIGNED--> EXECUTIVE ORDER 14322 / SAVING COLLEGE SPORTS
```

**Temporal/topic overlap:** BOUND.  
**Golf conversation caused EO 14322:** HOLD.

## Edge ladder

1. `GOLF_PARTNER -> DATE + COURSE` = PROVEN for enumerated verified-core events.
2. `DATE + COURSE -> PUBLIC/PRIVATE ROLE` = PROVEN for named actors.
3. `ROLE -> SUBSEQUENT MEETING` = BOUND where dated meeting receipts exist.
4. `SUBSEQUENT MEETING -> POLICY/CONTRACT` = BOUND where later action exists and subject matter overlaps.
5. `POLICY/CONTRACT -> ENTITY` = PROVEN where official awards identify counterparties.
6. `ENTITY -> PAYMENT` = HOLD unless payment/disbursement record acquired.
7. `PAYMENT -> BANK` = HOLD unless account/custodian record acquired lawfully.
8. `BANK -> COURT/OIG/CONGRESSIONAL_FINDING` = HOLD unless official finding exists.

## Overlay algorithm

For each golf event `G` at `t0`:

1. Freeze partner list and source.
2. Resolve each partner's office/entity on `t0`.
3. Search forward and reverse for subject-matched records.
4. Compute temporal distance in days.
5. Require entity match or explicit subject match before promoting `TEMPORAL_OVERLAP`.
6. Require primary/official evidence before promoting `POLICY`, `CONTRACT`, `PAYMENT`, or `FINDING` edges.
7. Keep `causal_claim_state` independent from `evidence_state`.

Descriptive windows: `14 | 30 | 90 | 180 | 365` days. No window creates causation.

## Candidate-edge queue

Historical partner names from prior research belong in a re-verification queue until their source is re-fetched and assigned a source ID. Candidate examples include Tiger Woods, Shinzo Abe, Ernie Els, Rory McIlroy, Jack Nicklaus, Dustin Johnson, Bryson DeChambeau, Fred Funk, Lexi Thompson, Pat Perez, John Daly, Brooks Koepka, Saquon Barkley, and others.

## Source registry

- `SRC-001` — American Presidency Project, Digest of Other White House Announcements, 2025-03-29.
- `SRC-002` — American Presidency Project / archived Trump public statement, 2025-03-29, linking Stubb golf and icebreaker cooperation.
- `SRC-003` — Finnish Government, *Finland and USA deepen icebreaker cooperation*, 2025-10-10.
- `SRC-004` — U.S. Coast Guard, Arctic Security Cutter contract awards, 2025-12-29/30.
- `SRC-005` — Finnish Government, Finnish shipyards and U.S. Coast Guard agreements, 2026-02-11.
- `SRC-006` — PGA TOUR, White House working-session statement, 2025-02-20.
- `SRC-007` — Greg Sankey public confirmation / contemporaneous reporting of 2025-06-08 Bedminster golf discussion.
- `SRC-008` — White House / GovInfo, Executive Order 14322, 2025-07-24.
- `SRC-009` — Congressional Record / S.Res. 242 discussion referencing LIV Golf at Trump National Doral in April 2025.

## OpenAI Developer processor contract

A model/runtime may extract entities and dates, propose candidate nodes/edges, calculate temporal deltas, compare canonicalized records, flag missing receipt fields, and emit visualization-ready JSON.

It may **not** promote temporal overlap into causation, infer corruption from golf access, infer a payment or bank from a contract, convert a political allegation into a finding, or create government/judicial/evidentiary authority.

```text
MODEL OUTPUT
   -> HUMAN/SOURCE REVIEW
   -> PRIMARY RECEIPT
   -> EDGE STATE
```

## Current sack state

```text
RECORD          = PARTIALLY_PROVEN
AUTHORITY       = PARTIALLY_BOUND
MONEY_EXECUTION = BOUND_THROUGH_IDENTIFIED_CONTRACTS_ON_STUBB_RAIL
PAYMENT_BANK    = HOLD
OVERSIGHT       = PARTIAL
EDGE_CHAIN      = BOUND_THROUGH_CONTRACT_ON_ONE_RAIL
OVERALL         = HOLD
```

> Map the relationship. Freeze the date. Show the contract. Then show the payment. Do not skip the edge.
