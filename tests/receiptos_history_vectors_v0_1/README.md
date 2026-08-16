# ReceiptOS History Regression V0.1

This fixture family tests a foundational ReceiptOS rule:

`SAME ENDPOINT != SAME HISTORY`

A state commitment answers **what state exists now**. A path commitment answers **what event history produced or preceded that state**. ReceiptOS must never infer the second from the first.

## Canonical hashing

```text
STATE_HASH = SHA256(canonical(FINAL_STATE))
PATH_HASH  = SHA256(canonical(EVENT_HISTORY))
```

Canonical JSON for this vector is UTF-8 JSON with sorted object keys, compact separators `,` and `:`, and `ensure_ascii=false`.

## Fixture

`AUNT_RANN_SAME_ENDPOINT_DIFFERENT_HISTORY_V0_1.json`

Both paths end at:

```json
{"consent":"HOLD","content":"Meet me by the pink tree.","delivered":false}
```

Path A has no events.

Path B records:

```text
ROUTE_REQUESTED
CONSENT_CHECKED
ROUTE_BLOCKED
```

Expected result:

```text
PATH_A.STATE_HASH == PATH_B.STATE_HASH  -> TRUE
PATH_A.PATH_HASH  == PATH_B.PATH_HASH   -> FALSE
```

Exact commitments:

```text
STATE_HASH = sha256:30cc29ff65e9f94595a0c1c0e35ad4e58692d1dea4c4ed4badf83719435cfdd9
PATH_A     = sha256:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
PATH_B     = sha256:ba6ab657988d965d2bbba0096a7ce94cbf843c09bf3d2e9c540eda1f9448fa7e
```

## Regression law

- `STATE_HASH_EQUAL != HISTORY_HASH_EQUAL`
- `ENDPOINT != HISTORY`
- `STATE_ROOT != EVENT_ROOT`
- `OBSERVED_RESULT != PROVEN_CAUSE`
- `NO_VISIBLE_STATE_CHANGE != NO_INTERACTION`

The unsupported promotion `DELIVERED_FALSE -> NOBODY_TRIED` must remain blocked.

## Three Wisdom Girls surface

- **Witness** — reports the visible state and does not infer cause.
- **Challenger** — requests the event receipts and reconstructs the path.
- **Gatekeeper** — blocks causal claims that the available history does not support.

Child sentence: **Two roads can end at the same house.**

This is a synthetic regression fixture. It creates no family, wallet, institutional, or protocol authority.

`authority_created=false`
