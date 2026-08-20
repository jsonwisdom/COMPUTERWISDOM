# Congress 3.0 — Onion Metadata Mesh v0.2

**Observed:** 2026-08-20  
**Operator label:** `jaywisdom.base.eth`  
**Classification:** `CITIZEN_SYSTEMS_ACCOUNTABILITY_METADATA_ARCHITECTURE`  
**Authority created:** `false`

## Why this exists

The banking lane is only one layer. Digital-asset systems cross multiple legal, commercial, custody, identity, fraud, privacy, and enforcement domains. The mesh keeps those layers separate while allowing a single event to be replayed end to end.

```text
CONGRESS / LAW
  -> WAR / NATIONAL SECURITY
  -> COMMERCIAL / CORPORATE
  -> POLICY / REGULATION
  -> BANKING / FINANCIAL INSTITUTIONS
  -> DIGITAL-ASSET MARKET STRUCTURE
  -> EXCHANGE / BROKER / DEALER
  -> CUSTODY
  -> SELF-CUSTODY / SOFTWARE WALLET
  -> BLOCKCHAIN / PUBLIC LEDGER
  -> FRAUD / SCAM INFRASTRUCTURE
  -> FBI / DOJ / SECRET SERVICE / TREASURY
  -> AI / ANALYTICS
  -> STATE / FIELD-OFFICE CONSEQUENCE
  -> CITIZEN NOTICE / REVIEW / CORRECTION
  -> RECEIPT / REPLAY
```

No layer silently inherits the authority or metadata rules of another.

## Required metadata envelope

Every edge should preserve, when known:

```text
event_id
claim_id
observed_at
occurred_at
source_published_at
jurisdiction
geography
layer
sub_layer
actor
actor_role
system
system_owner
system_operator
execution_identity
authority_source
authority_state
policy_or_rule
machine_rule
custody_model
wallet_model
asset_or_token
account_or_wallet_identifier
transaction_identifier
transaction_timestamp
transaction_amount
counterparty
communication_channel
device_or_network_metadata
data_collected
data_derived
data_retention
data_access
data_sharing
legal_process
ai_use
ai_output_role
human_review_required
record_delta
citizen_consequence
notice
review_path
correction_path
source_uri
source_hash
confidence
evidence_state
open_questions
authority_created
```

`UNKNOWN` is a valid value. Missing retention, access, or model-detail fields must not be invented.

## Onion A — Congress / enacted authority

Questions:
- What bill, statute, appropriation, resolution, hearing, committee report, or oversight action exists?
- What chamber/state is it in?
- Does the source describe policy, enact law, fund enforcement, or merely investigate?

Membranes:

```text
HEARING != LAW
CRS_REPORT != LAW
COMMITTEE_ADVANCE != LAW
PASSED_HOUSE != LAW
APPROPRIATION != EXECUTION
```

## Onion B — War / national security

Use only when the digital-asset event intersects sanctions, terrorism, cartels, hostile-state activity, trafficking, transnational organized crime, or national-security authorities.

Metadata additions:

```text
threat_actor_class
foreign_jurisdiction
sanctions_nexus
trafficking_nexus
critical_infrastructure_nexus
national_security_authority
interagency_partners
```

`CRYPTO_USED_BY_CRIMINAL != CRYPTO_IS_CRIMINAL`.

## Onion C — Commercial / corporate

Separate corporation from product and product from legal role.

Example:

```text
Coinbase Global, Inc. = public corporate parent
Coinbase exchange/account = custodial/commercial financial service
Coinbase Wallet / Base App = separate self-custodial software/product lane
Base blockchain = public blockchain infrastructure lane
```

Do not collapse these into `COINBASE`.

Required corporate metadata:

```text
legal_entity
product
service
registration_status
customer_relationship
custody_control
terms_version
privacy_policy_version
regulator
law_enforcement_request_surface
```

## Onion D — Policy / regulation

Bind:

```text
regulator
proposed_rule
final_rule
policy_version
effective_date
regulated_activity
exemption
recordkeeping_requirement
customer_protection_requirement
```

`POLICY != STATUTE` and `PROPOSED_RULE != FINAL_RULE`.

## Onion E — Banking / fiat rails

Track the fiat boundary separately from the blockchain boundary.

```text
bank
payment_rail
ACH/wire/card/cash
account_number_or_tokenized_reference
originating_institution
receiving_institution
fraud_freeze_attempt
recovery_action
```

This is where IC3's Financial Fraud Kill Chain and financial-institution coordination can intersect an otherwise on-chain event.

## Onion F — Digital-asset market structure

H.R. 3633 / CLARITY is a market-structure lane, not a complete anti-scam statute.

Track:

```text
asset_classification
SEC_jurisdiction
CFTC_jurisdiction
broker_status
dealer_status
exchange_status
custodian_status
recordkeeping_duty
self_custody_right
```

The House-passed CLARITY text protects lawful hardware/software self-custody and peer-to-peer use while separately imposing recordkeeping, audit-trail, customer-protection, and information duties on covered digital commodity brokers/dealers.

## Onion G — Exchange / broker / custodial platform

Example: a hosted Coinbase account.

Potential platform metadata, depending on product and legal basis:

```text
basic_customer_information
identity/KYC_information
transaction_information
wallet_information
blockchain_data
IP_address
device/browser_information
product_usage
support_communications
payment_method
legal_request_identifier
requesting_agency
```

Coinbase's 2025 Transparency Report states it received 12,716 government/law-enforcement information requests during its reporting period and says governments do not receive direct access to Coinbase customer systems.

## Onion H — Self-custody / wallet software

A self-custodial wallet is not the same object as a custodial exchange account.

Potential service-layer metadata can still exist even when the provider does not hold the private key. Coinbase Wallet/Base App public privacy notices describe collection that can include public wallet addresses, product usage, diagnostic data, device/browser data, IP address, push tokens, and temporary dapp-connection information.

```text
PRIVATE_KEY_CUSTODY = USER/DEVICE
PUBLIC_ADDRESS = PUBLIC_CHAIN_IDENTIFIER
SERVICE_METADATA != PRIVATE_KEY
WALLET_SOFTWARE != CUSTODIAL_EXCHANGE
SELF_CUSTODY != NO_METADATA
```

## Onion I — Public blockchain

Public-chain metadata is different from platform metadata.

```text
block_number
block_timestamp
transaction_hash
from_address
to_address
amount
token_contract
method/event
logs
fee/gas
signature/public-key evidence
```

Public blockchain visibility does not by itself identify a natural person.

## Onion J — Fraud / scam center

The FBI's 2025 IC3 report calls cryptocurrency investment fraud the highest source of financial losses to Americans in 2025, with about $7.2B reported in losses. It describes organized scam operations in Southeast Asia, including trafficking/forced-labor elements.

Track:

```text
initial_contact_channel
social_media_or_dating_app
messaging_platform
fake_investment_platform
wallet_destination
crypto_asset
fiat_onramp
exchange_onramp
withdrawal_blocked
tax_or_fee_demand
recovery_scam_follow_on
human_trafficking_nexus
scam_compound_location
```

## Onion K — FBI / DOJ / enforcement

Do not call this a `Louisiana AI database` unless a source proves that exact system exists.

Observed public architecture:
- FBI New Orleans is the FBI field office covering Louisiana.
- IC3 is a national FBI complaint/intelligence mechanism.
- FBI states that IC3 complaints are analyzed and disseminated for investigative/intelligence purposes and shared through FBI field offices and law-enforcement partners.
- FBI public fraud guidance requests metadata such as websites, emails, phone numbers, dates, payment type, amount, account numbers, receiving financial institution, cryptocurrency addresses, and interaction narrative.
- Some FBI victim forms state information is maintained in the FBI Central Records System, `DOJ/FBI-002`.

Potential enforcement metadata envelope:

```text
complainant_state
complaint_id
complaint_date
crime_type
descriptor
contact_channel
website/url
email
phone
transaction_date
payment_type
amount
account_number
financial_institution
crypto_address
interaction_narrative
referral
field_office
partner_agency
asset_freeze_or_recovery
```

Retention period, exact database tables, exact AI model/version, query logs, and Louisiana-specific storage architecture are `UNKNOWN` unless separately source-bound.

## Onion L — FBI AI / analytics

The FBI publicly says it uses AI for vehicle recognition, triage of voice samples for language identification, speech-to-text generation, and video analytics. It says AI-generated information is used for investigative leads and that a human investigator/analyst must assess output before substantive action.

Track:

```text
input_data_type
ai_capability
model_or_vendor_if_public
lead_generated
human_reviewer
review_timestamp
substantive_action
validation_result
```

```text
AI_LEAD != PROBABLE_CAUSE
AI_LEAD != GUILT
AI_OUTPUT != GOVERNMENT_DECISION
SYSTEM_OWNER = FBI
FBI_DIRECTOR = EXECUTIVE_LEADERSHIP
DIRECTOR_NAME != SYSTEM_OPERATOR_PER_EVENT
```

Kash Patel is the current FBI Director; that does not mean he personally operates each AI system, database query, IC3 referral, or Louisiana investigation.

## Onion M — Louisiana / John Kennedy lens

Sen. John Kennedy is a Louisiana senator serving on Banking and Judiciary. His public record provides useful but separate policy lenses:

1. Digital-asset market structure: move deliberately because crypto integration with federal regulation is confusing.
2. Shadow banking: entities performing bank-like functions should not escape bank-like oversight merely through corporate form.
3. Financial-data privacy: Kennedy has opposed the SEC Consolidated Audit Trail's collection of customer/order information and argued Congress did not authorize that system.

This does **not** mean Kennedy has endorsed this metadata mesh.

Useful Kennedy-style questions:

```text
WHO COLLECTED IT?
WHAT EXACT DATA DID THEY COLLECT?
WHO AUTHORIZED THAT COLLECTION?
WHERE IS IT STORED?
HOW LONG IS IT RETAINED?
WHO CAN QUERY IT?
WHO CAN SHARE IT?
WHAT MACHINE TOUCHED IT?
WHAT DID THE MACHINE INFER?
WHAT HUMAN CHECKED THE INFERENCE?
WHAT ACTION FOLLOWED?
WHAT CAN THE CITIZEN CHALLENGE?
```

## Onion N — Congress's anti-scam lanes

Congress is not doing nothing; the lanes are fragmented.

```text
CRS IF13008 (2025) = congressional research on cryptocurrency investment / pig-butchering scams
S.710 = Crypto ATM Fraud Prevention Act of 2025; introduced/referred
S.2544 = GUARD Act; reported by Judiciary and placed on Senate Legislative Calendar in Feb. 2026
H.R.5490 = Dismantle Foreign Scam Syndicates Act; introduced/referred
H.R.3633 = CLARITY; market structure, separate lane
Senate Judiciary 2025 hearing = transnational scam/older-American/crypto-ATM oversight lane
```

The metadata problem is that these are different committees, statutes, agencies, and technical systems. The mesh should join evidence without pretending Congress itself has joined the programs.

## Onion O — State crisscross

State numbers are victim-report metadata, not proof of local enforcement quality or scam origin.

The 2025 IC3 cryptocurrency state table reports:

| State | Complaints | Losses | Loss/complaint |
|---|---:|---:|---:|
| Louisiana | 1,366 | $53,679,269 | ~$39,297 |
| Minnesota | 2,253 | $151,658,166 | ~$67,314 |
| Alabama | 1,687 | $93,813,940 | ~$55,610 |
| Wisconsin | 3,092 | $87,426,944 | ~$28,275 |

Compared with 2024:

| State | Complaint delta | Complaint % | Loss delta | Loss % |
|---|---:|---:|---:|---:|
| Louisiana | +201 | +17.3% | +$4,373,249 | +8.9% |
| Minnesota | +401 | +21.7% | +$60,043,473 | +65.5% |
| Alabama | +374 | +28.5% | +$42,540,342 | +83.0% |
| Wisconsin | +1,119 | +56.7% | +$19,913,149 | +29.5% |

Minnesota had 839 fewer reported crypto complaints than Wisconsin in 2025 but about $64.2M more reported loss. That is a severity signal, not a causal finding.

## Final mesh law

```text
CONGRESS != BANK
BANK != EXCHANGE
EXCHANGE != WALLET
WALLET != BLOCKCHAIN
BLOCKCHAIN_ADDRESS != NATURAL_PERSON
PUBLIC_LEDGER != PLATFORM_METADATA
PLATFORM_METADATA != FBI_RECORD
FBI_RECORD != AI_INFERENCE
AI_INFERENCE != INVESTIGATIVE_FACT
INVESTIGATIVE_FACT != LEGAL_FINDING
LAW_ENFORCEMENT_ACTIVITY != CONGRESSIONAL_ACTION

JOIN BY RECEIPT.
DO NOT JOIN BY NAME.
```
