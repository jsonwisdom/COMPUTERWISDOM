import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "ALPR_MAX_LEDGER_HOLD_0001.json"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_synthetic_metrics_cannot_be_observed():
    data = load_fixture()
    for metric in data["derived_metrics"]:
        if metric["model_mode"] == "SYNTHETIC_STRESS_TEST":
            assert metric["observed_activity"] is False
            assert metric["state"] in {"HOLD", "CONFLICT", "REJECT"}


def test_county_projection_uses_contact_unit_not_search_unit():
    data = load_fixture()
    labels = {m["metric_id"]: m for m in data["derived_metrics"]}
    assert labels["MN-COUNTY-STRESS-001"]["unit"] == "TARGET_NETWORK_CONTACT"
    assert labels["AL-COUNTY-STRESS-001"]["unit"] == "TARGET_NETWORK_CONTACT"


def test_capacity_fails_closed_without_capacity_evidence():
    data = load_fixture()
    c = data["capacity_evidence"]
    required = [
        c["peak_qps"],
        c["concurrency_limit"],
        c["rate_limit"],
        c["fanout_limit_or_distribution"],
        c["response_latency_distribution"],
    ]
    assert all(v is None for v in required)
    assert c["state"] == "HOLD"
    assert data["disposition"]["machine_capacity"] == "HOLD"


def test_no_heat_claim_without_real_query_events_and_dedupe():
    data = load_fixture()
    assert data["query_events"] == []
    assert data["network_contacts"] == []
    assert data["disposition"]["dedupe"] == "HOLD"
    assert data["disposition"]["state_comparison"] == "HOLD"
    assert data["disposition"]["boxd_state"] == "HOLD"


if __name__ == "__main__":
    test_synthetic_metrics_cannot_be_observed()
    test_county_projection_uses_contact_unit_not_search_unit()
    test_capacity_fails_closed_without_capacity_evidence()
    test_no_heat_claim_without_real_query_events_and_dedupe()
    print("ALPR MAX ledger regression: PASS")
