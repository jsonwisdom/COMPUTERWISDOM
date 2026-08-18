import base64
import copy
import sys
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from attestation_verifier import (  # noqa: E402
    compute_key_event_id,
    compute_public_key_fingerprint,
    compute_receipt_id,
    compute_signing_event_id,
    raw_digest_from_sha256_id,
    verify_signed_receipt,
)


def h(label: str) -> str:
    import hashlib

    return "sha256:" + hashlib.sha256(label.encode("utf-8")).hexdigest()


def event(event_type, at, **extra):
    value = {"type": event_type, "at": at, **extra}
    value["key_event_id"] = compute_key_event_id(value)
    return value


def private_key(seed_byte: int) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(bytes([seed_byte]) * 32)


def key_record(key_id, key, tenant, role="REPLAY_SERVICE", terminal=None, terminal_at="2026-08-18T08:10:00Z"):
    public_raw = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    events = [
        event("KEY_CREATED", "2026-08-18T08:00:00Z"),
        event("KEY_REGISTERED", "2026-08-18T08:01:00Z"),
        event("TENANT_BOUND", "2026-08-18T08:02:00Z", tenant_id=tenant),
        event("ROLE_GRANTED", "2026-08-18T08:03:00Z", role=role),
        event("ACTIVE", "2026-08-18T08:04:00Z"),
    ]
    if terminal:
        events.append(event(terminal, terminal_at))
    return {
        "key_id": key_id,
        "public_key_base64": base64.b64encode(public_raw).decode("ascii"),
        "public_key_fingerprint": compute_public_key_fingerprint(public_raw),
        "events": events,
    }


def payload(ruleset_version="v1.0.0", ruleset_hash=None):
    return {
        "case_id": "enterprise-case-001",
        "request_hash": h("request"),
        "replay_graph_hash": h("graph"),
        "evidence_hash": h("evidence"),
        "ruleset_hash": ruleset_hash or h("ruleset-v1"),
        "ruleset_version": ruleset_version,
        "disposition": "PASS",
    }


def sign_receipt(payload_value, key_id, key, registry, signed_at="2026-08-18T08:06:00Z", role="REPLAY_SERVICE"):
    receipt_id = compute_receipt_id(payload_value)
    signature = key.sign(raw_digest_from_sha256_id(receipt_id))
    signature_b64 = base64.b64encode(signature).decode("ascii")
    fingerprint = registry["keys"][key_id]["public_key_fingerprint"]
    signing_event_id = compute_signing_event_id(receipt_id, key_id, signed_at, signature_b64)
    return {
        "case_id": payload_value["case_id"],
        "disposition": payload_value["disposition"],
        "receipt_payload": copy.deepcopy(payload_value),
        "receipt_id": receipt_id,
        "signature_bundle": {
            "algorithm": "Ed25519",
            "key_id": key_id,
            "public_key_fingerprint": fingerprint,
            "payload_hash": receipt_id,
            "signature": signature_b64,
            "signed_at": signed_at,
            "signer_role": role,
            "signing_event_id": signing_event_id,
        },
    }


class NegativeTestPackV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key_a = private_key(0x11)
        cls.key_b = private_key(0x22)
        cls.key_audit = private_key(0x33)
        cls.key_suspended = private_key(0x44)
        cls.key_revoked = private_key(0x55)
        cls.key_expired = private_key(0x66)
        cls.key_rotated = private_key(0x77)
        cls.registry = {
            "registry_version": "v0.2",
            "keys": {
                "key-a": key_record("key-a", cls.key_a, "tenant-a"),
                "key-b": key_record("key-b", cls.key_b, "tenant-b"),
                "key-audit": key_record("key-audit", cls.key_audit, "tenant-a", role="AUDIT_SERVICE"),
                "key-suspended": key_record("key-suspended", cls.key_suspended, "tenant-a", terminal="SUSPENDED"),
                "key-revoked": key_record("key-revoked", cls.key_revoked, "tenant-a", terminal="REVOKED"),
                "key-expired": key_record("key-expired", cls.key_expired, "tenant-a", terminal="EXPIRED"),
                "key-rotated": key_record("key-rotated", cls.key_rotated, "tenant-a", terminal="ROTATED"),
            },
        }

    def test_01_valid_authorized_signature(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertTrue(result["authorized_attestation"])
        self.assertEqual(result["disposition"], "PASS")

    def test_02_altered_payload_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signed["receipt_payload"]["evidence_hash"] = h("mutated-evidence")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertFalse(result["authorized_attestation"])
        self.assertIn("RECEIPT_ID_MISMATCH", result["signals"])
        self.assertIn("PAYLOAD_HASH_MISMATCH", result["signals"])
        self.assertIn("SIGNATURE_INVALID", result["signals"])

    def test_03_payload_hash_mismatch_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signed["signature_bundle"]["payload_hash"] = h("wrong-payload-hash")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("PAYLOAD_HASH_MISMATCH", result["signals"])

    def test_04_wrong_tenant_rejected(self):
        signed = sign_receipt(payload(), "key-b", self.key_b, self.registry)
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("TENANT_MISMATCH", result["signals"])

    def test_05_unregistered_key_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signed["signature_bundle"]["key_id"] = "missing-key"
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("KEY_ID_UNREGISTERED", result["signals"])

    def test_06_wrong_role_rejected(self):
        signed = sign_receipt(payload(), "key-audit", self.key_audit, self.registry, role="REPLAY_SERVICE")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("SIGNER_ROLE_NOT_ALLOWED", result["signals"])

    def test_07_suspended_key_rejected_after_suspension(self):
        signed = sign_receipt(payload(), "key-suspended", self.key_suspended, self.registry, signed_at="2026-08-18T08:11:00Z")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("KEY_SUSPENDED_FOR_EVENT_SCOPE", result["signals"])

    def test_08_revoked_key_rejected_after_revocation(self):
        signed = sign_receipt(payload(), "key-revoked", self.key_revoked, self.registry, signed_at="2026-08-18T08:11:00Z")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("KEY_REVOKED_FOR_EVENT_SCOPE", result["signals"])

    def test_09_expired_key_rejected_after_expiration(self):
        signed = sign_receipt(payload(), "key-expired", self.key_expired, self.registry, signed_at="2026-08-18T08:11:00Z")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("KEY_EXPIRED_FOR_EVENT_SCOPE", result["signals"])

    def test_10_forged_receipt_id_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signed["receipt_id"] = h("forged-receipt")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("RECEIPT_ID_MISMATCH", result["signals"])

    def test_11_forged_signature_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signature = bytearray(base64.b64decode(signed["signature_bundle"]["signature"]))
        signature[0] ^= 0x01
        signed["signature_bundle"]["signature"] = base64.b64encode(bytes(signature)).decode("ascii")
        signed["signature_bundle"]["signing_event_id"] = compute_signing_event_id(
            signed["receipt_id"],
            "key-a",
            signed["signature_bundle"]["signed_at"],
            signed["signature_bundle"]["signature"],
        )
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("SIGNATURE_INVALID", result["signals"])

    def test_12_rotated_key_historical_valid_future_invalid(self):
        before = sign_receipt(payload(), "key-rotated", self.key_rotated, self.registry, signed_at="2026-08-18T08:09:00Z")
        after = sign_receipt(payload(), "key-rotated", self.key_rotated, self.registry, signed_at="2026-08-18T08:11:00Z")
        before_result = verify_signed_receipt(before, self.registry, "tenant-a")
        after_result = verify_signed_receipt(after, self.registry, "tenant-a")
        self.assertTrue(before_result["authorized_attestation"])
        self.assertIn("KEY_ROTATED_FOR_EVENT_SCOPE", after_result["signals"])

    def test_13_public_key_fingerprint_mismatch_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signed["signature_bundle"]["public_key_fingerprint"] = h("wrong-fingerprint")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("PUBLIC_KEY_FINGERPRINT_MISMATCH", result["signals"])

    def test_14_ruleset_drift_changes_receipt_identity(self):
        receipt_v1 = compute_receipt_id(payload("v1.0.0", h("ruleset-v1")))
        receipt_v2 = compute_receipt_id(payload("v2.0.0", h("ruleset-v2")))
        self.assertNotEqual(receipt_v1, receipt_v2)

    def test_15_model_output_promotion_field_rejected(self):
        p = payload()
        p["model_disposition"] = "PASS"
        signed = sign_receipt(p, "key-a", self.key_a, self.registry)
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("RECEIPT_PAYLOAD_FIELDS_INVALID", result["signals"])

    def test_16_signing_event_id_mismatch_rejected(self):
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        signed["signature_bundle"]["signing_event_id"] = h("wrong-signing-event")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertIn("SIGNING_EVENT_ID_MISMATCH", result["signals"])

    def test_17_same_receipt_two_signing_events(self):
        p = payload()
        first = sign_receipt(p, "key-a", self.key_a, self.registry, signed_at="2026-08-18T08:06:00Z")
        second = sign_receipt(p, "key-a", self.key_a, self.registry, signed_at="2026-08-18T08:07:00Z")
        first_result = verify_signed_receipt(first, self.registry, "tenant-a")
        second_result = verify_signed_receipt(second, self.registry, "tenant-a")
        self.assertTrue(first_result["authorized_attestation"])
        self.assertTrue(second_result["authorized_attestation"])
        self.assertEqual(first["receipt_id"], second["receipt_id"])
        self.assertNotEqual(first["signature_bundle"]["signing_event_id"], second["signature_bundle"]["signing_event_id"])

    def test_18_key_event_id_tampering_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["keys"]["key-a"]["events"][2]["tenant_id"] = "tenant-b"
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        result = verify_signed_receipt(signed, registry, "tenant-a")
        self.assertTrue(any(signal.startswith("KEY_EVENT_ID_MISMATCH:") for signal in result["signals"]))

    def test_19_revoked_key_historical_signature_remains_valid(self):
        signed = sign_receipt(payload(), "key-revoked", self.key_revoked, self.registry, signed_at="2026-08-18T08:09:00Z")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertTrue(result["authorized_attestation"])

    def test_20_suspended_key_historical_signature_remains_valid(self):
        signed = sign_receipt(payload(), "key-suspended", self.key_suspended, self.registry, signed_at="2026-08-18T08:09:00Z")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertTrue(result["authorized_attestation"])

    def test_21_expired_key_historical_signature_remains_valid(self):
        signed = sign_receipt(payload(), "key-expired", self.key_expired, self.registry, signed_at="2026-08-18T08:09:00Z")
        result = verify_signed_receipt(signed, self.registry, "tenant-a")
        self.assertTrue(result["authorized_attestation"])

    def test_22_registry_fingerprint_tampering_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["keys"]["key-a"]["public_key_fingerprint"] = h("tampered-registry-fingerprint")
        signed = sign_receipt(payload(), "key-a", self.key_a, self.registry)
        result = verify_signed_receipt(signed, registry, "tenant-a")
        self.assertIn("REGISTRY_FINGERPRINT_MISMATCH", result["signals"])


if __name__ == "__main__":
    unittest.main()
