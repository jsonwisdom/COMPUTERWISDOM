# Ziggy Base Sepolia Test Runs

This directory is for **test-only execution records** targeting Base Sepolia.

Network:

- Name: Base Sepolia
- Chain ID: `84532`
- Hex chain ID: `0x14a34`

## Test-run rule

`PROPOSED → HUMAN_AUTHORIZED → SUBMITTED → RECEIPT_CAPTURED → INDEPENDENTLY_VERIFIED`

A proposed run is not a submitted run. A wallet signature is not a transaction. A transaction hash is not an attestation UID.

## Required test receipt fields

- source repository / commit
- launch manifest identity
- requested signer address
- actual signer address
- chain ID observed from wallet/provider
- transaction hash, if submitted
- attestation UID, if one is actually returned
- block number / timestamp when verified
- success/failure state
- gap declarations
- `authority_created=false`

## Promotion boundary

A successful Base Sepolia test may inform a later launch decision. It cannot silently promote itself to Base Mainnet or to a production claim.

`TESTNET_PASS ≠ MAINNET_LAUNCH`
