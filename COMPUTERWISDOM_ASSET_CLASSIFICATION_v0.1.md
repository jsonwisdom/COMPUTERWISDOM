# COMPUTERWISDOM Asset Classification Law v0.1

## Orthogonal classification

Repository assets are classified on separate axes.

```text
ARTIFACT CLASS: executable | fixture | proof | whitepaper
CAPABILITY ROLE: instrument | future roles...
```

Artifact class governs the canonical discovery/storage surface. Capability role describes semantics and may require a companion contract, but it does not create a second canonical home.

Therefore:

```text
EXECUTABLE + INSTRUMENT_ROLE != MULTI_HOME_CONFLICT
FIXTURE_NAMED_AUDIT          != INSTRUMENT
PROOF_NAMED_AUDIT            != INSTRUMENT
ROLE                          != LOCATION
LOCATION                      != AUTHORITY
```

True multi-artifact ambiguity remains fail-closed and requires semantic review.

No classification authorizes relocation.
