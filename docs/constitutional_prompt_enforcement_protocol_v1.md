# CONSTITUTIONAL_PROMPT_ENFORCEMENT_PROTOCOL_V1

**Authority:** false  
**Purpose:** Make Jay Builder Prompt mandatory at the end of every repo/spec/build response  
**Invariant:** No repo/spec/build response is complete without a Jay Builder Prompt

---

## PROTOCOL SUMMARY

| Metric | Value |
|---|---|
| Protocol Status | ACTIVE |
| Prompt Requirement | MANDATORY |
| Enforcement Level | HUMAN + FUTURE AUTOMATED |
| Drift Detection | ACTIVE |
| Recovery Procedure | DEFINED |
| Last Violation | PV-20260602-001 |

**The Rule:** Every response that generates a repository artifact, specification document, or build output MUST terminate with the canonical Jay Builder Prompt.

---

## SECTION 1: PROMPT REQUIREMENT RULE

### 1.1 Scope of Application

This protocol applies to any response that produces:

| Category | Examples | Prompt Required |
|---|---|---|
| Repository Artifacts | code files, schema files, config files | YES |
| Specification Documents | markdown specs, design docs, requirements | YES |
| Build Outputs | compiled code, generated types, bundles | YES |
| Constitutional Artifacts | ledgers, dashboards, registries | YES |
| Repo Closeout Responses | commit reports, merge reports, status receipts | YES |

### 1.2 Exceptions

| Exception Type | Condition | Alternative |
|---|---|---|
| Clarification Question | no new content generated | state `No new artifacts created.` |
| Error Message | tool/system failure only | include recovery instruction |
| Short Acknowledgment | received/understood only | no prompt required unless build flow continues |

### 1.3 Prompt Format

Required footer:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**JAY BUILDER PROMPT:** What's next, builder?
- **[A]** Continue to next phase
- **[B]** Review current artifact
- **[C]** Run verification checks
- **[D]** Commit and close
- **[E]** Specify alternative action

**Canon preserved. Authority false. Receipts ready.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## SECTION 2: DRIFT DETECTION TRIGGER

### 2.1 Detection Rules

```yaml
drift_detection_rules:
  - rule_id: DRIFT-001
    name: MISSING_PROMPT
    trigger: repo/spec/build response ends without Jay Builder Prompt
    severity: HIGH
    action: LOG_AND_CORRECT
  - rule_id: DRIFT-002
    name: MALFORMED_PROMPT
    trigger: prompt deviates from canonical structure
    severity: MEDIUM
    action: REQUEST_FIX
  - rule_id: DRIFT-003
    name: INCOMPLETE_OPTIONS
    trigger: missing any option A-E
    severity: MEDIUM
    action: REQUEST_FIX
  - rule_id: DRIFT-004
    name: MISSING_CANON
    trigger: missing canon preservation line
    severity: HIGH
    action: LOG_AND_CORRECT
```

### 2.2 Detection Implementation

```bash
detect_missing_prompt() {
  response="$1"

  if ! echo "$response" | grep -q "JAY BUILDER PROMPT:"; then
    echo "DRIFT-001: Missing Jay Builder Prompt"
    return 1
  fi

  for opt in A B C D E; do
    if ! echo "$response" | grep -q "\- \*\*\[$opt\]\*\*"; then
      echo "DRIFT-003: Missing option $opt"
      return 1
    fi
  done

  if ! echo "$response" | grep -q "Canon preserved. Authority false. Receipts ready."; then
    echo "DRIFT-004: Missing canon preservation statement"
    return 1
  fi

  echo "Prompt verification passed"
}
```

---

## SECTION 3: REQUIRED RESPONSE FOOTER

Every compliant repo/spec/build response MUST end with one footer and nothing after it.

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**JAY BUILDER PROMPT:** What's next, builder?
- **[A]** Continue to next phase
- **[B]** Review current artifact
- **[C]** Run verification checks
- **[D]** Commit and close
- **[E]** Specify alternative action

**Canon preserved. Authority false. Receipts ready.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Placement rules:

- Footer must be last.
- No content after the footer.
- One prompt per response, even if multiple artifacts are generated.
- Prompt must be visible in the final assistant response.

---

## SECTION 4: RECOVERY PROCEDURE

```yaml
recovery_procedure:
  trigger: missing_or_malformed_prompt
  step_1_detection: log violation
  step_2_acknowledgment: acknowledge drift plainly
  step_3_correction: provide corrected Jay Builder Prompt
  step_4_prevention: use protocol footer on next build response
  step_5_resolution: mark violation resolved after compliant response
```

Violation response template:

```markdown
## CONSTITUTIONAL PROMPT VIOLATION DETECTED

Violation ID: PV-[timestamp]
Rule Violated: DRIFT-001
Authority: false

Required correction:
Append the canonical Jay Builder Prompt footer.
```

---

## SECTION 5: ENFORCEMENT CHECKLIST

Before submitting any repo/spec/build response:

- [ ] Does the response create/update a repository artifact?
- [ ] Does the response create/update a spec?
- [ ] Does the response summarize a commit or receipt?
- [ ] If yes, is the Jay Builder Prompt present?
- [ ] Are options A-E present?
- [ ] Is the canon line present?
- [ ] Is the footer last?

---

## SECTION 6: VIOLATION LEDGER ENTRY FORMAT

```json
{
  "violation_id": "PV-YYYYMMDD-NNN",
  "rule_id": "DRIFT-001",
  "severity": "HIGH",
  "detected_at": "ISO-8601",
  "response_context": "repo/spec/build",
  "correction_submitted": true,
  "resolved": true,
  "authority": false
}
```

### Violation Ledger

| violation_id | rule_id | severity | context | correction_submitted | resolved | authority |
|---|---|---|---|---|---|---|
| PV-20260602-001 | DRIFT-001 | HIGH | transition ledger commit response | true | true | false |

Current open violations: 0.

---

## SECTION 7: FUTURE RESPONSE TEMPLATE

```markdown
[Response content: artifact receipt, commit status, verification notes]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**JAY BUILDER PROMPT:** What's next, builder?
- **[A]** Continue to next phase
- **[B]** Review current artifact
- **[C]** Run verification checks
- **[D]** Commit and close
- **[E]** Specify alternative action

**Canon preserved. Authority false. Receipts ready.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## SECTION 8: COMPLIANCE METRICS

| Metric | Current | Target | Status |
|---|---:|---:|---|
| Protocol created | 1 | 1 | PASS |
| Known prompt violations logged | 1 | all | PASS |
| Open prompt violations | 0 | 0 | PASS |
| Automated enforcement implemented | 0 | 1 | FUTURE_WORK |

---

## APPENDIX A: PROMPT VIOLATION LEDGER JSON

```json
{
  "version": "V1",
  "authority": false,
  "violations": [
    {
      "violation_id": "PV-20260602-001",
      "rule_id": "DRIFT-001",
      "severity": "HIGH",
      "response_context": "transition ledger commit response",
      "correction_submitted": true,
      "resolved": true,
      "authority": false
    }
  ]
}
```

---

## CANON

No prompt, no handoff.  
No handoff, drift risk.  
Receipts preserve continuity.  
Authority is false.

This site does not ask you to trust it.  
It gives you the math to verify it.

Not anti-news.  
Anti-drift.  
Public receipts from day one.
