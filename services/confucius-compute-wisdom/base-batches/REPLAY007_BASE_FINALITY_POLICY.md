# REPLAY 007 — §5a Base finality / reorg policy

**Review candidate only · chain 8453 · NOT ACTIVE.** Witness/publication/export enrollment and x402 payments remain HOLD.

## Decision rule

Base distinguishes **unsafe**, **safe**, and **finalized** L2 blocks. A descendant-count alone is not L1-derived finality. Candidate operator threshold:

**N = 12 subsequent L2 blocks AND the observed block is included in an independently verified `finalized` L2 head**, with its *exact block hash*, correct Base chain ID and canonical L1-origin hash. N is an additional policy margin, **not** a Base protocol finality guarantee. Independent operator approval of N, the node sources and key custody is **PENDING**, so no production finality verdict may pass. Reference: [Base L2 derivation/forkchoice](https://docs.base.org/base-chain/specs/protocol/consensus/derivation).

At acceptance, record block height **and hash**, L1-origin height/hash, source identifier, observation time, root, and the independently signed witness attestation. Cross-check against an independently retrieved finalized view before changing status. Verify hashes and canonical origins, not just heights.

**Critical separation:** the root is an *off-chain* candidate. A finalized Base block can authenticate a reference block/time; **it cannot prove that this root was ever included onchain** without an independently verifiable inclusion commitment.

## Acceptance now, finality later

The existing witness signs `root`, `createdAtBlock`, `observedAtBlock` and `observedAt` inside a ~300-second acceptance window. Base finality may occur after that window.

1. Accept a valid independent witness promptly as **`OBSERVED_UNFINALIZED`**. Never backdate it.
2. Later record a separately authenticated **`FINALITY_REVIEW_PASSED`** decision once the proposed N **and** finalized-head/hash conditions pass. This later decision requires a reviewed addition; it is **not implemented** by current §5a code.
3. No witness, no approved threshold, no verified finalized view, or no authenticated block hash → **HOLD**. Existing `maximumBlockWindow: 12` constrains witness timing; it is **not** the finality policy.

## Reorg and provenance response

- Before finalization: disagreeing RPCs, block-hash/parent change, L1-origin reorg or node outage → `BLOCK_REFERENCE_UNFINALIZED`; quarantine root and refuse export. Append a signed incident, retaining original evidence.
- After a prior finality decision: any authenticated contradictory evidence → `DISPUTED`, freeze future exports, preserve both histories and require an independent incident reviewer. Never erase the nonce ledger or silently replace a witness record.
- New canonical reference or replacement root needs fresh attribution, witness and nonces.

**Creator attribution is still OPEN.** `bundle.creator` is currently a claimed database/input address. Before activation, require a **creator-signed EIP-712 statement** over root, creator address, origin, chain 8453, purpose, policy version, issued time and unique nonce; verify against a versioned creator authorization policy. An unsigned DB column is insufficient.

**Witness independence is an existing tested assertion** (`W3`: witness equals batch signer → `WITNESS_IS_BATCH_SIGNER`; `W4`: witness equals creator → `WITNESS_IS_CREATOR`). Enroll a dedicated real-world witness key only by independently authenticated out-of-band publication. One witness key means a **single-witness trust root**; use separate custody, revocation/rotation and incident records, with threshold custody a v2 option.

## Activation tests (future)

Unsafe/safe-only block, fewer than N descendants, missing finalized hash, reorg, untrusted witness, unsigned creator attribution or expired acceptance-time witness → **HOLD**. All finality attestations must include hashes and trusted source evidence. Multi-host SQLite replay protection remains NOT established.

**Code status:** §5a cryptographic tests PASS; finality source, creator signature, approved N, independent key enrollment and operational activation OPEN. No payment or publication authority.
