# WITNESS_ATTESTATION_CHECKLIST_V1

Status: FROZEN PROCEDURE
Bundle: P0_EXECUTION_HARNESS_V1
Authority: false
Estate advancement: none

## Purpose

This checklist operationalizes `CHAIN_OF_CUSTODY_WITNESS_PROTOCOL_V1` for a single manifest-recovery candidate. It confirms byte preservation and hashing procedure only. It cannot establish admissibility, completeness, repository identity, or authority.

## Candidate linkage

Record before witnessing:

- `candidate_id`
- `execution_id`
- candidate-log entry locator
- source locator
- preserved artifact locator
- operator ID
- witness ID or `WITNESS_NOT_AVAILABLE`

If linkage is incomplete, record `WITNESS_LINKAGE_INCOMPLETE` and stop.

## Witness checklist

The witness must mark each item `OBSERVED`, `INDEPENDENTLY_VERIFIED`, `NOT_OBSERVED`, or `NOT_APPLICABLE`.

1. Source location or transfer surface was identified.
2. Original filename or source label was recorded.
3. Preserved raw artifact exists at the recorded locator.
4. Preservation occurred before parsing, normalization, or transcription.
5. Preserved byte length matches the candidate-log entry.
6. SHA-256 was computed over preserved raw bytes.
7. Hashing tool and version were recorded.
8. The recorded SHA-256 digest has 64 lowercase hexadecimal characters.
9. The witness independently recomputed the digest when access allowed.
10. Independent digest matches the operator digest.
11. Recovery observation time is recorded in RFC 3339 UTC.
12. Preservation time is recorded separately.
13. Hashing time is recorded separately.
14. Historical capture time is not inferred from recovery time.
15. Operator identity is recorded.
16. Witness identity or unavailability is recorded.
17. Access limitations and provenance ambiguity are visible.
18. `self_ratification` remains `false`.
19. `authority` remains `false`.
20. No identity extraction or reconciliation authorization is present.

## Digest outcome

Record exactly one:

- `HASH_MATCH`
- `HASH_MISMATCH`
- `INDEPENDENT_REHASH_NOT_AVAILABLE`
- `HASH_PROCEDURE_NOT_OBSERVED`

`HASH_MISMATCH` suspends admissibility evaluation and must be recorded without replacing either digest.

## Witness attestation statement

Use the bounded statement:

> I observed or independently reproduced preservation and SHA-256 hashing of the identified candidate artifact. This attestation establishes the observed byte identity and procedure only. It does not establish historical completeness, admissibility, repository identity, authorization to extract names, authorization to reconcile, or authority.

## Required witness record

The completed checklist must record:

- candidate ID
- execution ID
- witness ID or unavailability code
- witness UTC timestamp
- item-level observations
- operator digest
- independently computed digest or `null`
- digest outcome
- limitations
- bounded attestation statement
- `admissibility_authorized: false`
- `identity_extraction_authorized: false`
- `reconciliation_authorized: false`
- `authority: false`

## Failure codes

- `WITNESS_LINKAGE_INCOMPLETE`
- `WITNESS_NOT_AVAILABLE`
- `SOURCE_LOCATOR_NOT_OBSERVED`
- `RAW_ARTIFACT_NOT_OBSERVED`
- `PRESERVATION_ORDER_UNKNOWN`
- `BYTE_LENGTH_MISMATCH`
- `HASH_TOOL_NOT_RECORDED`
- `DIGEST_FORMAT_INVALID`
- `HASH_MISMATCH`
- `INDEPENDENT_REHASH_NOT_AVAILABLE`
- `TIMESTAMP_ROLE_CONFUSION`
- `OPERATOR_ID_MISSING`
- `WITNESS_ID_MISSING`
- `PROVENANCE_AMBIGUOUS`
- `SELF_RATIFICATION_ATTEMPT`
- `AUTHORITY_ELEVATION_ATTEMPT`

## Completion rule

Checklist completion means only that witness observations were recorded. A fully checked witness record is not an admissibility decision.

## Constitutional boundary

`WITNESSED BYTES` is not `HISTORICAL SOURCE PROVEN`.

`HISTORICAL SOURCE PROVEN` is not `COMPLETE MANIFEST PROVEN`.

`COMPLETE MANIFEST PROVEN` is not `RECONCILIATION AUTHORIZED`.

Authority remains false.
