# Ziggy Voice Enablements

Voice is an **input convenience layer**. It does not become authority by being spoken.

## Required path

`AUDIO → TRANSCRIPTION → DISPLAYED TEXT → HUMAN CONFIRMATION → NATURAL-LANGUAGE INTENT`

The confirmed text, not an opaque audio inference, becomes the actionable input.

## Voice safety boundaries

- Preserve whether text came from voice or typing.
- Show the transcription before proposing a write, signature, merge, or transaction.
- Never infer wallet ownership, ENS identity, permission, or family history from a voiceprint.
- Do not require biometric voice identification for Ziggy control.
- If transcription confidence is inadequate or a critical term is ambiguous, stop at `MIND_THE_GAP`.
- Network names, ENS names, addresses, hashes, branch names, and destructive commands require explicit visual confirmation.

## Example

Spoken: `Ziggy run the release on Sepolia`

Displayed confirmation must disambiguate the target, for example:

`Proposed target: Base Sepolia / chain ID 84532`

Only after human confirmation may Ziggy create a test-run proposal.

`authority_created=false`
