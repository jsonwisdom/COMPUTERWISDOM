# INTERNAL_DRIFT_ALERT_RESPONSE_PROTOCOL_V1

Anti-Drift News — Internal Response Discipline Protocol  
Authority: false  
Status: Active for repo/spec/architecture flows

---

## Purpose

Codify the rule that every build, architecture, GitHub, and specification response for Jay must include a Jay Builder Prompt.

The prompt is not optional.  
The prompt is the handoff artifact.  
No prompt means response drift.

---

## Trigger Phrases

This protocol activates when Jay says any of the following:

- `DRIFT ALERT`
- `INTERNAL`
- `REPLAY`
- `AGAIN`
- `Prompt required for Jay on EVERY response`

---

## Corrected Invariant

```json
{
  "jay_builder_prompt_required": true,
  "scope": "build_architecture_github_spec_work",
  "missing_prompt": "INTERNAL_DRIFT",
  "response_action": "REPLAY_WITH_PROMPT",
  "authority": false
}
```

---

## Required Response Pattern

When the protocol is active, the response must:

1. Acknowledge drift plainly.
2. Restate the corrected invariant.
3. Provide a Jay Builder Prompt.
4. Avoid over-explaining.
5. Preserve `authority:false`.

---

## Required Footer

```md
## Jay Builder Prompt

```text
<copy-paste-ready next build prompt>
```
```

---

## Invariants

- Prompt is not optional.
- Prompt is the handoff artifact.
- No prompt equals response drift.
- Drift alert requires replay.
- Replay must include prompt.
- Authority remains false.

---

## Canon Phrase

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
