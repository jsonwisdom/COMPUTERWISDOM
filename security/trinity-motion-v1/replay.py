#!/usr/bin/env python3
"""CI-FIRST Trinity synthetic-only motion replay; read-only, standard library."""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "SYNTHETIC_MOTION_128BPM_V1.json"
PINNED_SHA256 = "9c5b24e2e889db86412155631df33aea6ec13e9d0d4c59c28f48b13dc4988d0c"

ALLOWED_KEYS = frozenset({
    "schema", "synthetic", "person_present", "consent_required_for_real_people",
    "coordinate_system", "tempo_reference_bpm", "camera_fps_reference_only",
    "observations", "rights", "identity_derived", "real_attestation"
})
ALLOWED_POINT_KEYS = frozenset({"t_seconds", "x_metres", "y_metres", "z_metres"})

def evaluate(raw: bytes, expected_digest: str = PINNED_SHA256) -> dict:
    """Verify fixture bytes before calculating synthetic speed; never authenticate people."""
    got = hashlib.sha256(raw).hexdigest()
    if got != expected_digest:
        raise ValueError("FAIL: original synthetic fixture bytes differ from pinned SHA256")
    data = json.loads(raw)
    if set(data) != ALLOWED_KEYS:
        raise ValueError("FAIL: missing or unexpected fields (possible privacy leak)")
    if data["schema"] != "CW_SYNTHETIC_MOTION_TRACE_V1":
        raise ValueError("FAIL: unknown schema")
    if data["synthetic"] is not True or data["person_present"] is not False:
        raise ValueError("FAIL: no human-person record is permitted in public synthetic CI")
    if data["identity_derived"] is not False or data["real_attestation"] is not False:
        raise ValueError("FAIL: synthetic math cannot certify identity or hardware")
    if data["consent_required_for_real_people"] is not True:
        raise ValueError("FAIL: consent boundary cannot be disabled")
    if data["coordinate_system"] != "METRES_LOCAL_SYNTHETIC":
        raise ValueError("FAIL: calibrated units not declared")
    if data["rights"] != "SYNTHETIC_CREATED_FOR_MATHEMATICAL_TEST_ONLY":
        raise ValueError("FAIL: unexpected rights scope")
    bpm = data["tempo_reference_bpm"]
    fps = data["camera_fps_reference_only"]
    if type(bpm) is not int or bpm != 128 or type(fps) is not int or fps != 30:
        raise ValueError("FAIL: expected reference tempo and sample rate")
    points = data["observations"]
    if not isinstance(points, list) or len(points) != 2:
        raise ValueError("FAIL: expected exactly two synthetic observations")
    for p in points:
        if set(p) != ALLOWED_POINT_KEYS:
            raise ValueError("FAIL: unrecognized motion fields")
        for k in ALLOWED_POINT_KEYS:
            try:
                v = Fraction(str(p[k]))
            except (ValueError, ZeroDivisionError, TypeError) as exc:
                raise ValueError("FAIL: nonnumeric synthetic coordinate") from exc
            if abs(v) > 1000000:
                raise ValueError("FAIL: out-of-bounds synthetic coordinate")
    a, b = points
    dt = Fraction(str(b["t_seconds"])) - Fraction(str(a["t_seconds"]))
    if dt <= 0:
        raise ValueError("FAIL: non-increasing timestamps")
    if dt != Fraction(60, bpm):
        raise ValueError("FAIL: fixture interval not precisely one reference beat")
    if any(Fraction(str(b[k])) != Fraction(str(a[k])) for k in ("y_metres","z_metres")):
        raise ValueError("FAIL: expected exact 1D synthetic fixture")
    distance = abs(Fraction(str(b["x_metres"])) - Fraction(str(a["x_metres"])))
    if distance != Fraction(1, 2):
        raise ValueError("FAIL: expected one 0.5 m synthetic forward step")
    speed = distance / dt
    return {
        "schema": "CW_TRINITY_MOTION_REPLAY_V1",
        "fixture_sha256": got,
        "synthetic_fixture_bytes": len(raw),
        "reference_beat_microseconds": 468750,
        "reference_frames_per_beat_fraction": "225/16",
        "illustrative_speed_metres_per_second_fraction": f"{speed.numerator}/{speed.denominator}",
        "illustrative_speed_kilometres_per_hour": float(speed * Fraction(18, 5)),
        "findings": {
            "fixture_sha256": "PASS",
            "synthetic_only_privacy_gate": "PASS",
            "reference_128_bpm": "PASS",
            "synthetic_speed_math": "PASS",
            "real_dancer_speed": "UNKNOWN",
            "official_identity_match": "UNKNOWN",
            "live_hardware_attestation": "UNKNOWN",
            "encrypted_windows_sync": "UNKNOWN",
            "live_hostname_routing": "UNKNOWN",
            "ens_wallet_signing_control": "UNKNOWN",
            "bns_identity_binding": "UNKNOWN",
        },
        "overall": "UNKNOWN",
        "authority_created": False,
        "biometric_enrollment_created": False,
        "wallet_signature_created": False,
        "production_deployment": False,
    }

class CIAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = FIXTURE.read_bytes()

    def mutation(self, **changes):
        m = json.loads(self.raw)
        m.update(changes)
        raw = json.dumps(m, sort_keys=True, separators=(",", ":")).encode()
        return raw, hashlib.sha256(raw).hexdigest()

    def test_fixture_passes_scoped_checks(self):
        result = evaluate(self.raw)
        self.assertEqual(result["findings"]["synthetic_speed_math"], "PASS")
        self.assertEqual(result["overall"], "UNKNOWN")
        self.assertFalse(result["authority_created"])

    def test_byte_tamper_detected(self):
        with self.assertRaises(ValueError):
            evaluate(self.raw + b" ")

    def test_no_real_person(self):
        raw, sha = self.mutation(person_present=True)
        with self.assertRaises(ValueError):
            evaluate(raw, sha)

    def test_no_identity_promotion(self):
        raw, sha = self.mutation(identity_derived=True)
        with self.assertRaises(ValueError):
            evaluate(raw, sha)

    def test_no_attestation_promotion(self):
        raw, sha = self.mutation(real_attestation=True)
        with self.assertRaises(ValueError):
            evaluate(raw, sha)

    def test_no_bypass_of_consent(self):
        raw, sha = self.mutation(consent_required_for_real_people=False)
        with self.assertRaises(ValueError):
            evaluate(raw, sha)

    def test_no_extra_personal_fields(self):
        raw, sha = self.mutation(person_name="PRIVATE_PERSON")
        with self.assertRaises(ValueError):
            evaluate(raw, sha)

    def test_no_fake_reference_tempo(self):
        raw, sha = self.mutation(tempo_reference_bpm=129)
        with self.assertRaises(ValueError):
            evaluate(raw, sha)

    def test_no_invalid_timestamp(self):
        m = json.loads(self.raw)
        m["observations"][1]["t_seconds"] = 0
        raw = json.dumps(m).encode()
        with self.assertRaises(ValueError):
            evaluate(raw, hashlib.sha256(raw).hexdigest())

    def test_no_false_speed(self):
        m = json.loads(self.raw)
        m["observations"][1]["x_metres"] = 1.0
        raw = json.dumps(m).encode()
        with self.assertRaises(ValueError):
            evaluate(raw, hashlib.sha256(raw).hexdigest())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic only: no biometric or PC access")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=["CIAdversarialTests"], exit=False, verbosity=2)
    else:
        print(json.dumps(evaluate(FIXTURE.read_bytes()), indent=2, sort_keys=True))
