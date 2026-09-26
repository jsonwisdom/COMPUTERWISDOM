# Jason's Call Bullshit — Two-Mode Front Door v0.1

**State:** `APPENDED / REVIEWABLE / NOT_MERGED`  
`STORY_V0_1_PRIOR_STATE = PRESERVED`  
`CODE_DEPLOYMENT = FALSE`  
`REAL_MONEY_WAGERING = NOT_DEFINED`  
`AUTHORITY_CREATED = FALSE`

## ⚡ COPILOT TASK → DO SOMETHING FOR ME

Action rail: research, find, draft, schedule, build, or other supported execution.

The task rail may use plans and connected tools when authorized, but execution state remains separate from verification state.

## 🚨 CALL BULLSHIT → VERIFY SOMETHING WITH ME

Verification rail:

| Field | Meaning |
|---|---|
| `EXACT WORDING` | Claim as stated, without semantic widening |
| `SOURCES` | Origin plus independently located supporting or contradicting sources |
| `TIMESTAMP` | When said, published, changed, or circulated |
| `EVIDENCE` | What the bound record actually supports |
| `VERDICT` | `PASS` · `HOLD` · `CONFLICT` · `REJECT` |
| `REPLAY RECEIPT` | Compact, shareable reconstruction of the evidence path |

## Router

```text
USER INPUT
→ ACTION REQUEST? → COPILOT TASK
→ CLAIM / QUOTE / STAT / STORY? → CALL BULLSHIT
→ AMBIGUOUS? → ASK WHICH RAIL OR PRESENT BOTH
```

## Bridge laws

```text
DO_SOMETHING != PROVE_SOMETHING
TASK_COMPLETION != CLAIM_VERIFICATION
RESEARCH_OUTPUT != RECEIPT_BY_DEFAULT
DRAFT != SOURCE
CONNECTED_TOOL_ACTION != AUTHORITY
PLAYER_CONFIDENCE != PROOF
GAME_SCORE != CURRENCY
GAMIFICATION != MONETIZATION
REPLAY_RESULT != LEGAL_VERDICT
AUTHORITY_CREATED = FALSE
```

## Front-door prompt

> **What would you like me to do for you, or what would you like me to verify?**

## Call Bullshit prompt

> Drop a claim, quote, stat, or story. The system freezes the wording, binds sources and timestamps, evaluates the evidence, returns `PASS / HOLD / CONFLICT / REJECT`, and produces a replay receipt.

## State transition

This file appends the two-mode UX layer to the existing story artifact. It does not rewrite the original story, deploy code, define a real-money wagering system, create a legal verdict, or create authority.
