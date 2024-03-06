import pytest
from playwright.sync_api import sync_playwright

from EXIST_TEST.oop_dtp import TestPage

# Сторінка яку тестуємо
url = 'https://dtp.com.ua'

# Відкриваємо браузер, переходимо на потрібну сторінку
@pytest.fixture
def test_page(request, headless=False, slow_mo=200):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        page = browser.new_page()
        page.goto(url)
        page.pause()
        yield TestPage(page)
        browser.close()

