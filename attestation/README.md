# Attestation — Nitro Enclave Verification Primitive

Verifies that a running enclave matches the ZTWS measurement bound on-chain.

## One-Command Verification

```bash
curl -sL https://raw.githubusercontent.com/jsonwisdom/COMPUTERWISDOM/main/attestation/verify.sh | bash -s -- --enclave-id $ENCLAVE_ID
```

## Manual Verification

```bash
python3 verify.py --attestation-file attestation.json --enclave-id $ENCLAVE_ID
```

## Expected Output

```text
ATTESTATION: VALID
├── PCR0: MATCH
├── PCR8: MATCH
└── Enclave: ztws-verifier
```

## Architecture

ZTWS registry binds MEASUREMENT → attestation proves running enclave matches → receipts are trusted.
