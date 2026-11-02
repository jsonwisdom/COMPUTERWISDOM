# COMPUTERWISDOM — Redundant Read/Write Architecture v0.1

Status: PROPOSAL / MASTER RULES UNCHANGED / FABRICATION HOLD

## Identity vs authorization
Hardware security keys, authenticator apps and biometrics authenticate access. They do not replace GitHub repository authorization, branch rules or CI checks. Never archive identity documents, Social Security numbers, recovery codes or private keys in this repository.

## Paths
1. READ_PRIMARY: clone/fetch the default branch and its signed or hashed manifests.
2. READ_MIRROR: independently maintained, periodically tested read-only replica; compare exact object IDs and inventory manifests.
3. READ_OFFLINE: versioned offline archives with recovery instructions and checksums; periodically test restoration.
4. WRITE_PRIMARY: reviewed PR to protected master, with required verify check.
5. WRITE_STAGING: push to named nonprotected staging branch; run tests and archive immutable candidate receipt. Staging does not imply merge or production authorization.
6. WRITE_RECOVERY: documented, owner-approved break-glass process, ideally two-person authorization, hardware-key-protected, time-bounded and independently logged; no silent bypass.
7. RECONCILE: inventory and compare refs, commits, blobs, manifests, missing objects, and semantic metadata before promotion.

## Merkle forest
Content-addressed leaves (bytes) -> Git trees (paths) -> commits (history) -> forest catalog (cross-repository typed references) -> archive checkpoints (time) -> replay engines (CWaaS/Flywheel). A hash verifies identity against a trusted reference, not semantic truth.

## Branch rules
Observed active default-branch rulesets: OBSERVER_REFUSAL_MEMBRANE_001 (16924885) and Verify (17085224). Direct master write returned 409, requiring PR and verify. Rule changes require explicit authorized GitHub administration; this document does not change rules. Retain verify unless an equivalent, tested control is deliberately substituted.

## Semantic recovery
Reference schematic v0.2: reported baselined. Human phases decode/calculate/detect/explain/reverse remain NOT_TESTED. No human data or fabrication certification. Production HOLD.

## Acceptance
- Mirror restoration independently tested.
- At least one staging write and replay checked.
- Master promotion only through current authorized policy.
- Offline archive restoration documented.
- No sensitive identity artifacts in public repository.
