# CoinBaseKid REPLAY 007 — §5a acceptance-time witness (candidate)

Status: **CODE REVIEW + SYNTHETIC TEST ONLY / PRODUCTION WITNESS NOT ENROLLED / NO PUBLICATION**.

This component does not take a live wallet signature. It never submits to a chain, witnesses a real block, grants token approval, publishes data, or transfers funds.

## Distinct trust roots

- **Batch signer** — the account whose EIP-712 wallet-control signature permitted the candidate batch; canonical policy is `flywheel-connect/base-wallet-policy.v2.json`.
- **Bundle creator** — the creator asserted in the submitted bundle context. **This identity is not yet authenticated independently.**
- **Witness signer** — a separate EIP-712 signing key, distinct from both creator and EVERY signer recorded in SQLite for the batch root.

The production witness policy (`witness-policy.v1.json`) has **zero authorized witnesses**, `productionEnabled:false`, and `externalKeyRegistration:"NOT_ESTABLISHED"`. This intentionally fails closed until an independent public key is authenticated and published outside the control of the batch creator. No fabricated key is enrolled.

## Exact signed witness object

EIP-712 domain: `name:"CoinBaseKid Independent Acceptance Witness"`, `version:"1"`, `chainId:8453`, `salt` pinned by the witness policy. Contract-free off-chain attestation; there is no verifying contract.

Signed primary type `AcceptanceWitness`:

```json
{
  "origin": "https://wallet.jsonwisdom.com",
  "root": "0x<batch-merkle-root>",
  "createdAtBlock": 24600000,
  "observedAtBlock": 24600002,
  "observedAt": 1793560821,
  "witnessNonce": "0x<32-byte-random-nonce>",
  "purpose": "I independently observed this candidate batch root at the signed Base block height; no payment or export authority."
}
```

Block heights above are **synthetic examples**, not claims of an observed Base block. `createdAtBlock` must come from an authenticated acceptance-time event **outside this component**; the current `replay_batches` table does not independently store or authenticate chain block height. The signed observation does not prove what actually existed on Base.

The witness must sign `root`, `createdAtBlock`, `observedAtBlock`, `observedAt`, `witnessNonce`, the exact origin and purpose. `observedAtBlock` must be within [`createdAtBlock`, `createdAtBlock + 12`]. The observed time must be near the batch `reserved_at`, not arbitrarily later or future.

## Durable local witness store

After verifying the signature and independent signer, one SQLite `BEGIN IMMEDIATE` transaction writes:

- `witness_attestations`: `root` primary key (at most one attestation per root), witness signer, EIP-712 data and signature, signature hash, creator claim, observed block and time.
- `witness_nonces`: `PRIMARY KEY(chain_id,witness_signer,nonce)`, with an FK to the accepted root. A witness nonce cannot be reused to attest another root.
- Duplicate root, duplicate nonce, wrong signer, changed root, missing witness, incorrect block or timestamps, and false origin all **HOLD**.

The SQLite file is private and local; stored signatures are **not encrypted to a recipient**. The publication inspection function checks exact stored evidence and returns `WITNESS_PRESENT_REVIEW_ONLY`, never `publication:true` or authorization. `publication:true` without one exact valid witness returns `NO_WITNESS` when a witness key is enrolled; production currently rejects all requests as `WITNESS_NOT_CONFIGURED`.

## Synthetic tests and boundaries

`node --test services/confucius-compute-wisdom/base-batches/acceptance-witness.test.mjs`

All tests sign actual EIP-712 messages using **unfunded public synthetic test-only private keys**; no real Coinbase key or payments. They check:
witness independent from creator/batch signer, exact signed root, block window, acceptance-time window, empty/orphaned witness HOLD, durable witness nonce uniqueness across two distinct roots, exactly one witness per root, wrong domain or signing key rejection, and production no-witness HOLD.

### Still OPEN before §5a production closure

1. Out-of-band registration/publication of a real independent witness public key, with provenance and key rotation policy.
2. Authenticated acceptance-time `createdAtBlock` and independent Base block-height source (the current module checks signed claims and bounded arithmetic only).
3. Authenticated `bundle.creator` identity, independent of request metadata.
4. Multi-replica consensus/nonce store: SQLite is single-writer on one authoritative host only; no shared NFS or separate load-balanced databases.
5. §5b signed export authorization, recipient encryption, expiry, and append-only export logs. **No proof bundle may be publicly exported by this component.**

This witness attestation is not legal identity, ENS ownership, payment authority, or a production-ready audit timestamp.
