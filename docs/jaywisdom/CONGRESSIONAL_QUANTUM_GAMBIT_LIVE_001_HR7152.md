# Congressional Quantum Gambit — Live Receipt 001 — H.R. 7152

Observer: `jaywisdom.base.eth`

## Claim under test

The U.S. House of Representatives passed H.R. 7152 — the Civil Rights Act of 1964 — on 1964-02-10 by a recorded vote of 290–130.

## Six-Dice Receipt

| Die | Element | Result |
|---|---|---|
| 1 | SOURCE | PASS |
| 2 | AUTHORITY | PASS |
| 3 | CLAIM | PASS |
| 4 | MONEY | NOT_REQUIRED |
| 5 | TIME | PASS |
| 6 | REPLAY | PASS |

## Official source convergence

- National Archives, House Roll Call 32: February 10, 1964; H.R. 7152 passed 290 to 130.
- National Archives engrossed-copy feature: final House-passed text; 290 in favor to 130 against on February 10, 1964.
- U.S. House History, Art & Archives / Office of the Clerk: February 10, 1964; final tally 290 to 130.
- Congress.gov actions overview: House passage 1964-02-10; Senate passage 1964-06-19; Public Law 88-352 on 1964-07-02.

## Scoped disposition

```text
OBSERVER_RESULT = REPLAYABLE
SEMANTIC_TYPE = BOUNDED_CONGRESSIONAL_EVIDENCE_GATE_DISPOSITION
CLAIM_SCOPE = HOUSE_PASSAGE_ONLY
HOUSE_PASSAGE_DATE = 1964-02-10
HOUSE_VOTE = 290-130
```

## Constitutional / legislative membranes

```text
PASSED_HOUSE != LAW
HOUSE_PASSAGE != SENATE_PASSAGE
HOUSE_PASSAGE != ENACTMENT
REPLAYABLE != LEGAL_CONCLUSION
```

The claim under test is House passage only. The later Senate-passage and enactment states are separately recorded only to prevent state collapse.

## BoxD boundary

This receipt binds source URLs but does not claim that source bytes have been frozen or authenticated.

```text
BOXD_MANIFEST = CANDIDATE_ONLY
SOURCE_URLS_BOUND = TRUE
SOURCE_BYTES_FETCHED_AND_FROZEN = FALSE
SOURCE_DIGEST_RECOMPUTED = FALSE
SOURCE_BYTE_AUTHENTICATION = NOT_PERFORMED

SOURCE_BOUND_PUBLIC_RECORD != BOXD_BYTES_PROVEN
```

## Mechanical close

```text
facts_promoted = 0
edges_inferred = 0
silent_inference = BLOCKED
authority_created = false
```
