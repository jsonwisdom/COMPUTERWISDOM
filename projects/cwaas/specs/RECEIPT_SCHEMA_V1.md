# RECEIPT_SCHEMA_V1

**Status:** v1 draft  
**Lane:** CWaaS / COMPUTERWISDOM as a Service  
**Role:** Foundational root of authority  
**Doctrine:** No schema, no green.

---

## 1. Purpose

`RECEIPT_SCHEMA_V1` defines the minimum admissible structure for a CWaaS receipt.

CWaaS does not accept narrative authority by default. A claim, agent action, treasury event, governance decision, or replay result becomes admissible only when it is represented as a structured receipt that can be hashed, replayed, challenged, and independently reviewed.

This schema is the root primitive for:

- Treasury Gate v0.2
- Replay Trace Format v1
- Agent Action Receipt v1
- Base Attestation Flow v1
- Coinbase-enabled treasury verification
- GitHub provenance review

---

## 2. Core Rule

```text
No Receipt = No Authority
No Schema = No Green
No Hash = No Replay
No Human Approval = No Treasury Execution
```

A receipt is not a story. A receipt is a falsifiable record.

---

## 3. Receipt Lifecycle

```text
ACTION
  ↓
RECEIPT
  ↓
CANONICALIZATION
  ↓
HASH
  ↓
REPLAY
  ↓
VERDICT
```

A CWaaS receipt must survive this lifecycle without relying on private interpretation.

---

## 4. Required Fields

Every `RECEIPT_SCHEMA_V1` object MUST include the following fields.

```yaml
schema_version: RECEIPT_SCHEMA_V1
receipt_id: string
timestamp_utc: ISO-8601 string
system: string
lane: string
action_type: string
actor: string
subject: string
execution_mode: string
human_approval: string
inputs_hash: sha256 string
outputs_hash: sha256 string | NONE
previous_receipt_hash: sha256 string | GENESIS
receipt_hash: sha256 string
replay_status: PASS | FAIL | DRIFT | BLOCKED | NOT_REPLAYED
verdict: ADMISSIBLE | REJECTED | PROVISIONAL | QUARANTINED
witnesses: list
notes: string
```

---

## 5. Field Definitions

### `schema_version`

Fixed value:

```text
RECEIPT_SCHEMA_V1
```

### `receipt_id`

Unique receipt identifier.

Recommended format:

```text
CWaaS-YYYYMMDD-NNNN
```

Example:

```text
CWaaS-20260619-0001
```

### `timestamp_utc`

UTC timestamp when the receipt was created.

Example:

```text
2026-06-19T00:00:00Z
```

### `system`

The system emitting the receipt.

Examples:

```text
COMPUTERWISDOM
AL
Coinbase
Base
GitHub
```

### `lane`

The operational lane.

Examples:

```text
cwaas
treasury
replay
agent-governance
base-attestation
github-provenance
```

### `action_type`

The kind of event being recorded.

Examples:

```text
BALANCE_INSPECTION
ORDER_PREVIEW
ORDER_EXECUTION_REQUEST
AGENT_ACTION
REPLAY_VERIFICATION
BASE_ATTESTATION
GITHUB_COMMIT
```

### `actor`

The human, agent, service, wallet, or repository initiating the action.

Examples:

```text
jaywisdom
COMPUTERWISDOM-AGENT-01
jsonwisdom/COMPUTERWISDOM
```

### `subject`

The object acted upon.

Examples:

```text
Coinbase portfolio snapshot
Base attestation UID
GitHub commit
Agent action bundle
```

### `execution_mode`

Allowed values:

```text
READ_ONLY
PREVIEW_ONLY
HUMAN_APPROVED
EXECUTED
BLOCKED
```

### `human_approval`

Allowed values:

```text
REQUIRED
GRANTED
DENIED
NOT_REQUIRED_READ_ONLY
```

Treasury actions that move assets MUST NOT be green unless `human_approval=GRANTED`.

### `inputs_hash`

SHA-256 hash of the canonical input bundle.

### `outputs_hash`

SHA-256 hash of the canonical output bundle, or:

```text
NONE
```

### `previous_receipt_hash`

The prior receipt hash in the relevant receipt chain, or:

```text
GENESIS
```

### `receipt_hash`

SHA-256 hash of the canonical receipt body.

The `receipt_hash` MUST be computed after excluding the `receipt_hash` field itself.

### `replay_status`

Allowed values:

```text
PASS
FAIL
DRIFT
BLOCKED
NOT_REPLAYED
```

### `verdict`

Allowed values:

```text
ADMISSIBLE
REJECTED
PROVISIONAL
QUARANTINED
```

### `witnesses`

List of witness records.

Minimum witness object:

```yaml
- witness_id: string
  witness_type: HUMAN | AGENT | SERVICE | REPOSITORY | WALLET
  witness_ref: string
  signature: string | NONE
```

### `notes`

Plain-language reviewer notes. Notes are not authority. They are explanatory context only.

---

## 6. Canonicalization Rule

Before hashing, every receipt MUST be canonicalized:

```text
UTF-8
sorted keys
no trailing whitespace
stable timestamp format
stable enum casing
receipt_hash field excluded from hash preimage
```

If canonicalization cannot be reproduced, the receipt is `REJECTED`.

---

## 7. Coinbase Treasury Constraints

For Coinbase-enabled CWaaS receipts:

```yaml
execution_mode: PREVIEW_ONLY | READ_ONLY | HUMAN_APPROVED | BLOCKED
human_approval: REQUIRED | GRANTED | DENIED | NOT_REQUIRED_READ_ONLY
```

Default v0.1 treasury posture:

```text
PREVIEW_ONLY=true
HUMAN_APPROVAL=required
RECEIPT_HASH_REQUIRED=true
AUTO_EXECUTION=false
```

Any asset-moving event without human approval is automatically:

```text
verdict: REJECTED
replay_status: BLOCKED
```

---

## 8. Example Receipt

```yaml
schema_version: RECEIPT_SCHEMA_V1
receipt_id: CWaaS-20260619-0001
timestamp_utc: 2026-06-19T00:00:00Z
system: COMPUTERWISDOM
lane: treasury
action_type: BALANCE_INSPECTION
actor: COMPUTERWISDOM-AGENT-01
subject: Coinbase portfolio snapshot
execution_mode: READ_ONLY
human_approval: NOT_REQUIRED_READ_ONLY
inputs_hash: sha256:1111111111111111111111111111111111111111111111111111111111111111
outputs_hash: sha256:2222222222222222222222222222222222222222222222222222222222222222
previous_receipt_hash: GENESIS
receipt_hash: sha256:3333333333333333333333333333333333333333333333333333333333333333
replay_status: PASS
verdict: ADMISSIBLE
witnesses:
  - witness_id: github-jsonwisdom-computerwisdom
    witness_type: REPOSITORY
    witness_ref: jsonwisdom/COMPUTERWISDOM
    signature: NONE
notes: Read-only Coinbase treasury inspection. No execution occurred.
```

---

## 9. Rejection Conditions

A receipt MUST be rejected when any of the following are true:

- Missing `schema_version`
- Missing required field
- Invalid enum value
- Non-reproducible canonicalization
- Missing `receipt_hash`
- Mismatched `receipt_hash`
- Asset-moving action without `human_approval=GRANTED`
- Replay required but `replay_status=NOT_REPLAYED`
- Witness required but absent
- Claim attempts to outrank the receipt record with narrative text

---

## 10. Review Boundary

This schema does not prove that an action was good.

It proves that an action was structured enough to be reviewed, hashed, replayed, challenged, and either admitted or rejected.

That is the CWaaS line.

---

## 11. Boss Brenda Lock

```text
No schema, no green.
No receipt hash, no authority.
No replay, no settlement.
No human approval, no treasury execution.
No narrative override.
```

---

## 12. Next Dependent Specs

After `RECEIPT_SCHEMA_V1`, the next primitives are:

1. `TREASURY_GATE_V0_2.md`
2. `REPLAY_TRACE_FORMAT_V1.md`
3. `AGENT_ACTION_RECEIPT_V1.md`
4. `BASE_ATTESTATION_FLOW_V1.md`

`RECEIPT_SCHEMA_V1` is the root. Everything else builds on it.
