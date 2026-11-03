# SEARCH_MISS_CLASSIFICATION_V0_1

STATUS = PROVISIONAL
CANON = FALSE
AUTHORITY_CREATED = FALSE
FINAL_DECISION = HUMAN
CONTRAPOSITIVE_RECEIPT_BOUNDARY = NOT_OPENED

## Membrane

NOT_FOUND != ABSENT
SEARCH_MISS != EXISTENTIAL_NEGATION
SEARCH_MISS != RULE_NONEXISTENCE
SEARCH_MISS != OBJECT_NONEXISTENCE

FOUND -> EXISTS
NOT_FOUND -/-> ABSENT

Absence requires separate proof from an exhaustive registry, a closed enumeration, or another source whose scope licenses existential negation.

## Typed search result

```yaml
SEARCH_RESULT:
  query_id:
  searched_surface:
  scope:
  branch_or_version:
  query_expression:
  observed_at:
  result_state:
    - FOUND
    - NOT_FOUND
    - SEARCH_UNAVAILABLE
    - SEARCH_PARTIAL
    - UNKNOWN
  coverage_state:
    - EXACT_TARGET
    - BOUNDED_SCOPE
    - NONEXHAUSTIVE
    - UNKNOWN
  existential_state:
    - EXISTS
    - ABSENCE_ESTABLISHED
    - NOT_ESTABLISHED
```

## Current connector observation

GitHub exact-path checks on branch:

`recusal-first-reciprocal-actor-state-v0-1`

Targets:

- `artifacts/SEARCH_MISS_CLASSIFICATION_V0_1.md`
- `artifacts/write_interval_executed_readback_v0_3_2.md`

Observed before creation in this run:

```text
result_state = NOT_FOUND
coverage_state = EXACT_TARGET / BOUNDED_TO_ONE_BRANCH
existential_state = NOT_ESTABLISHED
```

Google Drive title searches in the selected project account for:

- `SEARCH_MISS_CLASSIFICATION_V0_1`
- `write_interval_executed_readback_v0_3_2`

returned zero matches in the searched document-title surface.

Typed result:

```text
result_state = NOT_FOUND
coverage_state = BOUNDED_SCOPE
existential_state = NOT_ESTABLISHED
```

The GitHub exact-path miss and Drive title-search miss are separate observations. Neither proves global absence.

## Open alternatives after an ordinary miss

```text
ALTERNATE_NAME   = OPEN
ALTERNATE_PATH   = OPEN
ALTERNATE_BRANCH = OPEN
ALTERNATE_REPO   = OPEN
PRIVATE_OBJECT   = UNRESOLVED
UNINDEXED_OBJECT = UNRESOLVED
```

## Search result versus existence proposition

Search is an observation operation.
Existence is a proposition.

A search result may provide evidence about existence. It may not silently become the proposition's truth value.

## Prior user-declared search

A prior user declaration states that a code search of `jsonwisdom/COMPUTERWISDOM` for three terms returned count 0.

That prior declaration remains typed as a declaration unless independently replayed with the exact three query terms and scope.

```text
PRIOR_DECLARED_RESULT = NOT_FOUND
PRIOR_DECLARED_COVERAGE = BOUNDED_SCOPE
PRIOR_DECLARED_EXISTENCE = NOT_ESTABLISHED
```

NO_BACK_EDGES = TRUE
CANON = FALSE
AUTHORITY_CREATED = FALSE
