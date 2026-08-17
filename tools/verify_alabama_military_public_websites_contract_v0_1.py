#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "agents/congressional_accountability/alabama_military_public_websites_contract.json"

ALLOWED_HOSTS = {
    "home.army.mil",
    "anad.army.mil",
    "www.army.mil",
    "www.maxwell.af.mil",
    "www.187fw.ang.af.mil",
    "www.117arw.ang.af.mil",
    "al.ng.mil",
    "www.forcecom.uscg.mil",
    "www.atlanticarea.uscg.mil",
    "www.marforres.marines.mil",
    "www.navyreserve.navy.mil",
}

EXPECTED_IDS = {
    "AL_ARMY_REDSTONE_ARSENAL",
    "AL_ARMY_ANNISTON_ARMY_DEPOT",
    "AL_ARMY_FORT_RUCKER_AVCOE",
    "AL_AIR_FORCE_MAXWELL_GUNTER",
    "AL_ANG_187_FIGHTER_WING",
    "AL_ANG_117_AIR_REFUELING_WING",
    "AL_NATIONAL_GUARD_STATE_HOME",
    "AL_USCG_ATC_MOBILE",
    "AL_USCG_SECTOR_MOBILE",
    "AL_USMCR_MOBILE_BATTLESPACE_SURVEILLANCE_COMPANY",
    "AL_NAVY_RESERVE_CENTER_BIRMINGHAM_REFERENCE",
}

FALSE_GUARDS = (
    "raw_source_bytes_frozen",
    "operational_intelligence_collected",
    "claim_verified",
    "legal_finding_created",
    "misconduct_finding_created",
    "model_execution_performed",
    "authority_created",
)


def check(condition, label):
    if not condition:
        raise SystemExit(f"FAIL: {label}")
    print(f"PASS: {label}")


def main():
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    entries = data["entries"]

    check(data["format"] == "ALABAMA_MILITARY_PUBLIC_WEBSITES_CONGRESSIONAL_CONTRACT_V0.1", "format")
    check(data["classification"] == "PUBLIC_REFERENCE_LOCATOR_CONTRACT", "classification")
    check(data["scope"] == "OFFICIAL_PUBLIC_FACING_WEB_LOCATORS_ONLY", "scope")
    check(len(entries) == 11, "entry count = 11")
    check({e["id"] for e in entries} == EXPECTED_IDS, "expected public reference set")
    check(len({e["id"] for e in entries}) == len(entries), "unique entry ids")

    for entry in entries:
        parsed = urlparse(entry["primary_public_url"])
        check(parsed.scheme == "https", f"{entry['id']} uses https")
        check(parsed.hostname in ALLOWED_HOSTS, f"{entry['id']} host allowlisted")
        check(entry["locator_state"].startswith("OFFICIAL_"), f"{entry['id']} official locator typed")

    navy = next(e for e in entries if e["id"] == "AL_NAVY_RESERVE_CENTER_BIRMINGHAM_REFERENCE")
    check(navy["dedicated_home_verified"] is False, "NRC Birmingham dedicated-home gap preserved")

    deltas = data["public_web_deltas"]
    check(len(deltas) == 1, "one explicit web delta")
    delta = deltas[0]
    check(delta["observed_state"] == "OFFICIAL_PUBLIC_WEB_NOMENCLATURE_DELTA", "Rucker/Novosel delta typed")
    check(delta["error_asserted"] is False, "web delta does not assert error")
    check(delta["intent_asserted"] is False, "web delta does not assert intent")
    check(delta["misconduct_asserted"] is False, "web delta does not assert misconduct")

    membrane = data["membrane"]
    check(membrane["WEBSITE_DELTA"] == "DOES_NOT_PROVE_ERROR_OR_INTENT", "website delta boundary")
    check(membrane["MISSING_DEDICATED_HOME"] == "GAP_NOT_MISCONDUCT", "missing home boundary")
    check(membrane["TOOL_CALL"] == "DOES_NOT_EQUAL_GOVERNMENT_ACTION", "tool call boundary")
    check(membrane["OPENAI_DEVELOPER_SURFACE"] == "DOES_NOT_EQUAL_REPOSITORY_EXECUTOR", "OpenAI surface boundary")

    for key in FALSE_GUARDS:
        check(data[key] is False, f"{key}=false")

    print("STATUS = PASS_WITH_BOUNDARY")
    print("PUBLIC_LOCATORS_VERIFIED_BY_CONTRACT = 11")
    print("LIVE_NETWORK_FETCH_IN_VERIFIER = FALSE")
    print("CLAIM_VERIFIED = FALSE")
    print("MODEL_EXECUTION_PERFORMED = FALSE")
    print("AUTHORITY_CREATED = FALSE")


if __name__ == "__main__":
    main()
