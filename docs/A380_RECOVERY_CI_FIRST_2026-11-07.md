# CI-FIRST — A380 Smart Wallet authentication-path replay (DRAFT)

**Date:** 2026-11-07. **Status:** REVIEW ONLY / NO LIVE DEPLOY / NO WALLET AUTHORITY.  
**Target:** `jaywisdom.base.eth` → `0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8`.  
**Goal:** Determine whether the original Base Account SDK route can select the existing A380 signing credential on iPhone or Windows. No signing, custody, or payment authorization.

## Time-ordered evidence (UTC is canonical; Minnesota local included)

| UTC | Minnesota local | Platform | Observation | CI |
|---|---|---|---|---|
| 2026-10-05T07:39:32Z | Oct 5, 02:39:32 CDT | GitHub | Wallet-control added with `@base-org/account@2.5.10` and `createBaseAccountSDK`. Commit `8de2525ddc0b084ee631391de0d8c11262b1fd51`. | PASS |
| 2026-10-09T09:09:08Z | Oct 9, 04:09:08 CDT | ChatGPT signed receipt / Base | Historical A380 `personal_sign` receipt accepted by ERC-1271; read-only PowerShell replay on 2026-11-07 also returned 0x1626ba7e at historical and latest blocks. Not proof of fresh current signing. | PASS |
| 2026-10-28T11:08:05Z | Oct 28, 06:08:05 CDT | GitHub | Commit `745211228e976b186adb636508864ad554f362d0` replaced original SDK provider with Coinbase injected extension. | PASS |
| 2026-10-28T11:20:17Z | Oct 28, 06:20:17 CDT | Cloudflare | `jsonwisdom-workdesk-auth-staging` Worker created; distinct WebAuthn security gate, not wallet signer. | PASS |
| 2026-11-01T21:02:44Z | Nov 1, 15:02:44 CST | GitHub | Commit `d75d3aebac2579fd7edba48f408afdfac8dab219` added `flywheel-connect/jaywisdom.js` targeting A380 but using injected browser wallet. | PASS |
| 2026-11-01T21:03:38Z | Nov 1, 15:03:38 CST | Cloudflare | `jsonwisdom-wallet-connect` last deployment; worker has injected provider, not Base Account SDK. | PASS |
| 2026-11-05 (precise occurrence not established) | CST | iPhone / Coinbase | User reported original Base smart-wallet sign-in stopped after authentication changes. Exact credential failure and causation UNKNOWN. | REPORTED |

## Live hosting cross-check

Cloudflare custom domains **enabled / production**:  
- `wallet.jsonwisdom.com` → Worker `jsonwisdom-wallet-connect`.  
- `auth.jsonwisdom.com` → Worker `jsonwisdom-workdesk-auth-staging`.

These bindings **do not** imply either service can retrieve a Coinbase passkey. The former is an injected wallet flow and includes a route for `/jaywisdom`; latter is separate Workdesk WebAuthn.

## Independent chain state

A380 owners at Base block `0x31f291f` and at latest:  
`OWNER_0 0xe13c4abd8e4d3caf5a84238e047e1b7e8632d180`  
`OWNER_1 0x9d8b34122fcda3bd6d84eff4b921e9f68e6b201c`.  
Snapshots match. No complete intermediate ownership-event audit yet. Historical signature still verifies; fresh access UNKNOWN.

## Wolfram SHA-256 check

Policy string `COINBASEKID_BASE_WALLET_CONTROL_V2|https://wallet.jsonwisdom.com|8453` hashes to  
`f09262a7cdc2a8dd05f80ed656604534efaba598f0d9a1b7016a60af6f1ec275` and matches `flywheel-connect/base-wallet-policy.v2.json`.  
**Boundary:** that policy authorizes a *different desktop signer* `0x0f7018fea1dc9ba32ae817d896211f72f1197ad8`; it is NOT A380 signing authority.

## Drive boundary

2026-10-09 `COMPUTERWISDOM Operator Signing Map` lists multiple unreviewed signing routes and requires independent security review before deployment. Two Drive `CoinbaseWalletBackups` folders inspected: one contains a referral text file; one a zero-byte file. Neither provides a verified A380 wallet recovery credential.

## Proposed recovery test (NOT EXECUTED)

The adjacent `wallet-control/A380_SDK_DIAGNOSTIC_CANDIDATE_2026-11-07.txt` is inert source text, **not an HTML page deployed anywhere**. It reproduces only the original 2.5.10 provider path, on the reviewed `wallet.jsonwisdom.com` origin and only after deliberate user interaction.

It requests `eth_accounts`, optionally `eth_requestAccounts` (user connection consent), and `eth_chainId`. It does not sign, send, change network or owners, export secrets, request PINs, or make payments. It rejects any wallet other than A380. **Cancel if Coinbase prompts to create a new wallet.**

### Release gates (NOT MET)

- Independent review of pinned remote SDK, SRI/integrity, Content Security Policy, origin and dependency safety.
- Demonstrate existing credential selection only, without new-wallet onboarding.
- Synthetic tests for wrong wallet, wrong network, cancellation, no provider, and no accidental signing.
- Explicit approval for any deployment or subsequent fresh proof-of-control signature.
- Keep quarantined `wallet-control/jaywisdom-base/index.html` unchanged under PR #649 security controls.

**No wallet changes or production changes approved by this draft.**

## Evidence sources
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/8de2525ddc0b084ee631391de0d8c11262b1fd51/wallet-control/index.html
- https://github.com/jsonwisdom/COMPUTERWISDOM/commit/745211228e976b186adb636508864ad554f362d0
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/flywheel-connect/jaywisdom.js
- https://github.com/jsonwisdom/COMPUTERWISDOM/blob/master/flywheel-connect/recovery-index.json
- https://github.com/jsonwisdom/COMPUTERWISDOM/pull/649
- https://docs.google.com/document/d/1YvHPZ3YesjgcG-P4P5kvIw7qi2PTrqfJ9UkdL8_uVmw/edit

## 2026-11-07 official Coinbase login documentation clarification

Official Coinbase Help (retrieved 2026-11-07):
- https://help.coinbase.com/en/wallet/other-topics/mobile-app-sign-in-discontinued — Cross-device app connections using an external desktop/mobile browser QR code are no longer supported. Stop the prior Windows-PC QR-to-iPhone loop; it cannot be used as evidence a specific credential fails.
- https://help.coinbase.com/en/wallet/getting-started/smart-wallet — Smart wallets are passkey-based, can be managed via wallet.coinbase.com, and **cannot** be accessed through the Coinbase exchange app or Wallet extension.
- https://help.coinbase.com/en-sg/wallet/getting-started/smart-wallet-passkeys — Smart-wallet login supports existing email credentials, passkeys, and any previously configured recovery method. Passkey deletion risks account access. Apple passkeys are distinguished by their creation dates; the credential controlling A380 remains UNKNOWN.

### Device/account credential ledger (observed in previous PowerShell and iPhone reviews)
- iPhone Safari currently shows `0x5727…9BfD` associated with an Apple passkey dated 2024-08-17. **Not A380.**
- Windows Chrome Google Password Manager credential dated 2025-01-24 selected `0x0dAC…40cD`. **Not A380.**
- Hardware YubiKey FIDO2 inventory: `demo.yubico.com` / `jaywisdom44`; `vercel.com` / `jsonwisdom`; `coinbase.com` / `jaywisdom44@gmail.com`. The Coinbase RP credential was observed but **has not demonstrated A380 signing**. The Yubico demo credential is unrelated to wallet custody.
- Apple Passwords inventory of eight `keys.coinbase.com` passkeys reviewed already. Creation dates alone cannot cryptographically prove which is tied to A380. **Do not repeat this inventory or delete credentials.**

### What the application-layer fix can and cannot prove

The proposed SDK diagnostic is **NOT a wallet recovery credential**. It only compares a returned address with A380 on Base chain 8453. Even PASS_CONNECTED_ADDRESS_MATCH would not prove fresh signing until a separately approved, fresh signing operation succeeds. No offchain Github/Drive/Cloudflare tools can substitute for existing signing credentials or reassign wallet owners.

**Safe next step:** independent SDK and domain review, synthetic-only tests in isolated/non-production environment, then user-approved connection to **existing** Smart Wallet via same-device browser, without resets, wallet creation, QR-device sign-in, or seed entry. Do not deploy the PR or alter the locked-down historical signing page merely to make the test clickable.

## 2026-11-07T18:07 CST+ — original proof rehydrated, SDK/origin candidate corrected

**Primary receipt:** `JAYWISDOM_BASE_WALLET_CONTROL_2026-10-09.json` (private ChatGPT Library; do not publish full historical signature with this draft). Fields observed:

- `created_at = 2026-10-09T09:09:08.189Z` (2026-10-09 04:09:08.189 CDT).
- `connected_address = 0xA380552a27b0a5a2874Ea7AA52CAC09f542002E8`.
- `wallet_provider = BASE_ACCOUNT_SDK_2_5_10`.
- `challenge.page_origin = https://jsonwisdom.github.io` **NOT** `https://wallet.jsonwisdom.com`.
- `verification.verification_method = ERC1271_IS_VALID_SIGNATURE` and `verification.verified=true`.
- `signed_message_sha256 = 0xb832a9ae64fdd673b8ed0a83164171e6f0279f30e60c595cdd5325d6c42ec625`. **Wolfram independently recomputed this exact SHA-256 from the signed message UTF-8 bytes: PASS.**
- No passkey credential ID, original login email, or device identification is included. Cannot infer them from the historical signature or hash.

The SDK code **in place on Oct 9** was GitHub commit `5f32f98b65352a247f57a2af0901480fdba5f8fb` (Oct 6 2026 00:27:41Z), not the original Oct 5 `8de2525` draft. Exact prior working settings:
- App: `Computer Wisdom Wallet Control`
- SDK: `@base-org/account@2.5.10` from pinned unpkg path
- Recorded SRI: `sha384-Jcaa5XJIs34lC6Co7Ye/mAuxCGLTEdUYQuIyl4UrwRduYb6mOmW7SUCOPX/jdsKV`
- Chain: 8453
- Account-selection API: `eth_requestAccounts`
- Original signing-site origin: `https://jsonwisdom.github.io`.

**Corrected the inert diagnostic** to pin that original site origin, app name, SDK URL, and recorded SRI. Remote library integrity has NOT been independently re-fetched and checked; code is not deployed, and no live wallet was queried.

### Coinbase Smart Wallet authentication and QR nuance

As of Nov 7, 2026, Coinbase's Base Account help states existing accounts can use email OTP, registered passkey, or recovery phrase (only if previously set up):
https://help.coinbase.com/en/wallet/getting-started/smart-wallet-passkeys

This same official documentation describes cross-device QR **passkey** authentication as a supported configuration for certain devices. Do not generalize another Coinbase-app's discontinued QR *connection method* into a blanket statement that all passkey QR authentication is unsupported. Distinguish:
- an existing Base Smart Wallet account's passkey authentication,
- an extension wallet or dapp cross-device login,
- Coinbase exchange or Prime authentication.

Original Oct 9 receipt does not identify whether the signer was reached through an Apple passkey, Google passkey, YubiKey, or email OTP. The credential remains **UNKNOWN**.

Coinbase official recovery doc https://help.coinbase.com/en-sg/wallet/getting-started/smart-wallet-recovery says a new recovery phrase can only be generated **while original passkey is accessible**. Therefore do not pretend that creating one now could recover A380, or recommend wallet reset/new account. Existing previously configured recovery method, if any, remains UNKNOWN.

### Supplementary Nov 5 security chronology — user-reported notice times (CST)

- Nov 4 09:24 CST — user-provided receipt for 1,000 USDC transfer to A380; this is a payment observation, not proof of current signing.
- Nov 5 11:41 CST — notice of passkey added to `computerwisdom408@gmail.com`.
- Nov 5 12:29/12:48 CST — notices of 2FA changes to `jaywisdom44@gmail.com`.

These timestamps are user-reported from earlier chats, not independently authenticated credential-to-wallet bindings, and do **not** prove YubiKey caused A380 access loss.

**Next executable recovery gate:** independent review of the Oct 6 pinned SDK against the draft; only then a separately authorized, same-origin browser test of an EXISTING account, with wrong-address fail closed. The test is address observation, not access restoration. No production deployment, wallet signature, transfer, on-chain owner update or passkey mutation authorized by this PR.

## Draft diagnostic static audit — 2026-11-07

**PASS (static checks only, not browser authentication):** 10/10 checks confirmed the separate `.txt` candidate pins the historically observed Oct 9 `https://jsonwisdom.github.io` origin, the original app name, recorded Oct 6 SDK SRI, A380 target, only `eth_accounts`, `eth_requestAccounts` and `eth_chainId`, wrong-account fail-closed, click-only initiation and no signing, on-chain writes, passkey mutation or network upload. These checks do **NOT** validate CDN bytes, CSP, browser behavior or current signer control.

- Draft file SHA-256 recalculated by Wolfram from full UTF-8 bytes: `a6156ae92d9c678c75152dfa38a996f4b3e16c49df15fcf1150c5f3bcebd9b14`.
- Old signed Oct 9 message SHA-256 independently rechecked: `b832a9ae64fdd673b8ed0a83164171e6f0279f30e60c595cdd5325d6c42ec625`.
- The recorded Oct 9 origin and Nov 1 custom domain **differ**. No claim of resolved login or recovery by this source-only work.
- Earlier Coinbase support transcript calls `jwisdom44` a passkey login in November; it does **not** map the Oct 9 A380 account to an individual credential ID.
- Next gate is runtime synthetic test + independent SDK security review. Do not merge, publish, or initiate new authentication on user's device from this file. 
