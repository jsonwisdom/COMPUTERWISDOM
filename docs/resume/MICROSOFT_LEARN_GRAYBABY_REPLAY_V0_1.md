# Microsoft Learn → Gray Baby → ResumeReplay v0.1

Date: `2026-08-19`  
Status: `CANONICAL_DRAFT / REPLAY_LOCKED / AUTHORITY_FALSE`

## Purpose

This rail ingests Microsoft Learn / credential / execution evidence into the existing GrayBabyWitness → ReverseResumeReplay architecture without allowing any downstream component to upgrade evidence.

Canonical order:

```text
RAW INPUT
  ↓
NORMALIZE
  ↓
SCHEMA VALIDATE
  ↓
GRAY BABY OBSERVE
  ↓
PASS | HOLD | REJECT
  ↓
GENERATE_RESUME_LANGUAGE
  ↓
APPEND-ONLY RECEIPT
```

## Membrane

```text
RAW DATA
  cannot write résumé language

NORMALIZER
  cannot assign proof

SCHEMA
  cannot infer meaning

GRAY BABY
  classifies only

LANGUAGE GENERATOR
  phrases only

LEDGER
  remembers only
```

Hard invariants:

```text
TRAINING != CREDENTIAL
TRANSCRIPT != EMPLOYMENT
CERTIFICATION != PRODUCTION
APPLIED_SKILL != UNBOUNDED_EXPERTISE
VERIFIED_URL != WORK_HISTORY
MICROSOFT_RECEIPT + EXECUTION_RECEIPT -> bounded capability only
AUTHORITY_CREATED = FALSE
EMPLOYMENT_CREATED = FALSE
```

## Phase A — safe phrasing templates

Templates are descriptive only. They consume finalized fields and cannot modify the observer result or evidence state.

```text
TRAINING_MODULE
Completed Microsoft Learn training module '{name}' covering {scope}.
Scope: {scope}. Limitations: {limitations}.

LEARNING_PATH
Completed Microsoft Learn learning path '{name}' covering {scope}.
Scope: {scope}. Limitations: {limitations}.

TRANSCRIPT
Microsoft Learn transcript records training and credential activity within {scope}.
Limitations: {limitations}.

APPLIED_SKILL
Microsoft Applied Skill '{name}' verified for the assessed scenario: {scope}.
Limitations: {limitations}.

CERTIFICATION
Microsoft Certification '{name}' verified within its defined assessment scope: {scope}.
Limitations: {limitations}.

ONLINE_VERIFIABLE_CREDENTIAL
Microsoft-verifiable credential '{name}' confirmed within {scope}.
Limitations: {limitations}. Verification: {verified_url}

EXECUTION_RECEIPT
Execution receipt verifies operation of '{name}' within the bounded scope: {scope}.
Limitations: {limitations}.
```

Template rules:

```text
TEMPLATE != VERDICT
TEMPLATE cannot alter evidence_state
TEMPLATE cannot create employment
TEMPLATE cannot create authority
TEMPLATE cannot infer production
TEMPLATE must render scope
TEMPLATE must render limitations
```

## Phase B1 — normalize_learn_object()

Canonical implementation:

`tools/resume_replay/normalize_learn_object.py`

The normalizer is representation-only. It:

- deep-copies input;
- normalizes whitespace;
- canonicalizes `source_type` casing;
- de-duplicates ordered scope / limitation / denial lists;
- rejects unknown fields rather than silently dropping them;
- copies `evidence_state` exactly if supplied.

It does **not** derive proof, authority, employment, production, credential validity, or work history.

## Phase B2 — append_receipt()

Canonical implementation:

`tools/resume_replay/append_only_receipt.py`

The ledger is JSONL and hash-linked. Each append records:

```text
receipt_id
source_hash
source_type
normalized_object_hash
evidence_state
observer_verdict
observer_reason
rendered_language_hash
timestamp
prior_receipt_hash
authority_claim = FALSE
employment_claim = FALSE
production_proof_claim = observer read-only value
```

The function opens the ledger with append semantics, never seeks backward, and never rewrites prior rows.

Correction model:

```text
OLD RECEIPT
  ↓
NEW EVIDENCE
  ↓
NEW RECEIPT
  ↓
STATE DELTA
```

## State-field precision correction

The earlier receipt sketch used `observer_result` for a four-state class while the observer function also uses detailed evidence states such as `PROVEN_BOUND` and `PROVEN_OPERATION`.

To prevent state collapse, the canonical receipt keeps two distinct fields:

```text
evidence_state
  = PROVEN | BOUND | PROVEN_BOUND | PROVEN_OPERATION | HOLD | CONFLICT

observer_verdict
  = PASS | HOLD | REJECT
```

This is a schema precision correction only; it creates no stronger claim.

## Schemas

Canonical object schema:

`schemas/microsoft_learn_resume_replay.v0_1.schema.json`

Canonical append-only receipt schema:

`schemas/microsoft_learn_resume_replay_receipt.v0_1.schema.json`

The object schema is closed (`additionalProperties: false`) and enforces the source-type → evidence-state map:

```text
TRAINING_MODULE               -> PROVEN
LEARNING_PATH                 -> PROVEN
TRANSCRIPT                    -> BOUND
APPLIED_SKILL                 -> PROVEN
CERTIFICATION                 -> PROVEN
ONLINE_VERIFIABLE_CREDENTIAL  -> PROVEN_BOUND
EXECUTION_RECEIPT             -> PROVEN_OPERATION
```

`production_proof_created = true` is schema-valid only when at least one execution receipt is present with state `PROVEN_OPERATION`.

## Authority boundary

```text
AUTHORITY_CREATED = FALSE
EMPLOYMENT_CREATED = FALSE
CREDENTIAL != EMPLOYMENT
CI_SUCCESS != PRODUCTION_DEPLOYMENT
TRAINING_COMPLETION != PRODUCTION_OPERATION
MISSING_RECEIPT -> HOLD
CONFLICTING_WITNESS -> CONFLICT
```

This rail is a ResumeReplay evidence processor. It does not create institutional authority, employment history, or production proof from Microsoft Learn material alone.
