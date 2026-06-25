import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = ROOT / 'external-roots' / 'al-base-mcp-v0.1.json'


def load_root():
    return json.loads(EXTERNAL_ROOT.read_text(encoding='utf-8'))


def test_external_root_authority_boundaries():
    root = load_root()
    assert root['authority'] == 'NONE'
    assert root['runtime'] == 'NOT_PERMITTED'
    assert root['wallet_authority'] is False
    assert root['execution_authority'] is False
    assert root['merge_authority'] is False
    assert root['x402_enabled'] is False
    assert root['signing_enabled'] is False
    assert root['human_approval_required'] is True


def test_external_root_required_paths():
    root = load_root()
    assert root['source_repo'] == 'jsonwisdom/AL'
    assert root['identity_anchor'] == 'jaywisdom.base.eth'
    assert root['base_mcp_plan'] == 'docs/base-mcp-alms-agent-plan.md'
    assert root['scaffold_audit_receipt'] == 'docs/base-mcp-scaffold-audit-receipt.md'
    assert root['action_receipt_schema'] == 'agents/base_mcp/schemas/action_receipt.schema.json'
    assert root['permission_policy_schema'] == 'agents/base_mcp/schemas/permission_policy.schema.json'
    assert root['session_log_schema'] == 'agents/base_mcp/schemas/session_log.schema.json'


def test_external_root_target_stack():
    root = load_root()
    assert 'COMPUTERWISDOM' in root['target_stack']
    assert 'Receipt Core' in root['target_stack']
    assert 'EAS' in root['target_stack']
    assert 'Jaytree' in root['target_stack']
