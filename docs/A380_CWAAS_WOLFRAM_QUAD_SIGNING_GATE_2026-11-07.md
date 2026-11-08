# CI-FIRST — Computer Wisdom × Wolfram Quad Onion Signature Gate
Date: 2026-11-07 · Scope: A380 wallet recovery and two-name independent evidence
Status: DOCUMENTED / NOT DEPLOYED / NOT SIGNED
PR: #743 (draft only)
Authority: FALSE; USER APPROVAL REQUIRED for any signing.

## Principle: A signed story is not automatically a proved system
Jason's Quad Onion application has **four network-specific, independently replayed name evidence checks**, plus a **fifth, separately authenticated wallet-signing check**:

1. ETH_FORWARD: Ethereum ENS `jaywisdom.eth` forward resolution -> A380, observed at named chain/block/resolver and coin type.
2. ETH_REVERSE: Ethereum address A380 reverse -> `jaywisdom.eth`; verify same-snapshot forward-back loop.
3. BASE_FORWARD: Base `jaywisdom.base.eth` forward resolution -> A380, independently identifying chain/block/resolver.
4. BASE_REVERSE: Base A380 reverse -> `jaywisdom.base.eth`; verify same-snapshot forward-back loop.
5. FRESH_A380_SIGNATURE: newly issued, independently verified A380 `personal_sign`-compatible message using ERC-1271 `isValidSignature(bytes32,bytes)` on Base 8453, with exact contract address and current block reference. The signer’s wallet/credential must be existing and explicitly authorized by Jason.

Rules:
- Any **FAIL** => overall **FAIL** for the tested claim.
- All **PASS** => overall **PASS**, but only for the defined scoped claim; NOT legal identity, ENS registry ownership, custody of funds, or institutional authority.
- Otherwise => overall **UNKNOWN** (unproven). Missing/undetermined evidence is not FAIL by default.
- Current quad evidence: four separate readbacks UNKNOWN pending block+resolver+coin type verification. Historical A380 signature (2026-10-09T09:09:08.189Z) PASS **historically**, current signing UNKNOWN.
- A current wallet not equal to A380 can sign a **continuity receipt for itself** after review; such signature is NEVER substituted for the A380 signature. No re-binding, no asset redirects, no retroactive assertions.

## Wolfram verification: five synthetic edge cases (2026-11-07)
Test results:
- 4×PASS + A380 PASS -> PASS
- 4×UNKNOWN + A380 UNKNOWN -> UNKNOWN
- 3×PASS + 1×UNKNOWN + A380 PASS -> UNKNOWN
- ETH_REVERSE FAIL + others mixed -> FAIL
- 4×PASS + wrong-wallet signature FAIL -> FAIL

Wolfram results: 5/5 **mathematical gate tests PASS**. These are *logical tests only*, not evidence of a live name resolution or current cryptographic wallet access.

## Proposed signable receipt format
- Exact UTF-8 message using `CWAAAS_A380_QUAD_ONION_PROOF_INTENT_V1` + `chain_id=8453`, `wallet_address`, `name_refs`, `scope`, `evidence_bundle_sha256`, `nonce`, `issued_at`, `expires_at`, `page_origin`, `Base block number/hash`.
- **Nonce must be generated at signing time** from CSPRNG. Anchor to a recent Base block. Expiry check both before signature *and after return*; a prior PR #648 signer was quarantined for pre-sign-only expiry checking.
- Separate `address_returned` and `expected_A380`. Never let wrong wallet continue a transaction or portray a current-wallet signature as A380.
- Result fields: `signature_method=personal_sign`, `signing_address`, `owner_index_if_verified`, `verification_digest_type=EIP191`, `wallet_verification=ERC1271`, `verification_block`, `verification_result`.
- For a Coinbase Smart Wallet, the owner's ECDSA wrapper may require contract-specific *replay-safe* EIP-712 digest to recover the underlying owner. **Do not confuse EIP-191 message hash, replay-safe EIP-712 owner hash, Keccak-256 or SHA3-256.**
- Redact signature bytes and private challenge details from any public report when not necessary. No private key, recovery phrase, seed, passkey, OAuth token, 2FA code, or YubiKey secret is requested.
- The receipt can be frozen and exported as JSON for private replay. Zipping evidence is permitted only as a labelled DRAFT until all five gates pass; never call unsigned proof COMPLETE.

## Source/execution boundary
1. **GitHub / Computer Wisdom:** `wallet-control/jason-dual-path/index.html` already represents ONE SIGNATURE / TWO PATHS but itself states CONTROL HOLD, not independent verification. Use as reference only until security review. Do **not** reactivate quarantined `wallet-control/jaywisdom-base/index.html`.
2. **Google Drive:** private archive/continuity evidence, not a public dump of recovery credentials.
3. **Cloudflare:** current `jsonwisdom-wallet-connect` Worker points to A380 and Flywheel; origin/SDK routes differ from signed 2026-10-09 historical `https://jsonwisdom.github.io`. Do not infer credential control from matching strings.
4. **Wolfram:** deterministic hash and logic verification over declared, nonsecret input. Mathematical validation does not provide a signing credential.
5. **CI-FIRST / Computer Wisdom Replay:** read source/digest and evaluate five individually tagged gates. On unknowns emit missing evidence and blockers; do not manufacture pass/fail.
6. **Human:** a signature is a sensitive, user-authorized action. No automatic signing, passkey changes, merges, or DNS/payment mutation.

## Release decision
`DOCS_CONTRACT=PASS`
`WOLFRAM_QUAD_LOGIC=PASS`
`ALL_FOUR_LIVE_NAME_GATES=UNKNOWN`
`FRESH_A380_SIGNATURE=UNKNOWN`
`SIGNING_APP_SECURITY_REVIEW=UNKNOWN`
`WALLET_RESTORED=UNKNOWN`
`ZIP_FINALIZED=false`
`DEPLOYMENT_APPROVED=false`

Next: independently replay the four network name checks, review a separate *non-transaction* signer surface, then offer Jason one deliberate, understandable on-device signature that independently verifies under A380 if and only if his original credential is still accessible. If not, use the separate continuity lane without claiming wallet recovery.
