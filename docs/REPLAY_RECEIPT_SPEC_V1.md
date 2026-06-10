# REPLAY_RECEIPT_SPEC_V1

## Status

Canonical draft for Computer Wisdom.

This specification defines the replay receipt as the machine-verifiable proof surface beneath reputation continuity.

REPUTATION_CONTINUITY_SPEC_V1 defines what reputation continuity is.

REPLAY_RECEIPT_SPEC_V1 defines how continuity claims become testable, challengeable, and replay-aware.

---

## Core Doctrine

Brief = doorway.
Reputation Spec = canon.
Replay Receipt Spec = executable proof surface.

A replay receipt is not a narrative summary.

A replay receipt is a bounded, inspectable, machine-verifiable artifact or reference that declares what happened, what evidence was used, what rules applied, and how an independent verifier may evaluate the claim.

---

## 1. Canonical Receipt Fields

A replay receipt SHOULD contain the following fields when applicable:

```json
{
  "spec": "REPLAY_RECEIPT_SPEC_V1",
  "receipt_id": "string",
  "identity_ref": "string",
  "action_ref": "string",
  "timestamp": "string",
  "monotonic_counter": "string_or_number",
  "execution_environment": {
    "runtime": "string",
    "version": "string",
    "environment_hash": "string"
  },
  "source_artifacts": [
    {
      "uri": "string",
      "commit": "string",
      "sha256": "string"
    }
  ],
  "replay_parameters": {
    "canonicalization": "string",
    "hash_algorithm": "SHA-256",
    "verifier_version": "string",
    "scope": "string"
  },
  "output": {
    "claim": "string",
    "output_hash": "string"
  },
  "attestation": {
    "type": "string",
    "signature": "string",
    "attester": "string"
  },
  "human_summary_ref": "string"
}
```

Required minimum fields:

- spec
- receipt_id
- identity_ref
- action_ref
- source_artifacts
- replay_parameters
- output

A receipt MAY include timestamp, monotonic counter, signature, attestation, block reference, or hardware attestation when available.

A receipt MUST NOT imply that optional attestations exist when they do not.

---

## 2. Hash Rules

Deterministic receipts MUST define their hash rules explicitly.

Requirements:

- canonical JSON sorting or another declared canonical serialization format
- UTF-8 byte encoding unless another encoding is explicitly declared
- SHA-256 as the default content hash
- no non-cryptographic hashes for canonical proof claims
- no environment-dependent serialization
- no hidden normalization rules
- no mutable source artifacts without content hash binding

A hash binds bytes, not intention.

A receipt summary is not the hashed artifact unless explicitly canonicalized and declared as such.

---

## 3. Source Artifact Binding

A replay receipt MUST bind to the source artifacts needed to evaluate its claim.

Source artifact references SHOULD include:

- exact repository or storage URI
- exact commit or version identifier
- exact file path when applicable
- content hash
- dependency hash or lockfile hash when applicable
- artifact role

This prevents receipt laundering.

A receipt MUST NOT point vaguely at a project, folder, platform account, or institution and treat that as sufficient proof.

Operational authority is not canonical proof.

---

## 4. Verifier Assumptions

A replay receipt MUST declare what the verifier is expected to trust, recompute, reject, and ignore.

Verifier assumptions SHOULD include:

- trusted root or identity reference
- accepted canonicalization algorithm
- accepted hash algorithm
- accepted dependency graph
- required source artifacts
- runtime assumptions
- network assumptions, if any
- clock or block assumptions, if any
- attestation assumptions, if any

Verifier duties:

- recompute declared hashes when possible
- reject missing required artifacts
- reject undeclared canonicalization changes
- reject environment-dependent ambiguity in deterministic claims
- record divergence rather than silently normalizing it

A verifier MUST NOT treat human prose as proof unless the prose is itself the canonical artifact being verified.

---

## 5. Replay Scope

Every replay receipt MUST declare its replay scope.

Replay scope MAY be:

- byte-identical replay
- deterministic recomputation
- schema validation
- signature verification
- attestation verification
- provenance traversal
- bounded human-readable audit

The receipt MUST declare:

- what must be replayed
- what may be replayed
- what cannot be replayed
- what counts as replay equivalence
- what inputs are required
- what outputs are expected

Replay does not prove total truth.

Replay proves whether the declared claim survives the declared verification procedure.

---

## 6. Divergence Handling

A replay system MUST make divergence explicit.

Divergence classes:

- MISSING_ARTIFACT
- HASH_MISMATCH
- CANONICALIZATION_DRIFT
- RUNTIME_DRIFT
- DEPENDENCY_DRIFT
- NONDETERMINISTIC_OUTPUT
- SIGNATURE_INVALID
- ATTESTATION_INVALID
- SCOPE_UNVERIFIABLE
- HUMAN_INTERPRETATION_CONFLICT

A divergence record SHOULD include:

- receipt_id
- divergence_class
- expected_value
- observed_value
- verifier_identity
- verifier_version
- timestamp or block reference
- notes_ref, if human explanation is needed

No silent fork.

No hidden normalization.

No collapsing divergence into narrative.

---

## 7. Supersession and Revocation Rules

Receipts MUST be lineage-aware.

A receipt MAY be:

- active
- superseded
- revoked
- disputed
- deprecated
- unverifiable

Supersession MUST preserve:

- prior receipt reference
- new receipt reference
- reason code
- actor or authority making the change
- timestamp or monotonic event reference
- evidence reference

Revocation MUST NOT erase the original receipt.

Revocation records the change in status while preserving history.

Continuity is preserved through explicit lineage, not deletion.

---

## 8. Human Summary Separation

Machine receipts and human summaries MUST remain separate.

A human summary MAY explain:

- what the receipt means
- why it matters
- what institution should review
- what context affects interpretation
- what limitations remain

A human summary MUST NOT replace:

- canonical bytes
- source artifact hashes
- verifier outputs
- divergence records
- attestation envelopes

Narrative can guide inspection.

Narrative cannot substitute for receipt evidence.

---

## Minimal Valid Receipt Example

```json
{
  "spec": "REPLAY_RECEIPT_SPEC_V1",
  "receipt_id": "sha256:example",
  "identity_ref": "jaywisdom.base.eth",
  "action_ref": "docs/REPUTATION_CONTINUITY_SPEC_V1.md committed",
  "source_artifacts": [
    {
      "uri": "github:jsonwisdom/COMPUTERWISDOM/docs/REPUTATION_CONTINUITY_SPEC_V1.md",
      "commit": "466ea2f3ed612b34e613d7dbc616e127d993a37c",
      "sha256": "TBD_AFTER_CANONICAL_HASH"
    }
  ],
  "replay_parameters": {
    "canonicalization": "UTF-8 file bytes",
    "hash_algorithm": "SHA-256",
    "verifier_version": "manual_v1",
    "scope": "content hash verification"
  },
  "output": {
    "claim": "Reputation Continuity Spec V1 exists at declared commit and path",
    "output_hash": "TBD_AFTER_CANONICAL_HASH"
  },
  "human_summary_ref": "docs/REPUTATION_CONTINUITY_SPEC_V1.md"
}
```

---

## Boundary Rule

A receipt is not legitimacy by itself.

A hash is not meaning by itself.

A signature is not trust by itself.

A replay result is not human interpretation by itself.

Computer Wisdom keeps these surfaces connected but distinct.

---

## Closing Statement

The replay receipt is the executable proof surface beneath Computer Wisdom.

It turns continuity claims into inspectable artifacts.

It does not eliminate human judgment.

It gives human judgment a stable surface to inspect.
