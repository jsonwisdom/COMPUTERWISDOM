#!/usr/bin/env python3
"""Fail closed unless #488's new semantic lanes are governed and CI-admitted."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CONTRACTS = {
    "fixtures/jaywisdom/source_bytes/README.md": [
        "DIRECTORIES_FIRST_CORRECTIVE_SUPERSESSION",
        "Admitted artifact classes",
        "SOURCE_BYTES_RECEIPT_TEST_VECTORS_*.json",
        "File presence alone is not verification",
    ],
    "agents/congressional_accountability/README.md": [
        "DIRECTORIES_FIRST_CORRECTIVE_SUPERSESSION",
        "Admitted artifact classes",
        "AGENT_CONTRACT != MODEL_EXECUTION",
        "OPENAI_DEVELOPER_SURFACE != REPOSITORY_EXECUTOR",
    ],
}

REQUIRED_FILES = [
    "fixtures/jaywisdom/source_bytes/SOURCE_BYTES_RECEIPT_TEST_VECTORS_V0_1.json",
    "schemas/jaywisdom/source_bytes_receipt.v0_1.schema.json",
    "tools/verify_source_bytes_receipt_v0_1.py",
    "agents/congressional_accountability/agent_contract.json",
]

WORKFLOW = ".github/workflows/congressional-accountability-membrane-v0-1.yml"
WORKFLOW_MARKERS = [
    "fixtures/jaywisdom/source_bytes/**",
    "agents/congressional_accountability/**",
    "schemas/jaywisdom/source_bytes_receipt.v0_1.schema.json",
    "tools/verify_source_bytes_receipt_v0_1.py",
    "tools/verify_congressional_directory_contracts_v0_1.py",
    "python tools/verify_source_bytes_receipt_v0_1.py --self-test",
    "python tools/verify_congressional_directory_contracts_v0_1.py",
]


def main() -> int:
    failures = []
    checks = 0

    for relative, markers in CONTRACTS.items():
        path = ROOT / relative
        checks += 1
        if not path.is_file():
            failures.append(f"MISSING_DIRECTORY_CONTRACT:{relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            checks += 1
            if marker not in text:
                failures.append(f"CONTRACT_MARKER_MISSING:{relative}:{marker}")

    for relative in REQUIRED_FILES:
        checks += 1
        if not (ROOT / relative).is_file():
            failures.append(f"REQUIRED_ARTIFACT_MISSING:{relative}")

    workflow = ROOT / WORKFLOW
    checks += 1
    if not workflow.is_file():
        failures.append(f"WORKFLOW_MISSING:{WORKFLOW}")
    else:
        text = workflow.read_text(encoding="utf-8")
        for marker in WORKFLOW_MARKERS:
            checks += 1
            if marker not in text:
                failures.append(f"CI_ADMISSION_MISSING:{marker}")

    receipt = {
        "verifier": "CONGRESSIONAL_DIRECTORY_CONTRACTS_V0.1",
        "build_mode": "DIRECTORIES_FIRST_CORRECTIVE_SUPERSESSION",
        "violation_head_preserved": "f9eeff160f3084c2740ffa02be6c4b9b845ef9a8",
        "checks_executed": checks,
        "failures": failures,
        "result": "PASS" if not failures else "FAIL",
        "history_rewritten": False,
        "model_execution_performed": False,
        "authority_created": False,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

