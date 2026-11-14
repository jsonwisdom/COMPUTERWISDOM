# RECEIPT CLAIM-CLASS SPECIFICATION V0.1

**Module:** SUPREME_SEYMOUR_V0_1  
**Lane:** HOLD  
**Canon:** false  
**Authority created:** false  
**Formal alias:** HOLD  
**Relationship to prior records:** adjacent; does not overwrite PUBLIC_REPLAY_RUN_BINDING_V0_1 or V0_2.

## Purpose

This specification defines what a receipt is allowed to claim at each evidence level.

It does not replace the repository-wide receipt transport taxonomy in `docs/constitutional_receipt_ledger_v1.md`.

Two axes remain separate:

```text
RECEIPT_TRANSPORT_CLASS != RECEIPT_CLAIM_CLASS
```

The existing transport classes remain available, including:

```text
DOC_RECEIPT
SCHEMA_RECEIPT
CODE_RECEIPT
TEST_RECEIPT
CI_RECEIPT
DEPLOYMENT_RECEIPT
ANCHOR_RECEIPT
DEMOTION_RECEIPT
```

This specification adds claim scope only.

## Claim classes

### RC0 — POINTER_ONLY

Minimum evidence:
- stable source pointer, run ID, commit, file ID, URL, or hash prefix.

May claim:
- the pointer was observed;
- the pointer identifies a named evidence location.

May not claim:
- execution success;
- receipt production;
- artifact contents;
- replay;
- reproduction;
- consensus;
- authority.

### RC1 — EXECUTION_ONLY

Minimum evidence:
- direct execution-status readback from the execution rail;
- named run/job/check;
- terminal status or observed successful step sufficient for the narrow claim.

May claim:
- the named execution completed with the observed status;
- a receipt-emission step reported success when that step is directly observed.

May not claim:
- emitted artifact bytes were inspected;
- artifact contents are correct;
- artifact digest was independently recomputed;
- replay succeeded;
- independent reproduction occurred;
- consensus exists.

Canonical boundary:

```text
EXECUTION_PASS != ARTIFACT_INSPECTION
RECEIPT_EMISSION_STEP_PASS != RECEIPT_CONTENT_VERIFIED
```

### RC2 — PRODUCTION_METADATA

Minimum evidence:
- provider-side artifact/receipt listing or metadata readback.

May claim:
- provider reports the artifact exists;
- observed metadata such as artifact ID, name, size, provider digest, creation time, or run binding.

May not claim:
- artifact bytes were inspected;
- provider digest was independently recomputed;
- parsed receipt fields are correct;
- replay or independent reproduction.

Canonical boundary:

```text
ARTIFACT_LISTED != ARTIFACT_INSPECTED
PROVIDER_DIGEST != LOCALLY_RECOMPUTED_DIGEST
```

### RC3 — ARTIFACT_INSPECTED

Minimum evidence:
- artifact bytes retrieved;
- artifact bytes inspected or parsed;
- local hash computed over the retrieved bytes.

May claim:
- exact retrieved bytes and locally computed hash;
- fields directly parsed from those bytes.

May not claim:
- deterministic replay unless executed;
- independent reproduction;
- consensus;
- authority.

### RC4 — REPLAY_BOUND

Minimum evidence:
- RC3;
- exact bounded input;
- exact expected output;
- replay executed;
- input/output hashes matched the declared binding.

May claim:
- the bounded replay reproduced the expected output on the tested rail/environment.

May not claim:
- independent reproduction unless checker independence is separately established;
- consensus;
- authority.

Canonical boundary:

```text
SAME_RAIL_REPLAY != INDEPENDENT_REPRODUCTION
```

### RC5 — INDEPENDENT_REPRODUCTION

Minimum evidence:
- RC4;
- separate checker identity or execution environment;
- independently retrieved source/input;
- independently executed replay;
- independently computed relevant hashes;
- no reuse of prior output as a substitute for computation.

May claim:
- an independent checker reproduced the bounded result.

May not claim:
- broad consensus from one independent checker;
- authority.

### RC6 — CONSENSUS_EVIDENCE

Minimum evidence:
- declared consensus rule before promotion;
- at least two qualifying independent reproduction receipts unless a stricter rule is declared;
- conflict handling preserved.

May claim:
- the declared consensus threshold was met for the bounded proposition.

May not claim:
- legal, institutional, or adjudicative authority;
- truth outside the proposition and scope actually reproduced.

Canonical boundary:

```text
CONSENSUS_EVIDENCE != AUTHORITY
```

## Non-derivable state

No receipt class creates authority.

```text
RC0 -> RC1 -> RC2 -> RC3 -> RC4 -> RC5 -> RC6
                                  |
                                  +-> AUTHORITY_CREATED = FALSE
```

`AUTHORITY_CREATED = FALSE` is invariant across every class.

## Required common fields

```yaml
receipt_claim_record:
  receipt_id: string
  receipt_transport_class: string
  receipt_claim_class: RC0 | RC1 | RC2 | RC3 | RC4 | RC5 | RC6
  source_rail: string
  source_pointer: string
  observed_at: string | NOT_RECORDED

  execution_status: string | NOT_PERFORMED
  production_metadata_status: string | NOT_PERFORMED
  artifact_inspection: PERFORMED | NOT_PERFORMED
  local_hash_status: COMPUTED | NOT_COMPUTED
  replay_status: PASS | HOLD | REJECT | NOT_PERFORMED
  independent_reproduction: ESTABLISHED | NOT_ESTABLISHED
  consensus_status: ESTABLISHED | NOT_ESTABLISHED

  claims_allowed: []
  claims_forbidden: []

  canon: false
  authority_created: false
```

## Promotion rule

A receipt may move to a higher claim class only when the required new receipt is observed.

```text
LOWER_CLASS_RECEIPT + NARRATIVE != HIGHER_CLASS
ACCESSIBILITY != INSPECTION
INSPECTION != REPLAY
REPLAY != INDEPENDENT_REPRODUCTION
INDEPENDENT_REPRODUCTION != CONSENSUS
CONSENSUS != AUTHORITY
```

No skipped levels are inferred.

A higher-class receipt may cite lower-class receipts, but citation does not retroactively upgrade them.

## Change invalidation

A higher claim class is valid only for the bytes, run, inputs, outputs, and environment it actually binds.

Relevant change requires a new receipt:

```text
CODE_CHANGED -> REPLAY_RECEIPT_STALE
TEST_CHANGED -> TEST/CI_RECEIPT_STALE
FIXTURE_CHANGED -> REPLAY_BINDING_STALE
ARTIFACT_CHANGED -> ARTIFACT_HASH_STALE
RUN_CHANGED -> EXECUTION_POINTER_CHANGED
CONSENSUS_RULE_CHANGED -> CONSENSUS_REEVALUATION_REQUIRED
```

Old receipts remain historical records.

## Application to PUBLIC_REPLAY_RUN_BINDING_V0_2

V0_2 remains adjacent and unchanged.

Its narrow claim:

```yaml
PUBLIC_REPLAY_RUN_BINDING_V0_2:
  receipt_claim_class: RC1_EXECUTION_ONLY
  receipts_produced_basis: EXECUTION_SUCCESS_ONLY
  artifact_inspection: NOT_PERFORMED

  may_claim:
    - "the named execution succeeded as observed"
    - "receipt-producing execution steps succeeded if directly observed"

  may_not_claim:
    - "receipt artifact bytes were inspected"
    - "receipt contents were verified"
    - "artifact digest was independently recomputed"
    - "independent reproduction occurred"
    - "consensus exists"
    - "authority exists"
```

This specification does not silently upgrade V0_2 even if stronger evidence exists elsewhere. A later adjacent receipt must perform and record the stronger observation.

## Binding-edge gate

Any future Binding-Edge Protocol must consume the claim class, not merely the presence of a receipt.

```text
RECEIPT_EXISTS
-> CLASSIFY_CLAIM_SCOPE
-> CHECK_REQUIRED_CLASS_FOR_EDGE
-> BIND | HOLD | REJECT
```

Example:

```text
EDGE_REQUIRES = RC3_ARTIFACT_INSPECTED
AVAILABLE = RC1_EXECUTION_ONLY
RESULT = HOLD
MISSING_RECEIPT = ARTIFACT_INSPECTION
```

## State

```yaml
RECEIPT_CLAIM_CLASS_SPEC_V0_1:
  lane: HOLD
  canon: FALSE
  authority_created: FALSE
  global_receipt_taxonomy_overwritten: FALSE
  public_replay_binding_v0_1_overwritten: FALSE
  public_replay_binding_v0_2_overwritten: FALSE
  next_object: BINDING_EDGE_PROTOCOL
```
