"""Fail-closed v0.2 -> v0.3 migration gate. Preservation only; no semantic promotion."""
from __future__ import annotations
import hashlib, json

def canonical_bytes(obj):
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def sha256_bytes(data): return hashlib.sha256(data).hexdigest()

def build_v0_3_source(source_obj, exact_source_bytes):
    return {"schema_version":"0.3","source_type":source_obj["source_type"],"execution_subtype":source_obj["execution_subtype"],"execution":{"provider":source_obj["provider"],"workflow_name":source_obj["workflow_name"],"run_id":source_obj["run_id"],"run_number":source_obj["run_number"],"head_sha":source_obj["head_sha"],"result":source_obj["result"].lower()},"source_receipt_hash":sha256_bytes(exact_source_bytes),"evidence_state":source_obj["evidence_state"],"scope":source_obj["scope"],"limitations":source_obj["limitations"],"external_witness":None,"allowed_resume_language":source_obj["allowed_resume_language"],"production_proof_created":source_obj["production_proof_created"],"employment_created":source_obj["employment_created"],"authority_created":source_obj["authority_created"]}

def preservation_gate(source_obj,target_obj,exact_source_bytes):
    checks={"source_hash_match":target_obj["source_receipt_hash"]==sha256_bytes(exact_source_bytes),"execution_identity_preserved":target_obj["execution"]=={"provider":source_obj["provider"],"workflow_name":source_obj["workflow_name"],"run_id":source_obj["run_id"],"run_number":source_obj["run_number"],"head_sha":source_obj["head_sha"],"result":source_obj["result"].lower()},"evidence_state_unchanged":target_obj["evidence_state"]==source_obj["evidence_state"],"production_flag_unchanged":target_obj["production_proof_created"]==source_obj["production_proof_created"],"employment_flag_unchanged":target_obj["employment_created"]==source_obj["employment_created"],"authority_flag_unchanged":target_obj["authority_created"]==source_obj["authority_created"]}
    return checks,("PASS" if all(checks.values()) else "REJECT")
