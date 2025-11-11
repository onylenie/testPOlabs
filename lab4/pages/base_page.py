from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, locator):
        """Найти элемент с ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable_element(self, locator):
        """Найти кликабельный элемент"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_element_visible(self, locator):
        """Проверить видимость элемента (имеет класс 'show')"""
        try:
            element = self.find_element(locator)
            # Простая проверка - элемент имеет класс 'show'
            return 'show' in element.get_attribute('class')
        except TimeoutException:
            return False

    def get_element_text(self, locator):
        """Получить текст элемента"""
        return self.find_element(locator).text

    def click_element(self, locator):
        """Кликнуть по элементу"""
        self.find_clickable_element(locator).click()

    def input_text(self, locator, text):
        """Ввести текст в поле"""
        element = self.find_clickable_element(locator)
        element.clear()
        element.send_keys(text)