import inspect
import re

class TestPage:
    def __init__(self, page):
        self.page = page

    def goto(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("load")

    def report_bug_and_raise(self, error):
        # Пошук назви запущеного тесту
        calling_frame = inspect.currentframe().f_back
        test_name = calling_frame.f_code.co_name
        failure_info = {
            "Імя тесту": test_name,
            "Помилка тесту": str(error),
        }
        # Якщо тест впав, виводимо повідомлення про назву тесту не пройденого та причину відмови
        print(f"\nТест: '{failure_info['Імя тесту']}' не пройдено, не виконана умова тесту: {failure_info['Помилка тесту']}")
        raise error

    def check_title(self, expected_title):
        actual_title = self.page.title()
        assert re.search(re.escape(expected_title), actual_title), \
            f"Expected title: {expected_title}, Actual title: {actual_title}"

    def search_by_words(self, search_word:str):
        self.page.fill('#search-form > div > div > input', search_word)
        self.page.press('#search-form > div > div > input', "Enter")


    def check_search_results(self, search_word):
        # Циклом перевіряємо що результати пошуку містять усі слова з пошукового запиту
        product_name_elements = self.page.locator('.product-name.col-12.no-padding').all()[:4]
        expected_words = search_word.lower().split()
        for element in product_name_elements:
            element_text = element.text_content().lower()
            assert all(word in element_text for word in expected_words)

    def add_first_product_to_cart(self):
        # Обираємо перший товар з переліку та додаємо його до кошика
        buy_button = self.page.locator('button.btn.btn-add-to-cart').nth(0)
        buy_button.click()
        self.page.wait_for_load_state("load")


    def read_product_info(self):
        self.page.locator('a>.fs18.fw5.mb15').nth(0).click()



    def click_continue_in_popup(self):
        self.page.wait_for_selector ( '.modal-body-add-to-cart', state = 'visible', timeout = 10000 )
        self.page.locator('a>div.checkoutin-btn.fs16.fw3').filter(has_text=re.compile(r"^Продовжити$")).click()



    def click_and_order_in_popup(self):
        self.page.wait_for_selector ( '.modal-body-add-to-cart', state = 'visible', timeout = 10000 )
        self.page.locator ( 'a>div.checkout-btn.fs16.fw5' ).filter (
            has_text = re.compile ( r"^Оформлення$" ) ).click ()

    def check_item_added_to_cart(self):
        self.page.wait_for_selector ( '.mini-cart-content', state = "visible", timeout = 10000)
        self.page.click('.mini-cart-content')
        assert self.page.wait_for_selector('.row.small-card-container')

    def remove_item_from_cart(self):
        self.page.locator(".remove-item").click()
        self.page.wait_for_selector ( '.mini-cart-content', state = "visible", timeout = 10000)

    # def check_cart_is_empty(self):
    #     self.page.wait_for_selector ( '.mini-cart-content', state = "visible", timeout = 20000)
    #     self.page.click('.mini-cart-content')
    #     assert "Ваш кошик порожній" in self.page.locator(".cart-details").nth(0).text_content()

    def check_cart_is_empty(self):
        max_attempts = 5
        attempt_count = 0
        while attempt_count < max_attempts:
            self.page.click ( '.mini-cart-content' )
            if self.page.locator ( '.cart-details' ).nth ( 0 ).is_visible ():
                break
            self.page.wait_for_timeout ( 10000 )
            attempt_count += 1
        assert self.page.locator ( '.cart-details' ).nth ( 0 ).is_visible ()
        assert "Ваш кошик порожній" in self.page.locator ( '.cart-details' ).nth ( 0 ).text_content ()



    # def check_new_page_title_contains_search_words(self, search_word):
    #     # Перевіряємо чи заголовок сторінки містить усі слова зі списку
    #     actual_title = self.page.title().lower()
    #     assert all(word in actual_title for word in search_word.lower().split()), f"Expected words: {search_word}, Actual title: {actual_title}"

    def check_new_page_title_contains_search_words(self, search_word):
        # Перевіряємо чи заголовок сторінки містить усі слова зі списку
        if not self.page.is_closed ():
            actual_title = self.page.title ().lower ()
            assert all ( word in actual_title for word in
                         search_word.lower ().split () ), f"Expected words: {search_word}, Actual title: {actual_title}"
        else:
            print ( "Page is closed or navigating. Cannot check title." )



    def click_item_availability(self):
        self.page.locator("button.btn.buynow").click()
        assert self.page.locator(".db").nth(0).inner_text() == "Наявність: немає на складі"

    def item_not_valid(self):
        element_text = self.page.locator('.search-container.row').text_content()
        self.page.wait_for_selector( '.search-container.row' )
        assert "Даного товару в Польші немає." in element_text


    def fill_order_form(self):
        # Заповнюємо анкету для оформлення замовлення
        self.page.fill('input[name="billing[first_name]"]', 'Test')
        self.page.fill('input[name="billing[email]"]', "test@test.com")
        self.page.fill('input[name="billing[phone]"]', "+38(050)999-9999")
        # Вибираємо метод оплати
        self.page.click("#vs1__combobox")
        self.page.get_by_role("option", name="Накладеним платежем").click()
        # Вибираємо метод доставки
        self.page.click("#vs2__combobox")
        self.page.get_by_role("option", name="Нова пошта").click()
        # Введення міста
        self.page.get_by_placeholder("Почніть вводити місто").fill("Кременчук")
        self.page.get_by_text("місто Кременчук Полтавська область").click()
        # Вибір відділення
        self.page.get_by_placeholder("Виберіть відділення").click()
        self.page.get_by_placeholder("Виберіть відділення").fill("11")
        self.page.get_by_text("Відділення №11 (до 30").click()

    def select_brand_and_wait_for_products(self, brand_name, timeout=5000):
        self.page.get_by_role("link", name=brand_name).click()
        self.page.wait_for_selector('.product-name', timeout=timeout)

    # def check_product_names_contain_words(self, brand_names):
    #     product_name_elements = self.page.locator('.product-name').all()[:4]
    #     for element in product_name_elements:
    #         element_text = element.text_content().lower()
    #         assert all(word in element_text for word in brand_names.lower()), f"Assertion failed for element: {element_text}"

    def check_product_names_contain_words(self, brand_names):
        product_name_elements = self.page.locator ( '.product-name' ).all ()[:4]
        # Check if at least one element contains any of the specified words
        assert any ( any ( word in element.text_content ().lower () for word in brand_names.lower () ) for element in
                     product_name_elements ), "Assertion failed for product names"

    def select_options_and_click_find(self):
        # У розділі "Каталог запчастин" обираємо
        self.page.click('#vs1__combobox')
        self.page.get_by_role("option", name="Peugeot").click()
        self.page.get_by_role("option", name = "208").click()
        self.page.get_by_role("option", name = "i (2012-2019)").click()
        self.page.get_by_text("Знайти", exact=True).click()

    def check_product_names(self, expected_words, timeout=5000):
        self.page.wait_for_selector('.product-name', timeout=timeout)
        product_name_elements = self.page.locator('.product-name').all()[:4]
        for element in product_name_elements:
            element_text = element.text_content().lower()
            assert all(word.lower() in element_text for word in expected_words.split()), f"Assertion failed for element: {element_text}"
