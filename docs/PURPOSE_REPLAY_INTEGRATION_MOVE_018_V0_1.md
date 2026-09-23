# MOVE-018 — Purpose/RePlay Integration v0.1

```text
MOVE                 = MOVE_018
ROUND                = MATERIALIZED_DESIGN
VERIFICATION_LEVEL   = LEVEL_2_DESIGN_DISCUSSION
PROTOCOL_CLAIM       = FALSE
IMPLEMENTED          = FALSE
AUTHORITY_CREATED    = FALSE
NEXT_TRANSITION      = HUMAN_REVIEWS_PURPOSE_INTEGRATION
```

## Purpose

Define a bounded design for passing a human-authored purpose reference through RePlay receipts without allowing purpose, repository identity, routing, or storage to become verification authority.

## Verified repository roles

| Repository | Bounded role | Explicit non-claim |
| --- | --- | --- |
| `jsonwisdom/COMPUTERWISDOM` | Corporate/operational doctrine root and proposed integration host | Not the canonical Anchor 001 proof source |
| `jsonwisdom/AL` | Receipt and proof machinery; compatibility target | Not a source-of-truth authority |
| `jsonwisdom/JOY` | Separate family-safe witness/context surface | Not a universal identity constant or routing authority |
| `jsonwisdom/layered-proofing-state-level-alms` | Existing ALMS-named repository requiring separate inspection | Not automatically injected or renamed |

Cross-repository relationships are digest-bound pointers. No repository is imported as a monorepo, mounted as a shared filesystem, or granted authority by this design.

## Proposed receipt extension

```json
{
  "purpose_ref": {
    "repository": "jsonwisdom/COMPUTERWISDOM",
    "path": "docs/PURPOSE.md",
    "commit_sha": "<40-hex Git commit>",
    "sha256": "<64-hex SHA-256 of exact file bytes>"
  },
  "joy_ref": {
    "repository": "jsonwisdom/JOY",
    "commit_sha": "<40-hex Git commit>",
    "artifact_path": "<explicit path>",
    "sha256": "<64-hex SHA-256 of exact artifact bytes>"
  },
  "al_compatibility": {
    "repository": "jsonwisdom/AL",
    "commit_sha": "<40-hex Git commit>",
    "test_command": "<exact command>",
    "result": "NOT_RUN"
  },
  "alms_ref": null,
  "authority_created": false
}
```

`purpose_ref.sha256` binds the exact canonical purpose artifact bytes. It must not hash an informal paraphrase. `joy_ref` is an optional contextual pointer, not the literal constant `JOY`. AL compatibility can be claimed only after a pinned AL commit and exact test command execute successfully.

## Routing boundary

Purpose may select an eligible fixture or validator profile. Purpose must not:

- change validation results;
- bypass required checks;
- select authority;
- elevate a claim;
- mutate evidence;
- enable publication.

The selected profile, selection rule version, and purpose digest must be recorded for deterministic replay.

## ALMS boundary

`ALMS` has no newly accepted expansion in MOVE-018. The existing ALMS-named repository must first be inspected and its role reconciled. Until a later human-reviewed artifact defines the interface:

```text
ALMS_EXPANSION_ACCEPTED = FALSE
ALMS_SERVICE_CREATED    = FALSE
ALMS_STORAGE_VERIFIED   = FALSE
ALMS_REF                = NULL
```

Indexing, retention, minimization, query, and deletion behavior are implementation claims requiring data-flow tests, storage inspection, log audits, and deletion tests.

## Proposed implementation sequence

1. Freeze exact purpose bytes and compute SHA-256.
2. Define a JSON Schema for the receipt extension.
3. Add synthetic fixtures only.
4. Implement parsing and digest binding without routing authority.
5. Pin AL by commit and add a compatibility adapter; do not execute another repository's unreviewed code implicitly.
6. Inspect and reconcile the existing ALMS repository before defining any ALMS interface.
7. Run unit, replay, negative, privacy, and cross-repository drift tests.
8. Produce a verification receipt for human review.

## How we will fail

MOVE-018 fails if a repository is called a truth authority; a floating branch replaces a commit pin; purpose changes verification outcomes; JOY is treated as identity or authority; AL tests are claimed without execution; ALMS is expanded without reconciliation; private or real youth data enters fixtures; non-storage is inferred from declarations; or any receipt reports `authority_created=true`.

## Amendment history

| Version | Change | State |
| --- | --- | --- |
| v0.1 | Corrected repository roles and bounded purpose, JOY, AL, and ALMS integration. | Design candidate |

