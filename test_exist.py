url = 'https://exist.ua'
title = 'Автозапчастини EXIST.UA: Запчастини до авто онлайн!'
search_field = "div.HeaderMiddlestyle__HeaderButtonsWrapper-sc-bi2b2x-6.sfRjK > div.HeaderSearchstyle__HeaderSearchBlock-sc-att33u-0.hinRrM > button > div > div.HeaderSearchstyle__HeaderSearchPlaceholder-sc-att33u-2.yMCVq"
footer_locator = ".Footerstyle__FooterWrapper-sc-sqw8j4-0.eCPxDk"
header_locator = ".Headerstyle__HeaderContainer-sc-4fgvrl-0"
# Перевіряємо що заголовок сторінки завантажився
def test_title(my_page):
    # Open the target page
    my_page.open_page(url)
    # Assert the title
    my_page.assert_title(title)
    # Close the browser
    my_page.close_browser()

# Перевіряємо що поле пошуку завантажилось
def test_search_field(my_page):
    # Open the target page
    my_page.open_page(url)
    # Assert the search field
    expected_search_field_locator = search_field
    my_page.assert_search_field(expected_search_field_locator)
    # Close the browser
    my_page.close_browser()

# Перевіряємо що Футер сторінки завантажився
def test_footer(my_page):
    # Open the target page
    my_page.open_page(url)
    # Assert the visibility of the footer wrapper
    my_page.assert_element_visible(footer_locator, "Footer Wrapper")
    # Close the browser
    my_page.close_browser()

def test_header(my_page):
    # Open the target page
    my_page.open_page(url)
    # Assert the visibility of the footer wrapper
    my_page.assert_element_visible(header_locator, "Footer Wrapper")
    # Close the browser
    my_page.close_browser()

if __name__ == "__main__":
    test_title()
