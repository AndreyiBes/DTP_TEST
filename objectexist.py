from playwright.sync_api import Page

class TestPage:
    def __init__(self, page: Page):
        self.page = page

    def open_page(self, url):
        self.page.goto(url)

    def assert_title(self, expected_title):
        actual_title = self.page.title()
        assert actual_title == expected_title, f"Expected title: {expected_title}, Actual title: {actual_title}"

    def assert_search_field(self, expected_search_field_locator):
        search_field = self.page.locator(expected_search_field_locator)
        assert search_field.is_visible(), f"Expected search field to be visible, but it is not."

    def close_browser(self):
        self.page.close()

    def assert_element_visible(self, element_locator, element_name):
        element = self.page.locator(element_locator)
        assert element.is_visible(), f"{element_name} is not visible."