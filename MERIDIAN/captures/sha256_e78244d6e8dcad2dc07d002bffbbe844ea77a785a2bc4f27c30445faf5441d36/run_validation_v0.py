#!/usr/bin/env python3
# run_validation_v0.py
# Deterministic harness for captured Meridian validator inputs.
# Emits JSON only. No network. No enrichment. No evidence promotion.

import argparse
import importlib.util
import json
from pathlib import Path
import yaml


def load_yaml(path):
    return yaml.safe_load(Path(path).read_bytes())


def load_validator(path):
    spec = importlib.util.spec_from_file_location("meridian_validator", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def find_vector(manifest, vector_id):
    for v in manifest.get("vectors", []):
        if v.get("id") == vector_id:
            return v
        for sub in v.get("subcases", []) or []:
            if sub.get("id") == vector_id:
                return sub
    raise KeyError(vector_id)


def registered_codes(doc, top, key="codes"):
    return {
        x.get("code")
        for x in doc.get(top, {}).get(key, [])
        if isinstance(x, dict) and isinstance(x.get("code"), str)
    }


def run_one(validator, manifest, vector_id, fixture_doc):
    vector = find_vector(manifest, vector_id)
    if vector_id == "V3":
        event = {}
        registry = {}
    else:
        fixture = fixture_doc["fixture"]
        event = fixture.get("candidate", fixture.get("target", {}))
        registry = fixture.get("registry", {})
    result = validator.run_vector(vector, event, registry)
    return {
        "vector_id": vector_id,
        "outcome": result.result,
        "failure_code": result.error_code,
        "skip_code": result.reason if result.result == "skip" else None,
        "reason": result.reason,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validator", required=True)
    ap.add_argument("--vectors", required=True)
    ap.add_argument("--failure-registry", required=True)
    ap.add_argument("--skip-registry", required=True)
    ap.add_argument("--v7", required=True)
    ap.add_argument("--v13a", required=True)
    ap.add_argument("--v13b", required=True)
    args = ap.parse_args()

    validator = load_validator(args.validator)
    manifest = load_yaml(args.vectors)
    failure_doc = load_yaml(args.failure_registry)
    skip_doc = load_yaml(args.skip_registry)

    failure_codes = registered_codes(failure_doc, "failure_code_registry")
    skip_codes = registered_codes(skip_doc, "skip_code_registry")

    docs = {
        "V3": {},
        "V7": load_yaml(args.v7),
        "V13a": load_yaml(args.v13a),
        "V13b": load_yaml(args.v13b),
    }

    results = [
        run_one(validator, manifest, vid, docs[vid])
        for vid in ("V3", "V7", "V13a", "V13b")
    ]

    meta_failures = []
    for r in results:
        if r["failure_code"] and r["failure_code"] not in failure_codes:
            meta_failures.append({
                "vector_id": r["vector_id"],
                "code": "UNREGISTERED_FAILURE_CODE",
                "value": r["failure_code"],
            })
        if r["skip_code"] and r["skip_code"] not in skip_codes:
            meta_failures.append({
                "vector_id": r["vector_id"],
                "code": "UNREGISTERED_SKIP_CODE",
                "value": r["skip_code"],
            })

    summary = {
        "pass": sum(r["outcome"] == "pass" for r in results),
        "fail": sum(r["outcome"] == "fail" for r in results),
        "skip": sum(r["outcome"] == "skip" for r in results),
        "meta_fail": len(meta_failures),
    }

    out = {
        "results": results,
        "summary": summary,
        "meta_failures": meta_failures,
    }
    print(json.dumps(out, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
