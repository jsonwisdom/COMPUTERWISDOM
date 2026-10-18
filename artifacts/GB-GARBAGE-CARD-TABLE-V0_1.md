# GB-GARBAGE-CARD-TABLE-V0_1

STATUS = EMPTY EXECUTABLE TABLE
AUTHORITY_CREATED = FALSE
ROW_COUNT = 0

## Row schema
card_id
case_id
character
format
hook_type
prop_type
video_length
posted_at
views
retention
completion
shares
saves
comments
follows
search_rate
penalty
S_v
n_cell
source_receipt
receipt_status

## Receipt states
HOLD = incomplete evidence; estimator invisible.
PASS = complete metrics + replayable source_receipt.
REJECT = audit failure with reason code; estimator invisible.

## PASS law
PASS is a row-level audit state, not a performance trophy.
A flop with complete metrics and a valid receipt can PASS.
A banger with incomplete or unauditable evidence cannot PASS.

S_v = 0.35R + 0.20C + 0.15Sh + 0.10Sv + 0.10Cm + 0.05F + 0.05Q - P
Clip after penalty to [0,1].
Raw interaction counts must be converted to per-view rates exactly once under the active MODEL_VERSION.

n_cell = count of PASS rows only in (character, format, hook_type) after insert.

## Estimator gate
HOLD does not increment n.
REJECT does not increment n.
Only PASS rows update n_cell and cell aggregates.

NO PARENT -> NO SHRINKAGE.
NO COUNTS -> NO PRECISION.
NO PRECISION -> NO B.
