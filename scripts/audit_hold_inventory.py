#!/usr/bin/env python3
"""Read-only inventory of proof gaps, not a verdict on truth or completion."""
import csv, datetime, hashlib, json, pathlib, re, subprocess
ROOT=pathlib.Path(".")
PAT=re.compile(r"(?<![A-Z0-9_])(?:HOLD(?:_[A-Z0-9_]+)?|HELD|PENDING(?:_[A-Z0-9_]+)?|NOT_(?:VERIFIED|PROVEN|ESTABLISHED|IMPLEMENTED|RECOVERED|TESTED|PERFORMED)|UNRECOVERED|UNVERIFIED|UNKNOWN|MISSING(?:_[A-Z0-9_]+)?|PLACEHOLDER(?:_[A-Z0-9_]+)?|NO_OPERATIONAL_CORRELATION_ESTABLISHED)(?![A-Z0-9_])",re.I)
EXT={".md",".txt",".json",".jsonl",".yaml",".yml",".py",".js",".mjs",".ts",".html",".csv",".toml",".sh",".ps1"}
SKIP={".git","node_modules","dist","build",".next","vendor",".venv","venv","coverage"}
MAX_FILE=2_000_000
rows=[]; unreadable=[]; scanned=0; bytes_scanned=0
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or any(x in SKIP for x in p.parts) or p.suffix.lower() not in EXT: continue
    try:
        if p.stat().st_size>MAX_FILE:
            unreadable.append({"path":p.as_posix(),"reason":"OVERSIZED"});continue
        data=p.read_bytes(); s=data.decode("utf-8-sig")
    except (UnicodeError,OSError) as e:
        unreadable.append({"path":p.as_posix(),"reason":type(e).__name__});continue
    scanned+=1;bytes_scanned+=len(data)
    for n,line in enumerate(s.splitlines(),1):
        hits=sorted({m.group().upper() for m in PAT.finditer(line)})
        if not hits:continue
        nearby=line.strip().replace("\t"," ")
        # A mention is a candidate only: code/tests/docs may contain example tokens.
        kind="REFERENCE_OR_EXAMPLE"
        if re.search(r"(status|state|disposition|verification|authority|recovery|source|evidence|signature|receipt|production|eligib|execution|completion|pending|hold)\s*[:=|]",line,re.I):
            kind="STATUS_CANDIDATE"
        if re.search(r"(?i)(example|fixture|mock|sample|test.vector|regex|enum|schema)",p.as_posix()):kind="TEST_OR_SCHEMA_REFERENCE"
        rows.append({"path":p.as_posix(),"line":n,"markers":";".join(hits),"classification":kind,"excerpt":nearby[:350]})
out=pathlib.Path("hold-inventory");out.mkdir(exist_ok=True)
with (out/"all-markers.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["path","line","markers","classification","excerpt"]);w.writeheader();w.writerows(rows)
from collections import Counter
statuses=[r for r in rows if r["classification"]=="STATUS_CANDIDATE"]
summary={"schema":"SOW-HOLD-INVENTORY-0.1","at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"root":"COMPUTERWISDOM checked-out PR commit","scan_scope":"UTF-8 known text extensions <=2MB per file; not branches, other repos, GitHub Issues, private records, or chain state",
"files_scanned":scanned,"bytes_scanned":bytes_scanned,"marker_occurrences_by_line":len(rows),
"status_candidate_lines":len(statuses),"files_with_markers":len({r["path"] for r in rows}),
"markers_frequency_by_line":dict(Counter(m for r in rows for m in r["markers"].split(";"))),
"candidate_files":dict(Counter(r["path"] for r in statuses).most_common(100)),
"unreadable_or_skipped_large":unreadable,"limitations":"Search hits include safety policy, examples, old documents, and deliberate HOLDs; cannot assert all open tasks or no proof. No automatic promotion.",
"overall":"RESEARCH_GAP_CANDIDATES_ONLY","authority":False,"production_state":"HOLD"}
raw=(json.dumps(summary,indent=2,sort_keys=True)+"\n").encode()
(out/"summary.json").write_bytes(raw)
(out/"summary.sha256").write_text(hashlib.sha256(raw).hexdigest()+"  summary.json\n")
with open("hold-inventory/top-status-candidates.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=["path","line","markers","classification","excerpt"]);w.writeheader();w.writerows(statuses)
print(f"Scanned {scanned} files; marker lines={len(rows)}; status candidates={len(statuses)}; skipped={len(unreadable)}")
