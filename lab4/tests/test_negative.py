import pytest
from faker import Faker
import time
from selenium.webdriver.common.by import By


class TestNegativeScenario:
    """Тесты негативных сценариев"""

    def test_submit_form_with_empty_required_field(self, contact_page):
        """
        Негативный тест: попытка отправить форму с пустым обязательным полем
        и проверка текста ошибки
        """
        fake = Faker()

        # Генерация тестовых данных с пустым обязательным полем (name)
        test_data = {
            'name': '',  # Пустое обязательное поле
            'email': fake.email(),
            'phone': '+79123456789',
            'message': fake.text(max_nb_chars=100)[:100]
        }

        # Заполнение всех полей, кроме обязательного
        contact_page.fill_all_fields(
            test_data['name'],  # Пустое поле
            test_data['email'],
            test_data['phone'],
            test_data['message']
        )

        # Отправка формы
        contact_page.submit_form()

        # Ждем завершения валидации
        time.sleep(2)

        # Детальная отладочная информация
        print(f"\n=== ДЕТАЛЬНАЯ ОТЛАДОЧНАЯ ИНФОРМАЦИЯ (пустое имя) ===")

        elements_to_check = [
            ('success-message', contact_page.is_success_message_displayed()),
            ('name-error', contact_page.is_name_error_displayed()),
            ('email-error', contact_page.is_email_error_displayed()),
            ('message-error', contact_page.is_message_error_displayed())
        ]

        for element_id, is_visible in elements_to_check:
            try:
                element = contact_page.driver.find_element(By.ID, element_id)
                classes = element.get_attribute('class')
                text = element.text
                print(f"Элемент {element_id}: visible={is_visible}, classes='{classes}', text='{text}'")
            except Exception as e:
                print(f"Элемент {element_id}: ОШИБКА - {e}")

        print(f"==================\n")

        # Проверка, что успешное сообщение НЕ отображается
        assert not contact_page.is_success_message_displayed(), \
            "Сообщение об успехе отображается при ошибке валидации"

        # Проверка отображения сообщения об ошибке для поля имени
        assert contact_page.is_name_error_displayed(), \
            "Сообщение об ошибке для поля имени не отображается"

        # Проверка текста ошибки для обязательного поля
        error_text = contact_page.get_name_error_text()
        expected_error_keywords = ["обязательно", "заполнения"]

        # Проверка, что текст ошибки содержит ожидаемые ключевые слова
        assert any(keyword in error_text.lower() for keyword in expected_error_keywords), \
            f"Текст ошибки не соответствует ожиданиям: '{error_text}'"

    def test_submit_form_with_invalid_email(self, contact_page):
        """Дополнительный негативный тест: невалидный email"""
        fake = Faker()

        test_data = {
            'name': fake.name()[:30],
            'email': 'invalid-email',  # Невалидный email
            'phone': '+79123456789',
            'message': fake.text(max_nb_chars=100)[:100]
        }

        contact_page.fill_all_fields(**test_data)
        contact_page.submit_form()

        # Ждем завершения валидации
        time.sleep(2)

        # Отладочная информация
        print(f"\n=== ДЕТАЛЬНАЯ ОТЛАДОЧНАЯ ИНФОРМАЦИЯ (невалидный email) ===")
        print(f"Email error displayed: {contact_page.is_email_error_displayed()}")
        print(f"Email error text: '{contact_page.get_email_error_text()}'")
        print(f"==================\n")

        # Проверка ошибки для email
        assert not contact_page.is_success_message_displayed(), \
            "Сообщение об успехе отображается при невалидном email"

        assert contact_page.is_email_error_displayed(), \
            "Сообщение об ошибке email не отображается"

        email_error_text = contact_page.get_email_error_text()
        expected_email_error_keywords = ["email", "корректный", "адрес"]

        assert any(keyword in email_error_text.lower() for keyword in expected_email_error_keywords), \
            f"Текст ошибки email не соответствует ожиданиям: '{email_error_text}'"

    def test_submit_form_with_short_message(self, contact_page):
        """Тест: пустое сообщение"""
        fake = Faker()

        test_data = {
            'name': fake.name()[:30],
            'email': fake.email(),
            'phone': '+79123456789',
            'message': ''  # Пустое сообщение
        }

        contact_page.fill_all_fields(**test_data)
        contact_page.submit_form()

        # Ждем завершения валидации
        time.sleep(2)

        # Проверка ошибки для сообщения
        assert not contact_page.is_success_message_displayed()
        assert contact_page.is_message_error_displayed()

    def test_submit_completely_empty_form(self, contact_page):
        """Тест: отправка полностью пустой формы"""
        test_data = {
            'name': '',
            'email': '',
            'phone': '',
            'message': ''
        }

        contact_page.fill_all_fields(**test_data)
        contact_page.submit_form()

        # Ждем завершения валидации
        time.sleep(2)

        # Проверка, что успешное сообщение НЕ отображается
        assert not contact_page.is_success_message_displayed()

        # Должны быть ошибки для всех обязательных полей
        assert contact_page.is_name_error_displayed()
        assert contact_page.is_email_error_displayed()
        assert contact_page.is_message_error_displayed()