# Jay Dual Onion Daily v0.1

**Status:** DRAFT / REVIEWABLE OPERATING LAYER  
**Authority:** `AUTHORITY_CREATED = FALSE`  
**Rule:** exploration and story may organize attention; only evidence survives replay.

## Purpose

Jay Dual Onion Daily is a compact daily operating loop that joins the Blocks Explorer with the existing evidence/replay discipline.

```text
BLOCK → EXPLORE → STORY → FAMILY / LEARNING / WORK → CLAIM? → RECEIPT → REPLAY
```

Story is an interface. It is never proof.

## The Two Onions

### Onion A — RECORD

Question: **What does the record actually show?**

```text
CLAIM
  → SOURCE
  → OBSERVATION
  → BYTES / CANONICAL RECORD
  → HASH / VERSION
  → RECEIPT
  → CONTRADICTION CHECK
  → REPLAY
```

Institutional records and public records remain separate inputs until replay compares them.

```text
INSTITUTIONAL RECORD || PUBLIC RECORD
                 ↓
              REPLAY
                 ↓
              COMPARE
                 ↓
        STRUCTURAL DELTA
```

### Onion B — POWER

Question: **Who had authority to do what, and what action actually occurred?**

```text
ACTOR
  → CLAIMED AUTHORITY
  → LAW / POLICY / ROLE
  → ACTION
  → IMPLEMENTATION
  → CONSEQUENCE
  → RECEIPT
  → REPLAY
```

Authority is never inferred from narrative, status, access, identity, or machine output.

## Daily Cycle

### 1. OPEN — choose the active Blocks

Choose one or more:

- **WORK** — verification, provenance, agents, governance, deterministic infrastructure.
- **FAMILY** — continuity, family-safe memory, member spaces.
- **IMAGINATION** — quests, games, stories, exploratory navigation.
- **EVIDENCE** — receipts, hashes, Merkle commitments, replay frames.
- **PUBLIC** — résumé, portfolio, explorer, identity/discovery surfaces.

Record three different object types separately:

```text
OBSERVATION != IDEA != CLAIM
```

### 2. EXPLORE — permit imagination without promotion

Ideas, stories, diagrams, games, and associations may be used to explore the problem space.

```text
STORY = INTERFACE
STORY != SOURCE
STORY != RECEIPT
STORY != AUTHORITY
```

### 3. BIND — route truth claims into Evidence

When an exploration produces a factual or operational claim, bind the minimum chain:

```text
CLAIM → SOURCE → AUTHORITY → ACTION → RECEIPT
```

If a required edge is absent, the claim remains `HOLD`.

### 4. DUAL REPLAY — run both onions independently

**Record replay** checks whether the source trail supports the claimed event or state.

**Power replay** checks whether the named actor, authority, and action are independently supported.

Evidence in one onion may not pay for a missing edge in the other.

### 5. CLOSE — freeze the daily state

Every scoped claim ends the day in exactly one replay state:

- `PASS` — the scoped claim is mechanically supported by bound evidence.
- `HOLD` — a required edge or receipt is missing.
- `CONFLICT` — valid bound records disagree.
- `REJECT` — bound evidence contradicts the scoped claim.

A day does **not** need to end in PASS. `HOLD` and `CONFLICT` are valid preserved states.

## Dual Flywheel

### Institutional Update Loop

```text
SOURCE CHANGE
  → OBSERVE
  → CAPTURE
  → CANONICALIZE
  → HASH
  → RECEIPT
```

### Public Verification Loop

```text
PUBLIC POINTER
  → INDEPENDENT FETCH
  → REPLAY
  → COMPARE
  → DELTA
  → PASS | HOLD | CONFLICT | REJECT
```

The loops may run at different speeds. Machine speed does not create authority.

## Daily Receipt Shape

```json
{
  "date": "YYYY-MM-DD",
  "block": "WORK|FAMILY|IMAGINATION|EVIDENCE|PUBLIC",
  "claim_id": "optional-until-claim-exists",
  "observation": null,
  "idea": null,
  "claim": null,
  "record_onion": {
    "sources": [],
    "canonical_objects": [],
    "hashes": [],
    "contradictions": []
  },
  "power_onion": {
    "actor": null,
    "claimed_authority": null,
    "authority_source": null,
    "action": null,
    "implementation_receipts": []
  },
  "replay_state": "PASS|HOLD|CONFLICT|REJECT|null",
  "next_action": null,
  "carry_forward": true,
  "authority_created": false
}
```

## Block-Specific Boundaries

### Family

Family Blocks may preserve memory, continuity, stories, and member-safe navigation. They do not create institutional, legal, technical, or evidentiary authority.

### Work

Work Blocks may generate claims and proposed actions. Any claim promoted as verified must cross the Evidence Block and survive replay.

### Imagination

Imagination Blocks are intentionally permissive upstream. Their output becomes evidence only if an independent source/receipt is later bound.

### Public

Public Blocks explain, discover, and present. A résumé, portfolio page, ENS name, repository index, or explorer is a discovery surface, not authority.

### OpenAI Platform

Platform organization/project visibility is treated as an **access receipt only**. It is not evidence of production API integration, deployment, employment, endorsement, or institutional authority.

## Standing Invariants

```text
HASH != TRUTH
CONSENSUS != TRUTH
AI OUTPUT != TRUTH
STORY != PROOF
ACCESS != PRODUCTION DEPLOYMENT
ARTIFACT PROOF != EMPLOYMENT PROOF
ARTIFACT PROOF != CREDENTIAL PROOF
AUTHORITY_CREATED = FALSE
MACHINE SPEED != MACHINE AUTHORITY
```

## Promotion Rule

Nothing moves from exploratory description to verified résumé/portfolio claim merely because it is coherent or repeated.

Promotion requires the strongest available public binding appropriate to the claim:

```text
REPO → PATH → COMMIT → TEST/CI → DEPLOYMENT/READBACK
```

Missing edges stay visible.

## Companion Surfaces

- Jay Blocks Explorer Map
- Evidence-Weighted Functional Résumé
- Resume Evidence Appendix
- ReceiptOS / RePlayOS
- COMPUTERWISDOM
- JOY

---

**Canonical daily rule:** Explore freely. Bind narrowly. Replay independently. Preserve uncertainty.
