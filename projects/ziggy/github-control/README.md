# Ziggy GitHub Control

GitHub is the publication and change-control transport for Ziggy's public repository. It is not the system identity and does not create authority.

System identity:

`jsonwisdom/COMPUTERWISDOM`

## Control path

`NATURAL_LANGUAGE → SANDBOX BRANCH → PR → REQUIRED CHECKS → HUMAN MERGE → MASTER`

## Rules

- Ziggy-generated changes begin outside protected `master`.
- Every proposal names the exact files it intends to change.
- Existing unrelated work must not be staged or overwritten silently.
- Required repository checks must pass on the current PR head before merge.
- A merge records publication state only; it does not prove ENS control or submit a blockchain transaction.
- GitHub identity, ENS identity, wallet identity, and release authority remain distinct fields in receipts.

## Launch boundary

A merge into `master` may make a launch artifact public through GitHub Pages, but:

`MERGED ≠ SIGNED ≠ TRANSACTED ≠ ATTESTED`

## Natural-language control

A human may instruct Ziggy in plain language to create a branch, propose files, or prepare a test run. Ziggy must convert that request into a bounded GitHub diff and surface any unresolved identity/network gaps before promotion.

`authority_created=false`
