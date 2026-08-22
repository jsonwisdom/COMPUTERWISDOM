# Minnesota Banking / Merchant / Foreign Links — BoxD Quad Onion v0.1

Status: DRAFT / SOURCE-BOUND / PUBLIC-AUDIT / UNMERGED

```text
BOXD = INSTITUTIONAL REPLAY CONTAINER
MAX_GRAY_BABY = EPISTEMIC / DRIFT-CHECK EXPLAINER
AUTHORITY_CREATED = FALSE
LEGAL_FINDING_CREATED = FALSE
BANK_CULPABILITY_CREATED = FALSE
MERCHANT_CULPABILITY_CREATED = FALSE
FOREIGN_NEXUS != FOREIGN_CULPABILITY
```

## Scope

Audit Minnesota fraud records backward from plea / conviction / forfeiture / official charging record into the financial execution rails.

The four BoxD onions remain unchanged. Banking, credit-card, merchant, wire, crypto, property, and foreign-destination objects are execution subgraphs inside Onion 3; they do not become guilt labels merely because they appear in a transaction chain.

---

## 🧅 1 — RECORD / CRIMINAL RECEIPTS

### Feeding Our Future

As of July 21, 2026, DOJ reported 68 Feeding Our Future defendants convicted. A conviction or guilty plea is a PASS only for the defendant and conduct actually adjudicated or admitted.

```text
PLEA / CONVICTION
→ FALSE RECORD / CLAIM
→ PROGRAM PAYMENT
→ DISPOSITION
= PASS_CASE_BOUND
```

Source:
- https://www.justice.gov/usao-mn/pr/pelican-rapids-man-68th-defendant-plead-guilty-feeding-our-future-fraud-scheme

### HSS / Brilliant Minds

On July 24, 2026, DOJ reported that Moktar Hassan Aden, Mustafa Dayib Ali, Khalid Ahmed Dayib, and Abdifitah Mohamud Mohamed had each pleaded guilty to wire fraud involving approximately $2.2 million stolen from Minnesota Medicaid's Housing Stabilization Services program.

Source:
- https://www.justice.gov/opa/pr/four-men-plead-guilty-2m-minnesota-medicaid-fraud

```text
BRILLIANT_MINDS_WIRE_FRAUD = PASS_PLEA_BOUND
OTHER_UNADJUDICATED_HSS_DEFENDANTS = HOLD
```

---

## 🧅 2 — AUTHORITY / PAYMENT CONTROL

Relevant authority objects include MDE for the federal child-nutrition program and Minnesota DHS / Medicaid payment administration for state Medicaid benefits. Program authority is separate from criminal liability.

```text
PROGRAM_ADMINISTRATION = SOURCE_BOUND
PAYMENT_AUTHORITY = CASE / PROGRAM SPECIFIC
OVERSIGHT_FAILURE != CRIMINAL_FRAUD
OFFICE_HOLDER != TRANSACTION_ACTOR
```

The audit must bind:

```text
PROGRAM
→ PAYOR
→ CLAIM APPROVAL PATH
→ PAYMENT FILE / REMITTANCE
→ RECIPIENT ENTITY
→ ACCOUNT
→ BENEFICIAL / CONTROL PERSON, IF PROVEN
```

---

## 🧅 3 — EXECUTION / BANKING / MERCHANT / FOREIGN RAILS

### A. Named deposit institutions in Feeding Our Future forfeiture receipts

DOJ plea materials identify fraud-derived funds seized from accounts at:

- Bell Bank — $309,993.51 in an account for Cosmopolitan Business Solutions d/b/a Safari Restaurant.
- Bell Bank — $435,512.44 in an account for 3017 LLC.
- Northeast Bank — $472,889.08 in an account for 3017 LLC.
- Star Choice Credit Union — $343,418.98 in an account for Stone Bridge Development LLC.

Source:
- https://www.justice.gov/usao-mn/pr/former-minneapolis-mayoral-aide-and-safari-restaurant-co-owner-both-plead-guilty-250

Disposition:

```text
ACCOUNT_EXISTENCE_IN_CASE_RECORD = PASS
SEIZED_PROCEEDS_EDGE = PASS_PLEA_BOUND
BANK_PARTICIPATED_IN_FRAUD = NOT_ESTABLISHED
BANK_KNEW_SOURCE_WAS_FRAUD = NOT_ESTABLISHED
BANK_CONTROL_FAILURE = HOLD_REGULATORY_RECEIPT_REQUIRED
```

### B. Credit-card rail

DOJ alleged in the first HSS wave that Brilliant Minds defendants shared a Platinum American Express card, accrued nearly $500,000 in charges, and paid those charges from company accounts. The same four defendants later pleaded guilty to wire fraud in July 2026.

Sources:
- https://www.justice.gov/usao-mn/pr/defendants-charged-first-wave-housing-stabilization-fraud-cases
- https://www.justice.gov/opa/pr/four-men-plead-guilty-2m-minnesota-medicaid-fraud

```text
AMEX_CARD_RAIL = SOURCE_BOUND
COMPANY_ACCOUNT_TO_CARD_PAYMENT = SOURCE_BOUND
UNDERLYING_MERCHANT_LIST = HOLD
MERCHANT_CATEGORY_CODES = HOLD
ACQUIRING_BANK = HOLD
PROCESSOR / GATEWAY = HOLD
AMEX_KNOWLEDGE_OR_COMPLICITY = NOT_ESTABLISHED
```

Additional DOJ records show more than $200,000 in credit-card spending by Ahmed Abdullahi Ghedi from an account holding fraud proceeds, but the issuer and merchants are not identified in the public press release.

Source:
- https://www.justice.gov/usao-mn/pr/minneapolis-man-pleads-guilty-forty-seventh-conviction-feeding-our-future-fraud-scheme

### C. Managed-care / reimbursement rail

DOJ states that Smart Therapy and Star Autism received EIDBI reimbursement funds through Minnesota DHS and UCare in the cited fraud cases.

Source:
- https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes

```text
PAYOR_NAMED = PASS_SOURCE_BOUND
PAYOR_COMPLICITY = NOT_ESTABLISHED
CLAIM_EDIT / PREPAYMENT_CONTROL_HISTORY = HOLD_DEEPER_RECORD
```

### D. Primary foreign financial links

#### Kenya — strongest repeated foreign-money destination

Plea-bound example: Mohamed Ismail Alishire admitted a $216,300 wire from Hoodo Properties to Jaafar Jelle & Co. toward purchase of the Karibu Palms Resort in Diani Beach, Kenya, and agreed to forfeit a Nairobi apartment and the resort.

Source:
- https://www.justice.gov/usao-mn/pr/brooklyn-park-man-pleads-guilty-his-role-250-million-feeding-our-future-fraud-scheme

Other official records state:
- Asha Farhan Hassan pleaded guilty to wire fraud in December 2025; earlier charging records stated Smart Therapy proceeds were sent abroad and used for Kenya real estate.
- DOJ alleged Abdinajib Hassan Yussuf sent more than $200,000 in Star Autism proceeds to Kenya; that specific defendant was charged in the cited December 2025 record, not convicted there.
- DOJ alleged Asad Adow invested HSS proceeds in Kenya real estate.

Sources:
- https://www.justice.gov/usao-mn/pr/first-defendant-charged-autism-fraud-scheme-0
- https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes
- https://www.justice.gov/usao-mn/pr/defendants-charged-first-wave-housing-stabilization-fraud-cases

```text
KENYA_FINANCIAL_NEXUS = PASS_MULTIPLE_SOURCE_OBJECTS
PERSON_SPECIFIC_GUILT = PLEA / CONVICTION ONLY
KENYAN_INSTITUTION_CULPABILITY = NOT_ESTABLISHED
```

#### Turkey — scheme-level asset destination

DOJ's Bock/Said trial-conviction release states fraud proceeds were used to purchase real estate in Kenya and Turkey.

Source:
- https://www.justice.gov/usao-mn/pr/federal-jury-finds-feeding-our-future-mastermind-and-co-defendant-guilty-250-million

```text
TURKEY_ASSET_DESTINATION = PASS_SCHEME_SOURCE
TURKISH_INSTITUTION_CULPABILITY = NOT_ESTABLISHED
```

#### Travel is not a financial link

DOJ alleged personal travel funded with HSS proceeds to London, Sydney, Dubai, Istanbul, and destinations in Saudi Arabia for two Pristine Health defendants. That is a charged allegation in the cited record, not a conviction, and travel destination alone does not establish a foreign financial institution or conspirator.

Source:
- https://www.justice.gov/usao-mn/pr/six-additional-defendants-charged-one-defendant-pleads-guilty-ongoing-fraud-schemes

```text
TRAVEL_DESTINATION != FOREIGN_BANK
TRAVEL_DESTINATION != CONSPIRATOR
FOREIGN_PROPERTY != FOREIGN_GOVERNMENT INVOLVEMENT
WIRE_ABROAD != RECIPIENT_CULPABILITY
```

---

## 🧅 4 — OVERSIGHT / CORRECTION / RECOVERY

The strongest financial oversight receipts are seizures, forfeiture agreements, guilty pleas, convictions, subpoenas, Medicaid program controls, and HSS termination / fraud-response actions.

```text
CLAIM
→ PAYMENT
→ ACCOUNT / CARD / WIRE / ASSET
→ INVESTIGATION
→ SEIZURE / FORFEITURE
→ PLEA / CONVICTION / HOLD
→ RESTITUTION / SENTENCE, IF ENTERED
→ VERSIONED PUBLIC RECEIPT
```

A bank, card network, managed-care organization, merchant, processor, foreign recipient, or destination country is not promoted to culpability merely because it appears in this chain.

---

# MAX Gray Baby reverse questions

```text
START AT THE MONEY.
WHO PAID?
WHICH CLAIM CREATED THE PAYMENT?
WHICH ENTITY RECEIVED IT?
WHICH ACCOUNT / CARD / PROCESSOR TOUCHED IT?
WHICH MERCHANT RECEIVED THE NEXT LEG?
WAS THAT MERCHANT NAMED IN A PLEA, CONVICTION, FORFEITURE, OR ONLY AN ALLEGATION?
DID MONEY LEAVE THE UNITED STATES?
TO WHICH ACCOUNT / ENTITY / ASSET?
WHAT IS PROVEN ABOUT THE RECIPIENT?
WHAT CONTROL SHOULD HAVE FIRED?
WHEN DID NOTICE OCCUR?
WHAT WAS RECOVERED?
```

# BoxD disposition

```text
O1_RECORD / CRIMINAL = PASS_PARTIAL_CASE_BOUND
O2_AUTHORITY / PAYMENT_CONTROL = PASS_GENERAL / DEEPER_TRANSACTION_AUTHORITY_OPEN
O3_EXECUTION / BANKING / MERCHANT / FOREIGN = PASS_PARTIAL
O4_OVERSIGHT / RECOVERY = PASS_PARTIAL
LEELOO_MULTI_PASS = HOLD
```

Reason for HOLD:

```text
NAMED_BANKS != BANK_WRONGDOING
NAMED_CARD_NETWORK != PROCESSOR_COMPLICITY
PUBLIC_PRESS_RELEASE != COMPLETE TRANSACTION LEDGER
MERCHANT_LIST / MCC / ACQUIRER / GATEWAY = MISSING
FOREIGN_RECIPIENT BANK DETAILS = MOSTLY MISSING
SAR / AML / BSA RECORDS = NONPUBLIC OR NOT YET SOURCE-BOUND
```

## Core rule

**Follow the money without promoting the rail into the crime. Account → card → merchant → wire → asset → foreign destination must remain receipt-bound at every hop.**
