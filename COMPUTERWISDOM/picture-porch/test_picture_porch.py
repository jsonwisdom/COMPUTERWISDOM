from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
root=Path(__file__).parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(root), **kwargs)
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/index.html'
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    context=browser.new_context(accept_downloads=True,viewport={'width':1250,'height':880})
    page=context.new_page()
    errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto(url,wait_until='load')
    page.wait_for_function('document.querySelector("#counter").textContent.includes("0 of 8")')
    page.screenshot(path=str(root/'picture-porch-desktop.png'),full_page=True)
    print('INIT: 0 of 8; local store ready')
    assert not errors, errors
    assert all(u.startswith('http://127.0.0.1:') for u in requests),requests
    page.locator('#words').click()
    page.wait_for_function('document.querySelector("#counter").textContent.includes("0 of 8")')
    assert 'Your word picture is on your private Shelf' in page.locator('#notice').inner_text()
    assert page.locator('.shelf-item').count()==1
    assert page.locator('#joy').is_visible()
    page.reload()
    page.wait_for_function('document.querySelectorAll(".shelf-item").length === 1')
    print('WORD: word picture stored; shelf persists after reload; no count used')
    page.locator('#paint').click()
    page.wait_for_function('document.querySelector("#counter").textContent.includes("1 of 8")')
    assert page.locator('.shelf-item').count()==2
    assert page.locator('#joy').is_visible()
    assert page.locator('#art').is_visible()
    page.screenshot(path=str(root/'picture-porch-painted.png'),full_page=True)
    print('PAINT: painting saved; JOY question displayed; count 1')
    page.locator('#prompt').fill('Call me at 555-444-1234 for pancakes please')
    page.locator('#paint').click()
    assert 'contact details' in page.locator('#notice').inner_text()
    assert '1 of 8' in page.locator('#counter').inner_text()
    print('GUARD: contact-details prompt blocked')
    page.locator('#prompt').fill('A happy rainbow duck in rain boots!')
    for i in range(7):
      page.locator('#paint').click()
      page.wait_for_function(f'document.querySelector("#counter").textContent.includes("{i+2} of 8")')
    assert page.locator('#paint').is_disabled()
    assert page.locator('.shelf-item').count()==9
    print('CAP: eighth painting allowed; ninth disabled')
    page.reload()
    page.wait_for_function('document.querySelector("#counter").textContent.includes("8 of 8")')
    assert page.locator('#paint').is_disabled()
    assert page.locator('.shelf-item').count()==9
    assert not errors,errors
    assert all(u.startswith('http://127.0.0.1:') for u in requests),requests
    print('RELOAD: count and shelf persist; no JS errors; no external requests')
    context.close();browser.close()
finally:
 server.shutdown()
