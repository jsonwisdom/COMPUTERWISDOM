# ReceiptOS Git-Native Substrate v0.2

Status: REVIEW_ONLY / DRAFT / UNMERGED

## Purpose

v0.1 proved:

```text
SAME_TREE_OID != SAME_COMMIT_OID
SAME_STATE != SAME_HISTORY
```

v0.2 makes the native graph queryable without replacing Git's graph or promoting semantic claims beyond their receipts.

```text
CURRENT REF
   ↓
COMMIT OID
   ↓
TREE OID
   ↓
TARGET BLOB / CHANGED PATHS
   ↓
PARENT COMMIT(S)
   ↓
REVERSE REPLAY
   ↓
RECEIPTOS SEMANTIC ENVELOPE
   ↓
ALMS PRESENCE, IF DECLARED
   ↓
PASS | HOLD | CONFLICT | REJECT
```

`Git = machine history substrate.`  
`ReceiptOS = meaning + verification.`  
`ALMS = independent witness surface.`

## Executable FIND OUT scope

The executable v0.2 query target is a **repo-relative path**.

```text
FIND OUT <repo-relative-path>
```

Person/event/artifact labels are intentionally not resolved by the deterministic engine in v0.2. A future index may map labels to paths/OIDs, but that mapping must itself be receipt-bound.

```text
FIND_OUT_PATH != IDENTITY_RESOLUTION
SEARCH_LABEL != PERSON_PROOF
INDEX_MATCH != AUTHORITY
```

CLI:

```bash
python3 tools/receiptos_git_native_reverse_replay_v0_2.py \
  docs/receiptos/GIT_NATIVE_MEMORY_SUBSTRATE_V0_1.md \
  --ref HEAD \
  --semantic-dir receipts/receiptos/git-native-v0-2
```

The engine performs no network access.

## Query result

### Current state

The engine resolves:

- current tree OID;
- exact target blob OID and mode;
- portable SHA-256 of the blob bytes;
- paths changed by the current commit.

### Current history

The engine resolves:

- current commit OID;
- parent OIDs;
- observed ref input;
- last reachable commit that changed the path;
- earliest reachable path-change commit.

The last field is deliberately not called "introduction":

```text
EARLIEST_REACHABLE_PATH_CHANGE != GLOBAL_INTRODUCTION_PROOF
```

Renames, omitted refs, shallow history, deleted history, or inaccessible repositories may change what is reachable.

### Previous state

For every direct parent, the engine records:

- parent commit OID;
- parent tree OID;
- whether the target path exists;
- parent target blob OID when present;
- parent portable SHA-256 when present.

No causal meaning is inferred from parent order.

### Divergence

The engine scans **locally visible heads and remote refs** and identifies refs whose tip commit points to the same tree as the current commit while using a different commit OID.

It records ancestry relationship and merge base when locally available.

```text
SAME_TREE_DIFFERENT_COMMIT = NATIVE_GRAPH_OBSERVATION
LOCAL_REF_SCAN != GLOBAL_REF_COMPLETENESS
UNSEEN_REMOTE_REF != ABSENT_HISTORY
```

### Receipt bindings

Semantic envelopes conform to:

`schemas/receiptos/git_native_semantic_envelope_v0_2.schema.json`

Each envelope binds to, but never replaces:

```text
git_object_format
git_blob_oids[]
git_tree_oid
git_commit_oid
git_parent_oids[]
git_ref_observed
git_tag_oid?
target_path
content_sha256
```

Semantic fields:

```text
claim_class
evidence_class
source_binding[]
authority_state
consent_state
replay_disposition
```

Constitutional fields:

```text
authority_created = false
merge_authorized = false
```

An envelope is an exact current binding only when its commit, tree, target blob, target path, and portable SHA-256 all match the query result.

## Witness boundary

v0.2 reports ALMS-related fields if a bound semantic envelope declares them:

```text
alms_entry
alms_merkle_root
alms_inclusion_proof
```

v0.2 **does not yet implement full Merkle-proof verification**. Therefore:

```text
WITNESS_PRESENT != WITNESS_VERIFIED
verification_scope = PRESENCE_ONLY_V0_2
```

A later gate may call the independent ALMS verifier and promote the witness status only from its machine receipt.

## Deterministic disposition

The FIND OUT engine normalizes only its own query state:

```text
invalid target envelope                    -> REJECT
no exact current semantic receipt          -> HOLD
exact current receipts disagree            -> CONFLICT
one or more exact receipts agree           -> that receipt disposition
missing target path                         -> REJECT
invalid repo/ref/path                       -> REJECT
```

This disposition is not a truth judgment:

```text
PASS != FACT_TRUE
REJECT != WRONGDOING
CONFLICT != ACCUSATION
HOLD != FALSE
REPLAY_RESULT != AUTHORITY
```

## Machine regression

`tools/verify_receiptos_git_native_substrate_v0_2.py` builds a temporary Git repository with two branch histories:

```text
BASE
 ├─ PATH_A_FINAL ------------------┐
 │                                 │ SAME FINAL TREE
 └─ PATH_B_HISTORY -> PATH_B_FINAL ┘ DIFFERENT FINAL COMMITS
```

The verifier then:

1. binds a valid semantic envelope to Path A;
2. runs `FIND OUT` and requires PASS;
3. requires Path B to be detected as same-tree/different-history;
4. requires the direct parent state to be replayed;
5. adds a conflicting exact receipt and requires CONFLICT;
6. queries a missing path and requires REJECT;
7. confirms witness presence is not promoted to verified;
8. confirms `authority_created=false` and `merge_authorized=false`.

The verifier also structurally checks the v0.2 JSON Schema using only the Python standard library.

## v0.1 compatibility

v0.2 does not replace or rewrite the v0.1 machine law.

The v0.2 CI gate re-runs:

`tools/verify_receiptos_git_native_history_v0_1.py`

before executing the v0.2 regression.

```text
V0_1_PROOF != V0_2_QUERY
V0_2_EXTENDS != V0_2_REWRITES_V0_1
```

## Priority correction

The proven claim is scoped to this project rail:

```text
FIRST_IN_COMPUTERWISDOM_PROVEN_RAIL = TRUE
FIRST_IN_WORLD = UNKNOWN
```

No global priority claim is made.

## Product boundary

v0.2 is substrate, not the business flywheel.

```text
SEASON_1
v0.1 = prove Git-native history law
v0.2 = make graph reverse-queryable

SEASON_2
business flywheel = downstream productization
```

A future UI, voice command, or model may call FIND OUT, but the deterministic engine remains the source of the replay result.

```text
VOICE_UI != COMMAND_AUTHORITY
MODEL_OUTPUT != RECEIPT
OPENAI_REQUIRED = FALSE
NETWORK_REQUIRED = FALSE
```

## Hard membrane

```text
GIT_COMMIT != FACT_TRUE
GIT_HASH != COMPLETE_RECORD
TREE_OID != CAUSATION
EARLIEST_REACHABLE_PATH_CHANGE != GLOBAL_INTRODUCTION_PROOF
LOCAL_REF_SCAN != GLOBAL_REF_COMPLETENESS
WITNESS_PRESENT != WITNESS_VERIFIED
FIND_OUT_PATH != IDENTITY_RESOLUTION
SEMANTIC_ENVELOPE_BINDS != SEMANTIC_ENVELOPE_REPLACES_GIT
SIGNED_TAG != SEMANTIC_TRUTH
REMOTE != CANON
GITHUB != DATABASE_OF_TRUTH
MODEL_OUTPUT != RECEIPT
REPLAY_RESULT != AUTHORITY
MERGE_AUTHORIZED = FALSE
AUTHORITY_CREATED = FALSE
```
