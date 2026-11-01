# REPLAY 007 — §5b recipient identity → X25519 encryption key trust specification

**Status:** Candidate authentication specification only. Recipient identity binding is **NOT implemented or independently enrolled**. Production export remains **HOLD**. No new API, key, wallet transaction, or payment authority.

## What exists and what does not

The merged exporter accepts a caller-supplied X25519 public key; a signed `ExportAuthorization` binds its SHA-256 SPKI fingerprint, recipient label, root, scope, nonce and expiry. The local export test proves authenticated ciphertext decrypts with the matching private key and not an unrelated key. **This does not prove that the supplied key belongs to the named recipient.** A writable `recipient → key` database map is untrusted input.

The activation trust chain must be:

`recipient DID / identity` → `authenticated controller / verification method` → `controller-signed encryption-key binding` → `X25519 SPKI DER bytes (SHA-256)` → `signed export authorization's recipient + fingerprint` → `authenticated ciphertext` → `recipient private-key decryption`.

See W3C DID Core, including verification-method rotation and revocation: https://www.w3.org/TR/did-core/ . The existing X25519/HKDF/AES-GCM implementation is **custom envelope code**, not claimed RFC 9180 HPKE interoperability. RFC 9180 is background only: https://www.rfc-editor.org/rfc/rfc9180.html .

## Required recipient-key attestation (future protocol)

A versioned signed binding MUST contain exact fields:

```json
{
  "schema": "COINBASEKID_RECIPIENT_KEY_BINDING_V1",
  "recipient_id": "did:example:recipient",
  "controller_id": "did:example:controller",
  "verification_method": "did:example:controller#key-1",
  "encryption_key_type": "X25519-SPKI-DER",
  "recipient_key_sha256": "0x<32-byte-sha256-of-DER>",
  "issued_at": "<unix-seconds>",
  "expires_at": "<unix-seconds>",
  "binding_nonce": "0x<32-byte-random>",
  "policy_version": "1",
  "purpose": "COINBASEKID_RECIPIENT_EXPORT_DECRYPTION_ONLY",
  "signature": "<controller-signature-over-all-fields-above>"
}
```

**No invented DID, controller, or key is enrolled by this example.** Require a specified canonical encoding and controller-supported signature algorithm before implementation; the signature field must not be treated as covering itself. A DID document or signed registry entry MUST establish that the verification method is authorized by the resolved controller **as of the relevant issuance time**, with revocation and rotation checks. The registry/resolver trust root and independently authenticated retrieval channel must be named and versioned. DNS/ENS labels or database rows alone never establish the identity-to-X25519-key binding.

## Fail-closed export decision

1. Resolve recipient identity through the explicitly approved DID method / controller trust source. Retrieve and independently validate the controller-signed binding. Validate dates, nonce/replay status, version, purpose, issuer authority, revocation and key rotation. Missing, stale, malformed, conflicting, self-issued without authority, or unverifiable evidence → **HOLD / RECIPIENT_BINDING_UNVERIFIED**.
2. Parse the **exact supplied X25519 SPKI DER bytes** and calculate the SHA-256 fingerprint. Require both `binding.recipient_id == ExportAuthorization.recipient` and `binding.recipient_key_sha256 == ExportAuthorization.recipientKeyFingerprint == SHA256(DER)`. Any difference → **HOLD / RECIPIENT_KEY_BINDING_MISMATCH**, before encryption or export-ledger write.
3. Require an independently enrolled export-authority signature, distinct from creator, batch signers and witness, over root, recipient, fingerprint, scope, time and nonce. Require independently witnessed accepted root and independently verified creator provenance. Any missing link → HOLD. Existing `authorizedExportAuthorities: []` correctly blocks production.
4. Encrypt only to the verified recipient key, authenticate metadata, and log a separate signed export event. Apply scope to plaintext before encryption. `root_only` must never contain signature fields, even after authorized decryption.
5. Never fall back to a raw user-supplied key, an operator-edited mapping, guessed wallet public key, unsigned registry row or an unvalidated DID document. Key loss or verification outages mean HOLD, not bypass. Rotation requires a fresh, controller-authorized binding; expired/revoked keys cannot receive new exports. Existing ciphertext cannot be recalled after recipient-key compromise.

## Adversarial acceptance tests for implementation

**Key substitution (load-bearing):** A valid signed export authorization names recipient `R` and fingerprint of key `K_R`. Attacker with database write access replaces the mapping with `K_A`. The export MUST refuse the substituted key **before encryption** with `RECIPIENT_KEY_BINDING_MISMATCH`; zero new export events. A tampered or expired controller signature → HOLD. A valid controller rotation to `K_R2` requires a new signed authorization naming `K_R2`'s fingerprint; old export authorization cannot be silently upgraded.

**Existing crypto checks remain mandatory:** correct private key decrypts; wrong private key fails; ciphertext or AAD change fails; signed root/recipient/scope cannot be altered; expired export authorizations and reused nonces are rejected.

## Transport and operational boundary (not implemented)

A future export HTTP endpoint requires **authenticated recipient delivery + scoped, rate-limited ACL + audit logging**. Encrypted ciphertext may be observable without exposing plaintext; transport ACL prevents bulk harvesting and abuse but does not replace cryptography. TLS, request authentication, denial-of-service limits, and ciphertext-access logging require separate deployment review.

**Trust concentration:** one enrolled export authority or identity controller is a single-key trust root unless custody/threshold policy proves otherwise. Store signer keys separately; no code or test demonstrates independent human custodians today. Production remains disabled until externally verified recipient binding, witness/creator provenance, authority enrollment and the transport gate have all passed.
