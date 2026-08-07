# RePlay Wisdom Factory Game — Design Boundary

## Identity

**RePlay Wisdom Factory Game** is an **agentic pedagogical game** inside `jsonwisdom/COMPUTERWISDOM`.

It teaches the verification rhythm:

`PROPOSE → TEST → RECEIPT → REPLAY → VERIFIED`

It is **not** the JSONWisdom protocol verifier, not a fuzz harness, and not a source of execution authority.

## Boundary

```text
JSONWisdom / protocol engineering
        │
        │ concepts only
        ▼
RePlay Wisdom Factory Game
pedagogical agentic simulation
```

No in-game score, event, receipt, replay, checkpoint, or Constitution reward amends or verifies `jsonwisdom/AL`.

## Mechanic Classification

### Canonical Analogy
- Core verification rhythm
- `PASS != VERIFIED`
- Independent `REPLAY!`
- Evidence/receipt thinking
- Mandatory reflection after each round

### Simplified Analogy
- Dice/seed resolution
- Zero Trust ability
- Bullshit Detector ability
- Chaos Deck failures
- Replay anomaly branches

These compress real protocol failure modes into game events. They are not cryptographic verifier outcomes.

### Non-Canonical Gamification
- Wisdom points
- Intuition Reward — Non-Canonical
- In-game Constitution rewards
- `state/wisdom-graph.json`

These exist only to make learning fun and memorable.

## Game Zero

Game Zero teaches one thing above all:

> A passing test is not the same thing as a verified claim.

Two claims are played. Every resolved round ends with reflection:

1. What did you believe before?
2. What actually survived?

After both claims resolve, the game asks both players to explain why VERIFIED required more than PASS.

`gameZeroUnderstood` becomes `true` only when the players jointly confirm they can explain the distinction.

The success condition is therefore **understanding**, not obtaining a VERIFIED result.

## Agentic Loop

```text
MISSION
  ↓
PROPOSER — states the claim
  ↓
SKEPTIC — attacks assumptions
  ↓
TESTER — creates a falsification challenge
  ↓
PLAYERS — predict / decide
  ↓
REPLAYER — checks consistency
  ↓
SCRIBE — records the round
  ↓
REFLECTION — records mental-model change
```

## Runtime State

`state/wisdom-graph.json` is local session state and is ignored by Git.

A future committed fixture may live at:

`state/fixtures/sample-wisdom-graph.json`

## Playtest Question

The prototype succeeds if a new player eventually asks, without prompting:

> “It passed — but did somebody independently replay it?”
