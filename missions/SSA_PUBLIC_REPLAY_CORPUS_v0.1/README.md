# SSA Public Replay Corpus v0.1

Status: `PROPOSAL_SCAFFOLD`  
Synthetic router gate: `v0.2`  
Reverse audit: `CRISSCROSS_APPLESAUCE_v0.1`  
Live fetch: `PROHIBITED_UNTIL_SYNTHETIC_MATRIX_PASS`  
Authority created: `FALSE`

## Purpose

This mission defines a fail-closed container scaffold and a synthetic HTTP observation router for collecting and replaying public Social Security Administration web evidence.

It does **not** claim that a production corpus, manifest, successful live fetch, policy conclusion, or institutional authority exists.

## Boundary law

```text
A_child subseteq A_parent
200 + transport OK + zero redirects -> corpus/raw/SHA256(body)
403/404 response body                -> receipts/failures/body/SHA256(body)
redirect status or redirect history  -> HOLD
network failure                      -> failure receipt
failure or ambiguous body            -> corpus/raw/                  PROHIBITED
placeholder manifest                 -> manifest.jsonl               PROHIBITED
```

Only an exact HTTP `200` is admitted by Router Gate v0.2. Every unlisted status fails closed.

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
    ├── route-http-observation.sh
    ├── verify-layout.sh
    ├── verify-router-matrix.sh
    └── verify-reverse-audit.sh
```

The production runtime evidence paths are intentionally absent. Router tests create synthetic artifacts only below a temporary directory and remove that directory on exit.

## Synthetic routing matrix

`verify-router-matrix.sh` performs no network operation and tests:

| Observation | Required decision |
|---|---|
| `200`, no redirects | exact body bytes at `corpus/raw/SHA256(body)` |
| `403` | exact body bytes at `receipts/failures/body/SHA256(body)` |
| `404` | exact body bytes at `receipts/failures/body/SHA256(body)` |
| `3xx`, or final `200` with redirect history | `HOLD_REDIRECT_AMBIGUITY` |
| network failure | `receipts/failures/network/` receipt |

Every case asserts that no manifest is created. Every non-admission case asserts that no corpus object is created.

## CrissCross AppleSauce reverse audit

`verify-reverse-audit.sh` runs synthetic `403` and `404` observations over identical body bytes, then audits the resulting custody tree backward instead of trusting the forward labels.

The current receipt schema preserves the `HTTP_FAILURE` class and content-addressed failure body, but it does not preserve the upstream HTTP status. Therefore a reverse audit can prove **failure class**, but cannot prove **403 versus 404** from current stored evidence alone. Human-selected case IDs are labels, not evidence.

```text
FAILURE_CLASS_RECOVERABLE=TRUE
HTTP_STATUS_403_VS_404_RECOVERABLE=FALSE
CRISSCROSS_APPLESAUCE=HOLD_EXACT_STATUS_IDENTITY
MACOS_OBSERVATION_CREATED=FALSE
```

No macOS observation is synthesized by this test. Cross-platform equivalence remains unproven until independently observed bytes and transport metadata exist.

## Local Docker replay

From the `COMPUTERWISDOM` repository root:

```powershell
docker build --tag ssa-public-replay-scaffold:v0.2 missions/SSA_PUBLIC_REPLAY_CORPUS_v0.1
docker run --rm ssa-public-replay-scaffold:v0.2
```

The Dockerfile pins the exact Ubuntu image digest observed during the Windows/Docker/WSL2 verification session. The container runs the scaffold validator, synthetic router matrix, and reverse audit. It does not fetch SSA bytes.

## Promotion gates

The live-fetch gate remains on HOLD until:

1. Directory contract validates.
2. Docker build completes from the pinned base digest.
3. Container reports `SSA_SCAFFOLD_LAYOUT=PASS`.
4. Container reports `SSA_SYNTHETIC_ROUTER_MATRIX=PASS`.
5. Container reports `SSA_REVERSE_AUDIT=PASS` while exact-status identity remains explicitly held.
6. Operator independently confirms the container made no live SSA request.

After that gate, any future live observation must still classify bytes before a manifest can exist.

```text
SCAFFOLD != CORPUS
SCHEMA != LAW
RECEIPT != REMEDY
COMPUTATION != AUTHORITY
```
