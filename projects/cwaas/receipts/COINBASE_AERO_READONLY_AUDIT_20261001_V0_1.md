# Coinbase preview and Aerodrome audit — 2026-10-01

Record ID: COINBASE_AERO_READONLY_AUDIT_20261001_V0_1
Status: REVIEW_ONLY / PARTIAL_SOURCE_BINDING
Scope: preserve the conversation's read-only preview report and separate current protocol documentation from proposed Aero mechanics.
This is a research record, not a trade execution receipt or investment-quality verdict.

## Provenance and privacy

Coinbase findings below were supplied as pasted connector reports in the conversation. This writer did not replay Coinbase calls or receive raw Coinbase responses. Reported PASS is not promoted to independently verified PASS.
Private account balances, portfolio identifiers, and request identifiers are intentionally omitted from this repository-backed record.
The Aerodrome documentation was retrieved in this conversation at https://aerodrome.finance/docs. No immutable page capture or source-byte hash is attached. Search/retrieval excerpts are not an onchain binding.
Merger and sAERO details below are user-supplied summaries of purported primary pages; exact URLs, page captures, contract parameters, and hashes are absent.

## Budget preserved

| Proposed allocation | USDC |
| --- | ---: |
| AERO | 5 |
| BNKR | 5 |
| EDGE | 5 |
| Unallocated | 35 |
| Total designated budget | 50 |

Three allocations total 15 USDC (30%); unallocated amount is 35 USDC (70%).
This is a designated 50 USDC envelope. A starting 50 USD budget requires separately established conversion economics. USD and USDC are not silently equated.

## Reported Coinbase previews

| Product | Total estimated debit, USDC | Commission included, USDC | Amount toward tokens, USDC | Estimated base quantity | Average fill |
| --- | ---: | ---: | ---: | ---: | ---: |
| AERO-USDC | 5 | 0.0445986124876114965 | 4.9554013875123885 | 6.1369479826029308 | 0.80747 |
| BNKR-USDC | 5 | 0.0445986124876114965 | 4.9554013875123885 | 12086.3448475911914634 | 0.00041 |
| EDGE-USDC | 5 | 0.0445986124876114965 | 4.9554013875123885 | 45.1434944658138699 | 0.10977 |

Exact arithmetic from reported decimal strings:
- Three debits: 15 USDC.
- Commission sum: 0.1337958374628344895 USDC.
- Token-value sum: 14.8662041625371655 USDC.
- Per-preview token value plus commission: 4.9999999999999999965 USDC, differing from 5 by 0.0000000000000000035 USDC (decimal representation discrepancy).
Earlier connector summary rounded these totals; do not treat the rounded strings as different economic events.

The report states sufficient available USDC, no preview errors/warnings, and insufficient USD. Balance verification remains reported, not replayed.
No provider preview timestamp or locked quote ID was reported. Responses were reportedly captured before 2026-10-01T08:07:22Z; a request start time was not supplied. This is a host capture bound, not a Coinbase timestamp.
Base quantities remain estimates. Base increments are not assumed to reduce quote-sized fills.
Commission is reported inside the 5 USDC debit. Later withdrawals are separate unquoted actions; their fees are UNKNOWN and are not automatically assigned to an in-account spot purchase.
The remaining seven pictured projects have no resolved Coinbase preview in this record. HOLD / UNAVAILABLE is not a claim that no token exists elsewhere.

## Current Aerodrome documentation

Retrieved documentation distinguishes liquid ERC-20 AERO from veAERO, an NFT representing a locked position.
Liquid ownership alone does not provide voting participation or the veAERO exchange-revenue stream. Locking and voting are separate actions; this audit performed neither.
Locks can run from one week to four years. Four-year locking provides a 1:1 initial voting-power ratio; shorter remaining terms reduce power proportionately.

Documentation describes exchange revenue as:
- Swap fees from staked liquidity.
- A percentage of swap fees from unstaked liquidity.
- Voting incentives.
- Ignition launch payments.

A 10% default take on certain unstaked emissions-eligible Slipstream fees is reported in the documentation. This is not a universal take across all liquidity.
Protocol revenue cannot be compared with another provider's fee/revenue series until components, chains, dates, and measurement conventions match.

The docs describe seven-day epochs starting Thursday 00:00 UTC; voting closes Wednesday 23:00 UTC. Votes direct the next epoch's pool emissions.
Detailed fee and incentive payment timing in the supplied narrative is not independently replayed here.

## Emissions wording collision preserved

The supplied follow-up identifies approximately 10.9% annualized emissions, 1.88B total supply, and approximately 51% locked as April 2026 snapshots.
The independently retrieved documentation also contains later policy wording describing emissions held at approximately 10.92% per year heading toward Aero.
These are distinct statements. Do not silently erase either or infer that the October onchain rate was measured.
OCTOBER_LIVE_EMISSIONS_RATE = UNKNOWN.
An initial growth/decay schedule does not establish current policy.
The supplied rebase mechanism remains reported pending separate source binding.

## Proposed Aero migration — claim register

| Claim | Reported primary context | State in this record |
| --- | --- | --- |
| Aerodrome and Velodrome plan to merge in 2026 into Aero on MetaDEX03 | Retrieved Aerodrome docs | DOCUMENTED_PLAN; completion unverified |
| Token ticker remains AERO; existing token/NFT positions require upgrade | Reported May 8 FAQ | HOLD; source object not attached |
| 94.5% AERO community / 5.5% VELO community | Reported Foundation Paragraph post and launch update | HOLD |
| 52-week revenues of 260M versus 15M underpin allocation | Same reported announcement | HOLD; definitions and denominator not bound |
| Q2, then September, then October 21, 2026 launch targets | Reported dated project pages | SEQUENCING_UNRESOLVED / HOLD |
| Seven launch chains: Base, Ethereum, OP Mainnet, Arc, Ink, Robinhood Chain, Arbitrum | Reported September 25 launch update | HOLD |
| 20% global annual inflation ceiling; 8–12% expected realized rate | Reported June 7 AER Engine post | DESIGN_INTENT / HOLD |

Different announced target dates may represent revisions. A contradiction verdict requires exact dated source objects and supersession context.
A community allocation split does not establish a per-token conversion ratio.
Neither an announcement nor a liquid Coinbase preview proves a completed migration, deployed rules, or centralized-exchange migration support.

## Proposed sAERO / Predictive Allocation / Gauge Caps

The supplied narrative describes sAERO as an NFT stake replacing epoch voting with persistent pool allocations and simultaneous reward/revenue streams.
Reported design: an initial per-position 48-hour reallocation wait, term commitment without early exit, transferable NFTs, no planned splitting, removal of rebase, and optional Autopilot.
All remain proposed mechanics in this record; deployment and live availability were not verified.

Reported Gauge Caps limit dollar-valued pool rewards by projected revenue, under a global inflation ceiling. The revenue multiple is unspecified; the expected 48-hour recalibration is not a bound live parameter.
Projected revenue, allocation weights, price inputs, oracle policy, cap recalibration authority, and deployed contract implementation are not independently established here.
The reported dedicated AER Engine FAQ returning 404 is a retrieval outcome, not proof the design is invalid or absent.
No sAERO position, lock, vote, cap-setting action, upgrade, approval, or transfer was performed.

## Frozen reporting state

PREVIEW_CHECK = PASS_AS_REPORTED
INDEPENDENT_COINBASE_REPLAY = NOT_RUN
PRICE_LOCK = NONE
OTHER_SEVEN = HOLD / UNAVAILABLE
ALLOCATION_CHANGE = NONE
ORDER_EXECUTED = FALSE_AS_REPORTED
THIS_WRITER_ORDER_ACTION = NONE
CONVERSION_EXECUTED = FALSE_AS_REPORTED
SOURCE_BINDING = PARTIAL
ONCHAIN_BINDING = NONE
IDENTITY_BINDING = NONE
FACTUAL_PROMOTION_FROM_SATIRE_OR_LOGOS = NONE

## Next evidentiary events

Preserve raw Coinbase responses with capture times; bind each announcement to its exact URL and immutable bytes; record supersession relationships; inspect deployed contracts and dated onchain parameters separately.
GitHub and Drive copies preserve this record. Copying, hashing, or publishing it does not independently verify the underlying claims.
