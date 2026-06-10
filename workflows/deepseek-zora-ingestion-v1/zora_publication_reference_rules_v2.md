# Zora Publication Reference Rules V2

## Publication is Not Proof

Zora and Base are publication surfaces and mirrors only. They never constitute receipt or proof.

## Allowed Publication by State

- `CANDIDATE`: permitted only with full disclaimer.
- `HELD`: permitted as metadata-only disclosure.
- `REJECTED`: permitted for transparency and replay.
- `VERIFIED_RECEIPT`: permitted with receipt digest and vault reference.
- `CANON`: permitted only after full replay confirmation.

## Forbidden Publication by State

- No publication may claim `CANON` before explicit CANON transition in the Receipt Vault.
- No publication during invalid state transition.
- No publication that substitutes publication links for receipts.

## HELD Metadata-Only Disclosure Rule

HELD publications must contain only:

- metadata
- mandatory disclosure block
- reference to pending receipt state

No HELD publication may imply verification.

## VERIFIED_RECEIPT Publication Rule

VERIFIED_RECEIPT publications may reference:

- `receipt_digest`
- `merkle_root`
- replay summary reference

## CANON Publication Rule

CANON publication requires:

- replay log confirmation
- contradiction replay confirmation
- matching Merkle chain
- valid state transition chain

## Required Caption Disclaimer

> This is a [STATUS] publication under PROOF_OF_PLAYABLE_VERIFICATION_V2. It is a mirror surface. Claims require verifiable receipts in the append-only vault.

## Receipt Reference Minimum Fields

Every publication must include at least:

- `receipt_digest`
- `merkle_root`
- `vault_replay_summary_hash`

## Violation Handling

Any violation triggers:

- contradiction replay log entry
- replay audit review
- potential REJECTED state

Publication does not override vault state.

## Statement

Publication surfaces are mirrors, not judges.

Replayability is the constitution. Receipts are the atoms. Publication surfaces are mirrors, not judges.
