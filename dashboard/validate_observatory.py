
import json,hashlib
from pathlib import Path

root=Path(__file__).resolve().parent
d=json.loads((root/"observatory-v1.json").read_text(encoding="utf-8-sig"))
s=json.loads((root/"observatory-SSA-001.json").read_text())
raw=(root/"observatory-preview-v2.html").read_bytes()

tests={
 "lane_count":len(d["lanes"])==12,
 "lane_ids":sorted(x["id"] for x in d["lanes"])==list(range(1,13)),
 "fragment_integrity":d["fragments"]==d["hash_pass"],
 "investigation_id":s["id"]=="SSA-001",
 "measurement_unit":s["unit"]=="CALL_EVENTS",
 "citizen_count_unknown":s["unique_citizens"] is None,
 "remedy_unknown":s["citizen_remedy"]=="UNKNOWN",
 "publication_hold":d["publication"]==s["publication"]=="HOLD",
 "authority_boundary":s["government_authority"] is False,
 "preview_hash":hashlib.sha256(raw.replace(b"\r\n",b"\n")).hexdigest()=="675b00a1c72f162531c64d1aaf6dbd73468c850789d4b2cbbeb41d67c9e4b980",
 "source_link":s["source"].encode() in raw
}

for k,v in tests.items():
    print(k,"PASS" if v else "FAIL")

print("CI_ACCEPTANCE",sum(tests.values()),"/",len(tests))
raise SystemExit(0 if all(tests.values()) else 1)
