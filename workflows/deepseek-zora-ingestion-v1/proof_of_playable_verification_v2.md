# PROOF_OF_PLAYABLE_VERIFICATION_V2

## Canonical States (only)

- `CANDIDATE` — claim with at least one receipt, not yet checked for contradictions.
- `HELD` — claim with unresolved contradiction or missing secondary receipt.
- `REJECTED` — claim proven false by verified contradiction receipt.
- `VERIFIED_RECEIPT` — receipt passes all gates, no active contradiction.
- `CANON` — `VERIFIED_RECEIPT` with replayable contradiction log and time anchor.

## Core Laws

- No receipt → no state entry.
- No replayable contradiction log → no CANON.
- Publication through Zora/Base is a reference surface, not proof.
- All unknown hashes = `PENDING_HASH`.
- All example URLs = `EXAMPLE_PLACEHOLDER_NOT_VERIFIED`.

## Replay Semantics

- Contradiction scans run from genesis block.
- Receipt Vault is append-only.
- Each state transition logs deterministic diff.

## Authority Boundary

- Jay submits signals, but cannot force state promotion.
- DeepSeek outputs enter as `CANDIDATE` only.
- Machine speed sorts; receipts decide.

Replayability is the constitution.  
Receipts are the atoms.
