# COMPUTERWISDOM — Ten-Case Audit Receipt v1.1

**Status:** HOLD  
**Date:** 2026-10-25  
**Scope:** Controlled local fixture evaluation only  
**Meaning of any future signature:** Receipt acknowledged. Not production authorized. Not deployment. Not trading. Not agent activation.

## Registry (unchanged)
- Path: `agents/registry.json`
- Blob SHA: `7ba84bb2560c18d6a5225c077c70cf5b9bf825c7`
- Observed at commit: `626e10362581559cbbd1fb36ac1072947fccaf14`
- All five agents: `authority: false`
- Issue #310: `agents_activated: false`, `implementation_committed: false`, `authority: false`

## Coinbase MCP adapter
- Path: `projects/cwaas/adapters/coinbase_mcp_adapter_v1.sh`
- Status: `DRY_RUN_ONLY`
- Does not move funds. Does not perform chain actions.

## Fixture hashes (re-verified this session)
- original.txt: `81087ef3debc0c2c82832588f06208ac20c09bbe061380af769331116e566565`
- tampered.txt: `719b4f2d5807076416f85d0a994cf47026bd308d3e4ab3ade774a709cf065a39`

## Case results (local controlled scope)

| Case | What was executed this session | Two-run | Result | Limitation |
|------|--------------------------------|---------|--------|------------|
| 01 Repository routing | Navigator skill stub (`/tmp/navigator_stub.py`) | Identical | LOCAL CANDIDATE | No live Navigator existed. Contract equivalence only. |
| 02 Custody capture | Fixture created and hashed | Hashes stable | LOCAL CANDIDATE (fixture) | No separate Custody tool harness executed in this session beyond fixture. |
| 03 Replay / tamper | Reported by operator | Reported identical | LOCAL CANDIDATE (reported) | Not re-executed as a named harness in this session. |
| 04 Missing evidence | `/tmp/case04_harness.py` | IDENTICAL | LOCAL PASS | Fail-closed on missing/empty evidence. |
| 05 CI / No Fake Green | `/tmp/case05_harness.py` | IDENTICAL | LOCAL PASS | green only when verification + evidence complete. |
| 06 PR no review | `/tmp/case06_harness.py` | IDENTICAL | LOCAL PASS | no approving review → BLOCKED. |
| 07 Manifest update | `/tmp/case07_harness.py` | IDENTICAL | LOCAL PASS | history preserved; orphan rejected. |
| 08 Wallet preview | `/tmp/case08_harness.py` | IDENTICAL | LOCAL PASS | signed=false, funds_moved=false, chain_action=false. |
| 09/10 Wallet approval | `/tmp/case10_harness.py` | IDENTICAL | LOCAL PASS | ELIGIBLE_ONLY ≠ EXECUTED. Agent-generated rejected. Test fixture only. |
| 10 Cross-agent replay | `/tmp/case10_replay_harness.py` | IDENTICAL | LOCAL PASS | All local candidates agreed on final SHA + lineage. |

## What was not claimed
- Operational equivalence with any live agent.
- Production migration authorization.
- Wallet control proof.
- Human identity binding.
- ENS ownership proof.
- Authority grant.

## Migration recommendation (evidence only — not authorized)
- Navigator → FOLD INTO SKILL (candidate)
- Custody → TURN INTO TOOL (candidate)
- Replay → TURN INTO TOOL (candidate)
- CI Gate → TURN INTO TOOL (candidate)
- Clerk → FOLD INTO SKILL (candidate)

None of the above are authorized for production migration.

## Final boundaries
- Registry: UNCHANGED
- Authority: FALSE
- Wallet execution: BLOCKED
- Agent activation: NONE
- Production migration: NOT AUTHORIZED
- Release: HOLD

Signature on this receipt, if later performed, means acknowledgment of the above text only.
