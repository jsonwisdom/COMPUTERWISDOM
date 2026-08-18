#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDINGS_PATH = ROOT / "fixtures/jaywisdom/fraud_ledger/DOJ_CRISSCROSS_PLAYBOOKPINCER_CLERK_LANE_BINDINGS_V0_2.json"
SOURCE_PATH = ROOT / "fixtures/jaywisdom/fraud_ledger/STACK_TERMS_CLERK_REPLAY_V0_1.json"

REQUIRED_RULES = {
    "GLOSSARY_TERM != DOJ_TERMINOLOGY",
    "ROUTING != EVIDENCE",
    "ROUTING != TERMINAL",
    "CHECKPOINT != APPROVAL",
    "FLAG != FINDING",
    "HYPOTHESIS != FACT",
    "REPLAY != VERDICT",
    "AUDIT != ACCUSATION",
    "NO_CLAIM_OUTRANKS_ITS_RECEIPTS",
    "CALLER_SUPPLIED_TERMINAL_FORBIDDEN = TRUE",
    "AUTHORITY_CREATED = FALSE",
}
EXPECTED_HELD = {"TODDBLANCHE_APPROVED", "702_SWITCHEROO", "INTERNAL_THREAT_FLAG"}
EXPECTED_TERMINALS = ["PASS", "HOLD", "CONFLICT", "REJECT"]
FORBIDDEN_ROUTE_KEYS = {"terminal", "disposition", "verdict", "finding", "approval"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors, code, detail):
    errors.append({"code": code, "detail": detail})


def main():
    errors = []
    bindings = load(BINDINGS_PATH)
    source = load(SOURCE_PATH)

    if bindings.get("format") != "DOJ_CRISSCROSS_PLAYBOOKPINCER_CLERK_LANE_BINDINGS_V0.2":
        fail(errors, "FORMAT", "Unexpected bindings format")
    if bindings.get("classification") != "ANALYTICAL_ROUTING_BINDINGS_ONLY":
        fail(errors, "CLASSIFICATION", "Bindings must remain analytical routing only")

    rules = set(bindings.get("rules", []))
    missing_rules = sorted(REQUIRED_RULES - rules)
    if missing_rules:
        fail(errors, "RULES", f"Missing required rules: {missing_rules}")

    allowed = bindings.get("allowed_clerk_lanes", [])
    if not allowed or len(allowed) != len(set(allowed)):
        fail(errors, "ALLOWED_LANES", "Allowed Clerk lanes must be non-empty and unique")
    allowed_set = set(allowed)

    source_terms = source.get("terms", [])
    source_map = {item.get("term"): item for item in source_terms}
    if None in source_map or len(source_map) != len(source_terms):
        fail(errors, "SOURCE_TERM_IDENTITY", "Source Clerk terms must have unique term names")

    routing = bindings.get("routing", [])
    route_map = {item.get("term"): item for item in routing}
    if None in route_map or len(route_map) != len(routing):
        fail(errors, "ROUTING_TERM_IDENTITY", "Routing terms must have unique term names")

    source_set = set(source_map)
    route_set = set(route_map)
    if source_set != route_set:
        fail(
            errors,
            "TERM_SET_MISMATCH",
            f"Routing must cover exactly the source Clerk terms; missing={sorted(source_set-route_set)}, extra={sorted(route_set-source_set)}",
        )

    for term in sorted(source_set & route_set):
        src = source_map[term]
        route = route_map[term]
        state = route.get("source_clerk_state")
        if state != src.get("state"):
            fail(errors, "STATE_DRIFT", f"{term}: route state {state!r} != source Clerk state {src.get('state')!r}")

        forbidden = sorted(FORBIDDEN_ROUTE_KEYS & set(route))
        if forbidden:
            fail(errors, "CALLER_TERMINAL_OR_FINDING", f"{term}: forbidden route keys {forbidden}")

        lanes = route.get("lanes")
        if not isinstance(lanes, list) or not lanes:
            fail(errors, "EMPTY_ROUTE", f"{term}: lanes must be a non-empty list")
            continue
        if len(lanes) != len(set(lanes)):
            fail(errors, "DUPLICATE_ROUTE", f"{term}: duplicate Clerk lane")
        unknown = sorted(set(lanes) - allowed_set)
        if unknown:
            fail(errors, "UNKNOWN_LANE", f"{term}: unknown lanes {unknown}")

        if src.get("state") == "HOLD" and not route.get("promotion_condition"):
            fail(errors, "HOLD_WITHOUT_CONDITION", f"{term}: HOLD routing requires explicit promotion_condition")

    held_from_source = {term for term, item in source_map.items() if item.get("state") == "HOLD"}
    held_declared = set(bindings.get("held_terms_must_remain", []))
    if held_from_source != EXPECTED_HELD:
        fail(errors, "SOURCE_HELD_DRIFT", f"Source Clerk held terms changed: {sorted(held_from_source)}")
    if held_declared != EXPECTED_HELD:
        fail(errors, "DECLARED_HELD_DRIFT", f"Bindings held terms changed: {sorted(held_declared)}")

    policy = bindings.get("derived_terminal_policy", {})
    if policy.get("routing_layer_may_assign_terminal") is not False:
        fail(errors, "TERMINAL_AUTHORITY", "Routing layer must not assign terminal states")
    if policy.get("terminal_states") != EXPECTED_TERMINALS:
        fail(errors, "TERMINAL_SET", "Terminal states must remain PASS/HOLD/CONFLICT/REJECT in order")

    summary = bindings.get("expected_summary", {})
    source_summary = source.get("replay_summary", {})
    expected_counts = {
        "terms": len(source_terms),
        "source_pass_terms": sum(1 for x in source_terms if x.get("state") == "PASS"),
        "source_hold_terms": sum(1 for x in source_terms if x.get("state") == "HOLD"),
        "world_fact_promotions": source_summary.get("world_fact_promotions"),
        "legal_findings_created": source_summary.get("legal_findings_created"),
        "doj_decisions_created": source_summary.get("doj_decisions_created"),
        "authority_created": source_summary.get("authority_created"),
    }
    if summary != expected_counts:
        fail(errors, "SUMMARY_DRIFT", f"Expected summary mismatch: actual={summary}, derived={expected_counts}")

    if summary.get("world_fact_promotions") != 0:
        fail(errors, "WORLD_FACT_PROMOTION", "World fact promotions must remain zero")
    if summary.get("legal_findings_created") != 0:
        fail(errors, "LEGAL_FINDING", "Legal findings created must remain zero")
    if summary.get("doj_decisions_created") != 0:
        fail(errors, "DOJ_DECISION", "DOJ decisions created must remain zero")
    if summary.get("authority_created") is not False:
        fail(errors, "AUTHORITY_CREATED", "Authority created must remain false")

    result = {
        "format": bindings.get("format"),
        "terms_checked": len(route_map),
        "allowed_clerk_lanes": len(allowed),
        "pass_terms": expected_counts["source_pass_terms"],
        "hold_terms": expected_counts["source_hold_terms"],
        "held_terms": sorted(EXPECTED_HELD),
        "world_fact_promotions": expected_counts["world_fact_promotions"],
        "legal_findings_created": expected_counts["legal_findings_created"],
        "doj_decisions_created": expected_counts["doj_decisions_created"],
        "authority_created": expected_counts["authority_created"],
        "errors": errors,
        "terminal": "PASS_CLERK_LANE_BINDINGS" if not errors else "HOLD_CLERK_LANE_BINDINGS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
