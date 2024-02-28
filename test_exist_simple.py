from playwright.sync_api import sync_playwright
url = 'https://exist.ua'

def test_exist_simple():
    with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=200)
            page = browser.new_page()
            page.goto(url)
            page.pause()
            office_selector = "#headerOffices"
            page.locator(office_selector).click()
            placeholder = 'Оберіть населений пункт'
            office_name = "Кременчук, Полтавська область"
            page.fill(f'input[placeholder="{placeholder}"]', office_name)

            # Find the button with aria-label "Кременчук"
            button_selector = 'button[aria-label="Вибрати"]'
            page.locator(button_selector).click()
            page.wait_for_selector(button_selector)
            page.click(button_selector)
            # Click on the element with class "OfficesListstyle__OfficeSelectButton-sc-105r2v6-3"
            select_button_selector = '.OfficesListstyle__OfficeSelectButton-sc-105r2v6-3'
            page.wait_for_selector(select_button_selector)
            page.click(select_button_selector)

