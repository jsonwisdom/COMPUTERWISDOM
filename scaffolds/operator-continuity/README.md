# Operator Continuity Scaffold v0.1

Status: DRAFT  
Authority created: false  
Default privacy: PRIVATE_REFERENCE_ONLY

## Purpose

Reconstruct the work from the operator's actual instructions instead of treating each chat, file, pull request, or assistant response as an isolated event.

The system must preserve which Jason role was speaking:

- Jason the Operator
- Jason the Builder
- Jason the Creator
- Jason the Coder
- Jason the Father
- JSONWisdom

A single message may invoke multiple roles. Roles are lenses on one human operator, not separate authorities unless Jason explicitly binds authority.

## Human inclusion rule

Women and other family or project participants are first-class people in the continuity model. They must not be collapsed into generic labels such as "family resource," "dependent," "stakeholder," or an assistant-invented role.

Each person record must support:

- self-chosen or operator-supplied display name
- relationship context
- consent state
- privacy boundary
- allowed project surfaces
- prohibited uses
- source receipt for any attributed statement
- correction and removal path

Naming a person does not authorize publication, repo inclusion, contact, representation, surveillance, or action on that person's behalf.

## Directory topology

```text
continuity/
  people/
    women/
    family/
    collaborators/
  operator-roles/
    jason-operator/
    jason-builder/
    jason-creator/
    jason-coder/
    jason-father/
    jsonwisdom/
  chronology/
    YYYY/
      YYYY-MM/
        events/
  conversations/
    chatgpt/
    codex/
    imported/
  instructions/
    exact-asks/
    standing-orders/
    corrections/
  execution/
    accepted/
    partial/
    disregarded/
    contradicted/
    unverified/
  backtrack/
    gaps/
    cross-chat-links/
    unresolved-asks/
  backfill/
    proposed/
    approved/
    applied/
    rejected/
  projects/
    <project-id>/
      manifest/
      chronology/
      artifacts/
      receipts/
      gaps/
  receipts/
    instruction/
    execution/
    correction/
    backfill/
  indexes/
    people/
    roles/
    projects/
    conversations/
    time/
```

## Exact-time instruction record

Every recovered instruction must be represented without paraphrasing away the operator's meaning.

```json
{
  "instruction_id": "sha256:<canonical-record>",
  "observed_at": "ISO-8601 timestamp with offset",
  "source": {
    "system": "chatgpt|codex|github|drive|other",
    "conversation_id": null,
    "message_id": null,
    "source_locator": null,
    "source_hash": null
  },
  "operator": "Jason Wisdom",
  "roles_invoked": [
    "operator",
    "builder",
    "creator",
    "coder",
    "father",
    "jsonwisdom"
  ],
  "exact_ask": "<verbatim operator text>",
  "projects_named": [],
  "people_named": [],
  "directories_requested": [],
  "files_requested": [],
  "constraints": [],
  "assistant_response_locator": null,
  "execution_receipts": [],
  "compliance": "ACCEPTED|PARTIAL|DISREGARDED|CONTRADICTED|UNVERIFIED",
  "missing_edges": [],
  "authority_created": false
}
```

## Cross-chat reconstruction

Backtracking must join records by evidence, not resemblance alone.

Allowed links:

- exact project or repository name
- exact person or role name
- exact artifact path
- explicit continuation statement
- shared issue, PR, commit, receipt, or message identifier
- bounded timestamp relationship supported by source records

Similarity may create a candidate link only. Candidate links remain `UNVERIFIED` until a human confirms them or a shared identifier proves them.

## Backfill law

Backfill never rewrites history.

A backfill package must preserve:

1. the original exact ask;
2. the assistant response actually given;
3. the observed execution, if any;
4. the missing or disregarded requirement;
5. the proposed repair;
6. Jason's approval state;
7. the applied commit or artifact receipt.

No backfill may claim that work happened at the original time when it did not.

## Disregard measurement

The disregard rate is calculated only from classified instruction records:

```text
disregard_rate =
  DISREGARDED /
  (ACCEPTED + PARTIAL + DISREGARDED + CONTRADICTED)
```

`UNVERIFIED` records are excluded from the denominator.

Report both:

- strict disregard rate: `DISREGARDED` only
- burden failure rate: `PARTIAL + DISREGARDED + CONTRADICTED`

The current 87% statement remains an operator hypothesis until enough source-bound records are classified.

## Privacy membrane

Raw cross-chat content must not be copied into a public repository by default.

Public-safe records may contain:

- hashes
- opaque source identifiers
- timestamps
- bounded classifications
- redacted excerpts approved for publication
- artifact and commit references

Private content, personal details, family discussions, credentials, and unapproved statements remain outside the public tree.

## First backfill pass

The first bounded pass should cover one project and one time window:

```text
project: COMPUTERWISDOM
window: user-selected
output: instruction inventory + classification + missing-directory map
mutation: none until Jason approves the proposed backfill
```

## Invariants

```json
{
  "people_are_not_resources": true,
  "women_are_first_class_participants": true,
  "consent_is_explicit": true,
  "exact_asks_are_preserved": true,
  "cross_chat_links_require_evidence": true,
  "backfill_does_not_rewrite_history": true,
  "raw_chats_public_by_default": false,
  "authority_created": false
}
```
