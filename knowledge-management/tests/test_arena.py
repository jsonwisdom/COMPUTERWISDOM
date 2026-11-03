#!/usr/bin/env python3
import importlib.util
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
ARENA_PATH = ROOT / "knowledge-management" / "arena" / "arena.py"
FIXTURE = ROOT / "knowledge-management" / "fixtures" / "valid" / "arena-round-minimal.json"

spec = importlib.util.spec_from_file_location("computerwisdom_arena", ARENA_PATH)
arena = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = arena
assert spec.loader is not None
spec.loader.exec_module(arena)


class SentinelArenaTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_round_is_contested_and_non_authoritative(self):
        report = arena.evaluate_round(self.load_fixture())
        self.assertEqual(report["status"], "contested")
        self.assertIsNone(report["winning_instrument"])
        self.assertFalse(report["authority"])
        self.assertFalse(report["remediation_applied"])
        self.assertFalse(report["escalate"])
        self.assertGreaterEqual(len(report["scores"]), 2)

    def test_declared_confidence_does_not_override_evidence(self):
        round_data = self.load_fixture()
        round_data["instruments"][0]["confidence"] = 0.01
        round_data["instruments"][1]["confidence"] = 0.99
        report = arena.evaluate_round(round_data)
        scores = {row["instrument_id"]: row for row in report["scores"]}
        self.assertGreater(
            scores["growth-durable"]["calibrated_confidence"],
            scores["growth-drift"]["calibrated_confidence"],
        )

    def test_arena_cannot_claim_authority(self):
        round_data = self.load_fixture()
        round_data["authority"] = True
        with self.assertRaises(arena.ArenaError):
            arena.evaluate_round(round_data)

    def test_critical_evidence_escalates_without_remediation(self):
        round_data = self.load_fixture()
        round_data["evidence"][0]["severity"] = "critical"
        report = arena.evaluate_round(round_data)
        self.assertEqual(report["status"], "escalate")
        self.assertTrue(report["escalate"])
        self.assertFalse(report["remediation_applied"])


if __name__ == "__main__":
    unittest.main()
