"""Normal-origin acceptance tests for Picture Porch v0.1.

Covers: shelf persistence after reload, daily painting cap (8),
concurrent-tab quota contention, PNG and TXT download content.

Requires: pip install playwright && python -m playwright install chromium

Note: Some environments block localhost navigation
(ERR_BLOCKED_BY_ADMINISTRATOR). A blocked run must not be reported as PASS.
"""
from pathlib import Path
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from playwright.sync_api import sync_playwright, expect
import re

root = Path(__file__).parent


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(root), **kwargs)

    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_port}/index.html"

try:
    with sync_playwright() as p:
        # Playwright-managed Chromium (portable; no hard-coded OS path)
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            accept_downloads=True,
            viewport={"width": 1250, "height": 880},
        )
        page = context.new_page()
        errors = []
        requests = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("request", lambda r: requests.append(r.url))

        page.goto(url, wait_until="load")
        expect(page.locator("#counter")).to_contain_text("0 of 8")
        page.screenshot(
            path=str(root / "picture-porch-desktop.png"), full_page=True
        )
        print("INIT: 0 of 8; local store ready")
        assert not errors, errors
        assert all(u.startswith("http://127.0.0.1:") for u in requests), requests

        # --- Word picture (does not consume painting quota) ---
        page.locator("#words").click()
        # Word pictures deliberately consume ZERO paintings. Waiting for
        # "0 of 8" is insufficient because it was already displayed before
        # the asynchronous IndexedDB commit and Shelf refresh completed.
        expect(page.locator(".shelf-item")).to_have_count(1, timeout=15000)
        expect(page.locator("#notice")).to_contain_text(
            "Your word picture is on your private Shelf", timeout=15000
        )
        assert "0 of 8" in page.locator("#counter").inner_text()
        assert page.locator(".shelf-item").count() == 1
        assert page.locator("#joy").is_visible()

        # TXT download content check
        with page.expect_download() as dl_info:
            page.locator("#download").click()
        download = dl_info.value
        assert download.suggested_filename == "picture-porch.txt"
        txt_path = root / "_test_word.txt"
        download.save_as(txt_path)
        txt_body = txt_path.read_text(encoding="utf-8")
        assert "pancake" in txt_body.lower() or "Imagine" in txt_body or "✨" in txt_body
        assert len(txt_body) > 20
        txt_path.unlink(missing_ok=True)
        print("WORD: word picture stored; TXT download content verified; no count used")

        # Shelf persistence after reload
        page.reload()
        expect(page.locator(".shelf-item")).to_have_count(1)
        expect(page.locator("#counter")).to_contain_text("0 of 8")
        print("RELOAD: shelf persists; counter still 0 of 8")

        # --- First painting + PNG download ---
        page.locator("#paint").click()
        expect(page.locator("#counter")).to_contain_text("1 of 8")
        assert page.locator(".shelf-item").count() == 2
        assert page.locator("#joy").is_visible()
        assert page.locator("#art").is_visible()

        with page.expect_download() as dl_info:
            page.locator("#download").click()
        download = dl_info.value
        assert download.suggested_filename == "picture-porch.png"
        png_path = root / "_test_paint.png"
        download.save_as(png_path)
        png_bytes = png_path.read_bytes()
        # PNG signature
        assert png_bytes[:8] == b"\x89PNG\r\n\x1a\n"
        assert len(png_bytes) > 500
        png_path.unlink(missing_ok=True)
        page.screenshot(
            path=str(root / "picture-porch-painted.png"), full_page=True
        )
        print("PAINT: painting saved; PNG download content verified; count 1")

        # Contact-details guard
        page.locator("#prompt").fill(
            "Call me at 555-444-1234 for pancakes please"
        )
        page.locator("#paint").click()
        assert "contact details" in page.locator("#notice").inner_text()
        assert "1 of 8" in page.locator("#counter").inner_text()
        print("GUARD: contact-details prompt blocked")

        # Stage seven paintings: the first seven slots are occupied.
        # The two tabs must both observe an available eighth slot.
        page.locator("#prompt").fill("A happy rainbow duck in rain boots!")
        for i in range(6):
            page.locator("#paint").click()
            expect(page.locator("#counter")).to_contain_text(f"{i + 2} of 8")
        assert page.locator(".shelf-item").count() == 8  # one word + seven paints
        assert page.locator("#paint").is_enabled()
        print("CAP: seven paintings saved, one slot remains")

        # --- Actual cross-tab contention at 7/8 (not post-cap disabled clicks) ---
        # Both tabs share an origin and IndexedDB, observe 7/8, and queue a
        # painting attempt for the same wall-clock deadline.
        page2 = context.new_page()
        page2.on("pageerror", lambda e: errors.append("tab2: " + str(e)))
        page2.on("request", lambda r: requests.append(r.url))
        page2.goto(url, wait_until="load")
        expect(page2.locator("#counter")).to_contain_text("7 of 8")
        assert page2.locator("#paint").is_enabled()

        page.locator("#prompt").fill("A rainbow duck dances with a spoon!")
        page2.locator("#prompt").fill("A silly robot waves from another tab!")
        for tab in (page, page2):
            tab.evaluate(
                'document.querySelector("#notice").textContent = "RACE_PENDING"'
            )
        deadline_ms = int(time.time() * 1000) + 1500
        for tab in (page, page2):
            tab.evaluate(
                """deadline => {
                    const button = document.querySelector("#paint");
                    setTimeout(() => button.click(), Math.max(0, deadline - Date.now()));
                }""",
                deadline_ms,
            )

        for tab in (page, page2):
            expect(tab.locator("#notice")).to_contain_text(
                re.compile(r"Your little cartoon is on your private Shelf!|Eight paintings are already"),
                timeout=15000,
            )
        notices = [tab.locator("#notice").inner_text() for tab in (page, page2)]
        winners = sum("Your little cartoon is on your private Shelf!" in n for n in notices)
        losers = sum("Eight paintings are already" in n for n in notices)
        assert (winners, losers) == (1, 1), notices

        # Read back from storage in BOTH tabs. Exactly one eighth painting
        # is committed; the denied write creates no ninth painting.
        for tab in (page, page2):
            tab.reload()
            expect(tab.locator("#counter")).to_contain_text("8 of 8")
            expect(tab.locator(".shelf-item")).to_have_count(9)
            assert tab.locator("#paint").is_disabled()
        print("MULTI_TAB: both attempted at 7/8; one succeeded; one denied; total 8")
        page2.close()

        # Final consistency checks
        page.reload()
        expect(page.locator("#counter")).to_contain_text("8 of 8")
        assert page.locator("#paint").is_disabled()
        assert page.locator(".shelf-item").count() == 9
        assert not errors, errors
        assert all(u.startswith("http://127.0.0.1:") for u in requests), requests
        print(
            "RELOAD: count and shelf persist; no JS errors; no external requests"
        )

        context.close()
        browser.close()
finally:
    server.shutdown()
