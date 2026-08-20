# Congress 3.0 — OpenAI runtime boundary

This lane implements the bounded `ONE_AGENT_ONE_DETERMINISTIC_FUNCTION_TOOL` pattern.

The OpenAI Agents SDK is used only as an intake/orchestration surface. The deterministic Python verifier remains the disposition authority for this research system. The agent is configured so the verifier tool result terminates the run without a second model turn.

```text
MODEL_INPUT -> FUNCTION_TOOL -> DETERMINISTIC_RECEIPT -> STOP
```

Required runtime dependency:

```text
openai-agents
```

An OpenAI API key is required only to run `agent.py`; the deterministic verifier and synthetic vectors do not require one. No API key or credential belongs in this repository.

```text
OPENAI_API_KEY_REQUIRED_FOR_DETERMINISTIC_VERIFIER = FALSE
OPENAI_API_KEY_REQUIRED_FOR_AGENT_RUNTIME = TRUE
RAW_RECORD_EXTRACTION = NOT_ADMITTED_IN_V0.1
MODEL_EXECUTION_PERFORMED_IN_REPOSITORY = FALSE
GOVERNMENT_ACTION_PERFORMED = FALSE
AUTHORITY_CREATED = FALSE
```
