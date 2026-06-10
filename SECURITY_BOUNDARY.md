# Security Boundary

## This repo contains operational signing logic

`COMPUTERWISDOM` includes:

- GCP KMS signer routing
- Foundry deploy scripts
- emergency agent revocation tooling
- anchor worker and finality observer logic
- Zodiac roles policy patterns

This makes the repository operationally sensitive even when no secrets are committed.

## Rules

| Rule | Status |
|---|---|
| `.env*` files must never be committed | Enforced by `.gitignore` |
| `.keys/` directory must never be committed | Enforced by `.gitignore` |
| Private key env vars such as `OWNER_PRIVATE_KEY` and `DEPLOYER_PRIVATE_KEY` | Never hardcode, never log, never commit |
| KMS env vars such as `KMS_KEY_VERSION`, `KMS_PUBLIC_KEY_HEX`, and `SIGNER_MODE` | May appear as documentation names only; never commit actual key material |
| Service account JSONs | Must remain ignored |
| Wallet exports, keystores, PEM files, and raw key files | Must remain ignored |

## If a key appears in any commit

1. Rotate it immediately.
2. Do not rely on git history cleanup as the remedy.
3. Treat rotation as the actual fix.
4. Document the rotation in this file.

## Audit Note

As of the latest repo scan, no literal private keys, mnemonics, or service account JSONs were found through available GitHub search.

This file exists because the repo contains signing, deployment, KMS, and revocation flows. The risk comes from operational proximity to keys, not from a confirmed exposed secret.

## Boundary Rule

Signing power must remain outside the repository.

Rule: no committed keys.
