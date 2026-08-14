# Ziggy Natural Language

Natural language is an **intent surface**, not an authority surface.

## Input shape

A human may say or type requests such as:

- create a Ziggy launch candidate
- bind this receipt to an ENS name
- run this manifest on Base Sepolia
- open a GitHub proposal

Ziggy must convert the request into an explicit intent record before any write or chain action.

## Intent states

`HEARD → PARSED → GAP_CHECKED → HUMAN_CONFIRMED → PROPOSED`

No state after `PARSED` may be skipped silently.

## Required fields

- original human text
- normalized intent
- requested target
- requested network, if any
- referenced ENS name/address, if any
- missing information
- proposed GitHub scope
- whether a signature or transaction would be required
- `authority_created=false`

## Creation rule

Natural language can create **candidate files, manifests, branches, and PR proposals** inside the imagination/GitHub lanes.

Natural language alone cannot:

- prove ENS ownership
- prove wallet control
- merge protected branches
- submit a chain transaction
- alter BoxD originals
- promote a testnet result to mainnet

## Replay rule

The original human wording must remain recoverable alongside the normalized intent so later replay can distinguish what the human actually said from what Ziggy interpreted.
