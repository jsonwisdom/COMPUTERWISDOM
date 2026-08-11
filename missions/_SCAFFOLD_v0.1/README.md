# COMPUTERWISDOM Mission Scaffold v0.1

Canonical directory contract for mission organization.

## Mission layout

```text
missions/<MISSION_ID>/
├── README.md
├── control/
│   ├── state/
│   └── handoffs/
├── sources/
├── corpus/
│   └── raw/
├── receipts/
├── manifests/
├── analysis/
├── schemas/
└── tests/
```

## Artifact boundaries

- `control/state/` — declared state checkpoints and gates.
- `control/handoffs/` — thread/session continuation artifacts such as `PINCER_NEXT_THREAD_HANDOFF.md`.
- `sources/` — source material or source references; source is not automatically evidence of a derived claim.
- `corpus/raw/` — admitted raw corpus bytes only after the mission's admission rules pass.
- `receipts/` — provenance, execution, failure, and verification receipts.
- `manifests/` — append-first inventories and content-addressed bindings.
- `analysis/` — derived interpretation; never relabeled as observation.
- `schemas/` — machine-readable contracts.
- `tests/` — synthetic and replay validation assets.

## Review state

Registry generation is discovery, not approval. Every generated branch-tip row begins as:

```text
MIGRATION_STATUS = PENDING_REVIEW
REVIEW_REQUIRED = TRUE
AUTHORITY_CREATED = FALSE
```

A reviewer may change a row to `REVIEWED` only after confirming its mission assignment, artifact class, source SHA, and canonical destination. `UNKNOWN` and ambiguous classifications remain review-required.

## Invariants

```text
SCAFFOLD != CORPUS
HANDOFF != SOURCE
HANDOFF != RECEIPT
HANDOFF != MANIFEST
COPY != AUTHORITY
PROVENANCE_RECEIPT != AUTHORITY_GRANT
DISCOVERY != CLASSIFICATION_CERTAINTY
BRANCH_NAME != MISSION_TRUTH
AUTHORITY_CREATED = FALSE unless separately evidenced
```

The migration workflow is intentionally absent from v0.1. Discovery, classification, indexing, validation, manual review, and directory creation must complete before any copy operation is eligible for later authorization.
