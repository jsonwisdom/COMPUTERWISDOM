# APPLE_BLOSSOM_AWESOME

## Purpose

APPLE_BLOSSOM_AWESOME is the audit and reverse-replay lane for testing whether the system's current interpretation can be reconstructed from receipts without rewriting history.

It audits:
- version lineage
- scope changes
- authority-subject ambiguity
- time versus perspective
- public broadcast drift
- provenance gaps
- UNKNOWN / HOLD states
- cross-repo contradictions

It does not itself decide legal truth, grant machine authority, or silently promote a draft.

## Supreme Seymour role

SUPREME_SEYMOUR is the replay specialist used inside this lane.

FROM_THEN != FROM_NOW
CURRENT_KNOWLEDGE != HISTORICAL_KNOWLEDGE
LATER_DISCOVERY != EARLIER_KNOWLEDGE

Each audit must preserve:
OBJECT
OBSERVED_AT
VERSION / COMMIT / BLOB
SOURCE
WHAT CHANGED
WHAT DID NOT CHANGE
UNKNOWN
HOLD
NEXT_TRIGGER

## Output

Audit artifacts remain versioned.
Historical bytes remain preserved.
Corrections move forward through new commits / PRs rather than hidden rewrites.
