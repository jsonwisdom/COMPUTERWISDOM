"""Replay v0.3 structural normalizer. No semantic evidence decisions."""
from __future__ import annotations
import copy, re

TOP_LEVEL_KEYS_V0_3={"schema_version","source_type","execution_subtype","execution","source_receipt_hash","evidence_state","scope","limitations","external_witness","allowed_resume_language","production_proof_created","employment_created","authority_created"}
EXECUTION_KEYS={"provider","workflow_name","run_id","run_number","head_sha","result"}
EXECUTION_SUBTYPES={"CI_RUN","ATTESTATION_RUN","VERIFIER_RUN","DEPLOYMENT_RECEIPT","LIVE_SYSTEM_OPERATION"}
class NormalizationError(ValueError): pass

def _clean_string(v,field):
    if not isinstance(v,str): raise NormalizationError(f"{field}: expected string")
    v=" ".join(v.split())
    if not v: raise NormalizationError(f"{field}: empty")
    return v

def _string_list(v,field):
    if not isinstance(v,list): raise NormalizationError(f"{field}: expected list")
    out=[]
    for i,x in enumerate(v):
        x=_clean_string(x,f"{field}[{i}]")
        if x not in out: out.append(x)
    return out

def _bool(v,field):
    if type(v) is not bool: raise NormalizationError(f"{field}: expected boolean")
    return v

def normalize_execution_v0_3(value):
    if not isinstance(value,dict): raise NormalizationError("execution: expected object")
    unknown=set(value)-EXECUTION_KEYS
    if unknown: raise NormalizationError(f"execution: unknown fields {sorted(unknown)}")
    missing=EXECUTION_KEYS-set(value)
    if missing: raise NormalizationError(f"execution: missing fields {sorted(missing)}")
    for f in ("run_id","run_number"):
        if type(value[f]) is not int or value[f] < 1: raise NormalizationError(f"execution.{f}: expected positive integer")
    return {"provider":_clean_string(value["provider"],"execution.provider"),"workflow_name":_clean_string(value["workflow_name"],"execution.workflow_name"),"run_id":value["run_id"],"run_number":value["run_number"],"head_sha":_clean_string(value["head_sha"],"execution.head_sha"),"result":_clean_string(value["result"],"execution.result").lower()}

def normalize_v0_3(raw_input):
    if not isinstance(raw_input,dict): raise NormalizationError("raw_input: expected object")
    if raw_input.get("schema_version")!="0.3": raise NormalizationError("schema_version: v0.3 normalizer accepts only 0.3")
    unknown=set(raw_input)-TOP_LEVEL_KEYS_V0_3
    if unknown: raise NormalizationError(f"raw_input: unknown fields {sorted(unknown)}")
    source_type=_clean_string(raw_input["source_type"],"source_type").upper()
    is_exec=source_type=="EXECUTION_RECEIPT"
    fields=("execution_subtype","execution","source_receipt_hash")
    if is_exec and any(f not in raw_input for f in fields): raise NormalizationError("execution receipt requires execution_subtype, execution, source_receipt_hash")
    if not is_exec and any(f in raw_input for f in fields): raise NormalizationError("execution fields forbidden for non-execution source")
    out={"schema_version":"0.3","source_type":source_type,"evidence_state":_clean_string(raw_input["evidence_state"],"evidence_state"),"scope":_string_list(raw_input["scope"],"scope"),"limitations":_string_list(raw_input["limitations"],"limitations"),"external_witness":copy.deepcopy(raw_input.get("external_witness")),"allowed_resume_language":_clean_string(raw_input["allowed_resume_language"],"allowed_resume_language"),"production_proof_created":_bool(raw_input["production_proof_created"],"production_proof_created"),"employment_created":_bool(raw_input["employment_created"],"employment_created"),"authority_created":_bool(raw_input["authority_created"],"authority_created")}
    if is_exec:
        subtype=_clean_string(raw_input["execution_subtype"],"execution_subtype").upper()
        if subtype not in EXECUTION_SUBTYPES: raise NormalizationError("execution_subtype: unsupported")
        h=_clean_string(raw_input["source_receipt_hash"],"source_receipt_hash").lower()
        if not re.fullmatch(r"[0-9a-f]{64}",h): raise NormalizationError("source_receipt_hash: invalid sha256")
        out["execution_subtype"]=subtype; out["execution"]=normalize_execution_v0_3(raw_input["execution"]); out["source_receipt_hash"]=h
    return out
