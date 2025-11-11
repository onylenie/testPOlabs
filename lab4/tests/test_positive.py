import pytest
from faker import Faker
import time


class TestPositiveScenario:
    """Тесты позитивных сценариев"""

    def test_submit_form_with_valid_data(self, contact_page):
        """
        Позитивный тест: заполнение всех полей формы валидными данными,
        отправка и проверка успешного сообщения
        """
        # Инициализация Faker для генерации тестовых данных
        fake = Faker()

        # Генерация валидных тестовых данных
        test_data = {
            'name': fake.name()[:30],
            'email': fake.email(),
            'phone': '+79123456789',
            'message': fake.text(max_nb_chars=100)[:100]
        }

        # Заполнение всех полей формы
        contact_page.fill_all_fields(
            test_data['name'],
            test_data['email'],
            test_data['phone'],
            test_data['message']
        )

        # Отправка формы
        contact_page.submit_form()

        # Ждем завершения валидации
        time.sleep(2)

        # Проверка успешного сообщения
        assert contact_page.is_success_message_displayed(), \
            "Сообщение об успехе не отображается"

        success_text = contact_page.get_success_message_text()
        expected_keywords = ["успешно", "спасибо"]

        # Проверка, что текст сообщения содержит ожидаемые ключевые слова
        assert any(keyword in success_text.lower() for keyword in expected_keywords), \
            f"Текст успешного сообщения не соответствует ожиданиям: {success_text}"