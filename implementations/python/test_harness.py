#!/usr/bin/env python3
import base64, glob, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from serializer import CanonicalError, canonicalize, state_hash

def main():
    rows=[]; failed=False
    for path in sorted(glob.glob("fixtures/replayos/canonical-serializer-v1/*.json")):
        fixture=json.load(open(path, encoding="utf-8"))
        results=[]
        for raw in fixture["inputs"]:
            try:
                data=canonicalize(raw)
                results.append({"ok":True,"bytes_b64":base64.b64encode(data).decode(),"sha256":state_hash(data)})
            except CanonicalError as exc:
                results.append({"ok":False,"error":str(exc)})
        valid=fixture["valid"]
        passed=all(x["ok"] for x in results) if valid else all((not x["ok"] and x["error"]==fixture["expected_error"]) for x in results)
        if fixture.get("expect_equal"): passed &= len({x.get("bytes_b64") for x in results})==1
        if fixture.get("expect_distinct"): passed &= len({x.get("bytes_b64") for x in results})==len(results)
        rows.append({"name":fixture["name"],"passed":bool(passed),"results":results})
        failed |= not passed
    print(json.dumps(rows, sort_keys=True, separators=(",",":")))
    return 1 if failed else 0
if __name__=="__main__": raise SystemExit(main())
