# HELP JAY'S BITS GET BETTER — APPEND-ONLY TASK LEDGER

MODE = APPEND_ONLY
PROJECT = ZORA_FLYWHEEL
BUILD_AUTHORITY = STANDING
GENERIC_AUTHORITY_PROMPTS = DISABLED
HUMAN_SIGNING_GATE = TERMINAL_ONLY

## TASK-001 — Inventory wallet objects

Status: ACTIVE

Inputs:
- Zora smart wallet 01
- Coinbase / Base wallet surfaces
- signer relationships
- ENS / BNS pointers

Output:
- typed wallet-object inventory
- unresolved joins remain HOLD

## TASK-002 — Audit objects

Status: ACTIVE

For every object:
- verify source
- classify type
- attach receipts
- record contradictions
- preserve unresolved fields
- never collapse wallet, signer, ENS, BNS, or human identity

## TASK-003 — Refresh knowledge

Status: ACTIVE

Collect new evidence from:
- wallet state
- on-chain activity
- connector observations
- transaction receipts
- creator rewards
- token metadata

Output:
- append-only observations
- replayable deltas
- no silent overwrites

## TASK-004 — Prepare swap intent

Status: WAITING_FOR_TRADE_PARAMETERS

Required before quote / execution:
- source wallet
- chain
- token_in
- token_out
- amount_in or amount_out
- slippage bound
- quote timestamp
- route
- fees
- expected minimum received

Build may prepare and audit the swap object without asking for authority.

Execution rule:

QUOTE != TRADE
TRADE_INTENT != SIGNED_TRANSACTION
SIGNED_TRANSACTION != CONFIRMED_SWAP

The human signing gate is reached only after the exact swap preimage / transaction payload is complete.

## TASK-005 — Knowledge / intelligence growth

Status: ACTIVE

Increase quality by:
- more verified receipts
- more reproducible replays
- fewer unresolved contradictions
- better source diversity
- successful prediction/calibration checks
- explicit error corrections

No score may rise because a claim is repeated.

## TASK-006 — Reputation toward Wisdom

Status: ACTIVE_INTERNAL_METRIC_ONLY

Reputation here means internal evidence-backed reliability, not an external platform reputation or social-credit score.

Positive inputs:
- verified receipts
- accurate replays
- corrected mistakes
- source transparency
- successful audits
- clear uncertainty
- safe terminal signing

Negative inputs:
- unresolved contradiction
- unsupported promotion
- duplicate evidence counted as independent
- missing provenance
- failed replay
- false certainty

WISDOM requires both knowledge and restraint.
