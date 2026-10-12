# GB-GARBAGE-LIBRARY-REJECT-ROW-LOGIC-2026-10-01

STATUS = LOCKED ROW-INTEGRITY MECHANICS
AUTHORITY_CREATED = FALSE

## Definition
receipt_status = REJECT

REJECT is an audit failure.
REJECT != LOW_SCORE
REJECT != PENALTY
REJECT != AUDIENCE_DISLIKE

A finished REJECT MUST carry one primary reason code.
No primary code => incomplete verdict; treat as HOLD until coded.

## Primary reason codes
1. REJECT_IDENTITY_COLLISION
2. REJECT_FABRICATED_METRICS
3. REJECT_RECEIPT_UNREPLAYABLE
4. REJECT_CONTAMINATED_WINDOW
5. REJECT_MODEL_INCOHERENT
6. REJECT_AUTHORITY_LAUNDER

Secondary codes may attach.

## Priority
Apply the first sufficient primary code in this order:
IDENTITY_COLLISION
FABRICATED_METRICS
RECEIPT_UNREPLAYABLE
CONTAMINATED_WINDOW
MODEL_INCOHERENT
AUTHORITY_LAUNDER

## Code triggers

### REJECT_IDENTITY_COLLISION
- reused or missing card_id after bind;
- blank character / format / hook_type while offered to a cell;
- silent rekey of an existing PASS id;
- duplicate live rows for one post without documented split.

### REJECT_FABRICATED_METRICS
- row value absent from bound receipt;
- row value differs from receipt beyond documented rounding;
- blank replaced with 0 to force S_v;
- S_v typed by hand instead of computed from locked weights;
- metrics altered in place after bind.

### REJECT_RECEIPT_UNREPLAYABLE
- row offered as estimable with no replayable source_receipt;
- missing/overwritten target;
- hash absent where required or hash mismatch;
- receipt refers to another video/account/date/window.

### REJECT_CONTAMINATED_WINDOW
- account-level totals written as video-level;
- wrong time window;
- another card's analytics pasted into the row;
- traffic class required by MODEL_VERSION is unlabeled or mixed.

### REJECT_MODEL_INCOHERENT
- raw counts placed in rate fields or vice versa against MODEL_VERSION;
- wrong S_v weights for the claimed version;
- penalty manipulated to force clipping;
- incompatible metric windows;
- mixed model versions within one row.

### REJECT_AUTHORITY_LAUNDER
- TikTok private weight / FYP score / algorithm rank represented as observed input;
- theta_hat or B written as raw card metric;
- "algorithm learned" / "proven winner" used to justify PASS;
- parent hyperparameters inserted into a card row to unblock execution.

If the raw metrics receipt is valid but a separate claim launders authority, preserve the metrics row and reject the claim object separately.

## Print contract
card_id
receipt_status = REJECT
primary_code
secondary_codes[]
bound_hash_or_pointer
detected_at
was_ever_pass
n_replay_required = true|false

was_ever_pass = true => n_replay_required = true

## Estimator effect
REJECT rows:
- do not increment n;
- do not update mean(S), mu_t, tau^2, or sigma^2;
- do not produce carry-forward theta_hat.

If a prior PASS becomes REJECT:
decrement n and replay any dependent aggregates and theta_hat.

Keep the rejected row/tombstone. Do not silently delete it.

## Transitions
HOLD -> REJECT when audit fails.
PASS -> REJECT when a bound receipt breaks or metrics are altered.
REJECT -> PASS requires a NEW card_id and NEW receipt after fabrication/contradiction.
REJECT -> HOLD only when the issue was prematurity rather than contradiction.

REJECT-only table => estimator counts absent.
