import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLoginAppCI:

    def setup_method(self):
        """Настройка перед каждым тестом"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Явно указываем путь к chromedriver
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)

        # Путь к HTML файлу внутри папки lab9
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = f"file://{current_dir}/../static/login_app.html"
        self.driver.get(html_file_path)

    def teardown_method(self):
        """Очистка после каждого теста"""
        if self.driver:
            self.driver.quit()

    def test_successful_login_admin(self):
        """Тест успешного входа с логином admin"""
        print("Тестирование успешного входа (admin)...")

        # Ввод валидных данных
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("admin123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        # Ожидание обновления DOM
        self.wait.until(EC.visibility_of_element_located((By.ID, "dashboard")))

        # Проверка успешного входа
        welcome_text = self.driver.find_element(By.ID, "userDisplay").text
        assert welcome_text == "admin", f"Ожидалось 'admin', получено '{welcome_text}'"

        print("✓ Успешный вход admin протестирован")

    def test_successful_login_user(self):
        """Тест успешного входа с логином user"""
        print("Тестирование успешного входа (user)...")

        # Ввод валидных данных
        self.driver.find_element(By.ID, "username").send_keys("user")
        self.driver.find_element(By.ID, "password").send_keys("user123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        # Ожидание обновления DOM
        self.wait.until(EC.visibility_of_element_located((By.ID, "dashboard")))

        # Проверка успешного входа
        welcome_text = self.driver.find_element(By.ID, "userDisplay").text
        assert welcome_text == "user", f"Ожидалось 'user', получено '{welcome_text}'"

        print("✓ Успешный вход user протестирован")

    def test_failed_login_wrong_password(self):
        """Тест неудачного входа (неверный пароль)"""
        print("Тестирование неудачного входа (неверный пароль)...")

        # Ввод невалидных данных
        self.driver.find_element(By.ID, "username").send_keys("admin")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()

        # Проверка сообщения об ошибке
        error_message = self.wait.until(
            EC.visibility_of_element_located((By.ID, "errorMessage"))
        )
        assert error_message.is_displayed()
        assert "Неверный логин или пароль" in error_message.text

        print("✓ Неудачный вход протестирован")

    def test_logout_functionality(self):
        """Тест выхода из системы"""
        print("Тестирование выхода из системы...")

        # Сначала логинимся
        self.driver.find_element(By.ID, "username").send_keys("test")
        self.driver.find_element(By.ID, "password").send_keys("test123")
        self.driver.find_element(By.XPATH, "//button[text()='Войти']").click()
        
        # Ожидаем появления dashboard
        self.wait.until(EC.visibility_of_element_located((By.ID, "dashboard")))

        # Проверяем, что вошли успешно
        welcome_text = self.driver.find_element(By.ID, "userDisplay").text
        assert welcome_text == "test"

        # Нажимаем кнопку выхода
        logout_btn = self.driver.find_element(By.CLASS_NAME, "logout-btn")
        logout_btn.click()

        # Проверяем, что вернулись к форме логина
        login_form = self.wait.until(
            EC.visibility_of_element_located((By.ID, "loginForm"))
        )
        assert login_form.is_displayed()

        print("✓ Выход из системы протестирован")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
