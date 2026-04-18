#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from urllib.parse import urlparse
from jsonschema import Draft7Validator

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "angie_act.schema.json"

with open(SCHEMA_PATH) as f:
    schema = json.load(f)

validator = Draft7Validator(schema)

def is_absolute_uri(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False

def validate_file(path: Path):
    with open(path) as f:
        data = json.load(f)

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        for e in errors:
            print(f"INVALID (schema): {e.message}")
        return False

    # Rule 1
    if data["overall_verdict"] == "clean" and len(data["source_links"]) == 0:
        print("INVALID: clean verdict requires at least one source_link")
        return False

    # Rule 2
    if data["filters"]["evidence"]["score"] == 2 and len(data["source_links"]) < 3:
        print("INVALID: Evidence score 2 requires at least 3 source_links")
        return False

    # Rule 4
    if data["amy_flag"] and len(data.get("audit_notes", "")) < 20:
        print("INVALID: amy_flag is true but audit_notes is empty or <20 chars")
        return False

    # Rule 5
    for k, v in data["filters"].items():
        if "explanation" in v and len(v["explanation"].strip()) == 0:
            print(f"INVALID: {k} explanation is empty")
            return False

    # Rule 6
    for i, s in enumerate(data["source_links"]):
        if not is_absolute_uri(s["url"]):
            print(f"INVALID: source_links[{i}].url must be a valid absolute URI")
            return False

    # Rule 7 (MN)
    if data["filters"]["evidence"]["claim_type"] == "minnesota_state":
        if not any("mn.gov" in s["url"] or "revisor.mn.gov" in s["url"] for s in data["source_links"]):
            print("INVALID: Minnesota claims require at least one MN source")
            return False

    print("VALID")
    return True


def main():
    target = Path(sys.argv[1])
    if target.is_file():
        validate_file(target)
    else:
        for p in sorted(target.glob("*.json")):
            print(f"\n{p.name}:")
            validate_file(p)

if __name__ == "__main__":
    main()
