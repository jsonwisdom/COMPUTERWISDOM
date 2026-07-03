# COMPUTERWISDOM Operating Charter

## Status

```text
repository: jsonwisdom/COMPUTERWISDOM
classification: CORPORATE_OPERATIONS_ROOT_QUALIFIED
canonical_proof_root: false
authority: false
truth_claim: false
issued_at: 2026-07-03
```

## Purpose

`COMPUTERWISDOM` is the qualified corporate operations root for Computer Wisdom / Sovereign OS work.

Its role is to coordinate operational records, replay receipts, signer boundaries, deployment surfaces, revocation tooling, workflow gates, and machine-auditable control-plane events.

This repository exists to make operational claims testable through receipts, not accepted through narrative.

## Scope

This repository may contain or coordinate:

- operational doctrine
- replay instructions
- workflow receipts
- signer-boundary documentation
- deployment preparation logic
- revocation and emergency-control documentation
- status files and receipt manifests
- public coordination artifacts
- cross-repository binding tables

This repository must not contain:

- private keys
- seed phrases
- service-account JSON files
- live signing authority
- unreviewed payment adapters
- claims of final authority without a separate authority-elevation receipt

## Authority Boundary

```text
authority:false is the default and standing posture.
```

Promotion, merge, replay success, CI success, issue creation, or operator action does not create authority.

Authority may only be elevated through a dedicated governance event containing:

1. a specific authority-elevation PR;
2. a governance artifact defining the requested authority;
3. a machine-generated attestation or receipt;
4. lineage linking the elevation to the relevant proof root;
5. explicit review and merge;
6. a follow-up receipt binding the final commit hash.

Until that full path exists, this repository remains an operational control plane only.

## Relationship to Anchor 001

`COMPUTERWISDOM` is not the canonical Anchor 001 proof source.

The current canonical Anchor 001 proof source is:

```text
jsonwisdom/Welcome-to-JSONWISDOM
```

Operational relationship:

```text
Welcome-to-JSONWISDOM = canonical Anchor 001 proof source
COMPUTERWISDOM         = corporate / operational doctrine root
AL                     = receipt / proof machinery
receiptos-base         = replay / frame / receipt rail
EAS                    = witness layer
ENS                    = discovery layer
```

## Governance Model

The governance model is receipt-first:

```text
Observe -> Capture -> Hash -> Replay -> Attest -> Promote -> Bind
```

Required invariants:

- no receipt, no authority;
- preservation is not validation;
- indexing is not accusation;
- replay is not truth by itself;
- GitHub contextualizes, but does not become the truth surface;
- EAS witnesses, but does not create global legitimacy;
- ENS discovers, but does not create authority.

## Operator Quick Rule

```text
If a claim changes operational state, it needs a receipt.
If a receipt changes authority, it needs a separate governance path.
```

## Binding Status

This charter is a repository artifact. It becomes stronger only when bound to a commit hash, branch, PR, and follow-up receipt.
