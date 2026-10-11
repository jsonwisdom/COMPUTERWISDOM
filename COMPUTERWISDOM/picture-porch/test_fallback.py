"""Opaque-origin / storage-unavailable smoke test for Picture Porch v0.1.

Requires: pip install playwright && python -m playwright install chromium
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

html = Path(__file__).with_name("index.html").read_text(encoding="utf-8")

with sync_playwright() as p:
    # Playwright-managed Chromium (portable; no hard-coded OS path)
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 1250, "height": 950}, device_scale_factor=1)
    errors = []
    requests = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: requests.append(r.url))
    page.set_content(html, wait_until="load")
    page.wait_for_timeout(400)

    assert page.locator("#paint").is_disabled()
    assert "Shelf unavailable" in page.locator("#counter").inner_text()
    page.screenshot(path=str(Path(__file__).with_name("picture-porch-preview.png")), full_page=True)

    page.locator("#words").click()
    assert page.locator("#joy").is_visible()
    assert page.locator("#word-panel").is_visible()
    assert "Unsaved word picture" in page.locator("#stage-status").inner_text()

    page.locator("#prompt").fill("Call me at 555-444-1234 for pancakes!")
    page.locator("#words").click()
    assert "contact details" in page.locator("#notice").inner_text()

    assert not errors, errors
    assert requests == [], requests

    print("PASS: renders UI in opaque-origin browser")
    print("PASS: fails closed when IndexedDB unavailable")
    print("PASS: word-picture fallback + JOY question works unsaved")
    print("PASS: basic contact-details guard blocks sample")
    print("PASS: no JS errors, no network requests in fallback")
    browser.close()
