# IDENTITY_ATTESTATION_SCHEMA_V1

Status: DRAFT_LOCKED  
Lane: CWaaS / Identity / EAS Schema  
Depends on:
- IDENTITY_ATTESTATION_RECEIPT_V1
- REPLAY_TRACE_FORMAT_V1
- BASE_ATTESTATION_FLOW_V1

## 1. Purpose

Defines the canonical schema for a future EAS witness attestation of a CWaaS identity binding.

This schema does not create truth. It defines the shape of the witness record that may later be anchored through EAS after the underlying identity binding receipt and replay trace exist.

## 2. Constitutional Role

```text
ENS root        = sovereign identity label
Basename        = operator / reputation identity
GitHub          = provenance matrix
CWaaS receipts  = replay authority
EAS             = witness registry
Base            = on-chain settlement surface
```

EAS witnesses the receipt. EAS does not replace the receipt.

## 3. Required Attestation Fields

```yaml
schema_name: IDENTITY_ATTESTATION_SCHEMA_V1
schema_version: 1
identity_root: string
operator_identity: string
github_identity: string
binding_hash: bytes32
replay_trace_hash: bytes32
binding_status: string
witness_statement: string
github_commit: string
timestamp_utc: string
```

## 4. Suggested EAS Schema String

```text
string schema_name,string schema_version,string identity_root,string operator_identity,string github_identity,bytes32 binding_hash,bytes32 replay_trace_hash,string binding_status,string witness_statement,string github_commit,string timestamp_utc
```

## 5. Allowed Binding Status Values

```text
DECLARED_PENDING_EXTERNAL_WITNESS
WITNESSED_BY_EAS
SUPERSEDED
REVOKED
```

## 6. Required Witness Statement

The witness statement must be limited to:

```text
This attestation witnesses that a CWaaS identity binding receipt and replay trace existed at the referenced GitHub commit and hashes.
```

It must not claim legal identity verification, payment authorization, asset movement, endorsement, or account ownership unless a separate receipt proves that claim.

## 7. Prohibited Claims

An identity attestation using this schema may not claim:

```text
legal identity verification
Coinbase endorsement
Base endorsement
GitHub endorsement
payment authorization
asset custody
account ownership
funds moved
trade executed
```

## 8. Validation Rules

A payload is schema-valid only if:

```text
identity_root is present
operator_identity is present
github_identity is present
binding_hash is bytes32-compatible
replay_trace_hash is bytes32-compatible
github_commit is present
binding_status is allowed
witness_statement stays inside allowed scope
```

## 9. Boss Brenda Lock

```text
No identity receipt, no identity witness.
No replay trace, no EAS witness.
No binding hash, no schema-valid payload.
No endorsement by implication.
No payment authority from identity alone.
No fake green.
```
