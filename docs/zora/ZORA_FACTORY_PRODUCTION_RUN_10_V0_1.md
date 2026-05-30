# ZORA_FACTORY_PRODUCTION_RUN_10_V0_1

Author: jaywisdom  
Control Plane: Computer Wisdom  
Candidate Generator: Meta  
Scope: 10-item Zora Factory production run  
Status: Candidate production plan  
Authority: false  
Membrane: HOLDS  

## Purpose

Define a 10-artifact Zora Factory production run where Meta generates and renders candidate artifacts, Computer Wisdom structures and gates them, GitHub records them, and Zora publishes only after receipt approval.

## Core Rule

No item in this run becomes public canon until it has:

- source artifact
- rendered artifact
- metadata JSON
- metadata hash
- operator approval
- replay acquisition receipt after publication

## Operator Routing

Operator Jay routes.  
Computer Wisdom controls structure.  
Meta proposes and renders candidates.  
Codex / Cloud Shell executes file and hash operations.  
GitHub records.  
Zora publishes only after receipts exist.  
Authority remains false.

## Production Run Items

| Slot | Artifact ID | Candidate Title | Status | Destination |
| --- | --- | --- | --- | --- |
| 01 | ZF10-001 | Operator Jay Routes | CANDIDATE | docs/zora/render_prompts/ |
| 02 | ZF10-002 | Computer Wisdom Control Plane | CANDIDATE | docs/zora/render_prompts/ |
| 03 | ZF10-003 | Meta Candidate Engine | CANDIDATE | docs/zora/render_prompts/ |
| 04 | ZF10-004 | Codex Execution Lane | CANDIDATE | docs/zora/render_prompts/ |
| 05 | ZF10-005 | GitHub Records Surface | CANDIDATE | docs/zora/render_prompts/ |
| 06 | ZF10-006 | Zora Public Surface | CANDIDATE | docs/zora/render_prompts/ |
| 07 | ZF10-007 | Receipt Constraint Gate | CANDIDATE | docs/zora/render_prompts/ |
| 08 | ZF10-008 | Replay Confidence Engine | CANDIDATE | docs/zora/render_prompts/ |
| 09 | ZF10-009 | No Source No Post | CANDIDATE | docs/zora/render_prompts/ |
| 10 | ZF10-010 | Membrane Holds | CANDIDATE | docs/zora/render_prompts/ |

## Metadata Requirements Per Item

Each item must eventually produce:

```json
{
  "artifact_id": "ZF10-001",
  "name": "...",
  "description": "...",
  "image": "ipfs://... or https://...",
  "external_url": "...",
  "attributes": [
    { "trait_type": "Run", "value": "ZORA_FACTORY_PRODUCTION_RUN_10_V0_1" },
    { "trait_type": "Authority", "value": "false" },
    { "trait_type": "Reversibility Class", "value": "SYMBOLIC" },
    { "trait_type": "Status", "value": "CANDIDATE" }
  ]
}
```

## Render Rule

Meta may render or describe visual candidates, but every output remains SYMBOLIC_CANDIDATE until Computer Wisdom records the artifact and Operator Jay approves promotion.

## Publication Rule

Do not publish to Zora until:

1. rendered artifact exists,
2. metadata JSON exists,
3. metadata hash is computed,
4. Operator Jay approves public surface,
5. post-publication replay acquisition receipt is generated.

## Final Invariant

Meta builds candidate artifacts.  
Computer Wisdom structures the run.  
Receipts constrain publication.  
Zora publishes after approval.  
Authority remains false.
