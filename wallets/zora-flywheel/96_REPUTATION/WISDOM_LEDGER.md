# WISDOM LEDGER V0.1

MODE = APPEND_ONLY
SCOPE = INTERNAL_SYSTEM_QUALITY
EXTERNAL_REPUTATION_CLAIM = FALSE

## Dimensions

KNOWLEDGE
- verified facts available to the system

INTELLIGENCE
- ability to connect evidence correctly without invalid joins

REPUTATION
- historical reliability of outputs and receipts inside this system

WISDOM
- correct use of knowledge + intelligence + uncertainty + restraint

## Suggested normalized components

K = verified_evidence_ratio
I = valid_relation_ratio
R = replay_success_ratio
U = uncertainty_discipline
C = correction_quality

Candidate informational score:

W = (K * I * R * U * C)^(1/5)

This score is informational only.

W != HUMAN_WORTH
W != LEGAL_AUTHORITY
W != CREDIT_SCORE
W != PLATFORM_REPUTATION
W != IDENTITY_PROOF

A missing component remains MISSING; it is not silently replaced with zero or one.
