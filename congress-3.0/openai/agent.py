from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path

from agents import Agent, ModelSettings, Runner, function_tool

VERIFIER_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_congress_3_0.py"
spec = importlib.util.spec_from_file_location("congress_3_0_verifier", VERIFIER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load verifier from {VERIFIER_PATH}")
verifier_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier_module)


@function_tool
def verify_congress_3_0_case(case_json: str) -> str:
    """Run the deterministic Congress 3.0 verifier over one structured case JSON object.

    Args:
        case_json: Complete structured Congress 3.0 case JSON supplied by the user.
    """
    case = json.loads(case_json)
    receipt = verifier_module.verify(case)
    return json.dumps(receipt, sort_keys=True)


agent = Agent(
    name="Congress 3.0 Systems Accountability",
    instructions=(
        "You are a bounded intake surface for Congress 3.0 systems-accountability cases. "
        "Accept only structured case JSON supplied by the user. Pass that JSON to "
        "verify_congress_3_0_case exactly once. Do not invent missing receipts, authority, "
        "facts, legal conclusions, or government findings. The deterministic tool result is "
        "the final answer and must not be semantically widened."
    ),
    tools=[verify_congress_3_0_case],
    model_settings=ModelSettings(tool_choice="verify_congress_3_0_case"),
    tool_use_behavior="stop_on_first_tool",
)


async def main() -> None:
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: python agent.py '<case-json>'")

    result = await Runner.run(agent, sys.argv[1], max_turns=2)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
