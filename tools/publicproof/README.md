# PublicProof — Minnesota Round 001

**Mode:** `QUANTUM_PUBLIC_PROOF_PRIORITY_PERFECT_PRESS`

PublicProof is a nonpartisan, replayable evidence game for viral political claims. A player name is a case label, not an accusation. Party, office, popularity, and virality do not change evidence scores.

> PARTY != PROOF  
> VIRALITY != PROOF  
> OFFICE != PROOF  
> ACCUSATION != PROOF  
> REPLAYABLE_EVIDENCE -> SCORE

## Player 1

`PEGGYPLAYER1` is the first Minnesota case because the August 11, 2026 unofficial statewide results show Peggy Flanagan leading the DFL U.S. Senate primary with 411,541 votes (59.02%), with 100% of precincts reporting. Minnesota's results site expressly states that state and federal results remain unofficial until the State Canvassing Board certifies them on August 18, 2026.

The satirical wrapper `Flanagan Shenanigans` is presentation only. It creates **zero evidentiary weight** and is not a claim of misconduct.

## Cards

Every round may contain:

- Claim Card
- Source Card
- Law Card
- Video Receipt
- Counterevidence
- Public Verdict

## Evidence weights

| Evidence type | Points |
|---|---:|
| Primary government record | +100 |
| Full original video | +80 |
| Independent corroboration | +60 |
| Complete contextual quote | +40 |
| Campaign/party assertion | +10 |
| Cropped viral clip | 0 |
| Unsupported accusation | -50 |
| Proven fabrication | -100 |

Weights grade evidence objects, not people or parties.

## Round 001 — polling-place sting

Initial claim states:

- `CLAIMED_STING = HOLD`
- `NO_ID_ACTIVE_VOTER = VERIFIED`
- `8_PERSON_VOUCHING = VERIFIED`
- `VOUCH_PROVES_CITIZENSHIP = FALSE`
- `IMPERSONATION_OCCURRED = VIDEO_NEEDED`
- `ILLEGAL_BALLOT_CAST = NOT_PROVEN`
- `PEGGY_INVOLVEMENT = NOT_ESTABLISHED`

The fixture in `fixtures/publicproof/MN_2026_ROUND_001.json` carries the replayable claim/evidence state. `publicproof.py` computes evidence totals and rejects party-based scoring fields.

## Primary sources

- Minnesota Secretary of State — 2026 U.S. Senate primary results: https://electionresults.sos.mn.gov/Results/Index?ErsElectionId=200&electionDate=08%2F11%2F2026+00%3A00%3A00&officeInElectionIdList=-1&officeInElectionIdList=38485&scenario=USSenate
- Minnesota Secretary of State — current/active voters do not need ID at sign-in: https://www.sos.mn.gov/elections-voting/election-day-voting/do-i-need-to-bring-id/
- Minnesota Secretary of State — Election Day registration/vouching: https://www.sos.mn.gov/elections-voting/register-to-vote/register-on-election-day/
- Minnesota Statutes §201.061 subd. 3 — registered precinct voter may vouch for residence for up to eight voters: https://www.revisor.mn.gov/statutes/?id=201.061

## Guardrails

1. A claim does not become true because a source exists; the source must actually support it.
2. Vouching under §201.061 is evidence of **residence**, not a substitute for legal voter eligibility or citizenship.
3. `VIDEO_NEEDED` means the claimed event is not scored as established until the original evidence can be replayed.
4. `NOT_PROVEN` and `NOT_ESTABLISHED` must never be rendered as guilt.
5. Any candidate, campaign, election official, journalist, activist, or citizen is evaluated by the same evidence weights.
