# cw-report-client

Public, zero-trust replay verifier for Computer Wisdom receipts.

## Purpose

This client enables third-party auditors to:

- Verify SHA256 payload hashes
- Recompute Merkle roots
- Verify Base / EAS attestations
- Replay constitutional verification locally
- Emit deterministic ACCEPT / REJECT verdicts

## Release Law

> Public replay clients must distrust both the bundle and the chain until roots reconcile.

## Usage

```bash
npm install
npx @jsonwisdom/cw-report-client verify bundle.json
```

## Deterministic Guarantees

- Canonical JSON serialization
- Deterministic exit codes
- Pinned ethers version
- Replay-safe hashing
- Explicit EAS verification

Replay is legitimacy.
