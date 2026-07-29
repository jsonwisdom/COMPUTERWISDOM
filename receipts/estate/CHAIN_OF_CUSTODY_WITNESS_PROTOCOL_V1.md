# CHAIN_OF_CUSTODY_WITNESS_PROTOCOL_V1

Status: FROZEN PROCEDURE
Authority: false
Estate advancement: none

## Purpose

This protocol governs witnessing, hashing, timestamping, and actor attribution for historical manifest-recovery candidates. It does not determine candidate admissibility by itself and cannot establish repository identity.

## Roles

### Operator

The operator performs the search or receives the candidate artifact, preserves the raw bytes, computes the digest, and creates the candidate-log entry.

### Witness

The witness independently observes the preservation and hashing procedure. The witness must not claim that the candidate is admissible merely because the bytes and digest were observed.

### Admissibility reviewer

The admissibility reviewer evaluates provenance, integrity, completeness, and non-derivation. This role must remain logically distinct from the artifact's historical creator. When operator and reviewer are the same person, the record must disclose that limitation and cannot claim independent review.

## Required witness observations

A witness attestation must record that the witness observed or independently verified:

1. The source location or transfer surface from which the candidate was obtained.
2. The candidate's original filename or source label.
3. Preservation of the candidate without content modification.
4. The preserved artifact's byte length.
5. The SHA-256 calculation over the preserved raw bytes.
6. The resulting SHA-256 digest.
7. The UTC timestamp of observation.
8. The operator identity or stable operator identifier.
9. Any access limitations, missing provenance, or ambiguity.

## Hash procedure

- Hash the preserved raw file bytes, not extracted text or a normalized copy.
- Use SHA-256.
- Record the digest as 64 lowercase hexadecimal characters.
- Record the exact tool and command or implementation used.
- Recompute the digest independently when a witness has the required access.
- A digest mismatch must produce `HASH_MISMATCH` and suspend admissibility evaluation.

## Timestamp rules

Every attestation must use an RFC 3339 UTC timestamp.

The record must distinguish:

- historical capture time, when known
- recovery observation time
- preservation time
- hashing time
- witness attestation time

Recovery time must never be represented as historical capture time.

## Attestation statement

A compliant witness statement must communicate only the bounded claim:

> I observed or independently reproduced preservation and SHA-256 hashing of the identified candidate artifact. This attestation establishes the observed byte identity and procedure only. It does not establish historical completeness, admissibility, repository identity, or authority.

## Independence and self-ratification

- A candidate must not become admissible solely through the operator's own assertion.
- Absence of an independent witness must be recorded as `WITNESS_NOT_AVAILABLE`.
- Lack of a witness does not automatically destroy a candidate, but it lowers evidentiary strength and must remain visible.
- `self_ratification` must remain `false`.
- No witness may authorize `ORIGINAL_72_MANIFEST_V1`; authorization requires a separate admissibility decision under the frozen rules.

## Required record fields

- candidate_id
- execution_id
- operator_id
- witness_id or `WITNESS_NOT_AVAILABLE`
- source locator
- preserved artifact locator
- byte length
- SHA-256 digest
- hashing tool and version
- operator timestamp
- witness timestamp
- limitations
- operator attestation
- witness attestation
- authority: false

## Failure and rejection codes

- `SOURCE_LOCATOR_MISSING`
- `RAW_ARTIFACT_NOT_PRESERVED`
- `BYTE_LENGTH_MISSING`
- `DIGEST_MISSING`
- `DIGEST_FORMAT_INVALID`
- `HASH_MISMATCH`
- `TIMESTAMP_MISSING`
- `TIMESTAMP_ROLE_CONFUSION`
- `OPERATOR_ID_MISSING`
- `WITNESS_NOT_AVAILABLE`
- `WITNESS_ID_MISSING`
- `SELF_RATIFICATION_ATTEMPT`
- `PROVENANCE_AMBIGUOUS`

## Boundary

A valid witness record proves only that a particular byte sequence was observed and hashed under a documented procedure.

It does not prove:

- that the artifact is historical
- that it contains all 75 repositories
- that it contains the original 72 non-anchor identities
- that names may be extracted
- that reconciliation may begin
- that authority has changed

Authority remains false.
