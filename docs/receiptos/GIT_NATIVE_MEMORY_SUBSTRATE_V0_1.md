# ReceiptOS Git-Native Memory Substrate v0.1

Status: REVIEW_ONLY / DRAFT / UNMERGED

## Architectural inversion

ReceiptOS MUST NOT duplicate history primitives that Git already provides.

```text
JASON / OWNER
    |
    v
  GIT DAG
    |
    +-- blob  = content object / evidence bytes
    +-- tree  = exact named directory snapshot
    +-- commit = tree + parent history + author/committer metadata + message
    +-- ref   = movable name pointing into the graph
    +-- merge = commit with multiple parents / history convergence
    +-- annotated signed tag = cryptographic checkpoint candidate
    +-- remote = replication / transport surface

JAY / EXPLORER
    |
    +-- voice
    +-- search
    +-- dice
    +-- reverse replay
    +-- graphical debugger
```

The existing ReceiptOS regression already establishes:

```text
SAME ENDPOINT != SAME HISTORY
STATE_HASH_EQUAL != HISTORY_HASH_EQUAL
ENDPOINT != HISTORY
```

Git gives this architecture a native substrate:

```text
git_tree_oid   = repository-native state commitment
git_commit_oid = repository-native history commitment
```

Two commits may point to the same tree while having different parent histories. Therefore:

```text
SAME_TREE_OID != SAME_COMMIT_OID
SAME_STATE != SAME_HISTORY
```

## ReceiptOS responsibility after inversion

ReceiptOS remains necessary, but its job changes.

ReceiptOS owns semantic and verification fields that Git does not prove by itself:

- claim classification
- evidence/source typing
- authority/consent boundaries
- PASS | HOLD | CONFLICT | REJECT
- portable content digests
- external timestamp/witness bindings
- human promotion policy
- replay interpretation
- completeness / omission warnings

Recommended receipt bindings:

```text
git_object_format
git_blob_oid
git_tree_oid
git_commit_oid
git_tag_oid              # optional
content_sha256            # portable receipt identifier
external_log_entry        # optional ALMS / transparency-log pointer
external_inclusion_proof  # optional
```

`content_sha256` remains useful because Git object IDs are repository-object-format-native and include Git object framing; they are not a universal portable receipt identifier.

## ALMS responsibility

The ALMS transparency log remains complementary rather than redundant.

Git refs are movable and unreachable Git objects can eventually be pruned. The external append-only log supplies a separate witness surface with inclusion proofs and public replay.

```text
GIT DAG = machine history substrate
RECEIPTOS = meaning + verification
ALMS MERKLE LOG = external append-only witness / inclusion proof
GITHUB = transport + collaboration + rendering surface
OWNER = consequential promotion authority
```

## Signed-tag boundary

An annotated signed tag MAY represent an owner checkpoint or promotion candidate, but the signature proves only that the signing key signed the tagged object. It does not prove the semantic truth of the underlying claims.

```text
SIGNED_TAG != TRUTH
SIGNED_TAG != LEGAL_AUTHORITY
SIGNED_TAG != TRUSTED_TIMESTAMP
```

## Timestamp boundary

Git commit author/committer dates are metadata, not trusted timestamps. Git permits author and committer dates to be supplied by the caller.

```text
GIT_DATE != TRUSTED_TIME
COMMIT_ORDER != WALL_CLOCK_PROOF
```

External timestamping or transparency-log witnesses remain separate when trusted time matters.

## Ref-storage boundary

A branch is logically a ref, not necessarily a loose text file. Git may store refs as loose refs, `packed-refs`, or reftable-backed storage.

```text
BRANCH = LOGICAL_REF
BRANCH != GUARANTEED_TEXT_FILE
```

## Object-retention boundary

Git objects are immutable once addressed, but unreachable objects are not guaranteed to remain forever. Garbage collection may eventually prune them.

```text
OBJECT_IMMUTABLE != OBJECT_PERMANENTLY_RETAINED
REACHABILITY != TRUTH
```

## Machine regression

`tools/verify_receiptos_git_native_history_v0_1.py` constructs two native Git histories:

Path A:

```text
FINAL_TREE -> FINAL_COMMIT_A (no parent)
```

Path B:

```text
EVENT_TREE -> HISTORY_COMMIT_B -> FINAL_COMMIT_B
                               \
                                -> FINAL_TREE
```

Both final commits point to the exact same `FINAL_TREE`. The final commit metadata/message are held equal; Path B differs by parent history.

Expected invariant:

```text
FINAL_TREE_A == FINAL_TREE_B  -> TRUE
FINAL_COMMIT_A == FINAL_COMMIT_B -> FALSE
```

The fixture also recomputes the existing portable ReceiptOS state commitment:

```text
sha256:30cc29ff65e9f94595a0c1c0e35ad4e58692d1dea4c4ed4badf83719435cfdd9
```

## Product value

```text
Git = Jason's machine-history substrate
ReceiptOS = semantic / verification membrane
Jason = owner
Jay = query / replay interface
Homepage = graphical debugger for the Git + ReceiptOS graph
```

The interface may traverse history; it MUST NOT rewrite history or promote authority without an explicit owner action.

## Hard membrane

```text
GIT_COMMIT != FACT_TRUE
GIT_HASH != COMPLETE_RECORD
TREE_OID != CAUSATION
COMMIT_OID != TRUSTED_TIMESTAMP
SIGNED_TAG != SEMANTIC_TRUTH
REMOTE != CANON
GITHUB != DATABASE_OF_TRUTH
MODEL_OUTPUT != RECEIPT
REPLAY_RESULT != AUTHORITY
MERGE_AUTHORIZED = FALSE
AUTHORITY_CREATED = FALSE
```

References in the existing estate:

- `tests/receiptos_history_vectors_v0_1/README.md`
- `receipts-engine-v1/docs/ALMS_TRANSPARENCY_LOG_SPEC_V0_1.md`

This document proposes a substrate refactor. It does not rewrite prior receipts and does not merge or promote any branch.