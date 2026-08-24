# REVERSE_REPLAY_REMEMBER_V1

**Standard:** `GBS-BOXDEE-BURDEN-V001`  
**Status:** PROPOSED / PR-BOUND  
**Authority created:** `FALSE`

## Purpose

`ReverseReplayRemember` preserves where to look and which exact receipt bytes must be replayed before a remembered claim may be reused.

```text
MEMORY != PROOF
MEMORY != CURRENT_STATE
MEMORY != AUTHORITY
REMEMBER -> LOCATE -> RE-READ BYTES -> VERIFY HASH -> FREEZE EVIDENCE -> P1
```

## Boundary

`MEMORY_INDEX_V1` is advisory only and MUST NOT be inserted into `INPUT_EVIDENCE_V1`.

P1 performs no live network fetch and no memory lookup. Any external acquisition happens before P1 and must be frozen into `INPUT_EVIDENCE_V1`.

```text
MEMORY_INDEX_V1
  -> pre-verifier acquisition / ReverseReplay
  -> exact receipt-byte verification
  -> frozen INPUT_EVIDENCE_V1
  -> RFC 8785 canonical bytes
  -> SHA-256 inputDigest
  -> P1_VERIFIER_SPEC_V1
  -> canonical RESULT_CONTRACT_V1_OUTPUT bytes
  -> SHA-256 output digest
  -> BOXDEE_BYTE_REPLAY_RECEIPT_V1
```

## Replay-before-reuse law

For each `MEMORY_INDEX_V1.requiredReceipts[*]`, the pre-verifier resolver MUST:

1. re-read the named receipt bytes;
2. compute SHA-256 over those exact bytes;
3. compare to the remembered expected digest;
4. establish that the same digest is bound into the frozen input receipts;
5. fail closed before P1 if any byte receipt is unavailable or mismatched.

`lastDerived`, `lastBurden`, `lastInputDigest`, and `lastOutputDigest` are informative only. They never satisfy current burden.

## Deterministic P1 boundary

P1 consumes only the frozen input object. It MUST NOT depend on wall-clock time, random IDs, live networks, local hostnames, or remembered prior outcomes.

Partial replay remains incompleteness:

```text
PARTIAL_CHAIN  -> HOLD
PARTIAL_REPLAY -> HOLD
INCOMPLETE     != DELTA
```

Actual mismatch remains `DELTA`; invariant failure or explicit contradictory admissible receipts remain `FAIL`.

## Byte identity

`tools/boxdee_p1_verifier_v1.mjs` emits:

- canonical input bytes;
- canonical result bytes;
- a deterministic `BOXDEE_BYTE_REPLAY_RECEIPT_V1` containing raw-input, canonical-input, and canonical-output SHA-256 digests and byte lengths;
- optional memory-resolution byte receipts when `--memory` is supplied.

Canonical output bytes contain no timestamp. Replaying identical canonical input under the same verifier version MUST produce byte-identical canonical output.

## Authority

```text
BYTE_MATCH != AUTHORITY
P1_PASS    != AUTHORITY
MEMORY     != AUTHORITY
AUTHORITY_CREATED = FALSE
```
