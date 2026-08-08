# ⚙️ RePlay Wisdom Factory Game

A cooperative **agentic game** for Jay, David, and friends.

The game teaches one habit:

> **PASS is not VERIFIED.**

Players propose claims, attack assumptions, run tests, demand independent replay, record receipts, and reflect on what survived.

This is a **pedagogical game**. It does not create protocol authority and does not verify or amend `jsonwisdom/AL`.

## Play Game Zero

Requirements: Node.js 18+.

```bash
cd agentic-game
npm start
```

Optional deterministic playtest seed:

```bash
WISDOM_SEED=42 npm start
```

On Windows PowerShell:

```powershell
$env:WISDOM_SEED=42; npm start
```

## Two-Player Loop

```text
PLAYER 1 CLAIM
      ↓
PLAYER 2 ATTACKS
      ↓
TESTER
      ↓
PASS / FAIL
      ↓
REPLAY!
      ↓
RECEIPT
      ↓
REFLECTION
```

Then roles reverse.

After both claims resolve, Game Zero asks both players:

**Why does VERIFIED require more than PASS?**

The game only sets `gameZeroUnderstood: true` after both explanations and shared agreement.

## Agents

- **Proposer** — states the claim.
- **Skeptic** — attacks an assumption.
- **Tester** — creates the primary test outcome.
- **Replayer** — independently checks the result.
- **Scribe** — records the receipt.
- **Gatekeeper** — refuses to equate PASS with VERIFIED.

## Reflection

Every round asks:

1. What did you believe before?
2. What actually survived?

Reflection happens after success **and** failure.

## Wisdom Points

Wisdom points are game feedback only. More points do not create more authority.

The former “David Jackpot” is now the **Intuition Reward — Non-Canonical** concept: fun for the game, meaningless to the protocol.

## Runtime State

Sessions save locally to:

```text
state/wisdom-graph.json
```

That file is gitignored. Do not submit personal/private session state in issues.

## Receipt Renderer V0.1

`src/renderer/` is a read-only projection boundary for canonical `REPLAY_HANDOFF_V0_1` receipts from `../revenue_agent/schemas/receipt.schema.json`.

The renderer:

- rejects any key matching `^authority(_|$)` anywhere in the receipt;
- rejects malformed receipt digests;
- validates against the canonical closed receipt schema;
- deep-clones and deep-freezes projected values;
- copies `receipt_digest` unchanged and never recomputes it;
- exposes only the projection whitelist;
- never promotes semantic, verification, economic, or authority state.

```text
RECEIPT = SOURCE OF RECORD
RENDERER = READ-ONLY PROJECTION
UI = EXPERIENCE ONLY
AUTHORITY FIELD PRESENT = REJECT
```

Run the renderer security suite with:

```bash
npm install
npm test
```

The current Game Zero CLI does not contain a `SIGNOFF` state. Renderer-to-SIGNOFF wiring is therefore intentionally not fabricated in v0.1; integration remains a separate change after a real state-machine seam exists.

## David + Friends Playtest

For the first public test, play Game Zero once and report:

- Did you understand why PASS was insufficient?
- At what moment did you want to demand REPLAY yourself?
- What confused you?
- Did the Chaos Card help or distract?
- Did Reflection change your opinion of the claim?
- What should tomorrow's build change first?

### Snapchat RePlay feedback lane

Snapchat can be used to share the **experience** of the playtest with friends: reactions, screenshots that contain no private data, and short “what survived?” recaps.

Snapchat sharing is a **feedback/distribution enablement only**. A Snap is not evidence, a game receipt, or protocol authority.

Please move durable feedback into the GitHub feedback issue so tomorrow's work has a replayable record.

## Design Boundary

Read [`DESIGN.md`](./DESIGN.md) before changing game mechanics. It labels mechanics as:

- Canonical Analogy
- Simplified Analogy
- Non-Canonical Gamification

## Game Zero Success

You do **not** win because a claim gets VERIFIED.

You win when both players can explain why a passing test alone was not enough.
