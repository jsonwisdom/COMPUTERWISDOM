# CoinBaseKid REPLAY 007 — §5b signed encrypted export candidate

**Status: PRODUCTION EXPORT HOLD.** Code and synthetic tests only. This module does not expose a URL, publish a bundle, sign real wallet requests, grant payment authority, or move funds.

## Two independent mechanisms

The recipient's ability to decrypt is NOT the same as authorization to export.

1. **Authorization** is an EIP-712 typed signature from a separate export-authority signer, with exact Base domain (name, version, chainId 8453, salt) and signed action, bundle root, recipient identifier, X25519 recipient-key fingerprint, scope, issue/expiry, export nonce, authority address, origin, and no-payment purpose.
2. **Confidentiality** comes from recipient-specific X25519 ephemeral ECDH, HKDF-SHA256 with a fresh salt and authenticated AES-256-GCM. The AEAD associated data binds root, recipient, public key fingerprint, scope, expiry, nonce, and authorization digest. Raw ciphertext can be downloaded without giving access to signatures. A wrong X25519 private key fails to decrypt. Never use an Ethereum wallet address alone as an encryption key.

The recipient label (DID/0x) and recipient's X25519 public key must be bound through an **external, authenticated identity/key registry**. This repository does not perform DID resolution or attest recipient identity. Even with a valid public key, any holder of the corresponding *private key* can decrypt the exported ciphertext. Export expiry prevents new export issuance; it cannot claw back ciphertext already given to a recipient.

## Role separation and release prerequisites

- Batch signer = wallet-control proof signer. Production signer policy is separately pinned and never grants export rights.
- Bundle creator = creator declared in the private bundle; creator provenance is not yet independently authenticated.
- Acceptance witness = separate signed, durable root/block observer; production witness public key is not yet enrolled.
- Export authority = second independent, scoped key, unequal to bundle creator, batch signer, or witness. Production export policy has \`authorizedExportAuthorities:[]\`, \`productionEnabled:false\`, and out-of-band key verification NOT_ESTABLISHED. **No production export can pass**.

Before any export candidate, a cryptographically valid witness must already exist for the root in the local SQLite database, and the exact original EIP-712 proof list must recompute the same candidate Merkle root. For archival replay after a proof's five-minute live window, the proof is evaluated at the separately witnessed acceptance timestamp. An independent witnessed timestamp/actual Base block height still needs a trusted external source. No accepted root can be inferred from a signature alone.

## Scope discipline

- \`root_only\`: decrypted payload includes exactly \`{root,createdAtBlock}\`. No proof or signature fields anywhere in this decrypted payload.
- \`proofs_only\`: decrypted payload includes exactly \`{root,proofs}\`.
- \`full\`: decrypted payload includes \`{root,creator,createdAtBlock,witnesses,proofs}\`.
- Scope changes after signing invalidate EIP-712 recovery. Encryption authenticates the chosen scope and destination. No cross-root authorizations.
- All output is a **local encrypted candidate** with \`publication:false\` and \`authority:false\`. No HTTP GET/export route was created.

## Append-only export events

In the same local SQLite file, \`export_events\` records each successful distinct export event (its own autoincrement id, signed authorization and ciphertext digest). \`export_nonces\` prevents reusing the same authorization nonce, even for an unchanged root. Two separately signed export requests for one root create two separate events. This is append-only at the application level; a database administrator could still delete or alter SQLite files. External tamper-evident replication/checkpoints are a separate gate.

## Integration test

\`node --test services/confucius-compute-wisdom/base-batches/encrypted-export.test.mjs\`

The tests create **synthetic, unfunded** EIP-712 signing keys for batch, independent witness, separate export signer and creator. Tests also generate ephemeral recipient X25519 keys and verify correct decrypt, wrong key refusal, authenticated tampering refusal, no raw signature in encrypted envelope, strict scope, expiry, nonce replay, multiple export event rows, independent role rejection, and production HOLD.

## Production blockers (OPEN)

- Independently enrolled acceptance witness public key and authenticated creator/block-height provenance (§5a).
- Out-of-band verified export-authority key and recipient DID-to-X25519 key binding (§5b).
- Robust centralized multi-instance replay/nonce store; the SQLite prototype is one authoritative local DB.
- Independent review of recipient delivery, optional ciphertext storage/envelope file permissions, logging/redaction, key rotation and security operations.
- Full public release of proofs is **not** enabled; privacy and independently recomputable proofs are compatible only for specifically authorized recipients.

No mainnet payments, x402 settlement or wallet approvals are authorized by this prototype.
