# AUTHORITY_DECLARATION_SCHEMA_V1

## Status

Canonical draft for Sovereign OS.

This schema defines the minimum machine-readable authority boundary required before any Sovereign OS action may execute.

It inherits the verified COMPUTERWISDOM anchor topology:

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

---

## Root Binding

All authority declarations must bind back to the COMPUTERWISDOM root:

```text
0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b
```

EAS witness:

```text
0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84
```

---

## Purpose

An authority declaration defines who or what is permitted to propose, execute, verify, repair, or interpret an action.

It does not grant legitimacy by itself.

It creates an inspectable boundary before action.

---

## Required Fields

```json
{
  "authority_id": "string",
  "subject": "string",
  "role": "string",
  "scope": "string",
  "allowed_actions": ["string"],
  "forbidden_actions": ["string"],
  "root_hash": "string",
  "eas_attestation_uid": "string",
  "effective_from": "string",
  "expires_at": "string|null",
  "revocable": true,
  "human_interpretation_required": true
}
```

---

## Role Classes

Initial role classes:

- OPERATOR
- VERIFIER
- REPAIR_ACTOR
- INTERPRETER
- OBSERVER
- ARCHIVE_MAINTAINER

A role must not silently inherit authority from another role.

---

## Authority Invariants

```text
authority_declared != action_authorized
action_authorized != action_executed
action_executed != action_legitimate
```

Authority must be explicit, scoped, revocable, and receipt-bound.

---

## Forbidden Defaults

Sovereign OS V1 forbids:

- ambient authority
- inherited authority by implication
- silent role expansion
- unsigned repair authority
- verifier self-approval
- interpreter mutation rights

---

## Required Receipt

Every authority declaration must emit:

```text
AUTHORITY_DECLARATION_RECEIPT_<N>.json
```

The receipt must bind:

- authority declaration hash
- subject
- role
- scope
- allowed actions
- forbidden actions
- root hash
- EAS witness UID
- revocation path

---

## Failure Handling

If an action is attempted outside declared scope, the system must emit:

```text
AUTHORITY_VIOLATION_RECEIPT_<N>.json
```

Authority violations are not warnings.
They are continuity events.

---

## Anti-Claims

This schema does not claim:

- legal authority
- institutional authority
- global legitimacy
- sovereignty by declaration
- trust without replay

It claims only:

- a declared boundary exists
- the boundary is machine-readable
- future actions can be checked against it

---

## Closing Statement

Sovereign OS begins with bounded authority.

No action should execute before its authority surface is declared.
