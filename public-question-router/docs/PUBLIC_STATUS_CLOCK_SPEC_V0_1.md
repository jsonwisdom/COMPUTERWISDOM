# Public Status Clock Spec v0.1

Status: DRAFT / REVIEW-ONLY

## Scope

Define the portal-owned 24-hour transparency/status clock without modifying any external legal duty or deadline.

```text
PORTAL_24H = SELF-IMPOSED PUBLIC STATUS SLA
PORTAL_24H != FOIA DEADLINE
PORTAL_24H != COURT DEADLINE
PORTAL_24H != OIG DEADLINE
PORTAL_24H != CONGRESSIONAL DEADLINE
LEGAL_DUTY_CREATED = FALSE
```

## Clock origin

`started_at` is the canonical timestamp at which a valid public question is accepted and a Q-object is created.

All clock arithmetic uses UTC. Display layers may render local time separately.

## Target events

```text
T+00:00  QUESTION_ACCEPTED
T+00:05  DIRECTORY_MATERIALIZED target
T+01:00  CANDIDATE_AUTHORITY_ROUTED target
T+24:00  PUBLIC_STATUS_RECEIPT_DUE
```

The 5-minute and 1-hour markers are operational targets, not legal obligations.

## T+24 terminal public-status requirement

By `status_due_at`, the portal must append a receipt containing exactly one bounded public status:

```text
ANSWER_RECEIVED
RECORDS_RECEIVED
ACKNOWLEDGMENT_RECEIVED
ROUTED_TO_STATUTORY_PROCESS
NO_RESPONSE_OBSERVED
JURISDICTION_UNRESOLVED
```

A status receipt must include:

- question ID;
- clock start and due timestamps;
- status timestamp;
- evidence/receipt references supporting the status;
- known external process or tracking number when public and applicable;
- missing edges;
- `authority_created=false`.

## Silence rule

```text
NO_RESPONSE_OBSERVED = NO QUALIFYING RESPONSE BOUND BY CLOCK CUT
NO_RESPONSE_OBSERVED != REFUSAL
NO_RESPONSE_OBSERVED != OBSTRUCTION
NO_RESPONSE_OBSERVED != GUILT
NO_RESPONSE_OBSERVED != MISCONDUCT
```

Later responses append new receipts. They do not erase the historical T+24 receipt.

## Portal SLA breach

If the portal itself fails to publish a bounded status by T+24, the clock state becomes:

`BREACHED_PORTAL_SLA`

This describes portal performance only. It says nothing about government conduct.

## External-clock registry

Legal and administrative clocks are stored independently in `clocks/legal_deadlines.json` or the Q-object `external_clocks` collection.

An external clock may be promoted from `UNBOUND` only when its source is identified and bound, such as a statute, regulation, rule, court order, or official agency process.

For federal FOIA requests, DOJ public guidance describes a general 20-business-day statutory response period, subject to the statute's rules and circumstances. The portal records the source and calculated deadline separately rather than converting it into 24 hours.

For federal court records, PACER is a public-record retrieval surface; docket availability is not treated as a response from a party or agency.

## Append-only state transitions

```text
QUESTION_ACCEPTED
→ DIRECTORY_MATERIALIZED
→ CANDIDATE_AUTHORITY_ROUTED
→ [ZERO OR MORE INTERMEDIATE RECEIPTS]
→ T+24 STATUS RECEIPT
→ [LATER RECORD / RESPONSE RECEIPTS]
→ REPLAY
```

Historical receipts are never rewritten merely because later information arrives.

## Deterministic checks

A clock verifier should reject or hold when:

- `status_due_at != started_at + 24h`;
- timestamps lack timezone/UTC normalization;
- a T+24 receipt is missing after the due time;
- the portal claims a legal deadline without a bound external source;
- `NO_RESPONSE_OBSERVED` is promoted into a misconduct conclusion;
- a later response overwrites rather than appends to historical state.

## Core rule

**The portal must account for its own silence before it criticizes anyone else's.**
