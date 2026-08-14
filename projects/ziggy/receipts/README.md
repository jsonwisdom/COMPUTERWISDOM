# Ziggy Receipts

Receipts preserve state transitions without upgrading claims beyond the evidence.

## Receipt families

- intent receipt
- ENS resolution receipt
- voice transcription confirmation receipt
- imagination sandbox receipt
- GitHub proposal / merge receipt
- wallet signature receipt
- Base Sepolia test-run receipt
- attestation receipt, only when a real UID and transaction hash exist

## Required doctrine

Every receipt must distinguish:

`CLAIMED / OBSERVED / VERIFIED / SIGNED / SUBMITTED / ATTESTED`

Missing fields remain null or explicitly unknown. They are never backfilled by inference.

`authority_created=false`
