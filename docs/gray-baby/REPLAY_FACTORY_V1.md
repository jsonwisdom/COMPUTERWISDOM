# Gray Baby Replay Factory V1

**Product:** `GRAY_BABY_BULK_REPLAY_V1`  
**Factory:** `GRAY_BABY_REPLAY_FACTORY_V1`  
**Role:** batch replay orchestrator  
**Authority created:** false  
**Default access:** read only

This factory composes the existing replay kernel, replay-receipt spec, and Gray Baby gap-observer docs into one batch orchestrator. It does not open a second authority surface.

## Invariant

```text
MANY_OPERATORS_AVAILABLE != MANY_OPERATORS_REQUIRED
CHEAP_PASS_FIRST
DEEP_PASS_ON_EXCEPTION
ONE RECEIPT = ONE BOUNDARY
CORRECTION becomes NEW RULE
NEW RULE triggers REPLAY OLD POPULATION
```

Operator count follows uncertainty on the object. An idle batch is valid. A full pool is not a reason to run every operator.

The cheap lane for every object is `OBJECT_SELECTOR`, `TEMPORAL_GUARD`, `CHAIN_BINDER`, `RECEIPT_COMPARATOR`, and `DELTA_CLASSIFIER`. Decoders, binders, and sentinels are added only when the object carries the matching gap. An object that still matches no known state after two passes is routed to `ALIEN_ROUTER` and deep replay.

## Membranes

```text
SOURCE_ORDER = RAW_CHAIN > REPO_RECEIPTS > DRIVE_HISTORY > PUBLIC_INDEXES > PAGE_LABELS
```

A stronger receipt may be recorded as a new receipt (`UPGRADED`, `CORRECTED`, `DEMOTED`). The prior hash stays on that receipt.

A search miss cannot delete an object. A weaker source cannot override a stronger one. A wallet reference cannot become a human identity. An older snapshot cannot falsify a later object. Missing chain, RPC, account-abstraction, or Drive bytes stay `MISSING_RECEIPT` or `HOLD`. They are not filled in.

HOLD is not promoted here. Promotion out of HOLD is outside this factory.

## What this run proves

A batch receipt is a `REPLAY_RECEIPT_SPEC_V1` envelope: spec, receipt id, identity reference, action reference, source artifacts, replay parameters, and output. Identity references are roles or object ids. `authority` is false and `authority_boundary` is `NONE`, matching replay kernel V0.1.

Hashes use the kernel's canonical JSON and `sha256:` prefix. `replay()` itself is not called on inventory rows, because those rows are not `ERS_V0_1` artifacts. The kernel's rejection rules (authority must be false, boundary `NONE`) still describe this factory's receipts.

The scoreboard stores counts and ratios only. It does not emit a quality score.

## Fixture

The design default is batch size 32 over a 1,024-object inventory (32 batches). This repo does not contain that inventory. `fixtures/gray_baby/synthetic_inventory_v1.json` is a small synthetic fixture for tests and for the manual workflow. Its chain fields are not real chain data.

## Workflow

`.github/workflows/gray-baby-bulk-replay-v1.yml` is `workflow_dispatch` only, with `contents: read`. It checks out the repo, builds one batch, replays it, validates membranes, classifies deltas, writes receipts, and builds a scoreboard. Receipts are uploaded as an artifact. The job does not commit them and does not read secrets.

If `expected_sha` is provided, the job fails when `GITHUB_SHA` or `HEAD` differs. That is the Gray Baby platform rule for exact SHA validation. An empty `expected_sha` means the run is not SHA-pinned; the receipt still binds the inventory by content hash.
