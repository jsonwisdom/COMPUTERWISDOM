# CI-FIRST — A380 Quad Onion / Dual-Forward-Dual-Reverse Replay
Date: 2026-11-07 · Status: DOCUMENTED + RULE REPLAY PASS / LIVE NAME CONTROLS UNKNOWN
Authority: FALSE · No wallet control recovered · No deployment · No sign or transaction requested.

## Jason's correction
"Two forwards, two backs." Track **jaywisdom.eth** and **jaywisdom.base.eth** as independent identity rails, not interchangeable names, and preserve *which step was ahead in GitHub* rather than flattening both into a static A380 pointer.

Do not conflate the general Quad Onion four-layer reasoning architecture with this specific **dual-name 2×2 proof application**. The architecture's own doctrine requires independent source edges, continuity, receipt, and authority boundaries. Historical name lookup is an observation, not an owner/control certificate.

## Four explicitly separate tests
| Edge | Network & question | Verdict without primary readback |
|---|---|---|
| ETH_FORWARD | Ethereum ENS `jaywisdom.eth` resolves to WHICH address, with which resolver/coin type at which block/time? | UNKNOWN |
| ETH_REVERSE | Starting from A380 address, does an Ethereum ENS reverse record name `jaywisdom.eth`, and does the forward-back check agree at same snapshot? | UNKNOWN |
| BASE_FORWARD | Base/Basename `jaywisdom.base.eth` resolves to WHICH address, which onchain/offchain resolver and at which block/time? | UNKNOWN |
| BASE_REVERSE | Starting from A380, does Base's independent reverse name identify `jaywisdom.base.eth`, and does its forward-back check agree? | UNKNOWN |

A named label may have been observed resolving to A380 in a prior Blockscout readback logged by Jason, but it lacks independent current chain/coinType-resolved evidence; **do not set four green checks**. Different network primary names must not substitute for each other.

## Evidence already examined (source-specific)
1. GitHub `wallet-control/jason-dual-path/index.html` says "ONE SIGNATURE. TWO PATHS", names BASE/BNS and ETH/ENS independently, requires separate review and marks both CONTROL HOLD; signature is a candidate, not verified proof of registry/manager control.
2. GitHub `docs/jaywisdom/JAYWISDOM_VELOCITY_ARCS_V0_1.md`: identity rail = `jaywisdom.eth` (human explanation), execution rail = `jaywisdom.base.eth` (structured data, payment, receipts, RePlay).
3. GitHub `receipts/wallet_binding_v2.md`: name labels + A380 controller are DECLARED with `PREPARED_NOT_SIGNED`, `SHOW_WALLET_PROOF=PENDING`.
4. Google Drive `COMPUTERWISDOM — Living Sync Ledger — jaywisdom.eth ↔ jaywisdom.base.eth` (2026-10-14 append) explicitly asks for independent ENS and Basename forward lookups, *separate* reverse primary-record checks with coinType and chain, registry owner/manager, and chain receipt. Screenshots not proof of finality.
5. Google Drive `JASON QUAD ONION CLAIM V0 — First Public Claim Run`: an onion layer may feed the next but never proves it; experience/continuity/receipts/authority boundaries remain separate. `APPLE_BLOSSOM_QUAD_ONION_LOCKSET_V0` documents replay procedure hash, source bytes, and nondestructive corrections.
6. Google Drive `Jay Dual Onion Daily — v0.1 — 2026-08-18`: record/proof onion and power/authority onion stay independent; exact source-to-replay continuity.
7. Historical Oct 9 09:09:08Z signed A380 proof matches `wallet-control/jaywisdom-base/index.html` from PR #648 merged at Oct 9 09:07:20Z (exact receipt schema `CWAAS_BASENAME_WALLET_CONTROL_PROOF_V1`; appName `JayWisdom Wallet Proof`; pinned SDK 2.5.10). Verified ECDSA ownerIndex0 replay-safe hash recovers `0xe13c4abd8e4d3caf5a84238e047e1b7e8632d180`. This proves a **historic wallet signature**; does not prove name-registry owner/manager, surviving device credential, or both reverses.
8. Oct 9 09:31Z GitHub quarantined alternate page, Oct 9 11:54Z PR #649 merged lockdown. Preserve original source; never reenable quarantined signer without independent review.
9. GitHub flywheel payment rail and Cloudflare wallet Worker contain A380 destination references. Those are *purpose/evidence edges*, not authority or cryptographic wallet control.

## Model-level CI-FIRST replay
Wolfram evaluated four independent Boolean gates using four synthetic cases. Expected outcomes: ALL 4 TRUE = PASS; any unproven edge = UNKNOWN, NEVER global PASS. 4/4 model tests passed, no false promotion.

A mathematical model **does not mean** the ENS/Basename reverse records have been read live. Do not claim full Quad Onion production replay PASS. Each edge must get block/network/source/digest/UTC and a reproducible API/readback before status changes.

## Two controlled exit paths
**Recovery:** identify current existing signer credential controlling owner0 (or owner1) and obtain a new, separately approved A380 ERC-1271-valid signature. Then restore the original attestation UI without changing wallet ownership.

**Continuity:** if A380 cannot currently sign, allow Jason to publish *new, clearly independent* attestations with his currently accessible wallet and verified new signer address, using explicit new wallet metadata and name binding only after independent name-control checks. Never imply retroactive A380 signatures, redirect assets, impersonate A380, merge registry identities, or silently rebind ENS/Basename/receipts.

The historical A380 ledger and its Flywheel payment destination remain preserved, not automatically migrated. Redirection of new payment routes would require separate explicit instruction and downstream proofs.

## CI-FIRST next gates
- PASS: design/proof separation, Oct 9 historic A380 owner0 signature, source path identity, Wolfram 2×2 mock truth-table.
- UNKNOWN: current ETH_FORWARD / ETH_REVERSE / BASE_FORWARD / BASE_REVERSE, full registry control, current A380 credential control, restoration.
- FAIL if wrong-wallet address is presented as A380 or a model-only replay is reported as live.
- DOCUMENTS BEFORE CODE; draft PR only. No Grok, bot authorizations, or destructive recovery attempts.

Primary URLs:
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/wallet-control/jason-dual-path/index.html
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/docs/jaywisdom/JAYWISDOM_VELOCITY_ARCS_V0_1.md
- https://github.com/jsonwisdom/COMPUTERWISDOM/commit/6fc04b3ac94a75caccdd020bfae4282e740d075f
- https://github.com/jsonwisdom/COMPUTERWISDOM/pull/649
- https://docs.google.com/document/d/1tePBcJmEFE-uSQIkeDXIsyNCxNCH6LFrO3V9NiOzR7c/edit
