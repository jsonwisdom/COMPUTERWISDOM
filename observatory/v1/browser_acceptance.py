from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_default_timeout(5000)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto("http://127.0.0.1:8767/observatory/v1/")
    page.get_by_text("10/10 manifest byte checks passed", exact=False).wait_for()

    search = page.locator("input").first

    def count(n):
        expect(page.get_by_text(
            f"{n} matching findings", exact=True
        )).to_be_visible()

    for q,n in [("SSA-001",1),("NONEXISTENT",0)]:
        search.fill(q)
        count(n)
    search.fill("")

    cases = {
        "lane": [("2",1),("6",1),("3",0)],
        "state": [("US",1),("MN",0)],
        "status": [
            ("HOLD",1),
            ("OPERATOR_DECLARED_UNTIL_REPLAYED",1),
            ("VERIFIED",0),("FAILED",0),
            ("UNKNOWN",0),("PUBLISHED",0)
        ]
    }

    for key, tests in cases.items():
        control = page.locator("#" + key)
        for value,n in tests:
            control.select_option(value=value)
            count(n)
            control.select_option(index=0)
            print("PASS:", key, value)

    assert not errors, errors
    print("BROWSER_ACCEPTANCE: 13/13 PASS")
    browser.close()
