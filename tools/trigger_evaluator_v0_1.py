"""
tools/trigger_evaluator_v0_1.py
Receipt-gated trigger evaluator for watch_trigger_engine_v0_1
Enforces strict binary: MAINTAIN / OBSERVE / TRANSITION_READY
"""

from typing import Dict, Any


class TriggerEvaluator:
    def __init__(self, trigger_schema: Dict[str, Any], receipt_schema: Dict[str, Any]):
        self.trigger_schema = trigger_schema
        self.receipt_schema = receipt_schema
        self.authority = False

    def evaluate(self, trigger: Dict[str, Any], receipt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate trigger against receipt per binary state table.

        States:
        - MAINTAIN: domain mismatch or receipt missing critical fields
        - OBSERVE: domain matches but artifact_type mismatch or unverified
        - TRANSITION_READY: domain + artifact_type match + verified true

        state_transition is True ONLY in TRANSITION_READY.
        No fourth state exists.
        """
        result = {
            "status": "MAINTAIN",
            "state_transition": False,
            "from_level": None,
            "to_level": None,
            "authority": False,
        }

        trigger_domain = trigger.get("source_domain")
        trigger_artifact_type = trigger.get("artifact_type")
        trigger_transition = trigger.get("state_transition", {})
        from_level = trigger_transition.get("from_level")
        to_level = trigger_transition.get("to_level")

        receipt_domain = receipt.get("source_domain")
        receipt_artifact_type = receipt.get("artifact_type")
        receipt_verified = receipt.get("verified", False)

        if trigger_domain != receipt_domain:
            result["status"] = "MAINTAIN"
            result["state_transition"] = False
            return result

        if trigger_artifact_type != receipt_artifact_type or not receipt_verified:
            result["status"] = "OBSERVE"
            result["state_transition"] = False
            return result

        if (
            trigger_domain == receipt_domain
            and trigger_artifact_type == receipt_artifact_type
            and receipt_verified is True
        ):
            result["status"] = "TRANSITION_READY"
            result["state_transition"] = True
            result["from_level"] = from_level
            result["to_level"] = to_level
            return result

        result["status"] = "MAINTAIN"
        result["state_transition"] = False
        return result
