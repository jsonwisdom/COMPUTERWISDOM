# Supreme Seymour Recursive Learning Flywheel — Operator Contract V0.1

## Purpose

Run a read-only daily comparison across Jay's public GitHub estate and emit only the observed head-level deltas.

The runner is not the operator.

`FINAL_DECISION = JASON`

## Flow

`GITHUB ESTATE → BASELINE → DELTA → ARTIFACT → DRIVE CHECKPOINT → GMAIL LINK → JASON`

The workflow implements only the GitHub portion today:

`GITHUB ESTATE → BASELINE → DELTA → ARTIFACT`

Drive and Gmail remain separate authenticated delivery rails.

## What runs

- enumerates public repositories owned by `jsonwisdom`;
- resolves each default-branch head where possible;
- compares it to `MASTER_ROOM/SNAPSHOT_INDEX_V1.json`;
- emits VERSION_DELTA / STRUCTURE_DELTA / ABSENCE_CLAIM_DELTA;
- records unresolved heads as UNKNOWN;
- uploads JSON + Markdown artifacts.

## What does not run

- no repository mutation;
- no purpose inference;
- no role promotion;
- no merge;
- no Drive write;
- no Gmail send;
- no cross-repo write;
- no authority creation.

## Operator delivery law

Jason should receive **email only** for:

- instructions;
- updates;
- manuals.

Those emails should point to a Google Drive object containing the durable human-facing artifact.

GitHub Actions artifacts are machine/runtime receipts, not the final operator surface.

## Current ceiling

`PROMOTION_BLOCK = INTERFACE_ONLY`

`STORE_GATE = NOT_PRESENT`

`CROSS_REPO_WRITE_PATH = NOT_PRESENT`

`GMAIL_FROM_ACTIONS = NOT_CONFIGURED`

## Existing runner patterns reused

- JOY Family Daily Audit: exact checkout, read-only audit, artifact upload.
- JOY Trigger Hunter: scheduled observation and artifact output.
- Master Room: delta-first / no fake green / Jason final gate.

## Next seam

Bind the artifact handoff:

`workflow artifact → Drive checkpoint/manual → Gmail delivery to Jason`

without putting Gmail credentials into the GitHub workflow.
