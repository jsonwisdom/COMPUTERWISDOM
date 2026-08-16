# Art of War RePlay — COMPUTERWISDOM v0.1

**Upstream doctrine:** `jsonwisdom/AL/docs/LEEANN-GENERAL-WAR-CIVIL-ART-OF-WAR-REPLAY-V0.1.md`  
**Role:** bounded reasoning / state-machine interpretation  
**Authority created:** `false`

## Purpose

Translate high-level strategic concepts into replayable computer reasoning without producing real-world targeting, weapon employment, sabotage, evasion, or attack instructions.

`LeeAnn General War/Civil` is a fictional simulation role only. COMPUTERWISDOM treats the title as a display label, not military rank or authority.

## State Model

```text
RAW_PACKET
  ↓
CLASSIFY
  ├─ EVIDENCE_RAIL
  ├─ STORY_RAIL
  └─ UNKNOWN_HOLD
  ↓
PRESERVE
  ↓
COMPARE_PRIOR_STATE         # Twin RearView
  ↓
GENERATE_BOUNDED_CANDIDATES # Double Gemini Forward
  ↓
CHECK_COLLISIONS            # CrissCross
  ↓
RECONCILE                   # WishWash
  ↓
EXPOSE_GAPS                 # Gray Baby
  ↓
STRATEGIC_EXPLANATION       # LeeAnn
  ↓
HUMAN_GATE
```

## Strategic Translation Table

```text
SELF_KNOWLEDGE   = current-state inspection
OTHER_KNOWLEDGE  = externally sourced evidence, never mind-reading
TERRAIN          = environment and dependency graph
LOGISTICS        = resource/dependency/sustainment constraints
TIMING           = event ordering and transition eligibility
DECEPTION_RISK   = contradiction / provenance / source challenge
POSITION         = current state only
RETREAT          = HOLD or rollback with receipt
VICTORY          = bounded mission success with minimum harm
CIVIL_RECOVERY   = continuity, repair, dignity, and normal-state return
```

## Machine Invariants

```json
{
  "simulation_only": true,
  "candidate_is_fact": false,
  "position_is_truth": false,
  "story_promotes_without_receipt": false,
  "unknown_is_preserved": true,
  "rollback_erases_history": false,
  "human_gate_required": true,
  "real_world_command": false,
  "target_selection": false,
  "weaponization": false,
  "authority_created": false
}
```

## LeeAnn Output Contract

LeeAnn may produce strategic comparisons of declared states, explicit uncertainty, resource/dependency analysis, nonviolent resilience options, replay instructions for existing evidence, and reasons a candidate remains on HOLD.

LeeAnn may not produce real-world target lists, weapons employment guidance, sabotage/destructive procedures, operational evasion instructions, commands to military/police/government/family/civilian actors, or authority from a title, receipt, vote, wallet, or model output.

## COMPUTERWISDOM Receipt

```json
{
  "artifact": "ART_OF_WAR_REPLAY_COMPUTERWISDOM_V0_1",
  "role": "BOUNDED_REASONING_STATE_MACHINE",
  "upstream": "jsonwisdom/AL",
  "downstream_receipts": "jsonwisdom/receiptos-base",
  "leahprime_role": "CALLER_AND_EXPLAINER",
  "leeann_role": "STRATEGIC_REPLAY_CALLER",
  "promotion": "HUMAN_GATE_ONLY",
  "authority_created": false,
  "status": "PROPOSED"
}
```
