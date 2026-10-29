# JASON WALLET SIGNING — EXECUTION CONTRACT V0.1
Status: HOLD. Build specification only; no wallet transaction code enabled.

## Separation of authorities

1. **Jason (person):** final denomination and approval. Never inferred from CI, WebAuthn, Coinbase authentication or elapsed time.
2. **GitHub:** source, immutable commit SHA, reviewed controls and evidence; a green workflow cannot sign.
3. **jsonwisdom.com:** public interface; never receives wallet private key or seed phrase.
4. **Workdesk authentication:** YubiKey WebAuthn login verifies a site-specific credential; **does not** authorize a blockchain transaction.
5. **Wallet:** independently asks Jason to inspect and approve every final transaction. No pre-authorization, standing unlimited allowance or hidden batch signatures.
6. **x402 receipts:** distinct payment service; remains HOLD independently of identity and wallet-connect passes.

## Stage 0 — fail closed

- The Workdesk Worker exposes GET /wallet/readiness only after an authenticated owner session, returning chain `eip155:8453` (Base), `READ_ONLY`, signingEnabled=false and paymentsEnabled=false.
- Any private data or wallet readiness response to an unauthenticated request is FAIL.
- No wallet connector is wired to this server; browser Wallet API must not be accessed before explicit selection.

## Stage 1 — read-only wallet connection

- Jason initiates wallet connection in the authenticated browser.
- Request only `eth_accounts` initially; `eth_requestAccounts` only on the explicit Connect button.
- Show selected account and `eth_chainId` without prompting a transaction. Verify Base chain ID `0x2105` (8453) and show mismatch without auto-switch.
- Any wallet balance must be labeled with chain/contract/source as of block number, and token contract decimals verified.
- Read-only does not prove ownership of onchain assets or permit signature approvals.

## Stage 2 — transaction preview (not execution)

- A pure, immutable preview lists chain, from, to, contract, function selector, decoded calldata, native value, estimated fees, slippage, approvals/allowances, deadline, spend cap, human-readable counterparty.
- Preview binds exact payload, contract, chain ID and account to hash; mismatch or changed provider state invalidates it.
- Transaction creation, broadcast, replay and price-impact decisions remain disabled during Stage 2.

## Stage 3 — separately approved signing (future)

- Require a fresh owner WebAuthn assertion on a new challenge bound to the *exact* transaction preview hash immediately before any signing action.
- Require a separate wallet-specific confirmation on the trusted wallet UI; **WebAuthn is not a blockchain signature**.
- No private keys/seeds, permit-style unlimited allowances or payment execution on the public web server.
- Session timeout, network changes, changed payload or expired approval => DENY.
- Record `ORDER_CREATED ≠ FILLED ≠ PROFITABLE`; receipts represent what was observed, not authorization or financial outcome.
- Never auto-enable x402 based on a wallet signature.

## Promotion gate

REQUIRED: WebAuthn successful physical-key enrollment and login, denial and replay tests, independent deployment security review, protected branch and secret isolation, wallet read-only account/chain inspection, exact-preview consistency tests, transaction simulator and human acceptance.
Only Jason approves final promotion. Routine construction/test revisions can proceed without repeated prompts, but key touches, enrollment secrets, signing, funds movement and promotion of financial authority cannot be delegated.
