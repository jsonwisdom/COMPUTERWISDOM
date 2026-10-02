# CWaaS Operator Contract — Trial 0

## Goal

Turn customer-service chaos into a deterministic proposed state and a neutral receipt. The model explains; deterministic code classifies; authorized systems act.

## Boundary

```text
MODEL_OUTPUT != AUTHORITY
HISTORICAL_TRUTH != LIVE_AUTHORIZATION
DOCUMENT_UPLOADED != DOCUMENT_ACCEPTED
API_ACCEPTED != EXECUTED
UNKNOWN_LIVE_STATE = FORBIDDEN_EXECUTION
ACCEPTANCE_IS_ATOMIC_TO_CREDENTIAL
SAFETY_IS_TIER_AGNOSTIC
```

## Trial 0 I/O

Input is a fixture containing observed facts only. Output contains a state, hashes, and explicit `execution_allowed=false`, `facts_promoted=0`, and `authority_created=false`.

## OpenAI agent boundary

Start with one agent. Its tools are read-only observation and deterministic trial evaluation. The agent must never call a live execution tool in Trial 0. Missing evidence routes to HOLD. Any later human approval must bind the exact epoch, credential hash, case ID, action, destination, amount, nonce, and expiry.

## Not admitted

- live wallets or private keys
- live RPC or bank execution
- raw customer documents
- webhook delivery
- counterparty acceptance
- default-branch writes or merge
- production, legal, fiduciary, or court-ready claims

## Promotion gate

Trial 0 may advance only after fixtures pass in CI and a human reviews the draft PR. Advancing authorizes design iteration only; it does not authorize deployment or financial execution.

