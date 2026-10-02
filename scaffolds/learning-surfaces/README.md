# Learning Surfaces Registry v0.1

Status: DRAFT  
Authority created: false

## Proposed surfaces

| Surface | Intended purpose | Current verified status |
|---|---|---|
| `learn.jsonwisdom.com` | Wisdom Family Ledger, PersonalPrioritiesPublicly, purpose layers, replay, boundaries, and family-approved learning | PROPOSED / PUBLIC RESOLUTION UNVERIFIED |
| `learn.justice.com` | Justice-learning concept named by Jason | PROPOSED / PUBLIC RESOLUTION UNVERIFIED |
| `learn.microsoft.com` | External Microsoft learning authority | LIVE / MICROSOFT-CONTROLLED |
| `learn.openai.com` | OpenAI learning entry named by Jason | REDIRECTS TO `learn.chatgpt.com` |
| `justice.gov` | Official U.S. Department of Justice | LIVE / U.S. GOVERNMENT |

## Non-confusion rule

`justice.com` and any subdomain under it must not be represented as the U.S. Department of Justice.

The official federal DOJ domain is:

```text
https://www.justice.gov/
```

A proposed `learn.justice.com` surface requires verified domain control, DNS, content ownership, purpose, privacy terms, and a visible non-government disclaimer before publication.

## Purpose relationship

```text
PURPOSE LAYER
  ├── learn.jsonwisdom.com
  │     └── family-ledger learning and personal priorities
  ├── learn.justice.com
  │     └── independently identified justice-learning surface
  ├── learn.microsoft.com
  │     └── Microsoft technical and responsible-AI learning
  └── learn.openai.com → learn.chatgpt.com
        └── OpenAI and ChatGPT product learning
```

External learning sites may inform a build. They do not own Jason's priorities, the Wisdom Family Ledger, personal boundaries, or publication decisions.

## Admission gates for a new learning hostname

```json
{
  "domain_control_verified": false,
  "dns_verified": false,
  "tls_verified": false,
  "publisher_identified": false,
  "public_purpose_published": false,
  "privacy_policy_published": false,
  "personal_boundary_contract_linked": false,
  "correction_path_published": false,
  "non_government_disclaimer_required": true,
  "content_deployed": false,
  "authority_created": false
}
```

All false or missing gates produce `HOLD`.

## Boundary

A memorable hostname is placement. Trust requires purpose, provenance, control, consent, security, and readback.
