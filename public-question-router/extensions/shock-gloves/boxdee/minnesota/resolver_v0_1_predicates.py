"""RESOLVER_V0_1 predicate bodies.

Pure applicability checks only.
No authority creation. No legal/factual adjudication.
SHAPE_ONLY / NON_SEMANTIC inputs fail closed to HOLD.
"""

from datetime import datetime, timezone

PASS = "PASS"
FAIL = "FAIL"
HOLD = "HOLD"
CONFLICT = "CONFLICT"


def _result(status, reason, details=None):
    return {
        "status": status,
        "reason": reason,
        "details": details or {},
        "authority_created": False,
        "verdict_created": False,
        "predicate_truth_created": False,
    }


def _shape_only(value):
    if value is None:
        return False
    if isinstance(value, str):
        return value.startswith("SHAPE_ONLY") or value.startswith("fixture://shape/")
    if isinstance(value, list):
        return any(_shape_only(v) for v in value)
    if isinstance(value, dict):
        if value.get("shape_only") is True:
            return True
        if value.get("semantic_class") == "NON_SEMANTIC":
            return True
        if value.get("binding_class") == "SHAPE_ONLY":
            return True
        return any(_shape_only(v) for v in value.values())
    return False


def _guard(inputs):
    if not isinstance(inputs, dict):
        return _result(HOLD, "inputs must be an object")
    if _shape_only(inputs):
        return _result(HOLD, "NON_SEMANTIC / SHAPE_ONLY input cannot support a semantic outcome")
    receipts = inputs.get("receipts")
    if not receipts:
        return _result(HOLD, "required receipts are absent")
    return None


def _parse_time(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        v = value[:-1] + "+00:00" if value.endswith("Z") else value
        dt = datetime.fromisoformat(v)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def _exact_member(value, rules):
    if not isinstance(rules, list):
        return None
    return value in rules


def check_R1_SOURCE_IDENTITY(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    source_id = inputs.get("authority_source_id")
    sources = inputs.get("authority_sources")
    if source_id is None or not isinstance(sources, list):
        return _result(HOLD, "source identity inputs are incomplete")
    return _result(PASS if source_id in sources else FAIL,
                   "authority source is listed" if source_id in sources else "authority source is not listed")


def check_R2_JURISDICTION_SCOPE(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    domain = inputs.get("event_domain")
    scope = inputs.get("scope")
    if domain is None or not isinstance(scope, list):
        return _result(HOLD, "jurisdiction scope inputs are incomplete")
    return _result(PASS if domain in scope else FAIL,
                   "event domain is in scope" if domain in scope else "event domain is outside scope")


def check_R3_TEMPORAL_APPLICABILITY(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    event_time = _parse_time(inputs.get("event_time"))
    valid_from = _parse_time(inputs.get("valid_from"))
    valid_to = _parse_time(inputs.get("valid_to"))
    if None in (event_time, valid_from, valid_to):
        return _result(HOLD, "temporal inputs are missing or malformed")
    inside = valid_from <= event_time <= valid_to
    return _result(PASS if inside else FAIL,
                   "event time is inside validity window" if inside else "event time is outside validity window")


def check_R4_ACTOR_APPLICABILITY(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    actor = inputs.get("actor")
    matched = _exact_member(actor, inputs.get("actor_rules"))
    if actor is None or matched is None:
        return _result(HOLD, "actor applicability inputs are incomplete")
    return _result(PASS if matched else FAIL,
                   "actor exactly matches an actor rule" if matched else "actor does not match actor rules")


def check_R5_SUBJECT_APPLICABILITY(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    subject = inputs.get("subject")
    matched = _exact_member(subject, inputs.get("subject_rules"))
    if subject is None or matched is None:
        return _result(HOLD, "subject applicability inputs are incomplete")
    return _result(PASS if matched else FAIL,
                   "subject exactly matches a subject rule" if matched else "subject does not match subject rules")


def check_R6_ACTION_APPLICABILITY(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    action = inputs.get("action")
    matched = _exact_member(action, inputs.get("action_rules"))
    if action is None or matched is None:
        return _result(HOLD, "action applicability inputs are incomplete")
    return _result(PASS if matched else FAIL,
                   "action exactly matches an action rule" if matched else "action does not match action rules")


def check_R7_DELEGATION_AUTHORIZATION(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    delegation = inputs.get("delegation")
    actor = inputs.get("actor")
    action = inputs.get("action")
    if not isinstance(delegation, dict) or not isinstance(delegation.get("authorized"), bool):
        return _result(HOLD, "delegation must explicitly provide authorized=true|false")
    if "actor" in delegation and delegation["actor"] != actor:
        return _result(FAIL, "delegation actor does not match event actor")
    if "action" in delegation and delegation["action"] != action:
        return _result(FAIL, "delegation action does not match event action")
    return _result(PASS if delegation["authorized"] else FAIL,
                   "delegation explicitly authorizes the action" if delegation["authorized"] else "delegation explicitly does not authorize the action")


def _applies_state(items):
    if items is None:
        return None
    if not isinstance(items, list):
        return None
    states = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("applies"), bool):
            return None
        states.append(item["applies"])
    return states


def check_R8_LIMIT_EXCEPTION_CHECK(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    limit_states = _applies_state(inputs.get("limits"))
    exception_states = _applies_state(inputs.get("exceptions"))
    if limit_states is None or exception_states is None or not isinstance(inputs.get("event"), dict):
        return _result(HOLD, "limit/exception applicability is incomplete or malformed")
    blocked = any(limit_states) or any(exception_states)
    return _result(FAIL if blocked else PASS,
                   "an applicable limit or exception blocks the action" if blocked else "no applicable limit or exception blocks the action")


def check_R9_PROCEDURAL_TRIGGER(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    rules = inputs.get("trigger_rules")
    if not isinstance(rules, list) or not rules or not isinstance(inputs.get("event"), dict):
        return _result(HOLD, "procedural trigger inputs are incomplete")
    states = []
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("satisfied"), bool):
            return _result(HOLD, "each procedural trigger must explicitly provide satisfied=true|false")
        states.append(rule["satisfied"])
    satisfied = all(states)
    return _result(PASS if satisfied else FAIL,
                   "all required procedural triggers are satisfied" if satisfied else "one or more required procedural triggers are not satisfied")


def check_R10_VERSION_SUPERSESSION(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    version = inputs.get("authority_version")
    event_time = _parse_time(inputs.get("event_time"))
    supersession = inputs.get("supersession")
    if version is None or event_time is None or not isinstance(supersession, dict):
        return _result(HOLD, "version/supersession inputs are incomplete or malformed")
    superseded = supersession.get("superseded")
    if not isinstance(superseded, bool):
        return _result(HOLD, "supersession must explicitly provide superseded=true|false")
    if not superseded:
        return _result(PASS, "authority version is explicitly current")
    effective_at = _parse_time(supersession.get("effective_at"))
    if effective_at is None:
        return _result(HOLD, "supersession is asserted but effective_at is missing or malformed")
    return _result(FAIL if effective_at <= event_time else PASS,
                   "authority version was superseded before the event" if effective_at <= event_time else "supersession occurs after the event")


def check_R11_STATE_CONFLICT(inputs):
    guard = _guard(inputs)
    if guard:
        return guard
    claim = inputs.get("claim_object")
    runtime_state = inputs.get("runtime_state")
    if not isinstance(claim, dict) or not isinstance(runtime_state, dict):
        return _result(HOLD, "claim/runtime state inputs are incomplete")
    if "state" not in claim or "state" not in runtime_state:
        return _result(HOLD, "claim.state and runtime_state.state are required")
    same = claim["state"] == runtime_state["state"]
    return _result(PASS if same else CONFLICT,
                   "runtime state is consistent with claim state" if same else "runtime state conflicts with claim state")


predicate_registry = {
    "R1": check_R1_SOURCE_IDENTITY,
    "R2": check_R2_JURISDICTION_SCOPE,
    "R3": check_R3_TEMPORAL_APPLICABILITY,
    "R4": check_R4_ACTOR_APPLICABILITY,
    "R5": check_R5_SUBJECT_APPLICABILITY,
    "R6": check_R6_ACTION_APPLICABILITY,
    "R7": check_R7_DELEGATION_AUTHORIZATION,
    "R8": check_R8_LIMIT_EXCEPTION_CHECK,
    "R9": check_R9_PROCEDURAL_TRIGGER,
    "R10": check_R10_VERSION_SUPERSESSION,
    "R11": check_R11_STATE_CONFLICT,
}
