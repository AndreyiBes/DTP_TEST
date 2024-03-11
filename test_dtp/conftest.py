import pytest
from playwright.sync_api import sync_playwright
from pageobject.oop_dtp import TestPage

url = 'https://dtp.com.ua'

# @pytest.fixture
# def test_page(request, headless=False, slow_mo=3000):
#     with sync_playwright () as p:
#         browser = p.chromium.launch ( headless = headless, slow_mo = slow_mo )
#         context = browser.new_context (record_video_dir = './videos/')
#         page = context.new_page ()
#         page.goto ( url )
#         page.pause ()
#         yield TestPage ( page )
#         context.close ()
#         browser.close ()


@pytest.fixture ()
def test_page(request, browsers=None, headless=False, slow_mo=3000):
    if browsers is None:
        browsers = ['chromium']
    valid_browsers = ['chromium', 'firefox', 'webkit']
    for browser_type in browsers:
        if browser_type not in valid_browsers:
            raise ValueError(f"Invalid browser type: {browser_type}")
    with sync_playwright() as p:
        for browser_type in browsers:
            browser = getattr(p, browser_type).launch(headless=headless, slow_mo=slow_mo)
            context = browser.new_context(record_video_dir=f'./videos/{browser_type}/')
            page = context.new_page()
            page.goto(url)
            page.pause()
            yield TestPage(page)
            context.close()
            browser.close()
