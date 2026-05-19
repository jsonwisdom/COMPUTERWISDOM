# Automated Replay Convergence Pseudocode V1

1. On receipt of valid CONVERGENCE_TRIGGER_RECEIPT:
   - Verify previous_merkle_root
   - Run full Forest Replay Validator on current vault

2. If validator.replay_status == "HALTED" or integrity_errors contains critical failures:
   - Append CONVERGENCE_RESULT_RECEIPT with status=HELD
   - Log all errors
   - Halt

3. If COMPLETE:
   - For each grove in scope:
     - Identify latest receipted TREE_ROOT per path
     - Apply all relevant bridges
     - Check for dangling references
   - Collect converged_paths
   - Collect non_converged_paths with reasons
   - Append CONVERGENCE_RESULT_RECEIPT
   - Optionally append PUBLIC_INDEX mirror update (mirror only)

4. All steps logged with deterministic replay_log_entry_hash

## Hard Rules
- No direct state mutation
- No auto-canonization
- No hidden orchestration
- No authority granted to automation
- Replay must remain reproducible from genesis

## Halt Conditions
- integrity error
- dangling reference
- unresolved critical contradiction
- invalid previous_vault_merkle_root
- invalid state transition

## Final Line
A validator does not decide truth by authority. It replays receipts until the forest either converges or halts.
