# GRAYBABY_WITNESS_REVERSE_RESUME_REPLAY_V0_1

Status: `DRAFT_CANONICAL / REVIEWABLE`  
Date: `2026-08-19`  
Authority created: `FALSE`  
Employment proof created: `FALSE`  
Credential proof created: `FALSE`  
Production deployment proof created: `FALSE`  
Migration authorized: `FALSE`

## Purpose

Create a reusable, cross-repository resume-evidence engine that converts bounded receipts into defensible capability language without allowing artifacts, publications, access, identity labels, or narrative to silently become employment, credential, authority, or production-deployment proof.

## Core inversion

```text
RECEIPTS
  -> DEMONSTRATED FUNCTION
  -> BOUNDED CAPABILITY
  -> ALLOWED_RESUME_LANGUAGE
```

Never:

```text
RESUME CLAIM -> SEARCH FOR SUPPORT
```

## Separation of duties

- `GrayBabyWitness` = evidence acquisition + witness classification.
- `ReverseResumeReplay` = evidence -> capability extraction -> wording gate.
- Gray Baby does not author resume claims. It supplies bounded witnesses.
- ReverseResumeReplay does not create evidence. It consumes witnesses and determines the strongest wording the receipts permit.

## Canonical unit

```text
RESUME_CAPABILITY
├── FUNCTION
├── ARTIFACT
├── REPO
├── PATH
├── COMMIT
├── TEST_CI
├── EXTERNAL_WITNESS
├── EVIDENCE_STATE
├── LIMITATIONS
└── ALLOWED_RESUME_LANGUAGE
```

## Required evidence path

```text
REPO -> PATH -> COMMIT -> TEST/CI -> DEPLOYMENT/READBACK
```

Any missing required edge remains `HOLD`.

Artifact proof is kept separate from employment, credentials, institutional authority, and production deployment.

## Evidence states

| State | Meaning |
|---|---|
| `PROVEN` | Required receipts directly establish the bounded claim. |
| `BOUND` | Implementation or artifact process is receipt-linked, but broader real-world claims remain excluded. |
| `HOLD` | Evidence is missing, unresolved, stale, or insufficient for promotion. |
| `CONFLICT` | Witnesses materially disagree; no promotion until resolved. |

## Promotion gate

A capability may be promoted only when:

1. The function is identified from receipts rather than self-description.
2. Repository/path/commit identity is bound where applicable.
3. Test/CI or equivalent execution evidence is bound where claimed.
4. External witness is typed separately from underlying claim proof.
5. Limitations are explicit.
6. Proposed resume wording does not exceed the evidence state.

## Fail-closed rules

```text
PUBLICATION_WITNESS != UNDERLYING_CLAIM_PROOF
ARTIFACT != EMPLOYMENT
ARTIFACT != CREDENTIAL
CI_SUCCESS != PRODUCTION_DEPLOYMENT
PLATFORM_ACCESS != APPLICATION_EXECUTION
IDENTITY_LABEL != INSTITUTIONAL_AUTHORITY
MISSING_RECEIPT -> HOLD
CONFLICTING_WITNESS -> CONFLICT
```

## Cross-surface roles

- **Google Drive** = evidence master / document witness / claim inventory context.
- **GitHub** = code, path, commit, PR, CI, and replayable implementation receipts.
- **OpenAI Platform** = connected topology/access context only; resume-proof weight = `0` unless independent runtime/deployment receipts are separately bound.
- **Public publication surfaces** = temporal/publication witnesses only unless the underlying claim is independently proven.

Drive mirror/specification: https://docs.google.com/document/d/1XnfaAWna77E3yke7uLbaX1yNeWNcYxhGISl4fpibi48/edit

## Gray Baby seed witness

```text
REPOSITORY = jsonwisdom/COMPUTERWISDOM
PATH = ARTIFACTS/GRAY_BABY/AMERICAN_GRAY_BABY_RECEIPT_STANDARD_v0.1.md
PR = #509
HEAD = ba726a40144266bc91df46802907c0bc215231d5
PR_STATE = OPEN / DRAFT / MERGEABLE
CI = SUCCESS
```

The seed witness preserves observer-only, receipt-first, Hold/Proven semantics.

## Allowed example capability

> **Cross-surface publication-witness replay** — Built an append-only verification workflow binding public artifacts to cryptographic byte receipts, repository state, independent records, temporal witnesses, and fail-closed evidence gates.

```text
EVIDENCE_STATE = BOUND
PROCESS_CLASS = BOUND_ARTIFACT_PROCESS
```

## Explicit non-promotions

```text
CISA collaboration = FALSE / NOT PROVEN
Medusa 500+ independently proven = FALSE / NOT PROVEN
Production deployment = NOT PROVEN
Employment verification = NOT PROVEN
Credential verification = NOT PROVEN
```

## Batch Resume Builder contract

For each repository or project candidate:

1. `ACQUIRE` witnesses.
2. `NORMALIZE` into `RESUME_CAPABILITY` fields.
3. `VERIFY` identity and execution receipts.
4. `CLASSIFY` evidence state.
5. `EXTRACT` demonstrated function.
6. `APPLY` limitations.
7. `GENERATE` only allowed resume language.
8. `EMIT HOLD` instead of filling gaps.
9. `RETAIN PROVENANCE` so every resume line can be reverse-replayed to its receipts.

## Output object

```yaml
capability_id: string
function: string
evidence_refs: []
repo: string | null
path: string | null
commit: string | null
test_ci: string | null
external_witnesses: []
evidence_state: PROVEN | BOUND | HOLD | CONFLICT
limitations: []
allowed_resume_language: string | null
forbidden_promotions: []
replay_timestamp: string
```

## Source bindings

- Resume evidence doctrine: `Jason Jay Wisdom Resume Evidence Appendix — 2026-08-18`.
- Gray Baby doctrine: `American Gray Baby — Receipt Standard v0.1 — 2026-08-19`.
- This implementation: `docs/resume/GRAYBABY_WITNESS_REVERSE_RESUME_REPLAY_V0_1.md`.

## Promotion condition

This object is repository-bound when committed and reviewable. Merge is a separate state transition and must never be implied by draft status.

## Farcaster public-distribution witness — 2026-08-19

Source type: `USER_SUPPLIED_INDEPENDENT_BROWSER_VERIFICATION`  
Cast URL: `https://farcaster.xyz/cmptrwsdm/0x0bb67e6e`  
Author: `@cmptrwsdm`

Canonical body reported as independently verified:

> American Gray Baby 👽🇺🇸  
> Not a ruler. Not a faction. Not a story.  
> An observer with one job:  
> Observe → Receipt → Verify → Check Authority → Replay → Hold or Prove.  
> Every public claim gets a public witness. Every missing receipt stays HOLD.  
> $GRAYBABY · Base · Receipt Standard v0.1 🧅⚙️

Reported browser/screenshot witness state:

```text
CAST_URL = VERIFIED
CAST_AUTHOR = VERIFIED
CAST_BODY = VERIFIED
GRAYBABY_BASE_RECEIPT_STANDARD_TEXT = VERIFIED
IMAGE_PRESENCE = VERIFIED
IMAGE_VISUAL_CONTENT = VERIFIED
RELATIVE_TIMESTAMP_DISPLAY = VERIFIED_AS_3_TO_4_MINUTES_AT_OBSERVATION
PUBLIC_DISTRIBUTION_WITNESS = CONFIRMED
```

Visual-content witness reports the rendered American Gray Baby Receipt Standard v0.1 graphic with central gray alien observer, Observe / Receipt / Verify / Authority / Replay / Hold-Proven process nodes, `$GRAYBABY`, `Base`, `PUBLIC_RECEIPT_ARTIFACT`, and all authority flags shown as `FALSE`.

Expected canonical source-image receipt:

```text
EXPECTED_IMAGE_SHA256 = 615f57d1965d2ae1982d60d7e24f42a3d84264558b9cea303ef7bff3b3be5d19
ABSOLUTE_CAST_TIMESTAMP = HOLD_NOT_BOUND
CAST_HOSTED_IMAGE_BYTE_SHA256 = HOLD_NOT_BOUND
BYTE_FOR_BYTE_IMAGE_EQUIVALENCE = HOLD_NOT_BOUND
UNDERLYING_EXTERNAL_CLAIMS = HOLD_UNTIL_PRIMARY_RECEIPT
```

This witness promotes only public distribution of the bounded Gray Baby artifact. It does not create proof of production deployment, employment, credentials, institutional authority, CISA collaboration, Medusa victim counts, or any other underlying external claim.
