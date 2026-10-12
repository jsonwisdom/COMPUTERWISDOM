# Wisconsin Lesson 002 — Follow the Dollar v0.1

Status: REVIEW_OPEN  
Predecessor: Wisconsin Lesson 001 — The Giant M  
Profile: ZiggyPrime — Applied Provenance Profile v0.1  
LeahPrime role: classifier / explainer / gap guardian  
Gray Baby role: GAP_WATCHER  
Authority created: false

## Lesson thesis

Every public number has a type, owner, time, fund/kind, action state, and provenance trail. Finding a number is not the same as finding the vote or authorization that gives the number meaning.

`FOLLOW_THE_DOLLAR <=> FOLLOW_THE_VOTE`

A record can be source-bound at one hop while downstream replay remains open. `PUBLIC_TRAIL_GAP` is therefore positional: name the exact missing edge instead of treating the whole trail as missing.

ZiggyPrime asks and navigates. LeahPrime classifies and explains. Gray Baby watches the unresolved boundary. RePlay preserves the path.

## Six-year-old mission

**Mission:** Can we prove what this public dollar number means, and can we follow it to the next public record?

Example interaction:

1. `Ziggy, budget Potosi.`
   - `PUBLIC_DOLLAR_HOPPER` gathers candidate numbers.
2. `LeahPrime, what kind of number?`
   - `NUMBER_TYPE_CLASSIFIER` labels levy / budget / fund / proposal / debt service / other.
3. `Gray Baby, did we find the vote?`
   - `VOTE_FINDER` + `GRAY_BABY_GAP_CARD` => YES / NO / UNKNOWN_HOLD.
4. `CrissCross Platteville.`
   - `CRISSCROSS_COMPARATOR` permits comparison only when type + year + unit are compatible; fund/kind differences stay visible.
5. `Reverse $482,569.`
   - `REVERSE_DOLLAR_REPLAY` walks the record chain and names the first unresolved downstream edge.

## Universal public-dollar replay

```text
PROPOSAL
  -> FUND BREAKOUT
  -> ELECTOR / BOARD AUTHORITY
  -> REFERENDUM (IF APPLICABLE)
  -> FINAL BUDGET
  -> LEVY CERTIFICATION
  -> PI-401 / PI-1508
  -> MUNICIPAL APPORTIONMENT
  -> PROPERTY-TAX BILL
  -> RECEIPT / SPENDING
  -> AUDIT
```

`PUBLIC_TRAIL_GAP = FIRST_UNRESOLVED_POSITION`, not a blanket accusation and not proof of fraud.

## Canonical receipt shape

```text
NUMBER:      $482,569
TYPE:        DEBT_SERVICE_LEVY
OWNER:       POTOSI SCHOOL DISTRICT
YEAR:        2025-26
FUND/KIND:   DEBT SERVICE
MEETING:     <SOURCE-BOUND VALUE OR UNKNOWN_HOLD>
ACTION:      PROPOSED | VOTED | CERTIFIED | SPENT | UNKNOWN_HOLD
SOURCE:      <PUBLIC RECORD REFERENCE>
PROVENANCE:  SOURCE_BOUND | DOWNSTREAM_REPLAY_OPEN | CLOSED | UNKNOWN_HOLD
NEXT_GAP:    <FIRST UNRESOLVED DOWNSTREAM EDGE>
```

## Potosi replay upgrade — 2025-26

The earlier state `$482,569 = SOURCE_BINDING_INCOMPLETE` is superseded.

### Source-bound upstream record

Potosi's official BoardBook Annual Meeting agenda for October 20, 2025 at 7:00 PM records:

- voting by voice vote unless a division of the house is requested;
- `Resolution A: Adoption of the 2025-26 budget and tax levy`;
- `$2,136,978` for operation;
- `$482,569` for debt service;
- `$0` for community service;
- `$2,619,547` total levy.

Official replay surface:
`https://meetings.boardbook.org/Public/Agenda/2042?meeting=712671`

Potosi's separate October 20, 2025 at 7:30 PM Budget Hearing agenda names two explicit action items:

- `Formal Approval of 2025-26 Budget`
- `Certification of Tax Levy`

Official replay surface:
`https://meetings.boardbook.org/Public/Agenda/2042?meeting=712684`

Wisconsin DPI's FY 2025-2026 public tax-levy table independently reproduces the Potosi breakout and total: `$2,136,978` operating + `$482,569` debt = `$2,619,547` total. DPI's FY 2025-2026 equalized levy-rate table reports Potosi's total levy as `$2,619,547` on `$279,155,186` TIF-out equalized value, for a `9.38` mill rate.

DPI replay surfaces:
`https://sfs.dpi.wi.gov/safr_ro/all_tax_levy.asp?year=2026`
`https://sfs.dpi.wi.gov/sfssafr/safr/all_mill_rate.asp?year=2026`

### Potosi receipt state

```text
NUMBER $482,569:                 SOURCE_BOUND
TYPE DEBT_SERVICE_LEVY:         SOURCE_BOUND
OPERATIONS $2,136,978:          SOURCE_BOUND
COMMUNITY_SERVICE $0:           SOURCE_BOUND
TOTAL $2,619,547:               RECONCILES
ANNUAL_RESOLUTION:              RESOLUTION_A_FOUND
ANNUAL_MEETING_VOTE_METHOD:     VOICE_VOTE_DEFAULT_SOURCE_BOUND
BUDGET_APPROVAL_ACTION:         OBSERVED_ON_OFFICIAL_AGENDA
LEVY_CERTIFICATION_ACTION:      OBSERVED_ON_OFFICIAL_AGENDA
DPI_TAX_LEVY_DATA:              SOURCE_BOUND
DPI_TOTAL_AND_MILL_RATE:        SOURCE_BOUND
BOARD_MINUTES_CERTIFICATION:    REPORTED_OBSERVED; DIRECT_TEXT_REPLAY_OPEN
BOARD_MINUTES_5_0:              REPORTED_OBSERVED; DIRECT_TEXT_REPLAY_OPEN
REFERENDUM_CONDITION:           LIKELY_SATISFIED; RESULT_SOURCE_BIND_OPEN
PI-401_SUBMISSION_ARTIFACT:     OPEN
PI-1508_CERTIFICATE:            OPEN
MUNICIPAL_APPORTIONMENT:        OPEN
ACTUAL_PROPERTY_TAX_BILL:       OPEN
DEBT_SERVICE_EXPENDITURE:       OPEN
AUDIT_RECONCILIATION:           OPEN
```

The indexed BoardBook minutes are reported to show certification of the `$2,619,547` levy at a `9.38` mill rate with a `5-0` motion. The public BoardBook minutes endpoints are identified, but the direct minutes body was not reproduced in the current replay capture, so the vote count remains a named replay edge rather than being silently promoted from an index/snippet.

Potosi also published that an operating referendum vote was scheduled for April 2, 2024. The referendum-result edge remains separately source-bindable; do not infer the result merely from the later levy record.

### State transition

```text
OLD: $482,569 = SOURCE_BINDING_INCOMPLETE
NEW: $482,569 = SOURCE_BOUND / DOWNSTREAM_REPLAY_OPEN

PRIMARY_GAP_OLD: AUTHORIZATION
PRIMARY_GAP_NEW: DOWNSTREAM_CERTIFICATION_APPORTIONMENT_RECONCILIATION
```

This is the point of positional provenance: the upstream number and fund breakout are no longer the main uncertainty. Replayers should now spend effort on the next unresolved links rather than repeatedly rediscovering the same agenda.

## Reverse Dollar Replay

```text
NUMBER
  -> TYPE
  -> OWNER
  -> YEAR
  -> FUND / KIND
  -> MEETING
  -> ACTION
  -> SOURCE
  -> RECEIPT STATE
  -> NEXT GAP
```

The receipt closes only when the requested trail closes. A source-bound authorization record may still remain `DOWNSTREAM_REPLAY_OPEN` for certification, apportionment, billing, spending, or audit reconciliation.

## CrissCross rule

A comparison is valid only when its dimensions are explicit.

Minimum comparator gate:

`SAME_TYPE + SAME_YEAR + SAME_UNIT`

Then expose, rather than erase, differences in:

- owner / district
- fund or kind
- proposal versus enacted state
- accounting scope
- source provenance
- current replay position

`SIMILAR_NUMBER != COMPARABLE_RECORD`

## Child Provenance Engine

```text
QUESTION
  -> PUBLIC_DOLLAR_HOPPER
  -> NUMBER_TYPE_CLASSIFIER
  -> OWNER_AND_YEAR_BINDER
  -> FUND_SPLITTER
  -> VOTE_FINDER
  -> GRAY_BABY_GAP_CARD
  -> CRISSCROSS_COMPARATOR
  -> REVERSE_DOLLAR_REPLAY
  -> PUBLIC_RECEIPT_BUILDER
  -> HUMAN REVIEW
```

LeahPrime may classify `VERIFIED`, `CANDIDATE`, `SOURCE_BOUND`, `DOWNSTREAM_REPLAY_OPEN`, `UNKNOWN_HOLD`, `FICTION`, or `SATIRE` where appropriate, but classification does not create source truth.

## Non-collapse doctrine

`NUMBER != AUTHORIZATION`

`PROPOSAL != VOTE`

`VOTE != CERTIFICATION`

`CERTIFICATION != APPORTIONMENT`

`APPORTIONMENT != TAX_BILL`

`TAX_BILL != EXPENDITURE`

`CERTIFICATION != SPEND`

`LEVY != BUDGET`

`DEBT_SERVICE != OPERATIONS`

`SOURCE_FOUND != TRAIL_CLOSED`

`SOURCE_BOUND != DOWNSTREAM_CLOSED`

`RECEIPT != TRUTH`

`OBSERVATION != AUTHORITY`

## Replay state

`ZIGGYPRIME_APPLIED_PROFILE = SEEDED`

`LEAHPRIME_CLASSIFY_EXPLAIN = ACTIVE`

`GRAY_BABY_GAP_WATCHER = ACTIVE`

`WISCONSIN_LESSON_001 = PREDECESSOR`

`WISCONSIN_LESSON_002 = REVIEW_OPEN`

`POTOSI_2025_26 = SOURCE_BOUND_DOWNSTREAM_REPLAY_OPEN`

`POTOSI_PRIMARY_GAP = DOWNSTREAM_CERTIFICATION_APPORTIONMENT_RECONCILIATION`

`FROZEN_FAMILY_STACK_MUTATED = FALSE`

`AUTHORITY_CREATED = FALSE`
