# Cabinet System v0.1

Author: Jay Wisdom  
Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade / Game of Growth  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Purpose

Define the Cabinet as the core playable location object in Public Receipt Arcade.

A cabinet is not a website.
A cabinet is a place turned into a game.

Players walk up, wiggle the joystick, and play.

## 1. What Is A Cabinet?

A cabinet is a stand-up arcade machine that lives on the Minnesota map.

Saint Cloud City Hall is not represented as a building in the map.
It is represented as a loon-shaped cabinet with blinking lights.

Like a Pokémon Gym, it has a theme.
Like a Zelda dungeon, it has rooms unlocked by doing work.
Like an arcade, it eats quarters players earn, not dollars players buy.

A cabinet never speaks for the city.

It only holds public records players have already pinned.

```json
{
  "cabinet": "PLACE_AS_PLAYABLE_PUBLIC_MEMORY_MACHINE",
  "speaks_for_city": false,
  "holds_public_records": true,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## 2. What Every Cabinet Contains

Every cabinet has the same six parts.

### Marquee

The parody art unlocked for that place.

### Joystick Slot

Governance by Joystick lives here.

- Push up to vote
- Push down to skip

### Three Court Lights

The cabinet shows three court lights:

- Source
- Replay
- Context

They blink green when a receipt passes.

### Receipt Tray

The Receipt Tray holds the current old-vs-new pair.

Always two public artifacts:

- PDFs
- CSVs
- meeting packets
- official pages
- datasets

No forms to fill.

### Memory Tape Wall

A shelf of VHS-style Media Cards showing every past drift that passed at this cabinet.

Public data appears byte by byte.
Names are blurred behind the membrane.

### Reward Chute

The chute spits out the player's:

- Quarter
- Decal
- Token
- Orchid
- Media Card

when they finish the work.

## Forbidden Cabinet Elements

No admin panel.
No search bar as first interaction.
No login screen.
No fraud button.
No accusation field.
No popularity leaderboard.

## 3. What Makes A Cabinet Fun?

### Two-Minute Loops

Insert 1 Replay ticket.
Compare two pages.
Tap same or different.
Done.

### Lights and Sound

Each court gives a ding when it passes.

Three dings in a row plays the town jingle.

### Co-op Seats

A second player can grab the other joystick and replay with you.

Both get credit.

### Easter Eggs

Wiggle left-left-right on the Saint Cloud cabinet and the loon winks.

It does nothing for score.

### Seasonal Skins

In October, the Bemidji axe cabinet gets cobwebs.

Same quests.
New paint.

### No People Leaderboard

The high score is:

```text
receipts verified this month
```

not who is popular.

## 4. What Unlocks New Cabinets?

New cabinets are not unlocked by admins.

The map unlocks like fog in Zelda.

A dark cabinet lights up when:

1. its neighbor has 3 receipts that passed all Three Courts,
2. 10 different local players have spent Replay tickets there, and
3. locals push the joystick to vote it open.

Example:

Brainerd stays dark until Saint Cloud players finish three park-budget drifts and vote.

Authority remains false because players open the path through receipts and replay, not because staff appoints it.

## 5. How Cabinet Quests Rotate

Quests are not assigned by arbitrary admin selection.

They rotate when public records change.

Every Monday, the cabinet checks its town website for a new version of the same file type it already holds.

Examples:

- new budget posted
- new meeting packet posted
- new fee schedule posted
- new annual report posted

The old-vs-new pair updates only when the source and schema rules allow it.

Players can also drop a new old-vs-new pair into the tray.

If it passes Source Court, it joins the weekly rotation.

Players vote by quick joystick flick:

```text
keep this pair another week
```

or

```text
swap it
```

No meetings.
No admin override.

## 6. How A Cabinet Remembers Local History

A cabinet does not present itself as a normal database table.

It uses the Memory Tape Wall.

Each passed drift becomes a VHS card on the shelf.

Oldest tapes sit left.
Newest tapes sit right.

Tap a tape and the player sees:

- old public page
- new public page
- old hash
- new hash
- byte sizes
- three court lights that blinked green
- replay status

For Saint Cloud, the wall might show:

- 2014 parks budget next to 2024 parks budget
- 2015 parks budget next to 2025 parks budget
- future pairs as they are added

This builds a visual timeline.

Anyone can replay any tape years later.

PII is never on the label.

Only the public numbers and approved public context appear.

## 7. How A Cabinet Becomes A Boss Cabinet

A town cabinet can become a boss cabinet when:

1. its wall contains 20 passed tapes, and
2. it has balanced tickets across all Three Courts, and
3. locals nominate it.

Boss cabinets are like gym leaders.

### County Boss

Example:

```text
Stearns County Boss Cabinet
```

It pulls the best three drifts from:

- Saint Cloud
- Sartell
- Waite Park

A player must have played each child cabinet once before challenging the County Boss.

### State Boss

The Minnesota Boss Cabinet appears after 5 county bosses are lit.

It only shows drifts that appeared in 3 or more counties.

### Federal Boss

The Capitol Arcade appears after 5 state bosses.

It shows only old-vs-new federal PDFs or datasets that passed in multiple states.

Boss cabinets have:

- bigger marquees
- deeper sounds
- special art drops
- harder replay routes

Boss cabinets do not give extra power.

They are harder because they require work across places, not because an admin said so.

## Cabinet Object Shape

Future schema candidate:

```json
{
  "cabinet_id": "mn_saint_cloud_loon_cabinet",
  "map": "Minnesota",
  "location": "Saint Cloud",
  "theme": "Loon Cabinet",
  "state": "ACTIVE",
  "marquee_art": [],
  "current_receipt_tray": [],
  "memory_tapes": [],
  "court_lights": {
    "source": false,
    "replay": false,
    "context": false
  },
  "reward_chute": [],
  "unlock_rules": [],
  "boss_status": "NONE",
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Safety Membrane

```json
{
  "public_records_only": true,
  "pii_public_display": false,
  "receipt_first": true,
  "replay_required": true,
  "admin_override": false,
  "pay_to_win": false,
  "fraud_button": false,
  "accusation_field": false,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Closing Rule

A cabinet is where public memory becomes playable.

It holds the records.
It lights the courts.
It drops the rewards.
It remembers the tapes.

The city does not speak through the cabinet.
The receipts do.

Authority remains false.
