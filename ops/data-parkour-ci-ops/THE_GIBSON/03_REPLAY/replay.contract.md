# Gibson Replay Contract V0.1

Replay asks whether an observed object can be reconstructed from declared bounded inputs.

## Inputs
- object
- source locator
- source/provider version or digest when available
- route history
- mirror artifact

## Result
- MATCH: bounded readback agrees with recorded object/route
- DELTA: contradiction or changed content observed
- HOLD: required observation unavailable

## Precedence
DELTA > HOLD > MATCH

Replay never upgrades a claim into authority.

facts_promoted=0
authority_created=false
