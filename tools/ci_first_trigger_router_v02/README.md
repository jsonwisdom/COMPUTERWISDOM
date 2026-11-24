# Computer Wisdom CI-FIRST Trigger Router v0.2 — standalone, read-only

**Status: candidate implementation; NOT merged, activated, deployed, or granted authority.**

This is a deterministic navigation receipt builder. It does **not** control thoughts or actions. It labels exact trigger phrases to select **research lanes only**, not people or permission scopes. It complements the current ERS replay kernel; it does not replace it.

`Giant Replay` -> ComputerWisdom replay; `OODA` -> observe/orient/decide/act; `ENS Emergency` -> ENS label/incident inspection, no wallet writes; `Super Secret Sister Sidecars` -> JOY preserve/continue/route, private by default; `LeahPrime` -> synthetic cluster review, independent of the content truth axis; `Jason Auth` -> request human review, **no identity proof or automatic authority**. Trigger vocabulary is fixed, versioned and deterministic.

## CI-FIRST

From the `tools/ci_first_trigger_router_v02` directory:

```bash
python -m unittest discover -s tests -v
python -m cw_router 'Giant Replay OODA Super Secret Sister Sidecars LeahPrime JASON Auth' --records fixtures/public_metadata.json
```

The fixture consists of **synthetic placeholder digests**, not verified GitHub or Cloudflare content. Output contains `routing`, `metadata_integrity`, `content_truth`, `source_authenticity` as separate fields. Input data is read-only. No remote fetches, signatures, family identity inference, wallet calls, webhook calls, or commits.

Metadata `sha256` records are **recorded-only** (not independently verified); same-instant conflicting hashes on one object are reported as integrity FAIL. Object IDs are hashed in the output to avoid leaking paths or identities. The query itself is not returned, only its digest and matched routing vocabulary. The system does not echo private sidecar messages.

This implementation purposely avoids coupling to any real-person or family account. `Sister Sidcars` is a separate JOY family rail from `LeahPrime`, per its documented boundaries. No gender, familial relationship, legal authority, official or military affiliation, consent or secret status is inferred.

Wolfram is used to independently validate fixed mathematical safety invariants, not to claim semantic content truth. Existing Cloudflare infrastructure is observed but not changed.

## Release gates

1. Review this candidate in a draft PR; run unit tests on the exact commit.
2. Independently reproduce output digest from identical bounded inputs.
3. Scope external connector ingestion, separate private storage, and exact source permissions.
4. Only with human approval: link to a real data ingestion runtime, merge, deploy, or authorize mutations.

**Invariants:** `authority_created=false`, `consent_created=false`, `system_mutations=0`, `external_calls=0`, `publication=NONE`, `SISTER_SIDECAR.terminal_hold=false`, `content_truth!=routing_status`.