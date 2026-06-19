# CONSTITUTIONAL_STATUS_TRANSITION_RULES_V1

Authority: false  
Purpose: Formalize allowed and forbidden transitions between constitutional states  
Invariant: No state transition without receipt evidence

---

## State Machine Overview

```txt
NONE
  -> DOCUMENTED_ONLY
  -> IMPLEMENTED
  -> VERIFIED
  -> DEPLOYED

ANY_STATE
  -> ANCHORED_MODIFIER

ANY_STATE
  -> DEMOTED
```

`ANCHORED` is a modifier, not a replacement for the underlying status.

---

## 1. Transition Matrix

### Allowed Transitions

| From State | To State | Transition ID | Required Receipts | Description |
|---|---|---|---|---|
| NONE | DOCUMENTED_ONLY | T-001 | DOC_RECEIPT | initial artifact documentation |
| DOCUMENTED_ONLY | IMPLEMENTED | T-002 | DOC_RECEIPT + CODE_RECEIPT or SCHEMA_RECEIPT | spec becomes code/schema |
| IMPLEMENTED | VERIFIED | T-003 | TEST_RECEIPT + CI_RECEIPT | implementation passes verification |
| VERIFIED | DEPLOYED | T-004 | DEPLOYMENT_RECEIPT | verified artifact becomes public runtime/deployment |
| ANY | ANCHORED_MODIFIER | T-005 | ANCHOR_RECEIPT | cross-repo or external anchor verified |
| ANY | DEMOTED | T-006 | DEMOTION_RECEIPT | state demoted due to failure/drift |
| DEMOTED | DOCUMENTED_ONLY | T-007 | DOC_RECEIPT + DEMOTION_RESOLUTION_RECEIPT | recovery starts at documented state |
| ANCHORED_MODIFIER | ANCHORED_MODIFIER | T-008 | ANCHOR_RECEIPT | anchor renewal |

### Forbidden Transitions

| From State | To State | Reason | Severity |
|---|---|---|---|
| DOCUMENTED_ONLY | VERIFIED | skipped implementation | CRITICAL |
| DOCUMENTED_ONLY | DEPLOYED | skipped implementation and verification | CRITICAL |
| IMPLEMENTED | DEPLOYED | skipped verification | CRITICAL |
| IMPLEMENTED | DOCUMENTED_ONLY | use demotion | MEDIUM |
| VERIFIED | IMPLEMENTED | use demotion | MEDIUM |
| VERIFIED | DOCUMENTED_ONLY | use demotion | MEDIUM |
| DEPLOYED | IMPLEMENTED | use rollback/demotion | CRITICAL |
| DEPLOYED | DOCUMENTED_ONLY | use rollback/demotion | CRITICAL |
| DEMOTED | VERIFIED | must recover through DOCUMENTED_ONLY | CRITICAL |
| DEMOTED | DEPLOYED | must recover through full path | CRITICAL |
| ANY | ANCHORED_MODIFIER without ANCHOR_RECEIPT | missing target verification | MEDIUM |

---

## 2. Transition Receipt Requirements

### T-001: NONE to DOCUMENTED_ONLY

Required:

- DOC_RECEIPT

Guard:

- artifact path exists
- authority posture is false

### T-002: DOCUMENTED_ONLY to IMPLEMENTED

Required:

- DOC_RECEIPT
- CODE_RECEIPT or SCHEMA_RECEIPT

Guard:

- implementation exists
- implementation matches documented path/spec
- authority posture remains false

### T-003: IMPLEMENTED to VERIFIED

Required:

- TEST_RECEIPT
- CI_RECEIPT

Guard:

- tests pass
- CI passes
- critical invariants are tested
- no self-issued final verification

### T-004: VERIFIED to DEPLOYED

Required:

- DEPLOYMENT_RECEIPT

Guard:

- public endpoint or release exists
- smoke tests pass
- rollback path exists

### T-005: ANY to ANCHORED_MODIFIER

Required:

- ANCHOR_RECEIPT

Guard:

- target exists
- target hash/SHA recorded
- target authority posture false

### T-006: ANY to DEMOTED

Required:

- DEMOTION_RECEIPT

Guard:

- demotion reason is recorded
- evidence hash is recorded
- prior state is preserved in history

### T-007: DEMOTED to DOCUMENTED_ONLY

Required:

- DOC_RECEIPT
- DEMOTION_RESOLUTION_RECEIPT

Guard:

- root cause is documented as resolved
- artifact restarts below implementation status

### T-008: ANCHORED_MODIFIER renewal

Required:

- ANCHOR_RECEIPT

Guard:

- target changed or renewal window requires fresh receipt
- old anchor remains visible in history

---

## 3. Rollback Transitions

| Original Path | Rollback Path | Required Receipts | Allowed |
|---|---|---|---|
| VERIFIED to DEPLOYED | DEPLOYED to VERIFIED | ROLLBACK_RECEIPT | yes |
| IMPLEMENTED to VERIFIED | VERIFIED to IMPLEMENTED | DEMOTION_RECEIPT + TEST_FAILURE_REPORT | yes |
| DOCUMENTED_ONLY to IMPLEMENTED | IMPLEMENTED to DOCUMENTED_ONLY | DEMOTION_RECEIPT + IMPLEMENTATION_DIVERGENCE_REPORT | yes |
| ANY to ANCHORED_MODIFIER | remove anchor modifier | ANCHOR_REVOCATION_RECEIPT | yes |

Rollback receipt sketch:

```json
{
  "receipt_id": "RLL-001",
  "receipt_class": "ROLLBACK_RECEIPT",
  "artifact_id": "ADN-000",
  "from_status": "DEPLOYED",
  "to_status": "VERIFIED",
  "reason": "ROLLBACK_FAILED_SMOKE",
  "evidence_hash": "sha256:...",
  "issued_by": "deployment-automation",
  "issued_at": "ISO-8601",
  "authority": false
}
```

---

## 4. Forbidden Transition Registry

| forbidden_id | from_state | to_state | reason | severity |
|---|---|---|---|---|
| FT-001 | DOCUMENTED_ONLY | VERIFIED | skipped implementation | CRITICAL |
| FT-002 | DOCUMENTED_ONLY | DEPLOYED | skipped implementation and verification | CRITICAL |
| FT-003 | IMPLEMENTED | DEPLOYED | skipped verification | CRITICAL |
| FT-004 | IMPLEMENTED | DOCUMENTED_ONLY | use demotion | MEDIUM |
| FT-005 | VERIFIED | IMPLEMENTED | use demotion | MEDIUM |
| FT-006 | VERIFIED | DOCUMENTED_ONLY | use demotion | MEDIUM |
| FT-007 | DEPLOYED | IMPLEMENTED | use rollback/demotion | CRITICAL |
| FT-008 | DEPLOYED | DOCUMENTED_ONLY | use rollback/demotion | CRITICAL |
| FT-009 | ANY | ANCHORED_MODIFIER without target receipt | missing target verification | MEDIUM |
| FT-010 | DEMOTED | VERIFIED | must recover through DOCUMENTED_ONLY | CRITICAL |
| FT-011 | DEMOTED | DEPLOYED | must recover through full path | CRITICAL |

---

## 5. Machine-Readable State Automaton

```json
{
  "automaton": {
    "name": "ConstitutionalStatusTransitionAutomaton",
    "version": "V1",
    "authority": false,
    "states": [
      "DOCUMENTED_ONLY",
      "IMPLEMENTED",
      "VERIFIED",
      "DEPLOYED",
      "ANCHORED_MODIFIER",
      "DEMOTED"
    ],
    "initial_state": "DOCUMENTED_ONLY",
    "transitions": [
      {
        "id": "T-001",
        "from": "NONE",
        "to": "DOCUMENTED_ONLY",
        "receipts": ["DOC_RECEIPT"],
        "guard": "artifact_path_exists_and_authority_false"
      },
      {
        "id": "T-002",
        "from": "DOCUMENTED_ONLY",
        "to": "IMPLEMENTED",
        "receipts": ["DOC_RECEIPT", "CODE_RECEIPT_OR_SCHEMA_RECEIPT"],
        "guard": "implementation_matches_spec"
      },
      {
        "id": "T-003",
        "from": "IMPLEMENTED",
        "to": "VERIFIED",
        "receipts": ["TEST_RECEIPT", "CI_RECEIPT"],
        "guard": "tests_and_ci_pass"
      },
      {
        "id": "T-004",
        "from": "VERIFIED",
        "to": "DEPLOYED",
        "receipts": ["DEPLOYMENT_RECEIPT"],
        "guard": "smoke_test_and_rollback_path_exist"
      },
      {
        "id": "T-005",
        "from": "ANY",
        "to": "ANCHORED_MODIFIER",
        "receipts": ["ANCHOR_RECEIPT"],
        "guard": "target_exists_and_authority_false",
        "modifier": true
      },
      {
        "id": "T-006",
        "from": "ANY",
        "to": "DEMOTED",
        "receipts": ["DEMOTION_RECEIPT"],
        "guard": "demotion_reason_valid"
      },
      {
        "id": "T-007",
        "from": "DEMOTED",
        "to": "DOCUMENTED_ONLY",
        "receipts": ["DOC_RECEIPT", "DEMOTION_RESOLUTION_RECEIPT"],
        "guard": "root_cause_resolved"
      }
    ],
    "forbidden_transitions": [
      {"from": "DOCUMENTED_ONLY", "to": "VERIFIED"},
      {"from": "DOCUMENTED_ONLY", "to": "DEPLOYED"},
      {"from": "IMPLEMENTED", "to": "DEPLOYED"},
      {"from": "IMPLEMENTED", "to": "DOCUMENTED_ONLY"},
      {"from": "VERIFIED", "to": "IMPLEMENTED"},
      {"from": "VERIFIED", "to": "DOCUMENTED_ONLY"},
      {"from": "DEPLOYED", "to": "IMPLEMENTED"},
      {"from": "DEPLOYED", "to": "DOCUMENTED_ONLY"},
      {"from": "DEMOTED", "to": "VERIFIED"},
      {"from": "DEMOTED", "to": "DEPLOYED"}
    ]
  }
}
```

---

## 6. Transition Guard Conditions

Guard: implementation matches spec

```bash
# future implementation
# verify spec path, implementation path, required exports/fields, and authority posture
```

Guard: tests and CI pass

```bash
# future implementation
# verify TEST_RECEIPT and CI_RECEIPT exist and match current commit
```

Guard: deployment smoke test passes

```bash
# future implementation
# verify DEPLOYMENT_RECEIPT and public endpoint
```

Guard: anchor target exists and authority false

```bash
# future implementation
# verify ANCHOR_RECEIPT target SHA/content hash
```

---

## 7. Transition Audit Trail

Every transition must record:

```json
{
  "transition_id": "T-003-001",
  "artifact_id": "ADN-000",
  "from_state": "IMPLEMENTED",
  "to_state": "VERIFIED",
  "receipt_hashes": ["TST-001", "CI-001"],
  "guard_conditions_passed": ["tests_pass", "ci_pass", "authority_false"],
  "timestamp": "ISO-8601",
  "transition_issuer": "github-actions",
  "transition_hash": "sha256:...",
  "authority": false
}
```

Current transition history:

```json
{
  "verified_transitions": 0,
  "implemented_transitions": 1,
  "deployment_transitions": 0,
  "anchor_transitions": 0,
  "authority": false
}
```

---

## 8. Transition Enforcement

Pre-transition checks:

```txt
1. transition is allowed
2. required receipts exist
3. forbidden receipts are absent
4. guard conditions pass
5. authority is false
```

Post-transition requirements:

```txt
1. append transition record
2. bind receipt hashes
3. update promotion ledger
4. update state dashboard
5. preserve prior state in history
```

---

## Appendix A: Transition Ledger JSON Sketch

```json
{
  "version": "V1",
  "authority": false,
  "ledger": [
    {
      "transition_id": "T-002-001",
      "artifact_id": "ADN-005",
      "from_state": "DOCUMENTED_ONLY",
      "to_state": "IMPLEMENTED",
      "receipts": ["SCH-001"],
      "issuer": "repo commit",
      "authority": false
    }
  ]
}
```

---

## Canon

State is observable.  
Receipts are verifiable.  
Promotion is traceable.  
Authority is false.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
