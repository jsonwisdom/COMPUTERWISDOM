# P0_DIRECTORY_LAYOUT_V1

Status: FROZEN CONTROL
Authority: false
Estate advancement: none

## Purpose

This document defines the deterministic filesystem layout for P0 manifest-recovery execution. It governs paths and filenames only. It does not create evidence, establish admissibility, or authorize identity extraction.

## Root

All P0 execution material must be stored under:

```text
evidence/estate/p0/
```

## Per-run layout

Each run uses one immutable execution directory:

```text
evidence/estate/p0/<execution_id>/
├── operator/
│   ├── checklist.json
│   └── checklist.md
├── search/
│   ├── terms.txt
│   ├── locations.json
│   └── execution.log
├── candidates/
│   └── <candidate_id>/
│       ├── raw.bin
│       ├── raw.bin.sha256
│       ├── metadata.json
│       ├── operator-attestation.json
│       └── witness-attestation.json
├── results/
│   ├── outcome.json
│   └── candidate-links.json
└── receipt/
    └── P0_RUN_RECEIPT_V1.json
```

## Identifier rules

- `execution_id` must be unique and stable.
- `candidate_id` must be unique within the candidate log and must not encode inferred repository identities.
- Identifiers must not be renamed after creation.
- Paths must use the recorded identifiers exactly.

## Raw artifact rule

`raw.bin` is the exact preserved byte sequence obtained from the historical source or transfer surface.

- It must be written before content inspection.
- It must not be normalized, reformatted, decompressed into replacement content, or regenerated.
- The original filename or source label belongs in `metadata.json`; it does not replace `raw.bin`.
- Derivative inspection copies, when necessary, must be stored outside the authoritative candidate directory and identified as derivatives.

## Digest file

`raw.bin.sha256` must contain exactly:

```text
<64-lowercase-hex-digest>  raw.bin
```

The digest must be computed over `raw.bin` bytes.

## Metadata requirements

`metadata.json` must record:

- candidate_id
- execution_id
- source_class
- source_locator
- original_filename_or_label
- historical_capture_timestamp_utc or `UNKNOWN`
- recovery_observation_timestamp_utc
- preservation_timestamp_utc
- byte_length
- sha256
- hashing_tool
- hashing_command_or_implementation
- access_state
- operator_id
- witness_state
- admissibility.status: `NOT_EVALUATED`
- identity_extraction_authorized: false
- reconciliation_authorized: false
- self_ratification: false
- authority: false

## No-result layout

For `NO_RESULT`, `ACCESS_DENIED`, `SOURCE_UNAVAILABLE`, or `RUN_ABORTED`:

- do not create a candidate directory
- preserve `operator/`, `search/`, `results/`, and `receipt/`
- record the exact outcome and limitations
- do not create placeholder `raw.bin` files

## Immutability

After the run receipt is finalized:

- existing files must not be overwritten
- corrections require a new execution ID or an append-only correction receipt
- candidate bytes and digests are immutable
- deletion is prohibited during the active recovery process

## Prohibited paths and substitutions

The following are prohibited:

- storing live GitHub inventory as a historical candidate
- naming candidate directories after inferred repositories
- replacing `raw.bin` with extracted text
- combining multiple candidate artifacts into one `raw.bin`
- silently overwriting an earlier candidate
- treating directory existence as evidence admissibility

## Boundary

A conforming directory proves only that execution material was arranged under the frozen structure. It does not prove historical provenance, completeness, admissibility, repository identity, or reconciliation authority.

Authority remains false.
