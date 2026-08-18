# Enterprise Receipt API v0.2 — Authorized Attestation + Negative Test Pack v2

This layer extends `JAYSPACE_REPLAY_SDK_v0.1` with an append-only Ed25519 key lifecycle, tenant-scoped authorization, historical verification, and adversarial verification vectors.

## Trust-chain invariant

```text
VALID_SIGNATURE != AUTHORIZED_SIGNATURE
```

A mathematically valid Ed25519 signature is an authorized attestation only when all policy gates are satisfied at the signing event time:

```text
SIGNATURE_VALID
AND KEY_FINGERPRINT_MATCH
AND KEY_ID_REGISTERED
AND TENANT_MATCH
AND SIGNER_ROLE_ALLOWED
AND KEY_ACTIVE_AT_SIGNING_EVENT
AND KEY_NOT_REVOKED_FOR_EVENT_SCOPE
= VALID_ATTESTATION
```

## Key lifecycle

Append-only event grammar:

```text
KEY_CREATED
-> KEY_REGISTERED
-> TENANT_BOUND
-> ROLE_GRANTED
-> ACTIVE
-> SIGN
-> ROTATED | SUSPENDED | REVOKED | EXPIRED
```

Lifecycle events do not rewrite prior receipts. Historical verification replays key state at `signed_at`.

## Three identities

```text
RECEIPT_ID
= sha256(JCS(receipt_payload))

SIGNING_EVENT_ID
= sha256(JCS({receipt_id,key_id,signed_at,signature}))

KEY_EVENT_ID
= sha256(JCS(key_event_payload))
```

`SIGNING_EVENT_ID` intentionally uses a canonical structured object rather than raw string concatenation. This removes delimiter/encoding ambiguity while preserving the intended identity of the signing act.

## Signature input

v0.2 signs the raw 32-byte SHA-256 digest represented by `receipt_id`.

```text
receipt_bytes = JCS(receipt_payload)
digest = SHA256(receipt_bytes)
receipt_id = "sha256:" + hex(digest)
signature = Ed25519.sign(digest)
```

The non-deterministic signing time belongs only to the signature attestation and never changes `receipt_id`.

## Tenant key registry

Each key record contains:

- `key_id`
- raw Ed25519 public key bytes encoded as Base64
- public-key SHA-256 fingerprint
- append-only lifecycle events

Lifecycle events bind tenant, role, activation, rotation, suspension, revocation, or expiration. A key may not authorize another tenant's receipt.

## Negative Test Pack v2

The test pack attacks the trust chain directly:

1. valid authorized signature
2. altered receipt payload
3. payload-hash mismatch
4. wrong tenant
5. unregistered key
6. wrong signer role
7. suspended key
8. revoked key
9. expired key
10. forged receipt ID
11. forged Ed25519 signature
12. rotation: historical-valid / future-invalid
13. public-key fingerprint mismatch
14. ruleset drift changes receipt identity
15. model-output promotion injected into deterministic receipt payload
16. signing-event-ID mismatch
17. same receipt signed at two valid times keeps one receipt identity but produces two signing-event identities
18. key-event payload tampering
19. historical validity before revocation
20. historical validity before suspension
21. historical validity before expiration
22. registry fingerprint tampering

## Cryptographic implementation boundary

This repository does not implement Ed25519 or RFC 8785 itself. CI uses established libraries for Ed25519 verification and JCS canonicalization. Production deployments should apply their normal dependency-vetting, key-storage, HSM/KMS, access-control, backup, and incident-response requirements.

## OpenAI boundary

The optional OpenAI layer remains downstream of deterministic replay and authorization. Model output may explain an already-produced receipt but cannot become `receipt_payload`, create a disposition, register a key, grant a role, bind a tenant, or authorize a signature.

```text
MODEL_OUTPUT != RECEIPT
MODEL_OUTPUT != KEY_EVENT
MODEL_OUTPUT != AUTHORIZED_SIGNATURE
AUTHORITY_CREATED = FALSE
```
