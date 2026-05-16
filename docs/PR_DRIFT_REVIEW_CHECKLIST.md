# COMPUTERWISDOM PR Drift Review Checklist

**Status:** ACTIVE  
**Applies To:** Pull requests targeting `master`  
**Purpose:** Prevent semantic, authority, anchor, and security drift before merge.

## Review Principle

A pull request may improve COMPUTERWISDOM only if it preserves the repository's role as an operational verification control plane.

No PR may silently convert COMPUTERWISDOM into an unrelated product, compliance pipeline, application monorepo, or authority surface.

## Required Classification

Every non-trivial PR should be classified before merge:

```text
NO_DRIFT
DOCS_ONLY_DRIFT
OPERATIONAL_DRIFT
SECURITY_DRIFT
AUTHORITY_DRIFT
ANCHOR_DRIFT
```

## Drift Classes

### NO_DRIFT
The PR preserves all constitutional boundaries and only improves implementation, documentation, or verification clarity.

### DOCS_ONLY_DRIFT
The PR changes language or framing but does not alter execution, claims, anchors, keys, policies, or repo identity.

### OPERATIONAL_DRIFT
The PR changes workflows, automation, deployment paths, pipelines, workers, scheduling, or runtime behavior.

Requires review for:

- ghost liveness
- false status indicators
- unbounded automated commits
- unclear output classification

### SECURITY_DRIFT
The PR touches signing, keys, credentials, KMS, deployment secrets, access control, or revocation logic.

Requires explicit review before merge.

### AUTHORITY_DRIFT
The PR allows an external system, workflow, dashboard, compliance regime, platform, or agent to define truth or legitimacy.

Requires constitutional amendment or rejection.

### ANCHOR_DRIFT
The PR modifies anchor claims, proof paths, attestation logic, EAS/ENS status, mainnet claims, receipt hashes, or canonical lineage.

Requires explicit receipt evidence.

## Merge Gate Questions

Before merge, answer:

1. Does this preserve the Anchor 001 boundary?
2. Does this preserve the layer law?
3. Does this preserve the security boundary?
4. Does this avoid ghost anchors?
5. Does this avoid unproven production claims?
6. Does this keep observers from becoming authority roots?
7. Does this preserve repo identity?
8. Are generated outputs classified as evidence, not truth by themselves?
9. Are automated workflows bounded and auditable?
10. Is there a rollback or revocation path if the change is wrong?

## Required PR Footer

Recommended footer for major PRs:

```text
Drift Classification: <NO_DRIFT | DOCS_ONLY_DRIFT | OPERATIONAL_DRIFT | SECURITY_DRIFT | AUTHORITY_DRIFT | ANCHOR_DRIFT>
Anchor Boundary Preserved: <YES | NO | N/A>
Security Boundary Preserved: <YES | NO | N/A>
Observer Authority Transfer: <NONE | PRESENT>
Receipts Provided: <YES | NO | N/A>
Constitutional Amendment Required: <YES | NO>
```

## Automatic Rejection Signals

Reject or hold a PR if it:

- claims mainnet anchoring without transaction receipts
- claims ENS write completion without visible ENS record evidence
- treats GitHub, EAS, ENS, Microsoft, Azure, or any platform as authority root
- commits secrets or key material
- creates automated liveness without verification meaning
- rewrites repo purpose without constitutional amendment
- collapses Anchor 001 into COMPUTERWISDOM without explicit transition receipt

## Closing Rule

Merge only what preserves replay, lineage, and bounded authority.

When in doubt, classify drift before merging.
