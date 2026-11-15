#!/usr/bin/env python3
"""CI-FIRST: read-only dual-route probe; Python standard library only."""
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

TARGETS = [
 ("PRIMARY","cw-ooda-emergency-50state-v01","https://emergency.jsonwisdom.com/api/v1/health"),
 ("REPLICA","cw-ooda-emergency-50state-replica-v01","https://emergency.jsonwisdom.io/api/v1/health"),
]
EXPECTED="cw-ooda-emergency-estate/0.1"
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00","Z")
def canonical(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False)
def sha(b): return hashlib.sha256(b).hexdigest()
def probe(target):
 role,worker,url=target
 r=dict(role=role,worker=worker,url=url,observed_utc=utc(),http=None,cf_ray=None,status="UNKNOWN",body_sha256=None,body_base64=None,error=None,schema=None,state_count=None,source_bundles_verified=None)
 try:
  req=urllib.request.Request(url,method="GET",headers={"Accept":"application/json","User-Agent":"CW-CI-FIRST/0.2"})
  with urllib.request.urlopen(req,timeout=20) as response:
   r["http"]=response.status
   r["cf_ray"]=response.headers.get("CF-Ray")
   body=response.read(65537)
  if len(body)>65536: raise ValueError("Body over 64KiB")
  r["body_sha256"]=sha(body)
  r["body_base64"]=base64.b64encode(body).decode("ascii")
  d=json.loads(body)
  if not isinstance(d,dict): raise ValueError("JSON is not object")
  r["schema"]=d.get("schema")
  r["state_count"]=d.get("state_count")
  r["source_bundles_verified"]=d.get("source_bundles_verified")
  valid=(r["http"]==200 and d.get("status")=="OK" and r["schema"]==EXPECTED
    and type(r["state_count"]) is int and r["state_count"]==50
    and type(r["source_bundles_verified"]) is int and r["source_bundles_verified"]>=0
    and d.get("authority_created") is False and d.get("live_alerts") is False)
  r["status"]="PASS" if valid else "HOLD"
 except urllib.error.HTTPError as e:
  r["http"]=e.code; r["cf_ray"]=e.headers.get("CF-Ray"); r["error"]="HTTP_"+str(e.code)
 except Exception as e:
  r["error"]=type(e).__name__+": "+str(e)[:150]
 return r

def verify_receipt(receipt):
 """Integrity and scope checks; not government-source authentication."""
 if receipt.get("schema") != "cw-dual-route-probe/0.2":
  return False
 digest = receipt.get("canonical_sha256")
 unsigned = {k:v for k,v in receipt.items() if k != "canonical_sha256"}
 if not isinstance(digest,str) or digest != sha(canonical(unsigned).encode("utf-8")):
  return False
 routes=receipt.get("routes")
 if not isinstance(routes,list) or len(routes)!=2:
  return False
 if [r.get("role") for r in routes]!=["PRIMARY","REPLICA"]:
  return False
 for r in routes:
  encoded=r.get("body_base64")
  if encoded is None:
   if r.get("body_sha256") is not None:
    return False
   continue
  try:
   raw=base64.b64decode(encoded,validate=True)
   if sha(raw)!=r.get("body_sha256"):
    return False
   data=json.loads(raw)
  except Exception:
   return False
  if r.get("status")=="PASS" and not (
   r.get("http")==200 and data.get("schema")==EXPECTED
   and type(data.get("state_count")) is int and data["state_count"]==50
   and type(data.get("source_bundles_verified")) is int
   and data["source_bundles_verified"]>=0
   and data.get("authority_created") is False
   and data.get("live_alerts") is False
  ):
   return False
 if receipt.get("authority_created") is not False:
  return False
 if receipt.get("live_emergency_feed")!="NOT_ESTABLISHED":
  return False
 return True

def main():
 paths=Path(os.getenv("CW_RECEIPT_DIR","cw-two-route-logs"))
 routes=[probe(t) for t in TARGETS]
 good=all(t["status"]=="PASS" for t in routes)
 receipt=dict(schema="cw-dual-route-probe/0.2",time_utc=utc(),routes=routes,
  two_route_status="PASS" if good else "UNKNOWN",
  parity="PASS" if good and routes[0]["body_sha256"]==routes[1]["body_sha256"] else "UNKNOWN",
  cross_provider_failover="NOT_ESTABLISHED",live_emergency_feed="NOT_ESTABLISHED",
  authority_created=False,purpose="Public evidence literacy",function="Dual route HTTP verification",
  joy="Human-approved deidentified lessons; no chat ingestion")
 receipt["canonical_sha256"]=sha(canonical(receipt).encode("utf-8"))
 paths.mkdir(parents=True,exist_ok=True)
 name="cw-ooda-"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")+".json"
 if not verify_receipt(receipt): raise RuntimeError("Receipt integrity check failed")
 dest=paths/name;dest.write_text(canonical(receipt)+"\n",encoding="utf-8")
 print(canonical({"file":str(dest),"status":receipt["two_route_status"],"parity":receipt["parity"],"hash":receipt["canonical_sha256"]}))
if __name__=="__main__":main()
