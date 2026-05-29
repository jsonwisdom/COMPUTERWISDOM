# AL_ADMISSION_POLICY_V1

Constitutional computing layer — evidence-only, no authority.

## 1. Identity

Component: Authoritative Log Admission Surface (AL)  
Domain: Constitutional log entry point  
Classification: Shared computational membrane — not a branch, not sovereign

Core invariant:

```text
AL_ADMITS_EVIDENCE
AL_DOES_NOT_PROPOSE
AL_DOES_NOT_EXECUTE
AL_DOES_NOT_ADJUDICATE
AL_DOES_NOT_SELF_SEAL
```

AL is the algorithmic gate where valid, replay-verified, lineage-continuous artifacts become admitted entries in the authoritative log.

It does not create, judge, or seal.

It admits only when all computational conditions are met.

## 2. Purpose

AL provides the constitutional admission surface for the Compute Wisdom stack:

- receive admission requests from Executive
- verify that the attached replay verdict is `REPLAY_VALID` and properly signed by Judicial
- perform deterministic lineage continuity checks
- enforce admission criteria such as schema invariants and fork policy
- log admission events as evidence
- prepare admitted artifacts for final sealing operations

AL is a pure function of the evidence presented.

It holds no discretion.

## 3. Boundaries

AL cannot:

- propose legislation
- execute or dispatch processes
- adjudicate or issue verdicts on validity
- create or modify policy
- seal an entry on its own

AL must reject any admission request that lacks:

- a valid replay verdict from Judicial
- a cryptographically intact artifact
- a verifiable lineage link to the previous log head

AL may only admit or reject under defined deterministic criteria.

## 4. Admission Criteria

Every admission request must satisfy all of the following.

### 4.1 Replay Verdict Requirement

- The request must include a signed verdict from the Judicial Branch with status `REPLAY_VALID`.
- The verdict must reference the execution trace hash and proposal hash.

### 4.2 Lineage Continuity

- The artifact pre-state hash must exactly match the current head of the authoritative log, or genesis if the log is empty.
- The artifact must not create an orphan or fork that violates declared fork-resolution policy.
- Linear extension is default unless an explicit fork-policy proposal has been admitted.

### 4.3 Structural Integrity

- The artifact must be syntactically valid per the current admitted schema.
- Schema-change proposals must have passed required pre-execution advisory review.
- Schema-change proposals must not introduce breaking replay-engine changes without an accompanying admitted replay-engine update.

### 4.4 Proposal Provenance

- The artifact must trace back to a proposal published by Legislative, or to a procedural request explicitly allowed by branch charters.
- The proposal hash must be included and must match.

### 4.5 No Double Admission

- The same artifact hash must not already exist in the log.

## 5. Admission Process

### 5.1 Request Submission

Executive submits an admission request containing:

- artifact hash
- artifact reference
- execution trace hash
- Judicial replay verdict
- proposal reference
- requested admission type

Allowed admission types include:

```text
log_append
schema_update
mission_state_change
policy_update
replay_engine_update
```

### 5.2 Automated Validation

AL performs deterministic checks:

- verdict signature valid
- verdict status equals `REPLAY_VALID`
- pre-state hash matches log head
- structural integrity check passes
- proposal provenance check passes
- duplicate admission check passes

### 5.3 Admission Event

If all checks pass, AL:

- computes the new log head as hash of old head plus artifact hash
- appends the artifact reference to the log
- emits an Admission Receipt
- makes the receipt available to Executive, Judicial, and sealing coordinators

Admission Receipt fields:

```text
admitted_artifact_hash
previous_head_hash
new_head_hash
admission_timestamp
evidence_references
authority_boundary
```

### 5.4 Rejection Handling

If any check fails, AL returns a Rejection Notice specifying the failed criterion.

No state is changed.

Executive may resubmit after correction.

## 6. Relationship to Sealing

Admission is not sealing.

Sealing is a separate computational act that finalizes admitted entries into immutable lineage, such as by producing compact cryptographic proof or external anchoring.

This policy does not define sealing mechanics.

It only guarantees that admitted artifacts are eligible for sealing.

Sealing must be replay-verifiable and defined by its own policy.

## 7. Evidence-Only Doctrine

This policy is evidence of intended admission rules.

No sovereignty is claimed.

The authoritative log is an evidence surface.

All entries are computational facts, not legal decrees.

Political facts require trusted external confirmation.

## 8. Closing Invariant

AL admits nothing by authority.

It admits only by computational proof.

The log grows only by evidence, never by will.
