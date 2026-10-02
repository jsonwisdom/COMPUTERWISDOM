# Jason's Call Bullshit Betting App — Story v0.1

**Promotion state:** `STORY_PROMOTED / REVIEWABLE / NOT_MERGED`  
`AUTHORITY_CREATED = FALSE`  
`LEGAL_FINDING_CREATED = FALSE`  
`REAL_MONEY_WAGERING = NOT_DEFINED`  
`GAME_SCORE != CURRENCY`  
`STORY != EVIDENCE`

## The story

The internet gives everybody a microphone. Jason's Call Bullshit gives everybody a receipt table.

A claim enters the room. It can come from a politician, company, headline, influencer, institution, friend, or player. Nobody wins because they sound confident. Nobody loses because they are unpopular. The question is simple:

**Can the claim survive replay?**

Players call `PASS`, `HOLD`, `CONFLICT`, or `REJECT` and put their confidence behind the call. Then the app opens the evidence rail: original words, source, timestamp, authority class, counterevidence, version history, and the exact receipt that would change the outcome.

The bet is not on a person. The bet is on whether the evidence survives.

- **CALL BULLSHIT:** show me the receipt.
- **CALL TRUE:** show me the receipt.
- **CALL HOLD:** we do not know yet.
- **CALL CONFLICT:** two supported records disagree.

Every round is reversible. New evidence does not erase yesterday's state. It appends a new state and lets the player replay exactly what changed.

## The Jason Rule

Jason is not the judge. Jason is the player who asks the uncomfortable question and accepts the same evidence rules when his own claim is tested.

> **BET ON THE RECEIPT, NOT THE PERSONALITY.**

## Round loop

```text
CLAIM
→ LOCK EXACT WORDING
→ SOURCE + TIMESTAMP
→ AUTHORITY CLASS
→ PLAYER CALL + CONFIDENCE
→ COUNTEREVIDENCE
→ PASS | HOLD | CONFLICT | REJECT
→ RECEIPT
→ REVERSE REPLAY
→ APPEND NEW STATE
```

## Product membranes

```text
POPULARITY != TRUTH
CONFIDENCE != PROOF
OFFICIAL_SOURCE != INFALLIBLE
AI_OUTPUT != RECEIPT
MISSING_SOURCE != AUTOMATIC_FALSEHOOD
GAME_SCORE != LEGAL_VERDICT
PLAYER_WIN != REAL_PERSON_GUILT
STORY_PROMOTION != CODE_DEPLOYMENT
GIT_MERGE != CONSENSUS_PROVEN
AUTHORITY_CREATED = FALSE
```

## Why it exists

Call Bullshit turns argument into a game where the most useful move is not shouting louder; it is producing better evidence. The app rewards correction, replay, and clean uncertainty. A player can win a round by proving a claim, disproving it, or correctly refusing to overclaim when the record is incomplete.

The best player is not the person who is always right.  
The best player is the person whose reasoning can be replayed.

## Promoted story line

**Jason's Call Bullshit — a betting game for claims, confidence, and receipts.**

**Tagline:** BET ON THE RECEIPT, NOT THE PERSONALITY.

## Promotion boundary

This artifact promotes the story into a persistent reviewable surface. It does not create a gambling license, real-money wagering system, financial product, legal finding, deployment, institutional endorsement, or authority.
