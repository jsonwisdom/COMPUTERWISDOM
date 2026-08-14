# Ziggy RePlay

RePlay reconstructs how a Ziggy artifact moved from human intent to any later public or chain-visible state.

## Replay chain

`ORIGINAL_REQUEST → NORMALIZED_INTENT → ENS/IDENTITY_CHECKS → SANDBOX_OUTPUT → HUMAN_DECISION → GITHUB_DIFF → STATUS_CHECKS → MERGE → TEST_RUN → RECEIPT`

Each link should point backward to its source rather than merely narrate what happened.

## Replay questions

- What did the human originally ask?
- What did Ziggy infer or normalize?
- Which identities were claimed, resolved, or cryptographically verified?
- Which files changed?
- Which checks ran?
- Who authorized promotion?
- Was anything signed?
- Was anything submitted to Base Sepolia?
- Is there a real transaction hash?
- Is there a real attestation UID?
- What gaps remain?

## Hard rule

RePlay must be able to say `UNKNOWN`, `NOT_PERFORMED`, or `NOT_CREATED` without pressure to complete the story.

`authority_created=false`
