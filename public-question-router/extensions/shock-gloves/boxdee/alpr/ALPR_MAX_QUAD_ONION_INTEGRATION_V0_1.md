# ALPR MAX — Quad Onion Integration v0.1

Status: DRAFT / SOURCE-BOUND / FAIL-CLOSED / UNMERGED

```text
BOXD = INSTITUTIONAL REPLAY CONTAINER
MAX_GRAY_BABY = UNIT-IDENTITY / DRIFT-CHECK EXPLAINER
LEELOO_MULTI_PASS = FAIL-CLOSED PROMOTION GATE
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
SURVEILLANCE_MISCONDUCT_CREATED = FALSE
```

## Purpose

Close the ALPR geometry hole by separating origin search events from downstream network contacts and by preventing synthetic county-normalized stress models from being promoted into observed state activity.

The core correction is unit identity:

```text
ORIGIN_SEARCH != TARGET_NETWORK_CONTACT
TARGET_NETWORK_CONTACT != RECORD_RETURNED
RECORD_RETURNED != HIT
HIT != EXPORT
AVERAGE_ACTIVITY != MACHINE_CAPACITY
COUNTY != HOMOGENEOUS_SENSOR_NODE
SYNTHETIC_PROJECTION != OBSERVED_ACTIVITY
FANOUT_DISTRIBUTION != CONSTANT_SCALAR
```

## O1 — Record / Reality

ALPR evidence objects must preserve the raw audit field identity before any calculation.

```text
SOURCE_ARTIFACT
→ SOURCE_ROW
→ QUERY_EVENT_ID / SEARCH_ID, IF PRESENT
→ ORIGIN_AGENCY
→ SEARCH_TIME + TIMEZONE
→ REASON / CASE NUMBER
→ QUERY PARAMETERS
→ TOTAL_NETWORKS_SEARCHED / FANOUT, IF PRESENT
→ TARGET_NETWORK, IF THIS ROW IS A NETWORK-CONTACT LOG
→ RAW BYTES / HASH / VERSION
→ RECEIPT STATE
```

Hard membrane:

```text
A ROW IN A TARGET NETWORK AUDIT DOES NOT BECOME AN ORIGIN SEARCH EVENT WITHOUT A SOURCE-BOUND ORIGIN / SEARCH-ID EDGE.
```

## O2 — Authority / Law

For each query event, record the source-bound authority and policy path separately from the technical event.

```text
QUERY_EVENT
→ ORIGIN_ACTOR / AGENCY
→ POLICY / STATUTE / AUTHORITY BASIS
→ PURPOSE / REASON / CASE
→ JURISDICTION
→ LIMITS / RETENTION / SHARING RULES
→ REVIEW / APPEAL / PUBLIC-ACCESS PATH
→ AUTHORITY STATE
```

No technical search record alone establishes lawful or unlawful use.

## O3 — Execution / Data

O3 receives a dedicated `QUERY_EVENT` object and separates every downstream unit.

```text
QUERY_EVENT
├── origin_search_event
├── fanout_count
├── network_contacts[]
├── returned_record_count
├── hit_count
├── exports[]
├── retention_events[]
└── sharing_events[]
```

Required query-event fields:

```text
query_event_id
origin_agency
timestamp_utc
source_local_timestamp
source_timezone
query_or_session_id
justification
case_number
query_parameters
fanout_count
source_receipt_ids[]
dedupe_key
state
```

Optional result fields remain null / HOLD when absent:

```text
returned_records
hits
exports
retention
sharing
```

### Network-contact object

```text
network_contact_id
query_event_id
target_network
target_agency
contact_timestamp_utc
source_receipt_ids[]
state
```

The same `query_event_id` may produce many network contacts. Counting those contacts as independent searches is prohibited.

## O4 — Oversight / Correction

```text
QUERY_EVENT / NETWORK_CONTACT
→ AUDIT LOG
→ RETENTION / SHARING REVIEW
→ STATUTORY / POLICY AUDIT
→ INTERNAL REVIEW / OIG / COURT, IF APPLICABLE
→ CORRECTION / DELETION / ACCESS REMEDY
→ VERSION DELTA
→ PUBLIC RECEIPT
→ OVERSIGHT STATE
```

No-response, missing logs, or incomplete public records remain HOLD; they do not become misconduct findings.

## Cross-Onion Joins

```text
O1_TO_O2: observed query / contact → source-bound authority path
O2_TO_O3: authority → actual query execution / fanout / result path
O3_TO_O4: execution → required logging / review / correction path
O4_TO_O1: review / correction → preserved record delta
```

Each join is independently:

`PASS | HOLD | CONFLICT | REJECT`

## Unit Registry

Every numeric field must declare one unit from the allowed registry:

```text
ORIGIN_SEARCH_EVENT
TARGET_NETWORK_CONTACT
RETURNED_RECORD
HIT
EXPORT_EVENT
RETENTION_EVENT
SHARING_EVENT
SECONDS
NETWORKS_PER_QUERY
QUERIES_PER_SECOND
CONTACTS_PER_SECOND
```

A calculation may not silently change units.

## Dedupe Contract

Cross-network state comparisons require a dedupe key.

Priority:

```text
1. provider search/query ID
2. provider session ID
3. source-bound composite key
4. otherwise HOLD_DEDUPE_KEY_MISSING
```

Composite dedupe keys must record the exact fields used; they may not be inferred after aggregation.

## Fanout Contract

Fanout is an event-level value or an evidence-bound distribution.

```text
FANOUT_MEASURED_PER_QUERY = ALLOWED
FANOUT_DISTRIBUTION = ALLOWED
FANOUT_FIXED_CONSTANT_WITHOUT_SOURCE = REJECT
```

Synthetic stress tests may use an explicit scalar only when labeled:

```text
MODEL_MODE = SYNTHETIC_STRESS_TEST
OBSERVED_ACTIVITY = FALSE
```

## Capacity Contract

Observed average activity cannot be promoted into machine throughput capacity.

Capacity requires source-bound evidence for the relevant system, such as:

```text
peak_qps
concurrency_limit
rate_limit
fanout_limit_or_distribution
response_latency_distribution
```

Missing capacity evidence forces:

```text
MACHINE_CAPACITY = HOLD
```

## MN / AL Comparison Rule

County-count geometry is permitted only as an explicitly synthetic comparison.

```text
MN_COUNTIES = 87
AL_COUNTIES = 67
COUNTY_COUNT_RATIO = 87 / 67
```

This geometry may describe county-count amplification under an artificial equal-county assumption.

It may NOT be labeled:

```text
MINNESOTA_SEARCH_COUNT
ALABAMA_SEARCH_COUNT
MINNESOTA_HEAT
ALABAMA_HEAT
OBSERVED_STATE_QPS
MACHINE_SPEED_MAX
```

without state-specific receipts.

## Required Real-State Evidence

To compare actual MN and AL activity, bind:

```text
origin_agencies[]
deduped_query_events[]
network_contacts[]
fanout_distribution
returned_records
hits
exports
observation_window
coverage_statement
missing-agency statement
source hashes / versions
```

## LeeLoo Multi Pass

```text
ALL FOUR ONIONS PASS
AND ALL REQUIRED CROSS-EDGES PASS
AND UNIT_IDENTITY_PASS
AND DEDUPE_PASS
AND NO SYNTHETIC_TO_OBSERVED PROMOTION
= MULTI_PASS_PASS
```

Fail closed:

```text
ANY REJECT   → MULTI_PASS_REJECT
ANY CONFLICT → MULTI_PASS_CONFLICT
ANY HOLD     → MULTI_PASS_HOLD
ALL PASS     → MULTI_PASS_PASS
```

## Current Disposition

```text
NEW_HANOVER_BENCHMARK_UNIT_IDENTITY = HOLD_SOURCE_FIELD_MAPPING_REQUIRED
MN_COUNTY_NORMALIZED_MODEL = SYNTHETIC_ONLY
AL_COUNTY_NORMALIZED_MODEL = SYNTHETIC_ONLY
MN_VS_AL_HEAT_COMPARISON = HOLD_REAL_STATE_RECEIPTS_REQUIRED
MACHINE_SPEED_MAX = HOLD_CAPACITY_EVIDENCE_REQUIRED
```

## Core Rule

**FOLLOW THE QUERY WITHOUT PROMOTING THE CONTACT INTO THE SEARCH.**

**FOLLOW THE MODEL WITHOUT PROMOTING IT INTO FACT.**
