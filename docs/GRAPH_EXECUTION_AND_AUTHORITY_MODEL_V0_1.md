# GRAPH_EXECUTION_AND_AUTHORITY_MODEL_V0_1

## Status

```text
artifact: GRAPH_EXECUTION_AND_AUTHORITY_MODEL_V0_1
repository: jsonwisdom/COMPUTERWISDOM
classification: DESIGN_DOCUMENT
authority: false
truth_claim: false
phase: DESIGN
issued_at: 2026-07-31
```

This document is doctrine + contract sketch only. It does not elevate authority,
claim truth, or promote any graph into an executable control plane.

## Purpose

COMPUTERWISDOM already contains multiple graph layers with strong doctrine and
weak runtime unification. This document defines a single execution-and-authority
model that:

1. Unifies existing graph types without replacing them.
2. Distinguishes execution, evidence, authorization, and truth.
3. Specifies typed nodes and edges with static validation rules.
4. Binds every execution result to replay receipts.
5. Preserves the standing posture: `authority: false`.

## Central Distinctions (Non-Negotiable)

```text
execution dependency  !=  evidence relationship
evidence relationship !=  authorization
authorization         !=  truth
replay success        !=  promotion
```

No edge type may cross these boundaries by implication.

## Existing Graph Layers (Preserved)

| Layer | Primary artifacts | Role |
|---|---|---|
| Repository / authority topology | `ROOT_BINDING.md`, `CHARTER.md` | Role and boundary map |
| Anchor / publication topology | `FINAL_ANCHOR_TOPOLOGY_v1.md` | Layer law (Replay / GitHub / EAS / ENS) |
| Cross-repo dependency graph | `docs/master_jsonwisdom_repo_graph_v1.md` | Repo roles and audit lanes |
| Amendment lineage graph | `data/amendment-graph-state-v0-8.json`, explorer | Provenance + traversal (currently empty) |
| Relationship / collaboration graphs | Goblin Court graph, Collaboration Graph schema | Typed relations with confidence / evidence |
| Claim graph (executable surface) | `signal-core/core.py` | Canonicalization + hash under `authority: NONE` |
| Workflow roles | `BRANCH_INTERACTION_MANIFEST_V1.md` | Legislative / Executive / Judicial / AL / Replay |

These layers remain authoritative for their own scope. This model supplies the
missing common runtime contract above them.

## Layer Law (Inherited and Reinforced)

```text
Replay verifies.
GitHub contextualizes.
EAS witnesses.
ENS discovers.
```

No layer may impersonate another.

## Typed Node Contract (V0.1)

Every node in an executable or validation graph MUST declare:

```json
{
  "node_id": "string (stable, unique within graph)",
  "node_kind": "task | checker | gate | receipt | artifact | role | state",
  "authority": false,
  "inputs": ["node_id"],
  "outputs": ["node_id or artifact_ref"],
  "receipt_required": true,
  "failure_policy": "fail_closed | fail_open | isolate",
  "scope": "string",
  "metadata": {}
}
```

### Node kinds

- **task** — performs work; produces artifacts and/or receipts.
- **checker** — pure validation node; must not mutate state; fail-closed by default.
- **gate** — admission or promotion decision; cannot itself create authority.
- **receipt** — immutable record of a prior execution or observation.
- **artifact** — content or reference that is hashed and bound.
- **role** — declared actor (Legislative, Executive, Judicial, AL, Replay, etc.).
- **state** — named condition (e.g. membrane HOLDS, authority false).

Checker nodes are first-class. A graph without explicit checkers is incomplete
for any path that claims validation or promotion readiness.

## Typed Edge Contract (V0.1)

Every edge MUST declare:

```json
{
  "edge_id": "string",
  "from": "node_id",
  "to": "node_id",
  "edge_kind": "DATA_DEP | VERIFY_DEP | AUTH_DEP | ORDER_ONLY | EVIDENCE | SUPPRESSES | WITNESSES | SUPERSEDES | PRODUCES_RECEIPT_FOR",
  "authority": false,
  "confidence": "asserted | observed | verified | unresolved",
  "evidence_refs": [],
  "must_not_imply": []
}
```

### Edge kind semantics

| Kind | Meaning | Forbidden implications |
|---|---|---|
| `DATA_DEP` | Data must exist before consumer runs | Does not imply verification or authority |
| `VERIFY_DEP` | Consumer may run only after successful verification | Does not imply authority or promotion |
| `AUTH_DEP` | Explicit authorization dependency (still authority:false unless elevated) | Does not equal truth |
| `ORDER_ONLY` | Sequencing constraint only | No data, verification, or authority claim |
| `EVIDENCE` | Source provides evidence about target | Not causal, not authoritative |
| `SUPPRESSES` | Soft or hard suppression signal | Not proof of falsehood |
| `WITNESSES` | Observational witness | Not legitimacy |
| `SUPERSEDES` | Later record replaces earlier for a named scope | Scope-limited |
| `PRODUCES_RECEIPT_FOR` | Execution of source yields a receipt bound to target | Receipt ≠ promotion |

Edges that claim proof, liability, or authoritative causation remain forbidden
(as already stated in the Goblin Court relationship graph).

## Static Validation Rules (DAG + Semantic)

A graph is statically invalid if any of the following hold:

1. Cycle involving `DATA_DEP`, `VERIFY_DEP`, or `AUTH_DEP`.
2. Missing dependency: a declared input has no producing edge.
3. Unreachable node required by a declared root or admission path.
4. Checker node has side-effect outputs.
5. Gate node lacks at least one `VERIFY_DEP` or explicit checker predecessor
   when used on a promotion path.
6. Any edge or node asserts `authority: true` without a linked
   authority-elevation receipt lineage.
7. Fan-in (diamond) convergence without an explicit convergence policy
   (`all_must_succeed | quorum | any | ordered`).
8. Partial branch failure at convergence without a declared policy.

### Diamond / fan-out / fan-in primitive

```text
          A
         / \
        B   C
         \ /
          D
```

- Fan-out from A must declare whether B and C are independent or ordered.
- Fan-in at D must declare convergence policy and failure policy.
- Default convergence policy: `all_must_succeed` + `fail_closed`.

## Execution Receipts

Every executed node (and optionally every edge traversal) produces a receipt
compatible with existing receipt doctrine (`docs/REPLAY_RECEIPT_SPEC_V1.md`,
`docs/EXECUTION_RECEIPT_SCHEMA_V1.md`, signal-core binding patterns).

Minimum receipt fields:

```json
{
  "receipt_id": "...",
  "graph_id": "...",
  "node_id": "...",
  "edge_ids": [],
  "inputs_hash": "...",
  "outputs_hash": "...",
  "result": "pass | fail | isolate",
  "authority": false,
  "replay_instructions": "...",
  "timestamp": "...",
  "actor_or_role": "..."
}
```

Replay success of a receipt does not promote the node, the graph, or any claim.

## Authority Elevation Path (Unchanged)

Authority remains false by default. Elevation still requires the full path
already defined in CHARTER and ROOT_BINDING:

1. Dedicated authority-elevation PR
2. Governance artifact defining requested authority
3. Machine-generated attestation / receipt
4. Lineage to the relevant proof root
5. Explicit review and merge
6. Follow-up receipt binding the final commit hash

Graph execution and validation never shortcut this path.

## Relationship to signal-core

`signal-core/core.py` already provides:

- canonical JSON encoding
- deterministic claim / dependency sorting
- graph hashing
- artifact-to-graph receipt binding
- rejection unless graph authority equals NONE

V0.1 extends this surface conceptually (not yet in code) to:

- general workflow DAGs (not only claim graphs)
- checker nodes
- typed edges beyond pure dependency
- static diamond and failure-policy validation
- per-node and per-edge execution receipts

Implementation of those extensions is out of scope for this design document.

## Gaps Closed by This Model

- Common node schema across amendment, collaboration, claim, workflow, and relationship graphs.
- Shared edge semantics with explicit must-not-imply rules.
- Formal fake-edge / cross-boundary prohibition.
- Static DAG validator requirements (cycles, missing deps, unreachable nodes, invalid convergence).
- Checker-node contract.
- Distinction among data, verification, authority, and ordering edges.
- Execution receipts per node (and optionally edge).
- Declared fan-out / fan-in and partial-failure policy.

## Non-Goals (V0.1)

- Replacing any existing graph document or schema.
- Populating the currently empty amendment graph state.
- Implementing a runtime engine.
- Claiming global legitimacy, mainnet anchoring, or elevated authority.
- Introducing secrets or live signing material into the repository.

## Recommended Follow-On Work (Tracking Issue Decomposition)

1. **Schemas** — formal JSON Schema for node, edge, graph, and execution receipt under this model.
2. **Validator** — static DAG + semantic checker (cycles, missing deps, convergence, authority:false invariant).
3. **Fixtures** — minimal valid and invalid graphs (including diamond and checker cases).
4. **Explorer** — read-only surface that renders a graph under this model without asserting truth or authority.
5. **signal-core extension** — optional, after schemas and fixtures stabilize.
6. **Amendment graph population** — separate lane; this model does not require it.

## Binding Note

This design document is a repository artifact. It becomes stronger only when
bound to a commit hash, branch, PR, and follow-up receipt. Until then it remains
operational design only.

```text
No receipt, no authority.
No replay, no promotion.
No secret in repo.
No fake green.
```
