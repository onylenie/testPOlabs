import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


@pytest.fixture
def driver():
    """Фикстура для инициализации драйвера"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Раскомментируйте для запуска без GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def contact_page(driver):
    """Фикстура для инициализации страницы контактов"""
    from pages.contact_page import ContactPage
    page = ContactPage(driver)

    # Открываем локальную тестовую форму
    current_dir = os.path.dirname(os.path.abspath(__file__))
    form_path = f"file://{current_dir}/test_form.html"
    page.open_contact_page(form_path)

    return page