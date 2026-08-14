# Ziggy Identity Threshold Layer

This directory separates blockchain activity, protocol participation, address control, identity binding, third-party attestations, and authority.

No layer silently promotes another.

## Canonical ladder

`ACTIVITY → PROTOCOL_ROLE → CONTROL → IDENTITY_BINDING → AUTHORITY`

Third-party attestation is evidence **about** an address or identity relationship. It is tracked separately because:

`ATTESTATION ABOUT ADDRESS ≠ SIGNATURE BY ADDRESS`

## Thresholds

### ACTIVITY

Current meaning: observable transactions, transfers, logs, calls, or state changes involving an address.

Activity proves only activity.

### PROTOCOL_ROLE

A protocol-role claim may be promoted only when protocol-specific evidence exists, for example:

- Uniswap `Swap` event involving the address
- explicit Universal Router / PoolManager interaction attributable to the address
- liquidity-position mint or protocol state assigning a position to the address

Token receipts alone do not cross this threshold.

### CONTROL

Control may be promoted only by cryptographic evidence attributable to the address itself:

- valid `personal_sign` signature recoverable to the address
- valid EIP-712 signature recoverable to the address
- valid ERC-1271 signature when the address is a contract wallet

A third-party attestation about the address is not proof that the address signed.

### IDENTITY_BINDING

Identity binding requires evidence connecting a cryptographically controlled address to a named identity such as `jaywisdom.eth`.

A convenience label, social statement, token transfer, or screenshot is insufficient.

### THIRD_PARTY_ATTESTATION

Third-party attestations are recorded as their own evidence class.

They may support an identity claim when the attester is independently trusted or verified, but they do not prove private-key control of the subject address and do not create authority by themselves.

### AUTHORITY

Authority is never inferred from activity, protocol role, ownership, control, identity, or attestation.

Authority crosses only when an explicit human or sealed-protocol command grants it within the relevant scope.

`authority_created=false` remains the default.

## Non-collapse doctrine

- observed edge ≠ ownership
- protocol ownership ≠ private-key control
- ownership ≠ control
- control ≠ identity
- identity ≠ authority
- attestation about address ≠ signature by address
- convenience label ≠ verified claim
- Merkle commitment ≠ wallet identity

See [`thresholds.v0.1.json`](./thresholds.v0.1.json) for the machine-readable rules and [`addresses/0xf18e616d5f315435f9a0c48eed52048d4051fb27.status.v0.1.json`](./addresses/0xf18e616d5f315435f9a0c48eed52048d4051fb27.status.v0.1.json) for the current bounded address snapshot.
