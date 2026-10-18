import json
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("router", HERE / "master_room_router_v1.py")
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)

def test_registry_count():
    s = router.status()
    assert s["public_repos"] == 80
    assert s["purpose_seated"] == 10
    assert s["purpose_unresolved"] == 70
    assert s["machine_authority_created"] is False

def test_known_repo_routes():
    r = router.route("jsonwisdom/COMPUTERWISDOM")
    assert r["terminal"] == "PASS_FOR_ROUTING_ONLY"
    assert r["purpose"]

def test_unresolved_repo_stops_at_jason():
    r = router.route("jsonwisdom/0")
    assert r["terminal"] == "HOLD"
    assert r["route"] == "JASON_OPERATOR_PURPOSE_GATE"

def test_unknown_repo_stops_at_jason():
    r = router.route("jsonwisdom/not-in-registry")
    assert r["terminal"] == "UNKNOWN"
    assert r["route"] == "JASON_OPERATOR"
