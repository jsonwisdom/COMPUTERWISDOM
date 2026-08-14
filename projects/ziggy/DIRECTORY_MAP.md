# Ziggy — Directories First Architecture

This tree defines boundaries before implementation.

```text
projects/ziggy/
├── natural-language/
├── ens/
├── voice/
├── imagination/
├── github-control/
├── launches/
│   └── main/
├── test-runs/
│   └── base-sepolia/
├── receipts/
└── replay/
```

## Core rule

`NATURAL_LANGUAGE → IDENTITY_CHECK → SANDBOX → HUMAN_REVIEW → PR → VERIFY → MERGE → OPTIONAL_TEST_RUN → RECEIPT → REPLAY`

No directory creates authority merely by existing.

## Boundary meanings

- `natural-language/` — human-readable commands become explicit intent records.
- `ens/` — ENS names, addresses, forward/reverse resolution results, and identity gaps.
- `voice/` — voice input becomes reviewable text before any action is proposed.
- `imagination/` — speculative/generated work stays outside preserved originals and protected release lanes.
- `github-control/` — proposal, branch, PR, status-check, and merge rules.
- `launches/main/` — canonical repository launch manifests. `main` here means the primary launch lane, **not Base Mainnet**.
- `test-runs/base-sepolia/` — test-only chain runs targeting Base Sepolia / chain ID 84532.
- `receipts/` — immutable-shaped records of what was proposed, verified, signed, merged, or tested.
- `replay/` — deterministic reconstruction of the reasoning and promotion path.

## Non-collapse doctrine

`NAME ≠ ADDRESS ≠ SIGNER_CONTROL ≠ GITHUB_IDENTITY ≠ RELEASE_AUTHORITY`

`VOICE ≠ COMMAND` until transcription is shown and confirmed.

`IMAGINED ≠ VERIFIED`.

`MERGED ≠ ON_CHAIN`.

`TESTNET ≠ MAINNET`.

`authority_created=false`
