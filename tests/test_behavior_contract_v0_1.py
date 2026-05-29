"""Behavior contract tests for classification validator kernel v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from validator.classification_validator_kernel_v0_1 import validate, validate_sequence  # noqa: E402

FIXTURE_DIR = ROOT / "fixtures"


def load_fixture(name: str) -> dict:
    with (FIXTURE_DIR / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def assert_expected(actual, fixture):
    verdict, reason_code, gate_triggered = actual
    expected = fixture["expected"]
    assert verdict == expected["verdict"]
    assert reason_code == expected["reason_code"]
    assert gate_triggered == expected["gate_triggered"]


def test_001_full_valid_lattice():
    fixture = load_fixture("001_full_valid_lattice.json")
    actual = validate_sequence(fixture["receipts"])
    assert_expected(actual, fixture)


def test_002_bad_authority_true():
    fixture = load_fixture("002_bad_authority_true.json")
    actual = validate(fixture["receipt"], {})
    assert_expected(actual, fixture)


def test_003_bad_hash_format():
    fixture = load_fixture("003_bad_hash_format.json")
    actual = validate(fixture["receipt"], {})
    assert_expected(actual, fixture)


def test_004_invalid_transition_skip():
    fixture = load_fixture("004_invalid_transition_skip.json")
    ledger = {item["receipt_id"]: item for item in fixture["ledger_seed"]}
    actual = validate(fixture["receipt"], ledger)
    assert_expected(actual, fixture)


def test_005_orphaned_parent():
    fixture = load_fixture("005_orphaned_parent.json")
    actual = validate(fixture["receipt"], {})
    assert_expected(actual, fixture)


def test_006_truth_claim_decision():
    fixture = load_fixture("006_truth_claim_decision.json")
    actual = validate(fixture["receipt"], {})
    assert_expected(actual, fixture)
