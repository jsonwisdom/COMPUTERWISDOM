# Jason Wisdom Public Family Plan v0.1

Status: DRAFT_FOR_FAMILY_REVIEW  
Steward: Jason Wisdom  
Authority created: false  
Public by default: no

## Mission

Build a public, family-centered record of creative, technical, and civic work while preserving each person's dignity, consent, safety, privacy, attribution, and right to correct or leave the record.

The family plan is not permission to publish the family.

## Five lanes

### 1. People

Each participant receives an individual, consent-bound record.

Required fields:

- chosen public name
- adult or minor classification
- relationship context
- participation choice: `YES|NO|LIMITED|UNASKED`
- approved subjects
- prohibited subjects
- approved attribution
- correction/removal method
- review date

Women are recorded individually. No person is collapsed into "the women," "the family," a project asset, or Jason's authority.

### 2. Projects

Every public project receives:

```text
projects/<project-id>/
  README.md
  people/
  purpose/
  chronology/
  artifacts/
  receipts/
  public/
  private-index/
  gaps/
```

The public tree contains approved material. `private-index/` contains references and hashes only; private source material remains in an access-controlled system outside public GitHub.

### 3. Instructions and history

Preserve:

- exact timestamp and timezone;
- exact operator ask;
- Jason role or roles invoked;
- people and projects named;
- response actually given;
- execution receipt;
- missing or disregarded requirements;
- later correction or approved backfill.

Backfill adds a correction record. It never pretends the repair occurred at the original time.

### 4. Publication gate

Nothing becomes public unless every applicable gate passes:

```text
SOURCE_BOUND
PERSON_IDENTIFIED_CORRECTLY
CONSENT_OBSERVED
MINOR_SAFETY_PASS
PRIVATE_DATA_REMOVED
SECRETS_SCAN_PASS
CLAIMS_SUPPORTED
HUMAN_PREVIEW_APPROVED
```

A missing gate produces `HOLD`.

### 5. Review and exit

Any represented person may request:

- correction;
- reduced attribution;
- removal from future publications;
- archival of approved contributions;
- separation of their identity from a project.

Git history may retain earlier public commits. Therefore sensitive material must be blocked before commit, not merely deleted later.

## Adult participation options

| Level | Public content |
|---|---|
| Private | No identity or contribution published |
| Named only | Approved name and bounded relationship |
| Contributor | Approved name, contribution, and attribution |
| Public builder | Approved bio, projects, and public contact lane |
| Case-specific | Separate approval for each publication |

Consent is specific and revocable for future use. Jason cannot grant another adult's consent.

## Children and minors

- No public account, identity, image, voice, location, school, schedule, private chat, or personal record by default.
- Use an adult-managed private workspace for learning artifacts.
- Publish only separately approved, minimized outputs.
- Never store a minor's raw ChatGPT conversation in public GitHub.
- ChatGPT is not intended for children under 13; ages 13–18 require parental consent under OpenAI's published guidance.
- Parental consent does not erase the child's dignity, privacy, or ability to object.

## AI use

AI may:

- organize approved information;
- draft code and documents;
- identify missing receipts;
- propose directory placement;
- compare execution against exact asks.

AI may not:

- invent family consent;
- infer private relationships as facts;
- contact or impersonate family members;
- publish or merge without approval;
- convert political framing into allegations;
- claim family authority.

## Microsoft/GitHub controls

Before public-family publication:

- enable available secret scanning and push protection;
- require pull requests for public changes;
- use least-privilege repository access;
- separate public and private repositories;
- review dependency and code-scanning alerts;
- treat repository history as durable public disclosure.

Microsoft guidance notes that repository scanning can find secrets in historical commits while push protection evaluates new pushes. Both prevention and historical review are required.

## OpenAI/ChatGPT controls

- Keep family work in purpose-specific projects or workspaces.
- Limit invitations and remove access when no longer required.
- Review sharing and data controls before importing private material.
- Use structured records and source identifiers instead of copying whole conversations.
- Treat model output as proposed labor requiring human review.
- Do not use memory as the sole historical receipt.

`learn.openai.com` currently redirects to `learn.chatgpt.com`, which documents projects/chats, permissions, record and replay, security, governance, and related controls.

## Political research lane

Family-centered civic research may examine Trump, any administration, public official, institution, company, or public claim.

Required boundary:

```text
PUBLIC EVIDENCE
+ ATTRIBUTED CLAIM
+ TIMESTAMP
+ CORRECTION PATH
!= FAMILY ENDORSEMENT
```

No family member is represented as joining a political position without their explicit approval.

## First 30-day rollout

### Week 1 — Inventory

- Choose one pilot project.
- List people named in it without publishing new personal data.
- Inventory existing public files and sensitive risks.
- Enable or verify security controls.

### Week 2 — Consent and placement

- Create one private consent worksheet per person.
- Classify every candidate artifact as `PUBLIC|PRIVATE|REDACT|HOLD`.
- Build project directories before moving files.

### Week 3 — Backtrack

- Review one bounded conversation window.
- Record exact asks and execution receipts.
- Classify `ACCEPTED|PARTIAL|DISREGARDED|CONTRADICTED|UNVERIFIED`.
- Propose backfills; do not apply them automatically.

### Week 4 — Publish one safe packet

- Publish one family-approved project manifest.
- Include purpose, contributors, chronology, evidence, gaps, and correction method.
- Run secrets/privacy review.
- Obtain human preview approval.
- Emit a publication receipt.

## Success condition

```json
{
  "family_members_included_by_choice": true,
  "women_recorded_individually": true,
  "minor_data_public_by_default": false,
  "directories_declared_first": true,
  "exact_asks_replayable": true,
  "backfills_separate_from_history": true,
  "secret_scan_required": true,
  "human_publication_approval": true,
  "authority_created": false
}
```
