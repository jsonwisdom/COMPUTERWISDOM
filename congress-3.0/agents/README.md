# Congress 3.0 — agent governance directory

This directory is the provider-neutral agent-governance lane declared by the Congress 3.0 directory contract.

The first executable provider-specific runtime is intentionally isolated under `../openai/`.

```text
AGENT_GOVERNANCE != PROVIDER_RUNTIME
AGENT_CONTRACT != MODEL_EXECUTION
MODEL_EXECUTION != GOVERNMENT_ACTION
AUTHORITY_CREATED = FALSE
```

Future agent providers or orchestration patterns must preserve the deterministic verifier as the terminal evidence-classification layer unless a separately reviewed versioned contract changes that rule.
