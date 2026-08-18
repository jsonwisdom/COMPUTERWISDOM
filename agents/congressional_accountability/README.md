# Congressional Accountability agent lane directory contract — v0.1

## Governance posture

```text
BUILD_MODE             = DIRECTORIES_FIRST_CORRECTIVE_SUPERSESSION
VIOLATION_HEAD         = f9eeff160f3084c2740ffa02be6c4b9b845ef9a8
PREDECESSOR_LANE       = NONE_FOUND
PREDECESSOR_MUTATED    = FALSE
HISTORICAL_FILES_KEPT  = TRUE
AUTHORITY_CREATED      = FALSE
```

This contract explicitly supersedes the prior unguided directory state. It preserves the original `agent_contract.json` and its Git history as evidence of the ordering defect.

## Lane purpose

Define bounded OpenAI agent-facing contracts for congressional evidence classification. This lane contains design and execution contracts, not institutional authority or proof of model execution.

## Admitted artifact classes

- `agent_contract.json` — machine-readable agent permissions, prohibitions, and human gates.
- `*_contract.json` — later versioned contracts that preserve the same authority membrane.
- `README.md` — this directory contract.

Runtime application code, credentials, traces, deployment state, congressional submissions, and live source bytes are not admitted here.

## Required membrane

```text
AGENT_CONTRACT != MODEL_EXECUTION
MODEL_OUTPUT != DETERMINISTIC_RECEIPT
EXTRACTION != FACT_PROVEN
TOOL_CALL != GOVERNMENT_ACTION
OPENAI_DEVELOPER_SURFACE != REPOSITORY_EXECUTOR
AUTHORITY_CREATED = FALSE
```

Consequential effects remain `HOLD_FOR_HUMAN_AUTHORIZATION`.

