# CANDIDATE_LOG_POPULATION_WORKFLOW_V1

Status: FROZEN PROCEDURE
Bundle: P0_EXECUTION_HARNESS_V1
Authority: false
Estate advancement: none

## Purpose

This workflow governs how a preserved historical-source candidate is added to `MANIFEST_RECOVERY_CANDIDATE_LOG_V1.json`. It does not decide admissibility, extract repository identities, or authorize reconciliation.

## Preconditions

A candidate-log entry may be populated only when:

1. A checklist execution record exists.
2. A candidate artifact has been preserved as raw bytes.
3. The raw artifact has a recorded byte length.
4. SHA-256 has been computed over the preserved bytes.
5. A stable `candidate_id` and `execution_id` exist.
6. The source locator and recovery timestamp are known.

If any precondition fails, do not create a partial identity-bearing record. Record the appropriate failure code in the execution record.

## Population sequence

1. Copy `CANDIDATE_LOG_ENTRY_TEMPLATE_V1.json` into a new in-memory record.
2. Populate `candidate_id` and `execution_id`.
3. Populate the source class and source locator exactly as observed.
4. Record the original filename or source label without normalization.
5. Record recovery observation, preservation, and hashing timestamps separately in RFC 3339 UTC.
6. Record historical capture time only when directly supported by the source. Otherwise use `null` and add `CAPTURE_TIME_UNKNOWN`.
7. Record preserved artifact path, byte length, SHA-256 digest, and hashing tool.
8. Record operator identity and operator attestation.
9. Record witness status as `PENDING`, `COMPLETED`, or `WITNESS_NOT_AVAILABLE`.
10. Record limitations and unresolved provenance explicitly.
11. Set `self_ratification` to `false`.
12. Set `authority` to `false`.
13. Set `admissibility.status` to `NOT_EVALUATED`.
14. Set `identity_extraction_authorized` to `false`.
15. Set `original_72_manifest_authorized` to `false`.
16. Set `reconciliation_authorized` to `false`.
17. Append the complete record to the candidate log without rewriting prior candidate entries.
18. Validate the resulting JSON.
19. Preserve the updated candidate log as a new repository version through normal commit history.

## Required fields

A populated candidate entry must include:

- candidate ID
- execution ID
- source class
- source locator
- original filename or source label
- recovery timestamp
- preservation timestamp
- hashing timestamp
- historical capture timestamp or explicit unknown state
- preserved artifact path
- byte length
- SHA-256 digest
- hashing tool and version
- operator identity
- witness status
- provenance limitations
- admissibility status
- authorization booleans
- `self_ratification: false`
- `authority: false`

## Failure codes

Use one or more of:

- `CHECKLIST_LINK_MISSING`
- `CANDIDATE_ID_MISSING`
- `EXECUTION_ID_MISSING`
- `SOURCE_CLASS_MISSING`
- `SOURCE_LOCATOR_MISSING`
- `RAW_ARTIFACT_NOT_PRESERVED`
- `BYTE_LENGTH_MISSING`
- `DIGEST_MISSING`
- `DIGEST_FORMAT_INVALID`
- `TIMESTAMP_MISSING`
- `CAPTURE_TIME_UNKNOWN`
- `OPERATOR_ID_MISSING`
- `WITNESS_PENDING`
- `WITNESS_NOT_AVAILABLE`
- `PROVENANCE_AMBIGUOUS`
- `PRESENT_DAY_DERIVATION_DETECTED`
- `SELF_RATIFICATION_ATTEMPT`
- `IDENTITY_EXTRACTION_ATTEMPT`
- `RECONCILIATION_AUTHORIZATION_ATTEMPT`

## Append-only rule

Candidate history is append-only.

- Do not delete rejected candidates.
- Do not replace earlier digests.
- Do not rewrite source locators.
- Corrections must be additional records referencing the prior candidate entry.
- A later admissibility decision must not alter the raw candidate record.

## Boundary

A populated candidate log proves only that a candidate was recovered, preserved, hashed, and recorded under the frozen procedure.

It does not prove:

- historical completeness
- authenticity of the claimed capture time
- presence of all 75 repository names
- identity of the original 72 non-anchor repositories
- authorization to transcribe names
- authorization to reconcile

Authority remains false.
