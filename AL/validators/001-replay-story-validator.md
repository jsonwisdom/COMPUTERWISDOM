# 001 — Replay Story Validator

**Memory type:** procedural  
**Validator type:** narrative admissibility  
**Authority:** false

The Replay Story Validator determines whether a replay story object is procedurally admissible.

It does not decide whether a story is true.
It does not interpret meaning.
It does not resolve disputes.
It does not generate authority.

It returns only a procedural verdict.

## Inputs

- replay story object
- replay story schema
- referenced receipt, when required
- replay result, when required

## Outputs

```json
{
  "authority": false,
  "verdict": "admissible | expression_only | invalid",
  "reason": "string"
}
```

## Validation Pipeline

1. Load replay story object.
2. Validate object shape against Replay Story Schema v0.1.
3. Read `story_type`.
4. If `story_type` is `expression`, return `expression_only` unless the object falsely claims admissibility.
5. If `story_type` is `narrative`, require `receipt_id`.
6. If `receipt_id` is missing, return `invalid`.
7. Load referenced receipt.
8. Invoke deterministic reconstruction.
9. Invoke receipt verification.
10. If replay passes, return `admissible`.
11. If replay fails, return `invalid`.

## Pseudocode

```text
function validateReplayStory(story):
  assert authority == false

  if schema_invalid(story):
    return invalid("schema_invalid")

  if story.story_type == "expression":
    if story.admissibility.claims_admissible == true:
      return invalid("expression_claims_admissibility")
    return expression_only("receipt_not_required")

  if story.story_type == "narrative":
    if missing(story.receipt_id):
      return invalid("missing_receipt")

    replay_result = reconstruct(story.receipt_id)

    if replay_result != "single_transition":
      return invalid("replay_failed")

    verification = verify_receipt(story.receipt_id)

    if verification == "valid":
      return admissible("receipt_replayed")

    return invalid("verification_failed")

  return invalid("unknown_story_type")
```

## Verdict Meanings

| Verdict | Meaning |
|---|---|
| `admissible` | Narrative is receipt-bound and replay-valid. |
| `expression_only` | Story may exist as expression but is not procedurally admissible. |
| `invalid` | Object fails schema, receipt, replay, or admissibility constraints. |

## Invariants

- Expression may exist without receipt.
- Narrative requires receipt.
- Receipt requires replay.
- Replay requires deterministic reconstruction.
- Validator returns procedure, not truth.
- Authority remains false.

## Operating Line

Validate shape.
Require receipt.
Replay transition.
Return verdict.
Do not interpret meaning.
