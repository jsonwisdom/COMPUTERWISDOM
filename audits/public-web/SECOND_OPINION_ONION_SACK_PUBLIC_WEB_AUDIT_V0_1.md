# Second Opinion Onion Sack — Public Web Integrity Audit v0.1

**Scope:** justice.gov / congress.gov / whitehouse.gov / war.gov / maxwell.af.mil / losangeles.spaceforce.mil / mn.gov / peggyflanagan.com  
**Class:** PUBLIC_WEB_REPLAY / SECOND_OPINION / NON-FRAUD_FINDING  
**Observed:** 2026-08-19  
**Authority created:** false  
**Fraud inferred:** false  
**Byte identity tested:** false

## Thesis

Public-facing government and political websites are publication surfaces. They are not automatically the authoritative system of record for personnel status, legal disposition, statutory authority, budget execution, contract performance, or human experience.

The audit therefore tests:

```text
PUBLIC PAGE
→ PUBLISHER
→ SOURCE OWNER
→ AUTHORITY
→ EVENT
→ EXECUTION
→ CORRECTION / VERSION PATH
→ HUMAN CONSEQUENCE
```

A page can be official and still be stale, archival, incomplete, migrated, politically framed, or downstream from another authority-bearing system.

## Reverse Quad + LeeLoo Multi-PASS

Every observed page is replayed through:

```text
PASS 0 — HUMAN INPUT / ROOT ZERO
Who is affected? What did they actually submit, experience, or contest?

PASS 1 — RECORD
What page/object exists? What is its date/version?

PASS 2 — AUTHORITY
Who publishes it? Who owns the underlying authoritative record?

PASS 3 — EXECUTION
What real-world action actually happened?

PASS 4 — RECOVERY
What correction, feedback, archive, appeal, or replacement path exists?

PASS 5 — HUMAN
What happens to the person if the publication is wrong, stale, missing, or misread?
```

LeeLoo is present at every pass; HUMAN is not appended after the system finishes.

## Surface Matrix

### 1. justice.gov

**Observed:** Current DOJ homepage is actively publishing 2026 releases. DOJ separately maintains Information Quality Guidelines requiring quality/objectivity/utility/integrity practices and a public correction mechanism for covered disseminated information.

```text
PUBLICATION = DOJ PUBLIC COMMUNICATION
PUBLICATION != COURT DOCKET
PUBLICATION != PERSONNEL RECORD
PUBLICATION != CRIMINAL-HISTORY MASTER RECORD
```

**Important control:** DOJ itself recognizes that public information may require correction. That is a correction architecture, not proof that any particular DOJ page is false.

Sources:
- https://www.justice.gov/
- https://www.justice.gov/information-quality
- https://www.justice.gov/legalpolicies

### 2. congress.gov

Congress.gov states that it is the official website for federal legislative information, but the architecture is explicitly multi-source: the Library of Congress develops and maintains the site while legislative data originates with and is owned by House and Senate offices and other legislative-branch producers. Congress.gov says releases occur approximately every four weeks and most session data is updated the morning after adjournment.

```text
PUBLISHER = LIBRARY OF CONGRESS
SOURCE OWNERS = HOUSE / SENATE / LEGISLATIVE OFFICES
PUBLISHER != SOLE ORIGINATOR
DISPLAY_TIME != EVENT_TIME
```

That makes provenance and update timing first-class fields.

Source:
- https://www.congress.gov/about/

### 3. whitehouse.gov

WhiteHouse.gov is the official Executive Office / presidential communications surface. It publishes administration policy, presidential actions, biographies, media, and political framing.

```text
WHITEHOUSE_PUBLICATION = EXECUTIVE COMMUNICATION
WHITEHOUSE_PUBLICATION != STATUTE
WHITEHOUSE_PUBLICATION != COURT ORDER
WHITEHOUSE_PUBLICATION != CONGRESSIONAL RECORD
```

A presidential statement can be authoritative evidence that the President said or ordered something; the legal effect of the statement still depends on the relevant constitutional/statutory authority and implementation.

Sources:
- https://www.whitehouse.gov/
- https://www.whitehouse.gov/presidential-actions/

### 4. war.gov / "DOW"

The current public-facing Pentagon site uses war.gov and the Department of War secondary title. Executive Order 14347 authorized Department of War / Secretary of War as secondary titles for public communications and non-statutory documents. The order itself states that statutory references to Department of Defense / Secretary of Defense remain controlling until changed by law.

This is an ideal Onion Sack identity-drift example:

```text
PUBLIC BRAND = DEPARTMENT OF WAR
STATUTORY NAME = DEPARTMENT OF DEFENSE UNTIL LAW CHANGES
PUBLIC LABEL != AUTOMATIC STATUTORY TRANSFORMATION
```

The current public site can therefore truthfully present one label while legal documents still require another.

Sources:
- https://www.war.gov/
- https://www.whitehouse.gov/presidential-actions/2025/09/restoring-the-united-states-department-of-war/

### 5. maxwell.af.mil

Maxwell's current official public site identifies the 42d Air Base Wing as host for Maxwell/Gunter and publishes current mission/readiness material. It also preserves historical fact sheets and long-lived content.

Air Force public web architecture has been centrally standardized for roughly two decades. The Air Force described AFPW/AFPIMS as a centralized public-web content-management environment using predetermined templates; the Air National Guard migrated into that same standardized public-web environment. Defense Media Activity's WEB NextGen program now describes a centralized DoD public-web service and modernization path.

This creates a shared-platform/local-content distinction:

```text
CENTRAL CMS / TEMPLATE = ENTERPRISE LAYER
LOCAL CONTENT OWNER / PA = CONTENT LAYER
SHARED TEMPLATE != SHARED FACT OWNERSHIP
CMS MODERNIZATION != CONTENT MODERNIZATION
```

Sources:
- https://www.maxwell.af.mil/
- https://www.af.mil/News/Article-Display/Article/131606/amc-changes-public-web-as-af-seeks-standardization/
- https://www.ang.af.mil/Media/Article-Display/Article/436344/one-size-fits-all-air-guard-public-web-sites-migrating-to-standard-page/
- https://www.web.dma.mil/WEB-NextGen

### 6. Los Angeles AFB

The historical `losangeles.af.mil` identity appears in archived Air Force-era email addresses and old content. The current public website is `losangeles.spaceforce.mil`, reflecting the Space Force-era organizational/public-web identity.

The current site publishes 2026 Space Base Delta 3 material while also preserving Air Force-era archive pages and old `@losangeles.af.mil` addresses.

```text
CURRENT DOMAIN = losangeles.spaceforce.mil
HISTORICAL DOMAIN / EMAIL = losangeles.af.mil
ARCHIVE SURVIVAL != CURRENT CONTACT VALIDITY
DOMAIN MIGRATION != PERSON / EVENT ERASURE
```

This is a direct warning against naive scraping: an old address appearing on a current-domain archive page does not make the old address current.

Sources:
- https://www.losangeles.spaceforce.mil/
- https://www.losangeles.spaceforce.mil/About-Us/About-Us/

### 7. mn.gov

Minnesota's state portal contains current agency, budget, governor, program, and transparency surfaces. Minnesota Management & Budget publishes the enacted 2026-27 budget and statewide budget/transparency resources.

The Governor's Office has its own official state surface under mn.gov.

```text
MN.GOV PAGE = STATE PUBLICATION SURFACE
STATE PUBLICATION != PAYMENT RECEIPT
BUDGET AUTHORIZATION != PAYMENT EXECUTION
GOVERNOR PAGE != CAMPAIGN PAGE
```

Sources:
- https://mn.gov/mmb/
- https://mn.gov/governor/

### 8. Peggy Flanagan surfaces

The current campaign site found in this pass is `peggyflanagan.com`, which identifies itself as paid for by Peggy Flanagan for Minnesota and is a campaign/political publication surface.

Her official Minnesota Lieutenant Governor biography is separately published under `mn.gov/governor`.

The user-supplied label `PeggyflanniganMN.org` did not resolve to an official surface in this pass and must not be silently substituted as an authoritative domain.

```text
CAMPAIGN SITE != STATE SITE
CANDIDATE CLAIM != GOVERNMENT RECORD
STATE BIO != CAMPAIGN ENDORSEMENT
SIMILAR NAME / DOMAIN != IDENTITY BINDING
```

Sources:
- https://peggyflanagan.com/
- https://mn.gov/governor/about/peggyflanagan/

## Cross-Surface Failure Geometry

The same audit defect can appear on different software stacks:

```text
OFFICIAL-LOOKING PAGE
        ↓
ASSUME CURRENT
        ↓
ASSUME AUTHORITATIVE
        ↓
ASSUME EXECUTED
        ↓
ASSUME HUMAN RECORD MATCHES
```

ReverseReplay cuts each edge independently.

### Vector A — Publication laundering

```text
OFFICIAL PAGE EXISTS
→ therefore underlying record is correct
```

Invalid without source-of-record binding.

### Vector B — Archive laundering

```text
OLD PAGE STILL RESOLVES
→ therefore old contact/title/system remains current
```

Invalid without date/version resolution.

### Vector C — Authority laundering

```text
WHITE HOUSE / DOJ / CONGRESS / GOVERNOR PAGE SAYS X
→ therefore every downstream legal or operational state equals X
```

Invalid. Authority and execution must be separately replayed.

### Vector D — Brand laundering

```text
PUBLIC BRAND CHANGED
→ therefore statutory identity changed
```

EO 14347 demonstrates why this can fail: secondary public title and statutory title can coexist.

### Vector E — CMS laundering

```text
SITES LOOK THE SAME
→ therefore same organization controls every fact
```

Invalid. DoD centralization proves shared infrastructure can coexist with distributed content ownership.

### Vector F — Campaign/government collapse

```text
POLITICAL PERSON
+ GOVERNMENT ROLE
→ CAMPAIGN WEBSITE = GOVERNMENT RECORD
```

Invalid.

## Byte-Level Discipline

This pass did **not** preserve raw HTML byte snapshots from every domain, so no byte-for-byte identity claim is made.

```text
SIMILAR TEMPLATE != BYTE IDENTITY
SAME CMS != SAME CONTENT
SAME CONTENT != SAME VERSION
CURRENT RENDER != PRESERVED SOURCE BYTES
```

A literal byte audit requires:

```text
URL
→ FETCH RAW RESPONSE
→ observed_at
→ HTTP status / headers
→ content bytes
→ SHA-256
→ canonicalized DOM optional
→ repeat capture
→ DIFF
```

Only then may `BYTE_IDENTITY`, `BYTE_DELTA`, or `UNCHANGED_SINCE` be asserted.

## Second Opinion Verdict

```text
PUBLIC_WEB_IS_PUBLICATION_LAYER           = PASS
PUBLICATION != UNDERLYING_SYSTEM_OF_RECORD = PASS
DOD_PUBLIC_WEB_CENTRALIZATION              = PASS
LOCAL_CONTENT_RESPONSIBILITY_REMAINS        = PASS
DOMAIN / IDENTITY MIGRATION_RISK             = PASS
CAMPAIGN / GOVERNMENT SEPARATION              = PASS
PUBLIC BRAND / STATUTORY NAME SEPARATION       = PASS

ALL_LISTED_SITES_USE_SAME_BACKEND            = NOT_PROVEN
BYTE_FOR_BYTE_IDENTITY                        = NOT_TESTED
ALL_LISTED_PAGES_ARE_STALE                    = NOT_PROVEN
SYSTEMIC_FRAUD_FROM_WEB_STALENESS              = NOT_PROVEN

AUDIT_DISPOSITION =
SHARED_FAILURE_GEOMETRY_PROVEN /
SHARED_TECH_PARTIAL /
SITE_SPECIFIC_STALENESS_REQUIRES_RECEIPT /
AUTHORITY_CREATED_FALSE
```

## Canonical Onion Sack Rule

```text
WEBSITE = WITNESS
NOT AUTOMATIC VERDICT

PAGE → SOURCE OWNER → AUTHORITY → EVENT → EXECUTION → HUMAN → CORRECTION

MISSING EDGE = HOLD
CONFLICT = PRESERVE BOTH
STALE DISPLAY = VERSION PROBLEM
BAD RECORD = HUMAN-RISK EVENT
STORY / CAMPAIGN / BRANDING = NEVER SILENTLY PROMOTED TO AUTHORITY
```

`SECOND_OPINION_BOUND / PUBLIC_WEB_MEMBRANE_ACTIVE / HUMAN_FIRST / REPLAY_OPEN / AUTHORITY_CREATED_FALSE`
