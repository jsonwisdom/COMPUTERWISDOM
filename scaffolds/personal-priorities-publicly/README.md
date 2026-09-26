# PersonalPrioritiesPublicly v0.1

Status: DRAFT  
Steward: Jason Wisdom  
Authority created: false

## Purpose

Help Jason state personal priorities publicly without surrendering privacy, family boundaries, choice, correction rights, or control of the underlying evidence.

Public priority is not public ownership of the person.

## Burden-of-proof allocation

The burden belongs to the actor making or transforming the claim.

| Event | Burden holder | Required proof |
|---|---|---|
| Jason states his priority | Jason, for accurate self-expression | Jason's approved statement |
| System paraphrases Jason | System | Exact source, timestamp, faithful comparison |
| System assigns a priority to another person | System; publication remains HOLD | That person's explicit approval |
| AI claims it followed an instruction | AI execution layer | Artifact, commit, receipt, and constraint readback |
| AI claims it could not comply | AI execution layer | Exact blocker and attempted bounded action |
| Repository publishes family material | Publisher/maintainer | Consent, privacy review, source, approval receipt |
| Public factual or political claim | Claimant | Primary sources and bounded wording |
| Person states a boundary | No justification burden | Boundary itself is sufficient |
| System overrides or limits a boundary | System/operator proposing override | Explicit authority, necessity, scope, review, and appeal |
| System claims deletion or removal | System | Verifiable deletion/readback plus disclosed durability limits |

A person does not have to prove why they deserve privacy, refusal, pause, correction, or exit.

## Priority record

```json
{
  "priority_id": "sha256:<canonical-priority>",
  "person": "Jason Wisdom",
  "statement": "<Jason-approved public wording>",
  "source_timestamp": "ISO-8601 with offset",
  "scope": [],
  "importance": "NOW|NEXT|LATER|PARKED",
  "public_detail": "TITLE_ONLY|SUMMARY|FULL_APPROVED_TEXT",
  "private_evidence_locator": null,
  "people_mentioned": [],
  "other_people_approved": false,
  "allowed_actions": [],
  "prohibited_actions": [],
  "review_on": null,
  "pause": true,
  "correct": true,
  "withdraw_future_use": true,
  "authority_created": false
}
```

## Public priority board

Only Jason-approved fields appear publicly:

```text
NOW
  What deserves attention now

NEXT
  What begins after the current gate

LATER
  Valid work without present urgency

PARKED
  Preserved without implied commitment

BOUNDARIES
  What the system must not do

HELP WANTED
  Specific contribution Jason invites

HOLD
  Missing proof, consent, authority, or capacity
```

Private reasons and evidence do not need to be public for a priority to be valid.

## Sentient burden posture

"Sentient" means the design knows where proof is owed before it acts. It does not mean software consciousness.

```text
CLAIMANT OWNS CLAIM BURDEN
TRANSFORMER OWNS FIDELITY BURDEN
EXECUTOR OWNS EXECUTION BURDEN
PUBLISHER OWNS PUBLICATION BURDEN
SYSTEM OWNS SAFETY AND READBACK BURDEN
PERSON OWNS THEIR CHOICE — NOT A DEFENSE OF THEIR DIGNITY
```

Missing proof produces `HOLD`, never a transfer of burden onto the person affected.

## Learning path

### Microsoft Learn

1. **Introduction to AI Literacy** — verification, privacy, transparency, human accountability, and communication with families.
2. **What is Responsible AI** — fairness, reliability and safety, privacy and security, inclusiveness, transparency, and accountability.
3. **Responsible AI for agent design** — disclose the agent's purpose, role, limitations, and risks so people can make informed choices.
4. **Responsible AI policies** — turn principles into enforceable workflow controls.
5. **Secret scanning and push protection** — prevent public priority artifacts from leaking credentials or private material.

### OpenAI Learn / ChatGPT Learn

`learn.openai.com` redirects to `learn.chatgpt.com`.

Study:

1. **Projects and chats** — separate priorities by purpose and context.
2. **Permissions** — bind who and what an agent may access or change.
3. **Record & Replay** — preserve execution evidence rather than trusting narrative.
4. **Projects in ChatGPT** — control membership and sharing.
5. **Shared links and Data Controls** — review audience and content; personal-account links may be viewable by anyone holding the link.
6. **Apps and connectors** — review permissions and third-party data terms before connecting private sources.
7. **Work chief of staff** — organize priorities and commitments while keeping final judgment with Jason.

## Publication workflow

```text
JASON STATES
→ SYSTEM QUOTES
→ JASON CORRECTS
→ PEOPLE/PRIVACY CHECK
→ EVIDENCE BOUND
→ PUBLIC PREVIEW
→ JASON APPROVES
→ PUBLISH
→ READBACK
→ CORRECTION / PAUSE / EXIT REMAINS AVAILABLE
```

No automatic publication follows from a chat statement.

## Invariants

```json
{
  "priority_owner_is_person": true,
  "system_owns_transformation_burden": true,
  "executor_owns_execution_burden": true,
  "publisher_owns_publication_burden": true,
  "boundary_requires_justification": false,
  "silence_is_consent": false,
  "missing_proof_transfers_burden": false,
  "public_priority_requires_public_private_lanes": true,
  "software_sentience_claimed": false,
  "authority_created": false
}
```
