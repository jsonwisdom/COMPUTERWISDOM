# LOOP_STICK_V0_1

Parent: `CMPTRWSDM_PARENT_SCAFFOLD_V0_1`  
Bus: `CMPTRWSDM_CIRCULAR_MISSION_BUS_V0_1`  
Mode: POINTER_ONLY  
Execution: NONE  
Authority created: FALSE  
Canon: FALSE  
Join: FALSE

## Purpose

The loop stick is the smallest mechanical pointer that returns each completed or halted mission cycle to the B0 registry.

It is not a scheduler, trade trigger, publisher, wallet signer, or authority grant.

## Loop

```text
ENTER
  ↓
READ B0 REGISTRY
  ↓
REQUIRED ID ABSENT?
  YES -> HOLD -> RETURN TO B0
  NO  -> B1
  ↓
B1 FREEZE
  ↓
B2 HUMAN APPROVAL
  ↓
B3 PUBLICATION RECEIPT
  ↓
B4-B6 RESERVED / UNATTACHED
  ↓
B7 EXECUTION RECEIPT
  ↓
B8 REPLAY
  ↓
RETURN TO B0
```

## Current register

```text
B0 = PARTIAL
B1 = 0
B2 = 0
B3 = 0
B4 = 0 / UNATTACHED
B5 = 0 / UNATTACHED
B6 = 0 / UNATTACHED
B7 = 0
B8 = 0
NEXT_ACTION = HOLD
```

## Mechanical rule

```text
IF required_bit == 0:
    NEXT_ACTION = HOLD
    RETURN_POINTER = B0
```

No social metric, price event, external model output, meme, or unbound token may override the return pointer.
