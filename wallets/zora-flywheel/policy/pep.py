"""Policy enforcement point for the shelf attribute policy.

The point asks the policy, then allows only a registered local handler.
Spend, sign, trade, and transfer have no handler.
"""

from __future__ import annotations

from abac_policy import decide


class EnforcementDenied(Exception):
    def __init__(self, decision: dict):
        self.decision = decision
        super().__init__(decision["reason"])


class PolicyEnforcementPoint:
    def __init__(self, handlers: dict | None = None):
        self.handlers = dict(handlers or {})
        for blocked in ("spend", "sign", "trade", "transfer"):
            self.handlers.pop(blocked, None)

    def enforce(self, request: dict):
        decision = decide(request)
        if decision["decision"] != "ALLOW":
            raise EnforcementDenied(decision)
        action = request.get("action")
        handler = self.handlers.get(action)
        if handler is None:
            raise EnforcementDenied(
                {
                    "decision": "DENY",
                    "reason": "NO_HANDLER",
                    "fields": [action],
                    "authority_created": False,
                    "spend": False,
                }
            )
        result = handler(request)
        return {
            "decision": decision,
            "result": result,
            "authority_created": False,
            "spend": False,
        }
