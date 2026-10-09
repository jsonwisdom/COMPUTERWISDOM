#!/usr/bin/env python3
"""Read-only daily operator packet. JSON + Markdown output, no repo/Drive writes."""
import datetime as dt
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out" / "operator"
OWNER_REPO = "jsonwisdom/COMPUTERWISDOM"
BASE = "https://api.github.com/repos/" + OWNER_REPO
CT = ZoneInfo("America/Chicago")

def current_time():
    return dt.datetime.now(CT)

def request_json(url):
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "computerwisdom-operator-morning/0.1", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as stream:
            return json.loads(stream.read(500000).decode("utf-8")), None
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError) as exc:
        return None, type(exc).__name__ + ": " + str(exc)

def pull(number):
    data, err = request_json(BASE + "/pulls/" + str(number))
    if data is None:
        return {"number": number, "status": "NOT_FETCHED", "reason": err, "url": "https://github.com/" + OWNER_REPO + "/pull/" + str(number)}
    return {"number": number, "state": data.get("state"), "draft": data.get("draft"), "merged": data.get("merged"),
            "head_sha": (data.get("head") or {}).get("sha"), "base_sha": (data.get("base") or {}).get("sha"),
            "url": data.get("html_url"), "updated_at": data.get("updated_at"), "status": "OBSERVED_METADATA_ONLY"}

def main():
    now = current_time()
    d = now.date().isoformat()
    matrix = json.loads((ROOT / "operator" / "SIGNING_MATRIX_V0_1.json").read_text(encoding="utf-8"))
    pr649 = pull(649)
    pr650 = pull(650)
    actions = [
      {"order": 1, "action": "Keep old JayWisdom Base signing page disabled; do not solicit signatures from it.", "status": "SECURITY_HOLD"},
      {"order": 2, "action": "Check hosted runtime separately for static HOLD notice. GitHub source and deployment alone are insufficient.", "status": "RUNTIME_CHECK_NEEDED"},
      {"order": 3, "action": "Review new candidate workbench code; obtain named independent reviewer and explicit human merge approval.", "status": "REVIEW_NEEDED"},
      {"order": 4, "action": "Keep PROCESS-649 open regardless of retention. New decision is not retroactive approval.", "status": "PROCESS_OPEN"},
      {"order": 5, "action": "Integrate PR #650 with post-649 master and review gate-integrity, PASS semantics, and receipt completeness before merge.", "status": "CI_HOLD"},
    ]
    report = {
      "schema": "COMPUTERWISDOM_OPERATOR_MORNING_V0_1",
      "generated_at": now.isoformat(), "date_ct": d,
      "source": {"repository": OWNER_REPO, "kind": "READ_ONLY_GITHUB_API_AND_PINNED_SIGNER_INVENTORY"},
      "pr649": pr649, "pr650": pr650,
      "signin_inventory": matrix["paths"],
      "actions": actions,
      "drive_upload": "NOT_CONFIGURED_IN_GITHUB_WORKFLOW",
      "signed_receipt_created": False,
      "runtime_verified": False,
      "human_approval_verified": False,
      "canon": False, "authority_created": False,
      "note": "GitHub CI success is not authorization, runtime proof or verified identity. This is an operator checklist, not a live signature receipt."
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (d + ".json")).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# CWaaS morning: " + d,
             "Generated " + now.isoformat() + " (America/Chicago). Read-only; NOT an identity or approval receipt.",
             "", "## Do this next"]
    lines += [str(a["order"]) + ". **" + a["status"] + "** — " + a["action"] for a in actions]
    lines += ["", "## Verified metadata / unresolved runtime"]
    for p in (pr649, pr650):
        lines += ["- PR #" + str(p["number"]) + ": " + p.get("status", "UNKNOWN") +
                 " · " + str(p.get("state", "UNKNOWN")) + " · draft " + str(p.get("draft", "UNKNOWN")) +
                 " · head " + str(p.get("head_sha", "UNKNOWN")) + " · " + str(p.get("url", ""))]
    lines += ["", "## Existing signing files (presence is NOT clearance)"]
    for item in matrix["paths"]:
        lines += ["- **" + item["name"] + "** — " + item["state"] + " — " + item["path"]]
    lines += ["", "## Boundaries", "- Protected signer remains disabled; do not use other signers as an unreviewed bypass.",
              "- No automatic Drive upload: GitHub has no configured least-privilege Drive credential in this workflow.",
              "- GitHub workflow artifact is a time-stamped checklist, NOT a user notification, signed receipt, or live deployment verification.",
              "- PROCESS-649 open. Human authorization separate from CI.", ""]
    (OUT / (d + ".md")).write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"created_files": [str(OUT / (d + ".json")), str(OUT / (d + ".md"))],
                      "date_ct": d, "pr649": pr649.get("status"), "pr650": pr650.get("status"),
                      "drive_upload": "NOT_CONFIGURED", "authority_created": False}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
