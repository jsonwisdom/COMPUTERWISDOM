# COMPUTER WISDOM — Book of Research · Seymour Discovery Index v0.1

**Owner:** Jason Wisdom · **Discovery coordinator:** Seymour (proposed integration; not a live delegation)  
**Snapshot:** 2026-11-18 / GitHub API readback during this session  
**Source:** [Machine-readable PR inventory](./SEYMOUR_RESEARCH_BOOK_PR_INDEX.json)  
**Scope:** `jsonwisdom/COMPUTERWISDOM` pull requests; 88 repositories discovered previously, but not all indexed here.  
**Authorization:** Read/discover/build/test on existing draft branch only. No merge, close, reopen, deploy, publish, spend, sign, or identity change.

## Inventory — nothing discarded

| State | Count | Meaning |
|---|---:|---|
| Open | 219 | Includes 187 draft PRs |
| Closed, merged | 324 | Historical integration, not proof of runtime correctness |
| Closed, unmerged | 16 | Preserve rejected/abandoned research, don't erase |
| **Total** | **559** | Every returned open/closed PR in this repository, four closed pages and three open pages |

All 559 entries in the JSON index include PR number, title, status, dates, commit head, original URL and a short body excerpt. **This is metadata discovery, not an exhaustive file/diff/content audit.** Never call a PR `COMPLETE` solely because it is merged.

## Open these chapters first

1. [#773 Quadratic restoration / continuity](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/773) — active draft checkpoint; evidence status contract and GitHub-first policy.
2. [#753 Eight-agent replay harness](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/753) — deterministic specialist handoffs and replay tests; distinguish simulation from live agents.
3. [#761 Authority-invariant regression](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/761) — 1,024 synthetic configurations, historical source snapshot, scoped evidence.
4. [#770 WOPR stack-flip](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/770) — billing-loss model; synthetic examples, not verified national losses.
5. [#757 A380 recovery console](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/757) — draft recovery research, not a resolution of access.
6. [#771 Shannon evidence attestations](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/771) — unsigned baseline; not proof of signed ownership.

## Closed chapters must remain searchable

- [#745 Wallet2 EIP-191 proof](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/745) — merged; scope to exact signature receipt and replay, not generalized ENS control.
- [#740 Citizen Root audit](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/740) — merged; original evidence and runtime claims require separate checks.
- [#720 REPLAY 007 SQLite nonce](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/720) — merged; read original tests and production boundary before claims.
- [#435 RePlay handoff receipts](https://github.com/jsonwisdom/COMPUTERWISDOM/pull/435) — merged historical handoff design.

## Seymour integration — existing source, not another duplicate

Source repository: [seymour-swarm-orchestrator](https://github.com/jsonwisdom/seymour-swarm-orchestrator).

Existing modules found:
- `src/project-index.ts` — unfinished mission index plus Drive pointers; currently **does not index GitHub PRs**.
- `src/recovery.ts` / `src/mission-state.ts` — durable mission checkpoints, bounded unfinished list.
- `src/task-ledger.ts` — task deduplication, dependencies and outcomes.
- `src/auto-persistence.ts` — synthetic cross-run storage probe.
- `src/investigation-workflow.ts` — workflow continuation design.

**Next drill:** Add a *read-only* GitHub PR adapter to Seymour's project index, ingest this inventory with pagination and immutable source pointers, and test open/closed/merged distinctions, restart recovery, stale snapshots and deduplication. Do not claim live Seymour orchestration until a real deployed recovery readback passes.

## Reading protocol

`OPEN BOOK → choose PR → fetch full PR description + changed files + commit history + CI runs → follow original evidence links → classify scoped claims → identify unfinished work → schedule verified next step`.

The index is an entry point, not a replacement for original receipts. GitHub is public: never commit private chat transcripts, credentials, family records, or private Google Drive document content.

## Continuation checkpoint

**Last verified action:** all 559 PR metadata records written to this draft branch; the book and inventory are available for retrieval.  
**Still missing:** full diff audit, cross-repository commit index, full 700-thread conversation mapping, live Seymour adapter and cross-execution recovery test.  
**Next executable step:** implement read-only GitHub PR adapter in Seymour on a review branch, with tests, under Jason's authorization. No automatic merge or deployment.
