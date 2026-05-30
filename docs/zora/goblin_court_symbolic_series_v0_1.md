# Goblin Court — Symbolic Coin Series Concept (Candidate v0.1)

**System Identity:** DeepSeek (candidate_generator)  
**Reversibility Class:** SYMBOLIC  
**Authority:** false  
**Receipt Required Before Publication:** true  

## Series Concept

The Goblin Court operates on verifiable narrative weapons. A coin series would externalize its internal metrics such as Assumption Density, Receipt Density, and Meme Potential as tradable, collectible symbols.

## Example Coins (Speculative)

- **TITAN_OF_ASSUMPTIONS** — coin representing high assumption density; mechanics TBD.
- **RECEIPT_KING** — minted only after a verified receipt exists.
- **GOBLIN_GATE** — requires a prior acquisition receipt to mint.

## Contract Design Candidates

Each coin would be a standard Zora Creator Coin with metadata pointing to a Goblin Court JSON schema. Metadata would include fields such as:

- `assumption_density_score`
- `receipt_density_score`
- `meme_potential_score`
- `reversibility_class: SYMBOLIC`

**Note:** No contract deployed. No metadata hashes exist. This is symbolic design only.

## Economic Speculation (Flagged)

Potential mechanisms:

- Bonding curve proceeds fund Goblin Court operations.
- Holding certain coins grants voting weight in symbolic disputes.
- Coins can be burned to produce `attestation_receipts`.

## Relation to Factory

The series would be deployed via Zora Factory, with each deployment generating a `replay_acquisition_receipt` in `receipts/zora_factory/`. Goblin Court would consume those receipts for symbolic interpretation — never the reverse.

## Known Gaps

- No coins have been deployed.
- All economic and governance mechanics are speculative.
- Goblin Court is not a legal entity.

## Missing Receipts

- No acquisition receipts exist for any Goblin Court coin.
- No metadata snapshot has been frozen.
