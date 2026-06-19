#!/usr/bin/env python3
"""Runtime harness for constitution v0.1 executable replay."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    cmd = [sys.executable, "court/judge_breaker.py"]
    result = subprocess.run(cmd, text=True, capture_output=True)
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.returncode != 0:
        return result.returncode

    output = Path("receipts/executable-selftest/selftest_output.txt").read_text()
    required = [
        "CASE_0007 PASS",
        "CASE_0008 PASS",
        "CASE_0009 PASS",
        "CASE_0010 PASS",
        "CASE_0011 PASS",
        "CASE_0012 PASS",
        "CASE_0013 PASS",
        "BORING_REPLAY_STREAK=7",
        "ROOT_MATCH=TRUE",
        "REPLAY_RECEIPTS_MATCH=TRUE",
        "RESULT=EXECUTABLE_REPLAY_PRESERVED",
        "VERDICT=REPLAY_PRESERVED",
    ]
    missing = [item for item in required if item not in output]
    if missing:
        print("Executable replay missing expected lines:", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
