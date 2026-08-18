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
EAS_CONTRACT = "0x4200000000000000000000000000000000000021"
SCHEMA_REGISTRY_CONTRACT = "0x4200000000000000000000000000000000000020"
ZERO_BYTES32 = "0x" + "0" * 64


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


def rpc_result(response):
    payload = response.get("json")
    return payload.get("result") if isinstance(payload, dict) else None


def selector(signature, ident):
    encoded = "0x" + signature.encode("utf-8").hex()
    digest = rpc_result(rpc("web3_sha3", [encoded], ident))
    return (digest[:10] if isinstance(digest, str) and digest.startswith("0x") and len(digest) >= 10 else None), digest


def direct_call(contract, function_signature, bytes32_arg, ident_base):
    sel, digest = selector(function_signature, ident_base)
    if not sel:
        return {"selector": None, "signature_hash": digest, "result": None, "error": "SELECTOR_UNAVAILABLE"}
    calldata = sel + bytes32_arg[2:]
    response = rpc("eth_call", [{"to": contract, "data": calldata}, "latest"], ident_base + 1)
    return {
        "selector": sel,
        "signature_hash": digest,
        "calldata": calldata,
        "rpc_http_status": response.get("http_status"),
        "rpc_error": ((response.get("json") or {}).get("error") if isinstance(response.get("json"), dict) else response.get("error")),
        "result": rpc_result(response),
    }


def words(raw):
    if not isinstance(raw, str) or not raw.startswith("0x"):
        return []
    body = raw[2:]
    if len(body) % 64:
        return []
    return [body[i:i + 64] for i in range(0, len(body), 64)]


def decode_dynamic_bytes(raw, offset_word):
    if not isinstance(raw, str) or not raw.startswith("0x"):
        return None
    body = raw[2:]
    try:
        offset_bytes = int(offset_word, 16)
        start = offset_bytes * 2
        if start + 64 > len(body):
            return None
        length = int(body[start:start + 64], 16)
        data_start = start + 64
        data_end = data_start + length * 2
        if data_end > len(body):
            return None
        return "0x" + body[data_start:data_end]
    except Exception:
        return None


def decode_attestation(raw):
    ws = words(raw)
    if len(ws) < 10:
        return None
    data = decode_dynamic_bytes(raw, ws[9])
    return {
        "uid": "0x" + ws[0],
        "schema": "0x" + ws[1],
        "time": int(ws[2], 16),
        "expirationTime": int(ws[3], 16),
        "revocationTime": int(ws[4], 16),
        "refUID": "0x" + ws[5],
        "recipient": "0x" + ws[6][-40:],
        "attester": "0x" + ws[7][-40:],
        "revocable": bool(int(ws[8], 16)),
        "data": data,
    }


def decode_schema(raw):
    ws = words(raw)
    if len(ws) < 4:
        return None
    dynamic = decode_dynamic_bytes(raw, ws[3])
    schema_text = None
    if dynamic is not None:
        try:
            schema_text = bytes.fromhex(dynamic[2:]).decode("utf-8")
        except Exception:
            schema_text = None
    return {
        "uid": "0x" + ws[0],
        "resolver": "0x" + ws[1][-40:],
        "revocable": bool(int(ws[2], 16)),
        "schema": schema_text,
        "schema_raw": dynamic,
    }


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
    direct_attestation_call = direct_call(EAS_CONTRACT, "getAttestation(bytes32)", UID, 10)
    direct_schema_call = direct_call(SCHEMA_REGISTRY_CONTRACT, "getSchema(bytes32)", DECLARED_SCHEMA_UID, 20)

    eas_json = eas.get("json") if isinstance(eas.get("json"), dict) else {}
    gql_errors = eas_json.get("errors")
    attestation = (eas_json.get("data") or {}).get("attestation") if not gql_errors else None

    chain_result = rpc_result(chain_id)
    tx_result = rpc_result(tx)
    receipt_result = rpc_result(receipt)
    contract_attestation = decode_attestation(direct_attestation_call.get("result"))
    contract_schema = decode_schema(direct_schema_call.get("result"))

    if eas.get("http_status") != 200 or gql_errors:
        uid_indexer_status = "HOLD_QUERY_ERROR"
    elif attestation is None:
        uid_indexer_status = "NOT_FOUND_IN_EASSCAN_INDEXER"
    else:
        uid_indexer_status = "FOUND_IN_EASSCAN_INDEXER"

    if contract_attestation is None:
        uid_contract_status = "HOLD_DIRECT_CALL_DECODE_ERROR"
    elif contract_attestation["uid"].lower() == UID.lower():
        uid_contract_status = "PASS_ATTESTATION_PRESENT_IN_EAS_CONTRACT"
    elif contract_attestation["uid"].lower() == ZERO_BYTES32.lower():
        uid_contract_status = "REJECT_ATTESTATION_UID_ABSENT_IN_EAS_CONTRACT"
    else:
        uid_contract_status = "CONFLICT_UNEXPECTED_UID_RETURNED"

    if contract_schema is None:
        schema_contract_status = "HOLD_DIRECT_CALL_DECODE_ERROR"
    elif contract_schema["uid"].lower() == DECLARED_SCHEMA_UID.lower():
        schema_contract_status = "PASS_SCHEMA_PRESENT_IN_REGISTRY"
    elif contract_schema["uid"].lower() == ZERO_BYTES32.lower():
        schema_contract_status = "REJECT_SCHEMA_UID_ABSENT_IN_REGISTRY"
    else:
        schema_contract_status = "CONFLICT_UNEXPECTED_UID_RETURNED"

    network_status = "PASS_BASE_SEPOLIA_CHAIN_ID" if chain_result == CHAIN_ID_EXPECTED else "CONFLICT_OR_HOLD_CHAIN_ID"

    declared_tx_rejected = tx_result is None and receipt_result is None and chain_result == CHAIN_ID_EXPECTED
    onchain_attestation_rejected = uid_contract_status == "REJECT_ATTESTATION_UID_ABSENT_IN_EAS_CONTRACT"
    schema_registration_rejected = schema_contract_status == "REJECT_SCHEMA_UID_ABSENT_IN_REGISTRY"

    if declared_tx_rejected and onchain_attestation_rejected and schema_registration_rejected:
        recovery_terminal = "REJECT_DECLARED_BASE_SEPOLIA_ANCHOR_OBJECTS"
    elif uid_contract_status.startswith("PASS_"):
        recovery_terminal = "PASS_UID_OBJECT_FOUND_DIRECT_CONTRACT"
    elif declared_tx_rejected or onchain_attestation_rejected or schema_registration_rejected:
        recovery_terminal = "CONFLICT_PARTIAL_NEGATIVE_DIRECT_REPLAY"
    else:
        recovery_terminal = "HOLD"

    output = {
        "schema": "citizen_eas_uid_live_replay_observation.v0_2",
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
            "eas_contract": EAS_CONTRACT,
            "schema_registry_contract": SCHEMA_REGISTRY_CONTRACT,
        },
        "observations": {
            "network_status": network_status,
            "rpc_chain_id_result": chain_result,
            "easscan_http_status": eas.get("http_status"),
            "easscan_graphql_errors": gql_errors,
            "uid_indexer_status": uid_indexer_status,
            "easscan_attestation": attestation,
            "declared_tx_rpc_transaction": tx_result,
            "declared_tx_rpc_receipt": receipt_result,
            "direct_attestation_call": direct_attestation_call,
            "direct_attestation_decoded": contract_attestation,
            "uid_contract_status": uid_contract_status,
            "direct_schema_call": direct_schema_call,
            "direct_schema_decoded": contract_schema,
            "schema_contract_status": schema_contract_status,
        },
        "classification": {
            "parent_historical_conflict_preserved": True,
            "declared_transaction_edge": "REJECT" if declared_tx_rejected else "PASS_OR_HOLD",
            "declared_transaction_receipt_edge": "REJECT" if declared_tx_rejected else "PASS_OR_HOLD",
            "declared_onchain_attestation_edge": "REJECT" if onchain_attestation_rejected else ("PASS" if uid_contract_status.startswith("PASS_") else "HOLD_OR_CONFLICT"),
            "declared_schema_registration_edge": "REJECT" if schema_registration_rejected else ("PASS" if schema_contract_status.startswith("PASS_") else "HOLD_OR_CONFLICT"),
            "recovery_terminal": recovery_terminal,
            "round_06_executive_advanced": False,
            "authority_created": False,
        },
        "boundaries": {
            "repository_record_not_chain_truth": True,
            "uid_string_not_attestation": True,
            "indexer_result_not_same_as_contract_state": True,
            "direct_contract_state_preferred_for_onchain_existence": True,
            "corrected_hash_must_come_from_bound_object": True,
            "parent_historical_conflict_must_not_be_rewritten": True,
            "family_lane_imported": False,
            "authority_created": False,
        },
    }

    print(json.dumps(output, indent=2, sort_keys=True))

    transport_bad = eas.get("http_status") != 200 or gql_errors or chain_result != CHAIN_ID_EXPECTED
    direct_call_bad = direct_attestation_call.get("result") is None or direct_schema_call.get("result") is None
    if transport_bad or direct_call_bad:
        sys.exit(2)


if __name__ == "__main__":
    main()
