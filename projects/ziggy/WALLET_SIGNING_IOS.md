# Ziggy v0.1 — iPhone Wallet Signing Guide

Verified against official Coinbase / Base documentation on 2026-08-14.

## What failed in signer v0.1

Signer v0.1 depended only on an injected EIP-1193 provider (`window.ethereum`).

Opening that page inside ChatGPT's in-app browser or ordinary Safari could therefore produce:

`No injected EVM wallet provider found`

That result means only:

`INJECTED_PROVIDER_NOT_PRESENT`

It is not proof of a wallet failure, chain failure, or attestation failure.

## Current signer — v0.2

Use:

`https://jsonwisdom.github.io/COMPUTERWISDOM/projects/ziggy/sign-v0.2.html`

Signer v0.2 uses two explicit provider paths:

1. If an injected EIP-1193 provider is present, use it.
2. Otherwise, create an EIP-1193 provider using the official Base Account SDK browser build.

The browser SDK is pinned in the page to:

`@base-org/account@2.5.7`

Official Base documentation supports loading the Base Account SDK directly in plain HTML through a CDN and obtaining an EIP-1193 provider with `createBaseAccountSDK(...).getProvider()`.

Official references:
- https://docs.base.org/base-account/quickstart/web
- https://docs.base.org/base-account/reference/core/createBaseAccount
- https://docs.base.org/base-account/reference/core/provider-rpc-methods/personal_sign

## What to do on iPhone now

1. Open the v0.2 signer URL above.
2. Tap **1 — CONNECT WALLET**.
3. Ziggy selects the provider path:
   - `INJECTED_EIP1193`, or
   - `BASE_ACCOUNT_SDK_2.5.7`.
4. Continue only after a real wallet/account address is displayed.
5. Tap **2 — USE BASE SEPOLIA** if the page is not already on chain ID `84532`.
6. Read and check the signature boundary acknowledgement.
7. Tap **3 — SIGN RELEASE RECEIPT**.
8. Approve only a **message signature**. Do not approve a transaction prompt for this step.
9. Download the JSON receipt.

If the Base Account SDK popup/handoff is blocked by the browser, preserve that exact error. Do not fall back to pretending a signature exists.

## COMPUTERWISDOM identity must remain explicit

GitHub is hosting/transport. Ziggy's repository/system identity remains:

`jsonwisdom/COMPUTERWISDOM`

The signer records that exact repository string in the signed message and receipt.

## Address claims

User-supplied claims currently preserved:

- `0x73ad550dcb47d254a5b3c335ae39d8999c42ff12`
- `0xa380552a27b0a5a2874ea7aa52cac09f542002e8`

Both remain:

`USER_SUPPLIED / UNVERIFIED / UNASSIGNED`

Signer v0.2 compares the connected address with these claims but does not treat a connection alone as proof of ownership. The receipt records match/mismatch explicitly.

## Base Sepolia

Ziggy v0.1 still targets Base Sepolia:

- chain ID: `84532`
- hex chain ID: `0x14a34`

Official reference:
- https://docs.base.org/base-chain/quickstart/connecting-to-base

## Signature boundary

Base Account's provider supports `personal_sign`. Ziggy v0.2 uses it only for the bounded release receipt.

The page does not call `eth_sendTransaction`, does not submit EAS, and does not spend gas.

After capture, the receipt states:

`SIGNATURE_CAPTURED_NOT_ATTESTED`

and independently records:

`signature_verification_state = NOT_PERFORMED`

until verification is actually performed.

## Product boundary

The Coinbase trading app and the Base app are different products. A screen showing market/trading navigation such as **Spot**, **Futures**, **Stocks**, **Portfolio**, or **Orders** is not evidence that an injected EVM provider exists.

Do not invent UI tap paths through a changing Coinbase interface. The v0.2 signer is designed so the web page itself owns the provider fallback instead of sending the human around the same loop.

## State doctrine

`PUBLISHED ≠ PRESERVED ≠ CONNECTED ≠ SIGNED ≠ ATTESTED`

A supplied address is not proof of control. A connected address is not yet a verified signature. A signature is not a transaction. A transaction is not an attestation until independently verified.

`authority_created=false`
