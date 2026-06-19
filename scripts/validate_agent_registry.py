#!/usr/bin/env python3
"""Validate JSONWisdom agent registry v0.1.

This validator intentionally treats AgentDefinition as the schema for one
agent entry and validates the registry wrapper separately.

Authority remains false. This script validates structure only.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

SCHEMA_URI = "https://jsonwisdom.org/schemas/AgentDefinition/v0.1"
ISSUE_310 = "https://github.com/jsonwisdom/COMPUTERWISDOM/issues/310"
AGENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
EXPECTED_AGENTS = {"navigator", "custody", "replay", "ci-gate", "clerk"}


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise SystemExit(f"FAILED to load {path}: {exc}") from exc


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"VALIDATION_FAILED: {message}")


def require_string(value: Any, field: str) -> None:
    require(isinstance(value, str) and len(value) > 0, f"{field} must be a non-empty string")


def validate_agent(agent: Dict[str, Any], index: int) -> str:
    allowed = {"agent_id", "purpose", "inputs", "outputs", "authority", "manifest_issue", "activated_at"}
    extra = set(agent) - allowed
    require(not extra, f"agent[{index}] has additional properties: {sorted(extra)}")

    require_string(agent.get("agent_id"), f"agent[{index}].agent_id")
    agent_id = agent["agent_id"]
    require(bool(AGENT_ID_RE.match(agent_id)), f"agent[{index}].agent_id has invalid format: {agent_id}")

    require_string(agent.get("purpose"), f"agent[{index}].purpose")
    require(agent.get("authority") is False, f"agent[{index}].authority must be false")

    for field in ("inputs", "outputs"):
        value = agent.get(field, [])
        require(isinstance(value, list), f"agent[{index}].{field} must be an array")
        require(all(isinstance(item, str) for item in value), f"agent[{index}].{field} items must be strings")

    if "manifest_issue" in agent:
        require(agent["manifest_issue"] == ISSUE_310, f"agent[{index}].manifest_issue must link to #310")

    if "activated_at" in agent:
        require_string(agent["activated_at"], f"agent[{index}].activated_at")

    return agent_id


def validate_registry(registry: Dict[str, Any]) -> None:
    allowed = {"schema", "registered_at", "agents"}
    extra = set(registry) - allowed
    require(not extra, f"registry has additional properties: {sorted(extra)}")

    require(registry.get("schema") == SCHEMA_URI, "registry.schema must reference AgentDefinition v0.1")
    require_string(registry.get("registered_at"), "registry.registered_at")

    agents = registry.get("agents")
    require(isinstance(agents, list), "registry.agents must be an array")
    require(len(agents) > 0, "registry.agents must not be empty")
    require(all(isinstance(agent, dict) for agent in agents), "registry.agents items must be objects")

    seen: List[str] = []
    for index, agent in enumerate(agents):
        seen.append(validate_agent(agent, index))

    require(len(seen) == len(set(seen)), "agent_id values must be unique")
    require(set(seen) == EXPECTED_AGENTS, f"registry agent set mismatch: observed={sorted(seen)}")


def main() -> int:
    schema_path = Path("schemas/AgentDefinition.schema.json")
    registry_path = Path("agents/registry.json")

    schema = load_json(schema_path)
    registry = load_json(registry_path)

    require(schema.get("$id") == SCHEMA_URI, "schema $id must match expected AgentDefinition URI")
    require(schema.get("type") == "object", "AgentDefinition schema must describe an object")
    require(schema.get("properties", {}).get("authority", {}).get("const") is False, "AgentDefinition authority must be const false")

    validate_registry(registry)

    print("VALIDATION_PASSED: JSONWisdom agent registry v0.1")
    print("authority=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
