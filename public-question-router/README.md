# Public Question → Authority Router v0.1

Status: DRAFT / REVIEW-ONLY / UNMERGED

```text
AUTHORITY_CREATED = FALSE
LEGAL_DUTY_CREATED = FALSE
PUBLIC_QUESTION != PROVEN_CLAIM
AI_ROUTING != GOVERNMENT_AUTHORITY
NO_RESPONSE != GUILT
```

## Purpose

Turn a public question into a deterministic, inspectable case directory that identifies candidate custodians/authorities, starts a visible portal clock, collects primary records, and preserves unanswered edges without allowing AI, media narrative, or office status to manufacture truth.

## Trigger

```text
PUBLIC QUESTION
→ NORMALIZE
→ QUESTION_ID
→ MATERIALIZE DIRECTORY
→ CLASSIFY CLAIM / RECORD / AUTHORITY EDGES
→ PROPOSE CANDIDATE AUTHORITY / CUSTODIAN
→ START PORTAL CLOCK
→ INGEST PUBLIC RECORDS
→ REQUEST / LINK OFFICIAL RESPONSE
→ REPLAY
→ PASS | HOLD | CONFLICT | REJECT
```

A question creates a directory. It does not create a factual allegation.

## Directory contract

Every question materializes:

```text
public-question-router/questions/<QUESTION_ID>/
├── QUESTION.md
├── intake.json
├── authority/
│   ├── candidates.json
│   ├── claimed_authority/
│   └── jurisdiction_receipts/
├── records/
│   ├── public/
│   ├── court/
│   ├── agency/
│   └── source_bytes/
├── money/
│   ├── appropriations/
│   ├── contracts/
│   └── travel_lodging/
├── responses/
│   ├── official/
│   ├── congressional/
│   └── oig/
├── clocks/
│   ├── portal_24h.json
│   └── legal_deadlines.json
├── contradictions/
├── receipts/
└── replay/
```

Git does not preserve empty directories; each directory is materialized when the first receipt or README enters it.

## 24-hour rule — portal SLA, not invented law

The portal uses a 24-hour **transparency/status SLA**:

```text
T+00:00 = QUESTION_ACCEPTED
T+00:05 = DIRECTORY_MATERIALIZED target
T+01:00 = CANDIDATE_AUTHORITY_ROUTED target
T+24:00 = PUBLIC_STATUS_RECEIPT_DUE
```

At T+24h the portal must publish one of:

```text
ANSWER_RECEIVED
RECORDS_RECEIVED
ACKNOWLEDGMENT_RECEIVED
ROUTED_TO_STATUTORY_PROCESS
NO_RESPONSE_OBSERVED
JURISDICTION_UNRESOLVED
```

`NO_RESPONSE_OBSERVED` is a transparency state only. It is not evidence of guilt, obstruction, corruption, illegality, or contempt.

External legal clocks remain separate. For example, DOJ states the general FOIA response period is 20 business days; the portal must not relabel that statutory process as a 24-hour legal duty.

## AI role

AI may:

- normalize the public question;
- identify entities, dates, offices, statutes, appropriations, contracts, dockets, and likely record custodians;
- propose candidate authority/custodian nodes;
- identify missing edges;
- fetch or classify public primary sources;
- generate a neutral request package;
- compare official answers against already-bound records.

AI may not:

```text
AI_PROPOSAL != AUTHORITY
AI_INFERENCE != FACT
OFFICE_HOLDER != AUTOMATIC_CUSTODIAN
CANDIDATE_AUTHORITY != PROVEN_AUTHORITY
PUBLIC_QUESTION != CRIMINAL_COMPLAINT
```

## Authority challenge

Every candidate authority node must answer the same machine-readable questions:

1. What office are you acting through?
2. What authority do you claim?
3. What text grants that authority?
4. What action occurred?
5. What public record proves the action?
6. What appropriation, contract, or payment supported it, if relevant?
7. What oversight body has jurisdiction?
8. What record is withheld, redacted, sealed, classified, or unavailable, and under what stated basis?
9. What correction or appeal path exists?

If the authority edge is not proven, status remains `HOLD_AUTHORITY_EDGE`.

## Court-record lane

Federal court records route to public judiciary sources such as PACER when available. PACER provides electronic public access to federal court records; sealed records are not publicly available. State and local court systems require jurisdiction-specific connectors or links.

```text
COURT_RECORD_NOT_FOUND != NO_CASE
SEALED != NONEXISTENT
DOCKET_ENTRY != MERITS_FINDING
ALLEGATION_IN_PLEADING != FACT_PROVEN
```

## Human accountability without demographic shortcuts

The router targets **offices, custodians, delegated authority, and money flows**, not age or gender categories.

```text
AGE != AUTHORITY
GENDER != AUTHORITY
TITLE != AUTHORITY
SALARY != MISCONDUCT
BADGE != LAWFULNESS
```

Representation and disparate-impact questions may be tracked as their own evidence lanes when the public question concerns exclusion, participation, employment, or equal treatment.

## Public-facing replay

```text
WHAT PUBLIC ASKED
↕
WHO CLAIMS AUTHORITY
↕
WHAT PRIMARY RECORDS EXIST
↕
WHAT THE OFFICE ANSWERED
↕
WHAT REMAINS MISSING
↕
WHAT COURT / OIG / CONGRESS RECORDS SAY
↕
REPLAY STATE
```

No media story is required for promotion. Media can be an intake pointer; primary records remain the preferred authority/evidence surface.

## Core rule

**Ask publicly. Route deterministically. Bind authority. Start the clock. Preserve silence. Publish receipts.**
