#!/usr/bin/env python3
import json, pathlib, subprocess, sys

def run(command):
    result=subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, file=sys.stderr, end="")
        raise SystemExit(result.returncode)
    return {row["name"]:row for row in json.loads(result.stdout)}

def main():
    py=run([sys.executable,"implementations/python/test_harness.py"])
    js=run(["node","implementations/javascript/test_harness.js"])
    failures=[]
    if set(py)!=set(js): failures.append("CASE_SET_MISMATCH")
    for name in sorted(set(py)&set(js)):
        if py[name]!=js[name]: failures.append(name)
    report={"status":"PASS" if not failures else "FAIL","failures":failures,"cases":len(set(py)&set(js))}
    out=pathlib.Path("evals/canonical-serializer-v1/results/latest.json")
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,sort_keys=True))
    return 1 if failures else 0
if __name__=="__main__": raise SystemExit(main())
