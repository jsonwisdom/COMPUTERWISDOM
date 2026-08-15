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

ZiggyPrime asks and navigates. LeahPrime classifies and explains. Gray Baby watches the unresolved boundary. RePlay preserves the path.

## Six-year-old mission

**Mission:** Can we prove what this public dollar number means?

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
   - `REVERSE_DOLLAR_REPLAY` walks backward through the record chain.

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
```

The receipt closes only when the authorization trail closes. Otherwise it remains `OPEN` or `UNKNOWN_HOLD` with the missing edge named.

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
PROVENANCE:  OPEN | CLOSED | UNKNOWN_HOLD
```

The example number is a teaching fixture until its complete public authorization chain is source-bound in the lesson receipt. The profile must not infer a missing meeting, vote, certification, or expenditure event.

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

LeahPrime may classify `VERIFIED`, `CANDIDATE`, `UNKNOWN_HOLD`, `FICTION`, or `SATIRE` where appropriate, but classification does not create source truth.

## Non-collapse doctrine

`NUMBER != AUTHORIZATION`

`PROPOSAL != VOTE`

`VOTE != CERTIFICATION`

`CERTIFICATION != SPEND`

`LEVY != BUDGET`

`DEBT_SERVICE != OPERATIONS`

`SOURCE_FOUND != TRAIL_CLOSED`

`RECEIPT != TRUTH`

`OBSERVATION != AUTHORITY`

## Replay state

`ZIGGYPRIME_APPLIED_PROFILE = SEEDED`

`LEAHPRIME_CLASSIFY_EXPLAIN = ACTIVE`

`GRAY_BABY_GAP_WATCHER = ACTIVE`

`WISCONSIN_LESSON_001 = PREDECESSOR`

`WISCONSIN_LESSON_002 = REVIEW_OPEN`

`FROZEN_FAMILY_STACK_MUTATED = FALSE`

`AUTHORITY_CREATED = FALSE`
