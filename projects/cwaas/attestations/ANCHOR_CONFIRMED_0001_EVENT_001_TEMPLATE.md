# ANCHOR_CONFIRMED_0001_EVENT_001_TEMPLATE

Status: TEMPLATE_ONLY  
Lane: CWaaS / Base Attestation / Anchor Receipt  
Depends on:
- RECEIPT_SCHEMA_V1
- REPLAY_TRACE_FORMAT_V1
- BASE_ATTESTATION_FLOW_V1
- ANCHOR_RECEIPT_V1
- EAS_BASE_PAYLOAD_0001_EVENT_001.json
- ANCHOR_0001_EVENT_001_PENDING.md

## 1. Purpose

This document is the confirmed-anchor receipt template for EVENT_001.

It must only be completed after a real Base/EAS submission exists and the resulting transaction hash and EAS attestation UID are known.

Until those fields are filled with real evidence, this document is not a confirmed anchor.

## 2. Anchor State

```text
anchor_state: CONFIRMED_TEMPLATE
execution_claim: NONE
financial_claim: NONE
endorsement_claim: NONE
```

## 3. Required Confirmation Evidence

```yaml
anchor_receipt_version: ANCHOR_RECEIPT_V1
anchor_id: ANCHOR_0001
source_event_id: EVENT_001
source_trace_id: TRACE_0001
source_payload_id: EAS_BASE_PAYLOAD_0001_EVENT_001

base_network: Base Mainnet | Base Sepolia
transaction_hash: <real_base_transaction_hash_required>
eas_attestation_uid: <real_eas_uid_required>
attester_address: <real_attester_address_required>
recipient_address: <real_recipient_address_required>
block_number: <real_block_number_required>
block_timestamp_utc: <real_block_timestamp_required>

github_branch: cwaas-receipt-schema-v1
github_commit_after_anchor: <commit_sha_required>

receipt_hash: <sha256_required>
trace_hash: <sha256_required>
payload_hash: <sha256_required>
anchor_receipt_hash: <sha256_required>

verdict: PASS | FAIL | DRIFT | BLOCKED | REJECTED
disposition: SETTLED | QUARANTINED | NEEDS_REVIEW | REJECTED | BLOCKED
```

## 4. Confirmation Rule

The anchor may only be marked confirmed when all of the following are present:

```text
real Base transaction hash
real EAS attestation UID
real attester address
real recipient address
real block number
real block timestamp
matching payload hash
matching replay trace hash
```

If any field is missing, placeholder, unverifiable, or inconsistent:

```text
anchor_state = PENDING_OR_INVALID
verdict != PASS
```

## 5. Non-Endorsement Rule

A confirmed anchor proves only that a payload was anchored.

It does not prove:

```text
Coinbase endorsement
Base endorsement
GitHub endorsement
legal approval
financial advice
fund movement
trade execution
```

unless those claims are separately receipted and replayed.

## 6. Replay Rule

A confirmed anchor must replay back to:

```text
EVENT_001 receipt
TRACE_0001 replay trace
BASE_ATTESTATION_0001 pointer
EAS_BASE_PAYLOAD_0001 JSON
HASH_RECEIPT_0001
ANCHOR_0001 pending receipt
```

Any mismatch creates:

```text
verdict: DRIFT
failure_class: ANCHOR_LINEAGE_MISMATCH
```

## 7. Boss Brenda Lock

```text
No real tx hash, no confirmed anchor.
No EAS UID, no attestation claim.
No matching payload hash, no settlement.
No replay, no green.
No endorsement by implication.
No fake green.
```
