#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "adapters" / "courts" / "replay_court_adapter_v0_1.py"
RECEIPT = ROOT / "fixtures" / "court" / "RECAP_TEST_RECEIPT_001.json"
DRY = ROOT / "fixtures" / "court" / "EAS_DRY_RUN_001.json"
SEAL = ROOT / "fixtures" / "court" / "SEAL_ENVELOPE_DRY_RUN_001.json"


def load_adapter():
    name = "replay_court_adapter_v0_1"
    spec = importlib.util.spec_from_file_location(name, ADAPTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load adapter")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    adapter = load_adapter()
    receipt = read_json(RECEIPT)
    expected_dry = read_json(DRY)
    expected_seal = read_json(SEAL)

    adapter.validate_receipt_core(receipt)
    actual_dry = adapter.build_eas_dry_run(receipt)
    if actual_dry != expected_dry:
        raise RuntimeError("EAS dry-run fixture mismatch")

    actual_seal = adapter.build_pending_seal_envelope(receipt, actual_dry)
    if actual_seal != expected_seal:
        raise RuntimeError("seal-envelope fixture mismatch")

    print(json.dumps({
        "state": "GREEN",
        "receipt_hash": receipt["integrity"]["self_hash"],
        "schema_uid": adapter.EAS_SCHEMA_UID,
        "attestation_created": False,
        "authority": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
