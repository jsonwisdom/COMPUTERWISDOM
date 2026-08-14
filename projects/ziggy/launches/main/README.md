# Ziggy Main Launch Lane

This directory holds canonical **repository launch manifests** after review and merge.

`main` in this path means Ziggy's primary launch lane. It does **not** mean Base Mainnet and must never be interpreted as chain ID 8453 unless a specific manifest explicitly says so.

## Promotion requirements

A launch candidate may enter this lane only after:

1. original intent preserved
2. identity/ENS gaps surfaced
3. imagination sandbox complete
4. human review complete
5. GitHub PR checks pass
6. merge is explicitly authorized

## Chain boundary

Launch manifests may reference a chain target, but publication here does not submit any transaction.

`MAIN_LAUNCH ≠ MAINNET_TRANSACTION`

Current Ziggy test lane is Base Sepolia / 84532.

`authority_created=false`
