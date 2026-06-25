from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cli.receipts import verify_receipt
from core import seal
from policy.rql_lite import PolicyError, evaluate_policy, parse_policy


def sealed_receipt(tmp_path):
    artifact = tmp_path / 'artifact.txt'
    artifact.write_text('hello', encoding='utf-8')
    graph = tmp_path / 'graph.json'
    graph.write_text(json.dumps({'authority':'NONE','claims':[{'claim_id':'a','dependencies':[]}]}), encoding='utf-8')
    receipt = seal(str(artifact), str(graph))
    receipt_path = tmp_path / 'sealed_receipt.json'
    receipt_path.write_text(json.dumps(receipt), encoding='utf-8')
    return receipt, receipt_path


def test_policy_accepts_strict_research(tmp_path):
    receipt, receipt_path = sealed_receipt(tmp_path)
    policy = tmp_path / 'policy.rql'
    policy.write_text('REQUIRE confidence.authority == NONE\nREQUIRE claims_count >= 1\n', encoding='utf-8')
    assert verify_receipt(str(receipt_path), policy_path=str(policy)) == 0


def test_policy_failure_exit_code_is_one(tmp_path):
    receipt, receipt_path = sealed_receipt(tmp_path)
    policy = tmp_path / 'policy.rql'
    policy.write_text('REQUIRE claims_count > 1\n', encoding='utf-8')
    assert verify_receipt(str(receipt_path), policy_path=str(policy)) == 1


def test_policy_denies_wrong_claim_count(tmp_path):
    receipt, _ = sealed_receipt(tmp_path)
    rules = parse_policy('REQUIRE claims_count > 1\n')
    try:
        evaluate_policy(receipt, rules)
        assert False
    except PolicyError as exc:
        assert 'REQUIRE failed' in str(exc)


def test_policy_denies_authority_root():
    receipt = {
        'confidence': {'authority': 'ROOT'},
        'claims_count': 1
    }
    rules = parse_policy('DENY confidence.authority != NONE\n')
    try:
        evaluate_policy(receipt, rules)
        assert False
    except PolicyError as exc:
        assert 'DENY failed' in str(exc)


def test_policy_missing_path_fails():
    rules = parse_policy('REQUIRE confidence.missing == NONE\n')
    try:
        evaluate_policy({'confidence': {'authority': 'NONE'}}, rules)
        assert False
    except PolicyError as exc:
        assert 'missing path' in str(exc)


def test_policy_float_comparison():
    rules = parse_policy('REQUIRE score >= 0.75\n')
    assert evaluate_policy({'score': 0.8}, rules) is True


def test_policy_rejects_in_operator():
    try:
        parse_policy('REQUIRE confidence.authority in NONE,ROOT\n')
        assert False
    except PolicyError as exc:
        assert 'invalid operator' in str(exc)
