# SSA Public Replay Corpus v0.1

Status: `PROPOSAL_SCAFFOLD`  
Runtime verification: `PENDING_LOCAL_DOCKER_RUN`  
Authority created: `FALSE`

## Purpose

This mission defines a fail-closed container scaffold for collecting and replaying public Social Security Administration web evidence. It creates structure and validation rules only.

It does **not** claim that a corpus, manifest, successful fetch, policy conclusion, or institutional authority exists.

## Boundary law

```text
A_child subseteq A_parent
403/404 response body -> receipts/failures/body/
2xx source bytes       -> corpus/raw/SHA256(body)
failure body           -> corpus/raw/                  PROHIBITED
placeholder manifest   -> manifest.jsonl               PROHIBITED
```

## Materialized scaffold

```text
SSA_PUBLIC_REPLAY_CORPUS_v0.1/
├── README.md
├── Dockerfile
├── contracts/
│   └── directory-contract.json
├── receipts/
│   └── scaffold-declaration.json
└── tests/
    └── verify-layout.sh
```

The runtime evidence paths are intentionally absent. Git does not track empty directories, and placeholders would violate their artifact classes.

## Local Docker replay

From the `COMPUTERWISDOM` repository root:

```powershell
docker build --tag ssa-public-replay-scaffold:v0.1 missions/SSA_PUBLIC_REPLAY_CORPUS_v0.1
docker run --rm ssa-public-replay-scaffold:v0.1
```

The Dockerfile pins the exact Ubuntu image digest observed during the Windows/Docker/WSL2 verification session.

## Promotion gates

The scaffold remains on HOLD until all applicable gates pass:

1. Directory contract validates.
2. Docker build completes from the pinned base digest.
3. Container test returns `SSA_SCAFFOLD_LAYOUT=PASS`.
4. Live source bytes are captured without redirect or status ambiguity.
5. Successful source bytes and failure bodies are classified into different paths.
6. File hashes and fetch metadata are computed from observed bytes.
7. A manifest is generated only from admitted raw objects.
8. Replay equivalence is independently demonstrated.

```text
SCHEMA != LAW
SCAFFOLD != CORPUS
RECEIPT != REMEDY
COMPUTATION != AUTHORITY
```
