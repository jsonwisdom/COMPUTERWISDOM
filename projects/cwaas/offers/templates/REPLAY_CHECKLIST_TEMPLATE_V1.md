# REPLAY_CHECKLIST_TEMPLATE_V1.md

**Receipt-First Agent Workflow Audit — Replay Checklist Template**

## Header

```text
receipt_id:
replay_trace_id:
auditor: jaywisdom.base.eth
status: REPLAY_CHECK_PENDING
no_fake_green: true
```

## Required Checks

```text
schema_valid:
hash_valid:
previous_hash_lineage_intact:
receipt_paths_identified:
human_approval_present:
failure_states_present:
rollback_path_present:
adapter_boundary_clear:
authority_boundary_clear:
payment_boundary_clear:
unauthorized_execution_absent:
fake_green_claims_absent:
```

## Replay Questions

1. Can another operator reproduce the workflow result?
2. Are all inputs visible?
3. Are all outputs bound to receipts?
4. Is there a hash, commit, log, or witness for each claim?
5. Does the workflow fail closed when evidence is missing?
6. Does the workflow avoid payment, settlement, production, or approval claims without proof?

## Replay Result

```text
verdict: PASS | FAIL | DRIFT | PARTIAL
disposition: REVIEW_GREEN | BLOCKED | QUARANTINED
blocked_reason:
next_required_receipt:
no_fake_green: true
```

## Boss Bre Lock

```text
No replay, no settlement.
No deterministic verdict, no green.
No fake green.
```

## Boundary

Replayability is not authority. This checklist does not prove payment, custody, settlement, legal status, or external endorsement.
