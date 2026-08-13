# jaywisdom.base.eth — Mr. Wisdom Resume + Mrs. Wisdom Reputation

```text
STATUS                = DESIGN_SCAFFOLD
DIRECTORIES_FIRST     = TRUE
ONCHAIN_WRITE         = FALSE
RESUME_BYTES_MUTATED  = FALSE
AUTHORITY_CREATED     = FALSE
NO_FAKE_GREEN         = TRUE
```

This directory is the human-readable documentation root for the public `jaywisdom.base.eth` resume and reputation architecture.

The existing resume artifact remains at:

`credentials/jay-wisdom/resume.json`

The existing resume manifest remains at:

`credentials/jay-wisdom/resume.manifest.json`

This documentation does **not** modify those bytes, does not create a new resume hash, does not create an attestation, and does not create authority.

## Directory map

```text
docs/jaywisdom.base.eth/
├── README.md
├── reputation/
│   ├── README.md
│   └── mrs-wisdom/
│       └── README.md
└── institutions/
    └── README.md
```

## The blend

```text
MR. WISDOM RESUME
    = the claim object

MRS. WISDOM
    = the reputational membrane

INSTITUTIONS
    = scoped evidence / verification / witness nodes

ENS
    = discovery

EAS / CHAIN
    = witness / shared memory when separately authorized
```

### Behind the resume

Preserve sources, receipts, conflicts, chronology, and provenance.

### Within the resume

Keep claims explicit, bounded, and typed. A claim may be user-attested, document-verified, third-party-verified, conflicted, unverified, inferred, or held.

### Around the resume

Allow institutions and people to contribute bounded reputation edges without rewriting the resume core or silently upgrading a claim.

## Constitutional invariant

```text
REPUTATION        != TRUTH
ENDORSEMENT       != AUTHORITY
IDENTITY          != AUTHORIZATION
INSTITUTION       != INFALLIBILITY
RECEIPT QUALITY   != CLAIM SUPPORT
POPULARITY        != VERIFICATION
```

A good reputation layer does not make Mr. Wisdom look good by force. It makes the record **legible, attributable, correctable, and replayable**.

## Public-root principle

`jaywisdom.base.eth` may serve as the public discovery and control-facing name for this architecture, but the name itself does not grant authority.

```text
ENS_DISCOVERY      = TRUE
ENS_AUTHORITY      = FALSE
```

## Scaling rule

Scale by adding independent, scoped institutional edges around claims rather than by increasing one global score.

```text
ONE RESUME
MANY CLAIMS
MANY SOURCES
MANY INSTITUTIONS
MANY RECEIPTS
NO AUTOMATIC THRONE
```
