# Ziggy — Directories First Architecture

This tree defines boundaries before implementation.

```text
projects/ziggy/
├── natural-language/
├── identity/
│   └── addresses/
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
- `identity/` — typed thresholds for activity, protocol role, control, identity binding, third-party attestation, and authority; address snapshots live under `identity/addresses/`.
- `ens/` — ENS names, addresses, forward/reverse resolution results, and identity gaps.
- `voice/` — voice input becomes reviewable text before any action is proposed.
- `imagination/` — speculative/generated work stays outside preserved originals and protected release lanes.
- `github-control/` — proposal, branch, PR, status-check, and merge rules.
- `launches/main/` — canonical repository launch manifests. `main` here means the primary launch lane, **not Base Mainnet**.
- `test-runs/base-sepolia/` — test-only chain runs targeting Base Sepolia / chain ID 84532.
- `receipts/` — immutable-shaped records of what was proposed, verified, signed, merged, or tested.
- `replay/` — deterministic reconstruction of the reasoning and promotion path.

## Identity ladder

`ACTIVITY → PROTOCOL_ROLE → CONTROL → IDENTITY_BINDING → AUTHORITY`

Third-party attestation is tracked separately:

`ATTESTATION ABOUT ADDRESS ≠ SIGNATURE BY ADDRESS`

Authority is not the automatic next state after identity. It requires an explicit human or sealed-protocol grant within a defined scope.

## Non-collapse doctrine

`NAME ≠ ADDRESS ≠ SIGNER_CONTROL ≠ GITHUB_IDENTITY ≠ RELEASE_AUTHORITY`

`OBSERVED_EDGE ≠ OWNERSHIP`.

`PROTOCOL_OWNERSHIP ≠ PRIVATE_KEY_CONTROL`.

`CONTROL ≠ IDENTITY`.

`IDENTITY ≠ AUTHORITY`.

`VOICE ≠ COMMAND` until transcription is shown and confirmed.

`IMAGINED ≠ VERIFIED`.

`MERGED ≠ ON_CHAIN`.

`TESTNET ≠ MAINNET`.

`authority_created=false`
