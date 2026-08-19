# Authority Router v0.1 — Integration Note

Status: DRAFT / REVIEW-ONLY / UNMERGED

```text
AUTHORITY_CREATED = FALSE
LEGAL_DUTY_CREATED = FALSE
PUBLIC_QUESTION != PROVEN_CLAIM
AI_PROPOSAL != AUTHORITY
```

## Purpose

Bind the Public Question → Authority Router to the existing COMPUTERWISDOM Dual Onion discipline without creating a new court, agency, statutory deadline, or adjudicative power.

## Constitutional surface

```text
PUBLIC QUESTION
→ QUESTION OBJECT
→ DIRECTORY MATERIALIZATION
→ RECORD ONION
→ POWER ONION
→ CANDIDATE AUTHORITY / CUSTODIAN
→ PRIMARY RECORDS
→ PUBLIC STATUS CLOCK
→ OFFICIAL RESPONSE / NO RESPONSE OBSERVED
→ OIG / CONGRESS / COURT ROUTING
→ RECEIPT
→ REPLAY
→ PASS | HOLD | CONFLICT | REJECT
```

### Record Onion

Question: **What does the record show?**

```text
QUESTION
→ SOURCE
→ OBSERVATION
→ ORIGINAL / CANONICAL RECORD
→ BYTES / VERSION
→ HASH / RECEIPT
→ CONTRADICTION CHECK
→ REPLAY
```

### Power Onion

Question: **Who possessed authority to do what?**

```text
ACTOR / OFFICE
→ CLAIMED AUTHORITY
→ GRANTING TEXT
→ JURISDICTION
→ ACTION
→ IMPLEMENTATION
→ CONSEQUENCE
→ OVERSIGHT
→ RECEIPT
→ REPLAY
```

Evidence in one onion may not pay for a missing edge in the other.

## Directory-trigger law

A normalized public question is sufficient to materialize a question directory. It is not sufficient to create a factual allegation or legal finding.

```text
QUESTION_ACCEPTED
→ Q-OBJECT CREATED
→ DIRECTORY MATERIALIZED
→ EMPTY EVIDENCE LANES EXPOSED
→ CANDIDATE CUSTODIANS PROPOSED
→ MISSING AUTHORITY EDGES EXPOSED
```

The directory exists to make missing information visible and fillable.

## AI membrane

AI may normalize, classify, search, route, compare, summarize, and propose candidate authority/custodian nodes.

AI may not create governmental authority, determine guilt, convert proximity into misconduct, invent a legal deadline, or promote an unsupported claim.

```text
AI_ROUTING = ADVISORY
DETERMINISTIC_MATERIALIZER = DIRECTORY AUTHORITY ONLY
HUMAN / SOURCE-BOUND PROMOTION = REQUIRED
```

## Public status layer

The portal owns a 24-hour **status obligation to itself**. The status clock does not alter FOIA, court, OIG, congressional, administrative, or statutory deadlines.

At the clock boundary, the portal publishes a bounded state and the evidence supporting that state.

## External legal clocks

External deadlines are admitted only when a statute, regulation, court order, rule, or official process source is bound.

Examples include FOIA processing clocks and jurisdiction-specific court deadlines. These clocks remain independent of the portal SLA.

## OpenAI boundary

The deterministic core does not require a model or API key.

```text
MODEL_REQUIRED = FALSE
OPENAI_OPTIONAL = TRUE
MODEL_OUTPUT != RECEIPT
MODEL_OUTPUT != AUTHORITY
MODEL_OUTPUT != LEGAL_FINDING
```

An optional OpenAI layer may produce structured routing proposals from already-bounded inputs; deterministic code and human review remain responsible for materialization and promotion.

## Core rule

**Ask publicly. Materialize deterministically. Bind records and authority separately. Preserve silence without interpreting it. Replay everything.**
