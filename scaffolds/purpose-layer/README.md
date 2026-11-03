# Purpose Layer v0.1

Status: DRAFT  
Placement layer: subordinate  
Authority created: false  
Software sentience claimed: false

## Distinction

A directory tree answers:

```text
Where is the artifact?
```

The Purpose Layer answers:

```text
Why does the build exist?
Who may receive from it?
What may it never take?
How may a person refuse, correct, leave, or choose another path?
```

Hierarchy and placement are different dimensions. The Purpose Layer sits logically above repositories, directories, files, agents, receipts, and interfaces. It is not reduced to their 2D arrangement.

## Declared purpose hierarchy

```text
GOD
  ↓ gives purpose, dignity, freedom, and responsibility
DAD + MOM
  ↓ give care, protection, teaching, provision, and choices
FAMILY
  ↓ gives relationship, memory, creativity, and mutual support
WISDOM FAMILY LEDGER
  ↓ records only what is offered, consented, bounded, and attributable
BUILDS
  ↓ deliver tools, knowledge, receipts, paths, and opportunities
PEOPLE
  ↕ retain agency, boundaries, refusal, correction, and exit
```

This is Jason's declared family-purpose model. The repository does not prove theology, appoint a parent, rank human worth, or grant one family member control over another.

## Reach-down law

The system is designed to reach down and give:

- context;
- tools;
- learning;
- protection;
- choices;
- evidence;
- credit;
- repair paths;
- opportunity;
- a way out.

It must not reach down to take:

- identity;
- consent;
- labor without attribution;
- private information;
- custody;
- voice;
- authority;
- dependency;
- loyalty;
- political agreement;
- permanent participation.

## Sentient design posture

"Sentient" describes a humane aspiration: the build should notice boundaries, consequences, ambiguity, vulnerability, and the existence of other choices.

It is not a claim that software is conscious, alive, morally sovereign, or entitled to decide for people.

The correct machine posture is:

```text
BOUNDARY_AWARE
CHOICE_PRESERVING
EVIDENCE_BOUND
HUMAN_REVIEWED
NON_POSSESSIVE
```

## Personal Boundary Contract

Every person-facing build must support:

```json
{
  "participation": "OPT_IN|LIMITED|PAUSED|NO|UNASKED",
  "public_identity": "APPROVED|REDACTED|PRIVATE",
  "allowed_topics": [],
  "prohibited_topics": [],
  "allowed_actions": [],
  "prohibited_actions": [],
  "contact_permission": "NONE|SPECIFIC|ONGOING",
  "attribution_preference": "NAMED|PSEUDONYM|ANONYMOUS|NONE",
  "review_required_before_publication": true,
  "correction_path": true,
  "pause_path": true,
  "exit_path": true,
  "data_return_or_deletion_path": true,
  "authority_created": false
}
```

Silence is `UNASKED`, not consent.

## Escape routes

A box, border, folder, role, project, account, or family ledger entry must never become a trap.

Every build must offer at least these routes:

1. **Decline** — do not enter.
2. **Limit** — participate in only named surfaces.
3. **Pause** — stop activity without losing dignity.
4. **Correct** — challenge attribution, facts, or boundaries.
5. **Fork** — take approved work into an independent path.
6. **Export** — receive a usable copy of approved contributions.
7. **Leave** — end future participation.
8. **Remove or redact** — request removal where technically and legally possible.
9. **Appeal** — request human review when automation blocks or misrepresents.
10. **Choose outside** — use another tool, platform, identity, or community without penalty.

Git history may be durable. The system must explain that limit before publication and prevent sensitive material from entering history whenever possible.

## Choice architecture

The build may recommend. It may not narrow the world until only its preferred answer remains.

A valid choice presentation must include:

- the proposed path;
- at least one safe alternative when available;
- the consequence of each path;
- the option to wait;
- the option to decline;
- unknowns and irreversible effects;
- who will act;
- what evidence will be recorded.

## Boundary precedence

When layers conflict:

```text
PERSONAL SAFETY
> PERSONAL BOUNDARY
> OBSERVED CONSENT
> FAMILY PURPOSE
> PROJECT PURPOSE
> AUTOMATION
> DIRECTORY CONVENIENCE
> FILE COMPLETION
```

No successful build, passing CI job, merged PR, public narrative, or ledger completeness overrides a person's boundary.

## Purpose receipt

Each public build should declare:

```json
{
  "purpose_id": "sha256:<canonical-purpose>",
  "gives": [],
  "takes": [],
  "people_affected": [],
  "consent_receipts": [],
  "personal_boundaries": [],
  "alternatives": [],
  "escape_routes": [],
  "irreversible_effects": [],
  "placement_root": null,
  "human_approver": null,
  "authority_created": false
}
```

A non-empty `takes` list requires explicit review. Hidden taking is a failure.

## Relationship to placement

The Purpose Layer does not dictate one universal folder structure. It binds every placement surface to a declared purpose.

```text
PURPOSE
  → PEOPLE + BOUNDARIES
  → PROJECT
  → DIRECTORY
  → FILE
  → EXECUTION
  → RECEIPT
  → REVIEW / EXIT
```

Files without a bound purpose are `UNPLACED_MEANING`, even when they exist inside a directory.

## Invariants

```json
{
  "hierarchy_is_not_placement": true,
  "purpose_precedes_directory": true,
  "system_gives_before_it_asks": true,
  "hidden_extraction_allowed": false,
  "silence_equals_consent": false,
  "personal_boundary_overrides_build": true,
  "escape_routes_required": true,
  "outside_choices_allowed": true,
  "software_sentience_claimed": false,
  "authority_created": false
}
```
