# Automated Forest Convergence Execution Spec V1

## Purpose
Deterministic, receipt-triggered execution of full Merkle Forest replay + convergence checks across all groves. Produces only receipts and logs. No direct state mutation.

## Trigger Rule
Convergence only begins after a valid CONVERGENCE_TRIGGER_RECEIPT is appended to the vault.

## Core Guarantees
- Linear vault replay first
- Per-grove tree validation
- Bridge application
- Convergence only on zero critical integrity errors
- All outputs are receipts or PUBLIC_INDEX mirror updates

## Automation Boundary
Automation has no authority to canonize, merge, supersede, or silently mutate forest state.

Automation may only:
- replay
- validate
- detect contradictions
- produce deterministic logs
- append convergence result receipts
- derive mirror state

## Halt Conditions
The execution MUST halt if:
- dangling references exist
- previous_vault_merkle_root mismatches
- invalid state transitions exist
- unresolved critical contradictions remain
- replay_status = HALTED

## Mirror Rule
PUBLIC_INDEX remains derived mirror state only.
It never acts as proof.

## Final Line
Convergence is not declared by authority. It is observed when replay completes without critical integrity failure.
