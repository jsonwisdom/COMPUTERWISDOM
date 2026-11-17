#!/usr/bin/env python3
"""CI-FIRST feeling librarians: read-only, deterministic, standard-library replay."""
import hashlib, json, pathlib, sys

MANIFEST = pathlib.Path(__file__).with_name("CI_FIRST_MUSIC_LIBRARIANS_FEELING_V1.json")
ALLOWED = {"PASS", "FAIL", "UNKNOWN"}
def run(path=MANIFEST):
    raw = path.read_bytes()
    data = json.loads(raw)
    findings = {}
    shelves = {s["id"] for s in data.get("shelves", [])}
    ids = [s["id"] for s in data.get("shelves", [])]
    findings["unique_shelf_ids"] = "PASS" if len(ids) == len(shelves) and len(ids) > 0 else "FAIL"
    findings["exact_128_bpm"] = "PASS" if data.get("beat_target", {}).get("beat_microseconds") == 468750 and data["beat_target"]["bar_microseconds"] == 1875000 and data["beat_target"]["bpm"] == 128 else "FAIL"
    findings["no_claimed_authority"] = "PASS" if data.get("authority") is False else "FAIL"
    findings["candidate_feelings_labeled"] = "PASS" if all(x.get("feeling_status") == "UNVERIFIED_CANDIDATE" and set(x.get("shelves_candidate", [])).issubset(shelves) for x in data.get("catalog", [])) else "FAIL"
    findings["no_invented_original_bpm"] = "PASS" if all(x.get("original_bpm") is None and x.get("original_bpm_verdict") == "UNKNOWN" for x in data.get("catalog", [])) else "FAIL"
    findings["metadata_only"] = "PASS" if all("lyrics" not in x and "audio" not in x and "lyrics_hash" in x for x in data.get("catalog", [])) else "FAIL"
    findings["historical_source_provenance"] = "PASS" if all(x.get("source_url") for x in data.get("catalog", [])) else "UNKNOWN"
    findings["historical_bpm_measured"] = "PASS" if all(x.get("original_bpm") is not None for x in data.get("catalog", [])) else "UNKNOWN"
    findings["feeling_listener_validated"] = "PASS" if all(x.get("feeling_status") == "LISTENER_TAGGED" for x in data.get("catalog", [])) else "UNKNOWN"
    receipt = {"schema": "CI_FIRST_MUSIC_LIBRARIANS_REPLAY_V1", "catalog_sha256": hashlib.sha256(raw).hexdigest(), "items": len(data.get("catalog", [])), "shelves": len(shelves), "findings": findings, "overall": "FAIL" if "FAIL" in findings.values() else ("UNKNOWN" if "UNKNOWN" in findings.values() else "PASS")}
    assert set(findings.values()).issubset(ALLOWED)
    return receipt
if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
    sys.exit(1 if run()["overall"] == "FAIL" else 0)
