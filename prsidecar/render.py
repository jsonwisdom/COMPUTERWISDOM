"""Deterministic PRSideCar renderer. Source truth is input. Output is a projection."""
from __future__ import annotations

import hashlib
import json

SCHEMA_VERSION = "prsidecar.v0"
REQUIRED = (
    "schema_version",
    "repo",
    "pr_number",
    "head_sha",
    "base_sha",
    "merge_state",
    "changed_paths",
    "evidence_refs",
    "receipt_refs",
    "typing",
    "unresolved_conflicts",
    "identity_binding",
    "authority_created",
    "replay_pointer",
    "renderer",
)

def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def render(source: dict) -> dict:
    if source.get("authority_created") is not False:
        raise ValueError("authority_created must be false")
    if source.get("identity_binding") != "HOLD":
        raise ValueError("identity_binding must remain HOLD")
    paths = sorted(source["changed_paths"])
    sidecar = {
        "schema_version": SCHEMA_VERSION,
        "repo": source["repo"],
        "pr_number": source["pr_number"],
        "head_sha": source["head_sha"],
        "base_sha": source["base_sha"],
        "merge_state": source["merge_state"],
        "changed_paths": paths,
        "evidence_refs": list(source["evidence_refs"]),
        "receipt_refs": list(source["receipt_refs"]),
        "typing": list(source["typing"]),
        "unresolved_conflicts": list(source["unresolved_conflicts"]),
        "identity_binding": "HOLD",
        "authority_created": False,
        "replay_pointer": source["replay_pointer"],
        "renderer": {
            "name": "prsidecar.render",
            "role": "PROJECTION",
            "source_is_not_output": True,
            "ens_binding": "NOT_IN_THIS_SLICE",
            "public_renderer_host": "UNVERIFIED",
        },
    }
    missing = [k for k in REQUIRED if k not in sidecar]
    if missing:
        raise ValueError("missing " + ",".join(missing))
    body = {k: sidecar[k] for k in sidecar if k != "renderer"}
    sidecar["renderer"]["source_projection_sha256"] = sha256(canonical(body))
    frozen = dict(sidecar)
    frozen["renderer"] = dict(sidecar["renderer"])
    frozen["renderer"].pop("sidecar_sha256", None)
    sidecar["renderer"]["sidecar_sha256"] = sha256(canonical(frozen))
    return sidecar

def receipt(source: dict, sidecar: dict) -> dict:
    return {
        "kind": "PRSIDECAR_RECEIPT",
        "schema_version": SCHEMA_VERSION,
        "repo": source["repo"],
        "pr_number": source["pr_number"],
        "head_sha": source["head_sha"],
        "base_sha": source["base_sha"],
        "source_observation": source["source_observation"],
        "sidecar_sha256": sidecar["renderer"]["sidecar_sha256"],
        "source_projection_sha256": sidecar["renderer"]["source_projection_sha256"],
        "renderer_is_not_source": True,
        "identity_binding": "HOLD",
        "authority_created": False,
        "ens_contenthash": "NOT_CHECKED",
        "eth_limo_readback": "NOT_CHECKED",
    }
