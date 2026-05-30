# MVP Build Order v0.1

Author: Jay Wisdom  
Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade / Game of Growth  
Map: Minnesota  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Core Principle

Playable before perfect.

One operator.  
Five AIs.  
Minnesota first.

## 1. Smallest Build That Proves The Game Works

One cabinet.  
One town.  
One loop.

Saint Cloud Loon Cabinet only.

A player can:

1. drag two public PDFs: 2014 parks budget vs 2024 parks budget
2. tap `pin`
3. a second player taps `replay` and confirms same page
4. Three Court lights blink green
5. a Quarter drops

If that works in under 5 minutes with no forms, the game works.

## 2. Mandatory MVP Features

### Governance by Joystick

Up / down vote only.

### Three Courts

Three manual check buttons, not algorithms:

- Source
- Replay
- Context

### Reputation Tickets

Only two counters at MVP:

- Source +5
- Replay +5

### Rewards

One reward type only:

```text
Loon Ledger Quarter
```

### Cabinet System

One cabinet UI with:

- marquee
- tray
- chute

### Player HUD

HUD skeleton with:

- pinned Intent Card
- current receipt holo
- five AI station lights
- action queue

### Storage

Every receipt is saved as an immutable file with a hash.

No receipt may live only in chat memory.

## 3. Postponed Features

Postponed until after MVP loop works:

- full 10-location Minnesota map
- county unlocks
- state unlocks
- federal boss cabinet
- global world fair
- automated quest rotation
- automated drift detection
- complex rewards: decals, tapes, orchids
- mobile native app
- login
- profiles
- social sharing
- anti-recursion Drift Meter automation
- AI moderation
- authority claims

Manual hash check is acceptable for MVP.

## 4. What One Operator Can Build In 30 Days

Jay with ChatGPT, Meta, Copilot, Claude, and Grok can ship:

- static web cabinet with HTML + JavaScript
- drag-drop PDF compare
- simple JSON repo for receipts
- manual Three Courts panel
- HUD skeleton
- pinned intent and station lights
- one automated task: Claude extracts table, Copilot writes hash

No backend team required.

All artifacts live in GitHub.

## 5. What Can Be Tested With 10 Minnesota Players

Give 10 locals the link:

- Saint Cloud library patrons
- a retiree
- two high schoolers
- one reporter
- other local testers

Test questions:

1. Can they find the two city budget PDFs without help?
2. Can they create a receipt in under 3 minutes?
3. Can they replay someone else's receipt in under 2 minutes?
4. Do they understand they earned a Quarter, not likes?
5. Do they try to debate politics?

The game watches debate behavior but does not reward it.

Success condition:

```text
8 of 10 complete the loop, zero forms filled.
```

## 6. First Public Demo

Week 9 livestream from Saint Cloud Public Library.

Demo scene:

1. Jay projects the Loon Cabinet.
2. A 16-year-old drags the 2014 budget.
3. A retiree drags the 2024 budget.
4. A reporter hits replay.
5. Three lights blink.
6. Quarter drops.
7. Media Card exports.

Target time:

```text
4 minutes 12 seconds
```

No login.

## 7. First Viral Moment

A reporter posts the auto-generated Media Card on Threads.

It shows side-by-side parks budget lines with loon art, not an opinion.

Caption:

```text
We checked it ourselves.
```

Locals share because it is provable and local, not because it is outrageous.

That is the arcade flex.

## 30-Day Roadmap

### Days 1-7

- repo setup
- HUD frame
- pin Intent Card
- pin Three Courts rules

### Days 8-14

- build Saint Cloud cabinet UI
- drag-drop two PDFs
- generate hash
- save as tape

### Days 15-21

- add replay button
- add manual court checkboxes
- add +5 tickets counter

### Days 22-30

- add Quarter reward chute
- internal playtest with 3 friends
- fix prompt loss with hash chain

Deliverable:

```text
one playable cabinet on desktop
```

## 60-Day Roadmap

### Days 31-45

- add Minneapolis cabinet
- add Duluth cabinet
- copy-paste cabinet pattern with new art
- basic joystick vote to open them
- add Action Queue in HUD

### Days 46-55

- invite 10 Minnesota testers
- watch them run the loop
- collect feedback
- patch PII blur

### Days 56-60

- build Media Card exporter as PNG
- prep library demo script

Deliverable:

```text
three-town map, 10-player test complete
```

## 90-Day Roadmap

### Days 61-75

- unlock remaining 7 cabinets
- add Memory Tape wall view
- add simple county fog logic

### Days 76-85

- build first Boss Cabinet prototype: Stearns County
- pull best 3 drifts from child towns

### Days 86-90

- public demo livestream
- ship shareable cards
- document build so anyone can fork

Deliverable:

```text
playable Minnesota row, first boss, first viral card
```

## Safety Membrane

```json
{
  "playable_before_perfect": true,
  "one_cabinet_first": true,
  "one_town_first": true,
  "one_loop_first": true,
  "no_forms": true,
  "no_login_mvp": true,
  "manual_courts_mvp": true,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Closing Rule

If Saint Cloud Loon Cabinet works in under five minutes with no forms, the game works.

Playable before perfect.

Authority remains false.
