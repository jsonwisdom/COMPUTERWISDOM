import json
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.qualification.eev_calculator import (
    EEV_THRESHOLD_USD,
    FORMULA_VERSION,
    OpportunityInputs,
    compute_eev_usd,
)

FIXTURES = ROOT / "tests" / "fixtures"
SCHEMA = json.loads((ROOT / "schemas" / "score.schema.json").read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft202012Validator(SCHEMA)

CASES = [
    ("score_boundary_12_60.json", 12.60, False, "LOW_EEV"),
    ("score_boundary_15_12.json", 15.12, True, "OK"),
    ("score_high_pass.json", 1960.00, True, "OK"),
    ("score_low_fail.json", -40.00, False, "LOW_EEV"),
]

def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

def score(name):
    return compute_eev_usd(
        OpportunityInputs(**load(name)),
        scored_at="2026-08-07T00:00:00+00:00",
    )

def test_contract_constants():
    assert EEV_THRESHOLD_USD == 15.0
    assert FORMULA_VERSION == "EEV_V0_1"

@pytest.mark.parametrize("name, expected_eev, expected_pass, expected_reason", CASES)
def test_fixture_contract(name, expected_eev, expected_pass, expected_reason):
    result = score(name)
    assert pytest.approx(result["expected_value_usd"], rel=0, abs=1e-9) == expected_eev
    assert result["threshold_usd"] == EEV_THRESHOLD_USD
    assert result["threshold_pass"] is expected_pass
    assert result["reason"] == expected_reason
    assert result["formula_version"] == FORMULA_VERSION
    VALIDATOR.validate(result)

def test_probability_above_one_fails_closed():
    bad = load("score_boundary_12_60.json")
    bad["acceptance_probability"] = 1.1
    with pytest.raises(ValueError):
        compute_eev_usd(OpportunityInputs(**bad))

def test_probability_below_zero_fails_closed():
    bad = load("score_boundary_12_60.json")
    bad["acceptance_probability"] = -0.1
    with pytest.raises(ValueError):
        compute_eev_usd(OpportunityInputs(**bad))

def test_negative_cost_fails_closed():
    bad = load("score_high_pass.json")
    bad["agent_hour_cost_usd"] = -5
    with pytest.raises(ValueError):
        compute_eev_usd(OpportunityInputs(**bad))

def test_missing_required_input_fails_closed():
    bad = load("score_high_pass.json")
    del bad["payout_usd"]
    with pytest.raises(TypeError):
        OpportunityInputs(**bad)
