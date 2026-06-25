# Jaytree External Roots

External roots connect existing proof surfaces outside COMPUTERWISDOM into the Jaytree / Receipt Core stack.

## Current external root

```text
al-base-mcp-v0.1.json
```

This root points to the existing `jsonwisdom/AL` Base MCP / ALMS scaffold.

## Boundary

```text
Authority: NONE
Runtime: NOT_PERMITTED
Wallet authority: false
Execution authority: false
x402 enabled: false
Signing enabled: false
```

## Purpose

The AL Base MCP external root is a read-only bridge. It records that the AL scaffold exists and can be referenced by COMPUTERWISDOM receipts later.

It does not grant execution authority, wallet authority, signing authority, payment authority, or runtime authority.

## Future receipt flow

```text
fetch raw AL files only
compute deterministic hashes
verify local manifest
seal Receipt Core receipt
attest only after local verify exit 0
```
