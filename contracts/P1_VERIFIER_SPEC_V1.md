# P1_VERIFIER_SPEC_V1

**Class:** Gray Baby / BoxDee deterministic verifier contract  
**Standard:** `GBS-BOXDEE-BURDEN-V001`  
**Status:** PROPOSED / PR-BOUND  
**Authority created:** `FALSE`

## 1. Purpose

Define the deterministic executable boundary that consumes caller-supplied evidence and emits a verifier-owned result candidate without allowing callers, visualizations, draft artifacts, or receipts alone to self-promote into PASS.

```text
CALLER INPUT      != RESULT
SCHEMA_VALID      != PASS
VERIFIER OUTPUT   = RESULT CANDIDATE
PASS              != AUTHORITY
AUTHORITY_CREATED = FALSE
```

This file is normative for P1 behavior within the proposing branch. It does not become repository-wide canonical merely by existing in an open pull request.

## 2. Contract bindings

P1 MUST consume:

`contracts/INPUT_EVIDENCE_V1.schema.json`

P1 MUST emit:

`contracts/RESULT_CONTRACT_V1_OUTPUT.schema.json`

The historical transition-receipt schema remains:

`docs/gray-baby/GBS_BOXDEE_BURDEN_V001.schema.json`

`FAIL` is introduced by the P1 output contract as a verifier-level disposition. This does not silently rewrite historical receipt objects that were valid under the earlier `PASS | DELTA | HOLD` receipt schema.

## 3. Required surfaces

The verifier MUST evaluate these surfaces independently:

1. `SOURCE`
2. `OBJECT`
3. `TIME`
4. `ACTION`
5. `READBACK`

For PASS eligibility:

```text
SOURCE.status   = OBSERVED
OBJECT.status   = OBSERVED
TIME.status     = OBSERVED
ACTION.status   = OBSERVED
READBACK.status = MATCH
```

The object identifier and time value MUST be non-empty for PASS eligibility.

## 4. Evidence admissibility

P1 recognizes three artifact classes from `INPUT_EVIDENCE_V1.receipts[*].class`:

- `RECEIPT` — may support a bounded observation when correctly bound and internally consistent.
- `VISUALIZATION` — illustrative only; MUST NOT satisfy burden.
- `DRAFT` — intent/scaffolding only; MUST NOT satisfy burden.

Constitutional rules:

```text
RECEIPT_EXISTENCE != BURDEN_SATISFIED
VISUALIZATION     != EVIDENCE_OF_UNDERLYING_CLAIM
DRAFT             != EVIDENCE
SCREENSHOT        != BACKEND_CAUSE
SEARCH_MISS       != ABSENCE
UNOBSERVED        != NONEXISTENT
```

A receipt may prove only the bounded fact the receipt actually witnesses.

## 5. Internal flags

The caller MUST NOT provide internal flags. P1 MUST derive all flags from validated input and reconciliation logic.

P1 emits:

- `hasInvariantViolation`
- `hasContradictoryReceipts`
- `hasMismatch`
- `hasPartialChain`
- `hasPartialReplay`
- `hasMissingEvidence`

### 5.1 hasInvariantViolation

TRUE when P1 detects a violation of a constitutional invariant or an impossible internal state after schema validation and normalization.

Examples include an attempted result/authority injection into a caller input path, broken deterministic normalization, or an implementation state that cannot satisfy this specification.

### 5.2 hasContradictoryReceipts

TRUE only when two or more admissible, bound receipts make mutually incompatible assertions about the same bounded object, time/action edge, or resulting state and the contradiction cannot be reconciled by scope.

Missing receipts are not contradictions.

### 5.3 hasMismatch

TRUE when the bound readback materially disagrees with the state required by the frozen claim/action relationship.

`READBACK.status = MISMATCH` MUST set `hasMismatch = true` unless a higher-order invariant failure prevents trustworthy evaluation.

### 5.4 hasPartialChain

TRUE when `replay.chainStatus = PARTIAL`.

A partial chain is incompleteness, not contradiction.

### 5.5 hasPartialReplay

TRUE when `replay.replayStatus = PARTIAL`.

A partial replay is incompleteness, not contradiction.

### 5.6 hasMissingEvidence

TRUE when any required evidence edge is absent, unavailable, invalid, search-missed, asserted-only where observation is required, or otherwise insufficient for burden satisfaction.

`hasPartialChain` or `hasPartialReplay` MUST contribute to `hasMissingEvidence` unless an independently established bound mismatch or contradiction already determines a higher-precedence disposition.

## 6. Constitutional precedence

The disposition precedence is:

```text
FAIL > DELTA > HOLD > PASS
```

Precedence is ordered. Lower states MUST NOT override a state already established by a higher rule.

### 6.1 FAIL

Emit `FAIL` when:

```text
hasInvariantViolation == true
OR
hasContradictoryReceipts == true
```

`FAIL` represents an invalid or internally contradictory verifier/evidence state. It MUST NOT be promoted to PASS, DELTA, or authority.

### 6.2 DELTA

If FAIL did not trigger, emit `DELTA` when:

```text
hasMismatch == true
```

DELTA requires an actual bounded disagreement.

```text
INCOMPLETE != DELTA
MISSING EDGE -> HOLD
BOUND CONTRADICTION OR MISMATCH -> DELTA or FAIL according to this spec
```

Partial chain or partial replay alone MUST NOT trigger DELTA.

### 6.3 HOLD

If neither FAIL nor DELTA triggered, emit `HOLD` when any of the following is true:

```text
hasMissingEvidence == true
SOURCE.status in {UNOBSERVED, INVALID, SEARCH_MISS}
OBJECT.status in {UNOBSERVED, INVALID}
TIME.status in {UNOBSERVED, INVALID}
ACTION.status in {UNOBSERVED, INVALID, ASSERTED_ONLY}
READBACK.status == UNAVAILABLE
hasPartialChain == true
hasPartialReplay == true
burdenSatisfied == false
```

HOLD means the required burden has not been fully discharged. It does not mean the asserted claim is false or nonexistent.

### 6.4 PASS

PASS is reachable only if FAIL, DELTA, and HOLD conditions are all false and every required edge is independently satisfied.

```text
SOURCE.status      == OBSERVED
OBJECT.status      == OBSERVED
OBJECT.identifier  != empty
TIME.status        == OBSERVED
TIME.value         != empty
ACTION.status      == OBSERVED
READBACK.status    == MATCH
hasPartialChain    == false
hasPartialReplay   == false
hasMissingEvidence == false
burdenSatisfied    == true
```

P1 MUST derive `burdenSatisfied`; the caller cannot supply it.

PASS is scoped only to the frozen bounded claim and MUST NOT create institutional, governmental, legal, identity, protocol, repository, or operator authority.

## 7. Burden derivation

P1 MUST compute `burdenSatisfied` after evidence classification and reconciliation.

`burdenSatisfied = true` only when:

1. every required surface is PASS-eligible;
2. readback is MATCH;
3. required replay edges are complete;
4. no invariant violation exists;
5. no contradictory admissible receipts exist;
6. no mismatch exists;
7. each relied-upon claim edge is supported by at least one appropriately bound admissible receipt or direct verifier observation;
8. no relied-upon support is solely a visualization or draft artifact.

Receipt count alone MUST NOT determine burden.

## 8. Deterministic algorithm

P1 MUST implement the following logical order:

```text
validate INPUT_EVIDENCE_V1
canonicalize input using RFC 8785 JSON Canonicalization Scheme
inputDigest = SHA256(canonical_input_bytes)

classify receipts
bind receipts to SOURCE / OBJECT / TIME / ACTION / READBACK
reconcile bounded assertions

flags.hasInvariantViolation      = deriveInvariantViolation()
flags.hasContradictoryReceipts   = deriveContradictoryReceipts()
flags.hasMismatch                = deriveMismatch()
flags.hasPartialChain            = replay.chainStatus == PARTIAL
flags.hasPartialReplay           = replay.replayStatus == PARTIAL
flags.hasMissingEvidence         = deriveMissingEvidence()

burdenSatisfied = deriveBurden()

if flags.hasInvariantViolation or flags.hasContradictoryReceipts:
    derivedResult = FAIL
else if flags.hasMismatch:
    derivedResult = DELTA
else if flags.hasMissingEvidence
     or flags.hasPartialChain
     or flags.hasPartialReplay
     or burdenSatisfied == false:
    derivedResult = HOLD
else:
    derivedResult = PASS

authority = false
emit RESULT_CONTRACT_V1_OUTPUT
```

The same normalized input under the same verifier version MUST produce the same normative output fields.

## 9. Output determinism

P1 MUST NOT include wall-clock time, random IDs, machine-local paths, hostnames, unordered reason generation, network race results, or other nondeterministic values in normative result derivation.

If `reasons` are emitted, they MUST be generated from a fixed reason-code vocabulary and sorted deterministically before serialization.

Network observation, if required, MUST first be captured into `INPUT_EVIDENCE_V1`; P1 verifies the frozen evidence object rather than racing live networks during derivation.

## 10. Caller boundary

Caller-controlled input MUST NOT include:

- `derivedResult`
- `burdenSatisfied`
- `authority`
- internal flags
- verifier-owned reason codes

Any transport or wrapper that attempts to inject these fields into the P1 input object MUST be rejected by the input schema or treated as an invariant violation before result promotion.

## 11. Authority boundary

The output contract MUST enforce:

```text
AUTHORITY_CREATED = FALSE
PASS != AUTHORITY
CI_PASS != AUTHORITY
VERIFIER_PASS != AUTHORITY
```

P1 has no authority-elevation code path.

## 12. Legacy compatibility

`docs/gray-baby/GBS_BOXDEE_BURDEN_V001.schema.json` remains the historical transition-receipt schema for this PR history.

The P1 contract set creates a stricter caller/verifier separation:

```text
INPUT_EVIDENCE_V1
      -> P1_VERIFIER_SPEC_V1
      -> RESULT_CONTRACT_V1_OUTPUT
```

Historical receipts MUST NOT be relabeled as P1 verifier output unless they are replayed through an implementation conforming to this specification.

## 13. Minimum conformance vectors

A P1 implementation is not conformant until deterministic tests establish at least:

1. all required observations + MATCH + complete replay -> PASS;
2. missing SOURCE -> HOLD;
3. SEARCH_MISS -> HOLD, not absence;
4. unavailable READBACK -> HOLD;
5. partial chain only -> HOLD;
6. partial replay only -> HOLD;
7. bound MISMATCH -> DELTA;
8. contradictory admissible receipts -> FAIL;
9. invariant violation -> FAIL;
10. visualization-only support -> HOLD;
11. draft-only support -> HOLD;
12. PASS output still has `authority = false`;
13. repeated execution on identical canonical input produces identical normative output.

Until these vectors pass against an executable P1 implementation:

```text
P1_CANONICAL_PASS = NOT ESTABLISHED
REPOSITORY_WIDE_GBS_PASS = NOT ESTABLISHED
AUTHORITY_CREATED = FALSE
```

## 14. Current constitutional status

This specification defines the executable contract boundary. It is not itself execution evidence.

```text
SPEC_EXISTS       != VERIFIER_IMPLEMENTED
SCHEMA_VALID       != PASS
TEST_VECTOR_EXISTS != TEST_VECTOR_PASSED
PR_FILE_EXISTS     != REPOSITORY_CANONICAL
AUTHORITY_CREATED   = FALSE
```
