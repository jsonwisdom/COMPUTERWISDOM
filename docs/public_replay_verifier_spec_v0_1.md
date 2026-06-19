# COMPUTERWISDOM_PUBLIC_REPLAY_VERIFIER_SPEC_V0_1

Status: DRAFT_READY  
Authority: false

## Purpose

This specification defines the deterministic behavior of a conforming Computer Wisdom public replay verifier.

A conforming verifier consumes a `COMPUTERWISDOM_REPLAY_PACKET_V1` object and emits exactly one `COMPUTERWISDOM_REPLAY_VERIFIER_V0_2` object.

The verifier does not create authority. It classifies replayability from observable evidence.

## I/O Contract

For any valid `COMPUTERWISDOM_REPLAY_PACKET_V1`, a conforming verifier must emit exactly one `COMPUTERWISDOM_REPLAY_VERIFIER_V0_2` object whose `status`, `promotion_allowed`, `replay_result`, and `verification_mode` are determined only by this specification and the observable state of the referenced evidence systems.

## State Space

Valid output states:

- `MAINTAIN`
- `OBSERVE`
- `PARTIAL_REPLAY_READY`
- `ANCHOR_READY`
- `ANCHORED`
- `FULLY_REPLAYABLE`

Authority must always be `false`.

## Deterministic Rules

### 1. Hash Mismatch Rule

If recomputed `sha256(claim_text)` does not equal `claim_hash`, the verifier must emit:

```json
{
  "status": "MAINTAIN",
  "promotion_allowed": false,
  "reconstructable": false,
  "survival_test": "FAIL"
}
```

Hash mismatch is a hard floor. No other evidence layer can override it.

### 2. Evidence Layer Failure Rule

If any required evidence layer fails hard, including GitHub, Base/EAS, or archive/IPFS, the verifier must not emit `ANCHORED` or `FULLY_REPLAYABLE`.

The maximum allowed status is:

```text
PARTIAL_REPLAY_READY
```

### 3. Routing Layer Failure Rule

Routing layer failures are non-fatal.

Examples:

- Zora unavailable
- X post unavailable
- Website unavailable
- Newsletter unavailable

If evidence layers remain valid, routing failure must not downgrade an otherwise valid packet.

### 4. Success Ceiling Rule

If all required checks pass and the survival test is run and passes, the verifier may emit:

```json
{
  "status": "FULLY_REPLAYABLE",
  "promotion_allowed": true,
  "reconstructable": true,
  "survival_test": "PASS"
}
```

## Failure Rule Mapping

```json
{
  "hash_mismatch": {
    "status": "MAINTAIN",
    "promotion_allowed": false
  },
  "any_evidence_layer_invalid": {
    "max_status": "PARTIAL_REPLAY_READY"
  },
  "routing_only_failure": {
    "non_fatal": true
  }
}
```

## Reference Artifacts

Schemas:

- `schemas/replay_packet.v1.schema.json`
- `schemas/replay_verifier.v0_2.schema.json`
- `schemas/replay_verifier_chain.v1.schema.json`
- `schemas/chain_of_receipts.v1.schema.json`

Golden vectors:

- `tests/public_replay_verifier_vectors_v0_1/`

Reference verifier:

- `tools/reference_replay_verifier_v0_1.py`

Verifier chain generator:

- `tools/replay_verifier_chain_generator_v0_1.py`

## Protocol Invariant

Anyone may build a verifier.

All conforming verifiers must land in the same classification state for the same packet and the same observable evidence state.

## Closing Rule

Receipts beat arguments.

Routing is not evidence.

Evidence failure is critical.

Authority remains false.
