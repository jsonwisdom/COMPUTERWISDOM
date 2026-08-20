from __future__ import annotations

import asyncio
import importlib.util
import json
from pathlib import Path

from agents import Agent, ModelSettings, Runner, function_tool

VERIFIER_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_banking_burden_flip_v0_1.py"
spec = importlib.util.spec_from_file_location("banking_burden_flip_verifier", VERIFIER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load verifier from {VERIFIER_PATH}")
verifier_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier_module)


@function_tool
def verify_banking_burden_flip(case_json: str) -> str:
    """Run the deterministic Citizen Banking Burden Flip verifier over one structured case.

    Args:
        case_json: Complete structured banking burden-flip case JSON supplied by the user.
    """
    case = json.loads(case_json)
    receipt = verifier_module.verify(case)
    return json.dumps(receipt, sort_keys=True)


agent = Agent(
    name="Congress 3.0 Citizen Banking Burden Flip",
    instructions=(
        "You are a bounded intake surface for Citizen Banking Burden Flip cases. "
        "Accept only structured case JSON supplied by the user. Pass it to "
        "verify_banking_burden_flip exactly once. Do not invent statutory triggers, "
        "actor classifications, deadlines, government attribution, legal conclusions, "
        "or constitutional findings. The deterministic tool receipt is final and must "
        "not be semantically widened."
    ),
    tools=[verify_banking_burden_flip],
    model_settings=ModelSettings(tool_choice="verify_banking_burden_flip"),
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
