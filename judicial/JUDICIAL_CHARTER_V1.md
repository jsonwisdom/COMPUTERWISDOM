# JUDICIAL_CHARTER_V1

Constitutional computing layer — evidence-only, no authority.

## 1. Branch Identity

Name: Judicial Branch (Compute Wisdom)  
Domain: Replay and lineage verification surfaces  
Classification: Non-legislative, non-executive, non-sovereign

Core invariant:

```text
JUDICIAL_REVIEWS
DOES_NOT_PROPOSE_EXCEPT_STRUCTURAL_REVIEW_QUERIES
DOES_NOT_EXECUTE
DOES_NOT_ADMIT
DOES_NOT_SELF_SEAL
```

The Judicial Branch examines execution traces, verifies replay determinism, and ensures lineage integrity.

It issues validity verdicts, not desirability judgments.

## 2. Purpose

The Judicial Branch provides the constitutional computing review layer:

- accept execution traces from Executive
- perform deterministic replay
- verify state transition equivalence
- confirm lineage continuity
- issue replay verdicts: VALID, INVALID, or INCOMPLETE
- detect constitutional invariant violations

It does not modify state.

It verifies replay.

## 3. Boundaries

Judicial cannot:

- execute code or dispatch processes
- draft proposals, except structural review queries that do not modify the constitutional corpus
- admit artifacts into the authoritative log
- finalize seals
- override prior verdicts without new replay evidence

Judicial bases verdicts solely on replay computation.

## 4. Directory Structure

```text
COMPUTERWISDOM/judicial/
├── README.md
├── JUDICIAL_CHARTER_V1.md
├── replay-engine/
├── verdicts/
├── lineage-checks/
└── review-queries/
```

`replay-engine/` contains deterministic replay implementations.  
`verdicts/` contains replay outcomes.  
`lineage-checks/` contains lineage verification utilities.

## 5. Judicial Process

### 5.1 Receiving an Execution Trace

Executive sends:

- proposal reference
- executed sequence
- pre-state hash
- post-state hash

### 5.2 Replay

Judicial independently recomputes the sequence.

If post-state hash matches:

```text
REPLAY_VALID
```

If hashes diverge:

```text
REPLAY_INVALID
```

If trace is incomplete:

```text
INCOMPLETE
```

### 5.3 Lineage Verification

Judicial checks:

- pre-state existence
- lineage continuity
- fork-policy consistency

### 5.4 Verdict Issuance

A replay verdict is produced and made available to Executive and AL.

The verdict is evidence.

Judicial reveals replay outcome; it does not compel.

## 6. Inter-Branch Membrane

Judicial may:

- receive traces from Executive
- publish verdicts
- send structural review queries to Legislative
- notify AL of replay outcomes

Judicial may not:

- execute
- legislate
- admit
- seal
- command Executive

## 7. Evidence-Only Doctrine

This charter is evidence.

Verdicts are computational evidence, not sovereign judgments.

Political facts require external confirmation.

## 8. Closing Invariant

Constitutional computing separates verification from execution.

The Judicial Branch is the replay witness, not the enforcer.
