"""CI-FIRST read-only review of the *candidate* four-node/six-edge identity graph.

Passing this review means the baseline is internally consistent, NOT that any
ENS name, wallet, person, or pairwise control relationship is cryptographically proven.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
NODES = ("HUMAN", "ENS", "BASE", "SIGNER")
EXPECTED_PAIRS = {frozenset(p) for p in itertools.combinations(NODES, 2)}


def review(owner, matrix, architecture):
    failures = []
    if owner.get("owner", {}).get("name") != "Jason Wisdom":
        failures.append("owner_mismatch")
    if owner.get("owner", {}).get("role") != "HUMAN_COMMAND_AUTHORITY":
        failures.append("human_authority_missing")
    if owner.get("builder", {}).get("role") != "DRAFT_BUILD_TEST_ANALYZE_NO_FINANCIAL_AUTHORITY":
        failures.append("builder_authority_overreach")
    perm = owner.get("permissions", {})
    for key in ("build", "test", "write_to_this_draft_branch"):
        if perm.get(key) is not True:
            failures.append("build_permission_disabled:" + key)
    for key in ("merge", "deploy", "sign", "spend", "identity_change", "external_publication"):
        if perm.get(key) is not False:
            failures.append("unauthorized_permission:" + key)
    if owner.get("target", {}).get("branch") != "oodleloop/quadratic-restoration-v0.3.0":
        failures.append("wrong_branch")
    if owner.get("target", {}).get("merge_authorized") is not False:
        failures.append("merge_authority_asserted")
    if owner.get("safeguards", {}).get("global_hold") is not False:
        failures.append("global_hold")
    if owner.get("safeguards", {}).get("signature_required_for_build") is not False:
        failures.append("duplicate_authentication_gate")
    if architecture.get("build_authority") != "ENABLED" or architecture.get("global_project_hold") is not False:
        failures.append("architecture_build_or_hold_drift")
    if architecture.get("operator") != "Jason Wisdom":
        failures.append("architecture_operator_drift")
    if architecture.get("rails", {}).get("secure", {}).get("identity") != "jaywisdom.eth":
        failures.append("secure_rail_drift")
    if architecture.get("rails", {}).get("public", {}).get("identity") != "jaywisdom.base.eth":
        failures.append("public_rail_drift")

    node_ids = [node.get("id") for node in matrix.get("nodes", [])]
    if len(node_ids) != 4 or set(node_ids) != set(NODES):
        failures.append("node_set_mismatch")
    edges = matrix.get("edges", [])
    if len(edges) != 6:
        failures.append("edge_count_mismatch")
    seen = set()
    for edge in edges:
        a, b = edge.get("from"), edge.get("to")
        pair = frozenset((a, b))
        if a == b or pair not in EXPECTED_PAIRS:
            failures.append("invalid_pair:" + str(edge.get("id")))
        if pair in seen:
            failures.append("duplicate_pair:" + str(edge.get("id")))
        seen.add(pair)
        if edge.get("status") != "UNKNOWN":
            failures.append("unsupported_edge_promotion:" + str(edge.get("id")))
        if edge.get("independent_check") != "NOT_COMPLETED":
            failures.append("unverified_independent_check:" + str(edge.get("id")))
        if edge.get("authority_granted") is not False:
            failures.append("fabricated_edge_authority:" + str(edge.get("id")))
    if seen != EXPECTED_PAIRS:
        failures.append("incomplete_pair_coverage")
    return sorted(set(failures))


def main():
    owner_bytes = (HERE / "OWNER_POLICY.json").read_bytes()
    matrix_bytes = (HERE / "quadratic_edges.json").read_bytes()
    architecture_bytes = (HERE / "architecture.json").read_bytes()
    owner, matrix, architecture = map(json.loads, (owner_bytes, matrix_bytes, architecture_bytes))
    failures = review(owner, matrix, architecture)
    output = {
        "schema": "computerwisdom.quadratic-baseline-review.v0.3.1",
        "status": "PASS" if not failures else "FAIL",
        "scope": "LOCAL_STATIC_BASELINE_ONLY",
        "candidate_edges": len(matrix.get("edges", [])),
        "cryptographically_verified_edges": 0,
        "proof_status": "UNKNOWN",
        "owner_policy_sha256": hashlib.sha256(owner_bytes).hexdigest(),
        "edge_matrix_sha256": hashlib.sha256(matrix_bytes).hexdigest(),
        "failures": failures,
        "authority_granted": False,
    }
    print(json.dumps(output, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
