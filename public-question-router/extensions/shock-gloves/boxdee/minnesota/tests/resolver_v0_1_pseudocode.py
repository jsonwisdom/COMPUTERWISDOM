# RESOLVER_V0_1 — Path 3 named-function registry
# PSEUDO-CODE / NON-AUTHORITY / RECEIPT-EMITTER ONLY
#
# Loader -> Dispatcher -> Receipt Emitter
# NO_FAKE_GREEN = True
# APPEND_ONLY = True
# AUTHORITY_CREATED = False
# VERDICT_CREATED = False

RESULT_DOMAIN = {"authorized", "not_authorized", "hold", "conflict"}

def check_R1_SOURCE_IDENTITY(inputs): raise NotImplementedError
def check_R2_JURISDICTION_SCOPE(inputs): raise NotImplementedError
def check_R3_TEMPORAL_APPLICABILITY(inputs): raise NotImplementedError
def check_R4_ACTOR_APPLICABILITY(inputs): raise NotImplementedError
def check_R5_SUBJECT_APPLICABILITY(inputs): raise NotImplementedError
def check_R6_ACTION_APPLICABILITY(inputs): raise NotImplementedError
def check_R7_DELEGATION_AUTHORIZATION(inputs): raise NotImplementedError
def check_R8_LIMIT_EXCEPTION_CHECK(inputs): raise NotImplementedError
def check_R9_PROCEDURAL_TRIGGER(inputs): raise NotImplementedError
def check_R10_VERSION_SUPERSESSION(inputs): raise NotImplementedError
def check_R11_STATE_CONFLICT(inputs): raise NotImplementedError

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

def resolve_path(obj, dotted_path):
    cur = obj
    for part in dotted_path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None, False
        cur = cur[part]
    return cur, True

def bind_inputs(runtime_object, input_map):
    bound, missing = {}, []
    for name, path in input_map.items():
        value, ok = resolve_path(runtime_object, path)
        bound[name] = value
        if not ok:
            missing.append(path)
    return bound, missing

def emit_receipt(fixture, rule, dispatch_status, semantic_status="NOT_EVALUATED", reason=""):
    return {
        "receipt_id": f"RESOLVER_V0_1::{fixture['fixture_id']}::{rule['predicate_id']}",
        "resolver_id": "RESOLVER_V0_1",
        "fixture_id": fixture["fixture_id"],
        "predicate_id": rule["predicate_id"],
        "function_name": rule["function_name"],
        "dispatch_status": dispatch_status,
        "semantic_status": semantic_status,
        "reason": reason,
        "authority_created": False,
        "verdict_created": False,
        "append_only": True,
    }

def run_fixture_set(config, fixture_set):
    # DRY-RUN means registry/wiring replay only.
    # Current TEST_FIXTURES_V0_1 does not carry every structured runtime input.
    receipts = []
    rules = {r["predicate_id"]: r for r in config["rules"] if r.get("enabled", True)}
    for fixture in fixture_set["fixtures"]:
        pid = fixture["predicate"]
        rule = rules.get(pid)
        fn = predicate_registry.get(pid)
        if rule is None or fn is None:
            receipts.append(emit_receipt(
                fixture,
                rule or {"predicate_id": pid, "function_name": "UNREGISTERED"},
                "REGISTRY_MISS",
                reason="predicate not registered"
            ))
            continue
        receipts.append(emit_receipt(
            fixture, rule, "DISPATCHED",
            semantic_status="NOT_EVALUATED",
            reason="dry-run registry/wiring check; semantic runtime inputs not yet bound"
        ))
    return {
        "fixture_count": len(fixture_set["fixtures"]),
        "receipt_count": len(receipts),
        "all_dispatchable": all(r["dispatch_status"] == "DISPATCHED" for r in receipts),
        "semantic_evaluations": 0,
        "authority_created": False,
        "verdict_created": False,
        "receipts": receipts,
    }

# Expected current dry-run:
# fixture_count = 33
# receipt_count = 33
# all_dispatchable = True
# semantic_evaluations = 0
