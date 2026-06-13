# Authority Replay MVP

**Tagline:** Don’t log the agent. Replay the authority.

Authority Replay is a verification game for agent teams. It trains humans and agents to distinguish action logs from authorization receipts.

GitHub-style stacks often show:

```text
User → Agent → Tool → Action
```

Evidence-grade stacks require:

```text
User → Policy → Agent → Tool → Action
```

## Goal

Promote this claim only when the full receipt chain exists:

```yaml
claim: agent_action_authorized
from: UNOBSERVED
to: OBSERVED
```

Required chain:

```yaml
required_receipt_chain:
  - user_identity_receipt
  - policy_receipt
  - delegation_receipt
  - revocation_status_receipt
  - agent_action_receipt
  - tool_execution_receipt
```

Forbidden substitutes:

```yaml
forbidden:
  - action_log_only
  - agent_identity_only
  - approval_screenshot_only
```

## Files

```text
AUTHORITY_REPLAY_MVP/
├── README.md
├── policy.schema.json
├── receipt.schema.json
├── scoring.yaml
├── valid_chain.json
├── expired_delegation.json
└── replay_engine.py
```

## Run

```bash
python artifacts/AUTHORITY_REPLAY_MVP/replay_engine.py artifacts/AUTHORITY_REPLAY_MVP/valid_chain.json
python artifacts/AUTHORITY_REPLAY_MVP/replay_engine.py artifacts/AUTHORITY_REPLAY_MVP/expired_delegation.json
```

Expected:

```text
valid_chain.json -> OBSERVED
expired_delegation.json -> UNOBSERVED
```

## xAI Pitch

Truth-seeking agents should not only explain what happened. They should prove whether the action was authorized when it happened.

Grok can explain the event. Authority Replay verifies the authority.
