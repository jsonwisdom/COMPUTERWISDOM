# Three Courts Reputation v0.1

Author: Jay Wisdom  
Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade / Game of Growth  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Core Idea

Reputation works like arcade tickets, not followers.

Players do not earn tickets for being loud. They earn tickets for doing the work.

There is no single score and no global leaderboard.

The Three Courts track separate reputation signals:

- Source: can you show where it came from?
- Replay: can anyone else get the same result following your steps?
- Context: do you make the room smarter, not angrier?

```json
{
  "reputation_model": "ARCADE_TICKETS_NOT_FOLLOWERS",
  "global_score": false,
  "leaderboard": false,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## 1. What earns reputation?

Players earn in the court where they did the work.

No likes.  
No shares.  
No speed bonus.  
No outrage bonus.

### Good receipts

+5 Source for a receipt with original link, timestamp, and file hash.

Bonus +2 Source if the player includes an archive link.

### Good replay

+5 Replay when three unrelated players successfully replay the steps and mark `same_result`.

### Good sourcing

+3 Source per primary source attached, capped at +9 per receipt so players do not dump links.

### Corrections

+10 Context for publicly correcting your own receipt with a new receipt.

+7 Context for correcting someone else, but only if the correction includes evidence, not opinion.

### Counter-receipts

+8 Context when a counter-receipt passes both Source and Replay courts.

It has to beat the receipt, not the person.

### Public education

+4 Context for a `how I checked this` guide that gets used by two newcomers in their first week.

The newcomers each get +2 Replay for using it.

## 2. What loses reputation?

Losses are court-specific, and they hurt more than gains.

### Outrage bait

-10 Context for caps-lock accusations, name-calling, or `you won't believe` framing.

### Accusations without receipt

-15 Source.

If you claim it, you show it.

### Harassment or doxxing

-50 across all three courts, and the player cannot earn for 7 days.

### Engagement farming

-5 Replay for copy-paste receipts or reposting the same receipt in multiple threads.

### Failed replay

-8 Replay after three independent players mark `cannot_reproduce` with their own attempt logs.

### Refusing correction

-12 Context if a receipt is proven wrong in both Source and Replay courts and the player does not update or retract within 48 hours.

## 3. How does a player recover reputation?

Players do not grind it back.

They repair it.

Recovery is a quest chain, not a timer:

1. Post a public correction with full Source and Replay.
2. Mentor two new players through their first successful replay.
3. Audit one of your own old receipts and re-source it.

Complete all three and regain half of what was lost in that court.

Complete the recovery chain twice and the player is fully restored.

Apologies without work do not count.

## 4. How do citizens trust high-reputation players?

Citizens do not trust the number.

They trust the paper trail.

Every profile should show:

- last 20 actions with court, result, and links
- correction rate, where high can be good
- balance across courts, not total

A 90-90-10 player may be a great sourcer but a poor teacher.

Reputation is portable.

It should be exportable as signed JSON. Any other arcade can verify it without calling home.

Citizens can click any ticket and see the exact receipts that earned it.

Ranks are fun and descriptive, not godlike:

- Paperboy
- Clerk
- Archivist
- Librarian
- Custodian

No crowns.

## 5. How does the system prevent mob behavior?

### Blind juries

Replay reviews are done by 7 random players. Current tally is hidden until the reviewer votes.

### Weight caps

No matter how high a player's score is, their vote counts at most 3x a new player's vote in any single case.

This prevents whales.

### Diversity rule

A replay only passes if the 3 successful replays come from players in at least 2 different time zones and who have not co-voted in the last 10 cases.

### Cooldowns

A player cannot review the same player twice in a row, or more than 3 receipts from one submitter per day.

### No visible popularity in courts

Upvotes, hearts, and view counts are hidden from the courts.

They may live in the lobby, but not in the game.

## 6. How should the Three Courts interact with reputation?

Each court spends and grants its own tickets.

A player cannot buy Source credibility with Context fame.

### Court of Source

Checks origins.

High Source lets a player submit receipts without a sponsor.

### Court of Replay

Checks steps.

High Replay lets a player sit on juries.

### Court of Context

Checks fairness.

High Context lets a player write guides and approve corrections.

## Advanced Actions

To unlock advanced actions like `challenge a Custodian receipt`, a player needs at least 50 in all three courts.

This forces balance.

A player can be a brilliant sourcer, but if they never teach or accept corrections, they stay a Clerk.

Tickets decay slowly after 90 days of inactivity.

Reputation is about recent work, not old glory.

## Safety Membrane

```json
{
  "reward_receipts": true,
  "reward_replay": true,
  "reward_corrections": true,
  "reward_public_education": true,
  "reward_outrage": false,
  "reward_accusation": false,
  "reward_harassment": false,
  "global_leaderboard": false,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Closing Rule

Reputation is earned by making public memory more replayable.

It is not earned by getting attention.
It is not earned by attacking people.
It is not earned by declaring fraud.

Tickets follow receipts.
Authority remains false.
