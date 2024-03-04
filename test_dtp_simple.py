import re
from playwright.sync_api import sync_playwright
url = 'https://dtp.com.ua'
page_title = 'Автозапчастини з Польщі пошук та підбір по VIN-коду та фото на DTP - Луцьк, Львів, Київ, Харків, Полтава, Вінниця, Тернопіль, Хмельницький, Рівне, Кривий Ріг, Івано-Франківськ, Чернівці, Черкаси, Червоноград, Івано -Франківськ.'


def create_bug_report(failure_info):
    # Example: You can print the information or log it to a bug tracking system
    print(f"\nТест: '{failure_info['Імя тесту']}' не пройдено, не виконана умова тесту: {failure_info['Помилка тесту']}")

def test_search_bucket_product_available():
    with sync_playwright() as p:
            try:
                    # Відкриваємо браузер
                    browser = p.chromium.launch(headless=False, slow_mo=1000)
                    page = browser.new_page()
                    # Переходимо на сторінку сайту
                    page.goto ( url )
                    # Перевіряємо що заголовок завантажено
                    assert page.title () == page_title
                    # Переходимо до поля пошуку та шукаємо необхідний товар
                    search_input_selector = '#search-form > div > div > input'
                    page.fill ( search_input_selector, 'Фільтр повітряний' )
                    page.press ( search_input_selector, "Enter" )
                    # Очікуємо результат пошуку
                    product_name_selector = '.product-name.col-12.no-padding'
                    page.wait_for_selector ( product_name_selector )
                    # Циклом перевіряємо що результати пошуку містять усі слова з пошукового запиту
                    product_name_elements = page.locator ( product_name_selector ).all ()
                    expected_words = "Фільтр повітряний".lower ().split ()
                    for element in product_name_elements:
                            element_text = element.text_content ().lower ()
                            assert all ( word in element_text for word in expected_words )
                    # Обираємо перший товар з переліку та додаємо його до кошика
                    buy_button_selector = 'button.btn.btn-add-to-cart'
                    page.locator(buy_button_selector).nth(0).click()
                    # Працюємо з вспливаючим віконцем, натискаємо продовжити
                    page.locator ( "a" ).filter ( has_text = re.compile ( r"^Продовжити$" ) ).click ()
                    # Перевіряємо чи товар додано до кошика
                    cart_button_selector = '.mini-cart-content'
                    page.click ( cart_button_selector )
                    cart_item_selector = '.row.small-card-container'
                    assert page.wait_for_selector ( cart_item_selector, timeout = 5000 )
                    # Прибираємо товар з кошика
                    page.locator(".remove-item").click()
                    # Перевіряємо що кошик порожній
                    cart_button_selector = '.mini-cart-content'
                    page.wait_for_selector ( cart_button_selector, timeout = 5000 )
                    page.click ( cart_button_selector )
                    assert "Ваш кошик порожній" in page.locator(".cart-details").nth(0).text_content()
            except Exception as e:
                    # Якщо тест не пройдено, повідомляємо про помилку:
                    failure_info = {
                            "Імя тесту": "test_search_bucket_product_available",
                            "Помилка тесту": str(e),
                    }
                    create_bug_report(failure_info)
                    raise e

def test_filter_product_catalog():
    with sync_playwright() as p:
            try:
                    # Відкриваємо браузер
                    browser = p.chromium.launch(headless=False, slow_mo=1000)
                    page = browser.new_page()
                    # Повертаємось на головну сторінку
                    page.goto(url)
                    # У розділі "Каталог запчастин" обираємо
                    dropdown_selector = '#vs1__combobox'
                    page.click(dropdown_selector)
                    page.get_by_role("option", name="Peugeot").click()
                    page.get_by_role("option", name = "208").click()
                    page.get_by_role("option", name = "i (2012-2019)").click()
                    page.get_by_text("Знайти", exact = True).click()
                    product_name_selector = '.product-name'
                    page.wait_for_selector(product_name_selector)
                    product_name_elements = page.locator(product_name_selector).all()[:4]
                    expected_words = "Peugeot 208".lower().split()
                    for element in product_name_elements:
                            element_text = element.text_content ().lower ()
                            assert all(word in element_text for word in expected_words)
            except Exception as e:
                    # Якщо тест не пройдено, повідомляємо про помилку:
                    failure_info = {
                            "Імя тесту": "test_filter_product_catalog",
                            "Помилка тесту": str(e),
                    }
                    create_bug_report(failure_info)
                    raise e

def test_product_catalog():
    with sync_playwright() as p:
            try:
                    # Відкриваємо браузер
                    browser = p.chromium.launch(headless=False, slow_mo=1000)
                    page = browser.new_page()
                    # Повертаємось на головну сторінку
                    page.goto(url)
                    # Шукаєммо в "Каталог запчастин" обрану марку "Peugeot"
                    page.get_by_role ( "link", name = "Peugeot" ).click ()
                    # Очікуємо результат запиту
                    product_name_selector = '.product-name'
                    page.wait_for_selector ( product_name_selector)
                    # Перевіряємо що у перших 4-х варіантів в найменуванні товару є слово "peugeot"
                    product_name_elements = page.locator ( product_name_selector ).all ()[:10]
                    expected_words = "Peugeot".lower ().split ()
                    for element in product_name_elements:
                            element_text = element.text_content ().lower ()
                            assert all(word in element_text for word in expected_words), f"Assertion failed for element: {element_text}"
            except Exception as e:
                    # Якщо тест не пройдено, повідомляємо про помилку:
                    failure_info = {
                            "Імя тесту": "test_product_catalog",
                            "Помилка тесту": str(e),
                    }
                    create_bug_report(failure_info)
                    raise e

def test_product_not_available():
        with sync_playwright () as p:
                try:
                        # Відкриваємо браузер
                        browser = p.chromium.launch ( headless = False, slow_mo = 1000 )
                        page = browser.new_page ()
                        # Переходимо на сторінку сайту
                        page.goto ( url )
                        # Перевіряємо що заголовок завантажено
                        assert page.title () == page_title
                        # Переходимо до поля пошуку та шукаємо необхідний товар
                        search_input_selector = '#search-form > div > div > input'
                        page.fill ( search_input_selector, 'Фільтр повітряний peugeot 208' )
                        page.press ( search_input_selector, "Enter" )
                        # Очікуємо результат пошуку
                        product_name_selector = '.product-name.col-12.no-padding'
                        page.wait_for_selector ( product_name_selector )
                        # Обираємо перший товар з переліку та додаємо його до кошика
                        buy_button_selector = 'button.btn.btn-add-to-cart'
                        page.locator ( buy_button_selector ).nth ( 0 ).click ()
                        page.wait_for_load_state("load")
                        new_page_title = 'Фільтр повітряний peugeot 208'.lower().split()
                        assert all(word in page.title().lower() for word in new_page_title)
                        page.locator("button.btn.buynow").click()
                        assert "Наявність: немає на складі" == page.locator(".db").nth ( 0 ).inner_text()
                        print(page.locator(".db").nth ( 0 ).inner_text())
                except Exception as e:
                        # Якщо тест не пройдено, повідомляємо про помилку:
                        failure_info = {
                                "Імя тесту": "test_product_not_available",
                                "Помилка тесту": str(e),
                        }
                        create_bug_report(failure_info)
                        raise e

def test_product_available_order():
    with sync_playwright() as p:
            try:
                    # Відкриваємо браузер
                    browser = p.chromium.launch(headless=False, slow_mo=1000)
                    page = browser.new_page()
                    # Переходимо на сторінку сайту
                    page.goto ( url )
                    page.pause()
                    # Перевіряємо що заголовок завантажено
                    assert page.title () == page_title
                    # Переходимо до поля пошуку та шукаємо необхідний товар
                    search_input_selector = '#search-form > div > div > input'
                    page.fill ( search_input_selector, 'Фільтр повітряний' )
                    page.press ( search_input_selector, "Enter" )
                    # Очікуємо результат пошуку
                    buy_button_selector = 'button.btn.btn-add-to-cart'
                    page.locator(buy_button_selector).nth(0).click()
                    # Працюємо з вспливаючим віконцем, натискаємо продовжити
                    page.locator ( "a" ).filter ( has_text = re.compile ( r"^Оформлення$" ) ).click ()
                    page.wait_for_load_state("load")
                    # Заповнюмо анкету для оформлення замовлення
                    page.fill('input[name="billing[first_name]"]', 'Test')
                    page.fill('input[name="billing[email]"]', "test@test.com")
                    page.fill('input[name="billing[phone]"]', "+38(050)999-9999")
                    page.click("#vs1__combobox") #"Накладеним платежем"
                    page.get_by_role("option", name="Накладеним платежем").click()
                    page.click("#vs2__combobox") #"Нова пошта"
                    page.get_by_role("option", name="Нова пошта").click()
                    page.get_by_placeholder("Почніть вводити місто").fill("Кременчук")
                    page.get_by_text("місто Кременчук Полтавська область").click()
                    page.get_by_placeholder("Виберіть відділення").click()
                    page.get_by_placeholder("Виберіть відділення").fill("11")
                    page.get_by_text("Відділення №11 (до 30").click()
            except Exception as e:
                    # Якщо тест не пройдено, повідомляємо про помилку:
                    failure_info = {
                            "Імя тесту": "test_search_bucket_product_available",
                            "Помилка тесту": str(e),
                    }
                    create_bug_report(failure_info)
                    raise e

def test_search_not_vailed():
        with sync_playwright() as p:
                try:
                        # Відкриваємо браузер
                        browser = p.chromium.launch(headless=False, slow_mo=1000)
                        page = browser.new_page()
                        # Переходимо на сторінку сайту
                        page.goto(url)
                        page.pause()
                        # Переходимо до поля пошуку та шукаємо необхідний товар
                        search_input_selector = '#search-form > div > div > input'
                        page.fill ( search_input_selector, 'dfgdfgdfgd' )
                        page.press ( search_input_selector, "Enter" )
                        # Очікуємо результат пошуку
                        product_name_selector = '.search-container.row'
                        page.wait_for_selector ( product_name_selector )
                        expected_text = "Даного товару в Польші немає."
                        element_text = page.locator(product_name_selector).text_content()
                        print(f"\n{element_text}")
                        assert expected_text in element_text, f"Очікуваний '{expected_text}' не знайдено в потрібному елементі"
                except Exception as e:
                    # Якщо тест не пройдено, повідомляємо про помилку:
                    failure_info = {
                            "Імя тесту": "test_search_bucket_product_available",
                            "Помилка тесту": str(e),
                    }
                    create_bug_report(failure_info)
                    raise e
