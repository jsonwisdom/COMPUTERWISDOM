# ZORA FLYWHEEL — OBJECT AUDIT SCHEMA V0.1

MODE = APPEND_ONLY
BUILD_AUTHORITY = STANDING
HUMAN_SIGNING_GATE = TERMINAL_ONLY

Every tracked object gets a stable object id and an append-only audit trail.

Required fields:

- object_id
- object_type
- source
- observed_at
- state
- evidence_refs
- classification
- confidence
- contradictions
- holds
- parent_refs
- supersedes
- signer_required
- terminal_action_required

Core laws:

MISSING != ZERO
HOLD != FALSE
OBSERVED != VERIFIED
VERIFIED != PROMOTED
WALLET != HUMAN
SIGNER != HUMAN_IDENTITY
CONNECTOR_ACCESS != WALLET_CONTROL
TRADE_INTENT != EXECUTED_TRADE
REPUTATION_SCORE != EXTERNAL_REPUTATION
KNOWLEDGE_SCORE != TRUTH

Audit is append-only. Corrections append successor records; prior records remain addressable.
