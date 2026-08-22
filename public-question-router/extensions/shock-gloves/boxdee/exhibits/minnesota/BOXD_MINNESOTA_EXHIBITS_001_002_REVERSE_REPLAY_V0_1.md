# BoxD Minnesota Exhibits 001–002 — Four-Onion Reverse RePlay v0.1

Status: DRAFT / ZERO-TRUST / EXHIBIT-INTEGRITY AUDIT / UNMERGED

```text
BOXD = PERSPECTIVE / DIAGNOSTIC LAYER
EXHIBIT != UNDERLYING FACT
IMAGE_HASH != CLAIM TRUTH
NAMED PUBLIC OFFICIAL != WRONGDOING
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
```

## Exhibit identities

### Exhibit 001 — Angie Craig BoxDee card

SHA-256:
`e36796ffaccc246c367c375c931c02336ec0e2c3312062f061cc1ed96a812c5b`

### Exhibit 002 — Peggy Flanagan BoxDee card

SHA-256:
`63a42a4e046be7f8171e57876f76c35ed2a4dce5e57955d97c816c66866e90fe`

The uploaded images are conversation exhibits. The repository stores their manifest/hashes and the replay findings; it does not currently store the raw image bytes.

---

# LeeLoo Multi Pass — Four Onions

```text
ONION 1 — RECORD / TRUTH
What exact factual proposition is shown, and does the cited source support it?

ONION 2 — AUTHORITY
What office/jurisdiction/statute/committee/delegation actually gives the subject power?

ONION 3 — EXECUTION / MONEY
What program, appropriation, contract, payment, administration, investigation, or implementation edge exists?

ONION 4 — OVERSIGHT / CORRECTION
What audit, OIG, court, legislative review, disclosure, correction, or appeal path exists?
```

Promotion rule:

```text
LEELoo_MULTI_PASS = PASS
ONLY IF
ONION_1 = PASS
AND ONION_2 = PASS
AND ONION_3 = PASS
AND ONION_4 = PASS
AND ALL REQUIRED CROSS-EDGES = PASS
```

A single `HOLD`, `CONFLICT`, or `REJECT` blocks promotion.

---

# Shared internal contradiction — both exhibits

Both cards display a replay/run timestamp in **2025-05-28** while their own timelines and source claims include **May 2026 events**.

```text
RUN_TIME = 2025-05-28
EVENT_CLAIM = 2026-05-21 / 2026-05-28

RESULT = CONFLICT_TEMPORAL_METADATA
```

The card cannot have been generated at the displayed 2025 timestamp while truthfully incorporating events that occurred in 2026, unless `Run Time` means something other than generation/observation time. No such alternate semantics are stated on the card.

This conflict applies to the artifact metadata itself, independent of any conclusion about the named person.

---

# Exhibit 001 — Angie Craig

## Onion 1 — Record / Truth

### PASS — current office

The U.S. House Clerk identifies Angie Craig as the Democratic Representative for Minnesota's 2nd District.

Official source:
- https://clerk.house.gov/members/C001119

### CONFLICT — current committee list on card

The card states current committees including Agriculture, Education & Workforce, and Small Business.

The current House Clerk page lists **Committee on Agriculture**. House historical records show Craig served on Small Business in the 116th–117th Congresses, not the current 119th Congress.

Official sources:
- https://clerk.house.gov/members/C001119
- https://history.house.gov/People/Detail/25769805182

Disposition:

```text
AGRICULTURE = PASS
EDUCATION_AND_WORKFORCE_AS_CURRENT_ASSIGNMENT = REJECT / UNSUPPORTED
SMALL_BUSINESS_AS_CURRENT_ASSIGNMENT = REJECT / HISTORICAL_ONLY
```

### REJECT — H.R. 1770 attribution

The card identifies `H.R. 1770, 2025` as a fraud-enforcement/accountability bill associated with Craig.

Congress.gov identifies H.R. 1770 in the 119th Congress as the **Consumer Safety Technology Act**, sponsored by Rep. Darren Soto, with three listed cosponsors; Angie Craig is not one of them.

Official source:
- https://www.congress.gov/bill/119th-congress/house-bill/1770

Craig did introduce a different fraud-related bill: **H.R. 7155, Stop Fraud in Federal Programs Act of 2026**, introduced January 20, 2026.

Official source:
- https://www.congress.gov/bill/119th-congress/house-bill/7155

Disposition:

```text
CARD_HR1770_FRAUD_CLAIM = REJECT
CRAIG_FRAUD_LEGISLATION_EXISTS = PASS_BOUNDED_TO_HR7155
```

### CONFLICT — financial disclosure custodian

The card points to `OGE.gov` for Craig's annual financial disclosures.

House Ethics guidance states House Members file Financial Disclosure reports with the **Clerk of the House**; the House Committee on Ethics is the supervising ethics office.

Official source:
- https://ethics.house.gov/financial-disclosure/

Disposition:

```text
HOUSE_MEMBER_FINANCIAL_DISCLOSURE_EXISTS = PASS_GENERAL
OGE_AS_PRIMARY_HOUSE_MEMBER_CUSTODIAN = REJECT
HOUSE_CLERK / HOUSE_ETHICS = PASS
```

### PASS — Minnesota May 21, 2026 health-care fraud takedown exists

DOJ announced charges against 15 defendants for alleged schemes involving more than $90 million in intended loss across seven state-managed Medicaid programs.

Official source:
- https://www.justice.gov/opa/pr/minnesota-health-care-fraud-takedown-results-charges-against-15-defendants-over-90m-fraud

Membrane:

```text
CHARGED != CONVICTED
ALLEGED_INTENDED_LOSS != FINAL_ADJUDICATED_LOSS
STATE_PROGRAM_FRAUD_CONTEXT != CRAIG_PERSONAL_MISCONDUCT
```

## Onion 2 — Authority

### PASS — legislative / committee authority exists

Craig is a Member of Congress and currently serves on the House Agriculture Committee; her official site identifies her as the top Democrat/ranking member on Agriculture.

Official sources:
- https://clerk.house.gov/members/C001119
- https://craig.house.gov/about/committees

### HOLD / REJECT — operational Minnesota DHS / Medicaid authority

No source bound in this replay gives Craig operational control over Minnesota DHS, Medicaid provider enrollment, claims payment, or DOJ/FBI fraud investigations.

```text
FEDERAL_LEGISLATOR = PASS
MN_DHS_OPERATOR = REJECT_UNSUPPORTED
DOJ_FBI_INVESTIGATOR = REJECT_UNSUPPORTED
```

## Onion 3 — Execution / Money

### HOLD

The card shows a general Medicaid money-flow diagram but does not bind Craig to a payment-authorization, provider-enrollment, claims-adjudication, contract, invoice, or operational-control edge.

```text
CRAIG_VOTE / LEGISLATION = SOURCEABLE
CRAIG_PAYMENT_AUTHORIZATION = HOLD / UNSUPPORTED
CRAIG_PROVIDER_ADMINISTRATION = HOLD / UNSUPPORTED
```

## Onion 4 — Oversight / Correction

### PASS_PARTIAL

Legislative activity and public disclosures are reviewable through Congress/House records. DOJ fraud cases have court and prosecutorial records. But the card's own source/citation errors require correction before it can be treated as an audit-grade exhibit.

## LeeLoo disposition — Exhibit 001

```text
ONION_1_RECORD = CONFLICT
ONION_2_AUTHORITY = PASS_PARTIAL / HOLD_OPERATIONAL
ONION_3_EXECUTION_MONEY = HOLD
ONION_4_OVERSIGHT_CORRECTION = PASS_PARTIAL
CROSS_EDGES = CONFLICT

LEELoo_MULTI_PASS = FAIL_CLOSED
EXHIBIT_STATE = CONFLICT
```

### Fraud-expert label

```text
ANGIE_CRAIG_AS_MINNESOTA_FRAUD_EXPERT = HOLD_ROLE_EXPERTISE
ANGIE_CRAIG_AS_FRAUD_LEGISLATION_ACTOR = PASS_BOUNDED
ANGIE_CRAIG_AS_OPERATIONAL_FRAUD_INVESTIGATOR = REJECT_UNSUPPORTED
```

---

# Exhibit 002 — Peggy Flanagan

## Onion 1 — Record / Truth

### PASS — office and housing/homelessness role

Minnesota's official Governor/Lieutenant Governor site identifies Peggy Flanagan as Minnesota's 50th Lieutenant Governor. It states that she advances housing stability, prioritizes the state's homelessness response, and chairs the Minnesota Interagency Council on Homelessness.

Official source:
- https://mn.gov/governor/about-gov/peggyflanagan/

### CONFLICT — Housing Stabilization Services launch date

The card states HSS launched January 1, 2022.

Minnesota DHS states HSS was launched in **2020**; a 2026 Minnesota House review describes the launch as **July 2020**. The official DHS termination notice confirms the program ended October 31, 2025 because of widespread fraud concerns.

Official sources:
- https://mn.gov/dhs/about-us/legislative-media/media/news/?id=1053-711321
- https://www.house.mn.gov/members/profile/news/15618/52234

Disposition:

```text
HSS_LAUNCH_2022 = REJECT
HSS_LAUNCH_2020 = PASS
HSS_ENDED_2025_10_31 = PASS
FRAUD_CONCERNS_AS_TERMINATION_REASON = PASS
```

### PASS — May 21, 2026 DOJ takedown context

DOJ's May 21, 2026 Minnesota Health Care Fraud Takedown charged 15 defendants in alleged schemes involving over $90 million in intended loss.

Official source:
- https://www.justice.gov/opa/pr/minnesota-health-care-fraud-takedown-results-charges-against-15-defendants-over-90m-fraud

Again:

```text
STATE_FRAUD_CONTEXT != FLANAGAN_PERSONAL_MISCONDUCT
```

## Onion 2 — Authority

### PASS — executive advocacy / coordination role

Flanagan's official profile supports a high-level housing-stability and interagency homelessness coordination role.

### HOLD / REJECT — day-to-day HSS operational control

The same profile does not establish that the Lieutenant Governor personally administered HSS claims, provider enrollment, payment controls, or fraud investigations. Minnesota DHS is the relevant administrative agency for the program.

```text
HOUSING_POLICY / INTERAGENCY_COORDINATION = PASS_GENERAL
HSS_DAY_TO_DAY_ADMINISTRATION = REJECT_UNSUPPORTED
MEDICAID_PAYMENT_AUTHORIZATION = REJECT_UNSUPPORTED
FRAUD_INVESTIGATION = REJECT_UNSUPPORTED
```

## Onion 3 — Execution / Money

### HOLD

The card's money-flow diagram correctly depicts a general federal Medicaid → state DHS → provider structure at a conceptual level, but it does not bind Flanagan to a specific payment authorization, invoice, provider enrollment, fraudulent claim, or operational decision.

## Onion 4 — Oversight / Correction

### PASS_PARTIAL

Minnesota DHS publicly documented HSS termination and multiple program-integrity actions, including provider payment suspensions, referrals to law enforcement, enrollment moratoria, revalidation, and enhanced review.

Official sources:
- https://mn.gov/dhs/program-integrity/factcheck/
- https://mn.gov/dhs/partners-and-providers/news-initiatives-reports-workgroups/minnesota-health-care-programs/provider-news/fighting-fraud-waste-and-abuse.jsp

The card nevertheless contains a hard launch-date error and impossible runtime chronology, so its own correction path is open.

## LeeLoo disposition — Exhibit 002

```text
ONION_1_RECORD = CONFLICT
ONION_2_AUTHORITY = PASS_GENERAL / HOLD_OPERATIONAL
ONION_3_EXECUTION_MONEY = HOLD
ONION_4_OVERSIGHT_CORRECTION = PASS_PARTIAL
CROSS_EDGES = HOLD / CONFLICT

LEELoo_MULTI_PASS = FAIL_CLOSED
EXHIBIT_STATE = CONFLICT
```

### Fraud-expert label

```text
PEGGY_FLANAGAN_AS_MINNESOTA_FRAUD_EXPERT = HOLD_ROLE_EXPERTISE
PEGGY_FLANAGAN_AS_HOUSING_POLICY / COORDINATION_ACTOR = PASS_GENERAL
PEGGY_FLANAGAN_AS_HSS_OPERATIONAL_ADMINISTRATOR = REJECT_UNSUPPORTED
PEGGY_FLANAGAN_AS_FRAUD_INVESTIGATOR = REJECT_UNSUPPORTED
```

---

# Cross-exhibit Reverse Replay

The two cards currently demonstrate a useful BoxD lesson:

```text
SATIRICAL_CARD_CAN_HAVE_GOOD_MEMBRANES
AND
STILL_CONTAIN_BAD_FACTS
```

Both cards correctly attempt to separate policy influence from operational control. But audit-grade promotion fails because the cards themselves contain source/chronology defects.

```text
EXHIBIT_001 = CONFLICT
EXHIBIT_002 = CONFLICT

NOT BECAUSE CRAIG OR FLANAGAN ARE PROVEN WRONGDOERS
BUT BECAUSE THE ARTIFACTS FAIL THEIR OWN RECEIPT STANDARD
```

## Required corrections before re-render

Exhibit 001:
1. correct runtime / replay timestamp semantics;
2. replace current committee assignments with current House Clerk data;
3. replace H.R. 1770 with H.R. 7155 if the intended claim is Craig's 2026 fraud legislation;
4. replace OGE disclosure reference with House Clerk / House Ethics;
5. distinguish introduced bill from enacted law;
6. preserve `charged != convicted` and `alleged intended loss != adjudicated loss`.

Exhibit 002:
1. correct runtime / replay timestamp semantics;
2. correct HSS launch date to 2020 (with exact July 2020 date if that source is selected as canonical);
3. distinguish housing/homelessness policy coordination from DHS operational authority;
4. preserve `charged != convicted` and person-specific non-attribution.

## BoxD terminal

```text
FIND_YOUR_WAY_OUT_OF_THE_BOX = ACTIVE
FAFO_ATTACHMENT = SOURCE_THE_CARD_ITSELF
LEELOO_MULTI_PASS = BLOCKED

CAUSE:
EXHIBIT_RECEIPT_INTEGRITY_CONFLICT
```

The fix is not to discard the exhibits. The fix is to replay and version them so the corrected cards preserve the original hashes as failed prior states.
