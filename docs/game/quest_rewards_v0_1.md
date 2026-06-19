# Quest Rewards v0.1

Author: Jay Wisdom  
Leaf: LEAF_003_PUBLIC_MEMORY_DRIFT_OBSERVATORY_V0_1  
Game: Public Receipt Arcade / Game of Growth  
Status: Draft  
Authority: false  
Fraud status: UNKNOWN

## Core Rule

Everything a player earns must come from doing the work.

No store.  
No gems.  
No boosters.  
No pay-to-win.  
No clout farming.

If a reward cannot be earned with a receipt, a replay, a lesson, or a correction, it does not exist.

```json
{
  "reward_model": "WORK_EARNED_COLLECTIBLES",
  "store": false,
  "gems": false,
  "boosters": false,
  "pay_to_win": false,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## 1. Collectible Families

Four collectible families exist, one per verified action type.

All collectibles are cosmetic and portable as SVG or PNG.

### Proof Pieces

Earned from receipts.

Proof Pieces are Quarter Tokens stamped with:

- date
- source type
- court

Examples:

- Newsprint Quarter for news article receipts
- Seal Quarter for government PDF receipts

### Replay Relics

Earned from replay.

Replay Relics are Cabinet Decals that players place on their virtual machine.

Examples:

- `3x Verified` bolt
- `Cross-Wire` for different time zones
- `Cold Boot` for replaying something older than one year

### Teacher Tapes

Earned from education.

Teacher Tapes are VHS-style Media Cards summarizing a how-to guide.

Front: the claim.  
Back: the steps.

Other players collect them to learn.

### Oops Orchids

Earned from corrections.

Oops Orchids are the rarest and most respected reward.

A player receives a pink orchid sticker for every public correction they make of their own receipt.

The orchid grows petals the more the player corrects gracefully.

## 2. Replay Badges

Replay badges go on the joystick, not the player's forehead.

They track skill, not fame.

Badges:

- First Try: first successful independent replay
- Three's Company: three different players replayed your receipt
- World Tour: those three are in at least two time zones
- Blind Test: replay completed without seeing the original conclusion first
- Ghost in the Machine: replayed a receipt older than 365 days
- Chain Reaction: your replay enabled five more downstream replays

Each tier changes joystick color:

```text
plastic -> chrome -> glow -> woodgrain
```

No stat boost.
Just flex.

## 3. Parody Art Unlocks

When a receipt passes both Source and Replay, the player unlocks an 8-bit arcade marquee.

The parody targets old game tropes and public-record absurdity, not private people.

Examples:

- Corporate greenwashing receipt -> Eco Invaders
- Political ad spend receipt -> PAC-Man
- Food label receipt -> Snack Attack
- Terms of service receipt -> Terms of Ender
- Health claim receipt -> Dr. Mario Fact Check

Governance by Joystick votes on new templates each quarter.

Artists submit.
Players pick with their joysticks.
Admins do not hand-pick reward skins.

## 4. Seasonal Events

Five short sprints exist, all skill-based.

### Spring Cleaning — March

Correct three receipts older than six months.

Reward: Dust Bunny Decal

### Summer Replay-a-thon — July

48-hour global replay relay.

Reward: Sun-Bleached Quarter

### Back to School — September

Publish a Teacher Tape used by five new players.

Reward: Chalkboard Sticker

### Spooky Sources — October

Find a primary source for a popular myth.

Reward: Ghost Receipt Media Card

### Winter Archive — December

Replay any receipt from last year's event.

Reward: Frosted Orchid petal

Events are announced two weeks early and end exactly on time.

No extensions.  
No paid skips.

## 5. Anti Pay-to-Win Rules

Rewards stay fun by refusing monetized advantage.

Rules:

1. No shop, ever.
2. Cosmetics only.
3. A glowing joystick does not make a vote heavier.
4. Every decal is an open SVG a player can download.
5. Scarcity comes from doing the task, not artificial rarity.
6. Tickets and seasonal decals fade if a player stops contributing for 90 days.
7. New rewards must pass a Governance by Joystick vote with at least 60 percent across all three courts.
8. Developers cannot sell a skin.
9. No loot boxes.
10. No random drops for cash.
11. No leaderboards based on collection size.

## 6. Player Collection Page

The collection page should feel like a pegboard in a garage arcade, not an Instagram profile.

### Top bar

Player joystick with badges clipped on.

### Left shelf — Source

Rows of Quarters.

Each quarter is clickable to the original receipt.

### Middle shelf — Replay

Cabinet Decals arranged like magnets.

### Right shelf — Context

Teacher Tapes fanned out.

Oops Orchids sit in a small vase front and center.

### Underneath

Only three numbers:

- Receipts Verified
- Replays Completed
- Corrections Made

No followers.  
No likes.

### Share formats

- 9:16 story
- square Discord card
- printable PDF

Each share includes a QR code linking to verifiable JSON so anyone can check it offline.

## 7. Why Gen Z Would Share It

### Anti-clout flex

The coolest item is the Oops Orchid.

Owning up is rarer than being right.

### Remix culture

Every piece is CC0 SVG.

Players can make stickers, phone wallpapers, laptop skins, and remixes.

### Co-op credits

Media Cards show all three replay partners' avatars.

Players show it because their crew is on it.

### Story-ready

One tap creates a TikTok green screen of marquee art with receipt steps scrolling behind.

### Skill FOMO, not money FOMO

Seasonal items say:

```text
I was there and did the work.
```

Not:

```text
I paid.
```

### No numbers to chase

Without like counts, showing a board feels like showing a skate deck, not a resume.

## Safety Membrane

```json
{
  "rewards_from_receipts": true,
  "rewards_from_replay": true,
  "rewards_from_education": true,
  "rewards_from_corrections": true,
  "rewards_from_popularity": false,
  "rewards_from_outrage": false,
  "rewards_from_accusation": false,
  "pay_to_win": false,
  "authority": false,
  "fraud_status": "UNKNOWN"
}
```

## Closing Rule

See the change.  
Save the proof.  
Skip the accusation.

Earn the sticker.
Print the proof.
Replay the record.

Authority remains false.
