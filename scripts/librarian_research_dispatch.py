#!/usr/bin/env python3
"""Librarian dispatcher: deterministic assignments and honest evidence accounting."""
import csv,datetime,hashlib,json,os,pathlib,collections,urllib.request,zipfile,io
root=pathlib.Path("hold-inventory")
records=list(csv.DictReader((root/"top-status-candidates.csv").open(encoding="utf-8")))
out=pathlib.Path("research-ledger");out.mkdir(exist_ok=True)
def team(path,excerpt):
    t=(path+" "+excerpt).lower()
    if any(s in t for s in ("wallet","coinbase","yubikey","signature","x402","payment","treasury","auth")):return "SECURITY_AUDITOR"
    if any(s in t for s in ("replay","merkle","hash","receipt","workflow","validator")):return "REPLAY_AUDITOR"
    if any(s in t for s in ("math","quantity","budget","count","estimate","score")):return "FULLMATH"
    if any(s in t for s in ("court","senate","law","judge","constitutional","supreme")):return "SUPREME_SEYMOUR"
    return "SOURCE_RESEARCHER"
def kind(row):
    p=row["path"].lower();s=row["excerpt"].lower()
    if any(x in p for x in ("/tests/","/fixtures/","/examples/","schema","test_")):return "REFERENCE_NOT_OPEN_CASE"
    if any(x in s for x in ("example","mock ","illustrative","do not","must not","forbidden","allowed statuses","can be","policy","schema")):return "NEEDS_HUMAN_TRIAGE"
    return "POTENTIAL_RESEARCH_GAP"
cases=[]
for row in records:
    key=f'{row["path"]}:{row["line"]}:{row["markers"]}'
    cid=hashlib.sha256(key.encode()).hexdigest()[:16]
    clas=kind(row)
    cases.append({"id":cid,"file":row["path"],"line":int(row["line"]),"markers":row["markers"].split(";"),
      "source_excerpt":row["excerpt"],"assignment":team(row["path"],row["excerpt"]),
      "classification":clas,"evidence_verified":"NOT_TESTED",
      "result":"HOLD" if clas=="POTENTIAL_RESEARCH_GAP" else "TRIAGE",
      "reason":"Marker is not evidence of research failure; seek original primary proof and versioned receipt",
      "next_action":"Find primary source and verify byte-level/replay evidence; retain HOLD until verified."})
cases.sort(key=lambda x:(x["file"],x["line"],x["id"]))
# Prior report from previous successful workflow run, if authorized to read its artifact.
baseline={"state":"NOT_AVAILABLE","artifact_id":None}
token=os.getenv("GH_TOKEN","")
repo=os.getenv("GITHUB_REPOSITORY","jsonwisdom/COMPUTERWISDOM")
if token:
    def github(url):
        req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json","User-Agent":"sow-research-ledger"})
        with urllib.request.urlopen(req,timeout=15) as response:return response.read()
    try:
        data=json.loads(github(f"https://api.github.com/repos/{repo}/actions/artifacts?per_page=100&name=school-of-wisdom-research-ledger"))
        valid=[a for a in data.get("artifacts",[]) if not a.get("expired")]
        if valid:
            item=max(valid,key=lambda a:a["id"])
            blob=github(item["archive_download_url"])
            with zipfile.ZipFile(io.BytesIO(blob)) as archive:
                raw=archive.read("cases.json")
                if len(raw)>8_000_000:raise ValueError("oversized historical ledger")
                prior=json.loads(raw)
            baseline={"state":"READ","artifact_id":item["id"],"cases":prior}
    except Exception as e:
        baseline={"state":"NOT_AVAILABLE","reason":type(e).__name__}
prev={c["id"]:c for c in baseline.get("cases",[])}
now={c["id"]:c for c in cases}
changes={"new_marker_candidates":sorted(set(now)-set(prev)) if prev else [],
         "no_longer_at_same_source_line":sorted(set(prev)-set(now)) if prev else [],
         "continuing_candidates":len(set(now)&set(prev)),
         "caution":"Disappearing markers do not prove research completion or correction."}
counts=dict(collections.Counter(x["assignment"] for x in cases))
result_counts=dict(collections.Counter(x["result"] for x in cases))
now_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest={"schema":"SOW_LIBRARIAN_RESEARCH_LEDGER_V1","run_at_utc":now_utc,
  "scope":"COMPUTERWISDOM checked-out branch only; no private sources or entire repository estate",
  "case_count":len(cases),"assignments":counts,"dispositions":result_counts,
  "successes":[{"step":"inventory","result":"PASS","proof":"hold-inventory/summary.json and SHA256"},{"step":"dispatch","result":"PASS","proof":"cases.json with deterministic assignments"}],
  "failures":[],"holds":["No independent external-source research performed","No case may be marked resolved by text disappearance","Production, payments, wallet authority unchanged"],
  "prior_artifact":{"state":baseline["state"],"artifact_id":baseline.get("artifact_id")},
  "comparison":changes,
  "research_completed":False,"research_proof_independently_verified":False,"human_authority":True,"governance":"HOLD"}
(out/"cases.json").write_text(json.dumps(cases,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
(out/"report.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf8")
with (out/"assignments.csv").open("w",newline="",encoding="utf8") as f:
    w=csv.DictWriter(f,fieldnames=["id","assignment","classification","result","file","line","markers","reason"])
    w.writeheader()
    for x in cases:w.writerow({k:(";".join(x[k]) if isinstance(x[k],list) else x.get(k,"")) for k in w.fieldnames})
with (out/"sha256sums.txt").open("w") as f:
    for p in sorted(out.glob("*")):
        if p.name=="sha256sums.txt":continue
        f.write(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name+"\n")
print("LIBRARIAN: cases",len(cases),"assignments",counts,"previous",baseline["state"])
print("PASS: deterministic triage and ledger; HOLD: primary research, independently verified case closure")
