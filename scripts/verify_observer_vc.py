#!/usr/bin/env python3
import json, sys, hashlib
from pathlib import Path

REQ = {
  "OBSERVER_IS_NOT_OFFICE",
  "MEDIA_REPORT_IS_NOT_BINDING_LAW",
  "ADVISORY_APPOINTMENT_IS_NOT_EXECUTIVE_ORDER",
  "CORROBORATION_IS_NOT_AUTHORITY"
}
PLACEHOLDER = "UNSIGNED_PLACEHOLDER_DO_NOT_TREAT_AS_VALID"
HASH_PLACEHOLDER = "REPLACE_WITH_SHA256_OF_REGISTRY_JSON"

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

if len(sys.argv) != 2:
    fail("usage: verify_observer_vc.py <vc.json>")

path = Path(sys.argv[1])
vc = json.loads(path.read_text())
sub = vc.get("credentialSubject", {})
claims = sub.get("claims", {})
delegation = sub.get("delegation", {})
proof = vc.get("proof", {})

if vc.get("status") == "UNSIGNED_DRAFT" and proof.get("proofValue") != PLACEHOLDER:
    fail("UNSIGNED_DRAFT must use unsigned placeholder proofValue")

if vc.get("status") == "SIGNED_ACTIVE":
    if proof.get("proofValue") == PLACEHOLDER:
        fail("SIGNED_ACTIVE cannot use placeholder proofValue")
    if not vc.get("issuer", {}).get("id"):
        fail("SIGNED_ACTIVE requires issuer.id")

if delegation.get("authority") != "NONE":
    fail("delegation authority must be NONE")

if claims.get("is_federal_authority") is not False:
    fail("is_federal_authority must be false")

missing = REQ - set(sub.get("invariants", []))
if missing:
    fail(f"missing invariants: {sorted(missing)}")

if claims.get("writes") != "APPEND_ONLY_RECEIPTS":
    fail("writes must be APPEND_ONLY_RECEIPTS")

if claims.get("public_sources_only") is not True:
    fail("public_sources_only must be true")

reg = sub.get("registry", {})
reg_hash = reg.get("registry_hash")
if reg_hash and reg_hash != HASH_PLACEHOLDER:
    reg_path = (path.parent / reg.get("registry_path")).resolve()
    actual = hashlib.sha256(reg_path.read_bytes()).hexdigest()
    if actual != reg_hash:
        fail(f"registry_hash mismatch expected={reg_hash} actual={actual}")

print("PASS")
