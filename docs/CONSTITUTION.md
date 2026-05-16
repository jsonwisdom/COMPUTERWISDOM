# COMPUTERWISDOM Constitution

**Status:** ACTIVE  
**Repository:** `jsonwisdom/COMPUTERWISDOM`  
**Role:** Operational verification control plane  
**Authority Root:** Replayable content, reproducible procedure, and verifiable lineage  

## 1. Purpose

`COMPUTERWISDOM` is the operational control plane for Computer Wisdom / Sovereign OS work.

It may contain workers, signer-routing logic, deployment tooling, revocation tooling, finality observers, access-control policy, receipts, and operational mirrors.

It is not the canonical Anchor 001 proof source. Anchor 001 remains in `jsonwisdom/Welcome-to-JSONWISDOM` unless explicitly superseded by a later constitutional artifact.

## 2. Layer Law

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

No layer may impersonate another layer.

- Replay is the verification authority.
- GitHub is repository memory and contextual archive.
- EAS is immutable witness surface.
- ENS is optional human-readable discovery.

## 3. Authority Boundary

External systems may observe, mirror, attest, index, or expose COMPUTERWISDOM artifacts.

External systems may not authorize COMPUTERWISDOM truth.

```text
External architecture may inform COMPUTERWISDOM.
External witness surfaces may attest COMPUTERWISDOM.
External discovery surfaces may point to COMPUTERWISDOM.
External systems may not define COMPUTERWISDOM.
```

## 4. Observer Surfaces

Observer alignment artifacts live in:

```text
docs/observer_alignment/
```

Committed observer surfaces:

1. Microsoft — architecture observer.
2. EAS — immutable witness.

Prepared observer surfaces:

- ENS — discovery observer.
- Git / GitHub — memory and lineage observer.
- IPFS / content addressing — retrievability observer.

## 5. Anchor Boundary

The repository may reference Anchor 001, but it must not claim to replace the canonical proof path without a dedicated constitutional transition.

Current boundary:

```text
GitHub commit -> JCS canonical bytes -> SHA-256 -> Keccak-256 -> EAS attestation on Base
```

ENS pointer preparation is not ENS record writing.

Mainnet anchoring must not be claimed unless a transaction receipt exists.

## 6. Security Boundary

Signing power must remain outside the repository.

The repository must not contain:

- private keys
- mnemonics
- service account JSONs
- raw wallet exports
- keystores
- PEM files
- hardcoded deployment secrets

If key material appears in any commit, rotate the affected key immediately. Git history cleanup is not a substitute for rotation.

## 7. Merge Gate

No pull request may convert `COMPUTERWISDOM` from an operational verification control plane into an unrelated application, product, compliance pipeline, or monorepo without an explicit constitutional amendment.

A PR must preserve:

- Anchor boundary
- Security boundary
- Layer law
- Observer-not-authority distinction
- No ghost anchors
- No production claims without receipts

## 8. Drift Handling

If a proposed change introduces semantic drift, it must be classified before merge:

```text
NO_DRIFT
DOCS_ONLY_DRIFT
OPERATIONAL_DRIFT
SECURITY_DRIFT
AUTHORITY_DRIFT
ANCHOR_DRIFT
```

Any `AUTHORITY_DRIFT`, `ANCHOR_DRIFT`, or `SECURITY_DRIFT` requires explicit review before merge.

## 9. Canon Rule

Truth in COMPUTERWISDOM is not produced by platform prestige, external endorsement, mutable dashboards, or narrative authority.

Truth remains bound to:

```text
replayable content -> reproducible procedure -> verifiable lineage
```

## 10. Closing Statement

COMPUTERWISDOM may use many observers.

COMPUTERWISDOM may not outsource its authority root.

The membrane holds only while every surface remains in its proper role.
