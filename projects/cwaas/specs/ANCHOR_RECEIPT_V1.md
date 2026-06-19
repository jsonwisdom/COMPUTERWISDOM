# ANCHOR_RECEIPT_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Base Anchor Receipts  
Depends on:
- RECEIPT_SCHEMA_V1
- REPLAY_TRACE_FORMAT_V1
- BASE_ATTESTATION_FLOW_V1
- EAS_BASE_PAYLOAD_0001_EVENT_001.json

## 1. Purpose

ANCHOR_RECEIPT_V1 defines how CWaaS records the act of anchoring a replay-verified event to Base/EAS.

The Base/EAS attestation is not the receipt itself.

The receipt records:

- what was anchored
- where it was anchored
- which payload was submitted
- which transaction or attestation UID resulted
- whether the anchor can be replay-verified

## 2. Core Rule

```text
No anchor receipt, no anchor green.
No transaction witness, no final settlement.
No EAS UID, no attestation claim.
No replay trace, no authority.
```

## 3. Required Fields

```yaml
anchor_receipt_version: ANCHOR_RECEIPT_V1
anchor_receipt_id: ANCHOR_0001_EVENT_001

source_event:
  receipt_id: EVENT_001
  receipt_hash: <sha256>
  replay_trace_id: TRACE_0001
  replay_trace_hash: <sha256>

payload:
  payload_id: EAS_BASE_PAYLOAD_0001_EVENT_001
  payload_path: projects/cwaas/attestations/EAS_BASE_PAYLOAD_0001_EVENT_001.json
  payload_hash: <sha256>

anchor_target:
  chain: Base
  protocol: EAS
  network: <mainnet|sepolia>
  schema_uid: <eas_schema_uid>
  recipient: <wallet_or_basename>

anchor_result:
  status: PENDING|SUBMITTED|CONFIRMED|FAILED|REJECTED
  transaction_hash: <tx_hash|null>
  attestation_uid: <eas_uid|null>
  block_number: <block_number|null>
  timestamp_utc: <iso8601>

provenance:
  github_repo: jsonwisdom/COMPUTERWISDOM
  github_branch: cwaas-receipt-schema-v1
  github_commit: <commit_sha>
  operator: <github_user_or_agent>
```

## 4. Anchor States

Allowed states:

```text
PENDING
SUBMITTED
CONFIRMED
FAILED
REJECTED
```

Meanings:

- PENDING: payload exists but has not been submitted
- SUBMITTED: transaction or attestation request was broadcast
- CONFIRMED: transaction and attestation UID are verified
- FAILED: submission failed or reverted
- REJECTED: anchor attempt violated policy or schema

## 5. Settlement Rule

An anchor may only be marked settled when:

```text
anchor_result.status = CONFIRMED
transaction_hash != null
attestation_uid != null
payload_hash matches current payload
receipt_hash matches source receipt
replay_trace_hash matches source trace
```

If any required value is missing or mismatched:

```text
anchor_result.status != CONFIRMED
settlement = BLOCKED
```

## 6. Prohibited Claims

An anchor receipt may not claim:

```text
Coinbase endorsement
Base endorsement
GitHub endorsement
legal approval
financial advice
funds moved
trade executed
```

unless a separate replayable receipt proves that claim.

## 7. Replay Requirements

A valid anchor replay must verify:

```yaml
checks:
  source_receipt_hash_valid: true
  replay_trace_hash_valid: true
  payload_hash_valid: true
  github_commit_valid: true
  transaction_hash_valid: true
  attestation_uid_valid: true
  prohibited_claims_absent: true
```

No null critical check may produce green.

## 8. Example Pending Anchor

```yaml
anchor_receipt_version: ANCHOR_RECEIPT_V1
anchor_receipt_id: ANCHOR_0001_EVENT_001

source_event:
  receipt_id: EVENT_001
  receipt_hash: feff0b8f2734e0a62f4b0b73b9cf08c94ba64214d9b94b891eeba656cd4bf3f8
  replay_trace_id: TRACE_0001
  replay_trace_hash: 578742202f9ffff6be6a41e45ef388e063a02cb4c37096af3b7cd6b5f10ff9f0

payload:
  payload_id: EAS_BASE_PAYLOAD_0001_EVENT_001
  payload_path: projects/cwaas/attestations/EAS_BASE_PAYLOAD_0001_EVENT_001.json
  payload_hash: ae65ca50fb9c058ac74eba037a29e79df14937b3d94da18118ab2a90bdcd1b78

anchor_target:
  chain: Base
  protocol: EAS
  network: sepolia
  schema_uid: <eas_schema_uid>
  recipient: jaywisdom.base.eth

anchor_result:
  status: PENDING
  transaction_hash: null
  attestation_uid: null
  block_number: null
  timestamp_utc: <iso8601>
```

## 9. Boss Brenda Lock

```text
No anchor receipt, no anchor green.
No transaction witness, no confirmed anchor.
No EAS UID, no attestation claim.
No replay, no settlement.
No endorsement by implication.
No fake green.
```
