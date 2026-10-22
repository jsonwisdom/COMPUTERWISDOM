# Presidential Dice v0.1

**Class:** public-education game / mathematical strategy simulation  
**Authority created:** false  
**Operational command claimed:** false

Presidential Dice combines a quadratic scoring model with dice-routed uncertainty and a separate receipt-based authority replay.

## Core equation

```text
Outcome = a * (x - h)^2 + k
```

- `x`: player-selected strategic variable
- `h`: scenario-defined ideal point
- `a`: friction coefficient from D6
- `k`: baseline uncertainty from D20

D6 mapping:

```text
1-2 -> a=1
3-4 -> a=2
5-6 -> a=3
```

Lower score is better **inside the simulation only**.

## Presidential stack

```text
D6 FRICTION
-> D20 FORTUNE
-> PLAYER CHOICE x
-> QUADRATIC SCORE
-> D8 AUTHORITY GATE
-> RECEIPTS
-> ADVERSARIAL REPLAY
-> PROVEN | BOUND | HOLD | CONFLICT | REJECT
```

The authority gate routes inquiry across constitutional, statutory, appropriations, executive-instrument, agency-implementation, foreign-affairs/military-authority, judicial-review, and congressional/inspector-oversight questions.

## Hard locks

```text
DICE != TRUTH
SCORE != LEGALITY
LOW SCORE != GOOD POLICY
MATHEMATICAL OPTIMUM != LAWFUL AUTHORITY
STRATEGY RESEMBLANCE != SUN TZU PROVENANCE
BOOK RECOMMENDATION != POLICY CAUSATION
MODEL OUTPUT != SOURCE
```

Sun Tzu is used as a historical strategy-analysis lens only. This game does not provide targeting, weapons, evasion, or operational military instructions.

## Replay contract

A run preserves the seed, rolls, `x`, `h`, `a`, `k`, score, source pointers, and evidence state.

```text
same seed + same inputs -> same game result
new receipts -> evidence state may change
```

Gray Baby standing order:

> **SHOW ME THE EDGE.**
