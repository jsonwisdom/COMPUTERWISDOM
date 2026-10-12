# Amy K Dual Onion Sacks — Gemini Forward + Reverse / Fortnight Timing v0.1

**Class:** public-record replay / corpus topology / non-authority  
**Authority created:** false  
**Proof inferred:** false

## Purpose

Expand **Amy's Reach** only as an observable public-record topology: institutions, archives, statements, votes, confirmations, appropriations, agency mirrors, courts, and oversight records that can be linked by dated receipts.

```text
REACH != POWER
REACH != CONTROL
REACH != COMPLICITY
```

## Dual Onion Sacks

### Sack A — Forward

```text
PRIMARY BYTE
-> HASH
-> SOURCE IDENTITY
-> DATE
-> OFFICE HELD
-> AUTHORITY
-> MONEY / EXECUTION
-> OUTCOME
-> OVERSIGHT
```

### Sack B — Reverse

```text
LATER CLAIM
-> EXACT WORDING
-> CLAIM DATE
-> OFFICE HELD
-> PRIOR ACTION CLAIMED
-> PRIMARY RECEIPT
-> AUTHORITY EDGE
-> MONEY / EXECUTION EDGE
-> OUTCOME
```

The two sacks share receipts but do not inherit conclusions from each other.

```text
FORWARD_RESULT != REVERSE_RESULT
SAME_RECEIPT != SAME_PROPOSITION
```

## Gemini Forward + Reverse

`Gemini-F` is chronology-first replay: **what happened next from this receipt?**  
`Gemini-R` is provenance-first replay: **what prior receipt must exist for this later claim to survive?**

A proposition strengthens only when the two independent passes converge on the same dated edge. Divergence yields `HOLD` or `CONFLICT`; it never authorizes an invented bridge.

## Public-record reach map

Observable source families include:

- Hennepin County Attorney era records and Minnesota data-practices history
- official U.S. Senate releases and issue pages
- Congressional Record / GovInfo speaker-attributed remarks
- Congress.gov legislative and amendment activity
- Judiciary / confirmation records
- appropriations and public-law records
- DOJ / EOUSA / USAO-MN agency-held correspondence and prosecution records
- USDA/FNS child-nutrition program records
- Minnesota MDE records
- Minnesota OLA oversight reports
- Minnesota courts only where a specific docket creates a judicial edge
- campaign materials as campaign records only

Hard membrane:

```text
PUBLIC APPEARANCE != EXECUTION
RECOMMENDATION != APPOINTMENT AUTHORITY
APPROPRIATION VOTE != DISTRICT-SPECIFIC FTE DELTA
PRESS RELEASE != INVESTIGATION
COURT RECORD != EXECUTIVE ACTION
```

## Fortnight timing

A fortnight is a **14-day analytical bucket**, not a statutory deadline.

For an anchor `T0`:

```text
FORTNIGHT_INDEX(event) = floor((event_date - T0) / 14 days)
FORTNIGHT_OFFSET(event) = (event_date - T0) mod 14 days
```

Each bucket records:

- declared records `D[k]`
- retrieved and integrity-checked records `R[k]`
- newly acquired source hashes
- Forward claims opened/closed
- Reverse claims opened/closed
- time-gap deltas
- evidence-state changes

```text
FORTNIGHT_DELTA[k] = MANIFEST_HASH[k] != MANIFEST_HASH[k-1]
```

A fortnight with no new public receipt is only an observed corpus state.

```text
NO_CHANGE != SILENCE_PROVEN
NO_CHANGE != MOTIVE
NO_CHANGE != CONCEALMENT
NO_CHANGE != DARVO
```

## Quadratic corpus pressure

```text
Q[k,c] = A[k,c] * (D[k,c] - R[k,c])^2 / P[t]
```

Where:

- `D` = officially declared/known documents
- `R` = documents acquired and integrity-checked
- `A` = predeclared relevance/authority weight
- `P[t]` = declared year-specific population denominator where population normalization is relevant

`Q` measures documentary incompleteness pressure only.

```text
Q != GUILT
Q != CORRUPTION
Q != LEGALITY
Q != DARVO
```

## Explicit replay registry

Replay-critical version axes are independent:

```text
schema_version
canonical_version
serializer_version
hash_algorithm
```

`canonical_version` must never default from `schema_version`.

Implemented reference registry:

```text
src/replay_registry_v0_2.py
```

The current `ERS_V0_1` entry explicitly declares:

```text
canonical_version = ERS_CANONICAL_V1_0
serializer_version = JSON_SORTED_COMPACT_UTF8_V1_0
hash_algorithm = sha256
canonicalizer = canonicalize_ers_v0_1
```

No replay-critical defaults exist.

## Permanent regression contract

```text
tests/replay/test_all_artifacts.py
tests/fixtures/replay_regression_manifest_v0_2.json
```

Every artifact admitted to the manifest must recompute to its stored expected replay hash using only registry-declared transforms.

Initial frozen vectors:

```text
examples/event_example.json
examples/observation_example.json
```

A schema change may reuse a canonical version only through an explicit registry entry. A canonicalization change requires an explicit canonical-version change or new schema-to-canonical mapping.

## Minnesota normalization next

Primary-source-first sequence:

1. freeze version semantics
2. freeze replay regression suite
3. expand Minnesota Legislature adapter: bills, companions, roll calls, committees, Revisor/chapter identities
4. compare equivalent Minnesota records against aggregator outputs afterward
5. add jurisdictions after primary-source normalization is stable

The replay kernel becomes the compatibility contract. Adapters remain the moving parts.

## OpenAI runtime lane

OpenAI may assist extraction, normalization proposals, source classification, and Forward/Reverse comparison.

```text
MODEL_OUTPUT != PRIMARY BYTE
MODEL_NORMALIZATION != OFFICIAL RECORD
MODEL_CONFIDENCE != EVIDENCE STATE
```

No OpenAI API key is required for this deterministic registry, regression suite, or document architecture. If an API-backed runtime is added later, model outputs enter as separate generated artifacts with provenance and never replace source bytes.

## Standing order

> **ONE SACK. TWO DIRECTIONS. SAME RECEIPTS. EXPLICIT VERSIONS. NO INVENTED EDGES.**
