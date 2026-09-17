# APPLE_BLOSSOM_REV2_TO_REV3_SEMANTIC_DELTA_V0_1

Status: DRAFT_UNSEALED  
Authority created: false  
No silent rewrite: true  
Migration implications binding: false

## Purpose

Preserve and compare the semantic delta between Drive revision 2 and Drive revision 3 of `Apple Blossom Awesome Audit — SideCarSam Scam Test V1` without retroactively assigning semantics to revision 2.

## Source lineage

```text
GitHub historical object:
jsonwisdom/COMPUTERWISDOM
commit: 99a5f172e21a485032db372118bea88d939277a4
path: docs/clawback-machine/APPLE_BLOSSOM_AWESOME_AUDIT_SIDECARSAM_SCAM_V1.md

Drive object:
Apple Blossom Awesome Audit — SideCarSam Scam Test V1
revision 2 modified: 2026-09-15T18:56:20.275Z
revision 3 modified: 2026-09-15T20:22:12.492Z
```

## Receipt draft

```json
{
  "artifact_id": "APPLE_BLOSSOM_REV2_TO_REV3_SEMANTIC_DELTA_V0_1",
  "artifact_type": "semantic_delta_receipt",
  "source": {
    "object": "Apple Blossom Awesome Audit — SideCarSam Scam Test V1",
    "drive_revision": "2",
    "revision_time": "2026-09-15T18:56:20.275Z",
    "terminal_tokens_observed": ["PASS", "DELTA", "HOLD"],
    "explicit_terminal_definitions": false,
    "semantic_definitions_observed": {},
    "canonical_text_sha256": null
  },
  "target": {
    "object": "Apple Blossom Awesome Audit — SideCarSam Scam Test V1",
    "drive_revision": "3",
    "revision_time": "2026-09-15T20:22:12.492Z",
    "terminal_definitions_observed": {
      "PASS": "primary/certified edges close",
      "DELTA": "surfaces differ but relationship is identified",
      "HOLD": "required edge or primary document missing",
      "CONFLICT": "primary receipts disagree",
      "REJECT": "asserted edge contradicted by controlling receipt"
    },
    "canonical_text_sha256": null
  },
  "changes": {
    "PASS": {
      "rev2_token_present": true,
      "rev2_explicit_definition_present": false,
      "rev3_token_present": true,
      "rev3_explicit_definition_present": true,
      "classification": "NARROWER_OR_FORMALIZED",
      "semantic_equivalence": "NOT_ESTABLISHED",
      "notes": "REV3 introduces the first explicit definition observed in this lineage object; REV2 semantics are not inferred."
    },
    "DELTA": {
      "rev2_token_present": true,
      "rev2_explicit_definition_present": false,
      "rev3_token_present": true,
      "rev3_explicit_definition_present": true,
      "classification": "NARROWER_OR_FORMALIZED",
      "semantic_equivalence": "NOT_ESTABLISHED",
      "notes": "REV3 introduces the first explicit definition observed in this lineage object; REV2 semantics are not inferred."
    },
    "HOLD": {
      "rev2_token_present": true,
      "rev2_explicit_definition_present": false,
      "rev3_token_present": true,
      "rev3_explicit_definition_present": true,
      "classification": "NARROWER_OR_FORMALIZED",
      "semantic_equivalence": "NOT_ESTABLISHED",
      "notes": "REV3 introduces the first explicit definition observed in this lineage object; REV2 semantics are not inferred."
    },
    "CONFLICT": {
      "rev2_token_present": false,
      "rev3_token_present": true,
      "classification": "NEW"
    },
    "REJECT": {
      "rev2_token_present": false,
      "rev3_token_present": true,
      "classification": "NEW"
    }
  },
  "migration_implications": {
    "PASS_TO_ADMIT": "CANDIDATE_NOT_PROVEN",
    "DELTA_TO_AUDIT": "DIRECT_RENAME_REJECTED",
    "HOLD_TO_HOLD": "CANDIDATE_NOT_PROVEN",
    "REJECT_TO_REJECT": "CANDIDATE_STRONG",
    "CONFLICT_ROLE": "INPUT_CONDITION_NOT_TERMINAL_VERDICT"
  },
  "migration_implications_binding": false,
  "invariants": {
    "REV2_SEMANTICS_INFERRED": false,
    "ABSENCE_OF_EXPLICIT_DEFINITION_NOT_EQUAL_PROOF_OF_UNDEFINED_HISTORICAL_USAGE": true,
    "NO_SILENT_REWRITE": true,
    "AUTHORITY_CREATED": false
  },
  "requirements_before_seal": [
    "select and prove a canonical revision-text representation",
    "compute REV2_CANONICAL_TEXT_SHA256",
    "compute REV3_CANONICAL_TEXT_SHA256",
    "bind both hashes into this receipt",
    "verify revision timestamps",
    "perform semantic review before setting migration_implications_binding=true"
  ],
  "authority": false,
  "status": "DRAFT_UNSEALED"
}
```

## Gate

```text
REV2_HASH_BOUND = FALSE
REV3_HASH_BOUND = FALSE
SEMANTIC_DELTA_DRAFTED = TRUE
SEMANTIC_DELTA_SEATED = FALSE
MIGRATION_IMPLICATIONS_BINDING = FALSE
V2_SCHEMA_DRAFT = BLOCKED
NO_SILENT_REWRITE = TRUE
AUTHORITY_CREATED = FALSE
```
