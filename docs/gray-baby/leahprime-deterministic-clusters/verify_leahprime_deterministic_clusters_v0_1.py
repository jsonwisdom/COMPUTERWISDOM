#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KERNEL = ROOT / "LEAHPRIME_DETERMINISTIC_CLUSTER_KERNEL_V0_1.json"
MANIFEST = ROOT / "LEAHPRIME_IMAGE_CLUSTER_MANIFEST_2026_08_18.json"
RECEIPT = ROOT / "LEAHPRIME_CLUSTER_REVIEW_RECEIPT_001.json"

EXPECTED_HASHES = {
    "LP_CLUSTER_IMAGE_001": "1b67b97c94a0b420f07cf90266ecc88cb933925674089714b3727a92f2a3e24e",
    "LP_CLUSTER_IMAGE_002": "98fb3352671be3065f3eb5814cf24a5b45541d8e411a4ffd0d02a8f720732275",
    "LP_CLUSTER_IMAGE_003": "923226448b4979d9fa7550a26c8f46ec32e8650c6d96df85522b6fb2acf82ce0",
    "LP_CLUSTER_IMAGE_004": "5ec0401c41b5b95464c2e169d94710ec42a30244ac69aab9493a17f40e7c0033",
    "LP_CLUSTER_IMAGE_005": "bd95ec0db905c61e41b2ec3a705173b02218b1f785d6630ceac033b2a33052f3",
    "LP_CLUSTER_IMAGE_006": "8dd4c8fc645be70fed0ae416fa6ed7d8faddc2fa89bd4ffefb8027ab596c03d4",
    "LP_CLUSTER_IMAGE_007": "0c23d7be190314e677da7014ded4310e61bd532e4b3b9092a8b346757fe50a42",
}


def load(path):
    return json.loads(path.read_text())


def main():
    kernel = load(KERNEL)
    manifest = load(MANIFEST)
    receipt = load(RECEIPT)

    assert kernel["reviewer"]["semantic_type"] == "SYNTHETIC_CLUSTER_REVIEWER"
    assert kernel["reviewer"]["real_person"] is False
    assert kernel["reviewer"]["military_authority"] is False
    assert kernel["reviewer"]["truth_source"] is False
    assert kernel["container"] == "BOXD"
    assert kernel["internal_operator"] == "ReverseReplay"
    assert kernel["executor"] == "logicBoy"
    assert kernel["memory_metaphor"]["human_memory_claim"] is False
    assert kernel["model_required"] is False
    assert kernel["authority_created"] is False

    assert manifest["source_class"] == "USER_PROVIDED_ARTWORK_IN_CHAT"
    assert manifest["blob_storage_in_repository"] is False
    assert manifest["semantic_promotion"] is False
    assert len(manifest["images"]) == 7
    observed = {item["image_id"]: item["sha256"] for item in manifest["images"]}
    assert observed == EXPECTED_HASHES
    for item in manifest["images"]:
        assert item["official_record"] is False
        assert item["authority_created"] is False

    assert receipt["reviewer_type"] == "SYNTHETIC_CLUSTER_REVIEWER"
    assert receipt["container"] == "BOXD"
    assert receipt["operator"] == "ReverseReplay"
    assert receipt["executor"] == "logicBoy"
    assert len(receipt["reviewed_clusters"]) == 7
    for cluster in receipt["reviewed_clusters"]:
        assert cluster["cluster_replay_status"] == "PASS"
        assert cluster["content_truth_status"] == "HOLD"

    state = receipt["memory_review_state"]
    assert state["clusters_opened"] == 7
    assert state["clusters_replayed"] == 7
    assert state["clusters_deleted"] == 0
    assert state["clusters_promoted_to_public_record"] == 0
    assert state["clusters_promoted_to_authority"] == 0
    assert state["contradictions_erased"] == 0
    assert state["gaps_filled_by_inference"] == 0

    disp = receipt["disposition"]
    assert disp["cluster_architecture"] == "PASS"
    assert disp["image_byte_binding"] == "PASS"
    assert disp["semantic_promotion"] == "HOLD"
    assert disp["authority_created"] is False

    print("LEAHPRIME_CLUSTER_KERNEL=PASS")
    print("IMAGE_INPUT_COUNT=7")
    print("IMAGE_BYTE_BINDING=PASS")
    print("CLUSTER_REPLAY=PASS")
    print("CONTENT_TRUTH=HOLD")
    print("LEAHPRIME_REAL_PERSON=FALSE")
    print("MODEL_REQUIRED=FALSE")
    print("AUTHORITY_CREATED=FALSE")


if __name__ == "__main__":
    main()
