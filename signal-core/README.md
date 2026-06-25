# Signal Core

Receipt pipeline scaffold for COMPUTERWISDOM.

## jaytree External Roots v0.1

- AL Base MCP: `jaytree/external-roots/al-base-mcp-v0.1.json`
  - Authority: NONE
  - Runtime: NOT_PERMITTED
  - Human approval: REQUIRED
  - Wallet authority: false
  - Execution authority: false
  - Signing enabled: false
  - x402 enabled: false
  - Connected to future Receipt bundles and EAS attestations

## Receipt flow

```text
fetch raw AL files only
compute deterministic hashes
verify local manifest
seal Receipt Core receipt
attest only after local verify exit 0
```
