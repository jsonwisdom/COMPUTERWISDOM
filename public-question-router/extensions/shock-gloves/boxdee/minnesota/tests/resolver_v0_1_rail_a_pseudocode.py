# RESOLVER_V0_1 — Rail A materialized-shape dry-run
# NEW APPENDED HARNESS. Prior resolver_v0_1_pseudocode.py remains preserved.
UNIMPLEMENTED = None

def _unimplemented(_inputs):
    return UNIMPLEMENTED

predicate_registry = {
    "R1": _unimplemented,  # check_R1_SOURCE_IDENTITY
    "R2": _unimplemented,  # check_R2_JURISDICTION_SCOPE
    "R3": _unimplemented,  # check_R3_TEMPORAL_APPLICABILITY
    "R4": _unimplemented,  # check_R4_ACTOR_APPLICABILITY
    "R5": _unimplemented,  # check_R5_SUBJECT_APPLICABILITY
    "R6": _unimplemented,  # check_R6_ACTION_APPLICABILITY
    "R7": _unimplemented,  # check_R7_DELEGATION_AUTHORIZATION
    "R8": _unimplemented,  # check_R8_LIMIT_EXCEPTION_CHECK
    "R9": _unimplemented,  # check_R9_PROCEDURAL_TRIGGER
    "R10": _unimplemented,  # check_R10_VERSION_SUPERSESSION
    "R11": _unimplemented,  # check_R11_STATE_CONFLICT
}

def resolve_path(obj, dotted_path):
    cur = obj
    for part in dotted_path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None, False
        cur = cur[part]
    return cur, True

def bind_inputs(runtime_input, input_map):
    bound, missing = {}, []
    for name, path in input_map.items():
        value, ok = resolve_path(runtime_input, path)
        bound[name] = value
        if not ok:
            missing.append(path)
    return bound, missing

def run_fixture_set(config, runtime_fixture_set):
    rules = {r["predicate_id"]: r for r in config["rules"] if r.get("enabled", True)}
    receipts = []
    semantic_evaluations = 0

    for fixture in runtime_fixture_set["fixtures"]:
        pid = fixture["predicate_id"]
        rule = rules[pid]
        fn = predicate_registry[pid]
        bound, missing = bind_inputs(fixture["runtime_input"], rule["input_map"])

        if missing:
            dispatch_status = "INPUT_MAP_ERROR"
            body_status = "NOT_CALLED"
        else:
            dispatch_status = "DISPATCHED"
            result = fn(bound)
            body_status = "UNIMPLEMENTED" if result is None else "IMPLEMENTED"
            # Rail A invariant: implemented semantic outcomes are not admitted here.
            if result is not None:
                raise RuntimeError("NO_FAKE_GREEN: Rail A forbids semantic predicate output")

        receipts.append({
            "source_fixture_id": fixture["source_fixture_id"],
            "predicate_id": pid,
            "function_name": rule["function_name"],
            "dispatch_status": dispatch_status,
            "predicate_body_status": body_status,
            "semantic_status": "NOT_EVALUATED",
            "predicate_truth_created": False,
            "authority_created": False,
            "verdict_created": False,
            "append_only": True,
        })

    return {
        "fixture_count": len(runtime_fixture_set["fixtures"]),
        "dispatch_count": sum(r["dispatch_status"] == "DISPATCHED" for r in receipts),
        "semantic_evaluations": semantic_evaluations,
        "predicate_truth_created": False,
        "authority_created": False,
        "verdict_created": False,
        "receipts": receipts,
    }
