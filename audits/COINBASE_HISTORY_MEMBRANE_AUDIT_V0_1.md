# Coinbase Full-History Membrane Audit v0.1

Status: REVIEW_ONLY

## Scope

This audit covers the public control plane only. Private Coinbase history remains in Google Drive and is not copied into this public repository.

## Findings

- Existing repository doctrine already requires human approval before Coinbase execution.
- The new membrane keeps Drive as the private archive and GitHub as the public logic surface.
- The workflow is always-on for control-plane validation on an hourly schedule and can also be triggered manually or by repository dispatch.
- Trigger classes are observations requiring review. They do not place trades.
- Timestamp differences are eligible trigger evidence but are not causal attribution.

## No-fake-green gates

A full-history result remains HOLD unless the private archive separately proves:
1. explicit pagination terminus for every requested surface,
2. complete chunk inventory,
3. stable-ID reconciliation,
4. hash continuity,
5. timestamp-gap/overlap audit,
6. field-semantics gate appropriate to the requested math.

## Execution

```text
AUTO_EXECUTION = FALSE
HUMAN_APPROVAL_REQUIRED = TRUE
EXECUTION_RECEIPT_REQUIRED = TRUE
AUTHORITY_CREATED = FALSE
```
