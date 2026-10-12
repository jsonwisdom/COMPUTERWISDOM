# Sentinel Arena v0.1

Status: EXPERIMENTAL / NON-AUTHORITATIVE  
Authority: false  
Remediation: disabled by contract

The Sentinel Arena is a replayable evidence-adjudication surface for COMPUTERWISDOM. It allows two or more instruments to submit competing hypotheses against a shared evidence set, calibrates those hypotheses from the evidence actually referenced, preserves dissent, and emits a non-authoritative **State of Reality** report for Orchestrator review.

It is not a governor, deployment agent, or automatic remediation system.

## Constitutional boundary

```text
Sentinel / Arena: observe -> question -> investigate -> answer -> calibrate -> report -> escalate
Orchestrator: decide
Builders / Scalers / Perfectors: act
```

The Arena MUST keep:

```text
authority: false
remediation_applied: false
```

A successful Arena run is a finding, not permission to act.

## Why an Arena

The Arena makes institutional disagreement explicit and machine-replayable instead of collapsing it into one narrative. A round contains one falsifiable question, at least two competing instruments/hypotheses, a shared evidence set, declared confidence from each instrument, reliability and severity on each evidence item, support/contradiction edges linking evidence to hypotheses, and a decision policy for evidence coverage, disagreement, and escalation.

Declared confidence is retained for audit, but the runtime does not treat confidence as evidence. It computes a separate calibrated confidence from weighted support, weighted contradiction, and evidence coverage.

## Runtime

```bash
python3 knowledge-management/arena/arena.py \
  knowledge-management/fixtures/valid/arena-round-minimal.json
```

Write the report:

```bash
python3 knowledge-management/arena/arena.py \
  knowledge-management/fixtures/valid/arena-round-minimal.json \
  --output /tmp/state-of-reality.json
```

The runtime uses only the Python standard library.

## Status rules

- `insufficient_evidence`: no hypothesis has the configured minimum relevant evidence coverage.
- `contested`: the top two calibrated scores remain within the configured disagreement threshold.
- `resolved`: one hypothesis leads beyond the disagreement threshold. This is still non-authoritative.
- `escalate`: evidence at or above the configured severity threshold is present and must be routed to the Orchestrator.

Unknown remains a valid outcome. A contested round intentionally returns no winning instrument.

## Proportionate skepticism

The Arena does not enforce equal-and-opposite skepticism. Evidence is weighted by its declared reliability and by whether it supports or contradicts a hypothesis. A weak contrarian claim therefore does not receive artificial parity with a strongly evidenced claim, while dissenting hypotheses remain visible in the report.

## Replay properties

A round is deterministic except for `generated_at`. Given the same round JSON, the same scoring and status result is produced. Reports preserve declared vs calibrated confidence, support and contradiction weights, evidence coverage, missing evidence references, dissenting hypotheses, critical evidence IDs, recommended next actions, and escalation state.

## Contracts

- `knowledge-management/contracts/arena/ArenaRound.v0.1.0.json`
- `knowledge-management/contracts/arena/ArenaReport.v0.1.0.json`

The repository contract validator compiles both schemas. Arena fixtures are included in the auditor-contract validation lane.

## Non-goals for v0.1

The Arena does not autonomously ingest private systems, call external models, change production state, grant authority, or execute recommendations. Future adapters may generate questions or evidence candidates, but those adapters must still emit replayable round records and remain inside the same authority boundary.
