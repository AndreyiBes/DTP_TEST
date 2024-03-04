import re

from playwright.sync_api import sync_playwright
url = 'https://dtp.com.ua'
page_title = 'Автозапчастини з Польщі пошук та підбір по VIN-коду та фото на DTP - Луцьк, Львів, Київ, Харків, Полтава, Вінниця, Тернопіль, Хмельницький, Рівне, Кривий Ріг, Івано-Франківськ, Чернівці, Черкаси, Червоноград, Івано -Франківськ.'

def test_exist_simple():
    with sync_playwright() as p:
            # Відкриваємо браузер
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            # Переходимо на сторінку сайту
            page.goto ( url )
            page.pause ()
            # Перевіряємо що заголовок завантажено
            assert page.title () == page_title
            # Переходимо до поля пошуку та шукаємо необхідний товар
            search_input_selector = '#search-form > div > div > input'
            page.fill ( search_input_selector, 'Фільтр повітряний peugeot 208' )
            page.press ( search_input_selector, "Enter" )
            # Очікуємо результат пошуку
            product_name_selector = '.product-name.col-12.no-padding'
            page.wait_for_selector ( product_name_selector )
            # Циклом перевіряємо що результати пошуку містять усі слова з пошукового запиту
            product_name_elements = page.locator ( product_name_selector ).all ()
            expected_words = "Фільтр повітряний peugeot 208".lower ().split ()
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
            page.pause ()

def test_filter_product_catalog():
    with sync_playwright() as p:
            # Відкриваємо браузер
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            # Повертаємось на головну сторінку
            page.goto(url)
            page.pause()
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
            page.pause()

def test_product_catalog():
    with sync_playwright() as p:
            # Відкриваємо браузер
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            page = browser.new_page()
            # Повертаємось на головну сторінку
            page.goto(url)
            page.pause()
            page.get_by_role ( "link", name = "Peugeot" ).click ()
            product_name_selector = '.product-name'
            page.wait_for_selector ( product_name_selector )
            product_name_elements = page.locator ( product_name_selector ).all ()[:4]
            expected_words = "Peugeot".lower ().split ()
            for element in product_name_elements:
                    element_text = element.text_content ().lower ()
                    assert all ( word in element_text for word in expected_words )
            page.pause ()

def test_order():
        with sync_playwright () as p:
                # Відкриваємо браузер
                browser = p.chromium.launch ( headless = False, slow_mo = 1000 )
                page = browser.new_page ()
                # Переходимо на сторінку сайту
                page.goto ( url )
                page.pause ()
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

                # Перевірка для випадку, коли з'являється вспливаюче вікно
                if page.locator ( "a" ).filter ( has_text = re.compile ( r"^Оформлення$" ) ).count () > 0:
                        # Обробляємо вспливаюче вікно та натискати на "Оформлення"
                        page.locator ( "a" ).filter ( has_text = re.compile ( r"^Оформлення$" ) ).click ()
                        # Почекайте, поки вспливаюче вікно завершиться

                else:
                        # Перевірка для випадку, коли відбувається перенаправлення на нову сторінку
                        page.wait_for_load_state ( "load" )
                        new_page_title = 'Фільтр повітряний peugeot 208'.lower().split()
                        assert all(word in page.title().lower() for word in new_page_title)
                        page.locator("button.btn.buynow").click()
                        assert "Наявність: немає на складі" == page.locator(".db").inner_text()

                page.pause ()
                # page1 = context.new_page ()
                # page1.goto ( "https://dtp.com.ua/checkout/onepage" )
                # page1.get_by_placeholder ( "Прізвище, ім'я, по батькові" ).click ()
                # page1.get_by_placeholder ( "Прізвище, ім'я, по батькові" ).fill ( "Test Test" )
                # page1.get_by_placeholder ( "Прізвище, ім'я, по батькові" ).press ( "Tab" )
                # page1.get_by_placeholder ( "e-mail" ).click ()
                # page1.get_by_placeholder ( "e-mail" ).fill ( "testavb911@gmail.com" )
                # page1.get_by_placeholder ( "+38 (___) ___ - ____" ).click ()
                # page1.get_by_placeholder ( "+38 (___) ___ - ____" ).press ( "ArrowRight" )
                # page1.get_by_placeholder ( "+38 (___) ___ - ____" ).press ( "ArrowRight" )
                # page1.get_by_placeholder ( "+38 (___) ___ - ____" ).fill ( "+38(050)999-999" )
                # page1.get_by_text ( "Накладеним платежем" ).click ()
                # page1.get_by_role ( "option", name = "Накладеним платежем" ).click ()
                # page1.get_by_text ( "Нова пошта" ).click ()
                # page1.get_by_role ( "option", name = "Нова пошта" ).click ()
                # page1.get_by_placeholder ( "Почніть вводити місто" ).click ()
                # page1.get_by_placeholder ( "Почніть вводити місто" ).click ()
                # page1.get_by_placeholder ( "Почніть вводити місто" ).fill ( "Кременчук" )
                # page1.get_by_text ( "місто Кременчук Полтавська область" ).click ()
                # page1.get_by_placeholder ( "Виберіть відділення" ).click ()
                # page1.get_by_placeholder ( "Виберіть відділення" ).fill ( "11" )
                # page1.get_by_text ( "Відділення №11 (до 30" ).click ()
                # page1.locator ( "#checkout div" ).filter ( has_text = "Не телефонувати" ).nth ( 3 ).click ()
                # page1.get_by_role ( "checkbox" ).check ()
                # page1.get_by_role ( "button", name = "Купити" ).click ()
                # page1.get_by_role ( "heading", name = "Дякую за ваше замовлення!" ).click ()
                # page1.get_by_text ( "ідентифікатор вашого замовлення #" ).click ()
                # page1.get_by_role ( "link", name = "Продовжити покупки" ).click ()


#search-form["search"]
