# Dual Onion Audit Flywheel v0.1

**Lane:** American Citizen / public-record audit

**Identity surface:** `jaywisdom.base.eth` / `jaywisdom.eth` as declared notebook labels only; neither label proves Azure login, tenant ownership, billing ownership, wallet custody, or authority.

**Status:** `DRAFT / HOLD_FOR_ACCOUNT_SPECIFIC_RECEIPTS`

**Authority created:** `FALSE`

---

## Purpose

Build a replayable dice game that compares two very different control substrates:

1. **Azure / Microsoft Entra** — tenant identity, sign-in, role assignment, billing, resource authorization, and audit logs.
2. **Blockchain / Ethereum-Base style systems** — key or smart-wallet control, signatures, transactions, contract events, and public ledger state.

The game asks:

- Who can log in?
- What power did that identity actually have?
- What documentary evidence exists for motive or stated purpose?
- What opportunity existed in the relevant time window?
- Why was Azure or blockchain used for the action?
- Can the control chain be replayed in reverse?

The game does not infer guilt, motive, ownership, or authority from a username, wallet address, role label, transaction hash, or audit-log existence.

---

## Core membrane

```text
LOGIN != OWNER
OWNER_ROLE != BILLING_OWNER
BILLING_OWNER != GLOBAL_ADMIN
GLOBAL_ADMIN != AUTOMATIC_RESOURCE_OWNER
ROLE_ASSIGNMENT != ACTION_PERFORMED
SIGN_IN != RESOURCE_MUTATION
AUDIT_LOG != MOTIVE
STATED_PURPOSE != INNER_MENTAL_STATE
OPPORTUNITY != ACTION
TX_SIGNATURE != NATURAL_PERSON_IDENTITY
WALLET_ADDRESS != LEGAL_IDENTITY
ONCHAIN_EVENT != INVOICE
HASH != SEMANTIC_TRUTH
DICE_ROLL != FINDING
MODEL_OUTPUT != AUTHORITY
```

---

## Microsoft control split

Azure does not have one universal "account holder" field that answers every control question.

The replay keeps these scopes separate:

```text
MICROSOFT_ENTRA_TENANT
    -> identities / directory roles

AZURE_SUBSCRIPTION
    -> Azure RBAC roles / resources

BILLING_ACCOUNT / PROFILE / INVOICE_SECTION
    -> billing roles / invoices / payment visibility

RESOURCE
    -> actual resource permissions and activity
```

A Microsoft Entra tenant supplies identities used to authenticate and authorize access. Azure RBAC governs Azure resources. Billing scopes have separate billing roles. A Global Administrator can in some circumstances elevate access to Azure resources, but directory and resource authorization remain distinct control planes.

---

## Dual Onion

### Azure onion — reverse replay

```text
OBSERVED_EFFECT
  ↓
RESOURCE_ACTIVITY / CONFIG_CHANGE
  ↓
AZURE_ACTIVITY_OR_RESOURCE_LOG
  ↓
ROLE / PERMISSION REQUIRED
  ↓
ROLE_ASSIGNMENT AT THAT TIME
  ↓
IDENTITY / SERVICE PRINCIPAL / MANAGED IDENTITY
  ↓
SIGN-IN OR TOKEN EVENT
  ↓
CLIENT / APPLICATION / AUTH METHOD
  ↓
ENTRA TENANT
  ↓
BILLING SCOPE IF MONEY IS RELEVANT
  ↓
INVOICE / COST / PAYMENT RECORD IF RELEVANT
  ↓
STATED PURPOSE / CHANGE REQUEST / TICKET IF AVAILABLE
```

A broken required edge returns `HOLD`.

### Blockchain onion — reverse replay

```text
OBSERVED_EFFECT
  ↓
TRANSACTION / STATE CHANGE
  ↓
BLOCK + RECEIPT + EVENT LOG
  ↓
CALL TARGET / CONTRACT FUNCTION
  ↓
SIGNATURE OR SMART-WALLET AUTHORIZATION
  ↓
ADDRESS / ACCOUNT CONTROL MECHANISM
  ↓
KEY / PASSKEY / MULTISIG / CONTRACT POLICY
  ↓
OFFCHAIN SESSION OR APPLICATION IF RELEVANT
  ↓
CLAIMED HUMAN / ORGANIZATION IDENTITY
  ↓
AGREEMENT / ORDER / INVOICE IF COMMERCIAL PURPOSE IS CLAIMED
```

A public transaction can prove that a valid account authorization caused a ledger state transition. It does not by itself prove the legal identity of the signer, the business purpose, an invoice, or motive.

---

## Dice

### 1. SURFACE DIE

```text
AZURE
BLOCKCHAIN
```

### 2. QUESTION DIE

```text
LOGIN
POWER
MOTIVE_EVIDENCE
OPPORTUNITY
WHY_THIS_SUBSTRATE
```

`MOTIVE_EVIDENCE` means documentary evidence of stated purpose, incentive, business reason, ticket, policy, or contemporaneous communication. It is not psychological mind-reading.

### 3. RECEIPT DIE

```text
SIGN_IN_LOG
AUDIT_LOG
ROLE_ASSIGNMENT
BILLING_RECORD
TRANSACTION_SIGNATURE
CONTRACT_EVENT
INVOICE
```

### 4. DIRECTION DIE

```text
REVERSE
FORWARD
CROSS_COMPARE
```

### 5. CITIZEN ACTION DIE

```text
ASK
BIND
COMPARE
REPAIR
HOLD
REPLAY
```

Dice select an investigative path. Dice do not determine truth.

---

## WHO / LOGIN

For Microsoft Entra, the strongest initial sign-in receipt asks:

```text
WHO  = identity
HOW  = client/application/authentication path
WHAT = target resource
```

Required account-specific fields should include when available:

```text
user_or_service_principal_id
user_principal_name_or_app_id
sign_in_time
client_app
resource
ip_or_network_context
authentication_method
conditional_access_result
session_or_correlation_id
result
```

Current state for this artifact:

```text
AZURE_ACCOUNT_HOLDER_IDENTITY = NOT_BOUND
AZURE_TENANT_ID = NOT_BOUND
AZURE_SUBSCRIPTION_ID = NOT_BOUND
AZURE_SIGN_IN_LOG = NOT_BOUND
AZURE_AUDIT_LOG = NOT_BOUND
```

`NOT_BOUND` means no account-specific Azure receipt was supplied to this audit. It does not mean no Azure account exists.

---

## POWER

Power must be replayed from the exact role at the exact scope and time.

```text
ENTRA_DIRECTORY_ROLE
AZURE_RBAC_ROLE
BILLING_ROLE
RESOURCE_SPECIFIC_PERMISSION
TEMPORARY_ELEVATION
UNKNOWN
```

Examples of materially different powers:

- Azure subscription `Owner`: full access to subscription resources and ability to grant access to others.
- Microsoft Entra `Global Administrator`: highly privileged directory role; it does not automatically equal resource ownership, although Microsoft documents a separate elevation mechanism that can grant User Access Administrator at root scope.
- Billing roles: control invoice/cost/billing visibility and related billing actions; they are not interchangeable with resource execution roles.

Required replay:

```text
ROLE_NAME
+ SCOPE
+ ASSIGNEE
+ START_TIME
+ END_TIME_OR_ACTIVE
+ ASSIGNMENT_SOURCE
+ ELIGIBLE_VS_ACTIVE_IF_PIM
```

---

## MOTIVE EVIDENCE

Never infer motive from access alone.

Admissible motive-evidence candidates:

```text
DECLARED_ADMIN_TASK
CHANGE_TICKET
DEPLOYMENT_REQUEST
BILLING_TASK
SECURITY_RESPONSE
AUTOMATION_JOB
POLICY_REQUIREMENT
CONTRACTUAL_PURPOSE
UNKNOWN
```

Membrane:

```text
ROLE != MOTIVE
LOGIN != MOTIVE
COST_INCREASE != MOTIVE
BLOCKCHAIN_TRANSFER != MOTIVE
MOTIVE_CLAIM_WITHOUT_CONTEMPORANEOUS_RECEIPT = HOLD
```

---

## OPPORTUNITY

Opportunity is a bounded capability-and-time question:

```text
IDENTITY_PRESENT
+ REQUIRED_PERMISSION_ACTIVE
+ TARGET_RESOURCE_REACHABLE
+ RELEVANT_TIME_WINDOW
= OPPORTUNITY_CANDIDATE
```

It still does not prove action.

```text
OPPORTUNITY != ACTION
ACTION != INTENT
```

---

## Why Azure?

This question is answered first as architecture, not motive.

Microsoft's documented substrate provides separable surfaces for:

- identity and authentication through Microsoft Entra;
- resource authorization through Azure RBAC;
- billing accounts, profiles, invoice sections, invoices, and cost controls;
- sign-in and audit logs;
- cloud execution and enterprise workload hosting.

The existing Computer Wisdom Microsoft brief independently describes the intended research fit as:

```text
GitHub -> code lineage
Azure -> cloud execution
Entra -> identity and authorization boundaries
Confidential Computing -> attestation surfaces
Replay receipts -> continuity verification
```

This is a design rationale, not proof that any specific workload or account actually used Azure.

---

## Azure vs blockchain

| Question | Azure / Entra | Blockchain |
|---|---|---|
| Login | Account/token/session authentication | Wallet signature or smart-wallet authorization; app may add offchain session |
| Identity | Tenant-managed user/app identity | Address/account is native; human identity requires separate binding |
| Power | Role + scope + policy | Key/smart-wallet/contract permissions + protocol rules |
| Action evidence | Sign-in/audit/activity/resource logs | Transaction, block receipt, events, state transition |
| Billing | Azure billing hierarchy + invoices | Gas/asset movement visible; commercial invoice is offchain unless explicitly bound |
| Revocation | Admin/policy/role/session controls | Key rotation, smart-wallet policy, contract controls; immutable past chain history remains |
| Public replay | Often requires tenant authorization to inspect logs | Ledger transaction history is publicly replayable on public chains |
| Natural-person proof | Directory account may bind organizational identity | Address/signature proves control, not automatically a natural person |
| Motive | Not in logs by default | Not in transaction by default |

Neither substrate proves semantic truth merely because its records are authentic.

---

## Dual Onion Flywheel

```text
CLAIM
  ↓
ROLL DICE
  ↓
SELECT MISSING EDGE
  ↓
FETCH RECEIPT
  ↓
NORMALIZE METADATA
  ↓
REVERSE REPLAY
  ↓
CROSS-COMPARE AZURE <-> BLOCKCHAIN
  ↓
PASS | GAP | CONFLICT | HOLD | FAIL
  ↓
APPEND RECEIPT
  ↓
NEXT QUESTION
```

Flywheel law:

```text
NEW_RECEIPT MAY CHANGE DISPOSITION
OLD_RECEIPT IS NOT SILENTLY DELETED
CORRECTION IS APPEND_ONLY
AUTHORITY_CREATED = FALSE
```

---

## Round 001

Secure random game roll recorded during construction:

```text
SURFACE_DIE        = AZURE
QUESTION_DIE       = WHY_THIS_SUBSTRATE
RECEIPT_DIE        = AUDIT_LOG
DIRECTION_DIE      = CROSS_COMPARE
CITIZEN_ACTION_DIE = COMPARE
```

Evidence-derived disposition:

```text
AZURE_ARCHITECTURE_PATH = SOURCE_BOUND_TO_MICROSOFT_LEARN
COMPUTERWISDOM_MICROSOFT_DESIGN_PATH = SOURCE_BOUND_TO_REPO
ACCOUNT_SPECIFIC_AZURE_AUDIT_LOG = NOT_BOUND
ACCOUNT_HOLDER_IDENTITY = NOT_BOUND
DISPOSITION = HOLD_FOR_ACCOUNT_SPECIFIC_RECEIPT
```

Family-facing or private-family inference is out of scope.

---

## Minimum next receipt

The cleanest Azure-specific next packet is one exported, appropriately redacted account-specific record set containing:

```text
TENANT_ID_OR_STABLE_ALIAS
SUBSCRIPTION_ID_OR_STABLE_ALIAS
RELEVANT_SIGN_IN_EVENT
RELEVANT_AUDIT_OR_ACTIVITY_EVENT
ROLE_ASSIGNMENT_AT_EVENT_TIME
BILLING_SCOPE_ONLY_IF_MONEY_IS_MATERIAL
```

Do not publish secrets, access tokens, passwords, recovery codes, private keys, full payment-card data, or unnecessary personal information.

---

## Official source rails

Microsoft Learn:

- Microsoft Entra sign-in log activity details: https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-sign-in-log-activity-details
- Microsoft Entra monitoring and health / activity logs: https://learn.microsoft.com/en-us/entra/identity/monitoring-health/overview-monitoring-health
- Azure subscription / Microsoft Entra tenant relationship: https://learn.microsoft.com/en-us/entra/fundamentals/how-subscriptions-associated-directory
- Assign Azure subscription Owner role: https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal-subscription-admin
- Elevate Global Administrator access to Azure resources: https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin
- Microsoft Customer Agreement billing roles: https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/understand-mca-roles
- Azure billing account overview: https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/mca-overview

Blockchain comparison:

- Ethereum accounts: https://ethereum.org/developers/docs/accounts/
- Ethereum transactions: https://ethereum.org/developers/docs/transactions/
- Ethereum authentication: https://ethereum.org/developers/docs/ethereum-stack/authentication/
- Base Account typed-data signing: https://docs.base.org/base-account/guides/sign-and-verify-typed-data

---

## Locked state

```text
AMERICAN_CITIZEN != AMERICAN_FAMILY
CITIZEN_RESEARCH = PUBLIC_OR_USER_AUTHORIZED_RECORDS_ONLY
JOY_FAMILY_PRIVACY = SEALED
AZURE_ACCOUNT_HOLDER = NOT_BOUND
AZURE_LOGIN_HOLDER = NOT_BOUND
POWER = REQUIRES_ROLE_AND_SCOPE_RECEIPT
MOTIVE = REQUIRES_DOCUMENTARY_EVIDENCE
OPPORTUNITY = REQUIRES_CAPABILITY_PLUS_TIME_RECEIPT
BLOCKCHAIN_CONTROL = REQUIRES_SIGNATURE_OR_ACCOUNT_CONTROL_RECEIPT
DICE_SELECT_QUESTION = TRUE
DICE_DECIDE_TRUTH = FALSE
AUTHORITY_CREATED = FALSE
```
