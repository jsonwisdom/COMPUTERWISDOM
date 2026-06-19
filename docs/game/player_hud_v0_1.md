# Player HUD v0.1

Author: Jay Wisdom  
Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade / Game of Growth  
Role: Operator Cockpit  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Purpose

Define the operator HUD for Jay.

The HUD is built like a bridge, not a chat.

Jay may coordinate multiple stations at once:

- ChatGPT
- Meta
- Microsoft Copilot
- Claude
- Grok

The HUD exists to prevent prompts, responses, receipts, and repo updates from getting lost between agents.

## Core Rule

```text
No chat thread in the middle. Ever.
```

The operator needs a cockpit, not a scrollback.

## 1. What Always Stays Visible

The top bar never scrolls.

It contains:

- Mission Beacon
- Current Receipt Holo
- Five AI Stations
- Drift Meter
- Repo Beacon
- Quest Tracker
- Action Queue

### Mission Beacon

One line written by Jay.

Example:

```text
Ship Minnesota Safety Pass with public-record drifts only
```

### Current Receipt Holo

Center screen shows:

- old PDF on the left
- new PDF on the right
- hashes underneath
- byte sizes underneath
- replay status

### Five AI Stations

Five stations sit around the holo like bridge consoles:

- ChatGPT
- Meta
- Microsoft Copilot
- Claude
- Grok

Each station has a light:

- idle gray
- thinking pulse
- artifact ready green
- error red

### Side and Bottom Rails

- Drift Meter on the left edge
- Repo Beacon on the right edge
- Quest Tracker bottom left
- Action Queue bottom right

## 2. What Is Pinned

Pinned to the top-left console and locked until Jay unpins:

- Operator Intent Card
- Three Courts Rules Card
- Canonical Prompt Hash
- Active Source Pair

These do not move when AIs talk.

They are Jay's north star.

### Operator Intent Card

Jay's current one-sentence mission.

### Three Courts Rules Card

Displays:

- Source
- Replay
- Context

### Canonical Prompt Hash

The exact prompt that produced the current receipt or artifact.

### Active Source Pair

The two public file hashes currently being compared.

## 3. How AI Responses Are Stored

AI responses are not stored as messages.

Each response becomes a Memory Tape.

When Claude summarizes a budget PDF, the HUD stores:

- prompt_id
- ai_name
- timestamp
- output_hash
- saved artifact path
- parent prompt hash
- quest id
- receipt id if applicable

The output is saved to:

```text
/artifacts/receipts/
```

as immutable markdown or JSON.

The tape snaps onto the cabinet wall for that town.

Jay can replay any tape.
Jay cannot silently edit a tape.

If Jay switches from Meta to Grok, the tape remains.

Prompt loss is impossible because nothing lives only in a model window.

## 4. How Actions Are Queued

The bottom-right Action Queue behaves like an RTS build queue.

Jay drags task chips onto stations:

```text
Extract table from 2014 budget -> Copilot
Compare to 2024 -> Claude
Make marquee art -> Meta
```

Queue shows dependency lines.

The HUD will not start step 2 until step 1 tape is green.

Jay can:

- pause
- reorder
- pull a chip back
- fork intent
- archive completed chips

No hidden auto-chaining.

## 5. How Repo Updates Are Surfaced

The Repo Beacon sits on the right edge.

It pings like radar, not email.

Each git commit appears as a blip:

- file name
- AI station that produced it
- linked receipt_id
- linked quest_id
- commit SHA

Click once for side-by-side diff.

Each repo update is auto-tagged to the quest that spawned it.

Jay sees code land in real time, not buried in a feed.

## 6. How Jay Knows The Next Move

The bottom-left Quest Tracker works like an MMO.

It shows:

- Active Quest
- Checklist
- Next Objective
- Suggested Station

Example:

```text
Active Quest: Saint Cloud Parks Drift
Checklist: sources locked [ ] receipt built [ ] courts passed
Next Objective: Send to Claude for table extract
Suggested Station: Claude console pulses
```

If the queue is empty, the center holo flashes:

```text
Awaiting Orders
```

and points to the Intent Card.

The HUD always shows what Jay wanted, not merely what the last AI said.

## 7. How The HUD Prevents Recursion Drift

Three locks prevent recursion drift.

### Hash Chain

Every prompt gets a parent hash.

The Drift Meter shows a tree.

If Jay tries to resend the same prompt to a different AI, it turns yellow and blocks until Jay clicks:

```text
Fork Intent
```

### Canonical Lock

Once a receipt passes the Three Courts, that prompt version is frozen.

No AI can silently rewrite it.

### No Loops

The HUD detects if output A is being fed back into input A without a new source.

It forces Jay to either:

- add a new file
- change the Intent Card
- fork the quest

This stops five models from endlessly rephrasing each other.

## HUD Object Shape

Future schema candidate:

```json
{
  "hud_id": "PLAYER_HUD_V0_1",
  "operator": "Jay Wisdom",
  "mission_beacon": "Ship Minnesota Safety Pass with public-record drifts only",
  "active_leaf": "LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1",
  "active_issue": 94,
  "active_pr": 95,
  "current_receipt_holo": {
    "old_artifact_ref": "",
    "new_artifact_ref": "",
    "old_hash_sha256": "",
    "new_hash_sha256": "",
    "replay_status": ""
  },
  "stations": {
    "ChatGPT": "IDLE",
    "Meta": "IDLE",
    "Microsoft_Copilot": "IDLE",
    "Claude": "IDLE",
    "Grok": "IDLE"
  },
  "pinned": {
    "operator_intent_card": "",
    "three_courts_rules_card": true,
    "canonical_prompt_hash": "",
    "active_source_pair": []
  },
  "action_queue": [],
  "quest_tracker": [],
  "repo_beacon": [],
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Safety Membrane

```json
{
  "chat_thread_center": false,
  "operator_as_memory_buffer": false,
  "prompt_loss_allowed": false,
  "hidden_auto_chaining": false,
  "canonical_lock": true,
  "hash_chain": true,
  "no_loops": true,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Closing Rule

The HUD is a spaceship bridge.

Jay sees the mission, the stations, the queue, and the history wall at once.

Not a chat.
Not an inbox.
Not a feed.

Authority remains false.
