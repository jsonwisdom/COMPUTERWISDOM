import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from authorization.claim import ClaimResult, FileBasedClaimStore
from authorization.decision import decide
from authorization.policy import AUTH_POLICY_DIGEST
from authorization.receipt_builder import build_authorization_receipt, verify_authorization_receipt
from authorization.signature import SimulationSignatureVerifier, VerificationResult
from authorization.verifier import generate_task_id, verify_authorization, verify_routing_receipt
from matrix.router import POLICY_DIGEST, route

AUTH_SCHEMA = json.loads(
    (ROOT / "authorization" / "schemas" / "auth_receipt.schema.json").read_text()
)


def consequential_receipt():
    return route(
        {
            "where": "R2-COUNTY042",
            "what": "infrastructure_outage",
            "severity_score": 1.0,
            "digest": "a" * 64,
        }
    )


def test_actual_router_policy_digest_is_registered():
    assert POLICY_DIGEST == "df206d84b75d1913607a01f1410fb28aa7c8999c56c8b21e39cc9fa100a3a016"


def test_full_v439_receipt_verifies_and_unknown_fields_fail():
    receipt = consequential_receipt()
    assert verify_routing_receipt(receipt)
    changed = copy.deepcopy(receipt)
    changed["sealed"] = True
    assert not verify_routing_receipt(changed)


def test_digest_recomputation_rejects_mutation():
    receipt = consequential_receipt()
    receipt["locality_scope"] = "R2-COUNTY999"
    assert not verify_routing_receipt(receipt)


def test_task_id_is_deterministic_and_128_bit():
    receipt = consequential_receipt()
    assert generate_task_id(receipt) == generate_task_id(copy.deepcopy(receipt))
    assert len(generate_task_id(receipt)) == len("TASK-") + 32


def test_simulation_is_indeterminate_and_never_authorizes():
    result = verify_authorization(
        consequential_receipt(),
        "jaywisdom.base.eth",
        "public_works",
        "b" * 64,
        b"simulation",
        SimulationSignatureVerifier(),
    )
    assert result.status == "INDETERMINATE"
    assert result.authorized is False


def test_non_consequential_route_cannot_enter_authorization():
    receipt = route(
        {"where": "R2-COUNTY042", "what": "weather_alert", "severity_score": 0.6, "digest": "a" * 64}
    )
    result = verify_authorization(
        receipt, "jaywisdom.base.eth", "public_works", "b" * 64, b"x", SimulationSignatureVerifier()
    )
    assert result.status == "INVALID"


def test_router_and_authorization_policy_must_both_allow_role():
    receipt = consequential_receipt()
    result = verify_authorization(
        receipt, "jaywisdom.base.eth", "public_observer", "b" * 64, b"x", SimulationSignatureVerifier()
    )
    assert result.status == "INVALID"


def test_claim_is_single_use(tmp_path):
    store = FileBasedClaimStore(tmp_path / "claims")
    task_id = generate_task_id(consequential_receipt())
    verified = VerificationResult("VERIFIED", "SIGNATURE_VALID", True)
    first = store.claim(task_id, "c" * 64, verified)
    second = store.claim(task_id, "c" * 64, verified)
    assert first.status == "CLAIMED"
    assert second.status == "ALREADY_CLAIMED"


def test_claim_rejects_unvalidated_identifiers(tmp_path):
    store = FileBasedClaimStore(tmp_path / "claims")
    verified = VerificationResult("VERIFIED", "SIGNATURE_VALID", True)
    assert store.claim("../../escape", "c" * 64, verified).status == "REJECTED"
    assert store.claim("TASK-" + "A" * 32, "X" * 64, verified).status == "REJECTED"


def test_simulation_cannot_consume_single_use_claim(tmp_path):
    store = FileBasedClaimStore(tmp_path / "claims")
    task_id = generate_task_id(consequential_receipt())
    simulation = VerificationResult("INDETERMINATE", "SIMULATION", False)
    result = store.claim(task_id, "c" * 64, simulation)
    assert result == ClaimResult("REJECTED", "SIGNATURE_NOT_VERIFIED")
    assert list((tmp_path / "claims").iterdir()) == []


@pytest.mark.parametrize(
    "verification,claim,expected",
    [
        (VerificationResult("VERIFIED", "SIGNATURE_VALID", True), ClaimResult("CLAIMED"), True),
        (VerificationResult("VERIFIED", "SIGNATURE_VALID", True), ClaimResult("ALREADY_CLAIMED"), False),
        (VerificationResult("INDETERMINATE", "SIMULATION", False), None, False),
        (VerificationResult("INVALID", "BAD_SIGNATURE", False), ClaimResult("CLAIMED"), False),
    ],
)
def test_decision_requires_verified_and_claimed(verification, claim, expected):
    decision = decide(verification, claim)
    assert decision.action_authorized is expected
    assert decision.authority_created is False


def test_authorization_receipt_is_digest_bound_and_schema_valid():
    receipt = consequential_receipt()
    built = build_authorization_receipt(
        generate_task_id(receipt),
        "jaywisdom.base.eth",
        "public_works",
        receipt["routing_digest"],
        VerificationResult("INDETERMINATE", "SIMULATION", False),
        "b" * 64,
        "2026-08-08T20:30:13Z",
    )
    jsonschema.Draft7Validator(AUTH_SCHEMA).validate(built)
    assert verify_authorization_receipt(built)
    built["signer_role"] = "forged"
    assert not verify_authorization_receipt(built)


def test_schema_uses_pattern_not_format():
    rendered = json.dumps(AUTH_SCHEMA, sort_keys=True)
    assert '"format"' not in rendered
    assert "^[a-f0-9]{64}$" in rendered


def test_invalid_verification_result_cannot_claim_authorized():
    with pytest.raises(ValueError):
        VerificationResult("INDETERMINATE", "bad", True)
