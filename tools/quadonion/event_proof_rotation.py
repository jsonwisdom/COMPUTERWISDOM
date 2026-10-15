#!/usr/bin/env python3
"""QuadOnion: bounded, event-triggered proof rotation; no schedule, network or release."""
import argparse
import hashlib
import json
import pathlib
import re

EVENT_KINDS = {
    "SOURCE_RECEIPT_ADDED", "SOURCE_BYTES_CHANGED", "CONTRADICTION_RECORDED",
    "CHECK_FAILED", "REPLAY_MISMATCH", "REVIEW_RECEIPT_ADDED"
}
ROTATING_SEATS = ("Leanne", "LeahPrime", "BoxDee", "Supreme Seymour")
REQUIRED_STATES = ("PASS", "HOLD", "FAIL")
SAFE_TOPICS = ("women_public_accountability", "public_institutional_audit", "general")
MAX_EVENTS = 256
MAX_QUESTIONS = 8
MAX_ART_CONCEPTS = 3

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()

def validate_event(event):
    if not isinstance(event, dict):
        return "event is not an object"
    if event.get("kind") not in EVENT_KINDS:
        return "event kind unsupported (questions alone never trigger)"
    if not isinstance(event.get("event_id"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]{4,96}", event["event_id"]):
        return "invalid event_id"
    if not isinstance(event.get("receipt_ref"), str) or not event["receipt_ref"]:
        return "missing receipt reference"
    if not isinstance(event.get("receipt_sha256"), str) or not re.fullmatch(r"[a-f0-9]{64}", event["receipt_sha256"]):
        return "missing full receipt digest"
    return None

def classify_sources(sources):
    if not isinstance(sources, list):
        return {"observation_count": 0, "declared_origin_count": 0,
                "independent_witness_count_verified": 0, "flags": ["sources must be a list"]}
    origins = set()
    flags = []
    for s in sources:
        if not isinstance(s, dict):
            flags.append("invalid source observation")
            continue
        origin = s.get("declared_origin_id")
        if isinstance(origin, str) and origin:
            origins.add(origin)
        else:
            flags.append("source origin unresolved")
        if s.get("content_sha256") and not re.fullmatch(r"[a-f0-9]{64}", str(s["content_sha256"])):
            flags.append("invalid content hash")
        if s.get("witness_independent") is True:
            flags.append("self-declared witness independence is not verified")
    return {
        "observation_count": len(sources),
        "declared_origin_count": len(origins),
        "independent_witness_count_verified": 0,
        "origin_verification_performed": False,
        "flags": sorted(set(flags))
    }

def questions_for(case, source_result):
    questions = []
    if not case.get("exact_claim"):
        questions.append("What is the exact, falsifiable proposition?")
    if source_result["observation_count"] == 0:
        questions.append("Where is the first dated primary-source receipt?")
    if source_result["declared_origin_count"] == 0:
        questions.append("What underlying origin produced each observed URL or proxy copy?")
    if not case.get("contrary_receipts"):
        questions.append("What contrary record could disconfirm this proposition?")
    if not case.get("source_bytes_inspected"):
        questions.append("Who has inspected the actual source bytes, with capture time and hash?")
    if not case.get("independent_origin_review_receipt"):
        questions.append("Which separate origin was independently authenticated, if any?")
    if not case.get("human_review_receipt"):
        questions.append("What must Jason review before any proposed conclusion or artwork release?")
    if case.get("topic") == "women_public_accountability":
        questions.append("Does the source support a claim about a public record rather than an inference about a woman?")
    return questions[:MAX_QUESTIONS]

def art_manifest(case_id, event_id, topic, n=MAX_ART_CONCEPTS):
    """Draft manifest ONLY. No pixels, TD IDs, mint, identification or release."""
    n = min(max(n, 0), MAX_ART_CONCEPTS)
    key = digest({"case_id":case_id,"event_id":event_id})[:12]
    subjects = (
        "Evidence queue: receipts are not independent witnesses",
        "Question engine: what would change this HOLD?",
        "Audit replay: count observations, not unsupported conclusions",
    )
    return [{
        "draft_id": f"ART_CANDIDATE_{key}_{i+1:02d}",
        "concept": subjects[i],
        "aspect_ratio": "3:4",
        "triggerdeck_id": None,
        "pixel_art_generated": False,
        "editorial_state": "HOLD",
        "release_authorized": False,
        "safety": "satirize process; no unsupported accusation or private woman/family portrayal",
        "topic":topic
    } for i in range(n)]

def evaluate(case):
    errors = []
    if not isinstance(case, dict):
        raise ValueError("case must be object")
    case_id = case.get("case_id")
    if not isinstance(case_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{4,96}",case_id):
        errors.append("invalid case_id")
        case_id = "INVALID"
    topic = case.get("topic", "general")
    if topic not in SAFE_TOPICS:
        errors.append("unrecognized topic / privacy scope")
        topic = "general"
    observations = classify_sources(case.get("sources", []))
    events = case.get("events", [])
    if not isinstance(events, list) or len(events) > MAX_EVENTS:
        errors.append("invalid event list / event cap exceeded")
        events = []
    seen = {}
    rotations = []
    for event in events:
        invalid = validate_event(event)
        if invalid:
            errors.append(invalid)
            continue
        eid = event["event_id"]
        ref = (event["kind"], event["receipt_ref"], event["receipt_sha256"])
        if eid in seen:
            if seen[eid] != ref:
                errors.append("CONFLICT: same event ID references different receipt")
            continue
        seen[eid] = ref
        index = len(rotations)
        rotations.append({
            "event_id": eid,
            "trigger_kind": event["kind"],
            "receipt_ref": event["receipt_ref"],
            "receipt_sha256_declared": event["receipt_sha256"],
            "receipt_bytes_fetched_or_verified": False,
            "marydee_role": "PURPOSE_AND_ROUTING_ONLY",
            "lead_reviewer": ROTATING_SEATS[index % len(ROTATING_SEATS)],
            "counter_reviewer": ROTATING_SEATS[(index + 1) % len(ROTATING_SEATS)],
            "privacy_gate": "Boss Brenda / HUMAN_REVIEW_REQUIRED",
            "bot_dispatched": False,
            "replay_proven": False,
            "art_candidates": art_manifest(case_id,eid,topic),
        })
    return {
        "schema": "QUADONION_EVENT_REPLAY_V0_1",
        "case_id": case_id,
        "topic": topic,
        "trigger_model": "EVENT_ONLY_NO_SCHEDULE",
        "processed_unique_event_count": len(rotations),
        "duplicate_event_count": max(0, len(events)-len(rotations)-sum(1 for e in events if validate_event(e))),
        "event_rotations": rotations,
        "source_counters": observations,
        "followup_questions": questions_for(case, observations),
        "verification_boundaries": {
            "event_metadata_checked": True,
            "external_sources_fetched": False,
            "source_content_verified": False,
            "historical_truth_established": False,
            "family_consents_obtained": False,
            "art_rendered": False,
            "actual_marydeebot_dispatched": False,
        },
        "errors": errors,
        "case_state": "HOLD",
        "gate_001_execution": "HOLD",
        "deployment_state": "DEPLOYMENT_HOLD",
        "publication_enabled": False,
        "joy_deployment_enabled": False,
        "authority_created": False,
        "final_release_authority": "Jason",
        "input_digest": digest(case)
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases-dir", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    case_dir = pathlib.Path(args.cases_dir)
    target = pathlib.Path(args.out)
    target.mkdir(parents=True, exist_ok=True)
    names = sorted(case_dir.glob("*.json"))
    results = []
    for file in names:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            output = evaluate(data)
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            output = {"schema": "QUADONION_EVENT_REPLAY_V0_1",
                      "case_state": "HOLD", "gate_001_execution": "HOLD",
                      "publication_enabled": False, "error": str(exc)}
        output["file_sha256"] = hashlib.sha256(file.read_bytes()).hexdigest()
        results.append(output)
    manifest = {
        "schema": "QUADONION_MANIFEST_V0_1",
        "source": "local repository case fixtures only",
        "results": results,
        "receipt_type": "SCOPED_MACHINE_METADATA_RESULT_NOT_HISTORICAL_PROOF",
        "external_source_count_checked": 0,
        "runtime_commit_not_bound_by_engine": True,
        "publication_enabled": False,
        "authority_created": False
    }
    (target / "quadonion-review.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"case_count":len(results),"event_count":sum(r.get("processed_unique_event_count",0) for r in results),
                      "states":[r["case_state"] for r in results],"released":False}))
    if any(r.get("errors") or r.get("error") for r in results):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
