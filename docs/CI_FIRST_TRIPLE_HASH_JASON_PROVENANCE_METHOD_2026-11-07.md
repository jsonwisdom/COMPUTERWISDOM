# CI-FIRST · Triple-Hash Provenance Toolbox — Jason Reference Model
Date: 2026-11-07 · Type: DOCUMENTATION / PROPOSAL · Status: PASS for reference vectors, UNKNOWN for live wallet access

## Governing question
For every claim, **What does this prove about Jason's particular system, from which bytes, on which platform, at what UTC time?** Use the user-directed identity anchor **Jason Wisdom / jaywisdom.base.eth / A380** to organize discovery. **Jason is the denominator for the investigation, NOT a cryptographic key or authority claim.**

A user name, ENS, GitHub namespace, domain, receipt destination or payment address is a *search anchor*, not wallet-signing evidence. All connections are typed and require a dated proof.

## Search rules by system
1. **GitHub**: query Jason's exact ENS, lowercased full A380, owner addresses and related file paths across repos, then fetch the exact blob/ref. Preserve repository, path, commit SHA, GitHub blob SHA and commit UTC. Do not rely solely on indexed code search: inspect the repo Git tree and likely files when an indexed query gives zero results.
2. **Cloudflare**: query Worker list, deployments, custom-domain bindings, routes, and current script content. Search exact A380 and owner addresses independently. Link service to source only through an independently corroborated deployment artifact or exact bytes. A matching string does not establish wallet control.
3. **Google Drive and ChatGPT records**: search receipts/signed JSON and logs by date, original bytes and actual signing origin; preserve exact timestamp and source. Never publish the original private signature or passkey identifiers into public documentation.
4. **Wolfram**: ask explicit, self-contained math questions with exact algorithm, input encoding, byte sequence, expected test vector, domain separator, chain ID and verifier when applicable. Recompute rather than assume. Wolfram is an independent mathematical check, not a custody provider.
5. **Base blockchain**: distinguish named wallet/contract, payment recipient, on-chain owner, signature index, and live signer capability. Historical ERC-1271 verification is not current credential possession.

## Three hashing algorithms — NOT interchangeable

Canonical test vector: UTF-8 bytes of `abc`, hexadecimal `616263`.

| Algorithm | Verified digest (hex, no 0x) |
|---|---|
| SHA-256 | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` |
| SHA3-256 (NIST FIPS 202) | `3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532` |
| Keccak-256 (Ethereum) | `4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45` |

Wolfram direct evaluation confirmed all three; **PASS: different results**. Reference: NIST FIPS 202 https://csrc.nist.gov/pubs/fips/202/final and EIP-712 https://eips.ethereum.org/EIPS/eip-712.

- Use SHA-256 for forensic source-file digests, declared receipt SHA-256, manifests/replay where the schema specifies SHA-256.
- Use **Keccak-256** for Ethereum addresses, ABI selectors, typed-data / replay-safe EIP-712 hashes. **Never replace with SHA3-256.**
- Use SHA3-256 only when the recorded protocol specifically requires the NIST SHA3-256 algorithm or as a separately labeled independent diagnostic.
- Track `algorithm`, `input_encoding`, `input_bytes_digest`, `prefix_and_domain`, `expected_digest`, `actual_digest`, `source`, `observed_at_utc`, `verdict`.
- Numeric `0x` display and byte order must be treated explicitly, never hashed as literal text unless declared.

## A380 forensic case study — typed links, not a collapsed narrative

A. The 2026-10-09 signed receipt from private user records connects **A380** on Base 8453 via Base Account SDK 2.5.10 at `https://jsonwisdom.github.io`. ERC-1271 PASS for a historical challenge. It does not include a passkey ID, device or login email.

B. Receipt signature decoded as an ABI wrapper with **ownerIndex 0**, then 65-byte Ethereum ECDSA signature. Ethereum's Coinbase Smart Wallet replay-safe EIP-712 digest (NOT the raw personal-sign EIP-191 digest) recovers `owner_0 = 0xe13c4abd8e4d3caf5a84238e047e1b7e8632d180`. Replay-safe hash observed in arithmetic check: `0xa59cdc5f98db2518ff6b622c6b05dc6b4180019d057d4cc95e938992c3caa52e`. **PASS historical owner index and recovered owner address; credential identity UNKNOWN.** Original signature bytes remain private.

C. Coinbase Smart Wallet `owner_1 = 0x9d8b34122fcda3bd6d84eff4b921e9f68e6b201c` remained an on-chain owner in checked snapshots, but no signature by owner_1 has been evidenced.

D. `jsonwisdom/flywheel-of-wisdom`: `README.md`, `STATUS.json`, `server.ts`, `src/payment/payment-evidence.ts`, and `.env.example` use A380 as `pay_to`/recipient. **PASS payment destination configuration. UNKNOWN wallet signing authority and actual payment settlement.** SDK/app checkout and x402 are not evidence of access to A380's owner key.

E. Cloudflare `jsonwisdom-wallet-connect` current source contains A380, `flywheel`, `x402`, and `eth_requestAccounts`; it does NOT contain owner_0, owner_1 or `createBaseAccountSDK`. **PASS string linkage only; actual credential recovery remains UNKNOWN.** `cwaas-knowledge-recovery` references flywheel but contains no A380 or owner addresses. There is no script named flywheel/x402 among the 24 listed Workers.

F. Different iPhone, Windows and YubiKey credentials have been observed, but no verified surviving credential mapping to owner_0 or owner_1. **UNKNOWN and do not guess**.

## Mandatory evidence-edge types

| Left | Right | Allowed link type |
|---|---|---|
| GitHub repo/file | Cloudflare Worker | code deployed IF version/content match, otherwise STRING_REF_ONLY |
| Cloudflare Worker | A380 | target/recipient reference; NOT signing authority |
| Flywheel x402 config | A380 | payment destination; NOT private-key control |
| A380 smart contract | owner_0 | on-chain owner slot and historically verified signature |
| owner_0 | Apple/Google/YubiKey credential | UNKNOWN until provable service mapping or fresh verified signature |
| Source JSON | hash | PASS only for exact bytes + declared algorithm |
| Name/ENS | person/wallet control | identity reference, authority UNKNOWN |

## CI release gates
- PASS, FAIL, UNKNOWN only, with timestamps and source refs; no automatic conversion of UNKNOWN to PASS.
- DOCUMENTS FIRST. No new login tool, code deployment, wallet creation/import/reset, passkey change, signing, transfers, credential export, DNS change or production mutation from this protocol.
- Current recovery success test: a **new, separately user-approved** signature verifies for A380 using an existing credential. This has **NOT** been achieved.
- Historical/source proof may be mathematically sound without being a wallet recovery path.

## Primary locators
- https://github.com/jsonwisdom/flywheel-of-wisdom/blob/main/server.ts
- https://github.com/jsonwisdom/flywheel-of-wisdom/blob/main/src/payment/payment-evidence.ts
- https://github.com/jsonwisdom/COMPUTERWISDOM/pull/743
- https://github.com/coinbase/smart-wallet
- https://eips.ethereum.org/EIPS/eip-712
- https://csrc.nist.gov/pubs/fips/202/final

**Memory/search doctrine:** Hold Jason as investigation reference, never as a cryptographic shortcut. Search both exact names and bytes across GitHub + Cloudflare + original receipts, then have Wolfram independently verify the exact math. Preserve uncertainty and provenance, not narrative.
