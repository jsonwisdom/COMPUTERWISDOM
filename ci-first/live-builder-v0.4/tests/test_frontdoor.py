"""CI-FIRST front-door validation; no keys, RPC, network, or external packages."""
import datetime
import json
import pathlib
import unittest
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1] / "site"

def load(name):
    with (ROOT / name).open(encoding="utf-8") as handle:
        return json.load(handle)

class HtmlRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.sources = []
        self.accessible_inputs = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag in ("script", "link") and ("src" in a or "href" in a):
            self.sources.append(a.get("src", a.get("href")))

class TestFrontDoor(unittest.TestCase):
    def test_public_inventory_only(self):
        data = load("projects.json")
        self.assertEqual(data["schema"], "computerwisdom.frontdoor.projects.v0.4")
        rows = data["projects"]
        self.assertEqual(data["public_count"], len(rows))
        self.assertGreater(data["private_excluded_count"], 0)
        self.assertEqual(len({r["repository"] for r in rows}), len(rows))
        self.assertEqual(len({r["id"] for r in rows}), len(rows))
        snapshot = datetime.datetime.fromisoformat(data["snapshot_utc"].replace("Z", "+00:00"))
        self.assertIsNotNone(snapshot.tzinfo)
        for r in rows:
            with self.subTest(repo=r["repository"]):
                self.assertEqual(r["visibility"], "public")
                self.assertTrue(r["repository"].startswith("jsonwisdom/"))
                self.assertEqual(r["url"], "https://github.com/" + r["repository"])
                self.assertEqual(urlparse(r["url"]).hostname, "github.com")
                self.assertEqual(r["last_seen_utc"], data["snapshot_utc"])
                self.assertIsNone(r["last_commit_utc"])
                self.assertIsNone(r["merkle_root"])
                self.assertEqual(r["nonempty"], r["size_kb"] > 0)

    def test_forest_does_not_fake_proofs(self):
        data = load("forest.json")
        self.assertEqual(data["schema"], "computerwisdom.frontdoor.forest.v0.4")
        self.assertEqual(data["source_schema_id"], "MERKLE_FOREST_SCHEMA_V1")
        self.assertEqual(data["forest_root"], "PENDING_HASH")
        self.assertEqual(data["forest_state"], "CANDIDATE")
        self.assertEqual(data["bridge_receipts_count"], 0)
        trees = data["trees"]
        self.assertEqual(len(trees), 5)
        self.assertEqual(len(data["groves"]), 3)
        ids = [t["id"] for t in trees]
        self.assertEqual(len(set(ids)), len(ids))
        for t in trees:
            self.assertIn(t["state"], data["canonical_states"])
            self.assertEqual(t["root"], "PENDING_HASH")
            self.assertIsNone(t["verified_leaf_count"])
            self.assertEqual(t["evidence"], "ROOT_NOT_COMPUTED")
        for grove in data["groves"]:
            self.assertTrue(set(grove["member_tree_ids"]).issubset(ids))
            self.assertEqual(grove["root"], "PENDING_HASH")

    def test_html_has_accessible_controls_and_local_assets(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        parser = HtmlRefs()
        parser.feed(page)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for required_id in ("main", "search", "size-filter", "projects-list", "forest-list", "snapshot", "contribute"):
            self.assertIn(required_id, parser.ids)
        for asset in ("./styles.css", "./app.js"):
            self.assertIn(asset, parser.sources)
            self.assertTrue((ROOT / asset).is_file())
        self.assertIn('aria-live="polite"', page)
        self.assertIn('href="#main"', page)
        self.assertIn("No tokens, wallet, or fee required.", page)
        self.assertNotIn("drive.google.com", page)
        self.assertNotIn("docs.google.com", page)

if __name__ == "__main__":
    unittest.main()
