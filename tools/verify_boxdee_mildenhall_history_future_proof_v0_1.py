import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATTESTATION = (
    ROOT
    / "fixtures"
    / "boxdee"
    / "mildenhall"
    / "BOXDEE_MILDENHALL_ONCHAIN_ATTESTATION_V0_1.json"
)


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def main():
    obj = json.loads(ATTESTATION.read_text(encoding="utf-8"))
    expected = obj.pop("canonical_attestation_sha256")
    actual = hashlib.sha256(canonical_json(obj)).hexdigest()

    assert actual == expected, (actual, expected)

    image = obj["image_receipt"]
    assert image["byte_identity_verified"] is True
    assert image["byte_length"] == image["drive_roundtrip_byte_length"]
    assert image["sha256"] == image["drive_roundtrip_sha256"]
    assert len(image["sha256"]) == 64

    assert obj["future_proof_rule"]["append_only"] is True
    assert obj["on_chain"]["raw_bytes_on_chain"] is False
    assert obj["on_chain"]["commitment_ready"] is True
    assert obj["on_chain"]["published"] is False
    assert obj["on_chain"]["chain_id"] is None
    assert obj["on_chain"]["transaction_hash"] is None
    assert obj["on_chain"]["attestation_uid"] is None
    assert obj["story_boundary"]["AUTHORITY_CREATED"] is False
    assert obj["subject"]["authority_created"] is False
    assert obj["openai"]["runtime_required"] is False
    assert obj["openai"]["model_output_creates_disposition"] is False

    for claim in obj["temporal_claims"]:
        assert claim["state"] == "SOURCE_BOUND_TEXT"
        assert claim["source_url"].startswith("https://")
        assert claim["page_bytes_sealed"] is False

    print("BOXDEE_MILDENHALL_V0_1=PASS")
    print(f"canonical_attestation_sha256={actual}")
    print(f"image_sha256={image['sha256']}")
    print("on_chain_published=false")
    print("authority_created=false")


if __name__ == "__main__":
    main()
