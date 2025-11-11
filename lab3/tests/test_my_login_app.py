import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestMyLoginApp:

    def setup_method(self):
        """Настройка перед каждым тестом"""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

        # Путь к вашему HTML файлу
        html_file_path = "file:///D:/Users/Павел/Desktop/Институт(7)/Тест%20ПО/lab3/login_app.html"
        self.driver.get(html_file_path)

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.driver.quit()

    def test_successful_login_admin(self):
        """Тест успешного входа с логином admin"""
        print("Тестирование успешного входа (admin)...")

        # Ввод валидных данных
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        # Ждем обновления DOM
        time.sleep(2)

        # Проверка успешного входа
        welcome_text = self.driver.find_element(By.ID, "userDisplay").text
        assert welcome_text == "admin", f"Ожидалось 'admin', получено '{welcome_text}'"

        # Проверка, что dashboard отображается
        dashboard = self.driver.find_element(By.ID, "dashboard")
        assert dashboard.is_displayed()

        # Проверка, что форма логина скрыта
        login_form = self.driver.find_element(By.ID, "loginForm")
        assert login_form.get_attribute("style") == "display: none;"

        # Кнопка выхода должна быть видна в dashboard
        logout_btn = self.driver.find_element(By.CLASS_NAME, "logout-btn")
        assert logout_btn.is_displayed()

        print("✓ Успешный вход протестирован")

    def test_successful_login_user(self):
        """Тест успешного входа с логином user"""
        print("Тестирование успешного входа (user)...")

        # Ввод валидных данных
        self.driver.find_element(By.ID, "username").send_keys("user")
        self.driver.find_element(By.ID, "password").send_keys("user123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        time.sleep(2)

        # Проверка успешного входа
        welcome_text = self.driver.find_element(By.ID, "userDisplay").text
        assert welcome_text == "user", f"Ожидалось 'user', получено '{welcome_text}'"

        # Проверка, что dashboard отображается
        dashboard = self.driver.find_element(By.ID, "dashboard")
        assert dashboard.is_displayed()

        print("✓ Успешный вход user протестирован")

    def test_failed_login_wrong_password(self):
        """Тест неудачного входа (неверный пароль)"""
        print("Тестирование неудачного входа (неверный пароль)...")

        # Ввод невалидных данных
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        time.sleep(2)

        # Проверка сообщения об ошибке
        error_message = self.driver.find_element(By.ID, "errorMessage")
        assert error_message.is_displayed()
        assert "Неверный логин или пароль" in error_message.text

        # Проверка, что форма логина все еще видна
        login_form = self.driver.find_element(By.ID, "loginForm")
        assert login_form.is_displayed()

        print("✓ Неудачный вход протестирован")

    def test_failed_login_wrong_username(self):
        """Тест неудачного входа (неверный логин)"""
        print("Тестирование неудачного входа (неверный логин)...")

        # Ввод невалидных данных
        self.driver.find_element(By.ID, "username").send_keys("unknownuser")
        self.driver.find_element(By.ID, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        time.sleep(2)

        # Проверка сообщения об ошибке
        error_message = self.driver.find_element(By.ID, "errorMessage")
        assert error_message.is_displayed()
        assert "Неверный логин или пароль" in error_message.text

        print("✓ Неудачный вход с неверным логином протестирован")

    def test_logout_functionality(self):
        """Тест выхода из системы"""
        print("Тестирование выхода из системы...")

        # Сначала логинимся
        self.driver.find_element(By.ID, "username").send_keys("test")
        self.driver.find_element(By.ID, "password").send_keys("test123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        time.sleep(2)

        # Проверяем, что вошли успешно
        welcome_text = self.driver.find_element(By.ID, "userDisplay").text
        assert welcome_text == "test"

        # Проверяем, что dashboard отображается
        dashboard = self.driver.find_element(By.ID, "dashboard")
        assert dashboard.is_displayed()

        # Нажимаем кнопку выхода (она уже видна в dashboard)
        logout_btn = self.driver.find_element(By.CLASS_NAME, "logout-btn")
        assert logout_btn.is_displayed()
        logout_btn.click()

        time.sleep(2)

        # Проверяем, что вернулись к форме логина
        login_form = self.driver.find_element(By.ID, "loginForm")
        assert login_form.is_displayed()

        # Проверяем, что поля очищены
        username_field = self.driver.find_element(By.ID, "username")
        password_field = self.driver.find_element(By.ID, "password")
        assert username_field.get_attribute("value") == ""
        assert password_field.get_attribute("value") == ""

        print("✓ Выход из системы протестирован")


# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])