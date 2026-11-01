# REPLAY 007 — §5b Recipient identity ↔ encryption-key binding

**Spec candidate; not implemented.** Production §5b is HOLD. Existing X25519/HKDF/AES-GCM ciphertext confidentiality tests PASS, but the local exporter accepts a caller-supplied public key; encryption does **not** establish which person/DID controls it.

## Required authentication chain

`recipient DID` → `authenticated DID controller and verification method` → `controller-signed X25519 key binding` → `SHA-256(SPKI DER)` → `signed ExportAuthorization(recipient, fingerprint, root, scope)` → `authenticated ciphertext`.

A writable `recipient → key` database row is **untrusted data**, never the trust root. A resolver/controller policy must be independently approved and versioned. Resolve the correct DID method, authenticate its controller and authorized verification method, and check revocation/rotation. Reference: [W3C DID Core](https://www.w3.org/TR/did-core/).

## Mandatory signed key binding (future format)

```json
{
  "schema": "COINBASEKID_RECIPIENT_KEY_BINDING_V1",
  "recipient_id": "did:example:recipient",
  "controller_id": "did:example:controller",
  "verification_method": "did:example:controller#key-1",
  "encryption_key_type": "X25519-SPKI-DER",
  "recipient_key_sha256": "0x<sha256-SPKI-DER>",
  "issued_at": "<unix-seconds>",
  "expires_at": "<unix-seconds>",
  "binding_nonce": "0x<bytes32>",
  "policy_version": "1",
  "purpose": "COINBASEKID_RECIPIENT_EXPORT_DECRYPTION_ONLY",
  "signature": "<controller signature>"
}
```

The signature MUST cover every field **except itself** with a documented canonical serialization and DID-method-approved algorithm. These are format placeholders, **not enrolled identities**. Controller ownership, fresh validity, binding nonce history, current revocation, key rotation and independently authenticated DID resolution must be established before use.

## Export decision — fail closed

1. Independently verify the DID/controller signature and binding validity. Missing, stale, conflicting, revoked, rotated, unresolvable or unsigned identity-to-key evidence → `RECIPIENT_BINDING_UNVERIFIED` / **HOLD**.
2. Parse exact X25519 SPKI DER bytes and recompute the fingerprint. Require **binding.recipient_id == signed ExportAuthorization.recipient** and **binding.recipient_key_sha256 == signed ExportAuthorization.recipientKeyFingerprint == SHA256(SPKI DER)**. Mismatch → `RECIPIENT_KEY_BINDING_MISMATCH` before encryption, network delivery or any export-log write.
3. Separately verify witnessed root, authenticated creator provenance, independent export-authority signature, root/scope, expiration and nonce. The current production authority/witness key lists are empty; all production exports continue to HOLD.
4. Scope plaintext *before* encryption: `root_only` must contain no signatures, `proofs_only` only matching proofs, `full` the approved bundle. Encrypt only to the **verified recipient's X25519 key** using fresh ephemeral key agreement and authenticated metadata. Existing implementation is custom, not asserted RFC 9180 HPKE compliant.

Never fall back to operator-edited key mappings, unsigned keys, unverified DID documents, an Ethereum wallet address misused as an X25519 key, or stale attestations. After approved key rotation, **new** exports require a **new** signed authorization binding the new fingerprint; old encrypted files cannot be recalled.

## Adversarial acceptance tests

**Key-substitution test:** Signed authorization names recipient R + key fingerprint `K_R`. Attacker can change a DB mapping to `K_A`. The export MUST reject `K_A` with `RECIPIENT_KEY_BINDING_MISMATCH`, **before encrypting**; export-event row count unchanged. Revoked controller, expired binding and modified attestation → HOLD. A legitimate rotation to `K_R2` cannot reuse an authorization signed for `K_R`.

Existing tests remain required: correct private key decrypts; unrelated key cannot; tampered authenticated ciphertext fails; scope and root are signed; expired authorizations/reused export nonces fail.

## Transport/custody — separate deployment gate

A future export endpoint must authenticate the recipient, apply scoped/rate-limited transport ACLs and log ciphertext access. Encryption protects plaintext, while ACLs mitigate unauthorized ciphertext harvesting; **neither substitutes for the other**. Any holder of the recipient private key can decrypt, regardless of the operator's ACL; revocation cannot retroactively remove already delivered ciphertext.

One controller key or one export-authority key is a **single-key trust root** until independent custody/threshold governance exists. Signed controller key registration, real export-authority enrollment, independent witness/block/creator provenance and reviewed transport deployment are OPEN.

**Disposition:** §5b cryptographic code PASS; authenticated recipient identity-to-key chain NOT ESTABLISHED; production export/payments HOLD.
