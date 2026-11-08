# CI-FIRST — A380 Wallet Recovery: Documents Before Code
**Date:** 2026-11-07 (America/Chicago)  
**Status:** DOCUMENTATION-ONLY / DRAFT / NOT AUTHORIZED TO DEPLOY OR SIGN  
**Related:** PR #743; prior signer containment PR #649; Coinbase support case #27829182.  
**Identity target:** `jaywisdom.base.eth` = `0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8` on Base 8453.

## 0. Non-negotiable recovery goal
Recover *current*, user-controlled signing access to the existing A380 Smart Wallet. The wrong wallets `0x5727…9BfD` (iPhone), `0x0dAC…40cD` (Windows passkey) and `0x65891F…61f1B0` (Chrome extension) are not substitutes. Restoration requires a fresh A380 signature independently verified on Base. Reading an address, listing credentials, source-code audit or seeing a balance is **not** recovery.

## 1. Evidence already established
| Date / source | Verification |
|---|---|
| 2026-10-09T09:09:08.189Z original signed JSON | A380 signature verified by ERC-1271; `BASE_ACCOUNT_SDK_2_5_10`; `page_origin=https://jsonwisdom.github.io`; wallet address matched. |
| 2026-10-06T00:27:41Z GitHub `5f32f98...` | Original `wallet-control/index.html` used Base Account SDK 2.5.10, app name `Computer Wisdom Wallet Control`, pinned CDN SRI. |
| 2026-10-28T11:08:05Z GitHub `7452112...` | Application connection changed to injected Coinbase Wallet extension. **This is not evidence of a change to wallet owner keys.** |
| 2026-11-01T21:03:38Z Cloudflare | Last `jsonwisdom-wallet-connect` Worker deployment. Custom domain `wallet.jsonwisdom.com` routes there; that Worker uses injected provider, not original Base SDK. |
| 2026-11-05T17:41:08Z Gmail `computerwisdom408` | Coinbase account passkey added. |
| 2026-11-05T21:46:54Z and 21:49:02Z Gmail `jaywisdom44` | Coinbase account passkey removed then added. **Not linked by message to an A380 WebAuthn credential ID.** |
| 2026-11-07 prior self-contained PowerShell on Base | Historical and latest owner snapshots agree: `owner_0=0xe13c4abd8e4d3caf5a84238e047e1b7e8632d180`, `owner_1=0x9d8b34122fcda3bd6d84eff4b921e9f68e6b201c`. Signature historical and latest ERC-1271 `0x1626ba7e`. **Intermediate events not exhaustively checked.** |
| Nov 7 YubiKey FIDO inventory | Separate RP-ID credentials `demo.yubico.com`, `vercel.com`, `coinbase.com`; neither user ID nor `coinbase.com` proves control of A380. |
| Nov 7 iPhone and Windows passkey review | Eight Apple `keys.coinbase.com` passkeys inspected; a known iPhone credential returned wrong `0x5727…9BfD` and Windows credential returned wrong `0x0dAC…40cD`. Do NOT repeat inventory or guess passkey by date. |

## 2. Unanswered questions — evidence requests (not speculation)
A. What exact public key and signer scheme do A380 owner slots represent? Are both EOAs or wrapped WebAuthn owners? Obtain verified ABI and on-chain owner event history.  
B. Which *already-existing* credential or wallet account maps to either A380 owner? This requires provider-side mapping or a fresh safe signature, **not** inference from passkey names.  
C. Which local device/browser, email identity and RP ID were used by the original Oct 9 SDK session? Original JSON contains **no** passkey ID/device/email; locate contemporaneous authentication logs only if accessible lawfully.  
D. What changed on Nov 5? Separate Coinbase exchange 2FA notifications from Base Smart Wallet passkey events. The email headers demonstrate passkey changes, **not** that they caused wallet access loss.  
E. Does an old Chrome extension or account provide access to `owner_0` or `owner_1`? Verify exact addresses and session permissions **without** imports, resets, key exports or signing.

## 3. CI contracts / PASS–FAIL–UNKNOWN
1. **PROVENANCE:** Every factual record carries source, UTC timestamp, platform, immutable identifier and SHA-256 when bytes are available; otherwise UNKNOWN, not fabricated.
2. **AUTHENTICATION:** Exact smart-wallet address A380 must be returned on Base chain 8453. A wrong address = FAIL; account prompt / canceled = UNKNOWN; only a returned matching address = ADDRESS_MATCH_PASS (not signing proof).
3. **SIGNING:** Only after documented independent security review and specific user approval, a fresh non-transaction signature must verify under A380 via ERC-1271 at current block = PASS. Anything else = UNKNOWN/FAIL.
4. **NO LOSS:** Never delete or rename passkeys, reset YubiKey, sign out existing sessions, import/replace wallet, move funds, modify owner keys, change DNS/Cloudflare/GitHub production or issue token approvals without explicit authorization.
5. **INDEPENDENT REVIEW:** Existing PR #649 quarantine stands; new SDK dependencies, SRI, CSP, origin, and user-consent UX must be independently reviewed before any deploy.
6. **RUNTIME:** Test synthetic right-wallet, wrong-wallet, refusal, wrong chain, wrong origin, and no-provider cases before interacting with an account. A passing test harness ≠ live recovery.
7. **DEVICE:** Provide one screenshot-grounded action only when current UI screenshot is available and user requests interaction. Do not send user back into already-reviewed iPhone settings or ask for the eight passkeys again.

## 4. Recovery decision tree (documentation, not active instructions)
- Existing credential **cryptographically demonstrated** to control owner and A380 => propose fresh user-approved local signing test.
- Provider returns a different wallet => stop; compare signer/address mapping without modifying sessions.
- Existing credential missing => request Coinbase Smart Wallet account-specific recovery evidence from case #27829182; do not assume a seed phrase or a replacement passkey can recover it.
- Verification blocked => keep UNKNOWN, preserve original bytes and audit, no production deployment.

## 5. Next work items IN ORDER
**First:** document exact owner type, logs/metadata, passkey RP-ID mapping and time-window from primary records.  
**Second:** independent review of reconstructed Oct 6 SDK code against Oct 9 signed receipt, including original `jsonwisdom.github.io` origin.  
**Third:** synthetic-only connection-path tests.  
**Fourth:** with explicit user approval, request a *current* existing-account connection from the correct origin and validate the full address.  
**Fifth:** a separately approved fresh A380 signature; only then propose site/GitHub changes to restore the attestation workflow.

### Release gate
`DOCUMENTS_APPROVED=false`  
`AUTH_RECOVERED=false`  
`FRESH_A380_SIGNATURE=false`  
`DEPLOYMENT_APPROVED=false`  
`WALLET_MUTATION_AUTHORIZED=false`

**CI-FIRST conclusion:** We have a verified historic A380 signature and a source-code drift; we do **not** have a verified surviving signer binding. Document that distinction before changing code.
