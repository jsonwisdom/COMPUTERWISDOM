# Validator Membrane Spec V1

## Purpose
Define the strict operational boundary that keeps the Merkle Forest lawful. The validator is a pure replay machine.

## Allowed Behaviors
- Validates receipt chains and merkle links
- Replays vault receipts in strict append order
- Detects contradictions, dangling references, and integrity errors
- Logs every step with deterministic replay_log_entry_hash
- Halts on any violation (dangling reference, root mismatch, invalid transition, etc.)

## Forbidden Behaviors
- Declares truth by itself (no implicit CANON without explicit receipt)
- Overrides or modifies existing receipts
- Mutates canon silently (all changes via visible supersedes/bridge receipts)
- Bypasses replay (no shortcuts, no cached final states treated as authoritative)
- Treats PUBLIC_INDEX, Zora, or Base as proof

## Enforcement
These rules are checked as part of every Forest Replay Validator run.

Violation of membrane rules produces:

```text
INTEGRITY_ERROR_MEMBRANE_VIOLATION
```

and forces HALTED state.

## Status Attachment
Membrane compliance status attaches only to specific validator execution receipts.

## Constraint Rule
The membrane is a constraint set, not an agent.
It grants no authority outside replay validation.

## Final Line
This distinction is the membrane keeping the whole forest lawful.
