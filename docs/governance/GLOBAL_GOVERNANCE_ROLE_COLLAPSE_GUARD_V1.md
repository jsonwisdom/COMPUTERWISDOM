# GLOBAL_GOVERNANCE_ROLE_COLLAPSE_GUARD_V1

Status: ACTIVE CONTROL-PLANE GUARD  
Scope: Global governance identity claims  
Boundary: `CANDIDATE_NOMINEE_SUCCESSOR_ELECT_NOT_CURRENT_OFFICE_HOLDER`

## Purpose

This guard prevents temporal governance role-collapse across jurisdictions.

The failure class is global:

```text
CURRENT_OFFICE_HOLDER != CANDIDATE != NOMINEE != SUCCESSOR_ELECT
```

No operator is blamed for schema drift. The control plane must reject role ambiguity structurally.

## Required Fields

Every governance identity claim must include:

```text
jurisdiction
office
person
role_status
as_of
sources
boundary
```

## Allowed Role Status Values

```text
CURRENT_OFFICE_HOLDER
CANDIDATE
NOMINEE
SUCCESSOR_ELECT
FORMER_OFFICE_HOLDER
UNKNOWN
```

## Forbidden Promotions

The guard rejects any claim or mission that promotes:

```text
candidate -> current officeholder
nominee -> current officeholder
likely successor -> current officeholder
successor-elect -> current officeholder before assumption of office
former officeholder -> current officeholder without current source
```

## State-Agnostic Rule

This guard is not Alabama-specific.

It applies to:

- all 50 U.S. states
- federal offices
- counties
- municipalities
- agencies
- courts
- boards
- commissions
- foreign jurisdictions when modeled

## Control-Plane Position

```text
COMPUTERWISDOM contextualizes.
AL admits.
Replay seals.
```

GitHub pointers are not truth. Search snippets are not officeholder status. Election trajectory is not executive authority.

## Minimum Claim Form

```json
{
  "anchor_id": "GLOBAL_GOVERNANCE_ROLE_ANCHOR_V1",
  "as_of": "2026-05-27",
  "jurisdiction": "Alabama",
  "office": "Governor",
  "person": "Kay Ivey",
  "role_status": "CURRENT_OFFICE_HOLDER",
  "sources": ["https://example.gov/source"],
  "boundary": "CANDIDATE_NOMINEE_SUCCESSOR_ELECT_NOT_CURRENT_OFFICE_HOLDER"
}
```

## Core Invariant

```text
No governance identity claim without time, office, role, jurisdiction, and source.
```
