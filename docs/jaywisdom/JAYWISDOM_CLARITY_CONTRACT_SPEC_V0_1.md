# JAYWISDOM CLARITY Contract Specification V0.1

## Holding

The fastest wise path is not to make `$JWIS` the thing customers must speculate on before Jay earns money.

```text
CUSTOMER_PAYS_FOR_CLARITY
JAY_EARNS_ON_FULFILLMENT
JWIS_REWARDS_COMPLETED_SERVICE
REPLAY_PROVES_PROCESS_CONTINUITY
```

## Why stablecoin pricing comes first

The product ladder is denominated in dollars. V0.1 accepts a six-decimal USD payment token supplied at deployment. This removes the incorrect assumption that `1e18 wei` equals one dollar and avoids an oracle dependency in the first revenue test.

## Roles

- **Owner:** changes administrative configuration through an explicit transaction.
- **Treasury:** receives settled service revenue.
- **Fulfiller:** commits the CLARITY result produced by Jay's approved human/AI workflow.
- **Customer:** creates an order and retains the refund right until valid fulfillment.
- **Independent replayer:** recomputes the declared replay hash without receiving authority.

```text
OWNER_CONTROL != LEGAL_AUTHORITY
FULFILLER_COMMITMENT != TRUTH
REPLAY_MATCH != VERDICT
```

## Order lifecycle

```text
NONE
→ PAID
→ FULFILLED
```

or:

```text
NONE
→ PAID
→ REFUNDED_AFTER_DEADLINE
```

## CLARITY commitment

Every fulfillment binds seven nonzero hashes:

```text
C = controllingAuthority
L = lawfulPurpose
A = responsibleActor
R = requiredEvidence
I = instrumentsEnablements
T = trackingCustody
Y = remedyAppeal
```

The underlying human-readable documents remain off-chain. Their exact bytes should be content-addressed; the contract records their commitments and receipt-reference hashes.

## Revenue rule

```text
PAID_ORDER + VALID_CLARITY + AUTHORIZED_FULFILLER
→ TREASURY_SETTLEMENT + RECEIPT + OPTIONAL_JWIS_REWARD
```

The JWIS cap must never block paid service delivery. If the cap is exhausted, fulfillment still settles revenue and records the receipt, while the reward amount becomes zero.

## RePlay rule

The replay hash binds:

- chain ID and contract address;
- order ID and customer;
- product type and question hash;
- rubric version;
- all seven CLARITY dimensions;
- result and URI hashes;
- finding state.

Exact inputs reproduce `MATCH`; any changed bound input produces `DIVERGE`.

## Mainnet gate

Base mainnet deployment is prohibited until:

1. Foundry compilation and fixtures pass;
2. contract-specific review is complete;
3. treasury, owner, and fulfiller addresses are verified;
4. the payment token address is verified from an official source;
5. refund behavior is tested on Base Sepolia;
6. frontend delivery and customer disclosures exist;
7. token/legal review is completed for the intended jurisdiction;
8. deployment and source verification receipts are generated.
