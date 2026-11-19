# CI-FIRST Evidence Continuity Contract v0.1

## Purpose
Stop repeated evidence-intake loops and distinguish missing retrieval from missing proof.
This contract is a **draft-branch research scaffold**; it cannot directly change
ChatGPT's native memory, retrieval behavior, or evidence visibility.

## Required order
1. Retrieve the last checkpoint for the exact claim and proof scope.
2. Search authorized existing evidence sources (GitHub / Drive / prior receipts).
3. Reuse original receipts; record immutable references and source metadata.
4. Compare the newly available material with the prior finding.
5. Preserve previous scoped test outcomes; flag contradictions.
6. Only promote a stronger claim after an independently replayable proof.
7. Do not trigger duplicate wallet authentication, spending, deployment or merge.

## Status semantics
| Status | Meaning |
| --- | --- |
| UNKNOWN_NOT_SEARCHED | No source search recorded; never interpret as no evidence. |
| UNKNOWN_NOT_VERIFIED | Search or candidate evidence exists, but the exact scope is not verified. |
| PASS_PREVIOUSLY_VERIFIED | An earlier scoped test passed; reuse within that scope only. |
| FAIL | Evidence/test failed within the specified claim scope. |
| CONFLICT | Retrieved records disagree; reconcile before promotion. |

## Minimum receipt
- claim_id and precisely stated scope
- source and immutable link/commit where possible
- exact test_id and original method
- evidence SHA-256 and test result
- verification timestamp, provenance/chain-of-custody where available
- distinction between *reported* previous PASS and independently replayed proof

A SHA-256 digest checks bytes against a digest, not their authenticity. A GitHub
workflow PASS proves its configured job completed successfully, not wallet ownership.

## Regression criteria
- A previous EIP-191 message-signature PASS never establishes ENS or A380 control.
- Missing retrieval reports UNKNOWN_NOT_SEARCHED.
- Search with no scoped proof reports UNKNOWN_NOT_VERIFIED.
- Contradictory PASS/FAIL reports CONFLICT.
- No unknown status silently overwrites a previous scoped PASS record.
- No result confers signing, spending, merging, identity-change, deployment,
  external publication or consequential authority.

## Execution and boundaries
Run: `python3 -m unittest -v test_audit test_quadratic test_continuity`
Read-only library logic; no network calls, secrets, account changes or deployments.
The current independent graph verification remains 0/6 until actual cryptographic
evidence is obtained and replayed. No global hold; keep master unchanged.
