# EXECUTION_RECEIPT_SCHEMA_V1

## Status

Canonical draft for Sovereign OS.

This schema defines the bounded execution evidence surface required after authority and proposal validation.

It inherits:

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

---

## Root Binding

All execution receipts must bind back to the COMPUTERWISDOM root:

```text
0x102e70b50594e412b8f15d311cc4e04f5126a4405fb3b1d02652e3d11afeaf5b
```

EAS witness:

```text
0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84
```

---

## Purpose

An execution receipt records that a proposed and authorized action actually ran.

It does not prove legitimacy by itself.
It does not replace verifier replay.
It does not erase proposal or authority requirements.

It creates an inspectable execution evidence object.

---

## Required Fields

```json
{
  "execution_id": "string",
  "proposal_id": "string",
  "authority_id": "string",
  "executor": "string",
  "action_type": "string",
  "target": "string",
  "runtime": "string",
  "runtime_version": "string",
  "input_hash": "string",
  "output_hash": "string",
  "started_at": "string",
  "completed_at": "string",
  "result": "SUCCESS|FAILURE|PARTIAL|DIVERGED",
  "root_hash": "string",
  "eas_attestation_uid": "string",
  "verifier_required": true
}
```

---

## Required Pre-Execution Checks

Before an execution receipt may be valid, the system must verify:

- authority declaration exists
- proposal exists
- proposal has not expired
- action type is allowed by authority scope
- target matches proposal target
- input hash matches proposal inputs
- expected outputs are declared
- verifier requirement is present

---

## Execution Invariants

```text
execution_recorded != execution_verified
execution_verified != action_legitimate
execution_success != human_approval
```

Execution is evidence of runtime activity, not legitimacy.

---

## Forbidden Defaults

Sovereign OS V1 forbids:

- execution without proposal
- execution without authority reference
- hidden runtime context
- unbound inputs
- unbound outputs
- missing verifier requirement
- retroactive execution receipts
- execution receipts that overwrite failure evidence

---

## Required Receipts

Every execution must emit:

```text
EXECUTION_RECEIPT_<N>.json
```

If execution fails, emit:

```text
EXECUTION_FAILURE_RECEIPT_<N>.json
```

If execution diverges from expected outputs, emit:

```text
EXECUTION_DIVERGENCE_RECEIPT_<N>.json
```

---

## Replay Requirement

Every execution receipt must be followed by a verifier run:

```text
VERIFIER_RUN_RECEIPT_<N>.json
```

The verifier must recompute or inspect:

- declared inputs
- declared outputs
- runtime assumptions
- proposal binding
- authority binding
- result class

---

## Failure Handling

Execution failures are continuity events.

They must record:

- execution id
- proposal id
- authority id
- failure class
- expected output
- observed output
- runtime context
- verifier identity if available
- repair path if proposed

Failures must not be silently normalized.

---

## Anti-Claims

This schema does not claim:

- execution equals legitimacy
- runtime success equals correctness
- output hash equals human approval
- action is globally valid
- institution endorsed the result

It claims only:

- an execution event occurred
- the event is bound to proposal and authority surfaces
- the event can be checked by verifier replay

---

## Closing Statement

Sovereign OS execution must be receipt-bound before it can be replay-verified.

No action should advance from execution to legitimacy without verifier evidence and human interpretation.
