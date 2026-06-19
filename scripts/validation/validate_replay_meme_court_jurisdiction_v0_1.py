import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
JURISDICTION = ROOT / "replay" / "jurisdiction" / "replay_meme_court_jurisdiction_v0_1.json"
SCHEMA = ROOT / "schemas" / "replay_meme_court_jurisdiction.v0_1.schema.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    jurisdiction = load_json(JURISDICTION)
    schema = load_json(SCHEMA)
    jsonschema.Draft202012Validator(schema).validate(jurisdiction)

    assert jurisdiction["authority"] is False
    assert jurisdiction["operator"]["name"] == "Jay Wisdom"
    assert jurisdiction["operator"]["ens_base_l2"] == "jaywisdom.base.eth"
    assert jurisdiction["target"]["repository_full_name"] == "jsonwisdom/COMPUTERWISDOM"
    assert jurisdiction["validators"]["authority"] is False
    assert jurisdiction["court"]["authority"] is False

    print("REPLAY_MEME_COURT_JURISDICTION_V0_1: MATCH_CONFIRMED")
    print("authority=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
