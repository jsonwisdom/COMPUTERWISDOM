# CONSTITUTIONAL_GAME_STACK_V0_3_RUNTIME_DEMO

Status: PUBLIC_PACKAGING_AND_RUNTIME_DEMO  
Issue: #90  
Supersedes: #67  
Authority: false  
Membrane: HOLDS

## Purpose

v0.3 upgrades the completed Constitutional Game Stack v0.2 from a merged governance substrate into a public, replayable demonstration.

The goal is to show outsiders how a claim moves through bounded caseflow, verifier checks, agent receipts, replay scoring, anchor hygiene, and final replay packaging without any authority upgrade.

## Demo Flow

Claim input -> Caseflow transition -> Goblin verification -> Agent action receipt -> Replay score receipt -> Anchor hygiene check -> Final replay packet

## Exercised v0.2 Artifacts

- Caseflow State Machine v0.2
- Goblin Verifier v0.1
- Replay Score Receipt v0.1
- Agent Action Receipt v0.1
- Base Anchor Hygiene Gate v0.1

## Demo Input Shape

```json
{
  "claim_id": "claim_demo_001",
  "claim_text": "A public artifact was observed and should be routed for receipt review.",
  "source_ref": "demo://source/public-artifact-001",
  "requested_transition": {
    "from_state": "DRAFT",
    "to_state": "UNDER_REVIEW"
  },
  "authority": false
}
```

## Demo Output Shape

```json
{
  "demo_id": "constitutional_game_stack_v0_3_demo_001",
  "caseflow_transition": "DRAFT_TO_UNDER_REVIEW",
  "goblin_verifier_output": "PASS_TO_EXISTENCE_CHECK",
  "agent_action_receipt": "agent_action_receipt_demo_001",
  "replay_score_receipt": "replay_score_receipt_demo_001",
  "anchor_hygiene_gate": "NO_ANCHOR_CLAIM_PRESENT",
  "authority": false
}
```

## Boundary Rules

- No truth-finality claim
- No legal authority claim
- No wallet signing automation
- No Base or ENS claim without real tx or UID
- No social-credit scoring
- No autonomous merge authority

## Public Positioning

Receipt-first governance for bounded AI agent actions.

Observers surface. Witnesses report. Agents play. Verifiers gate. Courts translate. Receipts replay. Humans merge. Authority remains false.

## Closing Rule

v0.3 must make the system legible, replayable, and demonstrable without changing the authority boundary.
