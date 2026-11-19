"""Metadata refresh invariants: original observation and public-only policy."""
import importlib.util
import json
import pathlib
import unittest
from unittest.mock import patch

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("refresh_commit_metadata", ROOT / "scripts" / "refresh_commit_metadata.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class MetadataTest(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"site"/"projects.json").read_text(encoding="utf-8"))
    def test_unmodified_snapshot_contract(self):
        mod.validate(self.data)
        self.assertEqual(self.data["snapshot_utc"],mod.BASELINE)
    def test_private_entry_rejected(self):
        self.data["projects"][0]["visibility"]="private"
        with self.assertRaises(ValueError):
            mod.validate(self.data)
    def test_last_seen_mutation_rejected(self):
        self.data["projects"][0]["last_seen_utc"]="2020-01-01T00:00:00Z"
        with self.assertRaises(ValueError):
            mod.validate(self.data)
    def test_empty_repo_commit_rejected(self):
        empty=next(r for r in self.data["projects"] if not r["nonempty"])
        empty["last_commit_utc"]="2026-11-18T05:00:00Z"
        with self.assertRaises(ValueError):
            mod.validate(self.data)
    def test_real_branch_metadata_and_late_commit_allowed(self):
        target=next(r for r in self.data["projects"] if r["nonempty"])
        sha="a"*40
        target.update(last_commit_utc="2026-11-20T00:00:00Z",last_commit_sha=sha,last_commit_url=target["url"]+"/commit/"+sha)
        mod.validate(self.data)
    def test_bad_sha_or_source_rejected(self):
        target=next(r for r in self.data["projects"] if r["nonempty"])
        target.update(last_commit_utc="2026-11-20T00:00:00Z",last_commit_sha="abc",last_commit_url=target["url"]+"/commit/abc")
        with self.assertRaises(ValueError):
            mod.validate(self.data)
    def test_branch_lookup_not_any_branch_search(self):
        calls=[]
        def get(url,token):
            calls.append(url)
            sha="b"*40
            repo=url.split("/repos/",1)[1].split("/commits/",1)[0]
            return {"sha":sha,"html_url":"https://github.com/"+repo+"/commit/"+sha,"commit":{"committer":{"date":"2026-11-19T13:00:00Z"}}}
        with patch.object(mod,"request_json",side_effect=get):
            refreshed=mod.refresh(self.data,"test-token-not-sent")
        self.assertEqual(len(calls),65)
        self.assertEqual(refreshed["commit_metadata"]["retrieved_count"],65)
        self.assertEqual(refreshed["commit_metadata"]["missing_count"],0)
        self.assertTrue(all("/commits/" in c for c in calls))
        self.assertEqual(refreshed["snapshot_utc"],mod.BASELINE)
        self.assertTrue(all(r["last_seen_utc"]==mod.BASELINE for r in refreshed["projects"]))
        self.assertTrue(all(r["last_commit_utc"] is None for r in refreshed["projects"] if not r["nonempty"]))

if __name__=="__main__":
    unittest.main()
