"""Fail-closed attribute policy for the purposeful wallet shelf.

This evaluates declarations. It does not sign, spend, or grant control.
"""

from __future__ import annotations

DENY = "DENY"
ALLOW = "ALLOW"

SPEND_ACTIONS = {"spend", "sign", "trade", "transfer"}
APPEND_ACTIONS = {"append_leaf", "append_edge"}


def decide(request: dict) -> dict:
    subject = request.get("subject") or {}
    obj = request.get("object") or {}
    action = request.get("action")
    context = request.get("context") or {}
    missing = [
        name
        for name, value in (
            ("action", action),
            ("subject.seat", subject.get("seat")),
            ("object.kind", obj.get("kind")),
        )
        if not value
    ]
    if missing:
        return _deny("MISSING_ATTRIBUTE", missing)

    if action in SPEND_ACTIONS:
        return _deny("SPEND_NOT_GRANTED_BY_POLICY", [action])
    if obj.get("coinbase_baseline") is True:
        return _deny("COINBASE_EXCLUDED", ["object.coinbase_baseline"])
    if action == "grant_family_seat" or obj.get("kind") == "family_seat":
        if context.get("sister_answered") is not True:
            return _deny("SISTER_UNANSWERED", ["context.sister_answered"])
    if action == "promote":
        return _deny("PROMOTION_CLOSED", ["action"])
    if action in APPEND_ACTIONS and obj.get("kind") == "prior_receipt":
        return _deny("PRIOR_RECEIPT_NOT_EDITABLE", ["object.kind"])
    if action == "append_forest" and obj.get("leaf_complete") is not True:
        return _deny("LEAF_INCOMPLETE", ["object.leaf_complete"])
    if action == "bind_control" and obj.get("control_proven") is not True:
        return _deny("CONTROL_NOT_PROVEN", ["object.control_proven"])
    if subject.get("seat") == "reader" and action != "read":
        return _deny("READER_READ_ONLY", ["subject.seat", "action"])
    if action == "read":
        return _allow("READ_ALLOWED")
    if action in APPEND_ACTIONS and subject.get("seat") == "appender":
        return _allow("APPEND_ALLOWED")
    return _deny("NO_MATCHING_RULE", ["action", "subject.seat"])


def _deny(reason: str, fields: list[str]) -> dict:
    return {
        "decision": DENY,
        "reason": reason,
        "fields": fields,
        "authority_created": False,
        "spend": False,
    }


def _allow(reason: str) -> dict:
    return {
        "decision": ALLOW,
        "reason": reason,
        "fields": [],
        "authority_created": False,
        "spend": False,
    }
