# CI-FIRST — Dual Audit / Dual Recovery / Quad Onion — jaywisdom.eth

**Date:** 2026-11-07 · **State:** DRAFT, READ-ONLY FIRST PUSH · **Authority:** FALSE

This plan audits **`jaywisdom.eth` on Ethereum mainnet**, not `jaywisdom.base.eth` on Base. Same naming family does **not** prove shared registration, ownership, signing access, or permissions.

## Forward A: ENS onchain (UNKNOWN pending verification)

Collect block-anchored proof of current ENSv1/ENSv2 registration and current owner/manager, expiry, resolver, and resolved payment address. `owner` / `manager` / `resolver.addr` / wallet's reverse primary name are **different records**. Confirm the correct ENS version and contract path before reading; cached UI evidence is insufficient.

## Forward B: Existing Windows PC wallet

Known historical PC Wallet2/Address2 `0x65891F97db01C8fC9F76f4DFE65Bd44F8261f1B0` successfully replays a preexisting EIP-191 signed message from GitHub PR #745 in independent Wolfram. That proves the signer for that exact historical message, **not today's connected session** or ENS control. A separate Cloudflare desktop app expects `0x0f7018fea1dc9ba32ae817d896211f72f1197ad8` for its **different EIP-712 v2 policy**. Do not infer equivalence.

## Backward A: Prior identity evidence

`receipts/wallet_binding_v2.md` is `PREPARED_NOT_SIGNED` and claims `0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8` as historical identity controller; that is **not** independent onchain owner proof. Its separate EAS/browser signer and Sepolia receipt do not grant mainnet ENS authority.

## Backward B: Independent byte recovery

Use immutable GitHub commit/blob anchors, a private Google Drive evidence archive, and the isolated Cloudflare KV recovery archive. Recompute SHA-256 + Git blob ID on any restored source. These archives preserve **code and public proof bytes only**; they cannot recover a lost private key.

## CI FIRST contract

- `PASS`: Namehash deterministic mathematics and address distinction (Wolfram), previous Wallet2 EIP-191 historical message verification.
- `UNKNOWN`: live ENS owner/manager, expiry, current connected Windows wallet, present signing capability, name recovery authorization.
- `FAIL`: None inferred merely from unavailable data.
- No name transfer, wallet switch/import/reset, signature, wallet secrets, deployment, funds, GitHub merge, or authority promotion.

**Next user-observed evidence:** a fresh screenshot of the existing Coinbase Wallet extension in Windows Chrome showing the selected address. Only after read-only owner verification and a fresh, explicitly approved signing proof may a recovery attestation be considered.

**Automated test:** Evaluate `CI_FIRST_JAYWISDOM_ETH_QUAD_ONION_V1.wl` in Wolfram Language; it does not make network calls. `CI_FIRST_JAYWISDOM_ETH_QUAD_ONION_V1.json` is the durable input/evidence contract.
