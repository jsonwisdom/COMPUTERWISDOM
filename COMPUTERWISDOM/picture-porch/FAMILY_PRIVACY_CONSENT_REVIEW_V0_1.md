# Picture Porch V0.1 — Family, Privacy & Consent Review

**Classification:** Independent adult/family review packet; **NOT approval**, legal certification, consent receipt, deployment authorization, or testimony about any child.

**Scope:** Only `COMPUTERWISDOM/picture-porch/index.html` on draft PR #645. Keep JOY's existing page untouched. This document contains no child names, prompts, pictures, or family records.

## Decision boundary

```text
TECHNICAL_STATIC_REVIEW = PERFORMED
ADULT_FAMILY_REVIEW = PENDING
CHILD_CONSENT = NOT_ASSUMED
CHILD_FACING_RELEASE = HOLD
MERGE = HOLD
DEPLOYMENT = HOLD
NO_FAKE_GREEN = ACTIVE
```

## Technical observations — review, not certification

| Area | Observed behavior or design | Unresolved concern / gate |
|---|---|---|
| Drawing | Browser Canvas procedural cartoons; no generative-image service | Not open-ended image generation; acceptable age band and depiction review pending |
| External communication | CSP includes `connect-src 'none'`; no application fetch/XHR, wallet, posting or analytics code identified | Source-level observation, not a live network-security guarantee; embedded browser extensions and hosting context are outside this test |
| Browser data | IndexedDB stores plaintext prompts, generated images or word pictures, creation timestamps, and daily usage | Anyone with access to the same browser profile or local device may access the data; storage is not encrypted or access-controlled |
| Reflection | JOY question displayed; reflection answers intentionally not written to IndexedDB | Confirm with normal-origin test and adult review; user could still screenshot or share |
| Privacy prompting | A partial regex guard detects some phone/address/email and harmful terms | Easily bypassed by formats, names, clues, Unicode, or contextual disclosures; no comprehensive safety filter |
| Downloads | PNG and TXT files are created on demand on-device | Files can be shared outside the app; adult review of download expectations required |
| Daily limit | Eight saved paintings per local-calendar day, counted in IndexedDB transaction; word pictures exempt | Device clock, profile switching, or clearing storage bypasses limit. This is a convenience limit, **not** a child-access security control |
| Content appropriateness | Limited word guard; no human moderator, age verification, or parental gate in app | Inappropriate concepts and personal details may still be entered; adult supervision necessary |
| Public source | GitHub contains implementation and synthetic tests, not child-produced content | Any future telemetry, real test fixture, screenshot, or receipt must exclude child data |
| Consent | No verified parental consent, family approval, or age suitability decision supplied | **RELEASE BLOCKER** |

## Independent adult/family reviewer checklist — unchecked

- [ ] Identify intended child age band, supervising adult and intended *private* use context without publishing child identity.
- [ ] Confirm parental/guardian authorization for the actual children who may use it; do not publish consent details in GitHub.
- [ ] Confirm instructions are understandable to the intended age group and do not invite entering real names, school, addresses, personal contacts or secrets.
- [ ] Assess whether the incomplete regex guard is acceptable **with adult supervision**; document any required stronger controls before children use the app.
- [ ] Decide data retention/erasure procedures for prompts, PNGs, TXT downloads and browser Shelf; test deletion and explain browser-profile sharing.
- [ ] Check local storage persistence, privacy mode, browser profile, sync/backup and accessible-device consequences; do not claim data encryption.
- [ ] Confirm accessibility (keyboard-only operation, screen readers, contrast, and motor/vision accommodation) for the chosen age band.
- [ ] Verify normal-origin testing with synthetic prompts only: Shelf persistence, eight cap, two-tab race (starting at seven), PNG/TXT bytes and no external network.
- [ ] Check whether allowing downloads is suitable or should require adult supervision; downloads may leave the private porch.
- [ ] Record independent adult review decision as **APPROVED**, **CHANGES_REQUIRED**, or **DECLINED** outside public child records.
- [ ] Have Jason separately assess receipts, outstanding risks, and give or withhold final human release authorization.

## Browser evidence requirements

Record: repository, exact Git commit, HTML Git blob and separate SHA-256 byte digest, test-file blob, date/time with timezone, OS/browser/Playwright versions, commands, exit status, actual stdout/stderr, screenshots with **synthetic art only**, and reviewer's scope. A failed or blocked run is `HOLD`, never `PASS`. A passing browser suite does **not** convert family approval into true.

**Critical concurrency proof:** Begin with seven persisted paintings in one browser context, open two tabs before the eighth slot is used, issue two near-simultaneous requests, and assert exactly **one** stored success, **one** denied attempt, final usage count **eight**, and **eight paintings plus any prior word pictures** after reloading both tabs. This validates a real two-tab attempt, not two post-cap disabled buttons.

## Final review disposition

```text
STATIC_REVIEW_PACKET: PREPARED
INDEPENDENT_ADULT_DECISION: NOT_RECEIVED
PR_STATE_REQUIRED: DRAFT
APPLICATION_CHANGE_THIS_REVIEW: FALSE
FAMILY_CONSENT_PROVEN: FALSE
PUBLIC_RELEASE_AUTHORIZED: FALSE
```

**Rule:** COMPUTERWISDOM may prepare evidence. JOY may provide learning prompts. Only appropriate adult consent and Jason's separate release decision can authorize child-facing use. Repository CI and mathematical modeling are not substitutes.
