# Donald's Dice Game with Onions — Reverse Replay v0.1

**Class:** kid-safe public-record replay game / non-authority  
**Board:** Tom Homan reported $50,000 FBI matter  
**Proposition:** `FBI-TOM-HOMAN-50000-001`  
**AUTHORITY_CREATED:** false  
**PROOF_INFERRED:** false

## Why Donald's Dice Game

This board starts with the public Trump-administration / DOJ ending and walks backward toward the reported 2024 undercover event.

Donald Trump is a **context node** because Homan later served in the Trump administration and the White House publicly defended him. The game does **not** infer that Trump directed the reported 2024 operation, the transfer, the investigation, or its closure without a source-bound edge.

## Prime rule

> **Start at the ending. Roll for the onion. Walk backward. Stop where the receipt stops.**

Dice choose audit order only.

```text
DICE != TRUTH
DICE != GUILT
DICE != AUTHORITY
```

## Reverse board

```text
2026 DOJ / SENATE ANSWERS
        ↑
2025-2026 FOIA + CONGRESSIONAL QUESTIONS
        ↑
2025 DOJ/FBI PUBLIC CLOSURE VERSION
        ↑
2025 MEDIA DISCLOSURE / WHITE HOUSE VERSION
        ↑
2024 REPORTED UNDERCOVER FBI EVENT
        ↑
PRIMARY RECORDING / CASH-CUSTODY BYTE = NOT PUBLICLY ACQUIRED
```

The game is won by reaching a source-bound edge, not by reaching a preferred conclusion.

## D8 — Reverse route die

1. **CLOSURE** — begin with DOJ/FBI's public statement that the matter was reviewed and closed.
2. **SENATE** — inspect later Senate QFR answers for what DOJ would and would not disclose.
3. **HOUSE** — inspect House QFR questions about recordings, cash, timing, and decision-maker.
4. **ACCESS** — inspect FOIA requests/litigation and whether requested bytes became public.
5. **MEDIA** — inspect Reuters/AP/ABC publication snapshots and isolate what remained source-based.
6. **AUTHORITY AT T0** — freeze Homan's legal/official role at the reported 2024 event.
7. **MONEY CUSTODY** — ask what public record documents the reported $50,000 before, during, and after the operation.
8. **PRIMARY BYTE** — ask whether the reported audio/video, close memo, evidence log, or cash-custody record is publicly acquired.

## D4 — Onion die

1. **RECORD / REALITY** — what byte exists?
2. **AUTHORITY** — who had legal authority on that date?
3. **EXECUTION / MONEY / DATA** — who recorded, transferred, stored, reviewed, closed, or retained it?
4. **OVERSIGHT / RECOVERY** — who later asked, reviewed, sued, released, withheld, corrected, or appealed?

## D6 — Shock Glove test die

1. timestamp
2. source identity
3. actor / office-state
4. exact wording
5. custody / system-of-record
6. contradiction / version delta

## ReverseReplay — current run

The first live workflow run established a **byte-retrieval receipt**, not truth of the underlying allegations.

Fetched official/oversight bytes included:

- Senate Judiciary QFR: `4,140,308` bytes — SHA-256 `c43ed362ff9b50f3b85e290bbeceba28b2fb955157d9838237fb4a6b34377638`
- House Judiciary QFR: `124,299` bytes — SHA-256 `b5cb4e9b6de2446f2b31a375e97feb55ae1863f77f905e65fe224b3d190dbf3b`
- Senate oversight statement: `194,755` bytes — SHA-256 `7f967235fa0b3e44e219812d937efbfa4025fa781ad30dc064fda6f20bb9071a`
- Senate FOIA request: `390,487` bytes — SHA-256 `e1cae3cd7bead2f2a2466c6e3449d5189a773731fd7e5e69fd7f3433ea6f56ed`

Media/access fetches were mixed: AP and ABC returned public bytes; Reuters returned HTTP 401 in that workflow run; one access-litigation page returned HTTP 403. Those response codes are **access states**, not evidence deletion or concealment.

## The central reverse replay

```text
END CLAIM:
DOJ/FBI: matter reviewed + closed; no credible evidence of criminal wrongdoing
        ↓ REVERSE
WHO CLOSED IT?                  = HOLD_PUBLIC
WHEN EXACTLY?                   = HOLD_PUBLIC
CLOSE-OUT / DECLINATION MEMO?   = HOLD_PUBLIC
WHAT HAPPENED TO REPORTED CASH? = HOLD_PUBLIC
WHITE HOUSE COMMUNICATIONS?     = HOLD_PUBLIC
        ↓ REVERSE
CONGRESS ASKS THOSE QUESTIONS   = PROVEN
        ↓ REVERSE
FOIA REQUESTS / ACCESS SUITS     = PROVEN
        ↓ REVERSE
MEDIA REPORTS RECORDING + CASH   = BOUND_MULTI_SOURCE / HOLD_PRIMARY
        ↓ REVERSE
PRIMARY RECORDING                = NOT PUBLICLY ACQUIRED
PRIMARY CASH-CUSTODY RECORD      = NOT PUBLICLY ACQUIRED
```

## Version cards

### Card A — Media version

A publication freezes what reporters could support at publication time.

`MEDIA_VERSION[t] = SNAPSHOT`

### Card B — Government version

An agency statement establishes what the agency publicly said. It does not automatically establish every underlying fact.

`OFFICIAL_STATEMENT != COMPLETE_CASE_FILE`

### Card C — Congressional version

Congressional questions prove the questions were asked. They do not prove their factual premises.

`QUESTION != ANSWER`

### Card D — Replay version

BoxD never freezes at the headline. Every new run starts again at the source registry.

```text
SOURCE REGISTRY
→ FETCH PUBLIC BYTES
→ SHA-256
→ COMPARE PRIOR RUN
→ NEW BYTE? NEW HASH? NEW ANSWER?
→ REVERSE REPLAY
→ PROVEN | BOUND | HOLD | CONFLICT | REJECT
```

## Promotion rules

```text
CASE_CLOSED != EVENT_ERASED
CASH_REPORTED != BRIBE_PROVEN
RECORDING_REPORTED != RECORDING_PUBLIC
PRIVATE_CITIZEN != CONTRACTING_AUTHORITY
NO_CREDIBLE_CRIMINAL_EVIDENCE != NO_INVESTIGATIVE_RECORD
FOIA_WITHHELD != DELETED
ACCESS_FAILURE != CONCEALMENT
```

## Win condition

There is no partisan win condition.

A round ends when:

- a missing edge becomes source-bound;
- a claim is rejected by the acquired record;
- conflicting official versions are preserved as `CONFLICT`; or
- no new public receipt exists and the board remains `HOLD`.

> **Donald's Dice Game with Onions: roll the route, peel the layer, reverse the story, keep the receipt.**
