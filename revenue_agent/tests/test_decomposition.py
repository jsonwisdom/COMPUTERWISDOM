import json
import math
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from decomposition.agent import (
    DECOMPOSITION_VERSION,
    decompose_claim,
    generate_work_order_id,
)
from src.qualification.eev_calculator import OpportunityInputs, compute_eev_usd

SCHEMA = json.loads(
    (ROOT / "schemas" / "work_order.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)
FIXTURES = ROOT / "tests" / "fixtures"


def test_work_order_validates_against_schema():
    result = decompose_claim("Test claim", token_weight=1.5)
    assert len(result) == 1
    for work_order in result:
        VALIDATOR.validate(work_order)


def test_quadratic_weight_is_pass_through_metadata_only():
    work_order = decompose_claim("Test claim", token_weight=4.25)[0]
    assert work_order["quadratic_weight"] == 4.25
    assert work_order["verification_status"] == "UNVERIFIED"
    assert work_order["authority_created"] is False
    assert work_order["method"] == "PENDING"
    assert work_order["acceptance_test"] == "PENDING"


def test_decomposition_version_is_locked():
    work_order = decompose_claim("Test claim")[0]
    assert work_order["decomposition_version"] == DECOMPOSITION_VERSION
    assert DECOMPOSITION_VERSION == "DECOMPOSITION_V0_1"


def test_work_order_id_is_deterministic():
    a = decompose_claim("  Test claim  ", parent_id="parent_1", token_weight=1.5)[0]
    b = decompose_claim("Test claim", parent_id="parent_1", token_weight=1.5)[0]
    assert a["work_order_id"] == b["work_order_id"]
    assert a["work_order_id"] == generate_work_order_id("Test claim", "parent_1", 1.5)
    assert a["work_order_id"].startswith("JOY-")
    assert a["claim_text"] == "Test claim"


def test_parent_changes_identity():
    a = decompose_claim("Test claim", parent_id="parent_1", token_weight=1.5)[0]
    b = decompose_claim("Test claim", parent_id="parent_2", token_weight=1.5)[0]
    assert a["work_order_id"] != b["work_order_id"]


def test_quadratic_weight_changes_identity_but_not_verification_state():
    a = decompose_claim("Test claim", parent_id="parent_1", token_weight=1.0)[0]
    b = decompose_claim("Test claim", parent_id="parent_1", token_weight=2.0)[0]
    assert a["work_order_id"] != b["work_order_id"]
    assert a["verification_status"] == b["verification_status"] == "UNVERIFIED"
    assert a["authority_created"] is b["authority_created"] is False


@pytest.mark.parametrize("bad_weight", [-0.01, math.inf, -math.inf, math.nan])
def test_invalid_quadratic_weight_fails_closed(bad_weight):
    with pytest.raises(ValueError):
        decompose_claim("Test claim", token_weight=bad_weight)


def test_boolean_weight_fails_closed():
    with pytest.raises(TypeError):
        decompose_claim("Test claim", token_weight=True)


def test_blank_claim_fails_closed():
    with pytest.raises(ValueError):
        decompose_claim("   ")


def test_blank_parent_fails_closed():
    with pytest.raises(ValueError):
        decompose_claim("Test claim", parent_id="   ")


def test_schema_rejects_authority_creation():
    work_order = decompose_claim("Test claim")[0]
    work_order["authority_created"] = True
    with pytest.raises(jsonschema.ValidationError):
        VALIDATOR.validate(work_order)


def test_first_eev_work_order_fixture_is_deterministic():
    score_inputs = json.loads(
        (FIXTURES / "score_high_pass.json").read_text(encoding="utf-8")
    )
    score = compute_eev_usd(
        OpportunityInputs(**score_inputs),
        scored_at="2026-08-08T00:00:00+00:00",
    )
    assert score["expected_value_usd"] == 1960.0
    assert score["threshold_pass"] is True

    claim_text = (
        f"EEV fixture {score['opportunity_id']} has expected economic value "
        f"{score['expected_value_usd']:.2f} USD under {score['formula_version']} "
        f"and passes the {score['threshold_usd']:.2f} USD qualification threshold."
    )
    generated = decompose_claim(
        claim_text,
        parent_id=score["opportunity_id"],
        token_weight=1.0,
    )[0]
    expected = json.loads(
        (FIXTURES / "work_order_first_eev.json").read_text(encoding="utf-8")
    )

    assert generated == expected
    assert generated["work_order_id"] == "JOY-CD8D67E3"
    VALIDATOR.validate(generated)
