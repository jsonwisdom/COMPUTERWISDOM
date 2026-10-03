# LOCAL_STORAGE_PERSISTENCE_PLAN_V0

```text
STATUS                 = EXECUTED
APPROVED_AT            = 2026-10-02 23:25 CDT
EXECUTED_AT            = 2026-10-02 23:26 CDT
CANON                  = false
AUTHORITY_CREATED      = false
COINBASE_MUTATION      = NONE
TOKEN_COPY             = false
MERGE                  = NONE
BRANCH                 = coinbase-e2e-read-2026-10-02
HEAD                   = 75c0d6fe8dd54bbabac28f6bbed11344f0663fd1
DRIVE_FOLDER           = 122IUlDyjfE9E6OKJQupThxK3as8ZbyUw
```

## What is on disk now

One sandbox disk, `/dev/vdc` ext4, mounts `/`, `/tmp`, and `/root`. This is not the user computer. Survival after sandbox teardown is NOT_OBSERVED.

Present:

- `/workspace/artifacts/COINBASE_TEST_06_END_TO_END_RECEIPT.json`
- `/workspace/artifacts/COINBASE_TEST_03_BALANCES.json`
- `/workspace/artifacts/COINBASE_03_BALANCES_CURRENT.json`
- `/workspace/artifacts/COINBASE_04_MARKETS_PRODUCTS.json`
- raw balance dumps under `/workspace/artifacts/.tmp/mcp-results/`
- customer schema copies under `/workspace/artifacts/projects/cwaas/customer/`

Not a Coinbase session store:

- no Coinbase token file
- no Coinbase entry in `/tmp/grok/connectors/index.json`
- no Coinbase-issued session UUID

Do not persist:

- `/tmp/grok/connectors/github.token`
- `/root/.grok/auth.json`
- any refresh token, bearer, or key

## Objects

```text
P1  E2E receipt JSON
P2  balance row JSON
P3  market product JSON
P4  this plan
```

Customer schema is already on branch `customer-receipt-schema-v0-1` and draft PR #603. It is not part of the Coinbase persistence set.

## Gates

```text
LOCAL_COPY_IN_ARTIFACTS     = already true for P1–P3
PERSIST_TO_REPO             = closed until explicit human approval
PERSIST_TO_DRIVE            = closed until explicit human approval
SECOND_SESSION_REREAD       = closed until named
WRITE_PATH                  = closed
```

A file write is not a Coinbase mutation. A repo write is not a customer receipt. A Drive copy is not an independent second source.

## If repo persistence is later approved

Target only, not executed:

```text
jsonwisdom/COMPUTERWISDOM
branch   coinbase-e2e-read-2026-10-02
files    projects/cwaas/coinbase/2026-10-02/
           COINBASE_TEST_06_END_TO_END_RECEIPT.json
           COINBASE_TEST_03_BALANCES.json
           COINBASE_04_MARKETS_PRODUCTS.json
           LOCAL_STORAGE_PERSISTENCE_PLAN_V0.md
base     master
merge    NONE until a separate seal
```

Receipt header to add at write time, not before:

```text
SOURCE_DISK        = sandbox /dev/vdc
SOURCE_SESSION     = bd53a4ba-a923-50a5-80d4-b766882e0ced
PORTFOLIO_UUID     = 09bcd23b-4b26-50ea-8bee-f4f107657834
RETRIEVAL_WINDOW   = 2026-10-02 23:15 CDT
CROSS_SESSION      = NOT_CLAIMED
TOKENS_INCLUDED    = false
```

## If Drive persistence is later approved

One file per object. No token file. Record Drive file id after the write. Search miss before the write stays a scoped negative.

## What persistence still will not prove

```text
portfolio UUID stability in a later session
Coinbase token expiry or refresh
USDC-USD negative outside this session
write path
independent second source
```

Those remain separate transitions. This plan does not authorize them.
