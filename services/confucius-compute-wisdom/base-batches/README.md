# CoinBaseKidSignatureProofExactMatch — Base Batch Cryptographic Gate V1

Status: OFFLINE REVIEW CANDIDATE ONLY. Not x402 settlement, an onchain receipt, ENS ownership, production payment batch, or delegated authorization.

This checker independently verifies the EIP-712 signing format deployed at https://wallet.jsonwisdom.com, and composes candidate proof hashes into a Merkle root only after every input is accepted.

## Exact contract

- Signed EIP-712 domain name: Flywheel Base Wallet Control; version: 1; numeric chainId: 8453. Ethereum-mainnet chain 1 NEVER passes.
- Typed-data primaryType: WalletControl. Strict ordered fields: origin (string), wallet (address), purpose (string), nonce (bytes32), issuedAt (uint256), expiresAt (uint256), policy (string). Exact EIP712Domain types are name, version and chainId.
- Signed origin: https://wallet.jsonwisdom.com. Signed purpose: Prove control of this account on Base ONLY.
- Signed policy: No transaction, token approval, payment, login, ENS/DNS ownership proof or Coinbase API authorization
- Each proof requires explicit expectedSigner, full typedData, and a 65-byte ECDSA signature. Verifier independently recomputes the digest and recovered signer. All three addresses (expectedSigner, typedData.message.wallet, recovered signer) must match.
- Nonce: 32 bytes, unique across the batch. Signed challenge duration: 300 seconds; future tolerance: 30 seconds.
- The entire batch is HOLD if any record is invalid or duplicated. There is no partial accepted root. Maximum 1,000 proof rows.
- This checker uses no wallet API, RPC, network requests, seed phrases, API keys, transactions, transfers, signing, ENS or DNS lookup. No history or receipt files are written.
- Output never echoes raw signature bytes. CANDIDATE_ROOT_READY is not verified historical provenance, authorization, production readiness, onchain status, or evidence authenticity.

## JSON input

Top level must have exactly one field: proofs (an array of 1–1,000 objects).
Each proof has exactly expectedSigner, typedData, signature fields.
The typedData shape is the EIP-712 object supplied to eth_signTypedData_v4 (types, primaryType, domain, message).

Do not submit synthetic test keys as production keys, or put private keys, Coinbase API credentials or personal information into inputs.

## Local read-only command

After installing pinned ethers@6.17.0 in this folder, run:
  node services/confucius-compute-wisdom/base-batches/verify-base-signatures.mjs < local-proofs.json

Run regression tests:
  node --test services/confucius-compute-wisdom/base-batches/verify-base-signatures.test.mjs

## Deterministic candidate Merkle format

For each independently matched proof:
  typedDataDigest = lowercase EIP-712 digest
  signatureHash = 0x + SHA256(raw 65-byte signature)
  tuple = JSON.stringify(["COINBASEKID_BASE_SIGNATURE_EXACT_MATCH_V1",lowercaseSigner,typedDataDigest,signatureHash])
  leaf = SHA256(0x00 || UTF8(tuple))
  parent = SHA256(0x01 || leftNode32 || rightNode32)

Duplicate the final node at odd-width levels. Root is a lowercase 0x-prefixed digest. Leaf order matters. The candidate Merkle root is NOT published to Base and does NOT authorize anything.

Bulk builder Base batches still require separate artifact byte hashes, original source evidence, independent reproduction, and explicit approvals before publishing or settlement. Signatures authenticate only their exact signed messages.

IMPORTANT: Proofs imported offline cannot alone prove that an origin server really generated the nonce or that a signature hasn't been replayed in another batch. Only per-batch uniqueness is enforced. Fresh issuer-side nonce storage/replay rejection is a separate gate.
