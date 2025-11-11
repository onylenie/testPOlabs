from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Инициализация Chrome браузера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Открытие страницы
    driver.get("https://www.saucedemo.com/")
    print("Страница успешно открыта")
    print(f"Заголовок страницы: {driver.title}")

    # Небольшая пауза, чтобы увидеть результат
    import time

    time.sleep(3)

finally:
    # Закрытие браузера
    driver.quit()
    print("Браузер закрыт")
