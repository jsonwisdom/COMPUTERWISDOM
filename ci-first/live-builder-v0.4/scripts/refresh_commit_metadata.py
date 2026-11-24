#!/usr/bin/env python3
"""Refresh public GitHub repository DEFAULT-BRANCH commit metadata.

The original inventory remains the observation baseline. Only commit fields are
updated; project scope, ordering, public visibility and timestamp remain fixed.
Run with --output to produce a review artifact without writing the source.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASELINE = "2026-11-19T04:45:29.213Z"
EXPECTED = (81, 7, 65, 16)
API = "https://api.github.com"
def iso(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp must be an explicit UTC ISO8601 string")
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.utcoffset() != dt.timedelta(0):
        raise ValueError("timestamp not UTC")
    return parsed

def request_json(url, token, retries=3):
    headers = {"Accept":"application/vnd.github+json", "User-Agent":"ComputerWisdom-CI-FIRST/0.4",
               "X-GitHub-Api-Version":"2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=20) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 502, 503, 504) and attempt < retries-1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("GitHub API returned HTTP " + str(exc.code) + " for public repo metadata") from exc
        except (OSError, TimeoutError) as exc:
            if attempt < retries-1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("GitHub API transport error") from exc
    raise RuntimeError("retry limit exceeded")

def validate(data):
    if data.get("schema") != "computerwisdom.frontdoor.projects.v0.4":
        raise ValueError("unsupported inventory schema")
    if data.get("snapshot_utc") != BASELINE:
        raise ValueError("historical snapshot altered")
    records = data.get("projects", [])
    if (len(records), data.get("private_excluded_count"),
            sum(bool(r.get("nonempty")) for r in records),
            sum(not bool(r.get("nonempty")) for r in records)) != EXPECTED:
        raise ValueError("public/private/size partition drift")
    if len({r.get("repository") for r in records}) != len(records):
        raise ValueError("duplicate repository")
    for r in records:
        repo = r.get("repository", "")
        if (r.get("visibility") != "public" or not repo.startswith("jsonwisdom/")
                or r.get("url") != "https://github.com/" + repo
                or r.get("last_seen_utc") != BASELINE):
            raise ValueError("privacy, source URL or observation time contract failed")
        if not r.get("default_branch"):
            raise ValueError("missing default branch")
        if not r.get("nonempty") and any(r.get(k) is not None for k in
                ("last_commit_utc", "last_commit_sha", "last_commit_url")):
            raise ValueError("fabricated commit metadata for empty repo")
        when = r.get("last_commit_utc")
        if when is not None:
            iso(when)
            sha = r.get("last_commit_sha")
            if not isinstance(sha, str) or len(sha) != 40 or any(c not in "0123456789abcdefABCDEF" for c in sha):
                raise ValueError("invalid commit SHA")
            if r.get("last_commit_url") != "https://github.com/" + repo + "/commit/" + sha:
                raise ValueError("invalid commit source URL")

def refresh(data, token):
    validate(data)
    rows = data["projects"]
    failures = []
    for index, row in enumerate(rows):
        if not row["nonempty"]:
            row["last_commit_utc"] = None
            row["last_commit_sha"] = None
            row["last_commit_url"] = None
            continue
        # A direct GET /commits/{branch} follows that exact default branch,
        # unlike search-index order or latest-any-branch search results.
        repo = row["repository"]
        branch = urllib.parse.quote(row["default_branch"], safe="")
        url = API + "/repos/" + repo + "/commits/" + branch
        try:
            result = request_json(url, token)
            sha = result["sha"]
            commit = result["commit"]
            timestamp = commit["committer"]["date"]
            iso(timestamp)
            if result.get("html_url") != "https://github.com/" + repo + "/commit/" + sha:
                raise ValueError("commit source URL mismatch")
            row["last_commit_utc"] = timestamp
            row["last_commit_sha"] = sha
            row["last_commit_url"] = result["html_url"]
            row["last_commit_source"] = "GitHub GET /repos/{owner}/{repo}/commits/{default_branch}"
        except (KeyError, ValueError, RuntimeError, urllib.error.URLError) as exc:
            failures.append({"repository":repo, "error":type(exc).__name__})
            # Don't silently reuse possibly stale values.
            row["last_commit_utc"] = None
            row["last_commit_sha"] = None
            row["last_commit_url"] = None
        if (index + 1) % 10 == 0:
            print(f"Queried {index+1} inventory rows", file=sys.stderr)
    data["commit_metadata"] = {
        "source":"GitHub REST default-branch commit endpoint",
        "retrieved_count":sum(bool(r["last_commit_utc"]) for r in rows),
        "missing_count":sum(r["nonempty"] and r["last_commit_utc"] is None for r in rows),
        "requested_count":sum(r["nonempty"] for r in rows),
        "failed_repositories":failures,
        "observation_timestamp_preserved":BASELINE,
        "meaning":"last_commit_utc is the committer date on the latest commit at the observed default branch; it may postdate the original inventory observation",
    }
    validate(data)
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", help="Write review artifact here, leaving --input unchanged")
    parser.add_argument("--preserve-snapshot", action="store_true", required=True)
    parser.add_argument("--null-for-empty", action="store_true", required=True)
    parser.add_argument("--require-complete", action="store_true", help="Fail if any nonempty repository has no commit metadata")
    args = parser.parse_args()
    src = pathlib.Path(args.input)
    data = json.loads(src.read_text(encoding="utf-8"))
    refreshed = refresh(data, os.environ.get("GITHUB_TOKEN"))
    out = pathlib.Path(args.output) if args.output else src
    out.write_text(json.dumps(refreshed, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k:refreshed["commit_metadata"][k] for k in ("retrieved_count","requested_count","missing_count")},indent=2))
    if args.require_complete and refreshed["commit_metadata"]["missing_count"]:
        sys.exit("Incomplete metadata; artifact written for investigation, not promotion.")

if __name__ == "__main__":
    main()
