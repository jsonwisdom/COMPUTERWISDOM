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

## Classification-Debt Intercept Safeguards (Issue #453)

The system SHALL apply the following safeguards whenever a classification-debt intercept is detected:

1. **LABEL_PROVISIONAL**
   - A classification derived from an observation MUST remain `PROVISIONAL` until source-bound, contradiction-aware validation is complete.
   - Interface or connector failure MUST NOT be promoted into a capability, permission, role, or identity claim.

2. **CLAIM_SOURCE_REQUIRED**
   - No capability, permission, role, or identity MAY be inferred from an observation alone.
   - Every classification MUST include an explicit, human-auditable `CLAIM_SOURCE` and evidence reference.

3. **CONTRADICTION-DRIVEN_RECLASSIFICATION**
   - A material contradiction SHALL trigger reclassification and replay through the Epistemic Stack validators.
   - The prior label MUST remain append-only evidence and MUST be marked superseded by a new reclassification receipt; it MUST NOT be silently erased or mutated.

### Human Appeal Path (Six Questions)

The system SHALL provide a human appeal path that answers:

1. Who labeled me?
2. From what evidence?
3. When?
4. Under which rule?
5. What changed because of it?
6. How do I correct it?

The answers and resulting reclassification MUST be preserved as replayable receipts. Neither classification nor reclassification creates authority.

```json
{
  "label_provisional": true,
  "claim_source_required": true,
  "contradiction_reclassification": "REQUIRED",
  "appeal_path": "MANDATORY",
  "authority": false
}
```

## Operator Quick Rule

```text
If a claim changes operational state, it needs a receipt.
If a receipt changes authority, it needs a separate governance path.
```

## Binding Status

This charter is a repository artifact. It becomes stronger only when bound to a commit hash, branch, PR, and follow-up receipt.
