# REPLAY 007 — §5a Base finality, reorg and creator provenance policy

**Status:** Candidate policy for independent security review. **Not activated.** Base mainnet chain ID 8453 only. Payment, public proof release and production witness enrollment: **HOLD**.

## Exact distinction: acceptance vs finality

The current signed `AcceptanceWitness` records an off-chain root and claimed `createdAtBlock` / `observedAtBlock`. The code checks `observedAtBlock ∈ [createdAtBlock, createdAtBlock + 12]` and a time window near SQLite `reserved_at`. It does **not** establish that the block was canonical/finalized, that the creator signed the root, or that the root was committed onchain. **A Base finalized block can be used as a reference clock; it cannot prove that an entirely off-chain Merkle root was published on Base.**

Base uses L2 **unsafe**, **safe**, and **finalized** forkchoice states. Unsafe sequencer visibility and an arbitrary number of L2 descendants do not, by themselves, equal L1-derived finality. Base derivation and L1 reorg handling are described in https://docs.base.org/base-chain/specs/protocol/consensus/derivation .

## Proposed activation threshold (not approved)

- **N = 12 L2 descendant blocks** beyond the exact observed block **AND** the observed block must be at or below the independently read **`finalized` L2 head** with the same immutable block hash and correct chain ID 8453. N=12 is an additional policy margin, **not a claim** that 12 confirmations produce Base/L1 finality; the `finalized` requirement controls.
- Gather block number **and hash** and corresponding L1 origin number/hash at acceptance from a trusted chain source. Compare against an independently retrieved canonical/finalized view before any status is upgraded. Keep the source, query time and header hashes in a signed, versioned **finality decision**. A claimed height alone fails.
- The existing witness signature must be issued near acceptance (current maximum lag 300 seconds). Base L2 finality may take longer than that. **Do not wait for finality and backdate the existing witness.** Treat the acceptance witness as `OBSERVED_UNFINALIZED`, and add a **separate later finalized-chain review** before claiming `FINALITY_REVIEW_PASSED`. This requires a future code/schema review; it is **not implemented** by the current witness module.
- Version the approved N and finality source in an operator-signed policy. Until an independently authorized operator approves sources, threshold and custody, `FINALITY_REVIEW_PASSED = false` and publication/export activation stay HOLD.

## Reorg and invalid-reference response

1. **Before finality:** hash mismatch, head regression, RPC disagreement, L1 origin reorg or unavailable trusted source → **HOLD / BLOCK_REFERENCE_UNFINALIZED**. No export or publication. Append a signed incident/quarantine record; never silently replace previously signed root/block evidence.
2. **After a previously reported finality:** unexpected conflicting finality evidence → freeze new exports, mark the prior decision **DISPUTED**, preserve both histories, and require independent incident review. Do not delete consumed nonces or rewrite existing witness signatures.
3. A new canonical block or new candidate root requires **fresh** signed attribution and independent observation; no signature or nonce reuse across the replacement.

## Creator provenance and signer independence

- Creator identity is **OPEN**: current `bundle.creator` is a claimed address column. Activation requires a separate **creator EIP-712 signature** committing to `bundle_root`, origin, chain 8453, creator identity, purpose, policy version, issued time and unique nonce. Verify the recovered address against a versioned creator authorization policy; no DB-column-only attribution.
- Witness is **not** the creator or any batch signer (existing test `W3`). A dedicated witness key must be enrolled through an out-of-band authenticated public-key record, with an independent custodian, rotation, compromise/revocation response and audit log. A single key is a **single-witness trust root**, not threshold security; threshold custody is a possible v2 mitigation.
- An attestation never authorizes payments, identity claims, or publication. Preserve separately: **(a) cryptographic proof, (b) acceptance observation, (c) finalized-chain review, (d) verified creator attribution**.

## Acceptance assertions for later code/operations

`WITNESS_IS_BATCH_SIGNER` / `WITNESS_IS_CREATOR` → HOLD; a block-number-only claim or unsafe/safe-only block → HOLD; fewer than N descendants → HOLD; no finalized-head/hash agreement → HOLD; L1 reorg or hash conflict → HOLD; missing signed creator attribution → HOLD; witness signed after the 300-second acceptance window → HOLD (not backdated); finality review not completed → no export/publication.

**Deployment restriction:** §4 SQLite remains one authoritative local writer, not a multi-replica nonce service. This document changes no runtime. The candidate finality policy and creator identity chain require approval before activation.
