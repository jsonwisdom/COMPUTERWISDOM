# ACTION_PROPOSAL_SCHEMA_V1

## Status

Canonical draft for Sovereign OS.

This schema defines the minimum machine-readable proposal surface required before any Sovereign OS action may execute.

It inherits:

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

---

## Root Binding

All action proposals must bind back to the COMPUTERWISDOM root:

```text
0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b
```

EAS witness:

```text
0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84
```

---

## Purpose

An action proposal declares an intended governance action before execution.

It does not authorize itself.
It does not execute itself.
It does not create legitimacy by existing.

It creates an inspectable pre-execution object.

---

## Required Fields

```json
{
  "proposal_id": "string",
  "authority_id": "string",
  "proposer": "string",
  "action_type": "string",
  "target": "string",
  "intent": "string",
  "inputs": {},
  "expected_outputs": {},
  "risk_class": "LOW|MEDIUM|HIGH|CRITICAL",
  "required_verifier": "string",
  "root_hash": "string",
  "eas_attestation_uid": "string",
  "created_at": "string",
  "expires_at": "string|null"
}
```

---

## Required Checks

Before execution, the system must verify:

- authority declaration exists
- authority scope permits the proposed action
- proposal is not expired
- proposal target is explicit
- expected outputs are declared
- verifier surface is declared
- root hash matches the current COMPUTERWISDOM spine

---

## Proposal Invariants

```text
proposal_created != action_authorized
proposal_validated != action_executed
proposal_executed != action_legitimate
```

A proposal is an inspectable intent object, not a grant of authority.

---

## Forbidden Defaults

Sovereign OS V1 forbids:

- ambient proposals
- implicit targets
- unstated inputs
- hidden expected outputs
- proposal execution without authority check
- verifier omission
- retroactive proposal creation

---

## Required Receipts

Every proposal must emit:

```text
ACTION_PROPOSAL_RECEIPT_<N>.json
```

If validation fails, emit:

```text
ACTION_PROPOSAL_REJECTION_RECEIPT_<N>.json
```

If execution occurs without a valid proposal, emit:

```text
UNPROPOSED_ACTION_RECEIPT_<N>.json
```

---

## Failure Handling

Proposal failures are continuity events.

They must record:

- proposal id
- rejection reason
- failed check
- expected value
- observed value
- verifier identity
- timestamp

Failures must not be silently repaired.

---

## Anti-Claims

This schema does not claim:

- proposal equals authorization
- proposal equals execution
- proposal equals legitimacy
- proposer authority by default
- global governance authority

It claims only:

- a proposed action exists
- the intended action is inspectable
- the proposal can be checked against authority boundaries

---

## Closing Statement

Sovereign OS actions begin as bounded proposals.

No execution should occur before proposal and authority surfaces are both declared.
