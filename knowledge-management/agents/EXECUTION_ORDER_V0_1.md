# Content-Aware Auditor Execution Order v0.1

Status: PROPOSED CONTRACT ON DRAFT PR
Authority: false
Inventory execution: prohibited until contract validation passes

## Canonical sequence

1. Repository Reader — observe repository content and metadata.
2. Evidence Preservation — write immutable evidence records and hashes.
3. Lineage Analyzer — reconstruct milestones and cross-repository relationships.
4. Trinity Classifier — assign AL, COMPUTERWISDOM, JOY, or UNKNOWN using cited evidence.
5. Security Gate — decide public, redacted, private, family-secure, operator-secure, blocked, or unknown publication state.
6. Importance Scorer — compute multidimensional importance without repository size.
7. Collaboration Graph — emit only evidence-backed edges.
8. Audit Receipt — bind inputs, outputs, contract versions, checkpoint, and hashes.
9. Audit Resume — persist exact machine state for deterministic continuation.

## Checkpoint gates

### CP-0 — Contract Gate

Required:
- all formal schemas present;
- valid fixtures pass;
- invalid fixtures fail for the expected reason;
- all artifacts enforce `authority: false`.

Failure action: halt. No repository scan permitted.

### CP-1 — Observation Gate

Required:
- repository and scan commit resolved;
- README, commits, PRs, workflows, schemas, receipts, and cross-references observed or explicitly marked `UNOBSERVED`;
- private content excluded from public artifacts.

Failure action: emit `BLOCKED` or `UNKNOWN`; do not infer missing evidence.

### CP-2 — Lineage Gate

Required:
- every confident milestone or relationship cites evidence;
- unresolved lineage remains visible;
- name similarity creates no edge.

Failure action: downgrade relationship confidence to `PARTIAL` or `UNKNOWN`.

### CP-3 — Classification Gate

Required:
- metadata-only classifications cannot exceed `PARTIAL`;
- `VERIFIED` and `STRONGLY_SUPPORTED` classifications cite at least two evidence references;
- counterevidence and unresolved questions are preserved.

Failure action: assign `UNKNOWN` or `CONFLICTED`.

### CP-4 — Security Gate

Required:
- private contents never enter public output;
- protection states cannot be downgraded without explicit human authorization;
- secret detection blocks publication.

Failure action: `BLOCKED_SECRET_DETECTED`, `PRIVATE_ONLY`, or `UNKNOWN_PENDING_REVIEW`.

### CP-5 — Graph and Importance Gate

Required:
- repository size is not used;
- every graph edge cites evidence;
- unverified edges remain unresolved;
- multidimensional scores preserve evidence strength separately from value.

Failure action: `UNCLASSIFIED` tier and unresolved graph edge.

### CP-6 — Receipt and Resume Gate

Required:
- audit receipt binds all inputs and outputs by SHA-256;
- contract and agent versions are recorded;
- checkpoint commit exists;
- resume integrity conditions are recorded;
- failed, blocked, and unknown repositories remain visible.

Failure action: no success claim. Resume status becomes `BLOCKED` or `FAILED`.

## Constitutional rules

- Unknown is a valid final result.
- Missing evidence is not negative evidence.
- A workflow file is not proof of a successful workflow run.
- ENS names, Base addresses, EAS attestations, X402 payments, and Zora publications require separate observed receipts for their specific claims.
- No agent may claim legal, family, wallet, or institutional authority.
- No canonical Trinity classification may be published until CP-0 through CP-6 are satisfied.
