# COMPUTERWISDOM FAMILY SECURE CORRIDOR V0.1

**Repo:** `jsonwisdom/COMPUTERWISDOM`  
**Branch:** `master`  
**Authority:** false  
**Mode:** WATCHER_FIRST / REVIEW_BEFORE_PROMOTION  
**Purpose:** Define a public-safe corridor for family continuity coordination without private data, ownership claims, rendering claims, or merge claims.

---

## 1. Corridor Boundary

This corridor exists to coordinate family-continuity documentation across COMPUTERWISDOM, AL, JOY, and confirmed family repo surfaces.

It does **not** grant authority over any person, family member, wallet, repo, identity, or future action.

```json
{
  "corridor": "COMPUTERWISDOM_FAMILY_SECURE_CORRIDOR_V0_1",
  "authority": false,
  "watcher_only_default": true,
  "family_authority_claims": false,
  "private_data_allowed": false,
  "rendering_allowed": false,
  "merge_claims_allowed": false,
  "promotion_requires_review": true
}
```

---

## 2. Allowed Corridor Inputs

Allowed:

- Public-safe repo paths
- Public-safe role descriptions
- Audit status labels
- Receipt pointers
- Review chamber notes
- Family continuity rules
- Non-sensitive continuity lessons

Not allowed:

- Private addresses
- Birthdates
- API keys, tokens, passwords, or secrets
- Medical, school, legal, or sensitive family records
- Ownership/control language over family members
- Claims that consent exists when consent is blocked, pending, or unwitnessed

---

## 3. Carry-Over Membrane State

```json
{
  "JOY_CONSENT": "BLOCKED_PENDING",
  "AL_COURT": "REVIEW_CHAMBER_NOT_AUTHORITY",
  "COMPUTERWISDOM": "COORDINATION_MEMBRANE",
  "AUTHORITY": false,
  "NO_FAKE_GREEN": true
}
```

---

## 4. Folder Map

```text
docs/
  COMPUTERWISDOM_FAMILY_SECURE_CORRIDOR_V0_1.md

corridors/family-secure-v0-1/
  README.md
  assignments.yml
  receipts/.gitkeep
  reviews/.gitkeep
  manifests/.gitkeep
```

---

## 5. Review Rules

Before any corridor material is promoted:

1. Confirm the source path exists.
2. Confirm `authority:false` is present.
3. Confirm no private data or secrets are included.
4. Confirm family/person language is stewardship-only.
5. Confirm consent state is not upgraded without a witnessed basis.
6. Confirm no workflow, merge, render, or deployment success is claimed without observed evidence.

---

## 6. Assignment Model

Assignments are role-based review duties only.

They are not authority claims.

```json
{
  "operator": "Jay Wisdom / jsonwisdom",
  "review_surface": "AL review chamber",
  "protection_surface": "JOY consent and alert lane",
  "coordination_surface": "COMPUTERWISDOM",
  "authority": false
}
```

---

## 7. Current Status

```json
{
  "status": "SEEDED_FOR_REVIEW",
  "canonical": false,
  "merge_ready": false,
  "render_ready": false,
  "authority": false,
  "next_action": "review scaffold and verify folder/yaml alignment"
}
```

Canon preserved.  
Authority false.  
No fake green.
