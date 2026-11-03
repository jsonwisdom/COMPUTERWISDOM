# ENS First — GitHub Quest Board

Non-Canonical Gamification, under ../../DESIGN.md. A standalone learning board; it does not alter Game Zero, canonical receipts, ENS state, CI verdicts or merge policy.

Run from the repository root with Node 18+:

```sh
node agentic-game/quests/ens-first/board.mjs
node --test agentic-game/quests/ens-first/board.test.mjs
```

Opening quest: **Name Cartographer**. Input label: jaywisdom.eth, unverified. Forward resolution, reverse resolution, control and GitHub binding are separate checkpoints. The existing projects/ziggy/ens/README.md is the local contract.

Six quests, 100 possible learning points: ENS map (10), control review (20), repository binding (20), CI replay lesson (20), counter-receipt (20), teach-back (10). No monetary prizes, token rewards or automatic writes.

The board initially awards zero. Optional local JSON ledger:

```json
[{"quest_id":"ENS_MAP","kind":"LEARNING_REVIEW","review_ref":"local:review-001","reflection":"Resolution alone did not establish control."}]
```

Pass its file path as the first argument. Store personal ledgers outside the repository. The CLI reads but never writes them. A review reference is a pointer supplied by a player, not an authenticated receipt. Game scoring checks progression and required text only. It never validates signatures, ENS responses, GitHub control or evidence. Anyone can fabricate a ledger: scores are educational feedback, not credentials. Repeated quests do not earn extra points; out-of-order rows are rejected and must be submitted again after prerequisites.

## Current starting state

At inspected master commit c1280bae2b2be33ddedad4bce918f928c4f8d0eb, receipts/anchor/ENS_TEXT_RECORD_POINTER_001.json labels the optional pointer prepared, with ens_record_written=false. This is repository state, not a fresh onchain observation. No ENS write is authorized by playing this board.

PR #590 is a case study, not an automatically completed quest. Connector metadata read this turn returned open, draft=true, merged=false, head 5cff857a6e0707fa81d273b4343ef3c2e047d65b. The pull-request workflow-runs connector returned seven successful runs on its first page. This is a different denominator from the supplied nine check-run summary; it does not establish full coverage or a contradiction.

The inspected constitutional_checks.yml listens to opened, edited, synchronize, reopened, labeled, unlabeled and ready_for_review. Preserve this correction to the supplied narrower event list. The agentic-game-renderer.yml path filter includes agentic-game/**, so this change is eligible for that workflow. Eligibility does not guarantee execution or success.

A merge_commit_sha field can refer to a test merge; merged=false and merged_at=null remain the merge state. Passing checks, learning points and ready-for-review do not authorize merge or trade.

## Replay boundaries

ENS discovers; control proofs prove only their scoped challenge; GitHub contextualizes; workflow checks cover their tested inputs. Separate source receipts from review notes. Preserve mismatches and UNKNOWN. Independent evidence checks and any future transaction require their own receipts.

No signatures are requested, no ENS records updated, no PRs merged and no Coinbase orders issued by this board.
