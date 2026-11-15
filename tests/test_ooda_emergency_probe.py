"""CI-FIRST mechanical checks. Synthetic fixtures are NOT external reachability proof."""
import base64
import copy
import json
import unittest
from scripts.ooda_emergency_probe import canonical, sha, verify_receipt

def receipt():
    body = json.dumps({
        "status": "OK", "schema": "cw-ooda-emergency-estate/0.1",
        "state_count": 50, "source_bundles_verified": 0,
        "authority_created": False, "live_alerts": False
    }, separators=(",", ":")).encode("utf-8")
    routes = [
        {"role": role, "http": 200, "status": "PASS",
         "body_sha256": sha(body), "body_base64": base64.b64encode(body).decode(),
         "schema": "cw-ooda-emergency-estate/0.1", "state_count": 50}
        for role in ("PRIMARY", "REPLICA")
    ]
    d = {"schema": "cw-dual-route-probe/0.2", "routes": routes,
         "authority_created": False, "live_emergency_feed": "NOT_ESTABLISHED",
         "cross_provider_failover": "NOT_ESTABLISHED"}
    return sign(d)

def sign(d):
    d["canonical_sha256"] = sha(canonical(
        {k: v for k, v in d.items() if k != "canonical_sha256"}
    ).encode("utf-8"))
    return d

class TestCI(unittest.TestCase):
    def test_synthetic_valid_receipt(self):
        self.assertTrue(verify_receipt(receipt()))
    def test_tampered_receipt_rejected(self):
        d = receipt()
        d["routes"][0]["http"] = 503
        self.assertFalse(verify_receipt(d))
    def test_recomputed_hash_cannot_hide_body_tamper(self):
        d = receipt()
        d["routes"][0]["body_base64"] = base64.b64encode(b'{"status":"FAILED"}').decode()
        sign(d)
        self.assertFalse(verify_receipt(d))
    def test_recomputed_hash_cannot_inflate_state_claim(self):
        d = receipt()
        d["routes"][0]["state_count"] = 51
        sign(d)
        # Route status needs to be bound to original HTTP body, not just claimed state_count.
        self.assertFalse(verify_receipt(d))
    def test_authority_inflation_rejected(self):
        d = receipt()
        d["authority_created"] = True
        sign(d)
        self.assertFalse(verify_receipt(d))

if __name__ == "__main__":
    unittest.main()
