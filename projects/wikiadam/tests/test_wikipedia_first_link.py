import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wikipedia_first_link as wiki


class FakePage:
    def __init__(self, articles):
        self.articles = articles
        self.url = "about:blank"

    def goto(self, url, **kwargs):
        if url not in self.articles:
            raise RuntimeError("Synthetic navigation unavailable")
        self.url = self.articles[url].get("redirect", url)

    def content(self):
        return "<main>SYNTHETIC WIKIPEDIA HTML</main>"

    def evaluate(self, _script):
        return {"next": self.articles[self.url].get("next"),
                "reason": "FIRST_BODY_LINK"}


class WikipediaFirstLinkTests(unittest.TestCase):
    def test_only_wikipedia_article_urls(self):
        self.assertTrue(wiki.allowed_article("https://en.wikipedia.org/wiki/Philosophy"))
        for x in ("https://evil.example/wiki/Philosophy",
                  "http://en.wikipedia.org/wiki/Philosophy",
                  "https://en.wikipedia.org/wiki/Special:Random",
                  "https://en.wikipedia.org/wiki/Category:Philosophy",
                  "https://en.wikipedia.org/wiki/Philosophy?x=1"):
            self.assertFalse(wiki.allowed_article(x), x)

    def test_start_topic_encodes_wiki_article(self):
        self.assertEqual(wiki.start_url("Alan Turing"), "https://en.wikipedia.org/wiki/Alan_Turing")

    def test_random_special_is_only_explicit_initial_exception(self):
        self.assertEqual(wiki.start_url(random_article=True),
                         "https://en.wikipedia.org/wiki/Special:Random")
        with self.assertRaises(ValueError):
            wiki.start_url("Banana", random_article=True)

    def test_bounded_walk_finds_philosophy(self):
        a = "https://en.wikipedia.org/wiki/Banana"
        b = "https://en.wikipedia.org/wiki/Fruit"
        c = "https://en.wikipedia.org/wiki/Philosophy"
        page = FakePage({a: {"next": b}, b: {"next": c}, c: {"next": None}})
        slept = []
        out = wiki.walk(page, a, max_hops=4, delay_seconds=1, sleep_fn=slept.append)
        self.assertEqual(out["stop_reason"], "REACHED_PHILOSOPHY")
        self.assertTrue(out["reached_philosophy"])
        self.assertEqual(len(out["steps"]), 3)
        self.assertEqual(len(slept), 2)
        self.assertFalse(out["person_authorship_proof"])

    def test_cycles_are_recorded_not_hidden(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        b = "https://en.wikipedia.org/wiki/BBB"
        out = wiki.walk(FakePage({a: {"next": b}, b: {"next": a}}), a,
                        max_hops=10, delay_seconds=1, sleep_fn=lambda _: None)
        self.assertEqual(out["stop_reason"], "CYCLE_DETECTED")
        self.assertFalse(out["reached_philosophy"])

    def test_missing_qualified_link_stops(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        out = wiki.walk(FakePage({a: {"next": None}}), a,
                        delay_seconds=1, sleep_fn=lambda _: None)
        self.assertEqual(out["stop_reason"], "NO_QUALIFIED_FIRST_LINK")

    def test_offsite_next_link_stops(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        out = wiki.walk(FakePage({a: {"next": "https://example.com/"}}), a,
                        delay_seconds=1, sleep_fn=lambda _: None)
        self.assertEqual(out["stop_reason"], "NO_QUALIFIED_FIRST_LINK")

    def test_max_hops_is_not_a_philosophy_result(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        b = "https://en.wikipedia.org/wiki/BBB"
        out = wiki.walk(FakePage({a: {"next": b}, b: {"next": a}}), a,
                        max_hops=1, delay_seconds=1, sleep_fn=lambda _: None)
        self.assertEqual(out["stop_reason"], "MAX_HOPS_REACHED")

    def test_unavailable_navigation_is_not_declared_missing_article(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        out = wiki.walk(FakePage({}), a, delay_seconds=1, sleep_fn=lambda _: None)
        self.assertEqual(out["stop_reason"], "NAVIGATION_ERROR_RuntimeError")

    def test_no_unbounded_requests(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        with self.assertRaises(ValueError):
            wiki.walk(FakePage({a: {"next": None}}), a, max_hops=999)
        with self.assertRaises(ValueError):
            wiki.walk(FakePage({a: {"next": None}}), a, delay_seconds=0)

    def test_readonly_report_keeps_independent_provenance_unclaimed(self):
        a = "https://en.wikipedia.org/wiki/AAA"
        out = wiki.walk(FakePage({a: {"next": None}}), a,
                        delay_seconds=1, sleep_fn=lambda _: None)
        self.assertFalse(out["historical_wikipedia_97_percent_verified"])
        self.assertFalse(out["person_authorship_proof"])
        self.assertEqual(len(out["steps"][0]["rendered_html_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
