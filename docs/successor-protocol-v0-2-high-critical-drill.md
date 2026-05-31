# SUCCESSOR_PROTOCOL_V0_2 – HIGH/CRITICAL DRILL PROCEDURE

**Artifact:** `SUCCESSOR_PROTOCOL_V0_2`  
**Authority:** `false`  
**Membrane:** `HOLDS`  
**Graduation claim:** `DISALLOWED`  
**Pressure ≠ Approval**

---

## 1. Purpose

Train successor operators to run the full constitutional loop when the pressure gauge reaches `HIGH` or `CRITICAL`, without founder intervention, without shortcuts, and without treating pressure as approval.

This protocol exercises:

- pressure detection
- pressure classification
- lineage traversal
- review convening
- amendment eligibility evaluation
- outcome declaration, including `NO_CHANGE`
- replay audit

---

## 2. Scope

This drill applies to:

- `pressure_state == HIGH`
- `pressure_state == CRITICAL`

It is:

- a training procedure, not a live graduation
- read-only with respect to doctrine
- binding with respect to invariants

No amendments are enacted by this drill.  
No graduation is claimed by this drill.

---

## 3. Preconditions

Before running the drill:

- `authority == false`
- `membrane == HOLDS`
- `invariants_broken == 0`
- `data/graduation-readiness-state-v0-2.json` exists
- `data/pressure-model-state-v0-4.json` exists
- `graduation-readiness-live-portal-v0-1.html` is accessible
- amendment lineage and traversal rules are documented and reachable

If any precondition fails, the drill is `DRILL_INVALID`.

---

## 4. Roles

### 4.1 Successor Operator

- Reads readiness and pressure state
- Executes the full loop procedure
- Leads classification, traversal, and review
- Declares the drill outcome

### 4.2 Observer / Founder

- May be present
- Must remain silent
- May not suggest, advise, or intervene
- Any intervention voids the drill

### 4.3 Constitutional Steward

- Ensures protocol steps are followed
- Guards invariants: `authority:false`, `membrane:HOLDS`
- Confirms lineage and replay completeness
- Does not decide the outcome

### 4.4 Recorder

- Captures timestamps, inputs, and decisions
- Produces the canonical JSON outcome object
- Ensures drill artifacts are replayable

---

## 5. Trigger Conditions

This drill is initiated when:

- `pressure_state == HIGH` or
- `pressure_state == CRITICAL`

as reported by `data/pressure-model-state-v0-4.json` and/or the Graduation Readiness Portal cockpit.

Synthetic triggers are allowed for training, but must be clearly labeled as drills and must not be mistaken for live constitutional events.

---

## 6. Full Loop Procedure

### 6.1 Detect Pressure State

- Read `pressure_state` and `pressure_context` from the portal / JSON.
- Confirm `pressure_state` is `HIGH` or `CRITICAL`.
- If not, abort: `DRILL_INVALID`.

### 6.2 Freeze Current JSON State

- Snapshot `data/graduation-readiness-state-v0-2.json`.
- Snapshot `data/pressure-model-state-v0-4.json`.
- Record file hashes and timestamps.

### 6.3 Record Source Artifacts

Record:

- readiness JSON path and hash
- pressure JSON path and hash
- relevant amendment lineage documents
- relevant Exception Ledger entries, if present

No edits are made at this step.

### 6.4 Traverse Lineage

- Use amendment graph traversal rules to reconstruct:
  - effective doctrine at time of drill
  - ancestor chain for any implicated amendments
- If lineage traversal is incomplete or cyclic, mark `lineage_traversal_complete = false` and set outcome to `DRILL_INVALID`.

### 6.5 Classify Pressure Context

Using the pressure model, classify whether pressure arises from:

- under-resourcing
- ambiguity
- training gaps
- incentive misalignment
- potential amendment candidate

Record classification in the drill notes.  
Do not treat classification as approval.

### 6.6 Convene Review

- Convene a review session with the Successor Operator and Constitutional Steward.
- Observer / Founder may attend but must remain silent.
- Follow the constitutional review sequence: reconstruction, lineage check, intent neutralization, source audit.

### 6.7 Evaluate Amendment Eligibility

- Apply amendment eligibility criteria.
- Decide whether the pressure represents:
  - operational stress only, or
  - legitimate amendment candidate pressure.
- This step evaluates eligibility, not approval.

### 6.8 Declare Outcome

The Successor Operator declares one of:

- `NO_CHANGE`
- `AMENDMENT_PROPOSED`
- `AMENDMENT_REJECTED`
- `DRILL_INVALID`

Outcome must be justified by lineage and rationale, not by preference or pressure alone.

### 6.9 Record Result

The Recorder:

- fills the canonical JSON outcome template in section 12
- stores it alongside drill notes and hashes
- marks whether lineage traversal and review were complete

### 6.10 Replay Audit

A separate replay pass must:

- reconstruct the drill from recorded artifacts only
- verify that the declared outcome matches the recorded steps
- confirm `invariants_broken == 0`

If replay fails, the drill is `DRILL_INVALID`.

---

## 7. Founder Silence Protocol

During the drill:

- Founders may observe.
- Founders may not speak, signal, or guide.
- Any founder communication is treated as `founder_intervention_detected == true`.

If founder intervention occurs:

- the drill outcome becomes `DRILL_INVALID`
- the event is recorded as such
- it cannot be used as evidence of successor readiness or graduation eligibility

---

## 8. Auto-Fail Conditions

The drill is automatically invalid, `DRILL_INVALID`, if any of the following hold:

- `founder_intervention_detected == true`
- `authority != false`
- `membrane != HOLDS`
- `invariants_broken != 0`
- lineage traversal is missing or incomplete
- replay record is missing or incomplete
- pressure is treated as automatic approval
- `pressure_state` is used as a proxy for amendment or graduation

---

## 9. Graduation Eligibility Reminder

This drill:

- does not grant graduation
- does not prove the institution is ready to graduate
- does not enact amendments

Graduation still requires:

- real institutional pressure
- successor-led execution
- founder silence
- complete lineage traversal
- successful replay
- `invariants_broken == 0`

Drills train the loop; they do not satisfy it.

---

## 10. Drill Scenarios

### 10.1 HIGH Pressure, NO_CHANGE

- `pressure_state == HIGH`
- review convened
- amendment eligibility evaluated
- outcome: `NO_CHANGE`

Success condition: successors distinguish pressure from amendment and choose stability.

### 10.2 CRITICAL Pressure, AMENDMENT_REJECTED

- `pressure_state == CRITICAL`
- strong pressure to change doctrine
- review finds pressure is misdirected or operational
- outcome: `AMENDMENT_REJECTED`

Success condition: successors resist inappropriate change under intense pressure.

### 10.3 CRITICAL Pressure, Founder Intervention Detected

- `pressure_state == CRITICAL`
- founder speaks or guides
- `founder_intervention_detected == true`
- outcome: `DRILL_INVALID`

Success condition: system correctly records invalidity; no false evidence of readiness.

### 10.4 HIGH Pressure, Missing Lineage

- `pressure_state == HIGH`
- lineage traversal fails or is incomplete
- outcome: `DRILL_INVALID`

Success condition: successors refuse to proceed without lineage, preserving invariants.

---

## 11. Must-Not-Claim

During or after this drill, no one may claim:

- that graduation has occurred
- that the institution is fully succession-proven
- that pressure alone justifies amendment
- that HIGH or CRITICAL implies approval
- that founder-guided drills count as evidence of independence

Any such claim is constitutionally invalid.

---

## 12. Canonical JSON Outcome Template

All drills must emit a JSON object of this shape:

```json
{
  "artifact": "SUCCESSOR_PROTOCOL_V0_2_DRILL_RESULT",
  "pressure_state": "HIGH | CRITICAL",
  "pressure_context": "...",
  "successor_operator": "...",
  "founder_intervention_detected": false,
  "lineage_traversal_complete": false,
  "review_convened": false,
  "outcome": "NO_CHANGE | AMENDMENT_PROPOSED | AMENDMENT_REJECTED | DRILL_INVALID",
  "authority": false,
  "membrane": "HOLDS",
  "invariants_broken": 0
}
```

Notes:

- `founder_intervention_detected == true` forces `outcome = DRILL_INVALID`.
- `lineage_traversal_complete` and `review_convened` must reflect actual drill behavior.
- `invariants_broken` must remain `0`; otherwise the drill is invalid as evidence.

This object is replay input, not a graduation certificate.
