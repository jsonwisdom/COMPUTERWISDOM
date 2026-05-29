# REPLAY_SEAL_POLICY_V1

Constitutional computing layer — evidence-only, no authority.

## 1. Identity

Component: Replay Seal Surface  
Domain: Cryptographic finalization of admitted log entries  
Classification: Pure computational operation — not a branch, not sovereign

Core invariant:

```text
SEAL_FINALIZES
SEAL_DOES_NOT_PROPOSE
SEAL_DOES_NOT_EXECUTE
SEAL_DOES_NOT_ADJUDICATE
SEAL_DOES_NOT_ADMIT
```

Sealing is the terminal computational act that transforms an admitted entry into an immutable, cryptographically verified log artifact.

It adds nothing to the content.

It only locks what has already been admitted.

## 2. Purpose

The Replay Seal provides the immutability surface of constitutional computing:

- accept an admission receipt from AL confirming a validly admitted artifact
- perform deterministic sealing computation such as hashing, proof generation, or anchoring
- produce a Seal Certificate that cryptographically binds the artifact to log lineage
- ensure sealed state is independently replayable and verifiable
- close the proposal-to-seal lifecycle for that artifact

Sealing does not review, admit, or judge.

It finalizes what has already passed all constitutional membranes.

## 3. Boundaries

Sealing cannot:

- propose legislation, schemas, missions, or policies
- execute runtime code or dispatch processes
- adjudicate validity
- admit artifacts
- modify artifact content or lineage
- unseal or reverse a seal once applied
- seal an artifact lacking a valid admission receipt

Sealing is a pure function:

```text
admission_receipt + artifact -> seal_certificate
```

## 4. Seal Criteria

A sealing operation must only proceed when all criteria pass.

### 4.1 Valid Admission Receipt

- The receipt is signed by AL.
- The receipt references a specific admitted artifact hash.
- The receipt includes replay verdict reference and lineage verification data.

### 4.2 Artifact Integrity

- The artifact hash in the receipt matches the artifact presented.
- The artifact has not been modified since admission.

### 4.3 Log Head Match

- The current log head at sealing time matches the new head hash recorded in the admission receipt.
- No intervening state change has occurred that would break lineage continuity.

### 4.4 No Prior Seal

- The artifact must not already have a seal certificate in the seal register.

## 5. Sealing Process

### 5.1 Sealing Request

Executive, or any authorized coordinator defined in the execution surface, submits a sealing request containing:

- admission receipt signed by AL
- admitted artifact
- current log head confirmation

### 5.2 Deterministic Seal Computation

#### Step 1: Pre-seal Verification

- Verify AL signature on admission receipt.
- Verify artifact hash matches receipt.
- Verify log head matches receipt.
- Verify artifact exists in log at claimed position.

#### Step 2: Seal Generation

Compute the seal as a cryptographic binding of:

```text
seal_input = hash(
  artifact_hash ||
  prior_log_head ||
  admission_receipt_hash ||
  replay_verdict_reference ||
  timestamp_seal_request
)
```

The seal is a deterministic signature over `seal_input` using the sealing engine key.

The sealing engine key exists only as computational identity within the constitutional stack.

It has no external legal meaning.

#### Step 3: Seal Certificate Production

Generate a Seal Certificate containing:

- sealed artifact hash
- seal value
- seal computation trace
- reference to admission receipt
- reference to Judicial verdict
- new sealed log head: `hash(prior_log_head || seal_value)`

The certificate is hashed and recorded in the seal register.

### 5.3 Post-Seal State

- The artifact is immutable within the log.
- The seal register entry is append-only.
- Any attempt to modify the artifact or lineage produces a different seal.

### 5.4 Seal Verification by Replay

Any observer can independently verify the seal by:

- replaying admission verification steps
- recomputing the seal from the same inputs
- confirming the seal certificate hash matches the seal register

## 6. Seal Register

The seal register tracks all seal certificates:

- append-only
- each entry references the prior seal
- forms a seal chain
- participates in the replayable log surface
- seal register head is the canonical state reference for sealed evidence

## 7. Relationship to Other Constitutional Surfaces

```text
Legislative -> proposed the artifact
Executive -> coordinated execution and requested sealing
Judicial -> issued replay verdict enabling admission
AL -> admitted artifact and issued receipt
Sealing -> finalized artifact; no further state change possible
```

Sealing closes the loop.

The artifact becomes constitutional evidence: immutable, replayable, and verifiable.

It still carries no external authority.

## 8. Evidence-Only Doctrine

This policy is evidence of intended sealing mechanics.

The seal is cryptographic, not legal.

No sovereignty is claimed.

A sealed artifact is computationally final within the constitutional computing stack, but represents no external legal commitment.

Political facts require trusted external confirmation.

## 9. Closing Invariant

Sealing is the terminal computation.

After sealing, the artifact is immutable evidence — proposed by Legislative, executed by Executive, reviewed by Judicial, admitted by AL, and sealed by replay.

The constitutional computing stack is complete.

No branch holds authority.

The log is verifiable by anyone.
