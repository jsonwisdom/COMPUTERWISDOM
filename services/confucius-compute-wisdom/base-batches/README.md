# CoinBaseKidSignatureProofExactMatch — REPLAY 005 v2

Status: **OFFLINE CRYPTOGRAPHIC CANDIDATE ONLY** · x402/production/publishing HOLD.

Canonical signed policy: [flywheel-connect/base-wallet-policy.v2.json](../../../flywheel-connect/base-wallet-policy.v2.json). The Flywheel page embeds a checked mirror; both are compared in CI. A change to signer membership requires a reviewed policy revision and matching website deployment. The test harness injects **synthetic-only** accounts into an internal `__testing` path; the public verifier never grants those test accounts production approval.

## REPLAY 005 seven gates

1. **Domain isolation — v2:** The signed EIP-712 domain pins `name: Flywheel Base Wallet Control`, `version: 2`, `chainId: 8453`, and the exact 32-byte app-specific `salt` from the versioned policy. No onchain verifying contract is deployed for this **off-chain** EOA control check. EIP-712 makes `verifyingContract` optional, and `salt` is the standard substitute for protocol-specific disambiguation. A supplied `verifyingContract`, missing/wrong salt, wrong name/version, chain 1 or 84532 all cause **HOLD**, not implicit trust. An arbitrary other application with the same public domain fields could technically mimic them; no cryptographic domain can prevent deliberate exact copying.
2. **Authorized signer — v2:** Verifier must confirm `recovered == typedData.message.wallet == expectedSigner` and signer membership in the canonical *versioned* allowlist. Membership is restricted to the known laptop account and to **off-chain control checks only**. It proves no ENS ownership, API authorization, contract permission or payment rights.
3. **Signed origin — already cryptographic:** `origin` is a `string` member of the signed `WalletControl` struct; it is hashed by EIP-712. Exact `https://wallet.jsonwisdom.com` required. An HTTP Origin header is never used as the proof. The verifier rejects origin changes even when the signature otherwise matches.
4. **Cross-batch nonce — LOCAL INTEGRATION CANDIDATE; production OPEN:** A separate opt-in SQLite entrypoint, `replay-ledger.mjs`, first cryptographically checks the entire EIP-712 proof batch with the shared policy. Only valid batches open SQLite and atomically consume `(chain_id, signer, nonce)` under `BEGIN IMMEDIATE`. **Permanent nonce rule:** consumption is per signer on Base, permanent across policy versions and domain salts; v3 does not reset it. Random bytes32 nonce *values* are not numeric sequences: the **consumed set** grows monotonically. Local SQLite does not coordinate across hosts or establish the nonce issuer; production global uniqueness remains OPEN.
5. **Public proof-list publication — OPEN:** A candidate root can be reproduced only when independently obtained input proofs and the documented leaf order are available. This tool does **not** automatically publish the raw signatures or proofs. Publication needs explicit privacy review and user authorization. A root by itself is not publicly auditable evidence.
6. **Empty batch — closed:** Explicit `n >= 1` and `n <= 1000` check, with distinct `EMPTY_BATCH` HOLD. No vacuous pass.
7. **Legacy signer — v2 gated:** Former EIP-191 signatures and v1 EIP-712 signatures are **not accepted by this v2 verifier**. The current Flywheel website code uses v2 only after its release is deployed. Previously opened tabs, downloaded signatures, or third-party systems using older protocols cannot be revoked solely by updating this verifier.

## Exact immutable proof requirements

Each item includes exactly `expectedSigner`, `typedData`, and `signature`. Typed data includes exactly `types`, `primaryType`, `domain`, and `message`.

Domain must contain exactly `name`, `version`, `chainId`, `salt`. EIP712Domain field order: name, version, chainId, salt. WalletControl field order: origin, wallet, purpose, nonce, issuedAt, expiresAt, policy. Missing or extra fields are rejected.

Exactly 65-byte ECDSA signature and recovered EOA address are checked using pinned `ethers@6.17.0`. **Contract-wallet/EIP-1271 signatures are outside this gate** and must not be mislabeled EOA proofs. Nonce length: 32 bytes. Expiry exactly 300 seconds after issue, with max +30 seconds clock skew.

The verifier **never contacts a wallet, chain, or network**; never signs, transfers, publishes, or writes a receipt. Its output does not echo the signature. Neither a cryptographic pass nor candidate batch Merkle root establishes historical issuer provenance or actual Base blockchain state. No real wallet keys are present in tests.

## Replay format and deterministic Merkle math

Top-level input `{"proofs":[...]}` (one to 1000 rows); source records must match the EIP-712 format displayed by the live website, including the current salt and version.

Usage after installing the pinned local dependency:

```bash
node --test services/confucius-compute-wisdom/base-batches/verify-base-signatures.test.mjs
node services/confucius-compute-wisdom/base-batches/verify-base-signatures.mjs < local-proofs.json
```

For each valid proof, recompute EIP-712 digest and `signatureHash = 0x + SHA256(raw signature bytes)`. Leaf = SHA256(0x00 || JSON UTF-8 tuple of `[COINBASEKID_BASE_SIGNATURE_EXACT_MATCH_V2, lowercaseSigner, lowercaseEIP712Digest, signatureHash]`). Internal parent = SHA256(0x01 || left32 || right32), duplicate odd last element. Root only if EVERY row matches and batch size is valid. The root is merely a private **candidate** until independent evidence publication and verification.

## Residuals

- An original issuer challenge and nonce consumption are not independently proven by self-reported typed-data fields.
- Membership in a local signer allowlist is a policy decision, not proof of legal identity, ENS control or permission to move funds.
- A versioned signature policy cannot disable already-running older browser tabs by itself.
- Wallet-extension/CDN telemetry may occur outside this verifier; no site code check can establish the wallet vendor's data-retention behavior.
- Mainnet funds and all x402 settlement remain HOLD.

## REPLAY 007 real-crypto-to-SQLite integration (review branch only)

- File: `replay-ledger.crypto.integration.test.mjs`. One integration test covers all five acceptance/replay/tamper/second-connection steps.
- The signer is a deterministic, unfunded **synthetic EIP-712 key** outside the production signer allowlist. It is admitted only through `__testing`, which runs actual ethers signature recovery, not mocked crypto; the production entrypoint still rejects this key.
- Step 1: verifyBaseProofBatch accepts exact EIP-712 v2 Base proof and produces the same typed-data digest recomputed separately.
- Step 2: BEGIN IMMEDIATE and one COMMIT insert the batch and nonce; SQL rows must match the typed-data digest and Merkle root.
- Step 3: identical proof returns HOLD/NONCE_REPLAY; both tables unchanged.
- Step 4: distinct fresh nonce plus signature by a different private key returns HOLD/PROOF_INVALID, and the database is untouched.
- Step 5: second SQLite connection observes persistent nonce and rejects the same proof; a manual SQL duplicate insertion with a distinct digest raises the UNIQUE constraint. The production reservation path catches it earlier via under-lock precheck.
- A fresh legitimate proof after rejected tampering still commits; synthetic key never passes the production policy.

**Open:** multi-host coordination, issuer-signed nonce origin, real-wallet production integration, acceptance-time independent witness, proof-list release, signed export authorization, encryption-to-recipient, global replay protection. The test makes **no** mainnet, x402, fund-transfer or publication claim.

### Deployment boundary — SINGLE-WRITER LOCAL SQLITE ONLY

The file-backed nonce ledger is scoped to **one authoritative process/host sharing one durable SQLite file**. A pool of two replicas behind a load balancer with separate local DB files **will accept the same valid proof twice**: the composite primary key only serializes writes within the same database. A shared SQLite file over network storage is **not** an approved production workaround. Do **not** deploy multiple replicas.

Future multi-instance support requires an independently reviewed centralized transaction store (e.g., PostgreSQL with unique `(chain_id, signer, nonce)`, atomic insert and conflict handling) or an issuer-controlled nonce service. Neither exists in this PR. All signatures/receipts continue to have `authority=false` and payments HOLD.

This review also confirms the stronger invalid-proof ordering assertion: the test checks SQLite `consumed_nonces` counts before and after tampering **and** asserts that a fresh, invalid EIP-712 proof leaves no SQLite, WAL or SHM file. The production code returns `PROOF_INVALID` before `openDb()` and before `BEGIN IMMEDIATE`.

