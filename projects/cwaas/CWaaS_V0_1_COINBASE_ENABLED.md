# CWaaS v0.1 — Coinbase-Enabled Replay Infrastructure

Status: DRAFT_LOCKED  
Lane: COMPUTERWISDOM as a Service / Coinbase Integration  
Branch: cwaas-receipt-schema-v1

## Executive Summary

CWaaS turns agent actions, governance decisions, and treasury events into replayable receipts that can be independently verified across GitHub, AL, Base, and Coinbase-connected execution surfaces.

CWaaS is not an AI certainty machine. It is receipt-first institutional memory.

## Core Thesis

COMPUTERWISDOM sells replayable institutional memory — not AI certainty.

Narratives can drift. Receipts can be replayed.

```text
GitHub stores code.
Coinbase stores assets.
Base stores attestations.
AL stores receipts.
COMPUTERWISDOM stores memory.

Replay proves all of it.
```

## System Role

CWaaS is a replay infrastructure layer for the agent economy.

It does not replace Coinbase, Base, GitHub, or AL. It coordinates proof between them.

```text
Coinbase = governed treasury surface
Base     = public attestation pointer
GitHub   = provenance and implementation record
AL       = receipt and replay authority
CWaaS    = memory/control plane
```

## v0.1 Constitutional Core

The minimum viable governance membrane contains five primitives:

```text
RECEIPT_SCHEMA_V1
TREASURY_GATE_V0_2
REPLAY_TRACE_FORMAT_V1
BASE_ATTESTATION_FLOW_V1
AGENT_ACTION_RECEIPT_V1
```

These primitives define:

1. what happened,
2. what was allowed,
3. whether it still verifies,
4. how it may be publicly anchored,
5. how agent activity becomes admissible.

## Coinbase-Enabled Surface

Coinbase is treated as a governed treasury surface.

Allowed v0.1 actions:

- portfolio inspection
- balance verification
- product lookup
- fee inspection
- order preview
- human-approved execution preparation

Disallowed v0.1 actions unless separately approved and receipted:

- autonomous trading
- silent execution
- implied endorsement
- unreceipted balance or order claims
- post-hoc fake green states

## Treasury Gate v0.1/v0.2 Posture

```text
PREVIEW_ONLY=true
HUMAN_APPROVAL=required
RECEIPT_HASH_REQUIRED=true
AUTO_EXECUTION=false
```

Any treasury event that crosses from read/preview into execution must include explicit human approval and a receipt hash.

No approval means no execution green.

## Replay Lifecycle

```text
AGENT INTENT
  ↓
ACTION RECEIPT
  ↓
RECEIPT HASH
  ↓
TREASURY / POLICY GATE
  ↓
REPLAY TRACE
  ↓
VERDICT
  ↓
OPTIONAL BASE ATTESTATION
```

A receipt says what happened.  
A replay trace proves whether it still verifies.  
A Base attestation makes the verification pointer public.

## Review Model

External reviewers should be able to answer these questions without trusting the operator:

- What action was requested?
- Which agent or human initiated it?
- Which tool surface was touched?
- Was Coinbase read-only, preview-only, or execution-capable?
- Was human approval required?
- Was human approval present?
- Which schema governed the receipt?
- Which verifier replayed it?
- What verdict was emitted?
- Was any public attestation made?

If any answer is missing, the action is not green.

## Required Green Conditions

```text
schema_valid=true
receipt_hash_valid=true
policy_gate_valid=true
replay_trace_present=true
verdict_deterministic=true
```

For Coinbase treasury execution, also required:

```text
human_approval_present=true
execution_state_declared=true
execution_receipt_present=true
```

## Failure States

Allowed non-green outcomes:

```text
FAIL
DRIFT
BLOCKED
REJECTED
QUARANTINED
NEEDS_REVIEW
```

A non-green state is not a system failure by itself. It is evidence that the governance layer is working.

## Prohibited Claims

CWaaS v0.1 may not claim:

- Coinbase endorsement
- Base endorsement
- GitHub endorsement
- legal approval
- funds moved
- trade executed
- agent autonomy

unless that specific claim is backed by replayable receipt evidence.

## Implementation Targets

Next implementation targets:

```text
projects/cwaas/README.md
projects/cwaas/specs/*.md
projects/cwaas/receipts/EVENT_001_TREASURY_ATTEST_V0.md
projects/cwaas/replay/TRACE_0001.md
scripts/cwaas_verify_receipt_v1.py
scripts/run_cwaas_selftest_v1.sh
```

## Acceptance Condition

CWaaS v0.1 is green only when a Coinbase-connected agent action can produce:

```text
agent action receipt
receipt hash
treasury gate result
replay trace
deterministic verdict
human approval state
```

and the same result can be replayed from GitHub state without narrative override.

## Boss Brenda Lock

```text
No schema, no green.
No receipt hash, no authority.
No replay trace, no settlement.
No human approval, no treasury execution.
No endorsement by implication.
No fake green.
```

## Final Summary

CWaaS v0.1 gives Coinbase-enabled agents a conservative governance layer:

- read first,
- preview second,
- require approval before execution,
- emit receipts for every action,
- replay before settlement,
- attest only what can be proven.

The product is not the action.

The product is the memory that proves the action happened under declared rules.
