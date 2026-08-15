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

## Reusable instruments

- [`ENFORCEMENT_TAIL_REPLAY_V0_1`](ENFORCEMENT_TAIL_REPLAY_V0_1.md) — CrissCross procedural-force audit: `CLAIM → LAW → AUTHORITY → PROCEDURE → ACTION → RECEIPT → EFFECT`, then reverse it until the chain is sourced or placed on HOLD.
- [`FAUCI_CONTEMPT_REFERRAL_2026_08_06`](fixtures/ENFORCEMENT_TAIL_FAUCI_2026_08_06.v0.1.json) — current procedural fixture; records observed steps and disputed/missing links without manufacturing prosecution, guilt, or statutory equivalence.
- [`SHOCK_GLOVE_BUDGET_POLICY_DEPLOYMENT_REPLAY_V0_1`](SHOCK_GLOVE_BUDGET_POLICY_DEPLOYMENT_REPLAY_V0_1.md) — follows a force-producing wearable from budget and procurement through policy, equipment authorization, training, task-force/squad assignment, incident reporting, and independent review.
- [`ICE_GLOVE_AUGUST_2026`](fixtures/SHOCK_GLOVE_ICE_2026_08.v0.1.json) — current public fixture; records the reported procurement ceiling and pending policy/training posture while leaving award, unit issuance, deployment, and incident use `NOT_ESTABLISHED` unless sourced.

## Hard rule

RePlay must be able to say `UNKNOWN`, `NOT_PERFORMED`, `NOT_CREATED`, `NOT_ESTABLISHED`, `DISPUTED`, or `HOLD` without pressure to complete the story.

`authority_created=false`
