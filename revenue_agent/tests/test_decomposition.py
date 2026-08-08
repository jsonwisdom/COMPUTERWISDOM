import json
import math
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from decomposition.agent import DECOMPOSITION_VERSION, decompose_claim

SCHEMA = json.loads(
    (ROOT / "schemas" / "work_order.schema.json").read_text(encoding="utf-8")
)
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)


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
    a = decompose_claim("  Test claim  ", parent_id="parent_1")[0]
    b = decompose_claim("Test claim", parent_id="parent_1")[0]
    assert a["work_order_id"] == b["work_order_id"]
    assert a["claim_text"] == "Test claim"


def test_parent_changes_identity():
    a = decompose_claim("Test claim", parent_id="parent_1")[0]
    b = decompose_claim("Test claim", parent_id="parent_2")[0]
    assert a["work_order_id"] != b["work_order_id"]


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
