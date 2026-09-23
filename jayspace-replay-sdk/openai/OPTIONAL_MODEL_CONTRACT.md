# Optional OpenAI Model Contract v0.1

The OpenAI layer is optional. The deterministic replay engine is authoritative only for its own typed software disposition.

## Allowed model functions

- explain a deterministic receipt in plain language
- summarize bound source metadata supplied by the caller
- translate labels without changing receipt semantics
- generate review questions from an existing receipt

## Forbidden promotions

```text
MODEL_OUTPUT -> PASS                FORBIDDEN
MODEL_OUTPUT -> IDENTITY_MATCH      FORBIDDEN
MODEL_OUTPUT -> RELATIONSHIP_FACT   FORBIDDEN
MODEL_OUTPUT -> AUTHORITY           FORBIDDEN
MODEL_OUTPUT -> LEGAL_FINDING       FORBIDDEN
MODEL_OUTPUT -> PERSONNEL_ACTION    FORBIDDEN
```

A model may describe `PASS`, `HOLD`, `CONFLICT`, or `REJECT` only after the deterministic engine has emitted that receipt.

No API key may be committed. Runtime credentials must be supplied outside source control.

`MODEL_REQUIRED = FALSE`
`AUTHORITY_CREATED = FALSE`
