# Wave 1 Feedback Ledger

**Compute Wisdom — Constitutional Verification Framework**  
**Public, Replayable, Append-Only Critique Record**

This directory is the canonical public ledger for Wave 1 critique.

It exists to ensure:

- no hidden reviewer queue
- no private authority channel
- no off-repo canonical feedback
- no email-based governance pathway
- all critique is publicly contextualized
- synthesis is transparent and traceable

## What Belongs Here

- Summaries of GitHub Issue critiques
- Links to original issues
- Categorized findings: constitutional, replay, protocol, failure modes, offline parity
- Synthesis notes
- Proposed v1.4 adjustments, non-binding

## What Does Not Belong Here

- PII
- Raw private reviewer notes
- Decisions, approvals, or governance actions
- Runtime semantics
- Authority-bearing statements

## Ledger Rules

- Append-only
- No deletion
- No rewriting history
- Each entry must reference a GitHub Issue ID
- Each entry must include a timestamp
- Each entry must be replayable

## Ledger File Naming

```text
YYYY-MM_waveX_ledger.md
```

Wave 1 begins with:

```text
2026-05_wave1_ledger.md
```

## Boundary

The feedback ledger is a synthesis surface. It is not a governance surface, approval mechanism, runtime, or source of authority.
