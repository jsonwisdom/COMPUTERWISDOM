from resolver_v0_1_predicates import *

R = [{"id":"receipt"}]

def status(fn, **kwargs):
    return fn({**kwargs, "receipts": R})["status"]

def test_R1():
    assert status(check_R1_SOURCE_IDENTITY, authority_source_id="A", authority_sources=["A"]) == PASS
    assert status(check_R1_SOURCE_IDENTITY, authority_source_id="B", authority_sources=["A"]) == FAIL

def test_R2():
    assert status(check_R2_JURISDICTION_SCOPE, event_domain="MN", scope=["MN"]) == PASS
    assert status(check_R2_JURISDICTION_SCOPE, event_domain="DC", scope=["MN"]) == FAIL

def test_R3():
    assert status(check_R3_TEMPORAL_APPLICABILITY, event_time="2026-01-15T00:00:00Z", valid_from="2026-01-01T00:00:00Z", valid_to="2026-01-31T00:00:00Z") == PASS
    assert status(check_R3_TEMPORAL_APPLICABILITY, event_time="2027-01-15T00:00:00Z", valid_from="2026-01-01T00:00:00Z", valid_to="2026-01-31T00:00:00Z") == FAIL

def test_R4_R5_R6():
    assert status(check_R4_ACTOR_APPLICABILITY, actor="A", actor_rules=["A"]) == PASS
    assert status(check_R5_SUBJECT_APPLICABILITY, subject="S", subject_rules=["S"]) == PASS
    assert status(check_R6_ACTION_APPLICABILITY, action="X", action_rules=["X"]) == PASS

def test_R7():
    assert status(check_R7_DELEGATION_AUTHORIZATION, delegation={"authorized":True,"actor":"A","action":"X"}, actor="A", action="X") == PASS
    assert status(check_R7_DELEGATION_AUTHORIZATION, delegation={"authorized":False}, actor="A", action="X") == FAIL

def test_R8():
    assert status(check_R8_LIMIT_EXCEPTION_CHECK, limits=[{"applies":False}], exceptions=[{"applies":False}], event={}) == PASS
    assert status(check_R8_LIMIT_EXCEPTION_CHECK, limits=[{"applies":True}], exceptions=[], event={}) == FAIL

def test_R9():
    assert status(check_R9_PROCEDURAL_TRIGGER, trigger_rules=[{"satisfied":True}], event={}) == PASS
    assert status(check_R9_PROCEDURAL_TRIGGER, trigger_rules=[{"satisfied":False}], event={}) == FAIL

def test_R10():
    assert status(check_R10_VERSION_SUPERSESSION, authority_version="1", event_time="2026-05-01T00:00:00Z", supersession={"superseded":False}) == PASS
    assert status(check_R10_VERSION_SUPERSESSION, authority_version="1", event_time="2026-05-01T00:00:00Z", supersession={"superseded":True,"effective_at":"2026-04-01T00:00:00Z"}) == FAIL

def test_R11():
    assert status(check_R11_STATE_CONFLICT, claim_object={"state":"A"}, runtime_state={"state":"A"}) == PASS
    assert status(check_R11_STATE_CONFLICT, claim_object={"state":"A"}, runtime_state={"state":"B"}) == CONFLICT

def test_shape_only_guard():
    assert status(check_R1_SOURCE_IDENTITY, authority_source_id="SHAPE_ONLY", authority_sources=["SHAPE_ONLY"]) == HOLD
