# CONSTITUTIONAL_RECEIPT_REQUIREMENTS_V1

Authority: false  
Purpose: Define the minimum receipt required before any artifact may be promoted  
Invariant: No silent category promotion. Plans are not implementations. Implementations are not verification. Verification is not deployment. Receipts distinguish them all.

---

## Promotion Ladder

```txt
DOCUMENTED_ONLY --[DOC_RECEIPT + SCHEMA_RECEIPT/CODE_RECEIPT]--> IMPLEMENTED
IMPLEMENTED     --[TEST_RECEIPT + CI_RECEIPT]------------------> VERIFIED
VERIFIED        --[DEPLOYMENT_RECEIPT]--------------------------> DEPLOYED
CROSS_REPO      --[ANCHOR_RECEIPT]------------------------------> ANCHORED
```

Rules:

- No artifact may skip a required receipt class.
- No receipt may be self-issued as final proof.
- Every receipt must be independently verifiable.
- Receipts must be listed in `CONSTITUTIONAL_RECEIPT_LEDGER_V1` or attached as CI/deployment artifacts.
- A receipt describes evidence; it does not create authority.

---

## 1. Promotion Rules

### 1.1 DOCUMENTED_ONLY to IMPLEMENTED

Required receipt:

```txt
DOC_RECEIPT + one of SCHEMA_RECEIPT or CODE_RECEIPT
```

Conditions:

- specification exists at documented path
- implementation exists at expected path
- implementation matches specification
- authority field or authority posture is verified false

Prohibitions:

- cannot promote with only documentation
- cannot promote with partial implementation
- cannot promote with `authority:true`

### 1.2 IMPLEMENTED to VERIFIED

Required receipt:

```txt
TEST_RECEIPT + CI_RECEIPT
```

Conditions:

- test suite covers specification claims
- tests pass in CI environment
- deterministic replay checks pass where relevant
- no known failing constitutional invariant

Prohibitions:

- cannot promote with manual testing only
- cannot promote with failing tests
- cannot promote with untested critical edge cases

### 1.3 VERIFIED to DEPLOYED

Required receipt:

```txt
DEPLOYMENT_RECEIPT
```

Conditions:

- artifact is deployed to production or public verification surface
- deployment passes smoke tests
- rollback procedure is documented
- monitoring or public verification path exists

Prohibitions:

- cannot promote from staging only
- cannot promote without rollback plan
- cannot promote without public verification route

### 1.4 Cross-Repo Anchoring

Required receipt:

```txt
ANCHOR_RECEIPT
```

Conditions:

- artifact is referenced from another repository
- reference includes target commit SHA or content hash
- target authority posture is verified false
- reference direction is documented

---

## 2. Receipt Classes

| Receipt Class | Purpose | Issued By | Storage Location | Expiration |
|---|---|---|---|---|
| DOC_RECEIPT | spec exists and is complete | reviewer or constitutional officer | receipt ledger | never unless doc changes |
| SCHEMA_RECEIPT | JSON schema validates | automated validator | CI artifact / receipt ledger | schema change |
| CODE_RECEIPT | code implements spec | compiler + reviewer | PR / receipt ledger | code change |
| TEST_RECEIPT | tests pass | test runner / CI | CI artifact | test change |
| CI_RECEIPT | pipeline green | GitHub Actions | workflow run | next run |
| DEPLOYMENT_RECEIPT | artifact publicly deployed | deployment automation | deployment log / receipt ledger | deployment change |
| ANCHOR_RECEIPT | cross-repo link verified | cross-repo verification job | receipt ledger | link or target change |

---

## 3. Implementation Evidence

### 3.1 SCHEMA_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| Schema file exists | `ls schemas/*.schema.json` | file found |
| Schema is valid JSON | `jq . schemas/artifact.schema.json` | parses without error |
| Schema has authority false where applicable | `jq '.properties.authority.const'` | equals false or not applicable |
| Schema has strict property posture | `jq '.additionalProperties'` | equals false |
| Example validates | `ajv validate -s schema.json -d example.json` | exit code 0 |

SCHEMA_RECEIPT format:

```json
{
  "receipt_type": "SCHEMA_RECEIPT",
  "artifact_id": "ADN-XXX",
  "schema_path": "schemas/artifact.v1.schema.json",
  "ajv_version": "8.x",
  "validation_hash": "sha256:...",
  "authority_check": "PASS",
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "ajv-ci",
  "authority": false
}
```

### 3.2 CODE_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| Code file exists | `ls src/anti_drift_news/*.ts` | file found |
| TypeScript compiles | `tsc --noEmit` | exit code 0 |
| No authority true posture | `grep -r "authority.*true" src/` | no unsafe matches |
| Required exports exist | `grep "export" src/anti_drift_news/*.ts` | expected exports found |
| No production debug leakage | review / lint | no unsafe debug paths |

CODE_RECEIPT format:

```json
{
  "receipt_type": "CODE_RECEIPT",
  "artifact_id": "ADN-XXX",
  "code_path": "src/anti_drift_news/replay.ts",
  "tsc_version": "5.x",
  "authority_check": "PASS",
  "exports": ["replayGame", "validateEvent", "computeEventHash"],
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "tsc-ci",
  "authority": false
}
```

### 3.3 DOC_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| Spec file exists | `ls docs/**/*.md` | file found |
| Spec has authority false | `grep "Authority: false" <doc>` | found or equivalent JSON authority false |
| Spec has canon phrase | `grep "Not anti-news" <doc>` | found where applicable |
| Required sections present | compare against template | no missing sections |
| Links resolve | link checker / file existence | no broken local links |

DOC_RECEIPT format:

```json
{
  "receipt_type": "DOC_RECEIPT",
  "artifact_id": "ADN-XXX",
  "doc_path": "docs/anti_drift_news/spec_v1.md",
  "sections": 10,
  "links_valid": true,
  "authority_check": "PASS",
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "constitutional-review",
  "authority": false
}
```

---

## 4. Verification Evidence

### 4.1 TEST_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| Test file exists | `ls tests/**/*.test.ts` | file found |
| Tests pass | `npm test` | 100% pass rate for required suite |
| Edge cases covered | `npm run test:edge-cases` | required cases pass |
| No skipped critical tests | `grep "test.skip" tests/` | no critical skips |

TEST_RECEIPT format:

```json
{
  "receipt_type": "TEST_RECEIPT",
  "artifact_id": "ADN-XXX",
  "test_path": "tests/anti_drift_news/replay.test.ts",
  "tests_passed": 87,
  "tests_failed": 0,
  "edge_cases_covered": ["timestamp", "authority", "duplicate", "hash"],
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "test-ci",
  "authority": false
}
```

### 4.2 CI_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| CI workflow exists | `ls .github/workflows/*.yml` | file found |
| Workflow passes | GitHub Actions status | green check |
| Determinism check passes | `npm run replay:determinism` | deterministic state output |
| Schema validation passes | `npm run validate:schemas` | exit code 0 |

CI_RECEIPT format:

```json
{
  "receipt_type": "CI_RECEIPT",
  "artifact_id": "ADN-XXX",
  "workflow_path": ".github/workflows/anti-drift-validate.yml",
  "last_run_status": "PASS",
  "determinism_checks": 100,
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "github-actions",
  "authority": false
}
```

---

## 5. Runtime Evidence

### 5.1 DEPLOYMENT_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| Public endpoint reachable | `curl <endpoint>` | 200 OK |
| Smoke test passes | `npm run smoke:production` | exit code 0 |
| Rollback documented | `ls docs/rollback/*.md` | file exists |
| Public verification available | `adn verify ...` | state verifies |

DEPLOYMENT_RECEIPT format:

```json
{
  "receipt_type": "DEPLOYMENT_RECEIPT",
  "artifact_id": "ADN-XXX",
  "environment": "production",
  "endpoint": "https://api.anti-drift.news/snapshot",
  "smoke_test": "PASS",
  "rollback_documented": true,
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "deployment-automation",
  "authority": false
}
```

---

## 6. Cross-Repo Evidence

### 6.1 ANCHOR_RECEIPT Requirements

| Requirement | Verification Command | Pass Condition |
|---|---|---|
| Target repo accessible | `git ls-remote <repo>` | exit code 0 |
| Target SHA exists | `git cat-file -e <sha>` | object exists |
| Authority posture verified | `grep "authority" <target>` | false posture found |
| Reference documented | inspect both docs | source reference exists |

ANCHOR_RECEIPT format:

```json
{
  "receipt_type": "ANCHOR_RECEIPT",
  "source_artifact": "ADN-XXX",
  "source_repo": "COMPUTERWISDOM",
  "target_repo": "AL",
  "target_artifact": "CONSISTENCY_CONSTITUTIONAL_BUILD_V1",
  "target_sha": "abc123def456",
  "authority_check": "PASS",
  "bidirectional": false,
  "issued_at": "2026-06-02T00:00:00Z",
  "issued_by": "cross-repo-ci",
  "authority": false
}
```

---

## 7. Constitutional Promotion Matrix

| Artifact Type | DOCUMENTED_ONLY to IMPLEMENTED | IMPLEMENTED to VERIFIED | VERIFIED to DEPLOYED |
|---|---|---|---|
| Schema | DOC_RECEIPT + SCHEMA_RECEIPT | TEST_RECEIPT + CI_RECEIPT | deployment only if hosted |
| Code | DOC_RECEIPT + CODE_RECEIPT | TEST_RECEIPT + CI_RECEIPT | DEPLOYMENT_RECEIPT |
| Test | DOC_RECEIPT + CODE_RECEIPT | TEST_RECEIPT + CI_RECEIPT | not applicable unless published |
| Documentation | DOC_RECEIPT | not applicable unless independently audited | DEPLOYMENT_RECEIPT if hosted |
| Cross-Repo | reference documented | ANCHOR_RECEIPT | ANCHOR_RECEIPT plus deployment if applicable |

---

## 8. Promotion Checklist

### 8.1 DOCUMENTED_ONLY to IMPLEMENTED

```md
## Promotion Request: ARTIFACT_NAME

Current Status: DOCUMENTED_ONLY
Requested Status: IMPLEMENTED

Receipts Attached:
- [ ] DOC_RECEIPT
- [ ] SCHEMA_RECEIPT or CODE_RECEIPT

Verification:
- [ ] Implementation matches spec
- [ ] Authority false verified
- [ ] Paths match constitutional index

Receipt Hash: sha256:...
```

### 8.2 IMPLEMENTED to VERIFIED

```md
## Promotion Request: ARTIFACT_NAME

Current Status: IMPLEMENTED
Requested Status: VERIFIED

Receipts Attached:
- [ ] TEST_RECEIPT
- [ ] CI_RECEIPT

Verification:
- [ ] Required tests pass
- [ ] Critical edge cases covered
- [ ] Determinism checks pass where applicable

Receipt Hash: sha256:...
```

### 8.3 VERIFIED to DEPLOYED

```md
## Promotion Request: ARTIFACT_NAME

Current Status: VERIFIED
Requested Status: DEPLOYED

Receipts Attached:
- [ ] DEPLOYMENT_RECEIPT

Verification:
- [ ] Rollback documented
- [ ] Public endpoint accessible
- [ ] Public verification path works

Receipt Hash: sha256:...
```

---

## 9. Receipt Validation

Example validation helpers:

```bash
validate_doc_receipt() {
  receipt="$1"
  doc_path=$(jq -r '.doc_path' "$receipt")
  test -f "$doc_path" || return 1
  grep -q "Authority: false\|authority.*false" "$doc_path" || return 1
  echo "DOC_RECEIPT valid"
}

validate_schema_receipt() {
  receipt="$1"
  schema_path=$(jq -r '.schema_path' "$receipt")
  validation_hash=$(jq -r '.validation_hash' "$receipt")
  actual_hash=$(sha256sum "$schema_path" | cut -d' ' -f1)
  [ "$actual_hash" = "${validation_hash#sha256:}" ] || return 1
  echo "SCHEMA_RECEIPT valid"
}

validate_test_receipt() {
  receipt="$1"
  tests_passed=$(jq -r '.tests_passed' "$receipt")
  tests_failed=$(jq -r '.tests_failed' "$receipt")
  [ "$tests_failed" -eq 0 ] || return 1
  [ "$tests_passed" -gt 0 ] || return 1
  echo "TEST_RECEIPT valid"
}
```

---

## 10. Violation Consequences

| Violation | Detection | Consequence | Remediation |
|---|---|---|---|
| Promotion without receipt | audit finds missing receipt | demote to previous status | issue proper receipt |
| Self-issued final receipt | issuer equals unchecked implementer | receipt invalidated | independent verification |
| Authority true posture | grep/schema/test catches it | promotion blocked | fix and re-verify |
| Incomplete tests | test coverage gap | promotion blocked | add tests |
| Flaky CI | inconsistent workflow runs | CI_RECEIPT revoked | stabilize tests |

---

## Appendix A: Receipt Registry Entry

```json
{
  "artifact_id": "ADN-XXX",
  "artifact_name": "ARTIFACT_NAME",
  "promotion_history": [
    {
      "from_status": "DOCUMENTED_ONLY",
      "to_status": "IMPLEMENTED",
      "receipts": ["DOC_RECEIPT", "CODE_RECEIPT"],
      "issued_at": "2026-06-02T00:00:00Z",
      "issued_by": "reviewer-or-ci",
      "authority": false
    },
    {
      "from_status": "IMPLEMENTED",
      "to_status": "VERIFIED",
      "receipts": ["TEST_RECEIPT", "CI_RECEIPT"],
      "issued_at": "2026-06-03T00:00:00Z",
      "issued_by": "github-actions",
      "authority": false
    }
  ],
  "current_status": "VERIFIED",
  "latest_receipt_hash": "sha256:...",
  "authority": false
}
```

---

## Canon

Plans are not implementations.  
Implementations are not verification.  
Verification is not deployment.  
Receipts distinguish them all.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
