import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import base64


def test_basic_selenium():
    """Базовый тест Selenium для Lab9 CI/CD"""
    print("Запуск Selenium теста")
    
    # Настройка Chrome в headless режиме
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Простая HTML страница для тестирования
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Lab9 CI/CD Test</title>
        </head>
        <body>
            <h1 id="test-title">Lab9 CI/CD Test</h1>
            <p id="test-text">This is a test page for CI/CD pipeline</p>
            <button id="test-button" onclick="document.getElementById('test-text').textContent='Button Clicked!'">Click Me</button>
        </body>
        </html>
        """
        
        # Создаем data URL
        data_url = f"data:text/html;base64,{base64.b64encode(html_content.encode()).decode()}"
        driver.get(data_url)
        
        # Проверяем элементы на странице
        title = driver.find_element(By.ID, "test-title")
        text = driver.find_element(By.ID, "test-text")
        button = driver.find_element(By.ID, "test-button")
        
        assert title.text == "Lab9 CI/CD Test"
        assert text.text == "This is a test page for CI/CD pipeline"
        
        # Тестируем взаимодействие
        button.click()
        time.sleep(1)
        
        # Проверяем изменение после клика
        assert text.text == "Button Clicked!"
        
        print("Selenium test passed successfully!")
        
    except Exception as e:
        print(f"Selenium test failed: {e}")
        raise
    finally:
        driver.quit()


def test_python_environment():
    """Тест окружения Python"""
    assert 2 + 2 == 4
    assert "hello".upper() == "HELLO"
    print("Python environment test passed!")


def test_imports():
    """Тест импортов библиотек"""
    import selenium
    import pytest
    import webdriver_manager
    print("All imports successful!")
    assert True


def test_ci_cd_workflow():
    """Тест специально для CI/CD workflow"""
    print("CI/CD workflow test executed!")
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
