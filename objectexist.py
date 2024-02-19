import configparser
from playwright.sync_api import Page


class TestPage:
    def __init__(self, page: Page):
        self.page = page
        self.load_credentials()

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

    def load_credentials(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
            self.username = config.get('credentials', 'username')
            self.password = config.get('credentials', 'password')
        except Exception as e:
            print(f"Error loading credentials from config.ini: {e}")

    def login_page(self):
        try:
            self.page.locator('.UserProfileMenustyle__UserProfileMenuDropdown-sc-r0spk5-0').click()
            self.page.fill('input[id="phone-field"]', self.username, force=True)
            self.page.fill('input[name="password"]', self.password, force=True)
            self.page.locator('.LoginFormstyle__LoginSubmit-sc-wocy7z-2').click()

            # Wait for the user menu badges to ensure they are visible
            # user_menu_badges = self.page.locator('.HeaderUserMenustyle__HeaderUserMenuBadge-sc-uxk3ae-2')
            user_menu_badges = self.page.get_by_label("dropdown-profile")
            # Iterate over user menu badges and handle based on text content
            assert user_menu_badges.is_visible(), f"{user_menu_badges}"


        except Exception as e:
            print(f"Error during login: {e}")



