"""Execute prsidecar/schema.json against a sidecar object. No third-party schema library."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "schema.json"

def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())

def validate(instance: dict, schema: dict | None = None) -> None:
    schema = schema if schema is not None else load_schema()
    if schema.get("type") == "object" and not isinstance(instance, dict):
        raise ValueError("instance is not an object")
    required = schema.get("required", [])
    missing = [k for k in required if k not in instance]
    if missing:
        raise ValueError("missing " + ",".join(missing))
    if schema.get("additionalProperties") is False:
        extra = [k for k in instance if k not in schema.get("properties", {})]
        if extra:
            raise ValueError("extra " + ",".join(sorted(extra)))
    props = schema.get("properties", {})
    for key, rule in props.items():
        if key not in instance:
            continue
        value = instance[key]
        if "const" in rule and value != rule["const"]:
            raise ValueError(f"{key} const mismatch")
        expected = rule.get("type")
        if expected == "string" and not isinstance(value, str):
            raise ValueError(f"{key} not string")
        if expected == "integer" and not isinstance(value, int):
            raise ValueError(f"{key} not integer")
        if expected == "array" and not isinstance(value, list):
            raise ValueError(f"{key} not array")
        if expected == "object" and not isinstance(value, dict):
            raise ValueError(f"{key} not object")
