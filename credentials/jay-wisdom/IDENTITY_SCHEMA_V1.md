# JSONWisdom Dedicated Identity Schema v1

Status: `DEFINED_RESOLVER_IMPLEMENTED_TESTED_NOT_REGISTERED`
Network target: `Base Sepolia`
Purpose: parent identity/provenance attestation accepted by `AuthorityGuardResolver` for the on-chain resume integrity chain.

## Design law

This schema records a cryptographic identity-binding statement. It does **not** create legal identity, institutional authority, credential authority, employment verification, or truth by itself.

```text
EXISTENCE != IDENTITY_AUTHORITY
ATTESTATION != CREDENTIAL
WITNESS != TRUTH
AUTHORITY_CREATED = FALSE
```

## Canonical schema string

```solidity
bytes32 bindingHash,string subjectAnchor,string artifactId,bool authorityCreated
```

### Fields

- `bindingHash` — nonzero SHA-256 digest of the canonical off-chain identity-binding statement/bundle.
- `subjectAnchor` — human-readable discovery label such as `jaywisdom.base.eth`; it is metadata, not proof of ENS control by itself.
- `artifactId` — stable version identifier such as `jay-identity-v1`.
- `authorityCreated` — MUST be `false` and MUST be rejected when `true`.

## EAS protocol fields used instead of duplicated schema fields

The following are deliberately **not** repeated in schema data:

- `recipient` — canonical subject/controller address.
- `attester` — signer that issued the identity-binding attestation.
- `time` — EAS creation timestamp.
- `expirationTime` — optional expiration / key-rotation boundary.
- `refUID` — MUST be zero for this root identity attestation.

This avoids dual truth sources such as `ethAddress != recipient` or `validUntil != expirationTime`.

## IdentityBindingResolver implementation

The identity schema MUST NOT be registered with resolver `0x0` while claiming fail-closed enforcement.

Implemented files:

```text
contracts/jaywisdom/src/IdentityBindingResolver.sol
contracts/jaywisdom/test/IdentityBindingResolver.t.sol
```

Verified CI result on code head `215d7a6abed9403addaca4e528aedd9be80a2220`:

```text
IdentityBindingResolver = 15 PASS / 0 FAIL / 0 SKIP
AuthorityGuardResolver  = 20 PASS / 0 FAIL / 0 SKIP
Full Foundry project    = 44 PASS / 0 FAIL / 0 SKIP
Secret scan             = PASS
```

Required gates:

```text
I1 attestation.attester == EXPECTED_ATTESTER
I2 attestation.recipient != address(0)
I3 bindingHash != bytes32(0)
I4 bytes(subjectAnchor).length > 0
I5 bytes(artifactId).length > 0
I6 authorityCreated == false
I7 attestation.refUID == bytes32(0)
```

Governance constraints:

```text
OWNER                  = NONE
PROXY                  = NONE
UPGRADEABILITY         = FALSE
MUTABLE_ALLOWLIST      = NONE
EXPECTED_ATTESTER      = IMMUTABLE
REVOCATION_ALLOWED     = TRUE
AUTHORITY_CREATED      = FALSE
```

## Expected attester deployment binding

```text
0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5
```

The implementation accepts the expected attester as an immutable constructor parameter. The Base Sepolia deployment is required to bind the candidate above into an actual deployed resolver address.

## Base Sepolia protocol targets

```text
EAS             = 0x4200000000000000000000000000000000000021
SchemaRegistry  = 0x4200000000000000000000000000000000000020
```

## Registration policy

```text
schema      = bytes32 bindingHash,string subjectAnchor,string artifactId,bool authorityCreated
resolver    = PENDING_BASE_SEPOLIA_DEPLOYMENT_ADDRESS
revocable   = true
schema_uid  = PENDING_REGISTRATION
```

No schema registration, resolver deployment, or attestation has occurred as a result of this document.

## Child relationship

A resume attestation may reference this identity attestation through `refUID` only when `AuthorityGuardResolver` independently verifies:

- parent UID exists;
- parent schema equals the registered dedicated Identity Schema UID;
- parent is not revoked;
- parent is not expired;
- parent attester equals the immutable expected attester;
- parent recipient equals the resume recipient.

## State transition

```text
DEFINE_DEDICATED_IDENTITY_SCHEMA = COMPLETE
IMPLEMENT_IDENTITY_BINDING_RESOLVER = COMPLETE
IDENTITY_RESOLVER_UNIT_TESTS = PASS
NEXT = DEPLOY_IDENTITY_RESOLVER_BASE_SEPOLIA
REGISTER_IDENTITY_SCHEMA_BASE_SEPOLIA = BLOCKED_UNTIL_RESOLVER_ADDRESS_CAPTURED
```
