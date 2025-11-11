from selenium.webdriver.common.by import By
from .base_page import BasePage


class ContactPage(BasePage):
    # Локаторы элементов формы
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    MESSAGE_TEXTAREA = (By.ID, "message")
    SUBMIT_BUTTON = (By.ID, "submit-button")
    SUCCESS_MESSAGE = (By.ID, "success-message")
    NAME_ERROR = (By.ID, "name-error")
    EMAIL_ERROR = (By.ID, "email-error")
    PHONE_ERROR = (By.ID, "phone-error")
    MESSAGE_ERROR = (By.ID, "message-error")

    def open_contact_page(self, url):
        """Открыть страницу с формой"""
        self.driver.get(url)

    def fill_name(self, name):
        """Заполнить поле имени"""
        self.input_text(self.NAME_INPUT, name)

    def fill_email(self, email):
        """Заполнить поле email"""
        self.input_text(self.EMAIL_INPUT, email)

    def fill_phone(self, phone):
        """Заполнить поле телефона"""
        self.input_text(self.PHONE_INPUT, phone)

    def fill_message(self, message):
        """Заполнить поле сообщения"""
        self.input_text(self.MESSAGE_TEXTAREA, message)

    def submit_form(self):
        """Отправить форму"""
        self.click_element(self.SUBMIT_BUTTON)

    def fill_all_fields(self, name, email, phone, message):
        """Заполнить все поля формы"""
        self.fill_name(name)
        self.fill_email(email)
        self.fill_phone(phone)
        self.fill_message(message)

    # Методы проверки видимости элементов
    def is_success_message_displayed(self):
        """Проверить отображение успешного сообщения"""
        return self.is_element_visible(self.SUCCESS_MESSAGE)

    def is_name_error_displayed(self):
        """Проверить отображение ошибки для поля имени"""
        return self.is_element_visible(self.NAME_ERROR)

    def is_email_error_displayed(self):
        """Проверить отображение ошибки для поля email"""
        return self.is_element_visible(self.EMAIL_ERROR)

    def is_phone_error_displayed(self):
        """Проверить отображение ошибки для поля телефона"""
        return self.is_element_visible(self.PHONE_ERROR)

    def is_message_error_displayed(self):
        """Проверить отображение ошибки для поля сообщения"""
        return self.is_element_visible(self.MESSAGE_ERROR)

    # Методы получения текста
    def get_success_message_text(self):
        """Получить текст успешного сообщения"""
        if self.is_success_message_displayed():
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return ""

    def get_name_error_text(self):
        """Получить текст ошибки для поля имени"""
        if self.is_name_error_displayed():
            return self.get_element_text(self.NAME_ERROR)
        return ""

    def get_email_error_text(self):
        """Получить текст ошибки для поля email"""
        if self.is_email_error_displayed():
            return self.get_element_text(self.EMAIL_ERROR)
        return ""