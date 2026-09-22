# TECHNICAL_CONTROLS_BOUNDARY_DECLARATION_V0_1

STATUS: CANDIDATE / UNSEATED
AUTHORITY: false
PROMOTION_ALLOWED: false
BINDING_CREATED: false
LAYER_DIGEST: NONE
PARENT_BIND: HOLD

## Purpose

Declare the next technical-controls artifact class without seating M5, M6, B4, CHAT_G5, or P-HASH-SWAP.

This declaration records three distinct arrows and forbids their collapse:

INHERITS != CONSTRAINED_BY
CONSTRAINED_BY != PARENT
DOES_NOT_INHERIT != ABSENCE

## Inheritance

INHERITS:
- PWC-001

Meaning:
- PWC-001 contributes the temporal envelope only.
- No technical-control taxonomy is inherited from PWC-001.
- Circular derivation back into PWC-001 is blocked.

## Constraint rule

CONSTRAINT_RULE:
- HASH_NE_TRUTH

The rule is the boundary. The repository SHAs below are byte-identity anchors for the artifacts expressing that boundary; the SHAs are not the rule itself.

CONSTRAINT_ANCHORS:
- 61f2baa59f3cfdd4e8a1762773297749a2c7fec4
  - HASH_MATCH != CLAIM_VALIDITY
  - BYTE_IDENTITY != SUBSTANTIVE_TRUTH
- e4b0c35edd5cccd8f9d51c8f367a69b5d2441a98
  - RECEIPT_HASHED -> TRUTH = DENIED
  - RECEIPT_ANCHORED -> TRUTH = DENIED
  - REPLAY_MATCH -> LIABILITY = DENIED
- e04c6599bf33fb2de4f1b1f5610c59aef009030e
  - preservation is not validation
  - replay is not truth by itself
- 5e8fa9b68a703cf2aec0242ca704f8173509ea62
  - SOURCE_VERIFIED != CLAIM_TRUE
  - CLAIM_TRUE != AUTHORITY
  - DO NOT TURN A HASH INTO TRUTH

## Constraint directionality

CONSTRAINT FLOWS:
repository source -> this artifact

CONSTRAINT DOES NOT FLOW:
repository source -> prior artifact -> this artifact

Constraint inheritance is non-transitive. A downstream artifact must cite and verify its repository constraint source directly rather than inheriting a prior artifact's citation as authority.

## Negative inheritance

DOES_NOT_INHERIT:
- CHAT_G5
- P-HASH-SWAP

CHAT_G5_PARENT: HOLD
P_HASH_SWAP: NOT_OBSERVED

The repository G5 Revision Gate and the conversation-local G5 naming-trap class remain distinct namespaces.

REPO_G5 != CHAT_G5

## Hash role boundary

P-HASH-SWAP:
- digest cited under the wrong object or role

HASH_NE_TRUTH:
- correct digest promoted into substantive truth, validity, liability, enforcement, or authority

P-HASH-SWAP != HASH_NE_TRUTH

## Drive mirror boundary

DRIVE_EXACT_MIRROR_SEARCH: NO_MATCH
MIRROR_EXISTENCE: UNRESOLVED
MIRROR_EQUIVALENCE: NOT_ESTABLISHED
IMPORT_ALLOWED: false

A search miss does not prove nonexistence.

## Standing holds

M5: UNSEATED
M6: UNSEATED
B4: UNSEATED
T_EMPTY: HOLDS
PWC_001_CIRCULARITY: BLOCKED

## Mutation classification

Creating or storing this candidate is a storage mutation only.

STORAGE_MUTATION != PROMOTION
STORAGE_MUTATION != BINDING
STORAGE_MUTATION != AUTHORITY
STORAGE_MUTATION != LAYER_DIGEST
GIT_BLOB_SHA != TECHNICAL_CONTROLS_LAYER_DIGEST

No technical-controls digest is computed or assigned by this declaration.

## Operator boundary

USER OWNS THE SWITCHBOARD.
AGENT MAINTAINS THE STATE.
RECEIPTS EXPLAIN THE CHANGE.

Gray Baby observes first, preserves viable paths, and lets receipts decide.
