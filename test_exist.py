from EXIST_TEST.conftest import my_page


url = 'https://exist.ua'
title = 'Автозапчастини EXIST.UA: Запчастини до авто онлайн!'
search_field = "div.HeaderMiddlestyle__HeaderButtonsWrapper-sc-bi2b2x-6.sfRjK > div.HeaderSearchstyle__HeaderSearchBlock-sc-att33u-0.hinRrM > button > div > div.HeaderSearchstyle__HeaderSearchPlaceholder-sc-att33u-2.yMCVq"
footer_locator = ".Footerstyle__FooterWrapper-sc-sqw8j4-0.eCPxDk"
header_locator = ".Headerstyle__HeaderContainer-sc-4fgvrl-0"

def test_main_elements(my_page):
    # Open the target page
    my_page.open_page(url)
    # Перевіряємо що заголовок сторінки завантажився
    my_page.assert_title(title)
    # Перевіряємо що поле пошуку завантажилось
    expected_search_field_locator = search_field
    my_page.assert_search_field(expected_search_field_locator)
    # Перевіряємо що Футер сторінки завантажився
    my_page.assert_element_visible(footer_locator, "Footer Wrapper")
    # Close the browser
    my_page.close_browser()

# Перевіряємо що є можливість залогіниться на сайт та вийти користувачу з сайту
def test_login_and_logout(my_page):
    my_page.open_page(url)
    my_page.login_page()
    my_page.logout_page()
    my_page.close_browser()


if __name__ == "__main__":
    test_main_elements(my_page)
    test_login_and_logout(my_page)

