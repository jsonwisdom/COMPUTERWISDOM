# GB-GARBAGE-LIBRARY-HOLD-ROW-LOGIC-2026-10-01

STATUS = LOCKED ROW-STATE MECHANICS
AUTHORITY_CREATED = FALSE

## Definition
receipt_status = HOLD

HOLD is an incomplete-evidence state.
HOLD != LOW_SCORE
HOLD != PENALTY
HOLD != JOKE_FAILURE

A HOLD row may identify the object while lacking one or more inputs required for S_v or lacking a replayable source_receipt.

## Allowed present fields
card_id
case_id
character
format
hook_type
prop_type
video_length
posted_at
source_receipt = pending | partial
some raw metrics = present
some raw metrics = blank

BLANK != ZERO
MISSING != ZERO
Writing 0 to replace an unknown value in order to compute S_v is not HOLD completion; it is an audit failure.

## Subtypes
HOLD-METRICS
Receipt exists, but one or more current MODEL_VERSION inputs are missing, immature, or incomplete.

HOLD-RECEIPT
Some metrics exist, but source_receipt is missing, unlinkable, partial, or not replayable.

Subtypes are labels only. Both remain receipt_status = HOLD.

## Estimator exclusions
On HOLD:
- do not compute carry-forward S_v for shrinkage;
- do not increment n_cell or n_kfh;
- do not update mean(S), mu_t, tau^2, or sigma^2;
- do not draw Thompson samples from the row;
- do not PROMOTE or RETIRE from the row.

HOLD is visible in the table and invisible to the estimator.

## Promotion
HOLD -> PASS only when:
1. every S_v input required by MODEL_VERSION is present;
2. source_receipt resolves to a replayable object;
3. raw-count vs rate semantics match MODEL_VERSION;
4. n_cell is recomputed from PASS rows only after the transition.

HOLD -> REJECT when audit fails.
HOLD -> HOLD when evidence remains incomplete.

Thin views alone do not force HOLD. A complete valid receipt with a small view count may PASS and later carry EVIDENCE_THIN.

## Gate
HOLD != PASS_CARD_ROW
HOLD != VERSIONED_PARENT_OBJECT
HOLD-only table => estimator counts absent
