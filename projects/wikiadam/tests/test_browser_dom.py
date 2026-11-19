from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wikipedia_first_link as wiki

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


@unittest.skipIf(sync_playwright is None, "Playwright/browser DOM tests run in the dedicated CI job")
class PlaywrightDomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page()
        self.addCleanup(self.page.close)

    def html(self, body):
        self.page.set_content(
            '<html><head><base href="https://en.wikipedia.org/"></head><body>'
            '<div id="mw-content-text"><div class="mw-parser-output">'
            + body + '</div></div></body></html>'
        )

    def first(self):
        return self.page.evaluate(wiki.FIRST_ARTICLE_LINK_JS)

    def test_skip_parenthetical_and_italic_first_link(self):
        self.html(
            '<p>The topic (<a href="/wiki/Wrong">wrong</a>) is '
            '<i><a href="/wiki/Also_wrong">italic link</a></i> '
            'and <a href="/wiki/Correct">correct link</a>.</p>'
        )
        o = self.first()
        self.assertEqual(o["next"], "https://en.wikipedia.org/wiki/Correct")

    def test_skip_navbox_external_and_namespaced(self):
        self.html(
            '<div class="navbox"><p><a href="/wiki/Nav">nav</a></p></div>'
            '<p><a href="https://example.org/wiki/External">out</a> '
            '<a href="/wiki/File:Example">file</a> '
            '<a href="/wiki/Actual">actual</a></p>'
        )
        self.assertEqual(self.first()["next"], "https://en.wikipedia.org/wiki/Actual")

    def test_missing_article_body_is_not_hallucinated(self):
        self.page.set_content("<html><p>no article body</p></html>")
        self.assertEqual(self.first()["reason"], "BODY_NOT_FOUND")

    def test_empty_paragraphs_do_not_invent_links(self):
        self.html("<p>Only text. No hyperlinks.</p>")
        self.assertEqual(self.first()["reason"], "NO_QUALIFIED_BODY_LINK")


if __name__ == "__main__":
    unittest.main()
