# Gray Baby Platform Preparedness v0.1

**Reviewed:** 2026-08-15  
**Scope:** Base / GitHub / Farcaster / Zora / Lean  
**Class:** preparedness and verification doctrine  
**Authority created:** false

This document records what each platform can prove, what it cannot prove, and which evidence must remain separate before Gray Baby permits promotion into a replay receipt.

## 1. Base

Official references reviewed:
- https://docs.base.org/base-chain/quickstart/connecting-to-base
- https://docs.base.org/base-account/overview/what-is-base-account
- https://docs.base.org/base-chain/api-reference/rpc-overview

Current network anchors:

```text
BASE_MAINNET_CHAIN_ID = 8453
BASE_SEPOLIA_CHAIN_ID = 84532
```

Preparedness gates:

```text
NETWORK_EXPLICIT
CHAIN_ID_VERIFIED
SIGNER_PATH_IDENTIFIED
TRANSACTION_HASH_REQUIRED_FOR_TRANSACTION_CLAIM
CONTRACT_ADDRESS_REQUIRED_FOR_DEPLOYMENT_CLAIM
READBACK_REQUIRED_FOR_STATE_CLAIM
PRIVATE_KEY_NEVER_COMMITTED
```

Boundaries:

```text
WALLET_CONNECTED != ADDRESS_CONTROL_PROVEN_FOR_ALL_CONTEXTS
ADDRESS_CONTROL   != IDENTITY_BINDING
TRANSACTION       != AUTHORITY
ATTESTATION       != TRUTH
BASE_RECORD       != BOXD_MUTATION
```

Base Account is a smart-wallet-backed account layer. Account or wallet capabilities may support authentication, signing, or payments, but those capabilities do not silently create civic, legal, family, or ReplayOS authority.

## 2. GitHub

Official reference reviewed:
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch

Current workflow-dispatch rule:

```text
workflow_dispatch ref = branch or tag
GITHUB_REF            = selected branch or tag
GITHUB_SHA            = last commit on selected branch or tag
workflow file          = must exist on default branch to dispatch
```

For exact-SHA validation, Gray Baby requires the workflow itself to compare the observed checkout SHA against an expected SHA and fail closed if they differ.

```text
EXPECTED_SHA
  ↓
DISPATCH ON BRANCH/TAG
  ↓
ASSERT GITHUB_SHA == EXPECTED_SHA
  ↓
ASSERT git rev-parse HEAD == EXPECTED_SHA
  ↓
RUN READ-ONLY VALIDATION
  ↓
CAPTURE RUN + ARTIFACT RECEIPT
```

Boundaries:

```text
GREEN_CHECK != MERGE
MERGE       != AUTHORITY
WORKFLOW_RUN != SOURCE_TRUTH
RUN_METADATA_SHA != CHECKED_OUT_SHA unless verified
CI_PASS     != AUTHORITY_CREATED
```

A workflow may produce logs and artifacts without changing Git history. Therefore `NO_GIT_HISTORY_MUTATION` must not be stated as `NO_EXECUTION_RECORD`.

## 3. Farcaster

Official reference reviewed:
- https://docs.farcaster.xyz/

Current developer surfaces include Mini Apps, Sign In with Farcaster, and protocol/data access through Farcaster infrastructure.

Preparedness gates:

```text
OBJECT_TYPE_IDENTIFIED
SOURCE_CLIENT_OR_PROTOCOL_SURFACE_RECORDED
TIMESTAMP_CAPTURED
CONTENT_OR_REFERENCE_PRESERVED
AUTHENTICATION_EVIDENCE_SEPARATE_FROM_CLAIM_CONTENT
SOCIAL_DISTRIBUTION_SEPARATE_FROM_FACT_PROMOTION
```

Boundaries:

```text
CAST_EXISTS      != CLAIM_TRUE
SOCIAL_PROFILE   != LEGAL_IDENTITY
SIGN_IN_SUCCESS  != AUTHORITY
ENGAGEMENT       != CONSENSUS
VIRALITY         != EVIDENCE_WEIGHT
```

Farcaster is a distribution and identity/authentication surface for social applications. Gray Baby treats casts, profiles, Mini Apps, and sign-in events as platform objects that may be preserved and compared, not as truth machines.

## 4. Zora

Official reference reviewed:
- https://docs.zora.co/

Current developer surfaces center on Zora Coins, the Coins SDK, protocol queries, profiles, balances, activity, and agent integrations.

Preparedness gates:

```text
CHAIN_OBJECT_IDENTIFIED
CONTRACT_OR_COIN_REFERENCE_CAPTURED
TRANSACTION_OR_QUERY_SOURCE_RECORDED
BLOCK/TIME_CONTEXT_RECORDED_WHEN_AVAILABLE
BYTE_OR_CANONICAL_PAYLOAD_DIGESTED_WHEN LOCAL ARTIFACT EXISTS
SERIES_MEMBERSHIP_REQUIRES_EXPLICIT EVIDENCE
```

Boundaries:

```text
COIN_EXISTS          != CREATOR_IDENTITY_PROVEN
TITLE_MATCH          != SERIES_MEMBERSHIP
PROFILE_ASSOCIATION  != WALLET_CONTROL
TRANSACTION          != INTERPRETIVE_TRUTH
INVENTORY_NEIGHBOR   != CANONICAL_LINEAGE
```

This preserves the existing Gray Baby ↔ Zora rule: candidate neighbors remain candidates until explicit evidence binds them.

## 5. Lean / Microsoft Research lineage

Official references reviewed:
- https://lean-lang.org/doc/reference/latest/
- https://www.microsoft.com/en-us/research/project/lean/

Lean is a functional programming language and interactive theorem prover with a small trusted kernel that checks proof terms. Microsoft Research records that Lean originated there in 2013; current language reference material is maintained on the Lean project documentation surface.

Preparedness gates for ReplayOS formalization:

```text
FORMAL_STATEMENT_EXPLICIT
AXIOMS_AND_ASSUMPTIONS_EXPLICIT
LEAN_VERSION_CAPTURED
PROOF_TERM_KERNEL_CHECKED
EXTERNAL_PREMISES_BOUND_TO_SEPARATE_RECEIPTS
```

Critical boundary:

```text
LEAN_PROVES(formal_statement | axioms)
        !=
REAL_WORLD_PREMISES_VERIFIED
```

Lean may prove that a ReplayOS state transition, invariant, hash-comparison rule, or gate follows from formal premises. It cannot independently establish that a screenshot is authentic, a public official made a claim, a statute was in force, or an external byte sequence came from the asserted source. Those premises remain BoxD / provenance work.

## Cross-platform Gray Baby matrix

| Platform | Strong evidence surface | Must not be promoted into |
|---|---|---|
| Base | chain ID, transaction/contract state, signatures when verified | truth, identity, authority |
| GitHub | commit/ref/run/check/artifact state | source truth, authority |
| Farcaster | social object / auth / distribution state | factual consensus, legal identity |
| Zora | coin/protocol/query/transaction state | lineage or creator identity without evidence |
| Lean | machine-checked implication from explicit premises | truth of unverified external premises |

## Universal release gate

```text
SOURCE_PRESENT
BYTE_OR_OBJECT_IDENTITY_VERIFIABLE
TIME_AND_VERSION_CAPTURED
PLATFORM_BOUNDARY_DECLARED
CONTRADICTIONS_PRESERVED
HUMAN_REVIEW_COMPLETE
BOXD_UNCHANGED
AUTHORITY_CREATED = FALSE
```

Preparedness means the object can be tested and replayed. It does not mean the object has been promoted to truth, law, identity, or authority.
