# PMEM-IMPL-006 — Temporal Validity + Revalidation Contract

Depends on: `001..005`

`STORED(m) != CURRENT(m,t)`.

Temporal metadata includes `observed_at`, `valid_from`, `valid_until`, `revalidate_after`, `last_verified_at`, and `temporal_class: STATIC|SLOW|VOLATILE|EVENT`.

`CONFIDENCE(m,t) != VALID(m,t)`. Confidence may decay without changing type; validity may expire despite previously high confidence.

Decay policies are versioned and may change only confidence metadata. Type immutability remains absolute.

Revalidation requires actual supporting evidence and creates new evidence/state assertions. `REVALIDATE != REFRESH TIMESTAMP`.

At/after expiration: `CURRENT=FALSE`, `USABLE=FALSE` unless independently supported. Historical replay remains available when authorized.

Volatile claims require explicit freshness constraints. For current-state queries, `STALE -> EXCLUDE` and `UNKNOWN_FRESHNESS -> FAIL_CLOSED`.

New contradictions do not erase old evidence.

Material time claims distinguish `EVENT_TIME`, `OBSERVATION_TIME`, `INGEST_TIME`, `LEDGER_TIME`; they are not silently treated as equal.

Core: **OLD != CURRENT; REVALIDATION != TIMESTAMP REFRESH; DECAY NEVER CHANGES TYPE**.

`AUTHORITY_CREATED = FALSE`
