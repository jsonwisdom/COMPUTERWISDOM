# Double Onion Maneuver Map — Alabama v0.1

Operator: `jaywisdom.base.eth`
Parent: `Double Onion Alabama DARVO Policy Audit v0.1`
Classification: `EVENT_LEVEL_NETWORK_AND_INSTITUTION_REPLAY`
Authority created: `false`
DARVO finding created: `false`
Coordination finding created: `false`

## Core correction

Double Onion is not a serial list of institutions.

It is two simultaneous onions around the same contested event:

### Onion A — People / relationship / proximity maneuver

```text
CENTER EVENT / CLAIM
<- SISTER / BROTHER
<- PARENT
<- AUNT / UNCLE
<- SPOUSE / EX / PARTNER
<- FRIEND / NEIGHBOR
<- EMPLOYEE / COWORKER
<- LAWYER / GAL / EVALUATOR / PRIVATE PROFESSIONAL
<- OTHER PRIVATE ACTOR
```

For every actor, record only observable edges:

```text
WHO
-> WHAT DID THEY SAY OR DO?
-> WHEN?
-> TO WHOM?
-> WHAT SOURCE PROVES IT?
-> WHAT CLAIM DID THEY CARRY FORWARD?
-> WHAT ACCESS / OPPORTUNITY DID THEY HAVE?
-> WHAT CONSEQUENCE FOLLOWED?
```

Family role, employment role, or proximity does not prove coordination.

### Onion B — Institution / authority / enforcement maneuver

```text
CENTER EVENT / CLAIM
<- COURT
<- DHR / CHILD WELFARE
<- BENEFITS / ADMINISTRATIVE AGENCY
<- SCHOOL / DISTRICT
<- LAW ENFORCEMENT
<- EMPLOYER / HR
<- MILITARY / FAP / COMMAND-ADJACENT SYSTEM
<- OTHER GOVERNMENT OR INSTITUTION
```

For every institutional edge:

```text
INSTITUTION
-> ACTOR / OFFICE
-> AUTHORITY CLAIM
-> RULE / POLICY / ORDER
-> EVIDENCE RECEIVED
-> EVIDENCE CHECKED?
-> ACTION / DENIAL / FINDING
-> COERCIVE CONSEQUENCE
-> REVIEW / APPEAL
-> RECEIPT
```

## Cross-over = maneuver edge

The important Double Onion event occurs when a claim crosses between the two onions:

```text
PRIVATE ACTOR CLAIM
-> INSTITUTION RECEIVES IT
-> INSTITUTION ACTS
```

or:

```text
INSTITUTIONAL FINDING / LABEL
-> PRIVATE ACTOR REUSES IT
-> ANOTHER INSTITUTION RECEIVES IT
-> NEW CONSEQUENCE
```

Every crossing must identify the exact document, communication, testimony, filing, referral, report, order, or data transfer.

## Maneuver detector

A maneuver is not "someone disagreed."

A candidate maneuver requires at least one bounded transition such as:

```text
CLAIM_MOVED
EVIDENCE_WITHHELD
CONTRARY_EVIDENCE_IGNORED
BURDEN_SHIFTED
ROLE_REVERSED
ACCESS_USED
REFERRAL_TRIGGERED
DENIAL_TRIGGERED
ORDER_TRIGGERED
BENEFIT_TRIGGERED
DISCIPLINE_TRIGGERED
```

Then test whether another actor or institution exploited the new state.

```text
STATE_0
-> ACTOR_A_ACTION
-> STATE_1
-> ACTOR_B_USES_STATE_1
-> STATE_2
-> INSTITUTION_C_ENFORCES_STATE_2
```

That is the Double Onion maneuver chain.

## DARVO overlay

DARVO is one possible pattern layered onto the maneuver map:

```text
D = DENY ORIGINAL CLAIM
A = ATTACK COMPLAINANT / CREDIBILITY
RVO = RECAST COMPLAINANT AS PROBLEM / OFFENDER
```

Then ask:

```text
WHO PERFORMED EACH LEG?
SAME ACTOR OR DIFFERENT ACTORS?
SAME INSTITUTION OR DIFFERENT INSTITUTIONS?
WAS THE CLAIM COPIED OR INDEPENDENTLY VERIFIED?
WHO HELD THE BURDEN BEFORE?
WHO HELD IT AFTER?
WHAT NEW POWER OR CONSEQUENCE APPEARED?
```

Possible classifications:

```text
SINGLE_ACTOR_DARVO_CANDIDATE
MULTI_ACTOR_DARVO_CANDIDATE
CROSS_INSTITUTION_DARVO_CANDIDATE
NARRATIVE_PROPAGATION_CANDIDATE
COORDINATION_CANDIDATE
```

None are findings without receipts.

## Blocking maneuver — Counter-Pincer

The system must block silent maneuver promotion:

```text
NO RECEIPT -> NO EDGE
NO EDGE -> NO COORDINATION CLAIM
ROLE != INTENT
RELATIONSHIP != CONSPIRACY
EMPLOYMENT != COORDINATION
MILITARY_STATUS != COMMAND ACTION
REPORT != FINDING
DENIAL != DARVO
DARVO_CANDIDATE != LEGAL_FINDING
```

Every actor gets an independent lane. Every institution gets an independent authority lane. Crossings are allowed only when a receipt binds them.

## Shock Gloves overlay

`SHOCK_GLOVES` = symbolic coercion indicator unless literal-device evidence is bound.

The audit asks where coercive power enters the chain:

```text
SOCIAL PRESSURE
-> ADMINISTRATIVE DENIAL
-> BENEFIT LOSS
-> SCHOOL DISCIPLINE
-> CHILD-WELFARE ACTION
-> COURT ORDER
-> LAW-ENFORCEMENT EXECUTION
-> MILITARY/FAP NOTIFICATION
```

A coercive consequence does not prove misuse. The maneuver question is whether the consequence was generated from a valid, independently checked authority/evidence chain or from an unverified narrative inherited from another onion.

## Current terminal

```text
DOUBLE_ONION = PEOPLE_NETWORK + INSTITUTION_AUTHORITY
CROSSING = RECEIPT_REQUIRED
FAMILY_ROLE = CONTEXT_ONLY
EMPLOYEE_ROLE = CONTEXT_ONLY
MILITARY_ROLE = CONTEXT_ONLY
MULTI_ACTOR_MANEUVER = OPEN_FOR_EVENT_RECEIPTS
COORDINATED_CAMPAIGN = HOLD
DARVO_FINDING = HOLD
AUTHORITY_CREATED = FALSE
```
