import pytest
from playwright.sync_api import sync_playwright
from objectexist import TestPage

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        yield browser
        browser.close()

@pytest.fixture
def my_page(browser):
    page = browser.new_page()
    page.pause()
    # page.pause()
    my_page_instance = TestPage(page)
    yield my_page_instance