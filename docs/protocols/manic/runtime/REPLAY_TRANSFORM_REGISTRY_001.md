# REPLAY_TRANSFORM_REGISTRY_001

**Replayable Manic – Replay Transform Registry**  
**Version:** 0.1  
**Status:** Constitutional Syscall Table  
**Continuity Flag:** COHERENTLY_INVALID_UNTIL_REPLAYED

## Core Invariant

A transform is not trusted because it ran.

A transform is admissible only if its rules are public, deterministic, and replayable.

## Registry Table

| Transform ID | Purpose | Admissibility | Interpretation | Network Access |
|---|---|---|---|---|
| `STRUCTURAL_SPLIT` | Decomposition of source into atomic structural parts | Required | NO | NO |
| `CONTENT_HASH` | Verification of content integrity | Required | NO | NO |
| `LOCATOR_CAPTURE` | Identification of source coordinates | Required | NO | NO |
| `SCHEMA_VALIDATE` | Enforcement of structural integrity | Required | NO | NO |

## Transform Specification

### 1. STRUCTURAL_SPLIT

- **Allowed Input:** `ROOT_SOURCE` or existing `REPLAY_NODE`
- **Allowed Output:** Atomic `REPLAY_NODE` segments
- **Forbidden Behavior:** merging disparate sources; logical inference; semantic summary
- **Refusal Codes:** `ERR_INFERENCE_DETECTED`, `ERR_SOURCE_MIXING`, `ERR_INTERPRETIVE_OUTPUT`

### 2. CONTENT_HASH

- **Allowed Input:** byte stream or canonicalized node content
- **Allowed Output:** SHA-256 digest as 64-character lowercase hex prefixed with `sha256:` where required
- **Forbidden Behavior:** truncation; approximation; non-deterministic hashing
- **Refusal Codes:** `ERR_NON_DETERMINISTIC_HASH`, `ERR_TRUNCATION`, `ERR_HASH_FORMAT`

### 3. LOCATOR_CAPTURE

- **Allowed Input:** URI, page number, section identifier, table identifier, footnote identifier, timestamp, or byte offset
- **Allowed Output:** qualified coordinate object
- **Forbidden Behavior:** contextualizing coordinates; semantic conclusion; implication language
- **Refusal Codes:** `ERR_INVALID_COORDINATE`, `ERR_INTERPRETIVE_METADATA`, `ERR_OFFSET_UNAVAILABLE`

### 4. SCHEMA_VALIDATE

- **Allowed Input:** JSON artifact and canonical schema
- **Allowed Output:** pass/fail result with explicit errors on failure
- **Forbidden Behavior:** soft-fail; warning-only output; partial validation treated as success
- **Refusal Codes:** `ERR_SCHEMA_DRIFT`, `ERR_INCOMPLETE_VALIDATION`, `ERR_SOFT_FAIL`

## Compliance Logic

All transforms must strictly forbid external network access and interpretive reasoning.

If a transform implementation requires a network call, it is disqualified from the MANIC runtime until the remote material is cached or anchored as a local `ROOT_SOURCE`.

If a transform emits semantic claims, summaries, predictions, judgments, or confidence-bearing interpretation, it is no longer a replay transform. It must move to the claim layer and follow MANIC runtime rules for interpretation.

## Runtime Boundary

Replay transforms may create structure.

Replay transforms may not create meaning.

## Status

Coherently Invalid until replayed.

Every map is incomplete.
