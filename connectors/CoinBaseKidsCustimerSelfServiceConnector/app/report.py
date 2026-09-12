from __future__ import annotations
import json
from .full_math import denominator


def build_report(events):
    return {
        "object": "COINBASE_KIDS_CUSTOMER_SELF_SERVICE_FULL_MATH_REPORT_V0",
        "denominator": denominator(events),
        "events": [e.to_dict() for e in events],
        "controls": {
            "write": False,
            "trade": False,
            "transfer": False,
            "sign": False,
            "authority_created": False,
            "no_fake_green": True,
        },
    }


def save_report(events, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(build_report(events), f, indent=2)
