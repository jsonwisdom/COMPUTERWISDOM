#!/usr/bin/env python3
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

UID = "0x23b3b97514fa232cfdbcdee7a5031ff11a5fcd36aa874a5f4067805cd0ad6c84"
DECLARED_SCHEMA_UID = "0x244c84adef25091c97090e6e3f0b1bb932fc7022b913b7546406f4213a202cab"
DECLARED_TX_HASH = "0x4cef493d67d8744d2458fd82c169aa872b14cfe2ecaf13f03329b57bd93acc35"
EASSCAN_GRAPHQL = "https://base-sepolia.easscan.org/graphql"
BASE_SEPOLIA_RPC = "https://sepolia.base.org"
CHAIN_ID_EXPECTED = "0x14a34"  # 84532


def post_json(url, payload, timeout=30):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"content-type": "application/json", "user-agent": "COMPUTERWISDOM-BoxD-Replay/0.1"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return {"http_status": resp.status, "json": json.loads(raw), "raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = None
        return {"http_status": e.code, "json": parsed, "raw": raw, "error": "HTTPError"}
    except Exception as e:
        return {"http_status": None, "json": None, "raw": None, "error": f"{type(e).__name__}: {e}"}


def rpc(method, params, ident):
    return post_json(BASE_SEPOLIA_RPC, {"jsonrpc": "2.0", "id": ident, "method": method, "params": params})


def main():
    observed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    query = """query Attestation($uid: String!) {
  attestation(where: { id: $uid }) {
    id
    attester
    recipient
    refUID
    revocable
    revocationTime
    expirationTime
    data
  }
}"""
    eas = post_json(EASSCAN_GRAPHQL, {"query": query, "variables": {"uid": UID}})
    chain_id = rpc("eth_chainId", [], 2)
    tx = rpc("eth_getTransactionByHash", [DECLARED_TX_HASH], 3)
    receipt = rpc("eth_getTransactionReceipt", [DECLARED_TX_HASH], 4)

    eas_json = eas.get("json") if isinstance(eas.get("json"), dict) else {}
    gql_errors = eas_json.get("errors")
    attestation = (eas_json.get("data") or {}).get("attestation") if not gql_errors else None

    chain_result = ((chain_id.get("json") or {}).get("result") if isinstance(chain_id.get("json"), dict) else None)
    tx_result = ((tx.get("json") or {}).get("result") if isinstance(tx.get("json"), dict) else None)
    receipt_result = ((receipt.get("json") or {}).get("result") if isinstance(receipt.get("json"), dict) else None)

    if eas.get("http_status") != 200 or gql_errors:
        uid_status = "HOLD_QUERY_ERROR"
    elif attestation is None:
        uid_status = "NOT_FOUND_IN_EASSCAN_INDEXER"
    else:
        uid_status = "FOUND_IN_EASSCAN_INDEXER"

    if chain_result == CHAIN_ID_EXPECTED:
        network_status = "PASS_BASE_SEPOLIA_CHAIN_ID"
    else:
        network_status = "CONFLICT_OR_HOLD_CHAIN_ID"

    output = {
        "schema": "citizen_eas_uid_live_replay_observation.v0_1",
        "observed_at_utc": observed_at,
        "parent_entry": "CITIZEN_LEDGER_ITEM_001",
        "source_class": "GITHUB_ACTIONS_PUBLIC_NETWORK_REPLAY",
        "query_targets": {
            "attestation_uid": UID,
            "declared_schema_uid": DECLARED_SCHEMA_UID,
            "declared_transaction_hash": DECLARED_TX_HASH,
            "easscan_graphql": EASSCAN_GRAPHQL,
            "base_sepolia_rpc": BASE_SEPOLIA_RPC,
            "expected_chain_id_decimal": 84532,
        },
        "observations": {
            "network_status": network_status,
            "rpc_chain_id_result": chain_result,
            "easscan_http_status": eas.get("http_status"),
            "easscan_graphql_errors": gql_errors,
            "uid_status": uid_status,
            "attestation": attestation,
            "declared_tx_rpc_transaction": tx_result,
            "declared_tx_rpc_receipt": receipt_result,
        },
        "classification": {
            "parent_conflict_rewritten": False,
            "uid_object_bound": bool(attestation),
            "declared_transaction_found": tx_result is not None,
            "declared_transaction_receipt_found": receipt_result is not None,
            "recovery_terminal": "PASS_UID_OBJECT_FOUND" if attestation else ("CONFLICT_UID_NOT_INDEXED_AND_TX_NOT_FOUND" if uid_status == "NOT_FOUND_IN_EASSCAN_INDEXER" and tx_result is None and receipt_result is None else "HOLD"),
            "round_06_executive_advanced": False,
            "authority_created": False,
        },
        "boundaries": {
            "repository_record_not_chain_truth": True,
            "uid_string_not_attestation": True,
            "easscan_indexer_result_not_same_as_direct_contract_state": True,
            "corrected_hash_must_come_from_bound_object": True,
            "parent_conflict_must_not_be_rewritten": True,
            "family_lane_imported": False,
            "authority_created": False,
        },
    }

    print(json.dumps(output, indent=2, sort_keys=True))

    # Exit nonzero only for transport/query failure; NOT_FOUND is a valid replay observation.
    if eas.get("http_status") != 200 or gql_errors or chain_result != CHAIN_ID_EXPECTED:
        sys.exit(2)


if __name__ == "__main__":
    main()
