import re
from oop_dtp import TestPage
url = 'https://dtp.com.ua'
expected_title = 'Автозапчастини з Польщі пошук та підбір по VIN-коду та фото на DTP - Луцьк, Львів, Київ, Харків, Полтава, Вінниця, Тернопіль, Хмельницький, Рівне, Кривий Ріг, Івано-Франківськ, Чернівці, Черкаси, Червоноград, Івано -Франківськ.'

def test_search_bucket_product_available(test_page):
    test_page.check_title(expected_title)
    search_word = 'Фільтр повітряний'
    test_page.search_by_words(search_word)
    test_page.check_search_results(search_word)
    test_page.add_first_product_to_cart()
    test_page.click_continue_in_popup()
    test_page.check_item_added_to_cart()
    test_page.remove_item_from_cart()
    test_page.check_cart_is_empty()

def test_product_not_available(test_page):
    test_page.check_title(expected_title)
    search_word = 'Фільтр повітряний peugeot 208'
    test_page.search_by_words(search_word)
    test_page.check_search_results(search_word)
    test_page.add_first_product_to_cart()
    test_page.check_new_page_title_contains_search_words(search_word)
    test_page.click_item_availability()

def test_product_available_order(test_page):
    test_page.check_title(expected_title)
    search_word = 'Фільтр повітряний'
    test_page.search_by_words(search_word)
    test_page.add_first_product_to_cart()
    test_page.click_and_order_in_popup()
    test_page.fill_order_form()

def test_search_not_valid(test_page):
    test_page.check_title(expected_title)
    search_word = 'dfgdfgdfgd'
    test_page.search_by_words(search_word)
    test_page.item_not_valid()

def test_product_catalog(test_page):
    brand_name = "Peugeot"
    test_page.select_brand_and_wait_for_products(brand_name)
    test_page.check_product_names_contain_words(brand_name)

def test_filter_product_catalog(test_page):
    test_page.select_options_and_click_find()






            test_page.wait_for_selector('.product-name')
            product_name_elements = test_page.locator('.product-name').all()[:4]
            expected_words = "Peugeot 208".lower().split()
            for element in product_name_elements:
                    element_text = element.text_content ().lower ()
                    assert all(word in element_text for word in expected_words)


