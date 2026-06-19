# IDENTITY_WITNESS_HUMAN_APPROVAL_GATE_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Identity / Human Approval / External Witness

## Purpose

Defines the human approval gate required before any EAS identity witness submission can occur.

This gate ensures:

- No autonomous identity witness submission
- No implicit endorsement
- No identity verification claim
- No payment authority
- No on-chain action without explicit human approval

This gate governs the transition:

```text
DRY_RUN → HUMAN_APPROVED → EAS_SUBMISSION_READY
```

It does not authorize the submission itself.  
It only authorizes the transition from preview to submission-eligible.

## Approval Command

Approval must be explicit and human-authored:

```text
/approve-identity-witness
```

This command must appear in:

- a GitHub issue
- a GitHub PR comment
- or a designated approval file

Automated systems may not issue this command.

## Gate Inputs

```text
identity_receipt: IDENTITY_ATTESTATION_RECEIPT_V1
dryrun_envelope: EAS_IDENTITY_WITNESS_ENVELOPE_DRYRUN_0001.json
dryrun_trace: EAS_IDENTITY_WITNESS_ENVELOPE_DRYRUN_TRACE_0001.md
schema: IDENTITY_ATTESTATION_SCHEMA_V1
binding_hash: <sha256>
replay_trace_hash: <sha256|null>
```

All inputs must be present and replay-verified.

## Gate Checks

```text
identity_receipt_present: true
dryrun_envelope_present: true
dryrun_trace_present: true
schema_valid: true
binding_hash_valid: true
dryrun_mode: true
on_chain_action_claimed: false
eas_uid_claimed: false
endorsement_claimed: false
payment_authority_claimed: false
```

If any check fails, the output is `BLOCKED`.

## Gate Output

If `/approve-identity-witness` is issued:

```text
approval_status: HUMAN_APPROVED
approval_actor: <github_username>
approval_timestamp_utc: <iso8601>
transition: DRY_RUN → EAS_SUBMISSION_READY
```

If rejected:

```text
approval_status: REJECTED
transition: DRY_RUN → BLOCKED
```

## Boundary Conditions

This gate does not:

- submit an EAS attestation
- create an EAS UID
- anchor anything on Base
- authorize payment
- verify legal identity
- imply endorsement by ENS, Base, Coinbase, GitHub, or EAS

It only authorizes the transition to a state where submission is allowed.

## Boss Brenda Lock

```text
No identity receipt, no approval gate.
No dry-run envelope, no approval gate.
No replay trace, no approval gate.
No human approval, no EAS submission.
No endorsement by implication.
No payment authority from identity alone.
No fake green.
```
