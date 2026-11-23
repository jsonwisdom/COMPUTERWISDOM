# Jason Wisdom — Historical Rebase Alternatives and Exact-Receipt Replay
**Date:** 2026-11-05  
**Scope:** `jsonwisdom/COMPUTERWISDOM`, historical cross-repository audit doctrine  
**Authority:** false by default; documentation is not authorization.

## Recovered historical anchors

1. **2025-05-07, fork-first workflow (historical conversation evidence):** `jaywisdom/COMPUTERWISDOM` as a fork of `jsonwisdom/COMPUTERWISDOM`; upstream PR proposed in preference to ad-hoc history cleanup. This is a prior-conversation reference, not independently revalidated fork state.
2. **2026-05-27, divergent local/remote history (historical conversation evidence):** `git pull --rebase origin master` was discussed to reconcile before push. It is a local rewrite option, **not** a requirement for evidence-custody workflows.
3. **2026-07-03, archived README rebase residue (repository evidence):** `ARCHIVE/README_REBASE_NOTES_2026-07-03.md` records that PR #202 anti-drift news replay additions were kept during a rebase and master README content retained. It says `truth_claim: false` and `authority: false`.
4. **2026-07-10, historical registry (conversation evidence):** observation-first, no repository history rewriting, deletion or merge before evidence. Reconstruction candidates and projections are not recovered historical bytes.
5. **2026-07-19, AL PR #404 (conversation evidence):** a reported 127-commit envelope motivated splitting / isolating changes and requiring fresh final-head CI; not proof of a later merge.
6. **2026-08-23, independent preservation branches (conversation evidence):** preserve original branch and run CI before proposing any merge; do not infer a merge from a claimed or planned operation.
7. **2026-10-01, explicit merge-method tradeoffs (conversation evidence):** merge commits preserve ancestry; squash and rebase produce new landed commit identities. Old-head CI does not automatically cover new-head commits.
8. **2026-11-05, PR #740 (live GitHub evidence):** user reported rebase merge; `a7e20ac003c610e97c2b8c6c95a767c54e87d3c9` resolves to `homepage: place CI-FIRST audit before Citizen Root and Base navigation`. The `master` homepage now contains the Citizen Root audit and navigation. The previous branch-side homepage commit `79b6f39d1d4ba8be2af743b475dde5d2478dde75` differs from the landed commit. PR merge metadata / parent lineage should be separately preserved before declaring a complete exact-head CI replay.

## Rebase alternatives — what each method retains

| Method | Historical effect | CI-first interpretation |
|---|---|---|
| **No mutation / read-only replay** | Original commits and bytes untouched | Preferred baseline for evidence acquisition and provenance |
| **Isolated branch + pull request** | Preserve base branch; changed commit set is reviewed separately | Run checks against exact proposed head |
| **Merge commit** (no fast-forward) | Keeps the original branch commits reachable in the resulting Git DAG; new merge commit has two parents | Preserve source head, base head, merge SHA and new-head CI |
| **Fast-forward** | Moves branch pointer without creating a merge commit where ancestry permits | Preserve original commits; no separate merge-node evidence |
| **Squash merge** | Creates a single new commit containing aggregated changes; original per-commit ancestry is not embedded in the target history | Retain original PR and source SHAs in an external receipt |
| **GitHub rebase and merge** | Replays individual commits onto target with new SHAs | Record source SHA → landed SHA mapping, exact landed-head CI |
| **Local interactive rebase** | Rewrites commit identities, may alter/drop changes if mishandled | Use disposable branch/worktree only; never rewrite protected evidence without explicit authorization |
| **Cherry-pick** | Copies selected changes to new commits; IDs change | Preserve explicit source→target commit mapping and omitted-change inventory |
| **Patch export and application** | Transfers a diff without retaining ancestry by itself | Store original patch bytes/hash and reconstructed file hashes; label as projection |
| **Revert commit** | Adds an inverse change without erasing prior commit history | Preferred corrective action for a bad publication over historical deletion |

**Graph invariant:** A Git commit graph is a directed acyclic graph. A true merge commit with two parents records ancestry; a rebase creates different commit objects on a new ancestry path. Wolfram graph evaluation confirmed the illustrative 2-parent merge graph is acyclic; the specific PR #740 parent and mapping details remain subject to exact commit inspection.

## PR #740 — correction record, not backdated permission

- Project: `jsonwisdom/COMPUTERWISDOM`.
- Branch-side homepage commit: `79b6f39d1d4ba8be2af743b475dde5d2478dde75`.
- Reported merge method: rebase.
- Verified landed commit: `a7e20ac003c610e97c2b8c6c95a767c54e87d3c9`.
- Live `master/index.html`: Citizen Root link and retrospective audit link present.
- Retrospective audit: `docs/CITIZEN_ROOT_AUDIT_2026-11-05.md`; it correctly preserves the **preflight audit gap = FAIL**.
- No evidence here establishes fresh post-rebase CI on the exact landed SHA or independent DNS/TLS/HTTP proof. **UNKNOWN until those receipts are collected.**

## Required minimal replay receipt for future operations

```json
{
  "project": "COMPUTERWISDOM",
  "method": "rebase-and-merge",
  "source_head_sha": "79b6f39d1d4ba8be2af743b475dde5d2478dde75",
  "landed_commit_sha": "a7e20ac003c610e97c2b8c6c95a767c54e87d3c9",
  "source_to_landed_map": "UNKNOWN",
  "final_head_ci": "UNKNOWN",
  "preflight_audit": "FAIL",
  "independent_http_check": "UNKNOWN",
  "authority_created": false,
  "wallet_execution": false
}
```

## CI-FIRST next gates

1. Read the original PR metadata, source and landed commits, and exact Git parent graph; archive refs without rewriting historical commits.
2. Check `verify` status and workflow artifacts for **the landed commit**, not just the PR source head.
3. Rehash independently materialized original evidence bytes where authorized, then attach receipts with source IDs.
4. Confirm externally observable homepage and Citizen Root HTTP/TLS state; do not equate configured infrastructure with successful service.
5. Keep authority, wallet ownership, payments, and citizen benefits separate from DNS, GitHub, and ENS discovery.

**Boundary law:** No receipt, no authority. No replay, no promotion. No secret in repo. No fake green.
