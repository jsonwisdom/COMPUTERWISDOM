# TRIGGER_EVALUATION_V0_1 — Execution Semantics

## State Machine

| Input Condition | Output State | Level Change |
|---|---|---|
| Malformed input | MAINTAIN | No |
| Unauthorized source domain | MAINTAIN | No |
| Authorized, trigger matched, no receipt | OBSERVE | No |
| Authorized, trigger matched, receipt verified | TRANSITION_READY | Recommended |
| Authorized, trigger not matched | OBSERVE (log) | No |

## Invariants

1. No silent mutation. State changes only via verified trigger.
2. Authority remains false. The engine recommends; a human or hybrid system authorizes.
3. Receipt supremacy. A verified receipt is necessary and sufficient for TRANSITION_READY.
4. Replay determinism. Same inputs produce same outputs.

## Verification Method Tiers (v0.2 candidate)

- cryptographic
- source_authenticity
- human_review
- independent_verification

## Test Vectors

- examples/trigger_evaluation_v0_1.valid_transition.json
- examples/trigger_evaluation_v0_1.observe_only.json
- examples/trigger_evaluation_v0_1.maintain_unauthorized_source.json
