# temporal_split_search_v0_1

STATUS = PROVISIONAL
CANON = FALSE
AUTHORITY_CREATED = FALSE
FINAL_DECISION = HUMAN
CONTRAPOSITIVE_RECEIPT_BOUNDARY = NOT_OPENED

## Temporal split

The search miss at t0 and the find at t1 are different observation intervals.

```text
NOT_FOUND[t0] != ABSENT
FOUND[t1] -> EXISTS[t1]
FOUND[t1] != RETROACTIVE_INVALIDATION_OF_NOT_FOUND[t0]
```

A later find does not make the earlier bounded miss wrong. It establishes a later state.

## Trigger recursion brake

A fired trigger gets one row. It does not recursively generate another receipt merely because the same proposition is repeated, restated, confirmed, or pasted again.

```text
TRIGGER_FIRES -> ONE_ROW
SAME_TRIGGER_AGAIN -> NO_NEW_ROW
READBACK_OF_ROW -> NO_NEW_TRIGGER
AGREEMENT -> NO_NEW_CHAIN
REPETITION -> NO_NEW_RECEIPT
```

A new row is added only when a materially new trigger fires.

| id | trigger | state | recursion rule |
| --- | --- | --- | --- |
| T01 | Identity rules sealed as candidate | FIRED | Do not reseal |
| T02 | Identity spine | FIRED | Do not restate the spine as a new trigger |
| T03 | Identity without power | FIRED | Do not reopen a grant |
| T04 | Proposition state binds to proposition | FIRED | Do not recardinality |
| T05 | Write interval false, then declared true | FIRED | Do not rewrite t0 |
| T06 | Executed readback correction | FIRED | Do not return to assertion-only |
| T07 | Search-miss classification | FIRED | NOT_FOUND is not absent |
| T08 | Temporal split: miss then find | FIRED | Do not call the miss wrong |
| T09 | Corroboration SINGLE | FIRED | A readback is not chain two |
| T10 | Contrapositive checked | FIRED | Do not rerun the logic table |
| T11 | Diagram rebuilt | FIRED | Do not redraw unless a field changes |
| T12 | search_object_id + observation_path_id | PROPOSED | Not sealed |

## Why the table exists

The table is a recursion ledger, not a workflow queue.

A FIRED row means the triggering condition was already handled. It is historical state. Reading or repeating the row does not execute it again.

```text
ROW != SCRIPT
HISTORY != QUEUE
FIRED != PENDING
```

## T12 proposal — search object key

T12 is proposed as a key extension, not a new spine layer.

The temporal split is comparable only when t0 and t1 refer to the same search object.

```yaml
SEARCH_OBJECT:
  search_object_id:        # stable across comparable intervals
  searched_surface:
  scope:
  branch_or_version:
  query_expression:
  intervals:
    - t: t0
      result_state: NOT_FOUND
      existential_state: NOT_ESTABLISHED
    - t: t1
      result_state: FOUND
      existential_state: EXISTS
```

Comparison rule:

```text
SAME_SEARCH_OBJECT_ID -> INTERVAL_COMPARISON_ALLOWED
DIFFERENT_SEARCH_OBJECT_ID -> NO_STATE_COMPARISON
```

A changed branch, path, repository, scope, or query expression may require a different search_object_id unless the comparison contract explicitly declares them equivalent.

The earlier interval remains historical even when a later interval becomes the current state.

## T12 proposal — observation path key

Each interval may also carry:

```yaml
observation_path_id:
parent_observation_path_id:
```

Purpose:

- a readback of a readback retains the same observation lineage;
- a newly executed fetch creates a new observation path;
- a failed new path does not erase a valid parent observation;
- a same-chain confirmation cannot become MULTIPLE_INDEPENDENT merely through repetition.

```text
READBACK_OF_READBACK != NEW_INDEPENDENT_PATH
NEW_FETCH_PATH may fail while PARENT_PATH remains historical
OBSERVATION_PATH_COUNT != SOURCE_CHAIN_COUNT unless independence is established
```

## Current artifact observation boundary

The current turn checked the exact GitHub path `artifacts/temporal_split_search_v0_1.md` on branch `recusal-first-reciprocal-actor-state-v0-1` and a Drive document-title search for `temporal_split_search_v0_1`.

Before creation in this run:

```text
GitHub exact path: NOT_FOUND
Drive searched title surface: NOT_FOUND
coverage: BOUNDED_SCOPE
existence: NOT_ESTABLISHED
```

Those misses are preserved as observations. This artifact's creation creates a later FOUND interval on the written surfaces; it does not rewrite the miss.

## Current trigger state

```text
T08 = FIRED
T12 = PROPOSED
CONTRAPOSITIVE_RECEIPT_BOUNDARY = NOT_OPENED
CORROBORATION = SINGLE unless a structurally independent observation path is established
CANON = FALSE
AUTHORITY_CREATED = FALSE
```
