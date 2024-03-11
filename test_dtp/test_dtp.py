import pytest
url = 'https://dtp.com.ua'
expected_title = 'Автозапчастини з Польщі пошук та підбір по VIN-коду та фото на DTP - Луцьк, Львів, Київ, Харків, Полтава, Вінниця, Тернопіль, Хмельницький, Рівне, Кривий Ріг, Івано-Франківськ, Чернівці, Черкаси, Червоноград, Івано -Франківськ.'


@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_search_bucket_product_available(test_page, browser, headless):
    test_page.check_title(expected_title)
    search_word = 'Фільтр повітряний'
    test_page.search_by_words(search_word)
    test_page.check_search_results(search_word)
    test_page.add_first_product_to_cart()
    test_page.click_continue_in_popup()
    test_page.check_item_added_to_cart()
    test_page.remove_item_from_cart()
    test_page.check_cart_is_empty()

@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_product_not_available(test_page, browser, headless):
    search_word = 'Фільтр повітряний peugeot 208'
    test_page.search_by_words(search_word)
    test_page.read_product_info()
    test_page.check_new_page_title_contains_search_words(search_word)
    test_page.click_item_availability()

@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_product_available_order(test_page, browser, headless):
    search_word = 'Фільтр повітряний'
    test_page.search_by_words(search_word)
    test_page.add_first_product_to_cart()
    test_page.click_and_order_in_popup()
    test_page.fill_order_form()
@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_search_not_valid(test_page, browser, headless):
    search_word = 'dfgdfgdfgd'
    test_page.search_by_words(search_word)
    test_page.item_not_valid()
@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_product_catalog(test_page, browser, headless):
    brand_names = "Peugeot"
    test_page.select_brand_and_wait_for_products(brand_names)
    test_page.check_product_names_contain_words(brand_names)
@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_filter_product_catalog(test_page, browser, headless):
    test_page.select_options_and_click_find()
    test_page.check_product_names("Peugeot 208")
@pytest.mark.parametrize("browser, headless", [('chromium', False), ('firefox', True), ('webkit', False)])
def test_end_to_end(test_page, browser, headless):
    test_page.check_title (expected_title)
    search_word = 'Фільтр повітряний'
    test_page.search_by_words(search_word)
    test_page.check_search_results(search_word)
    test_page.add_first_product_to_cart()
    test_page.click_continue_in_popup()
    test_page.check_item_added_to_cart()
    test_page.remove_item_from_cart()
    test_page.check_cart_is_empty()
    search_word = 'Фільтр повітряний peugeot 208'
    test_page.search_by_words(search_word)
    test_page.read_product_info()
    test_page.check_new_page_title_contains_search_words(search_word)
    test_page.click_item_availability()
    search_word = 'dfgdfgdfgd'
    test_page.search_by_words(search_word)
    test_page.item_not_valid()
    test_page.goto ( url )
    brand_names = "Peugeot"
    test_page.select_brand_and_wait_for_products(brand_names)
    test_page.check_product_names_contain_words(brand_names)
    test_page.goto ( url )
    test_page.select_options_and_click_find()
    test_page.check_product_names("Peugeot 208")
    test_page.goto ( url )
    search_word = 'Фільтр повітряний'
    test_page.search_by_words(search_word)
    test_page.add_first_product_to_cart()
    test_page.click_and_order_in_popup()
    test_page.fill_order_form()




