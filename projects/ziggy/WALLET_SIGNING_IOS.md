# Ziggy v0.1 — iPhone Wallet Signing Guide

Verified against official Coinbase / Base documentation on 2026-08-14.

## First: identify the app

The **Coinbase trading app** and the **Base app** are different products.

If the screen shows market/trading navigation such as **Spot**, **Futures**, **Stocks**, **Portfolio**, or **Orders**, do not treat that screen as the Base app explorer. Coinbase documents that a Coinbase primary balance cannot be used to access dapps.

Official source:
- https://help.coinbase.com/en/dapps/getting-started/comparing-coinbase-wallets
- https://help.coinbase.com/en/wallet/getting-started/what-is-coinbase-wallet

## Current Base app route on iPhone

Coinbase's current Base help says to connect to an app through the **Base app explorer**:

1. Open the **Base app** on the iPhone.
2. Open **Apps / app explorer**.
3. Manually enter the Ziggy signer URL in the explorer address field:
   `https://jsonwisdom.github.io/COMPUTERWISDOM/projects/ziggy/sign-v0.1.html`
4. Load the page.
5. Tap **1 — CONNECT WALLET**.
6. Continue only if the page reports a wallet provider and the wallet/account shown is the one the human intends to use.

Official source:
- https://help.coinbase.com/en-gb/wallet/other-topics/mobile-app-sign-in-discontinued

## Base Sepolia

Ziggy v0.1 targets **Base Sepolia**, chain ID **84532**. Base's network documentation lists 84532 as the Base Sepolia chain ID.

Official source:
- https://docs.base.org/base-chain/quickstart/connecting-to-base

## Important compatibility boundary

The Ziggy v0.1 signer currently uses an injected **EIP-1193** provider (`window.ethereum`) and `personal_sign`.

Therefore:

- Opening the page in ChatGPT's in-app browser or ordinary Safari may show `No injected EVM wallet provider found`.
- The Coinbase trading screen is **not evidence** that an injected provider exists.
- Do not invent a tap path through a changing Coinbase UI.
- Do not claim compatibility until the actual Base app explorer loads the page and exposes the wallet provider.
- If the Base app explorer does not expose an injected provider, stop at `SIGNATURE_NOT_CREATED`; that is a client-compatibility gap, not a blockchain failure.

## State doctrine

`PUBLISHED ≠ PRESERVED ≠ SIGNED ≠ ATTESTED`

A wallet connection is not a signature. A signature is not a transaction. A transaction is not an attestation until independently verified.

`authority_created=false`
